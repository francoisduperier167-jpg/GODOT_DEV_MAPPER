"""Commandes de travail des IA : prendre, cocher, fusionner, publier, verrou, etat, correction, arreter.

Chaque écriture passe par Git, de façon atomique :
- une unité se prend en poussant sa branche tache/<fiche> sans --force : si deux IA la prennent en même temps,
  le dépôt refuse la deuxième poussée ;
- une vérification se prend en poussant le fichier de verdict sur la branche, avec la même garantie ;
- toute écriture sur main (fusion, SUIVI.md, arrêt) se fait sous le verrou refs/heads/verrou/main, créé par
  une poussée qui échoue si le verrou existe déjà, et rendu même quand la commande échoue en route.

Les commandes qui créent ou suppriment des copies (../verif-*, ../fusion-*) travaillent depuis le clone
principal, jamais depuis une de ces copies, qu'elles pourraient supprimer sous leurs pieds.
"""
import json
import os
import pathlib
import shutil
import subprocess
import sys
import time

import commun as C


def stop(msg, code=3):
    print("REFUSÉ : " + msg)
    sys.exit(code)


def exiger_arret(uid, ia, raison):
    print(f"ARRÊT OBLIGATOIRE (docs/construction/sequence.md §5, n° 2) : {uid} {raison}.\n"
          f"Lance : python3 suivi/outil.py arreter --ia {ia} --unite {uid} --raison \"{uid} : {raison}\"\n"
          "puis termine ton créneau en citant cette raison.")
    sys.exit(4)


def nom(ia):
    """« IA n », ou « Humain » pour les commandes réservées à l'humain (lever)."""
    return f"IA {ia}" if isinstance(ia, int) else "Humain"


def identite(ia):
    """Options -c pour signer les commits « IA n » si aucune identité Git n'est configurée."""
    p = C.git("config", "user.email", check=False)
    if p.stdout.strip():
        return []
    return ["-c", f"user.name={nom(ia)}", "-c", f"user.email={nom(ia).lower().replace(' ', '')}@godot-dev-mapper.invalid"]


def commit(ia, message, cwd):
    C.git(*identite(ia), "commit", "--quiet", "-m", message, cwd=cwd)


def pousser(ia, dest, cwd, essais=4):
    """Pousse HEAD vers dest sans jamais forcer ; en cas de refus, rebase sur la branche distante puis réessaie."""
    for i in range(essais):
        p = C.git("push", "--quiet", "origin", f"HEAD:refs/heads/{dest}", cwd=cwd, check=False)
        if p.returncode == 0:
            return True
        r = C.git(*identite(ia), "pull", "--quiet", "--rebase", "origin", dest, cwd=cwd, check=False)
        if r.returncode != 0:
            C.git("rebase", "--abort", cwd=cwd, check=False)
            print(p.stderr.strip())
            return False
        time.sleep(2 ** (i + 1))
    return False


def clone_principal(depuis=None):
    """Racine du clone principal : le dossier qui contient le .git commun à toutes les copies."""
    p = C.git("rev-parse", "--path-format=absolute", "--git-common-dir", cwd=depuis or C.RACINE, check=False)
    if p.returncode == 0 and p.stdout.strip():
        return pathlib.Path(p.stdout.strip()).parent
    return C.racine_travail(depuis or C.RACINE)


def au_clone_principal():
    C.RACINE = clone_principal()
    return C.RACINE


def dans(chemin):
    """Vrai si le dossier courant est chemin ou l'un de ses sous-dossiers."""
    try:
        pathlib.Path.cwd().resolve().relative_to(pathlib.Path(chemin).resolve())
        return True
    except (ValueError, FileNotFoundError, OSError):
        return False


def recreer_copie(chemin, *args):
    """Supprime puis recrée une copie ../verif-* ou ../fusion-* depuis le clone principal."""
    if dans(chemin):
        stop(f"tu es dans {chemin}, que cette commande supprime puis recrée : cd {C.RACINE}, puis relance-la.", 2)
    if chemin.exists():
        C.git("worktree", "remove", "--force", str(chemin), check=False)
        shutil.rmtree(chemin, ignore_errors=True)
    C.git("worktree", "prune", check=False)
    C.git("worktree", "add", "--quiet", *args)


def supprimer_copie(chemin):
    if chemin.exists():
        C.git("worktree", "remove", "--force", str(chemin), check=False)
        shutil.rmtree(chemin, ignore_errors=True)
    C.git("worktree", "prune", check=False)


def propre(cwd=None):
    p = C.git("status", "--porcelain", "--untracked-files=no", cwd=cwd)
    if p.stdout.strip():
        stop("ta copie de travail a des modifications non commitées :\n" + p.stdout + "Commite-les sur leur branche, ou annule-les, avant de prendre une autre unité.")


def suivi_distant():
    t = C.montrer("origin/main", "SUIVI.md")
    if t is None:
        stop("SUIVI.md absent de origin/main", 2)
    return C.lire_suivi(t)


def arret_present():
    return C.montrer("origin/main", "rapports/ARRET.md") is not None


def etat_distant(S, uid, dist):
    """État d'une unité d'après le dépôt distant : (code, sous-étapes, rapport, verdict de la tentative en cours)."""
    u = S["unites"][uid]
    br = C.branche_de(u)
    if br in dist:
        ref = "origin/" + br
        etapes = C.lire_etapes(C.montrer(ref, u["fiche"]) or "")
        rap = C.lire_rapport(C.montrer(ref, f"rapports/{uid}.md"))
        ver = C.lire_verdict(C.montrer(ref, f"rapports/{uid}-verif-{rap['tentative']}.md"))
        return C.etat_unite(S, uid, etapes, rap, True, verdict=ver), etapes, rap, ver
    etapes = C.lire_etapes(C.montrer("origin/main", u["fiche"]) or "")
    return (C.etat_unite(S, uid, etapes, {}, False), etapes,
            C.lire_rapport(C.montrer("origin/main", f"rapports/{uid}.md")), C.lire_verdict(None))


def premiere_ouverte(etapes):
    for e in etapes:
        if not e["coche"]:
            return f"{e['id']} {e['texte']}"
    return "aucune : toutes les cases sont cochées"


def remplacer_ligne(texte, debut, nouvelle):
    lignes = texte.splitlines()
    for i, l in enumerate(lignes):
        if l.startswith(debut):
            lignes[i] = nouvelle(l)
            return "\n".join(lignes) + "\n", True
    return texte, False


def liste_ia(ias):
    return ", ".join(f"IA {x}" for x in ias) or "aucun"


# ---------------------------------------------------------------- rapports

def rapport_neuf(u, ia, tentative, ancien):
    t = C.horodatage()
    s = (f"# Rapport {u['id']} — {u['titre']}\n\n"
         f"- Statut : EN COURS\n- Auteurs : IA {ia}\n- Tentative : {tentative}\n- Créneaux utilisés : 1\n"
         f"- Prise en charge : {t} UTC par IA {ia}\n"
         + ("- Décision : \n" if C.est_porte(u) else "")
         + "- Fichiers modifiés : \n- Contrôles : \n- Contre-épreuves faites : \n"
         "- Écarts au contrat, au guide ou à la fiche : aucun\n- Hypothèses : aucune\n- Questions : aucune\n"
         "- Pour la recette : rien\n- Passation : \n")
    if ancien:
        s += "\n## Tentatives précédentes\n\n" + "\n".join("> " + l for l in ancien.splitlines()) + "\n"
    return s


