"""Lecture de SUIVI.md, des fiches et des rapports ; état des unités ; appels Git.

Module partagé par outil.py, travail.py, generation.py et tableau.py. Bibliothèque standard seulement.
"""
import datetime
import pathlib
import re
import subprocess
from collections import OrderedDict

RACINE = pathlib.Path(__file__).resolve().parent.parent
DEPOT = "francoisduperier167-jpg/GODOT_DEV_MAPPER"
IA_NOMS = {1: "IA 1", 2: "IA 2", 3: "IA 3"}
IA_ROLES = {1: "conception", 2: "développement", 3: "vérification"}
ABANDON_H = 20     # sans activité datée depuis 20 h (plus que l'écart, nuit comprise, entre deux créneaux d'une IA) : reprise par une autre IA
RELAIS_H = 12      # prête, à vérifier ou à fusionner depuis 12 h : une autre IA peut la prendre
VERROU_MIN = 45    # verrou de main plus vieux : périmé
REF_VERROU = "refs/heads/verrou/main"

RE_SECTION = re.compile(r"^## (.+)$")
RE_PISTE = re.compile(r"^### Piste (\S+) · (.+?)(?: — (.+))?$")
RE_RDV = re.compile(r"^### Rendez-vous(?: (.+?))?(?: — (.+))?$")
RE_LIGNE = re.compile(r"^- \[( |x)\] \*\*(S\d\d(?:\.[0-9A-Za-z]+)?)\*\* · (.*?) · réalise IA ([123]) · vérifie IA ([123]) · après (.*?) · fiche `(suivi/[^`]+)`(.*)$")
RE_FAIT = re.compile(r"fait le (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) UTC")
RE_ETAPE = re.compile(r"^- \[( |x)\] ((?:Rc|R|V|F)\d+(?:\.\d+)?) (.*)$")
RE_SIGNE = re.compile(r" — IA ([123]) · (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) UTC(?: · (ACCEPTÉE|REFUSÉE))?$")
RE_SATELLITE = re.compile(r"^S\d\d\.(\d+|c\d+)$")
RE_REPRISE = re.compile(r"(?m)^\W*Reprise\s*:\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) UTC(?: par IA ([123]))?")
RE_LEVEE = re.compile(r"(?m)^- Arrêt levé\s*:\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) UTC")
RE_AJOUTEE = re.compile(r"ajoutée le (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) UTC")
TENTATIVES_PRECEDENTES = "\n## Tentatives précédentes"



def maintenant():
    return datetime.datetime.now(datetime.timezone.utc)


def horodatage(t=None):
    return (t or maintenant()).strftime("%Y-%m-%d %H:%M")


def lire_date(s):
    return datetime.datetime.strptime(s, "%Y-%m-%d %H:%M").replace(tzinfo=datetime.timezone.utc)


# ---------------------------------------------------------------- SUIVI.md

def lire_suivi(texte):
    """Sections, groupes (pistes et rendez-vous) et unités, dans l'ordre du fichier."""
    sections, unites = [], OrderedDict()
    sec = grp = None
    for no, l in enumerate(texte.splitlines(), 1):
        m = RE_SECTION.match(l)
        if m:
            sec = dict(titre=m.group(1).strip(), groupes=[])
            sections.append(sec)
            grp = None
            continue
        m = RE_PISTE.match(l)
        if m and sec is not None:
            grp = dict(type="piste", id=m.group(1), nom=m.group(2).strip(), note=(m.group(3) or "").strip(), unites=[], ligne=no)
            sec["groupes"].append(grp)
            continue
        m = RE_RDV.match(l)
        if m and sec is not None:
            grp = dict(type="rdv", id="RDV-" + str(len(sections)), nom=(m.group(1) or "").strip(), note=(m.group(2) or "").strip(), unites=[], ligne=no)
            sec["groupes"].append(grp)
            continue
        if l.startswith("### "):
            grp = None
            continue
        m = RE_LIGNE.match(l)
        if m:
            coche, uid, titre, r, v, apres, fiche, suite = m.groups()
            dep = [] if apres.strip() == "—" else [x.strip() for x in apres.split(",")]
            f = RE_FAIT.search(suite)
            a = RE_AJOUTEE.search(suite)
            unites[uid] = dict(id=uid, coche=coche == "x", titre=titre, r=int(r), v=int(v), apres=dep, fiche=fiche,
                               suite=suite, fait=f.group(1) if f else None, ajoutee=a.group(1) if a else None, ligne=no,
                               section=sec["titre"] if sec else None, groupe=grp["id"] if grp else None)
            if grp is not None:
                grp["unites"].append(uid)
    return dict(sections=sections, unites=unites)