def maj_rapport(texte, ia, etat=None, statut=None, tentative_plus=False):
    """Inscrit une reprise : auteur ajouté, créneau compté, ligne « Reprise » datée (elle remet à zéro le
    compteur d'abandon) ; un refus passe à la tentative suivante."""
    lignes = texte.splitlines()
    out = []
    courant = True
    for l in lignes:
        if l.startswith("## "):
            courant = False
        if courant and l.lstrip("- ").startswith("Statut :") and etat in ("refusee", "bloquee"):
            l = "- Statut : EN COURS"
        elif courant and l.lstrip("- ").startswith(("Auteurs :", "Auteur :")):
            ias = C.lire_rapport(l)["auteurs"]
            if ia not in ias:
                ias.append(ia)
            l = "- Auteurs : " + liste_ia(ias)
        elif courant and l.lstrip("- ").startswith("Tentative :") and tentative_plus:
            l = f"- Tentative : {C.lire_rapport(l)['tentative'] + 1}"
        elif courant and l.lstrip("- ").startswith("Créneaux utilisés :"):
            l = f"- Créneaux utilisés : {C.lire_rapport(l)['creneaux'] + 1}"
        out.append(l)
    reprise = f"- Reprise : {C.horodatage()} UTC par IA {ia}" + (f" (état : {C.LIBELLES[etat]}" + (f", {statut}" if statut else "") + ")" if etat else "")
    # la ligne de reprise se range avec les champs de la tentative en cours, avant « ## Tentatives précédentes »
    for i, l in enumerate(out):
        if l.startswith("## "):
            j = i
            while j > 0 and not out[j - 1].strip():
                j -= 1
            out.insert(j, reprise)
            break
    else:
        out.append(reprise)
    return "\n".join(out) + "\n"


def verdict_neuf(uid, n, ia):
    return (f"# Verdict {uid}, tentative {n}\n\n- Verdict : EN COURS\n- Vérificateur : IA {ia}\n- Début : {C.horodatage()} UTC\n"
            "- Contrôles relancés : \n- Contre-épreuves : \n- Problèmes : aucun\n- Doutes non bloquants : \n")


# ---------------------------------------------------------------- prendre

def prendre(uid, ia, verification=False):
    au_clone_principal()
    C.fetch()
    if arret_present():
        stop("rapports/ARRET.md existe sur main : tous les créneaux s'arrêtent.", 4)
    S = suivi_distant()
    if uid not in S["unites"]:
        stop(f"{uid} absente de SUIVI.md sur main", 2)
    u = S["unites"][uid]
    if u["coche"]:
        stop(f"{uid} est déjà faite.")
    dist = C.branches_distantes()
    br = C.branche_de(u)
    etat, etapes, rap, ver = etat_distant(S, uid, dist)
    raison = C.arret_requis(etat, rap) if br in dist else None
    if raison:
        exiger_arret(uid, ia, raison)
    if verification:
        return prendre_verification(S, u, ia, etat, etapes, rap, ver, br)
    propre()
    t = C.maintenant()
    if etat == "attente":
        stop(f"prérequis non cochés dans SUIVI.md : {', '.join(C.prerequis_manquants(S, uid))}")
    if etat == "prete":
        if u["r"] != ia:
            p = C.pret_depuis(S, uid)
            if p is None or (t - p).total_seconds() < C.RELAIS_H * 3600:
                stop(f"{uid} est prévue pour IA {u['r']} ; une autre IA peut la prendre {C.RELAIS_H} h après qu'elle est devenue prête"
                     + (f" (prête depuis le {C.horodatage(p)} UTC)" if p else ""))
        return creer(u, ia, br)
    auteur = ia in rap["auteurs"]
    if etat == "en_cours" and not auteur:
        act = C.derniere_activite(etapes, rap, ver)
        stop(f"{uid} est en cours par {liste_ia(rap['auteurs'])} (dernière activité le {C.horodatage(act) if act else '?'} UTC) ; "
             f"reprise par une autre IA possible après {C.ABANDON_H} h sans activité.")
    if etat == "bloquee" and ia != C.resolveur(rap):
        stop(f"{uid} est en {rap['statut']} : elle revient à IA {C.resolveur(rap)}, qui répond dans le rapport et reprend l'unité.")
    if etat == "refusee" and not auteur and u["r"] != ia:
        stop(f"{uid} est refusée : elle revient à son auteur ({liste_ia(rap['auteurs'])}) ou à IA {u['r']}.")
    if etat == "en_cours" and auteur:     # une unité refusée n'est tenue par personne : tout auteur la reprend
        autre = tenue_par_autre(etapes, rap, ver, ia, t)
        if autre:
            stop(f"{uid} est tenue par IA {autre[1]}, co-autrice, depuis le {C.horodatage(autre[0])} UTC : une seule IA par branche. "
                 f"Tu la reprendras si elle reste {C.ABANDON_H} h sans activité.")
    if etat in ("en_cours", "abandonnee", "refusee", "bloquee"):
        if not auteur and len(set(rap["auteurs"])) >= 2:
            stop(f"{uid} a déjà deux auteurs ({liste_ia(rap['auteurs'])}) : tu serais la troisième, et plus personne ne pourrait la vérifier. "
                 "Elle revient à l'un de ses auteurs.")
        return reprendre(u, ia, br, etat, rap)
    stop(f"{uid} est « {C.LIBELLES[etat]} » : rien à réaliser maintenant"
         + (" ; si tu n'en es pas l'auteur, prends-la avec --verification" if etat in ("a_verifier", "verif_abandonnee", "en_verification") else "")
         + (" ; la fusion revient à l'IA qui a signé le verdict : `fusionner`" if etat == "a_fusionner" else ""))


def tenue_par_autre(etapes, rap, ver, ia, t=None):
    """(date, IA) si un autre auteur a agi en dernier sur l'unité il y a moins de ABANDON_H, sinon None."""
    t = t or C.maintenant()
    quand, qui = C.dernier_acteur(etapes, rap, ver)
    if qui is not None and qui != ia and qui in rap["auteurs"] and (t - quand).total_seconds() < C.ABANDON_H * 3600:
        return quand, qui
    return None


def ici():
    if not dans(C.RACINE):
        print(f"Copie de travail : cd {C.RACINE}")


def creer(u, ia, br):
    uid = u["id"]
    C.git("switch", "--quiet", "-C", br, "origin/main")
    fp = C.RACINE / u["fiche"]
    lignes = fp.read_text(encoding="utf-8").splitlines()
    rejeu = any(C.RE_ETAPE.match(l) and l.startswith("- [x]") for l in lignes)
    if rejeu:
        lignes = [C.decocher_ligne(l) if C.RE_ETAPE.match(l) else l for l in lignes]
    for i, l in enumerate(lignes):
        if l.startswith("- [ ] R0 "):
            lignes[i] = C.signer_ligne(l, ia)
            break
    else:
        stop(f"{u['fiche']} n'a pas de sous-étape R0", 2)
    fp.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    rp = C.RACINE / "rapports" / f"{uid}.md"
    ancien = rp.read_text(encoding="utf-8") if rp.exists() else None
    tentative = C.lire_rapport(ancien)["tentative"] + 1 if ancien else 1
    rp.parent.mkdir(exist_ok=True)
    rp.write_text(rapport_neuf(u, ia, tentative, ancien), encoding="utf-8")
    C.git("add", u["fiche"], f"rapports/{uid}.md")
    commit(ia, f"{uid} R0 : prise en charge par IA {ia}" + (" (porte rejouée)" if rejeu else ""), C.RACINE)
    p = C.git("push", "--quiet", "-u", "origin", br, check=False)
    if p.returncode != 0:
        C.git("switch", "--quiet", "--detach", "origin/main", check=False)
        C.git("branch", "-D", br, check=False)
        stop(f"une autre IA a pris {uid} au même moment (poussée refusée). Choisis une autre unité.")
    etapes = C.lire_etapes(fp.read_text(encoding="utf-8"))
    print(f"PRISE : {uid} par IA {ia}, branche {br}, tentative {tentative}.")
    ici()
    print(f"Prochaine sous-étape : {premiere_ouverte(etapes)}")


def reprendre(u, ia, br, etat, rap):
    uid = u["id"]
    C.git("switch", "--quiet", "-C", br, "origin/" + br)
    rp = C.RACINE / "rapports" / f"{uid}.md"
    rp.write_text(maj_rapport(rp.read_text(encoding="utf-8") if rp.exists() else rapport_neuf(u, ia, 1, None), ia, etat,
                              statut=rap["statut"] if etat == "bloquee" else None,
                              tentative_plus=(etat == "refusee")), encoding="utf-8")
    fp = C.RACINE / u["fiche"]
    texte = fp.read_text(encoding="utf-8")
    if etat in ("refusee", "bloquee"):
        lignes = texte.splitlines()
        etapes = C.lire_etapes(texte)
        R = [e for e in etapes if e["g"] == "R"]
        k = 1 + sum(1 for e in R if e["id"].startswith("Rc"))
        if etat == "refusee":
            quoi = f"Problèmes du verdict de la tentative {rap['tentative']} (`rapports/{uid}-verif-{rap['tentative']}.md`) corrigés un par un, chacun prouvé dans le rapport"
            for e in etapes:
                if e["g"] == "V" or e is R[-1]:
                    lignes[e["ligne"] - 1] = C.decocher_ligne(lignes[e["ligne"] - 1])
        else:
            quoi = f"{rap['statut']} traitée : réponse ou diagnostic écrit dans le rapport, puis travail repris"
        lignes.insert(R[-1]["ligne"] - 1, f"- [ ] Rc{k} {quoi} ⟶ cocher {uid} Rc{k}")
        fp.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    C.git("add", u["fiche"], f"rapports/{uid}.md")
    commit(ia, f"{uid} : reprise par IA {ia} ({C.LIBELLES[etat]})", C.RACINE)
    p = C.git("push", "--quiet", "origin", f"HEAD:refs/heads/{br}", check=False)
    if p.returncode != 0:
        C.git("switch", "--quiet", "--detach", "origin/main", check=False)
        C.git("branch", "-D", br, check=False)
        stop(f"une autre IA a repris {uid} au même moment (poussée refusée). Choisis une autre unité.")
    print(f"REPRISE : {uid} par IA {ia} ({C.LIBELLES[etat]}), branche {br}.")
    ici()
    print(f"Prochaine sous-étape : {premiere_ouverte(C.lire_etapes(fp.read_text(encoding='utf-8')))}")


def prendre_verification(S, u, ia, etat, etapes, rap, ver, br):
    uid = u["id"]
    if ia in rap["auteurs"]:
        stop(f"IA {ia} est auteur de {uid} : tu ne la vérifies jamais.")
    if etat == "en_verification" and ver["verificateur"] != ia:
        act = C.derniere_activite(etapes, rap, ver)
        stop(f"{uid} est en vérification par IA {ver['verificateur']} (dernière activité le {C.horodatage(act) if act else '?'} UTC) ; "
             f"reprise par une autre IA possible après {C.ABANDON_H} h sans activité.")
    if etat not in ("a_verifier", "verif_abandonnee", "en_verification"):
        stop(f"{uid} est « {C.LIBELLES[etat]} » : rien à vérifier maintenant.")
    if etat == "a_verifier" and u["v"] != ia and u["v"] not in rap["auteurs"]:
        R = [e for e in etapes if e["g"] == "R"]
        fin = C.lire_date(R[-1]["date"]) if R and R[-1]["date"] else None
        if fin is None or (C.maintenant() - fin).total_seconds() < C.RELAIS_H * 3600:
            stop(f"vérification prévue pour IA {u['v']} ; une autre IA non auteur peut la prendre {C.RELAIS_H} h après « TERMINÉ »"
                 + (f" (terminée le {C.horodatage(fin)} UTC)" if fin else ""))
    stem = C.stem_de(u)
    chemin = C.RACINE.parent / f"verif-{stem}"
    recreer_copie(chemin, "-B", f"verif/{stem}", str(chemin), f"origin/{br}")
    n = rap["tentative"]
    vp = chemin / "rapports" / f"{uid}-verif-{n}.md"
    vp.parent.mkdir(exist_ok=True)
    fp = chemin / u["fiche"]
    if etat == "a_verifier":
        vp.write_text(verdict_neuf(uid, n, ia), encoding="utf-8")
        texte, ok = remplacer_ligne(fp.read_text(encoding="utf-8"), "- [ ] V1 ", lambda l: C.signer_ligne(l, ia))
        if not ok:
            stop(f"{u['fiche']} n'a pas de sous-étape V1 ouverte", 2)
        fp.write_text(texte, encoding="utf-8")
        quoi = "vérification prise"
    else:
        # reprise : la sienne (nouveau créneau) ou celle d'une vérification abandonnée ; V1 n'est pas resignée
        t = vp.read_text(encoding="utf-8") if vp.exists() else verdict_neuf(uid, n, ia)
        t, _ = remplacer_ligne(t, "- Vérificateur :", lambda l: f"- Vérificateur : IA {ia}")
        vp.write_text(t.rstrip("\n") + f"\n- Reprise : {C.horodatage()} UTC par IA {ia}\n", encoding="utf-8")
        quoi = "vérification reprise"
    C.git("add", u["fiche"], f"rapports/{uid}-verif-{n}.md", cwd=chemin)
    commit(ia, f"{uid} V1 : {quoi} par IA {ia}", chemin)
    p = C.git("push", "--quiet", "origin", f"HEAD:refs/heads/{br}", cwd=chemin, check=False)
    if p.returncode != 0:
        supprimer_copie(chemin)
        stop(f"une autre IA a pris la vérification de {uid} au même moment (poussée refusée).")
    print(f"VÉRIFICATION {'PRISE' if etat == 'a_verifier' else 'REPRISE'} : {uid} par IA {ia}, tentative {n}.")
    print(f"Copie neuve : cd {chemin}")
    print(f"Prochaine sous-étape : {premiere_ouverte(C.lire_etapes(fp.read_text(encoding='utf-8')))}")


# ---------------------------------------------------------------- cocher

def normaliser_verdict(v):
    if v is None:
        return None
    v = v.upper().replace("É", "E")
    if v in ("ACCEPTEE", "ACCEPTE"):
        return "ACCEPTÉE"
    if v in ("REFUSEE", "REFUSE"):
        return "REFUSÉE"
    stop("--verdict vaut ACCEPTÉE ou REFUSÉE", 2)


def indexe(racine, chemin):
    """Contenu d'un fichier tel qu'il sera commité (index), ou None s'il n'y est pas."""
    p = C.git("show", f":{chemin}", cwd=racine, check=False)
    return p.stdout if p.returncode == 0 else None