def deps_reelles(S, uid):
    """Prérequis d'une unité, « Sxx.* » développé en tâches et corrections de la phase."""
    ids = S["unites"]
    out = []
    for d in ids[uid]["apres"]:
        if d.endswith(".*"):
            b = d[:-2]
            out += [x for x in ids if x.startswith(b + ".") and x != b + ".P"]
        else:
            out.append(d)
    return out


def prerequis_manquants(S, uid):
    return [d for d in deps_reelles(S, uid) if d not in S["unites"] or not S["unites"][d]["coche"]]


def pret_depuis(S, uid):
    """Date à laquelle l'unité est devenue prête : fusion de son dernier prérequis, ou, pour une unité de
    correction, « ajoutée le … » écrit sur sa ligne par `correction`. None sinon : S01 attend IA 1, sans relais."""
    u = S["unites"][uid]
    dates = [S["unites"][d]["fait"] for d in deps_reelles(S, uid) if d in S["unites"] and S["unites"][d]["fait"]]
    if dates:
        return lire_date(max(dates))
    return lire_date(u["ajoutee"]) if u.get("ajoutee") else None


def branche_de(u):
    return "tache/" + pathlib.Path(u["fiche"]).stem


def stem_de(u):
    return pathlib.Path(u["fiche"]).stem


# ---------------------------------------------------------------- fiches

def lire_etapes(texte):
    """Sous-étapes à cocher d'une fiche : id, groupe R, V ou F, case, texte, signature."""
    out = []
    for no, l in enumerate(texte.splitlines(), 1):
        m = RE_ETAPE.match(l)
        if not m:
            continue
        coche, eid, reste = m.groups()
        s = RE_SIGNE.search(reste)
        texte_seul = reste[: s.start()] if s else reste
        texte_seul = texte_seul.split(" ⟶ ")[0]
        out.append(dict(id=eid, g="R" if eid.startswith("R") else eid[0], coche=coche == "x", texte=texte_seul.strip(),
                        ia=int(s.group(1)) if s else None, date=s.group(2) if s else None,
                        verdict=s.group(3) if s else None, ligne=no))
    return out


def derniere_activite(etapes, *autres):
    """Date la plus récente parmi les signatures des cases et les lignes « Reprise » du rapport et du verdict."""
    dates = [e["date"] for e in etapes if e["date"]]
    for a in autres:
        dates += (a or {}).get("reprises", [])
    return lire_date(max(dates)) if dates else None


def dernier_acteur(etapes, *autres):
    """(date, IA) de la dernière activité signée : case cochée, ou ligne « Reprise … par IA n ». (None, None) sinon."""
    l = [(e["date"], e["ia"]) for e in etapes if e["date"] and e["ia"]]
    for a in autres:
        l += (a or {}).get("acteurs", [])
    if not l:
        return None, None
    d, ia = max(l)
    return lire_date(d), ia


def signer_ligne(ligne, ia, verdict=None, t=None):
    ligne = ligne.replace("- [ ]", "- [x]", 1)
    return ligne + f" — IA {ia} · {horodatage(t)} UTC" + (f" · {verdict}" if verdict else "")


def decocher_ligne(ligne):
    ligne = ligne.replace("- [x]", "- [ ]", 1)
    return RE_SIGNE.sub("", ligne)


# ---------------------------------------------------------------- rapports

def lire_rapport(texte):
    """Champs de la tentative en cours : la partie « ## Tentatives précédentes » (porte rejouée) n'est jamais lue.
    Refus et escalades se comptent depuis la dernière ligne « Arrêt levé » écrite par `lever`."""
    r = dict(statut=None, auteurs=[], tentative=1, creneaux=0, reprises=[], acteurs=[], escalades=0, refus=0, decision=None, levee=None)
    if not texte:
        return r
    texte = texte.split(TENTATIVES_PRECEDENTES)[0]
    m = re.search(r"(?m)^\W*Statut\s*:\s*([A-ZÉ]+)", texte)
    if m:
        r["statut"] = m.group(1)
    m = re.search(r"(?m)^\W*Auteurs?\s*:\s*(.*)$", texte)
    if m:
        r["auteurs"] = [int(x) for x in re.findall(r"IA ([123])", m.group(1))]
    m = re.search(r"(?m)^\W*Tentative\s*:\s*(\d+)", texte)
    if m:
        r["tentative"] = int(m.group(1))
    m = re.search(r"(?m)^\W*Créneaux utilisés\s*:\s*(\d+)", texte)
    if m:
        r["creneaux"] = int(m.group(1))
    r["reprises"] = [d for d, _ in RE_REPRISE.findall(texte)]
    r["acteurs"] = [(d, int(i)) for d, i in RE_REPRISE.findall(texte) if i]
    lev = RE_LEVEE.findall(texte)
    r["levee"] = max(lev) if lev else None
    apres = texte[max(m.end() for m in RE_LEVEE.finditer(texte)):] if lev else texte
    r["escalades"] = len(re.findall(r"(?m)^\W*Reprise\s*:.*\bESCALADE\b", apres)) + (r["statut"] == "ESCALADE")
    r["refus"] = len(re.findall(r"(?m)^\W*Reprise\s*:.*\(état : Refusée", apres))
    m = re.search(r"(?m)^\W*Décision\s*:\s*(PASSER|CORRIGER D['’]ABORD)", texte)
    if m:
        r["decision"] = "PASSER" if m.group(1) == "PASSER" else "CORRIGER D'ABORD"
    return r


def lire_verdict(texte):
    v = dict(verdict=None, verificateur=None, reprises=[], acteurs=[])
    if not texte:
        return v
    m = re.search(r"(?m)^\W*Verdict\s*:\s*(EN COURS|ACCEPTÉE|REFUSÉE)", texte)
    if m:
        v["verdict"] = m.group(1)
    m = re.search(r"(?m)^\W*Vérificateur\s*:\s*IA ([123])", texte)
    if m:
        v["verificateur"] = int(m.group(1))
    v["reprises"] = [d for d, _ in RE_REPRISE.findall(texte)]
    v["acteurs"] = [(d, int(i)) for d, i in RE_REPRISE.findall(texte) if i]
    return v


def est_porte(u):
    return u["titre"].startswith("Porte")


def resolveur(rap):
    """IA qui traite une QUESTION ou une ESCALADE : IA 1, ou IA 3 si IA 1 est auteur (§3)."""
    return 3 if 1 in rap["auteurs"] else 1


def arret_requis(etat, rap):
    """Raison d'un arrêt obligatoire n° 2 (§5) que l'état de l'unité impose, ou None. Les refus et les escalades
    se comptent depuis le dernier « Arrêt levé » ; après une levée, les cas de trois auteurs restent à la décision
    écrite par l'humain et ne redéclenchent pas l'arrêt."""
    if etat == "refusee" and rap["refus"] + 1 >= 3:
        return f"refusée trois fois (tentative {rap['tentative']})"
    if etat == "bloquee" and rap["escalades"] >= 2:
        return "passée deux fois en ESCALADE"
    if rap.get("levee"):
        return None
    if etat == "bloquee" and resolveur(rap) not in rap["auteurs"] and len(rap["auteurs"]) >= 2:
        return f"{rap['statut']} à traiter par IA {resolveur(rap)}, qui serait la troisième IA auteur : plus personne ne pourrait la vérifier"
    if len(set(rap["auteurs"])) >= 3:
        return "les trois IA sont auteurs : plus personne ne peut la vérifier"
    return None


# ---------------------------------------------------------------- état d'une unité

LIBELLES = {
    "faite": "Faite", "prete": "Prête", "attente": "En attente", "en_cours": "En cours", "abandonnee": "Abandonnée",
    "a_verifier": "À vérifier", "en_verification": "En vérification", "verif_abandonnee": "Vérification abandonnée",
    "refusee": "Refusée", "a_fusionner": "À fusionner", "bloquee": "Bloquée",
}