def cocher(uid, eid, ia, verdict=None):
    racine = C.racine_travail(pathlib.Path.cwd())
    S = C.lire_suivi((racine / "SUIVI.md").read_text(encoding="utf-8"))
    if uid not in S["unites"]:
        stop(f"{uid} absente de SUIVI.md", 2)
    u = S["unites"][uid]
    fp = racine / u["fiche"]
    texte = fp.read_text(encoding="utf-8")
    etapes = C.lire_etapes(texte)
    e = next((x for x in etapes if x["id"] == eid), None)
    if e is None:
        stop(f"sous-étape {eid} absente de {u['fiche']}", 2)
    if e["coche"]:
        stop(f"{eid} est déjà cochée ({e['date']} UTC, IA {e['ia']}).")
    avant = [x for x in etapes[: etapes.index(e)] if not x["coche"]]
    if avant:
        stop(f"coche d'abord {avant[0]['id']} : les sous-étapes se font dans l'ordre.")
    R = [x for x in etapes if x["g"] == "R"]
    V = [x for x in etapes if x["g"] == "V"]
    F = [x for x in etapes if x["g"] == "F"]
    if e is R[0]:
        stop("R0 se coche par `python3 suivi/outil.py prendre`.")
    if V and e is V[0]:
        stop("V1 se coche par `python3 suivi/outil.py prendre --verification`.")
    if F and e is F[0]:
        stop("F1 se coche par `python3 suivi/outil.py fusionner`.")
    if F and e is F[-1]:
        stop("la dernière case F se coche par `python3 suivi/outil.py publier`.")
    # rapport et verdict tels qu'ils seront commités : une modification non ajoutée (git add) ne compte pas
    rap = C.lire_rapport(indexe(racine, f"rapports/{uid}.md") or "")
    signe_verdict = None
    if e["g"] == "R":
        if ia not in rap["auteurs"]:
            stop(f"IA {ia} n'est pas auteur de {uid} : lance d'abord `python3 suivi/outil.py prendre {uid} --ia {ia}`.")
        if e is R[-1] and rap["statut"] != "TERMINÉ":
            stop(f"écris d'abord « Statut : TERMINÉ » dans rapports/{uid}.md, puis git add rapports/{uid}.md.")
        if e is R[-1] and C.est_porte(u) and rap["decision"] is None:
            stop(f"porte : écris d'abord « Décision : PASSER » ou « Décision : CORRIGER D'ABORD » dans rapports/{uid}.md, puis git add.")
    else:
        if ia in rap["auteurs"]:
            stop(f"IA {ia} est auteur de {uid} : elle ne la vérifie pas et ne la fusionne pas.")
        nom = f"rapports/{uid}-verif-{rap['tentative']}.md"
        ver = C.lire_verdict(indexe(racine, nom) or "")
        if e["g"] == "V" and ver["verificateur"] != ia:
            stop(f"le vérificateur inscrit dans {nom} est IA {ver['verificateur']} : lance d'abord `prendre {uid} --ia {ia} --verification`.")
        if e["g"] == "V" and e is V[-1]:
            verdict = normaliser_verdict(verdict)
            if verdict is None:
                stop("dernière sous-étape de vérification : ajoute --verdict ACCEPTÉE ou --verdict REFUSÉE.")
            if ver["verdict"] != verdict:
                stop(f"{nom} dit « Verdict : {ver['verdict']} » : écris-y « Verdict : {verdict} », puis git add {nom}.")
            signe_verdict = verdict
        if e["g"] == "F":
            if not V or V[-1]["verdict"] != "ACCEPTÉE":
                stop("aucun verdict ACCEPTÉE signé : pas de fusion.")
            if F[0]["ia"] != ia:
                stop(f"la fusion de {uid} est tenue par IA {F[0]['ia']}, qui a lancé `fusionner` : les cases F sont les siennes.")
    lignes = texte.splitlines()
    lignes[e["ligne"] - 1] = C.signer_ligne(lignes[e["ligne"] - 1], ia, signe_verdict)
    fp.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    nonajoutes = C.git("diff", "--name-only", cwd=racine).stdout.split()
    nonajoutes = [x for x in nonajoutes if x != u["fiche"]]
    C.git("add", u["fiche"], cwd=racine)
    commit(ia, f"{uid} {eid} : {e['texte'][:70]}", racine)
    msg = f"COCHÉE : {uid} {eid} — IA {ia}" + (f" · {signe_verdict}" if signe_verdict else "")
    if e["g"] in ("R", "V"):
        if not pousser(ia, C.branche_de(u), racine):
            stop(f"case cochée et commitée, mais la poussée vers {C.branche_de(u)} a échoué : relance `git push origin HEAD:{C.branche_de(u)}` avant toute autre chose.", 5)
        msg += f", poussée sur {C.branche_de(u)}"
    else:
        msg += " (commit local sur la copie de fusion ; `publier` poussera main)"
    print(msg)
    if nonajoutes:
        print("ATTENTION : fichiers modifiés non ajoutés à ce commit : " + ", ".join(nonajoutes))
    print(f"Prochaine sous-étape : {premiere_ouverte(C.lire_etapes(fp.read_text(encoding='utf-8')))}")
    if signe_verdict == "ACCEPTÉE":
        print(f"Suite : cd {clone_principal(racine)} && python3 suivi/outil.py fusionner {uid} --ia {ia}"
              + ("  (la décision CORRIGER D'ABORD du rapport laisse la ligne de la porte ouverte)" if rap["decision"] == "CORRIGER D'ABORD" else ""))
    elif signe_verdict == "REFUSÉE":
        print("Suite : arrête-toi sur cette unité ; son auteur la reprendra avec `prendre`.")


# ---------------------------------------------------------------- verrou de main

def etat_verrou():
    p = C.git("ls-remote", "origin", C.REF_VERROU, check=False)
    if p.returncode != 0 or not p.stdout.strip():
        return None
    sha = p.stdout.split()[0]
    C.git("fetch", "--quiet", "origin", f"+{C.REF_VERROU}:refs/gdm/verrou", check=False)
    s = C.git("log", "-1", "--format=%s%n%ct", "refs/gdm/verrou", check=False).stdout.strip()
    if "\n" not in s:
        return dict(sha=sha, message="?", age_min=0)
    msg, ct = s.rsplit("\n", 1)
    return dict(sha=sha, message=msg, age_min=(time.time() - int(ct)) / 60)


def prendre_verrou(ia, motif, attendre_min=30):
    vide = C.git("mktree", entree="").stdout.strip()
    fin = time.time() + attendre_min * 60
    while True:
        sha = C.git(*identite(ia), "commit-tree", vide, "-m", f"{nom(ia)} · {motif} · {C.horodatage()} UTC").stdout.strip()
        p = C.git("push", "--quiet", f"--force-with-lease={C.REF_VERROU}:", "origin", f"{sha}:{C.REF_VERROU}", check=False)
        if p.returncode == 0:
            print(f"VERROU PRIS : {nom(ia)} · {motif}")
            return sha
        e = etat_verrou()
        if e is None:
            if time.time() > fin:
                stop("impossible de créer le verrou de main (réseau ou droits) :\n" + p.stderr.strip(), 6)
            time.sleep(5)
            continue
        if e["age_min"] > C.VERROU_MIN:
            C.git("push", "--quiet", f"--force-with-lease={C.REF_VERROU}:{e['sha']}", "origin", f":{C.REF_VERROU}", check=False)
            print(f"verrou périmé supprimé ({e['message']}, {e['age_min']:.0f} min)")
            continue
        if time.time() > fin:
            stop(f"verrou de main occupé depuis {e['age_min']:.0f} min ({e['message']}) : prends une autre unité et reviens plus tard.", 6)
        print(f"verrou de main occupé ({e['message']}, {e['age_min']:.0f} min) : nouvel essai dans 30 s")
        time.sleep(30)


def lacher_verrou(sha):
    """Rend le verrou s'il est encore celui qu'on a pris (sha) ; ne fait rien sinon. Ne lève jamais."""
    p = C.git("push", "--quiet", f"--force-with-lease={C.REF_VERROU}:{sha}", "origin", f":{C.REF_VERROU}", check=False)
    return p.returncode == 0


def rendre_verrou(ia, silencieux=False):
    e = etat_verrou()
    if e is None:
        if not silencieux:
            print("verrou déjà libre")
        return
    if not e["message"].startswith(f"IA {ia} "):
        stop(f"le verrou appartient à « {e['message']} » : tu ne le rends pas.")
    p = C.git("push", "--quiet", f"--force-with-lease={C.REF_VERROU}:{e['sha']}", "origin", f":{C.REF_VERROU}", check=False)
    if p.returncode != 0:
        stop("le verrou a changé entre-temps ; relance `verrou etat`.", 6)
    print(f"VERROU RENDU : {e['message']}")


def verrou(action, ia=None, motif="écriture sur main"):
    if action == "etat":
        e = etat_verrou()
        print("verrou de main : libre" if e is None else f"verrou de main : {e['message']} (depuis {e['age_min']:.0f} min)")
    elif action == "prendre":
        prendre_verrou(ia, motif)
    elif action == "rendre":
        rendre_verrou(ia)


def fusion_en_cours(e, uid):
    return e is not None and f" · Fusion {uid} · " in e["message"]


# ---------------------------------------------------------------- Godot pour les contrôles de fusion

def version_stable(ref):
    t = C.montrer(ref, "addons/godot_dev_mapper/compat/versions.json")
    try:
        return json.loads(t)["stable"] if t else "4.7.2-stable"
    except (ValueError, KeyError, TypeError):
        return "4.7.2-stable"


def godot_valide(chemin, stable):
    if not chemin:
        return None
    exe = shutil.which(chemin) or (chemin if os.path.isfile(chemin) and os.access(chemin, os.X_OK) else None)
    if not exe:
        return None
    try:
        r = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.SubprocessError):
        return None
    return os.path.abspath(exe) if stable.replace("-", ".") in r.stdout else None


def trouver_godot(option, ref="origin/main"):
    """Godot stable pour run_all_checks.sh : --godot, puis $GODOT, puis le cache du bloc GODOT des fiches,
    puis tools/ci/fetch_godot.sh <stable de versions.json>. Chemin absolu contrôlé par --version, ou None."""
    stable = version_stable(ref)
    cache = pathlib.Path.home() / ".cache" / "gdm-godot" / stable / f"Godot_v{stable}_linux.x86_64"
    for c in (option, os.environ.get("GODOT"), str(cache)):
        exe = godot_valide(c, stable)
        if exe:
            return exe
    script = C.RACINE / "tools" / "ci" / "fetch_godot.sh"
    if script.exists():
        try:
            r = subprocess.run(["bash", str(script), stable], cwd=str(C.RACINE), capture_output=True, text=True, timeout=900)
            lignes = r.stdout.strip().splitlines()
            if r.returncode == 0 and lignes:
                return godot_valide(lignes[-1].strip(), stable)
        except (OSError, subprocess.SubprocessError):
            pass
    return None


# ---------------------------------------------------------------- fusionner et publier

def chemin_fusion(u):
    return C.RACINE.parent / f"fusion-{C.stem_de(u)}"


def controle_fusion(uid, ia):
    """Ce qui doit être vrai pour fusionner ; relu une seconde fois sous le verrou."""
    S = suivi_distant()
    if uid not in S["unites"]:
        stop(f"{uid} absente de SUIVI.md", 2)
    u = S["unites"][uid]
    if u["coche"]:
        stop(f"{uid} est déjà cochée dans SUIVI.md sur main : elle est déjà fusionnée.")
    br = C.branche_de(u)
    if br not in C.branches_distantes():
        stop(f"branche {br} absente du dépôt distant (fusion déjà publiée, ou unité jamais prise).")
    etapes = C.lire_etapes(C.montrer("origin/" + br, u["fiche"]) or "")
    rap = C.lire_rapport(C.montrer("origin/" + br, f"rapports/{uid}.md"))
    V = [e for e in etapes if e["g"] == "V"]
    if not V or not V[-1]["coche"] or V[-1]["verdict"] != "ACCEPTÉE":
        stop(f"{uid} n'a pas de verdict ACCEPTÉE signé sur {br}.")
    if ia in rap["auteurs"]:
        stop(f"IA {ia} est auteur de {uid} : elle ne la fusionne pas.")
    return u, br, etapes, rap, V


def refuser_fusion(u, ia, rap, raison):
    """La fusion a échoué : verdict passé à REFUSÉE sur la branche. Le verrou est rendu par fusionner."""
    uid, br, stem = u["id"], C.branche_de(u), C.stem_de(u)
    tmp = C.RACINE.parent / f"refus-{stem}"
    supprimer_copie(tmp)
    if C.git("worktree", "add", "--quiet", "--detach", str(tmp), f"origin/{br}", check=False).returncode != 0:
        stop(f"fusion de {uid} impossible et branche {br} illisible : main inchangée.\n{raison[-1500:]}", 5)
    fp = tmp / u["fiche"]
    lignes = fp.read_text(encoding="utf-8").splitlines()
    V = [e for e in C.lire_etapes("\n".join(lignes)) if e["g"] == "V"]
    if V:
        lignes[V[-1]["ligne"] - 1] = lignes[V[-1]["ligne"] - 1].replace(" · ACCEPTÉE", " · REFUSÉE")
    fp.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    vp = tmp / "rapports" / f"{uid}-verif-{rap['tentative']}.md"
    t = vp.read_text(encoding="utf-8") if vp.exists() else verdict_neuf(uid, rap["tentative"], ia)
    t = t.replace("Verdict : ACCEPTÉE", "Verdict : REFUSÉE")
    t += f"\n## Refus à la fusion\n\n{C.horodatage()} UTC, IA {ia}.\n\n```text\n{raison[-4000:]}\n```\n"
    vp.parent.mkdir(exist_ok=True)
    vp.write_text(t, encoding="utf-8")
    C.git("add", u["fiche"], str(vp.relative_to(tmp)), cwd=tmp)
    commit(ia, f"{uid} : REFUSÉE à la fusion", tmp)
    ok = pousser(ia, br, tmp)
    supprimer_copie(tmp)
    stop(f"fusion de {uid} refusée ; " + (f"verdict REFUSÉE poussé sur {br}" if ok else f"poussée du verdict REFUSÉE sur {br} impossible")
         + f", main inchangée, verrou rendu.\n{raison[-1500:]}", 5)