def carres(etapes, faite):
    """Cinq carrés : prise en charge, réalisation, contrôles et rapport, vérification, fusion (de 0 à 1 chacun)."""
    if faite:
        return [1.0] * 5
    R = [e for e in etapes if e["g"] == "R"]
    V = [e for e in etapes if e["g"] == "V"]
    F = [e for e in etapes if e["g"] == "F"]
    if not R:
        return [0.0] * 5
    mid = R[1:-1]
    c1 = 1.0 if R[0]["coche"] else 0.0
    c3 = 1.0 if R[-1]["coche"] else 0.0
    c2 = sum(e["coche"] for e in mid) / len(mid) if mid else c3
    c4 = sum(e["coche"] for e in V) / len(V) if V else c3
    c5 = sum(e["coche"] for e in F) / len(F) if F else 0.0
    return [c1, c2, c3, c4, c5]


def carres_unite(S, uid, etapes, branche):
    """Sans branche, une unité non faite n'a rien d'engagé : ses cases sur main datent d'une tentative close."""
    if S["unites"][uid]["coche"]:
        return [1.0] * 5
    return carres(etapes, False) if branche else [0.0] * 5


def etat_unite(S, uid, etapes, rapport, branche, t=None, verdict=None):
    """Code d'état, selon docs/construction/sequence.md §3. L'activité est la date la plus récente des signatures
    et des lignes « Reprise » du rapport et du verdict : une reprise remet le compteur d'abandon à zéro."""
    t = t or maintenant()
    u = S["unites"][uid]
    if u["coche"]:
        return "faite"
    if not branche:
        return "attente" if prerequis_manquants(S, uid) else "prete"
    if rapport.get("statut") in ("QUESTION", "ESCALADE"):
        return "bloquee"
    R = [e for e in etapes if e["g"] == "R"]
    V = [e for e in etapes if e["g"] == "V"]
    act = derniere_activite(etapes, rapport, verdict)
    vieux = act is not None and (t - act).total_seconds() > ABANDON_H * 3600
    if V and V[-1]["coche"]:
        return "refusee" if V[-1]["verdict"] == "REFUSÉE" else "a_fusionner"
    if V and V[0]["coche"]:
        return "verif_abandonnee" if vieux else "en_verification"
    if R and R[-1]["coche"]:
        return "a_verifier"
    return "abandonnee" if vieux else "en_cours"


# ---------------------------------------------------------------- Git

def git(*args, cwd=None, check=True, entree=None, env=None):
    p = subprocess.run(["git", *args], cwd=str(cwd or RACINE), capture_output=True, text=True, input=entree, env=env)
    if check and p.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} a échoué ({p.returncode}) :\n{p.stderr.strip()}")
    return p


def git_sortie(*args, cwd=None):
    return git(*args, cwd=cwd).stdout.strip()


def fetch(cwd=None):
    git("fetch", "--quiet", "--prune", "origin", cwd=cwd, check=False)


def branches_distantes(cwd=None):
    """{nom: sha} des branches de origin, d'après les références distantes locales (après fetch)."""
    out = git_sortie("for-each-ref", "--format=%(refname:strip=3) %(objectname)", "refs/remotes/origin", cwd=cwd)
    d = {}
    for l in out.splitlines():
        if " " in l:
            n, s = l.split(" ", 1)
            if n != "HEAD":
                d[n] = s
    return d


def montrer(ref, chemin, cwd=None):
    p = git("show", f"{ref}:{chemin}", cwd=cwd, check=False)
    return p.stdout if p.returncode == 0 else None


def racine_travail(cwd=None):
    return pathlib.Path(git_sortie("rev-parse", "--show-toplevel", cwd=cwd))


# ---------------------------------------------------------------- fiche de correction