def decision_porte(u, rap, porte_ko):
    """Porte KO ou non : lue dans « Décision : … » du rapport ; --porte-ko doit concorder."""
    if not C.est_porte(u):
        if porte_ko:
            stop("--porte-ko ne s'emploie que pour une porte dont la décision est « corriger d'abord ».", 2)
        return False
    d = rap["decision"]
    if d is None:
        if not porte_ko:
            print("ATTENTION : rapport de porte sans « Décision : PASSER | CORRIGER D'ABORD » : fusion comme PASSER.")
        return porte_ko
    if porte_ko and d == "PASSER":
        stop(f"le rapport de {u['id']} dit « Décision : PASSER » : --porte-ko refusé.", 2)
    return d == "CORRIGER D'ABORD"


def fusionner(uid, ia, porte_ko=False, godot=None):
    au_clone_principal()
    C.fetch()
    if arret_present():
        stop("rapports/ARRET.md existe sur main.", 4)
    u, br, etapes, rap, V = controle_fusion(uid, ia)
    signataire = V[-1]["ia"]
    if ia != signataire:
        quand = C.lire_date(V[-1]["date"])
        if (C.maintenant() - quand).total_seconds() < C.RELAIS_H * 3600:
            stop(f"la fusion de {uid} revient à IA {signataire}, qui a signé le verdict le {V[-1]['date']} UTC ; "
                 f"une autre IA non auteur peut la faire {C.RELAIS_H} h après.")
    ko = decision_porte(u, rap, porte_ko)
    chemin = chemin_fusion(u)
    if dans(chemin):
        stop(f"tu es dans {chemin}, que fusionner supprime puis recrée : cd {C.RACINE}, puis relance.", 2)
    exe = None
    controles = any(C.montrer(r, "tools/ci/run_all_checks.sh") is not None for r in ("origin/main", "origin/" + br))
    if controles and not ko:
        exe = trouver_godot(godot)
        if exe is None:
            stop(f"Godot {version_stable('origin/main')} introuvable (--godot, $GODOT, cache ou tools/ci/fetch_godot.sh) : "
                 "contrôles de fusion impossibles. Verdict inchangé, verrou non pris. Obtiens Godot (bloc GODOT des fiches) "
                 "et relance ; deux créneaux de suite sans Godot : arrêt obligatoire n° 5.", 6)
    sha = prendre_verrou(ia, f"Fusion {uid}")
    fini = False
    try:
        C.fetch()
        u, br, etapes, rap, V = controle_fusion(uid, ia)    # revérifié sous le verrou : une autre IA a pu fusionner
        recreer_copie(chemin, "--detach", str(chemin), "origin/main")
        p = C.git(*identite(ia), "merge", "--no-ff", f"origin/{br}", "-m", f"Fusion {uid} : {u['titre']}", cwd=chemin, check=False)
        if p.returncode != 0:
            C.git("merge", "--abort", cwd=chemin, check=False)
            supprimer_copie(chemin)
            refuser_fusion(u, ia, rap, "Conflit de fusion avec main : l'auteur intègre main dans sa branche et résout.\n" + p.stdout + p.stderr)
        script = chemin / "tools" / "ci" / "run_all_checks.sh"
        if script.exists() and not ko and exe is None:
            exe = trouver_godot(godot)    # run_all_checks.sh est arrivé sur main pendant l'attente du verrou
            if exe is None:
                stop(f"Godot introuvable alors que tools/ci/run_all_checks.sh existe désormais sur main : contrôles de fusion impossibles. "
                     "Verdict inchangé, verrou rendu ; obtiens Godot (bloc GODOT des fiches) et relance.", 6)
        if ko:
            print("Porte KO : la fusion n'apporte que le rapport de porte ; contrôles globaux non relancés, ligne de la porte laissée ouverte.")
        elif script.exists():
            env = os.environ.copy()
            env["GODOT"] = exe or env.get("GODOT", "")
            r = subprocess.run([str(script)], cwd=str(chemin), env=env, capture_output=True, text=True)
            sortie = r.stdout + r.stderr
            print("\n".join(sortie.strip().splitlines()[-12:]))
            if r.returncode != 0 or "ALL_CHECKS OK" not in sortie:
                supprimer_copie(chemin)
                refuser_fusion(u, ia, rap, "tools/ci/run_all_checks.sh sur main après fusion :\n" + sortie)
        else:
            print("tools/ci/run_all_checks.sh absent : pas encore de contrôle global (il arrive avec S06).")
        if not ko:
            sp = chemin / "SUIVI.md"
            auteurs = liste_ia(rap["auteurs"])
            t, ok = remplacer_ligne(sp.read_text(encoding="utf-8"), f"- [ ] **{uid}** ·",
                                    lambda l: l.replace("- [ ]", "- [x]", 1) + f" · fait le {C.horodatage()} UTC · {'auteurs' if len(rap['auteurs']) > 1 else 'auteur'} {auteurs} · vérifié par IA {V[-1]['ia']} · {rap['creneaux']} créneau{'x' if rap['creneaux'] > 1 else ''}")
            if not ok:
                stop(f"ligne {uid} introuvable dans SUIVI.md", 2)
            sp.write_text(t, encoding="utf-8")
        fp = chemin / u["fiche"]
        t, ok = remplacer_ligne(fp.read_text(encoding="utf-8"), "- [ ] F1 ", lambda l: C.signer_ligne(l, ia))
        fp.write_text(t, encoding="utf-8")
        C.git("add", "SUIVI.md", u["fiche"], cwd=chemin)
        commit(ia, f"Fusion {uid} : " + ("porte KO, ligne non cochée" if ko else "ligne cochée dans SUIVI.md") + ", F1", chemin)
        fini = True
    finally:
        if not fini:
            if chemin.exists():
                C.git("merge", "--abort", cwd=chemin, check=False)
            supprimer_copie(chemin)
            if lacher_verrou(sha):
                print("Verrou de main rendu, copie de fusion supprimée.")
    print(f"FUSION PRÊTE : {uid}, verrou de main tenu par IA {ia}.")
    print(f"Copie de fusion : cd {chemin}")
    print(f"Fais-y les sous-étapes F suivantes (cocher {uid} F<k> --ia {ia}), puis : python3 suivi/outil.py publier {uid} --ia {ia}")
    if ko:
        print(f"Porte KO : pour chaque correction, python3 suivi/outil.py correction {uid} --fautive <Syy> --titre \"…\" --realise <n> --verifie <m> --ia {ia}")


def publier(uid, ia):
    racine = C.racine_travail(pathlib.Path.cwd())
    principal = clone_principal(racine)
    S = C.lire_suivi((racine / "SUIVI.md").read_text(encoding="utf-8"))
    if uid not in S["unites"]:
        stop(f"{uid} absente de SUIVI.md", 2)
    u = S["unites"][uid]
    if racine.name != f"fusion-{C.stem_de(u)}":
        alt = principal.parent / f"fusion-{C.stem_de(u)}"
        if not alt.exists():
            stop(f"copie de fusion introuvable : cd {principal} && python3 suivi/outil.py fusionner {uid} --ia {ia}")
        racine = alt
    e = etat_verrou()
    if e is None or not e["message"].startswith(f"IA {ia} · Fusion {uid} "):
        stop(f"tu ne tiens pas le verrou de main pour {uid} ({e['message'] if e else 'libre'}) : relance la fusion depuis ton clone principal : "
             f"cd {principal} && python3 suivi/outil.py fusionner {uid} --ia {ia}", 6)
    sale = C.git("status", "--porcelain", "--untracked-files=no", cwd=racine).stdout.strip()
    if sale:
        stop(f"la copie de fusion {racine} a des modifications non commitées :\n{sale}\n"
             "Ajoute-les (git add) et coche la case F qui les couvre, ou annule-les ; le verrou reste à toi.", 5)
    fp = racine / u["fiche"]
    etapes = C.lire_etapes(fp.read_text(encoding="utf-8"))
    F = [x for x in etapes if x["g"] == "F"]
    ouvertes = [x["id"] for x in F[:-1] if not x["coche"]]
    if ouvertes:
        stop(f"sous-étapes F non cochées : {', '.join(ouvertes)}.")
    if F and not F[-1]["coche"]:
        t, _ = remplacer_ligne(fp.read_text(encoding="utf-8"), f"- [ ] {F[-1]['id']} ", lambda l: C.signer_ligne(l, ia))
        fp.write_text(t, encoding="utf-8")
    v = subprocess.run([sys.executable, str(racine / "suivi" / "outil.py"), "verifier"], cwd=str(racine), capture_output=True, text=True)
    print(v.stdout.strip())
    if v.returncode != 0:
        stop("`outil.py verifier` échoue sur la copie de fusion : corrige, puis relance publier. Le verrou reste à toi.", 5)
    C.git("add", u["fiche"], cwd=racine)
    if C.git("diff", "--cached", "--quiet", cwd=racine, check=False).returncode != 0:
        commit(ia, f"Fusion {uid} : {F[-1]['id'] if F else 'publication'}", racine)
    if not pousser(ia, "main", racine):
        stop("poussée de main refusée : vérifie le verrou (`verrou etat`) et relance publier.", 5)
    C.git("push", "--quiet", "origin", "--delete", C.branche_de(u), cwd=principal, check=False)
    rendre_verrou(ia)
    C.git("worktree", "remove", "--force", str(racine), cwd=principal, check=False)
    C.git("worktree", "prune", cwd=principal, check=False)
    print(f"PUBLIÉE : {uid} fusionnée sur main, branche {C.branche_de(u)} supprimée.")
    print(f"Retour au clone principal : cd {principal}")


# ---------------------------------------------------------------- correction demandée par une porte

def correction(porte, fautive, titre, realise, verifie, ia):
    racine = C.racine_travail(pathlib.Path.cwd())
    if realise == verifie:
        stop("--realise et --verifie doivent être deux IA différentes.", 2)
    e = etat_verrou()
    if e is None or not e["message"].startswith(f"IA {ia} · Fusion {porte} "):
        stop(f"une correction s'ajoute pendant la fusion de la porte {porte}, sous son verrou ({e['message'] if e else 'verrou libre'}) : "
             f"lance d'abord `fusionner {porte} --ia {ia}`.", 6)
    if not racine.name.startswith("fusion-"):
        stop(f"lance correction depuis la copie de fusion de {porte} (cd ../fusion-…).", 2)
    sp = racine / "SUIVI.md"
    texte = sp.read_text(encoding="utf-8")
    S = C.lire_suivi(texte)
    if porte not in S["unites"] or fautive not in S["unites"]:
        stop("porte ou unité fautive absente de SUIVI.md", 2)
    base = porte[:-2] if porte.endswith(".P") else porte
    k = 1 + sum(1 for x in S["unites"] if x.startswith(base + ".c"))
    cid = f"{base}.c{k}"
    (racine / "suivi" / f"{cid}-correction.md").write_text(C.fiche_correction(cid, porte, fautive, titre, realise, verifie), encoding="utf-8")
    ligne = (f"- [ ] **{cid}** · Correction : {titre} · réalise IA {realise} · vérifie IA {verifie} · après — · fiche `suivi/{cid}-correction.md`"
             f" · ajoutée le {C.horodatage()} UTC")
    lignes = texte.splitlines()
    i = S["unites"][porte]["ligne"] - 1
    if not porte.endswith(".P"):
        dep = S["unites"][porte]["apres"] + [cid]
        lignes[i] = C.RE_LIGNE.sub(lambda m: m.group(0).replace(f" · après {m.group(6)} · ", f" · après {', '.join(dep)} · "), lignes[i])
    lignes.insert(i, ligne)
    sp.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    C.git("add", "SUIVI.md", f"suivi/{cid}-correction.md", cwd=racine)
    commit(ia, f"{porte} KO : correction {cid} demandée ({fautive})", racine)
    print(f"CORRECTION AJOUTÉE : {cid}, avant {porte} ; réalise IA {realise}, vérifie IA {verifie}.")


# ---------------------------------------------------------------- arrêt obligatoire

def arreter(ia, raison, unite=None, preuve=None, humain=None):
    """Écrit rapports/ARRET.md sur main, sous le verrou (§5) : tous les créneaux suivants s'arrêtent."""
    au_clone_principal()
    C.fetch()
    if arret_present():
        print("ARRÊT déjà déclaré : rapports/ARRET.md existe sur main.\n" + (C.montrer("origin/main", "rapports/ARRET.md") or ""))
        sys.exit(4)
    detail = ""
    if unite:
        S = suivi_distant()
        if unite not in S["unites"]:
            stop(f"{unite} absente de SUIVI.md", 2)
        code, etapes, rap, ver = etat_distant(S, unite, C.branches_distantes())
        detail = (f"- État de l'unité : {C.LIBELLES[code]} ; auteurs {liste_ia(rap['auteurs'])} ; tentative {rap['tentative']} ; "
                  f"statut {rap['statut'] or '—'} ; branche `{C.branche_de(S['unites'][unite])}` ; fiche `{S['unites'][unite]['fiche']}`\n")
    chemin = C.RACINE.parent / "arret-main"
    sha = prendre_verrou(ia, "Arrêt")
    try:
        C.fetch()
        if arret_present():
            print("ARRÊT déjà déclaré par une autre IA.")
            sys.exit(4)
        recreer_copie(chemin, "--detach", str(chemin), "origin/main")
        ap = chemin / "rapports" / "ARRET.md"
        ap.parent.mkdir(exist_ok=True)
        ap.write_text(f"# Arrêt obligatoire\n\n- Date : {C.horodatage()} UTC\n- Déclaré par : IA {ia}\n- Unité : {unite or '—'}\n"
                      f"- Raison : {raison}\n{detail}- Preuve : {preuve or 'voir le rapport et la fiche de l’unité'}\n"
                      f"- Ce qu'il faut de toi : {humain or 'lire la raison et décider (docs/construction/sequence.md §5)'}\n"
                      f"- Pour relancer les créneaux : python3 suivi/outil.py lever --decision \"<ta décision>\"" + (f" --unite {unite}" if unite else "") + "\n",
                      encoding="utf-8")
        C.git("add", "rapports/ARRET.md", cwd=chemin)
        commit(ia, f"ARRÊT : {raison[:70]}", chemin)
        if not pousser(ia, "main", chemin):
            stop("poussée de rapports/ARRET.md sur main refusée.", 5)
    finally:
        supprimer_copie(chemin)
        lacher_verrou(sha)
    print(f"ARRÊT DÉCLARÉ : rapports/ARRET.md poussé sur main par IA {ia}. Termine ton créneau en citant la raison : {raison}")