def fiche_correction(cid, porte, fautive, titre, realise, verifie):
    """Fiche d'une unité de correction demandée par une porte KO."""
    stem = f"{cid}-correction"
    br = f"tache/{stem}"
    return f"""# {cid} — Correction demandée par la porte {porte}

> Fiche créée par `python3 suivi/outil.py correction` quand un point de contrôle de la porte {porte} est KO. Chaque case se coche avec `python3 suivi/outil.py cocher {cid} <sous-étape> --ia <n>`, juste après la sous-étape : la commande signe la case (IA, date, heure), commite et pousse.

| Champ | Valeur |
| --- | --- |
| Réalise | IA {realise} ({IA_ROLES[realise]}) |
| Vérifie | IA {verifie} ({IA_ROLES[verifie]}), jamais un auteur de l'unité |
| Piste | celle de la porte {porte}, juste avant elle |
| Commence après | rien : peut commencer tout de suite |
| Branche | `{br}` |
| Unité fautive | {fautive} |
| Correction | {titre} |

## Ce qu'il faut faire

- Corriger le défaut relevé par la porte {porte} (voir `rapports/{porte}.md`), dans les fichiers autorisés de l'unité fautive {fautive}.
- Rejouer les contrôles de l'unité fautive, puis le point de contrôle KO de la porte.

## Fichiers autorisés

Les fichiers autorisés de la fiche de {fautive}. Toujours autorisés en plus : `rapports/{cid}*.md` et les cases de cette fiche.

## Prompt de réalisation

```text
Tu corriges le défaut relevé par la porte {porte} du projet GODOT_DEV_MAPPER. Réalisation prévue : IA {realise}. Ton numéro d'IA est celui du prompt de créneau.
1. python3 suivi/outil.py prendre {cid} --ia <n>   (code non nul : l'unité n'est pas pour toi maintenant)
2. Lis rapports/{porte}.md (point KO, correction attendue) et la fiche de {fautive} dans suivi/ : ses règles, son bloc GODOT, ses fichiers autorisés et ses contrôles s'appliquent.
3. Fais la plus petite correction qui rend le point OK sans affaiblir aucun test. Colle les sorties des contrôles dans rapports/{cid}.md.
TRACE OBLIGATOIRE : après chaque sous-étape, git add des fichiers de la sous-étape, puis python3 suivi/outil.py cocher {cid} <sous-étape> --ia <n>. Une sous-étape non cochée par cette commande est considérée comme non faite.
```

## Sous-étapes de réalisation

- [ ] R0 Prise en charge par `prendre` : branche `{br}`, rapport « EN COURS » ⟶ cochée par `prendre`
- [ ] R1 Cause du point KO établie et écrite dans le rapport ⟶ cocher {cid} R1
- [ ] R2 Correction faite dans les fichiers autorisés de {fautive} ⟶ cocher {cid} R2
- [ ] R3 Contrôles de {fautive} et point KO de la porte rejoués → OK, sorties collées ; « Statut : TERMINÉ » ⟶ cocher {cid} R3

## Prompt de vérification

```text
Tu vérifies la correction {cid} du projet GODOT_DEV_MAPPER. Vérification prévue : IA {verifie}. Tu n'es jamais un auteur de l'unité.
1. python3 suivi/outil.py prendre {cid} --ia <n> --verification, puis cd dans la copie neuve indiquée.
2. Périmètre : fichiers de {fautive} seulement. Relance les contrôles de {fautive} et le point KO de la porte {porte}.
3. Verdict dans rapports/{cid}-verif-<tentative>.md ; dernière case : cocher {cid} V4 --ia <n> --verdict ACCEPTÉE (ou REFUSÉE).
4. Si ACCEPTÉE : depuis ton clone principal, python3 suivi/outil.py fusionner {cid} --ia <n> (Godot : la commande le trouve seule, par --godot, $GODOT, le cache du bloc GODOT ou tools/ci/fetch_godot.sh), puis, dans la copie de fusion, les cases F, puis python3 suivi/outil.py publier {cid} --ia <n>. La porte {porte} redevient alors disponible : elle sera rejouée.
TRACE OBLIGATOIRE : python3 suivi/outil.py cocher {cid} <sous-étape> --ia <n> après chaque sous-étape.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge par `prendre --verification` : pas un auteur ; copie neuve ⟶ cochée par `prendre`
- [ ] V2 Périmètre : fichiers de {fautive} seulement ⟶ cocher {cid} V2
- [ ] V3 Contrôles relancés ; point KO de la porte OK ⟶ cocher {cid} V3
- [ ] V4 Verdict écrit dans `rapports/{cid}-verif-<tentative>.md` ⟶ cocher {cid} V4 --verdict ACCEPTÉE ou REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `fusionner {cid} --ia <n>` depuis le clone principal : verrou de `main`, fusion, contrôles sur `main` avec Godot, ligne cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 `PROJECT_STATE.md` : mesures de l'unité ⟶ cocher {cid} F2
- [ ] F3 `publier` : `main` poussé, branche supprimée, verrou rendu ⟶ cochée par `publier`

## Pour la recette

Rien de propre à cette unité.
"""