def lever(decision, unite=None):
    """Réservée à l'humain : retire rapports/ARRET.md de main, sous le verrou, et, avec --unite, écrit dans le rapport de
    l'unité une ligne « Arrêt levé » datée avec la décision. Les refus et les escalades se recomptent depuis cette ligne :
    l'arrêt ne se redéclenche pas aussitôt."""
    au_clone_principal()
    C.fetch()
    S = suivi_distant()
    if unite and unite not in S["unites"]:
        stop(f"{unite} absente de SUIVI.md", 2)
    ligne = f"- Arrêt levé : {C.horodatage()} UTC par l'humain : {decision}"
    sha = prendre_verrou("humain", "Levée d'arrêt")
    copies = []
    try:
        C.fetch()
        if unite:
            u = S["unites"][unite]
            br = C.branche_de(u)
            if br in C.branches_distantes():
                tmp = C.RACINE.parent / f"levee-{C.stem_de(u)}"
                copies.append(tmp)
                recreer_copie(tmp, "--detach", str(tmp), f"origin/{br}")
                rp = tmp / "rapports" / f"{unite}.md"
                texte = rp.read_text(encoding="utf-8") if rp.exists() else f"# Rapport {unite}\n"
                tete, sep, reste = texte.partition(C.TENTATIVES_PRECEDENTES)
                rp.write_text(tete.rstrip("\n") + "\n" + ligne + "\n" + (sep + reste if sep else ""), encoding="utf-8")
                C.git("add", f"rapports/{unite}.md", cwd=tmp)
                commit("humain", f"{unite} : arrêt levé ({decision[:60]})", tmp)
                if not pousser("humain", br, tmp):
                    stop(f"poussée de la levée sur {br} refusée.", 5)
                print(f"Rapport de {unite} : « Arrêt levé » écrit sur {br}.")
            else:
                print(f"{unite} n'a pas de branche : rien à écrire dans son rapport.")
        if arret_present():
            chemin = C.RACINE.parent / "levee-main"
            copies.append(chemin)
            recreer_copie(chemin, "--detach", str(chemin), "origin/main")
            C.git("rm", "--quiet", "rapports/ARRET.md", cwd=chemin)
            commit("humain", f"Arrêt levé : {decision[:70]}", chemin)
            if not pousser("humain", "main", chemin):
                stop("poussée de main refusée.", 5)
            print("rapports/ARRET.md retiré de main.")
        else:
            print("rapports/ARRET.md absent de main.")
    finally:
        for c in copies:
            supprimer_copie(c)
        lacher_verrou(sha)
    print(f"ARRÊT LEVÉ : {decision}")


# ---------------------------------------------------------------- état pour une IA

def etat(ia):
    au_clone_principal()
    C.fetch()
    if arret_present():
        print("ARRÊT : rapports/ARRET.md existe sur main. Lis-le, ne fais rien d'autre, et termine en citant sa raison.")
        return
    S = suivi_distant()
    dist = C.branches_distantes()
    e = etat_verrou()
    print("verrou de main : " + ("libre" if e is None else f"{e['message']} (depuis {e['age_min']:.0f} min)"))
    t = C.maintenant()
    lignes = {k: [] for k in range(0, 8)}
    compte = {}
    vieux = lambda d: d is not None and (t - d).total_seconds() > C.RELAIS_H * 3600
    for uid, u in S["unites"].items():
        code, etapes, rap, ver = etat_distant(S, uid, dist)
        compte[code] = compte.get(code, 0) + 1
        engagee = not u["coche"] and C.branche_de(u) in dist
        aut = rap["auteurs"] if engagee else []
        R = [x for x in etapes if x["g"] == "R"]
        V = [x for x in etapes if x["g"] == "V"]
        raison = C.arret_requis(code, rap) if engagee else None
        if raison:
            lignes[0].append(f"{uid} {raison} → arreter --ia {ia} --unite {uid} --raison \"{uid} : {raison}\"")
        elif code == "bloquee":
            if ia == C.resolveur(rap) and (ia in aut or len(set(aut)) < 2):
                lignes[1].append(f"{uid} en {rap['statut']} : réponds et reprends → prendre {uid} --ia {ia}")
        elif code == "en_verification":
            if ver["verificateur"] == ia:
                lignes[2].append(f"{uid} : ta vérification en cours, à reprendre → prendre {uid} --ia {ia} --verification")
        elif code in ("a_verifier", "verif_abandonnee") and ia not in aut:
            fin = C.lire_date(R[-1]["date"]) if R and R[-1]["date"] else None
            if code == "verif_abandonnee" or u["v"] == ia or u["v"] in aut:
                lignes[2].append(f"{uid} {C.LIBELLES[code].lower()} (auteur {liste_ia(aut)}) → prendre {uid} --ia {ia} --verification")
            elif vieux(fin):
                lignes[7].append(f"{uid} à vérifier depuis plus de {C.RELAIS_H} h (prévue IA {u['v']}) → prendre {uid} --ia {ia} --verification")
        elif code == "a_fusionner" and ia not in aut:
            if fusion_en_cours(e, uid) and e["age_min"] <= C.VERROU_MIN:
                continue
            if V[-1]["ia"] == ia:
                lignes[3].append(f"{uid} acceptée, à fusionner → fusionner {uid} --ia {ia}")
            elif vieux(C.lire_date(V[-1]["date"])):
                lignes[7].append(f"{uid} acceptée depuis plus de {C.RELAIS_H} h (vérifiée par IA {V[-1]['ia']}) → fusionner {uid} --ia {ia}")
        elif code in ("en_cours", "refusee") and (ia in aut or (code == "refusee" and u["r"] == ia and len(set(aut)) < 2)):
            if not (code == "en_cours" and ia in aut and tenue_par_autre(etapes, rap, ver, ia, t)):
                lignes[4].append(f"{uid} {C.LIBELLES[code].lower()}, à reprendre → prendre {uid} --ia {ia}")
        elif code == "abandonnee":
            if ia in aut or (u["r"] == ia and len(set(aut)) < 2):
                lignes[5].append(f"{uid} abandonnée (plus de {C.ABANDON_H} h sans activité) → prendre {uid} --ia {ia}")
            elif len(set(aut)) < 2:
                lignes[7].append(f"{uid} abandonnée (plus de {C.ABANDON_H} h sans activité, prévue IA {u['r']}) → prendre {uid} --ia {ia}")
        elif code == "prete":
            if u["r"] == ia:
                lignes[6].append(f"{uid} prête : {u['titre']} → prendre {uid} --ia {ia}")
            elif vieux(C.pret_depuis(S, uid)):
                lignes[7].append(f"{uid} prête depuis plus de {C.RELAIS_H} h (prévue IA {u['r']}) → prendre {uid} --ia {ia}")
    titres = {0: "ARRÊT OBLIGATOIRE à déclencher (sequence.md §5)", 1: "Questions et escalades à traiter", 2: "À vérifier",
              3: "À fusionner", 4: "Tes unités à reprendre", 5: "Unités abandonnées de ton rôle", 6: "Unités prêtes pour toi",
              7: "Relais (une autre IA n'est pas passée)"}
    print("unités : " + ", ".join(f"{C.LIBELLES[k].lower()} {v}" for k, v in sorted(compte.items())))
    rien = True
    for k in range(0, 8):
        if lignes[k]:
            rien = False
            print(f"\n{k}. {titres[k]}")
            for l in lignes[k]:
                print("   " + l)
    if lignes[0]:
        print("\nLance la commande d'arrêt de la ligne 0 (python3 suivi/outil.py …), puis termine ton créneau en citant sa raison.")
    elif rien:
        print(f"\nRien pour IA {ia} maintenant. Termine ton créneau en le disant.")
    else:
        print("\nPrends la première ligne : lance python3 suivi/outil.py suivi de sa commande. Si elle répond REFUSÉ, passe à la suivante.")
