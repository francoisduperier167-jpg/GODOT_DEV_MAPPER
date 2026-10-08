#!/usr/bin/env python3
"""Fiches de suivi du mode autonome : génération et vérification.

    python3 suivi/outil.py verifier          contrôle la cohérence de SUIVI.md et des fiches
    python3 suivi/outil.py generer [--force] régénère SUIVI.md et les fiches depuis le guide

La génération refuse d'écraser une fiche où une case est déjà cochée, sauf avec --force.
Bibliothèque standard seulement.
"""
import re
import sys
import pathlib
from collections import OrderedDict

RACINE = pathlib.Path(__file__).resolve().parent.parent
GUIDE = RACINE / "docs" / "construction"
SUIVI_DIR = RACINE / "suivi"
SUIVI_MD = RACINE / "SUIVI.md"
ROLES = {"C": "Concepteur", "D": "Développeur", "V": "Vérificateur"}
DEBUT_GUIDE = "TRAVAIL TECHNIQUE — début de la copie exacte du guide"
FIN_GUIDE = "TRAVAIL TECHNIQUE — fin de la copie exacte du guide"

# ---------------------------------------------------------------- lecture du guide

def _lire(nom):
    return (GUIDE / nom).read_text(encoding="utf-8")


def section_guide(fichier, tache):
    s = _lire(fichier)
    m = re.search(r"^## " + re.escape(tache) + r" — .*$", s, re.M)
    if not m:
        raise SystemExit(f"section {tache} absente de {fichier}")
    reste = s[m.end():]
    n = re.search(r"^## ", reste, re.M)
    return reste[: n.start()] if n else reste


def prompts_guide(fichier, tache):
    return re.findall(r"```text\n(.*?)```", section_guide(fichier, tache), re.S)


def controles_guide(fichier, tache):
    ids = set(re.findall(r"\b(T\d{2}[abc]?-[a-z]\d?)\b", section_guide(fichier, tache)))
    return sorted(ids, key=lambda x: (x.split("-")[0], x.split("-")[1]))


def fichiers_guide(fichier, tache):
    sec = section_guide(fichier, tache)
    m = re.search(r"^(Fichiers autorisés[^\n]*)\n((?:- [^\n]*\n)*)", sec, re.M)
    if not m:
        return None
    return (m.group(1) + "\n" + m.group(2)).strip()


def points_porte(etape):
    s = _lire(f"etape-{etape}.md")
    lignes = re.findall(r"^\| (PC\d+\.\d+b?) \| (.*?) \| (.*) \| (.*?) \|$", s, re.M)
    return lignes


def prompt_porte_guide():
    s = _lire("README.md")
    m = re.search(r"## Prompt de porte d'étape\n\n```text\n(.*?)```", s, re.S)
    return m.group(1)


def prompt_decoupage():
    s = _lire("mvp.md")
    m = re.search(r"## Prompt de découpage d'une phase\n\n```text\n(.*?)```", s, re.S)
    return m.group(1)


def points_phase(fichier, phase):
    s = _lire(fichier)
    m = re.search(r"^## " + re.escape(phase) + r" — (.*)$", s, re.M)
    reste = s[m.end():]
    n = re.search(r"^## ", reste, re.M)
    sec = reste[: n.start()] if n else reste
    p = re.search(r"- \*\*Points de contrôle\.\*\*(.*?)(?=\n- \*\*|\Z)", sec, re.S)
    texte = p.group(1).strip() if p else ""
    puces = [l.strip()[2:] for l in texte.splitlines() if l.strip().startswith("- ")]
    if not puces:
        puces = [x.strip() for x in re.split(r" ; ", texte) if x.strip()]
    return m.group(1).strip(), puces


# ---------------------------------------------------------------- textes communs

GODOT = """GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3"""

REGLES = """RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/{id}.md et les cases de suivi/{f}.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu coches une case seulement quand elle est faite et prouvée. Tu commites et tu pousses après chaque case cochée.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic."""

RAPPORT = """FORMAT DE rapports/{id}.md
- Statut : EN COURS | TERMINÉ | QUESTION | ESCALADE
- Auteur : <ton nom d'IA> · Tentative : n · Créneaux utilisés : n
- Fichiers modifiés : liste
- Contrôles : pour chacun, commande, code de sortie, 10 dernières lignes de sortie
- Contre-épreuves faites : liste
- Écarts au contrat, au guide ou à la fiche : aucun, ou liste
- Hypothèses : aucune, ou liste
- Questions : aucune, ou liste
- Pour la recette : ce qu'un humain devra vérifier, ou « rien »
- Passation : cinq lignes au plus"""

CONTOURNEMENTS = """- test sans assertion, ou toujours vrai ;
   - test désactivé, renommé ou sorti du runner ;
   - valeur attendue recopiée depuis la sortie du code ;
   - marqueur supprimé de tests/pending/ sans test qui passe ;
   - fixture invalide rejetée pour un autre motif que celui de son nom ;
   - API Godot inventée ou non vérifiée ;
   - dépendance interdite entre modules ; API sensible hors de la frontière de compatibilité ;
   - affirmation du rapport sans sortie qui la prouve."""

# ---------------------------------------------------------------- unités

U = OrderedDict()


def unite(id, f, titre, r, v, apres, **k):
    k.update(id=id, f=f, titre=titre, r=r, v=v, apres=apres)
    k.setdefault("kind", "tache")
    k.setdefault("creneaux", 1)
    U[id] = k


# ---- Étape 0
unite("S01", "S01-0A-decisions", "0.A Dossier de décisions", "C", "V", [], etape=0,
      guide=("etape-0.md", "0.A", 0),
      faire=[
          "Créer `docs/DECISIONS.md` : une ligne d'en-tête « Statut : proposé · date », puis un tableau de D-01 à D-09.",
          "Colonnes : ID, question, options (deux ou trois), recommandation, conséquences de chaque option, échéance, statut, date.",
          "Recommandations : D-01 Godot 4.7.2 ; D-03 trois IA, deux créneaux chacune par jour ; D-05 runner maison minimal ; D-07 4.7.2 bloquant, préversion 4.8-dev7 dans un job non bloquant ; D-09 mode autonome (fiches `suivi/`, recette humaine finale).",
          "D-02 : critères de choix du banc d'essai (Godot 4.x en GDScript, au moins deux types d'ennemis qui décident, 30 à 500 scripts, licences du code et des assets qui permettent de redistribuer une copie modifiée). Le banc vivra dans des branches `banc/<nom>-*` de ce dépôt. Le choix se fait en S07.",
          "Statuts : « adoptée par défaut » pour D-01, D-03, D-05, D-07 et D-09 ; « critères adoptés par défaut, choix en S07 » pour D-02 ; « proposée » pour D-04, D-06 et D-08.",
      ],
      fichiers="`docs/DECISIONS.md`",
      R=[
          "Lire `docs/plan-directeur.md` (§0 et §10), `docs/spikes/SPIKE-01.md`, `docs/construction/etape-0.md` (0.A) et `docs/construction/sequence.md`.",
          "Écrire `docs/DECISIONS.md` : en-tête de statut, puis le tableau D-01 à D-09 avec toutes ses colonnes.",
          "Appliquer les statuts de la section « Ce qu'il faut faire ».",
          "Écrire dans le rapport la liste « Pour la recette » : chaque décision adoptée par défaut, une par ligne.",
      ],
      adapt=[
          "Le prompt du guide dit « Tu ne décides rien » et laisse toutes les lignes « proposée ». En mode autonome, tu inscris ensuite les statuts de la fiche : « adoptée par défaut » n'est pas « validée », la confirmation se fait à la recette.",
          "Ajoute D-09, absente du prompt du guide : mode d'exécution autonome, fiches `suivi/`, recette humaine finale.",
      ],
      controles=[
          ("S01-a", "for d in D-01 D-02 D-03 D-04 D-05 D-06 D-07 D-08 D-09; do c=$(grep -cE \"^\\| $d \" docs/DECISIONS.md); [ \"$c\" = 1 ] || echo \"$d : $c\"; done", "aucune sortie"),
          ("S01-b", "for d in D-01 D-03 D-05 D-07 D-09; do grep -E \"^\\| $d \" docs/DECISIONS.md | grep -q \"adoptée par défaut\" || echo \"manque $d\"; done", "aucune sortie"),
          ("S01-c", "grep -E \"^\\| D-0(4|6|8) \" docs/DECISIONS.md | grep -c \"proposée\"", "3"),
      ],
      ce=["(CE) Retirer « adoptée par défaut » de la ligne D-07, relancer S01-b : « manque D-07 » s'affiche ; annuler."],
      coherence="Les recommandations reprennent le plan §0 et §10 et `docs/construction/etape-0.md` ; D-09 reprend `docs/construction/sequence.md`.",
      recette=["Confirmer ou changer chaque décision « adoptée par défaut »."])

unite("S02", "S02-0B-squelettes", "0.B Squelettes et règles des agents", "C", "V", ["S01"], etape=0,
      guide=("etape-0.md", "0.B", 0),
      faire=[
          "Créer `docs/SPEC.md`, `docs/ARCHITECTURE.md` (avec la liste des API sensibles), `docs/CONTRACTS.md` (sept sections C-01 à C-07, sept rubriques chacune, contenu « à rédiger en T07 » ou « en T08 »), `docs/COMPATIBILITY.md`, `docs/TEST_PLAN.md`. Chacun commence par « Statut : proposé · date ».",
          "Créer `PROJECT_STATE.md` : mis à jour seulement à la fusion ; sections Mesures, Dette, Versions de Godot testées, Liste de recette (reprise du §7 de `sequence.md`). L'avancement des unités est dans `SUIVI.md` : ne pas le recopier.",
          "Créer `REGLES_AGENTS.md`, 150 lignes au plus : règles non négociables, règles de cochage des fiches `suivi/`, format de rapport, INV-01 à INV-09 en une ligne chacun, commandes de contrôle vérifiées, renvoi à `sequence.md` et à `SUIVI.md`.",
          "Créer `tools/sync_rules.sh` : copie `REGLES_AGENTS.md` vers `CLAUDE.md` et `GEMINI.md` ; avec `--check`, compare sans écrire et sort en 1 si une copie diffère.",
      ],
      R=[
          "Lire le plan, la méthode, `docs/DECISIONS.md`, `docs/construction/README.md` et `docs/construction/sequence.md`.",
          "Créer les cinq documents normatifs, chacun avec sa ligne de statut.",
          "Créer `PROJECT_STATE.md` selon la fiche (pas de tableau des tâches : il renvoie à `SUIVI.md`).",
          "Créer `REGLES_AGENTS.md` (150 lignes au plus) avec les règles de cochage des fiches `suivi/`.",
          "Créer `tools/sync_rules.sh`, le rendre exécutable, l'exécuter pour produire `CLAUDE.md` et `GEMINI.md`.",
      ],
      adapt=[
          "`PROJECT_STATE.md` ne contient pas le tableau des tâches T00 à T20 demandé par le guide : l'avancement vit dans `SUIVI.md`. Il contient les mesures, la dette, les versions testées et la liste de recette.",
          "`REGLES_AGENTS.md` ajoute les règles de cochage : une case cochée seulement quand elle est faite et prouvée, un push après chaque case, reprise à la première case non cochée.",
      ],
      controles=[
          ("S02-a", "for f in docs/SPEC.md docs/ARCHITECTURE.md docs/CONTRACTS.md docs/COMPATIBILITY.md docs/TEST_PLAN.md PROJECT_STATE.md REGLES_AGENTS.md; do test -s \"$f\" || echo \"manque $f\"; done", "aucune sortie"),
          ("S02-b", "grep -L \"^Statut\" docs/SPEC.md docs/ARCHITECTURE.md docs/CONTRACTS.md docs/COMPATIBILITY.md docs/TEST_PLAN.md", "aucune sortie"),
          ("S02-c", "tools/sync_rules.sh && tools/sync_rules.sh --check; echo $?", "0"),
          ("S02-d", "wc -l < REGLES_AGENTS.md", "150 au plus"),
          ("S02-e", "for c in C-01 C-02 C-03 C-04 C-05 C-06 C-07; do grep -c \"^## $c\" docs/CONTRACTS.md; done", "1 pour chacun"),
          ("S02-f", "grep -c \"SUIVI.md\" REGLES_AGENTS.md PROJECT_STATE.md", "au moins 1 dans chaque fichier"),
      ],
      ce=["(CE) `echo x >> CLAUDE.md; tools/sync_rules.sh --check; echo $?` → 1, puis `tools/sync_rules.sh` pour rétablir."],
      verif_extra=1,
      coherence="Aucune définition à deux endroits ; chaque règle du plan présente et non déformée ; INV-01 à INV-09 complets ; commandes identiques à celles du guide ; décisions de `docs/DECISIONS.md` reprises (prompt de relecture du guide, ci-dessous).",
      recette=[])

unite("S03", "S03-porte-0", "Porte de l'étape 0", "C", "V", ["S02"], kind="porte", etape=0,
      adapt_pc={
          "PC0.1": "Commande adaptée : `for d in D-01 D-05 D-07 D-09; do grep -E \"^\\| $d \" docs/DECISIONS.md | grep -qE \"validée|adoptée par défaut\" || echo \"manque $d\"; done` → aucune sortie.",
          "PC0.7": "Non exécuté en mode autonome : T00 exige ta machine. Noter « non exécuté » ; les tâches de Qwen vont au développeur.",
          "PC0.8": "Preuve : le verdict ACCEPTÉE de S02, qui contient la relecture croisée.",
      })

# ---- Étape 1
unite("S04", "S04-T01", "T01 Squelette du dépôt et plugin activable", "D", "V", ["S03"], etape=1,
      guide=("etape-1.md", "T01", 0),
      faire=[
          "Créer `project.godot` (config_version=5, nom « GODOT_DEV_MAPPER (dev) », section [editor_plugins] qui active le plugin).",
          "Créer `addons/godot_dev_mapper/plugin.cfg` et `plugin.gd` : @tool, extends EditorPlugin, n'affiche GDM_PLUGIN_ENTER et GDM_PLUGIN_EXIT que si GDM_TRACE_LIFECYCLE vaut 1, rien d'autre.",
          "Créer un `README.md` d'une ligne dans chacun des neuf modules (core, protocol, store, projections, ui, editor, persistence, acquisition, compat) et dans `addons/godot_dev_mapper_runtime/`.",
          "Compléter `.gitignore` : `.godot/`, `.godot-bin/`, `*.out`, `sandbox/`.",
      ],
      R=[
          "Obtenir Godot 4.7.2 (bloc GODOT du prompt).",
          "Créer `project.godot`.",
          "Créer `plugin.cfg` et `plugin.gd`.",
          "Créer les dix fichiers `README.md` d'une ligne.",
          "Compléter `.gitignore`.",
          "Faire la contre-épreuve : ajouter `print(undefined_var)` dans `_enter_tree`, relancer T01-b (au moins une ligne SCRIPT ERROR), puis annuler.",
      ],
      coherence="INV-06 (le dossier runtime ne référence pas le plugin) et INV-09 ; `plugin.gd` seul héritier d'EditorPlugin.")

unite("S05", "S05-T02", "T02 Runner de tests et contrôle de dépendances", "D", "V", ["S04"], etape=1,
      guide=("etape-1.md", "T02", 0),
      faire=[
          "Créer `tests/gdm_test.gd` (assertions et comptes) et `tests/run_all.gd` (découverte récursive des `test_*.gd`, marqueurs `tests/pending/`, test sans assertion compté en échec, ligne finale `GDM_TESTS passed=N failed=M pending=K`, code 0 ou 1).",
          "Créer `tests/unit/test_smoke.gd`, `tests/unit/test_selftest.gd`, `tests/pending/README.md`, `tests/README.md`.",
          "Créer `tools/deps_rules.json`, `tools/check_deps.py` (quatre règles, une ligne par violation, code 1 s'il y en a) et `tools/check_deps_fixtures/` (exactement trois violations : règles 1, 3 et 4).",
      ],
      R=[
          "Obtenir Godot 4.7.2.",
          "Écrire `tests/gdm_test.gd`.",
          "Écrire `tests/run_all.gd`.",
          "Écrire `tests/unit/test_smoke.gd` et `tests/unit/test_selftest.gd`.",
          "Écrire `tests/pending/README.md` et `tests/README.md` (dont la règle SCRIPT ERROR pour T03).",
          "Écrire `tools/deps_rules.json` à partir du plan §4 et de `docs/ARCHITECTURE.md`.",
          "Écrire `tools/check_deps.py`.",
          "Créer `tools/check_deps_fixtures/` avec ses trois violations.",
          "Faire la contre-épreuve T02-g (test en attente), puis supprimer ses deux fichiers.",
      ],
      coherence="Matrice de dépendances du plan §4 ; liste des API sensibles de `docs/ARCHITECTURE.md`.")

unite("S06", "S06-T03", "T03 Contrôle unique, lint et CI", "D", "C", ["S05"], etape=1,
      guide=("etape-1.md", "T03", 0),
      faire=[
          "Créer `addons/godot_dev_mapper/compat/versions.json` : `{\"stable\": \"4.7.2-stable\", \"preview\": \"4.8-dev7\"}`, seule source des versions.",
          "Créer `requirements-dev.txt` (gdtoolkit==4.5.0, jsonschema figé), `tools/ci/fetch_godot.sh`, `tools/ci/run_all_checks.sh` (sept étapes, lignes CHECK, ALL_CHECKS OK), `tools/ci/checks.d/README.md`, `tools/ci/known_engine_errors.txt`.",
          "Créer `.github/workflows/ci.yml` : job stable bloquant, job preview avec `continue-on-error: true`.",
      ],
      R=[
          "Écrire `versions.json` et `requirements-dev.txt` ; `pip install -r requirements-dev.txt`.",
          "Écrire `tools/ci/fetch_godot.sh` et le tester sur 4.7.2-stable et 4.8-dev7.",
          "Écrire `tools/ci/run_all_checks.sh`.",
          "Écrire `tools/ci/checks.d/README.md` et `tools/ci/known_engine_errors.txt`.",
          "Écrire `.github/workflows/ci.yml`.",
          "Faire les contre-épreuves T03-c, T03-d, T03-e et T03-i, puis annuler chacune.",
          "CI distante : si le dépôt exécute GitHub Actions, noter le résultat des deux jobs ; sinon, écrire « PC1.8 » dans « Pour la recette ».",
      ],
      coherence="Frontière de compatibilité (plan §4) : les versions ne sont écrites que dans `versions.json` ; `docs/COMPATIBILITY.md`.",
      recette=["PC1.8 si la CI distante n'a pas pu s'exécuter."])

unite("S07", "S07-T04-selection", "T04 Sélection du banc d'essai", "V", "C", ["S01"], etape=1,
      guide=("etape-1.md", "T04", 0),
      faire=[
          "Trouver au plus trois jeux candidats qui remplissent tous les critères de D-02.",
          "Pour chacun, vérifier dans son dépôt, à une révision épinglée (SHA de 40 caractères) : licence du code et licence des assets (fichiers qui le disent), version de Godot d'origine (`project.godot`), nombre de scripts `.gd`, scripts qui contiennent les décisions ciblées, risques de migration.",
          "Écarter tout candidat dont une licence est incertaine ou ne permet pas de redistribuer une copie modifiée : le banc vivra dans des branches de ce dépôt.",
          "Écrire `docs/benches/selection.md` : tableau comparatif avec liens épinglés, recommandation, deux faiblesses principales.",
      ],
      fichiers="`docs/benches/selection.md`. À la fusion seulement, par le concepteur : la ligne D-02 de `docs/DECISIONS.md`.",
      R=[
          "Relire D-02 dans `docs/DECISIONS.md`.",
          "Chercher des candidats (GitHub, bibliothèque d'assets de Godot) et en retenir au plus trois.",
          "Vérifier chaque fait dans le dépôt du candidat, à une révision épinglée ; noter le lien exact de chaque preuve.",
          "Écarter les candidats aux licences incertaines ou incompatibles avec une redistribution modifiée.",
          "Écrire `docs/benches/selection.md`.",
          "Écrire la recommandation et ses deux faiblesses.",
      ],
      adapt=[
          "« Tu choisis » (dans le guide, l'humain) : en mode autonome, le concepteur vérifie ta recommandation contre les critères et l'inscrit en D-02 à la fusion.",
          "Critère ajouté : les licences doivent permettre de redistribuer une copie modifiée, car le banc vivra dans des branches `banc/<nom>-*` de ce dépôt. « Non vérifié » sur une licence écarte le candidat.",
          "Écris le résultat dans `docs/benches/selection.md`, en plus de ta réponse.",
          "Les contrôles T04-a, T04-b et T04-c du guide portent sur la préparation : ils s'exécutent en S08.",
      ],
      ids_guide=False,
      controles=[
          ("S07-a", "test -s docs/benches/selection.md; echo $?", "0"),
          ("S07-b", "grep -Eo \"[0-9a-f]{40}\" docs/benches/selection.md | sort -u | wc -l", "au moins le nombre de candidats"),
          ("S07-c", "grep -i \"licen\" docs/benches/selection.md | grep -ci \"non vérifié\"", "0"),
      ],
      ce=["(CE) Remplacer une licence par « non vérifié » dans le fichier : S07-c donne au moins 1 ; annuler."],
      fusion=["Inscrire dans `docs/DECISIONS.md`, ligne D-02 : « adoptée par défaut : <nom>, <dépôt>@<SHA> », avec la date."],
      coherence="Critères de D-02 et de la fiche T04 ; règle du README du dépôt sur les licences des bancs d'essai.",
      recette=["Confirmer le choix du banc d'essai (D-02)."])

unite("S08", "S08-T04-preparation", "T04 Préparation du banc d'essai", "D", "V", ["S04", "S07"], etape=1,
      guide=("etape-1.md", "T04", 1),
      faire=[
          "Copier le jeu retenu, à sa révision épinglée, dans une branche orpheline `banc/<nom>-base` de ce dépôt (licences et fichiers LICENSE intacts), puis la pousser.",
          "L'importer avec Godot 4.7.2 et corriger seulement ce que la migration exige, une correction par commit, la raison dans le message.",
          "Sur la branche de la tâche : `benches/benches.json`, `tools/check_benches.py`, `docs/benches/<nom>.md`.",
      ],
      fichiers="Sur `tache/S08-T04-preparation` : `benches/benches.json`, `docs/benches/<nom>.md`, `tools/check_benches.py`. Hors de `main` : la branche orpheline `banc/<nom>-base`.",
      R=[
          "Relire D-02 et `docs/benches/selection.md` ; noter le nom court `<nom>`.",
          "Obtenir Godot 4.7.2.",
          "Créer la copie de travail du banc : `git worktree add --detach ../benches/<nom>`, puis dans ce dossier `git checkout --orphan banc/<nom>-base && git rm -rfq .` ; y copier le jeu à la révision épinglée (sans son `.git`) ; commit « Copie de <dépôt>@<SHA> » ; `git push origin banc/<nom>-base`.",
          "Importer : `godot --headless --path ../benches/<nom> --import > /tmp/bench.out 2>&1` ; corriger la migration, un commit par correction ; pousser `banc/<nom>-base`.",
          "Écrire `benches/benches.json` : nom, dépôt, révision d'origine, branche `banc/<nom>-base`, révision migrée, licences, version de Godot d'origine, scripts des décisions ciblées.",
          "Écrire `tools/check_benches.py` (JSON valide avec ces clés ; aucun fichier du jeu suivi par Git sur la branche courante hors de `banc/*`).",
          "Écrire `docs/benches/<nom>.md` : fiche du jeu, décisions observables, corrections de migration.",
          "Faire la contre-épreuve T04-c, puis l'annuler.",
      ],
      adapt=[
          "Le guide clone le jeu hors du dépôt, branche `gdm-base`. En mode autonome, chaque IA arrive dans un environnement neuf : la copie vit dans la branche orpheline `banc/<nom>-base` de ce dépôt, jamais sur `main`. Pour la retrouver : `git fetch origin banc/<nom>-base && git worktree add ../benches/<nom> origin/banc/<nom>-base`.",
          "Partout où le guide écrit `../benches/{nom}` ou `gdm-base`, lire la copie de travail de `banc/<nom>-base`.",
      ],
      coherence="Aucun fichier du jeu sur `main` ; licences reprises de `docs/benches/selection.md`.")

unite("S09", "S09-porte-1", "Porte de l'étape 1", "C", "V", ["S06", "S08"], kind="porte", etape=1,
      adapt_pc={"PC1.8": "Si GitHub Actions ne s'exécute pas sur le dépôt : noter PC1.8 dans la liste de recette ; PC1.7 en local fait foi."})

# ---- Étape 2
unite("S10", "S10-T05-spike01b", "T05 SPIKE-01b, partie éditeur, sous écran virtuel", "C", "V", ["S02"], etape=2,
      guide=("etape-2.md", "T05", None), creneaux=2,
      faire=[
          "Construire dans `spikes/spike01_debugger/editor/` un projet d'éditeur jetable dont le plugin déroule seul le scénario, sous écran virtuel avec rendu logiciel.",
          "Mesurer les six critères de la fiche T05, chacun déclenché par le plugin, et les afficher en lignes PASS ou FAIL par `spikes/spike01_debugger/editor/run.sh`.",
          "Compléter la section SPIKE-01b de `docs/spikes/SPIKE-01.md` et proposer KEEP, REWRITE ou DISCARD.",
      ],
      R=[
          "Lire `docs/spikes/SPIKE-01.md` et `spikes/spike01_debugger/` (jeu et récepteur).",
          "Obtenir Godot 4.7.2 ; vérifier l'écran virtuel : lancer l'éditeur 15 s sous xvfb-run sur `spikes/spike01_debugger/game` et retrouver « OpenGL API » dans la sortie.",
          "Créer le projet d'éditeur jetable : copie du jeu du spike et plugin de pilotage (EditorDebuggerPlugin et EditorPlugin).",
          "Critères 1 et 2 : « prêt » reçu ; « started » avant tout lot.",
          "Critère 3 : stop, « stopped » en 1 s au plus, aucun lot ensuite, puis désactivation du plugin.",
          "Critère 4 : jeu arrêté sans « stopped » → « fin inconnue » ; plugin retiré sans arrêt → bail côté jeu en 2 s au plus.",
          "Critère 5 : cinq lancements successifs sans erreur. Si deux commandes arrivent dans la même frame, remplacer la commande unique de FlowSpike par une file, et le noter : c'est un constat pour C-07.",
          "Critère 6 : débit et cadence à 1 200 et 10 000 événements par seconde, marqués « rendu logiciel, non représentatif d'un GPU ».",
          "Écrire `run.sh` : télécharge Godot au besoin, lance tout sous écran virtuel, affiche une ligne PASS ou FAIL par critère (critère 6 : MESURÉ avec les chiffres).",
          "Compléter la section SPIKE-01b de `docs/spikes/SPIKE-01.md` (critère, déclenchement, observation, chiffre, statut, limites) ; proposer KEEP, REWRITE ou DISCARD ; écrire dans le rapport le changement exact à faire au plan §6, sans l'appliquer.",
      ],
      prompt_perso="""Tu conduis SPIKE-01b du projet GODOT_DEV_MAPPER, la partie éditeur du canal du débogueur. La partie jeu est établie : lis docs/spikes/SPIKE-01.md et spikes/spike01_debugger/.

FAIT VÉRIFIÉ le 8 octobre 2026, dans un conteneur sans GPU :
- l'éditeur Godot 4.7.2 tourne sous xvfb-run avec --rendering-driver opengl3 et un rendu logiciel (llvmpipe) ;
- un plugin peut lancer le jeu avec EditorInterface.play_main_scene() ;
- un EditorDebuggerPlugin reçoit les messages « flowspike:* » et en envoie par EditorDebuggerSession.send_message ;
- le plugin ne reçoit pas les messages du moteur (set_pid, output).
Vérifie de nouveau chaque API avant de t'y fier : EditorDebuggerPlugin (_has_capture, _capture, _setup_session), EditorDebuggerSession.send_message, EditorInterface.play_main_scene, stop_playing_scene, set_plugin_enabled.

CONTRAINTES
- Code jetable dans spikes/spike01_debugger/editor/ uniquement ; rien dans addons/.
- Aucune manipulation humaine : le plugin déclenche chaque scénario.

LES SIX CRITÈRES
1. « prêt » reçu par le plugin.
2. « started » reçu avant tout lot.
3. Arrêt avant la désactivation du plugin : « stopped » reçu en une seconde au plus, et aucun lot ensuite.
4. Coupure : jeu arrêté sans « stopped » → l'éditeur conclut « fin inconnue » ; plugin retiré sans arrêt → le bail arrête la collecte côté jeu en 2 s au plus.
5. Cinq lancements successifs depuis l'éditeur, sans erreur ni fuite.
6. Débit et cadence à 1 200 et 10 000 événements par seconde, avec le rendu logiciel. Marque ces chiffres « non représentatifs d'un GPU ».
Le critère des instances enregistrées avant le démarrage relève du runtime : il est vérifié en T13a, pas ici.

À PRODUIRE
- spikes/spike01_debugger/editor/run.sh : une commande qui rejoue tout et affiche une ligne par critère (PASS, FAIL, ou MESURÉ avec les chiffres pour le critère 6).
- La section SPIKE-01b de docs/spikes/SPIKE-01.md : pour chaque critère, déclenchement, observation, chiffre, statut ; les limites (rendu logiciel, conteneur).
- Une proposition KEEP, REWRITE ou DISCARD ; si nécessaire, le changement exact à faire au plan §6, dans le rapport, sans l'appliquer.""",
      controles=[
          ("S10-a", "GODOT=\"$B\" spikes/spike01_debugger/editor/run.sh", "cinq lignes PASS et une ligne MESURÉ"),
          ("S10-b", "grep -c \"SPIKE-01b\" docs/spikes/SPIKE-01.md", "au moins 1, section avec les six critères"),
          ("T05-a", "Rapport et section SPIKE-01b : six critères, chacun avec déclenchement, observation, chiffre", "complet"),
          ("T05-b", "Le vérificateur rejoue le critère 3 seul avec run.sh", "même observation"),
          ("T05-c", "(CE) Retirer le plugin sans envoyer l'arrêt", "le jeu arrête seul sa collecte en 2 s au plus"),
      ],
      ce=["(CE) Faire envoyer au jeu un lot après « stopped » : le critère 3 passe à FAIL ; annuler.",
          "(CE) Retirer le contrôle du bail côté jeu : le critère 4 passe à FAIL ; annuler."],
      coherence="Constats de SPIKE-01a ; protocole de session du plan §6 ; critères de la fiche T05 de `docs/orchestration.md`.",
      fusion=["Inscrire dans `docs/DECISIONS.md` la décision KEEP, REWRITE ou DISCARD de SPIKE-01b, au statut « adoptée par défaut », avec la date."],
      recette=["Critère 6 de SPIKE-01b sur ta machine, avec GPU."])

unite("S11", "S11-T06-spike02", "T06 SPIKE-02, frontière de compatibilité", "C", "V", ["S06"], etape=2,
      guide=("etape-2.md", "T06", 0),
      faire=[
          "Répondre, preuves à l'appui sur 4.7.2 et sur 4.8-dev7, aux quatre questions : détection de capacités, isolation de compilation, UID des scripts, inventaire des API sensibles.",
          "Écrire `spikes/spike02_compat/run.sh` (rejoue tout pour une version passée en argument) et `docs/spikes/SPIKE-02.md` avec une décision KEEP, REWRITE ou DISCARD sur la règle d'isolation (plan §4) et sur la clé de correspondance (plan §5).",
      ],
      R=[
          "Obtenir les binaires 4.7.2-stable et 4.8-dev7 avec `tools/ci/fetch_godot.sh`.",
          "Q1 Détection de capacités : script, commande, sortie sur les deux versions.",
          "Q2 Isolation de compilation : `--check-only` et exécution réelle sur les deux versions.",
          "Q3 UID des scripts : fichier `.uid`, `ResourceLoader.get_resource_uid`, déplacement avec et sans `.uid`.",
          "Q4 Inventaire des API sensibles de `docs/ARCHITECTURE.md` : tableau par version.",
          "Écrire `spikes/spike02_compat/run.sh`.",
          "Écrire `docs/spikes/SPIKE-02.md` avec les deux décisions.",
      ],
      coherence="Plan §4 (isolation) et §5 (clé de correspondance) ; liste des API sensibles.",
      fusion=["Inscrire dans `docs/DECISIONS.md` les deux décisions de SPIKE-02 (règle d'isolation, clé de correspondance), au statut « adoptée par défaut », avec la date."])

unite("S12", "S12-porte-2", "Porte de l'étape 2", "C", "V", ["S09", "S10", "S11"], kind="porte", etape=2,
      adapt_pc={
          "PC2.4": "Les décisions KEEP, REWRITE ou DISCARD ont été inscrites à la fusion de S10 et de S11, au statut « adoptée par défaut » : vérifier leur présence.",
          "PC2.5": "Diff proposé du plan : appliqué au statut « proposé » si les spikes l'exigent, ou « aucun changement » justifié ; à confirmer à la recette.",
      })

# ---- Étape 3
unite("S13", "S13-T07-contrats", "T07 Contrats C-01, C-02, C-05", "C", "V", ["S09", "S11"], etape=3,
      guide=("etape-3.md", "T07", 0), creneaux=2,
      faire=[
          "Remplir dans `docs/CONTRACTS.md` les sept rubriques de C-01 (identités, cycle de vie, clés de sonde), C-02 (ancrage, révision, lien périmé) et C-05 (modèle minimal, `.flow.json` v1), avec leurs codes d'erreur.",
          "Écrire le schéma `contracts/schemas/declared_graph.v1.schema.json`, les fixtures valides et invalides, `tools/validate_fixtures.py`, `tools/check_contracts.py`, les deux tests de contrat avec leurs marqueurs T10, et les contrôles `checks.d/30-contracts.sh` et `31-fixtures.sh`.",
      ],
      R=[
          "Lire le plan §5 et §10, `docs/spikes/SPIKE-02.md`, `docs/DECISIONS.md`.",
          "Rédiger C-01 dans `docs/CONTRACTS.md` (sept rubriques, codes d'erreur).",
          "Rédiger C-02.",
          "Rédiger C-05.",
          "Écrire le schéma JSON du graphe déclaré.",
          "Écrire les fixtures `valid_*` et `invalid_<CODE>__*` (au moins les cinq invalides de la fiche).",
          "Écrire `tools/validate_fixtures.py` (deux niveaux, `--plan-examples`, `--kinds`, `--file`).",
          "Écrire `tools/check_contracts.py`.",
          "Écrire les deux tests de contrat et leurs marqueurs `tests/pending/` (« T10 »).",
          "Écrire `tools/ci/checks.d/30-contracts.sh` et `31-fixtures.sh`.",
          "Lister en tête du rapport tout écart avec le plan, sans le trancher.",
      ],
      coherence="Plan §5 et §10 ; SPIKE-02 ; règle « un exemple invalide et un test par règle du contrat ».")

unite("S14", "S14-T08-contrats", "T08 Contrats C-03, C-04, C-06, C-07", "C", "V", ["S10", "S12", "S13"], etape=3,
      guide=("etape-3.md", "T08", 0), creneaux=2,
      faire=[
          "Remplir les sept rubriques de C-03 (façades), C-04 (enveloppe et limites), C-06 (Event Store, lacunes, fin inconnue, chemin observé) et C-07 (API FlowTrace, table d'états du protocole de session, frontière de frame, bail, chemin désactivé).",
          "Écrire le schéma de l'enveloppe, ses fixtures, les sessions enregistrées, et les quatre tests de contrat avec leurs marqueurs (T09, T11, T12, T13a).",
      ],
      R=[
          "Lire le plan §4, §6 et §8, `docs/spikes/SPIKE-01.md` (01a et 01b), `docs/spikes/SPIKE-02.md` et C-01 validé.",
          "Rédiger C-03.",
          "Rédiger C-04.",
          "Rédiger C-06.",
          "Rédiger C-07, avec la table d'états complète et le constat de SPIKE-01b sur la file de commandes s'il existe.",
          "Écrire le schéma de l'enveloppe et ses fixtures (au moins les sept invalides de la fiche).",
          "Écrire les sessions enregistrées (au moins les cinq de la fiche).",
          "Écrire les quatre tests de contrat et leurs marqueurs.",
          "Écrire le tableau croisé transition → test de C-07 dans le rapport.",
      ],
      coherence="Plan §4, §6 et §8 ; constats de SPIKE-01a et 01b repris tels quels ; C-01 non modifié.")

unite("S15", "S15-porte-3-gel", "Porte de l'étape 3 et gel des contrats", "C", "V", ["S14"], kind="porte", etape=3,
      fichiers_porte="`docs/CONTRACTS.md` (ligne de statut seulement)",
      adapt_pc={"PC3.8": "Gel en mode autonome : la ligne de statut de `docs/CONTRACTS.md` devient « Statut : adopté par défaut · date ». Toute modification ultérieure passe par une analyse d'impact et un changement de version."},
      recette=["Confirmer le gel des contrats C-01 à C-07."])

# ---- Étape 4
for (sid, f, t, tache, r, v, apres, faire, R, coh) in [
    ("S16", "S16-T09-codec", "T09 Codec et validateur de l'enveloppe", "T09", "D", "V", ["S15"],
     ["Encodage dans `addons/godot_dev_mapper_runtime/envelope.gd`, sans dépendance hors du dossier runtime.",
      "Décodage et validation dans `addons/godot_dev_mapper/protocol/envelope_codec.gd`, avec les codes d'erreur de C-04 (ordre des séquences, taille en octets compris).",
      "Activer les tests T09 en supprimant leurs marqueurs, sans modifier tests ni fixtures."],
     ["Supprimer les marqueurs T09 de `tests/pending/` ; lancer le runner ; coller l'échec.",
      "Implémenter l'encodage dans `envelope.gd`.",
      "Implémenter le décodage et la validation dans `envelope_codec.gd`.",
      "Faire passer les tests sans les modifier.",
      "Prouver l'aller-retour de l'identifiant 9223372036854775807 (T09-c)."],
     "C-04 ; INV-06 pour `envelope.gd`."),
    ("S17", "S17-T10-modele", "T10 Modèle minimal, graphe déclaré, clés de sonde", "T10", "D", "V", ["S16"],
     ["Dans `addons/godot_dev_mapper/core/` : le modèle minimal, le chargeur de `.flow.json` v1 et la table des clés de sonde.",
      "Rejet de chaque fixture invalide avec son code ; références non résolues conservées ; clé inconnue « définition non résolue » ; `core/` sans dépendance."],
     ["Supprimer les marqueurs T10 ; coller l'échec.",
      "Implémenter le modèle minimal (C-01, C-02).",
      "Implémenter le chargeur de `.flow.json` v1 et ses codes d'erreur (C-05).",
      "Implémenter la table des clés de sonde.",
      "Faire passer les tests sans les modifier."],
     "C-01, C-02, C-05 ; `core/` ne dépend d'aucun autre module."),
    ("S18", "S18-T11-store", "T11 Event Store minimal", "T11", "D", "V", ["S17"],
     ["Dans `addons/godot_dev_mapper/store/` : sessions et lacunes, rétention avec marqueur « tronqué avant seq N », fin de session et « fin inconnue », requête « chemin observé » à trois états."],
     ["Supprimer les marqueurs T11 ; coller l'échec.",
      "Implémenter sessions et lacunes.",
      "Implémenter la rétention et le marqueur de troncature.",
      "Implémenter la fin de session et « fin inconnue ».",
      "Implémenter la requête « chemin observé ».",
      "Écrire dans le rapport, pour chaque fixture de session, l'état obtenu et l'état attendu (T11-c)."],
     "C-06 ; INV-04, INV-05, INV-07."),
    ("S19", "S19-T12-facades", "T12 Façades de compatibilité et profil moteur", "T12", "D", "C", ["S15"],
     ["Côté éditeur : façades débogueur et éditeur, profil moteur selon les règles de SPIKE-02.",
      "Côté runtime : `runtime_facade.gd`, avec un transport de substitution pour les tests, sans référence au plugin éditeur.",
      "Les API sensibles n'apparaissent que dans ces fichiers."],
     ["Supprimer les marqueurs T12 ; coller l'échec.",
      "Implémenter `compat/engine_facade.gd`.",
      "Implémenter `compat/engine_profile.gd`.",
      "Implémenter `addons/godot_dev_mapper_runtime/runtime_facade.gd`.",
      "Lancer le runner avec la préversion et coller le résultat (T12-c)."],
     "C-03 ; INV-09 ; règles de SPIKE-02."),
    ("S20", "S20-T13a-flowtrace", "T13a FlowTrace, runtime et protocole de session", "T13a", "D", "C", ["S16", "S19"],
     ["`addons/godot_dev_mapper_runtime/flow_trace.gd` : classe statique FlowTrace, sans autoload, par la façade runtime ; API de C-07, toute la table d'états, bail, réserve de contrôle, pile d'invocations, registre et état initial.",
      "Appliquer les constats de SPIKE-01a (et la file de commandes de SPIKE-01b si elle est au contrat)."],
     ["Supprimer les marqueurs T13a ; coller l'échec.",
      "Implémenter l'API statique et la table d'états.",
      "Implémenter le bail et la réserve de contrôle.",
      "Implémenter la pile d'invocations.",
      "Implémenter le registre des instances et l'état initial.",
      "Écrire `tests/unit/test_flow_trace_internals.gd` (transport de substitution, horloge factice).",
      "Écrire dans le rapport le tableau transition → test (T13a-d)."],
     "C-07, C-04 ; constats de SPIKE-01a ; INV-06."),
    ("S21", "S21-T13b-banc", "T13b Banc sans éditeur et scénarios de coupure", "T13b", "D", "C", ["S20"],
     ["`tools/harness/fake_editor.gd` réécrit depuis le récepteur de SPIKE-01a (port configurable, scénarios).",
      "`tools/harness/demo_game/` : deux instances dont une enregistrée avant le démarrage, une décision.",
      "`tests/integration/run_session.sh` et `tools/ci/checks.d/40-integration.sh`."],
     ["Écrire `tools/harness/fake_editor.gd`.",
      "Écrire `tools/harness/demo_game/`.",
      "Écrire `tests/integration/run_session.sh` (cinq vérifications).",
      "Écrire `tools/ci/checks.d/40-integration.sh`.",
      "Si un scénario révèle un défaut de `flow_trace.gd` : ESCALADE avec le diagnostic (la correction revient à S20 rouverte)."],
     "C-07 ; constats de SPIKE-01a ; aucun lot après « stopped »."),
    ("S22", "S22-T13c-mesures", "T13c Mesures de performance (SPIKE-05)", "T13c", "D", "V", ["S21"],
     ["`tools/bench/flow_trace_cost/` : projet de mesure reproductible, une commande.",
      "`docs/spikes/SPIKE-05.md` : méthode, machine, version, cinq répétitions au moins, chiffres, écarts, conclusion au regard du plan §8."],
     ["Écrire le projet de mesure.",
      "Mesurer le coût d'un appel désactivé, côté appelant compris.",
      "Mesurer le coût de la collecte active à 1 000 événements par seconde, avec et sans collecte.",
      "Répéter au moins cinq fois ; écrire `docs/spikes/SPIKE-05.md`."],
     "Plan §6 (coût du chemin désactivé) et §8 (budgets)."),
]:
    unite(sid, f, t, r, v, apres, etape=4, guide=("etape-4.md", tache, 0), faire=faire, R=R, coherence=coh)

unite("S23", "S23-porte-4", "Porte de l'étape 4", "C", "V", ["S18", "S22"], kind="porte", etape=4,
      adapt_pc={"PC4.6": "Taux d'acceptation au premier essai par IA, calculé depuis `SUIVI.md` et les verdicts."})

# ---- Étape 5
unite("S24", "S24-T14-reception", "T14 Réception côté éditeur", "D", "V", ["S18", "S20"], etape=5,
      guide=("etape-5.md", "T14", 0),
      faire=[
          "`editor/session_controller.gd` en logique pure : protocole de session côté éditeur, « fin inconnue », messages du moteur ignorés, lots validés puis rangés dans l'Event Store ; temps fourni de l'extérieur.",
          "`editor/debugger_bridge.gd`, passerelle mince ; `plugin.gd` : enregistrement et retrait de la passerelle seulement.",
          "`tests/unit/test_session_controller.gd` (rejoue chaque session enregistrée) et `tools/ci/checks.d/50-bridge.sh`.",
      ],
      R=[
          "Écrire `editor/session_controller.gd`.",
          "Écrire `editor/debugger_bridge.gd`.",
          "Modifier `plugin.gd` : enregistrement et retrait de la passerelle.",
          "Écrire `tests/unit/test_session_controller.gd`.",
          "Écrire `tools/ci/checks.d/50-bridge.sh`.",
          "Écrire dans le rapport la procédure de l'essai dans l'éditeur, que S26 exécutera sous écran virtuel.",
      ],
      adapt=["« SUR MA MACHINE, plus tard (PC5.6) » : l'essai se fait en S26, sous écran virtuel. Écris la procédure pour S26."],
      coherence="C-03 (façade débogueur), C-04, C-06, C-07 ; section 01b de SPIKE-01.")

unite("S25", "S25-T15-instrumentation", "T15 Instrumentation du banc d'essai", "D", "V", ["S08", "S21"], etape=5,
      guide=("etape-5.md", "T15", 0),
      faire=[
          "Créer la branche `banc/<nom>-instrumentation` depuis `banc/<nom>-base` : copie de `addons/godot_dev_mapper_runtime/`, deux types d'ennemis instrumentés (register, enter, exit, decision), scène de retrait puis réinsertion d'un ennemi ; la pousser.",
          "Sur la branche de la tâche : `benches/<nom>/flow.json` (6 à 12 éléments), `tools/check_probe_keys.py`, `tests/integration/run_bench.sh`, `docs/benches/<nom>.md`, `tools/ci/checks.d/55-bench.sh`.",
      ],
      fichiers="Sur `tache/S25-T15-instrumentation` : `benches/<nom>/flow.json`, `tools/check_probe_keys.py`, `tests/integration/run_bench.sh`, `docs/benches/<nom>.md`, `tools/ci/checks.d/55-bench.sh`. Hors de `main` : la branche `banc/<nom>-instrumentation`.",
      R=[
          "Copie de travail : `git fetch origin banc/<nom>-base && git worktree add ../benches/<nom> origin/banc/<nom>-base`, puis `git switch -c banc/<nom>-instrumentation` dans ce dossier.",
          "Copier `addons/godot_dev_mapper_runtime/` dans le banc.",
          "Instrumenter les deux types d'ennemis selon les règles d'appel de C-07 ; noter le temps passé par point instrumenté.",
          "Ajouter la scène de retrait puis réinsertion ; pousser `banc/<nom>-instrumentation`.",
          "Écrire `benches/<nom>/flow.json` avec les ancrages vers les fichiers et lignes du jeu.",
          "Écrire `tools/check_probe_keys.py`.",
          "Écrire `tests/integration/run_bench.sh` (récupère la branche du banc s'il le faut).",
          "Écrire `tools/ci/checks.d/55-bench.sh` : OK, KO, ou IGNORÉ si la branche du banc est absente, jamais un faux OK.",
      ],
      adapt=["Partout où le guide écrit `../benches/{nom}` et la branche `gdm-instrumentation`, lire la copie de travail de `banc/<nom>-instrumentation`, poussée sur le dépôt."],
      coherence="C-01, C-05, C-07 (règles d'appel) ; aucune clé orpheline.")

unite("S26", "S26-essai-editeur", "Essai dans l'éditeur sous écran virtuel (PC5.6)", "D", "C", ["S24", "S25"], etape=5,
      faire=[
          "Lancer, sous écran virtuel, l'éditeur avec le plugin sur une copie temporaire du banc instrumenté, jouer une session complète jusqu'à l'Event Store, et comparer les compteurs à ceux du banc sans éditeur.",
          "Enregistrer la session réelle comme fixture de régression (hors des fixtures de contrat).",
      ],
      fichiers="`tests/integration/run_editor_session.sh`, `tools/harness/editor_driver/`, `tests/fixtures/sessions_reelles/`, `tools/ci/checks.d/57-editor.sh`, `docs/benches/<nom>.md` (section « Essai dans l'éditeur »).",
      R=[
          "Écrire `tools/harness/editor_driver/` : un plugin de pilotage qui lance la scène principale, attend la session, l'arrête, puis écrit les compteurs du contrôleur de session (C-06) dans un fichier.",
          "Écrire `tests/integration/run_editor_session.sh` : copie temporaire de `banc/<nom>-instrumentation`, ajout du plugin et du pilote, éditeur sous xvfb-run, comparaison avec les compteurs de `run_bench.sh`.",
          "Enregistrer la session dans `tests/fixtures/sessions_reelles/`.",
          "Écrire `tools/ci/checks.d/57-editor.sh` : OK, KO, ou IGNORÉ si xvfb-run est absent, jamais un faux OK.",
          "Compléter `docs/benches/<nom>.md`, section « Essai dans l'éditeur ».",
      ],
      prompt_perso="""Tu réalises l'essai PC5.6 du projet GODOT_DEV_MAPPER, sans humain : une session du banc d'essai jusqu'au store de l'éditeur réel, sous écran virtuel.
CONTEXTE : docs/construction/etape-5.md (T14, PC5.6), rapport de S24 (procédure), docs/benches/<nom>.md, branche banc/<nom>-instrumentation.
OBJECTIF
1. tools/harness/editor_driver/ : plugin de pilotage, chargé avec le plugin du projet. Il lance la scène principale, attend la fin de la session, l'arrête, puis écrit dans un fichier les compteurs lus par l'API publique du contrôleur de session (C-06) : événements, trous, instances, fin.
2. tests/integration/run_editor_session.sh : prépare une copie temporaire du banc instrumenté, y ajoute addons/godot_dev_mapper/ et le pilote, lance l'éditeur sous xvfb-run, puis compare ces compteurs à ceux de tests/integration/run_bench.sh. Code 0 si les clés et les instances concordent et qu'aucune ligne ERROR n'apparaît.
3. La session reçue est enregistrée dans tests/fixtures/sessions_reelles/ ; elle ne remplace aucune fixture de contrat.
4. tools/ci/checks.d/57-editor.sh : « CHECK editor OK », « KO », ou « IGNORÉ (xvfb-run absent) ».
CONTRÔLES
S26-a  tests/integration/run_editor_session.sh ; echo $?   → 0
S26-b  GODOT="$B" tools/ci/run_all_checks.sh ; echo $?   → 0, CHECK editor OK ou IGNORÉ
CONTRE-ÉPREUVE (CE) pour le vérificateur : faire ignorer les lots par la passerelle → S26-a échoue.""",
      controles=[("S26-a", "tests/integration/run_editor_session.sh; echo $?", "0"),
                 ("S26-b", "GODOT=\"$B\" tools/ci/run_all_checks.sh; echo $?", "0, CHECK editor OK ou IGNORÉ")],
      ce=["(CE) Faire ignorer les lots par `debugger_bridge.gd` : S26-a échoue ; annuler."],
      coherence="Protocole de C-07 côté éditeur ; compteurs cohérents avec le banc sans éditeur.",
      recette=["Une session réelle dans ton éditeur, sur ta machine."])

unite("S27", "S27-porte-5", "Porte de l'étape 5", "C", "V", ["S23", "S26"], kind="porte", etape=5,
      adapt_pc={"PC5.6": "Preuve : le verdict ACCEPTÉE de S26, sous écran virtuel. L'essai sur ta machine passe à la recette."})

# ---- Étape 6
unite("S28", "S28-T16-panneau", "T16 Panneau du POC", "D", "V", ["S17", "S24"], etape=6,
      guide=("etape-6.md", "T16", 0),
      faire=[
          "`projections/journal_projection.gd` en logique pure (filtre par instance, pagination, regroupement par invocation, liste des instances, graphe déclaré en liste).",
          "`ui/poc_panel.tscn` et `poc_panel.gd` : sélecteur d'instance, journal virtualisé, arbre du graphe déclaré, 30 Hz au plus, GDM_PANEL_READY.",
          "Mesures de latence (aller-retour, délai réception → affichage) dans une zone de diagnostic ; tests et `checks.d/60-panel.sh`.",
      ],
      fichiers="`addons/godot_dev_mapper/projections/journal_projection.gd`, `addons/godot_dev_mapper/ui/poc_panel.tscn`, `addons/godot_dev_mapper/ui/poc_panel.gd`, `addons/godot_dev_mapper/editor/debugger_bridge.gd` (horodatage de réception), `addons/godot_dev_mapper/editor/latency_probe.gd` (nouveau : aller-retour), `addons/godot_dev_mapper/plugin.gd` (ajout du panneau), `tests/unit/test_journal_projection.gd`, `tools/ci/checks.d/60-panel.sh`.",
      R=[
          "Écrire `projections/journal_projection.gd`.",
          "Écrire `ui/poc_panel.tscn` et `ui/poc_panel.gd`.",
          "Ajouter l'horodatage de réception dans `debugger_bridge.gd` et l'aller-retour dans `editor/latency_probe.gd`.",
          "Ajouter le panneau dans `plugin.gd`.",
          "Écrire `tests/unit/test_journal_projection.gd` (dont 10 000 événements sous 50 ms et l'horloge factice).",
          "Écrire `tools/ci/checks.d/60-panel.sh`.",
          "Écrire dans le rapport la procédure de captures et de mesure de latence, que S31 exécutera.",
      ],
      adapt=[
          "Les fichiers autorisés sont plus étroits que dans le guide : `editor/session_controller.gd` n'est pas modifié ici, pour que S30 puisse avancer en même temps. L'aller-retour passe par le nouveau fichier `editor/latency_probe.gd`.",
          "« SUR MA MACHINE, plus tard (PC6.7) » : exécuté en S31 sous écran virtuel ; la mesure sur GPU passe à la recette.",
      ],
      coherence="C-05, C-06 ; plan §7 et §8 ; l'interface ne calcule rien.")

unite("S29", "S29-T17-chemin", "T17 Chemin observé et ouverture du code", "D", "V", ["S25", "S28"], etape=6,
      guide=("etape-6.md", "T17", 0),
      faire=[
          "`projections/observed_path.gd` : trois états avec leurs preuves.",
          "`editor/source_opener.gd` : ouverture à la ligne de l'ancrage par la façade éditeur, « lien périmé » si le range_hash diffère.",
          "Tests et fixtures : cohérent, incohérent, trou, sortie manquante, réentrance non garantie, source modifiée.",
      ],
      R=[
          "Écrire `projections/observed_path.gd`.",
          "Écrire `editor/source_opener.gd`.",
          "Brancher l'affichage dans `ui/poc_panel.gd`.",
          "Écrire `tests/unit/test_observed_path.gd` et ses six fixtures.",
          "Écrire dans le rapport, pour chaque fixture, l'état attendu et l'état obtenu (T17-b).",
      ],
      adapt=["« SUR MA MACHINE, plus tard » : le clic qui ouvre le bon fichier est vérifié en S31 sous écran virtuel."],
      coherence="C-02 (range_hash), C-06 (chemin observé) ; plan §6 ; jamais « cause ».")

unite("S30", "S30-T18-robustesse", "T18 Robustesse et cycle de vie", "D", "C", ["S21", "S24"], etape=6,
      guide=("etape-6.md", "T18", 0),
      faire=["`tests/integration/run_lifecycle.sh` : six scénarios (sans débogueur, cinq démarrages et arrêts, coupure du récepteur, jeu tué, désactivation simulée, redémarrage), et `checks.d/65-lifecycle.sh`.",
             "Corriger un défaut sans changer de contrat ; sinon QUESTION avec le diagnostic."],
      R=[
          "Scénario 1 : jeu sans débogueur.",
          "Scénario 2 : cinq démarrages et arrêts.",
          "Scénario 3 : coupure du récepteur.",
          "Scénario 4 : jeu tué (kill -9).",
          "Scénario 5 : désactivation du plugin simulée sur le contrôleur.",
          "Scénario 6 : jeu redémarré, nouvelle session.",
          "Écrire `tools/ci/checks.d/65-lifecycle.sh`.",
      ],
      adapt=["« SUR MA MACHINE, plus tard » : la désactivation du plugin pendant une vraie collecte passe à la recette."],
      coherence="Plan §8 (trois opérations du cycle de vie) ; C-07.",
      recette=["Désactiver le plugin pendant une vraie collecte, dans ton éditeur."])

unite("S31", "S31-demonstration", "Démonstration sous écran virtuel (PC6.7)", "D", "V", ["S28", "S29", "S30"], etape=6,
      faire=[
          "Sous écran virtuel, ouvrir l'éditeur avec le plugin sur le banc instrumenté, jouer une session, et produire des captures du panneau : deux instances distinguées, trois états du chemin observé, ouverture du code à la bonne ligne.",
          "Mesurer l'aller-retour et le délai réception → affichage, marqués « rendu logiciel ».",
      ],
      fichiers="`tests/integration/run_demo.sh`, `tools/harness/editor_driver/` (scénario de démonstration), `rapports/S31/` (captures PNG), `docs/mesures/latence-poc.md`.",
      R=[
          "Étendre `tools/harness/editor_driver/` : sélection d'instance, choix d'une invocation, ouverture du code, capture du viewport de l'éditeur.",
          "Écrire `tests/integration/run_demo.sh`.",
          "Produire les captures dans `rapports/S31/` : deux instances, trois états (fixtures « cohérent », « trou », « incohérent »), code ouvert à la bonne ligne.",
          "Écrire `docs/mesures/latence-poc.md` : aller-retour, délai réception → affichage, 95e centile, mention « rendu logiciel ».",
      ],
      prompt_perso="""Tu réalises la démonstration PC6.7 du projet GODOT_DEV_MAPPER, sans humain, sous écran virtuel.
CONTEXTE : docs/construction/etape-6.md (PC6.7, T16, T17), rapports de S28 et S29 (procédures), tools/harness/editor_driver/ (S26).
OBJECTIF
1. Étendre tools/harness/editor_driver/ : une fois la session reçue, sélectionner chaque instance, choisir une invocation, ouvrir le code par le panneau, et capturer le viewport de l'éditeur (get_viewport().get_texture().get_image().save_png) dans rapports/S31/.
2. tests/integration/run_demo.sh : lance tout sous xvfb-run, sur une copie temporaire de banc/<nom>-instrumentation, et affiche la ligne de script ouverte par l'éditeur (« OPEN res://…:ligne »).
3. Captures attendues : deux instances distinguées ; un chemin « cohérent », un « indéterminé — trace incomplète » (session à trou rejouée), un « incohérent » (fixture) ; le code ouvert à la ligne de l'ancrage.
4. docs/mesures/latence-poc.md : aller-retour et délai réception → affichage, 95e centile sur la session, latence estimée ; mention « rendu logiciel, non représentatif d'un GPU ».
CONTRÔLES
S31-a  tests/integration/run_demo.sh ; echo $?   → 0 et une ligne OPEN avec la ligne de l'ancrage
S31-b  ls rapports/S31/*.png | wc -l   → au moins 4
CONTRE-ÉPREUVE (CE) pour le vérificateur : faire ignorer le filtre d'instance au panneau → la capture des deux instances ne les distingue plus, et le test de projection échoue.""",
      controles=[("S31-a", "tests/integration/run_demo.sh; echo $?", "0 et une ligne OPEN avec la ligne de l'ancrage"),
                 ("S31-b", "ls rapports/S31/*.png | wc -l", "au moins 4")],
      ce=["(CE) Ignorer le filtre d'instance dans la projection : le test de projection échoue et la capture ne distingue plus les instances ; annuler."],
      verif_note="Le vérificateur ouvre chaque capture et décrit ce qu'il voit dans son verdict.",
      coherence="Plan §7 (pas de graphe dessiné au POC) ; états jamais portés par la seule couleur ; jamais « cause ».",
      recette=["Démonstration et latence sur ta machine, avec GPU ; jugement visuel du panneau."])

unite("S32", "S32-porte-6", "Porte de l'étape 6", "C", "V", ["S27", "S31"], kind="porte", etape=6,
      adapt_pc={"PC6.7": "Preuve : le verdict ACCEPTÉE de S31 (captures et latence sous rendu logiciel). La mesure sur GPU passe à la recette."})

# ---- Étape 7
unite("S33", "S33-T19-injection", "T19 Injection de trois bugs", "V", "C", ["S25"], etape=7,
      guide=("etape-7.md", "T19", 0),
      faire=[
          "Créer trois branches `banc/<nom>-bug-1` à `-bug-3` depuis `banc/<nom>-instrumentation`, un seul bug par branche, de difficulté comparable, sans toucher aux appels FlowTrace ni au graphe déclaré ; les pousser.",
          "Écrire l'enveloppe scellée dans une branche orpheline `banc/<nom>-enveloppe`, et seulement les symptômes dans `rapports/S33.md`.",
      ],
      fichiers="`rapports/S33.md` (symptômes et déclenchement seulement). Hors de `main` : les branches `banc/<nom>-bug-1` à `-bug-3` et `banc/<nom>-enveloppe`.",
      R=[
          "Copie de travail de `banc/<nom>-instrumentation`.",
          "Créer `banc/<nom>-bug-1` avec son bug ; vérifier que le symptôme se reproduit ; pousser.",
          "Créer `banc/<nom>-bug-2` ; vérifier ; pousser.",
          "Créer `banc/<nom>-bug-3` ; vérifier ; pousser.",
          "Écrire `ENVELOPPE_SCELLEE.md` dans la branche orpheline `banc/<nom>-enveloppe` ; pousser.",
          "Écrire dans `rapports/S33.md` seulement la branche, le symptôme et le déclenchement de chaque bug.",
      ],
      adapt=[
          "Les branches `gdm-bug-N` du guide deviennent `banc/<nom>-bug-N`, poussées sur le dépôt ; l'enveloppe vit dans la branche orpheline `banc/<nom>-enveloppe`.",
          "Règle pour toutes les IA : celle qui réalisera S34 ne récupère pas `banc/<nom>-enveloppe` avant d'avoir fini ses trois diagnostics.",
          "Contrôles du guide : T19-a (chaque branche reproduit son symptôme) est vérifié ici ; T19-b, T19-c et T19-d le sont en S34.",
      ],
      ids_guide=False,
      controles=[("S33-a", "git ls-remote origin \"refs/heads/banc/*-bug-*\" | wc -l", "3"),
                 ("T19-a", "Chaque branche de bug reproduit son symptôme seule, vérifié par le vérificateur", "trois symptômes reproduits"),
                 ("S33-b", "grep -cE \"\\.gd:[0-9]+\" rapports/S33.md", "0 (aucune cause divulguée)")],
      ce=["(CE) Ajouter une ligne « fichier.gd:12 » dans `rapports/S33.md` : S33-b donne 1 ; annuler."],
      coherence="Règles des bugs de la fiche T19 : une cause, difficulté comparable, natures variées.")

unite("S34", "S34-T19-diagnostic", "T19 Mesure de valeur par substitution", "D", "V", ["S32", "S33"], etape=7, creneaux=2,
      faire=[
          "Préparer `fake_editor.gd --record` et `tools/gdm_query.gd`, puis diagnostiquer les trois bugs : 1 avec l'outil, 2 sans, 3 avec, sans avoir lu l'enveloppe.",
          "Compter pour chaque bug les exécutions, lectures, modifications temporaires et le temps ; proposer la cause ; ouvrir l'enveloppe seulement après ; écrire `docs/mesures/valeur-poc-substitution.md`.",
          "Appliquer le critère d'arrêt : si l'outil n'a aidé sur aucun des bugs 1 et 3, écrire `rapports/ARRET.md`.",
      ],
      fichiers="`tools/harness/fake_editor.gd` (option `--record`), `tools/gdm_query.gd`, `docs/mesures/valeur-poc-substitution.md`.",
      R=[
          "Ajouter l'option `--record` à `tools/harness/fake_editor.gd` (session en JSONL).",
          "Écrire `tools/gdm_query.gd` : relit la session avec `store/` et `projections/`, affiche le journal d'une instance et le chemin observé de ses invocations.",
          "Bug 1, avec l'outil : diagnostic et comptes.",
          "Bug 2, sans l'outil : diagnostic et comptes.",
          "Bug 3, avec l'outil : diagnostic et comptes.",
          "Ouvrir l'enveloppe (`git fetch origin banc/<nom>-enveloppe`) ; noter l'heure ; comparer les causes.",
          "Écrire `docs/mesures/valeur-poc-substitution.md` (signal pour un agent, pas pour une personne, écrit en tête).",
          "Appliquer le critère d'arrêt.",
      ],
      prompt_perso="""Tu mesures, par substitution, l'utilité du POC du projet GODOT_DEV_MAPPER. Tu n'as pas lu ENVELOPPE_SCELLEE.md et tu ne récupères pas la branche banc/<nom>-enveloppe avant la fin des trois diagnostics.

PRÉPARE (fichiers autorisés : tools/harness/fake_editor.gd, tools/gdm_query.gd, docs/mesures/valeur-poc-substitution.md)
- --record enregistre la session reçue, lot par lot, dans un fichier JSONL.
- tools/gdm_query.gd relit ce fichier avec store/ et projections/, et affiche le journal d'une instance et le chemin observé de ses invocations.

MESURE, sur les branches banc/<nom>-bug-1 à -bug-3, dans cet ordre, avec les symptômes de rapports/S33.md :
- bug 1 avec l'outil : code du jeu, console du jeu, session enregistrée, sorties de gdm_query, captures du panneau sous écran virtuel si utile ;
- bug 2 sans l'outil : code du jeu et console du jeu seulement ; tu peux ajouter des print ;
- bug 3 avec l'outil.
Pour chaque bug, note : le nombre d'exécutions du jeu, de lectures de fichier et de modifications temporaires ; le temps écoulé ; la cause proposée, avec le fichier et la ligne ; ta confiance.
Ensuite seulement, récupère l'enveloppe, note l'heure, et note pour chaque bug si la cause est exacte.

RAPPORT dans docs/mesures/valeur-poc-substitution.md : le tableau de T19 adapté (colonnes : bug, branche, avec l'outil, préparation, exécutions, lectures, modifications, temps, cause proposée, confiance, cause exacte), puis une conclusion qualitative. Écris en tête : « Signal mesuré pour un agent, pas pour une personne ; la mesure humaine se fait à la recette. »

CRITÈRE D'ARRÊT : l'outil a aidé sur un bug s'il a permis de trouver la cause exacte avec moins d'exécutions qu'au bug 2, ou là où le bug 2 n'a pas été trouvé. S'il n'a aidé ni sur le bug 1 ni sur le bug 3, écris rapports/ARRET.md (raison, preuves, ce qu'il faut de l'humain), pousse-le sur main et arrête-toi.""",
      controles=[("S34-a", "grep -c \"pas pour une personne\" docs/mesures/valeur-poc-substitution.md", "1"),
                 ("T19-a", "Chaque branche de bug reproduit son symptôme seule", "trois symptômes reproduits"),
                 ("T19-b", "Heure d'ouverture de l'enveloppe notée après le dernier diagnostic", "présente"),
                 ("T19-c", "Tableau et conclusion complets, durées marquées indicatives", "aucune case vide"),
                 ("T19-d", "Le vérificateur relit le tableau contre l'enveloppe", "concordance des causes")],
      ce=["(CE) Le vérificateur relance `tools/gdm_query.gd` sur une session à trou : le chemin observé est « indéterminé »."],
      coherence="Fiche T19 ; plan §9 (mesure exploratoire, critère d'arrêt).",
      recette=["Mesure de valeur humaine (T19 du guide), sur trois nouveaux bugs."])

unite("S35", "S35-T20-revue", "T20 Revue de continuation et décision", "C", "V", ["S34"], etape=7,
      guide=("etape-7.md", "T20", 0),
      faire=[
          "Écrire `docs/revues/revue-poc.md` : budgets en créneaux, fiabilité par IA, signal d'utilité par substitution, risques, options, décisions à prendre, proposition d'amendement PD-0.6.",
          "Décider selon la règle : continuer si le signal est positif, si aucun arrêt n'est ouvert et si les créneaux consommés restent sous le double de l'estimation ; sinon écrire `rapports/ARRET.md`.",
          "Appliquer l'amendement PD-0.6 au statut « proposé ».",
      ],
      fichiers="`docs/revues/revue-poc.md`, `docs/plan-directeur.md` (amendement PD-0.6, statut « proposé »). À la fusion : la décision dans `docs/DECISIONS.md`.",
      R=[
          "Rassembler `SUIVI.md`, `PROJECT_STATE.md`, les verdicts, `docs/mesures/valeur-poc-substitution.md`, `docs/spikes/`.",
          "Écrire les sections 1 à 6 de la revue.",
          "Appliquer la règle de décision et l'écrire dans la revue.",
          "Écrire et appliquer l'amendement PD-0.6, au statut « proposé ».",
          "Si la décision est de s'arrêter : écrire `rapports/ARRET.md`.",
      ],
      adapt=[
          "« Tu ne décides pas : la décision est humaine » : en mode autonome, tu appliques la règle de décision de la fiche, et la décision est inscrite « adoptée par défaut ».",
          "Budgets : en créneaux d'IA (estimation de `sequence.md` §8), et non en heures humaines.",
          "SPIKE-04 : si la reprise d'AST Flow est recommandée, c'est une nouvelle dépendance, à décider par l'humain ; le MVP continue avec l'extraction maison en attendant.",
      ],
      fusion=["Inscrire la décision du POC dans `docs/DECISIONS.md`, au statut « adoptée par défaut »."],
      coherence="Plan §9 (portes, critères d'arrêt) ; `sequence.md` §5 et §8.",
      recette=["Confirmer la décision de continuer, et l'amendement PD-0.6."])

# ---- MVP et V1 : découpage, tâches ajoutées par le découpage, porte de phase
PHASES = [
    ("S36", "P4a", "mvp.md", ["S35"]),
    ("S37", "P4b", "mvp.md", ["S36.P"]),
    ("S38", "P5", "mvp.md", ["S37.P"]),
    ("S39", "P6", "mvp.md", ["S35"]),
    ("S40", "P7", "mvp.md", ["S39.P"]),
    ("S41", "P8", "mvp.md", ["S38.P", "S40.P"]),
    ("S42", "P9", "v1.md", ["S41.P"]),
    ("S43", "P10", "v1.md", ["S41.P"]),
    ("S44", "P11", "v1.md", ["S41.P"]),
    ("S45", "P12", "v1.md", ["S42.P", "S43.P"]),
    ("S46", "P13", "v1.md", ["S44.P", "S45.P"]),
    ("S47", "P14", "v1.md", ["S41.P"]),
    ("S48", "P15", "v1.md", ["S46.P"]),
    ("S49", "P16", "v1.md", ["S47.P", "S48.P"]),
]
for sid, ph, fich, apres in PHASES:
    titre, points = points_phase(fich, ph)
    unite(sid, f"{sid}-{ph}-decoupage", f"{ph} {titre} : découpage", "C", "V", apres, kind="phase",
          phase=ph, fichier_phase=fich, creneaux=1)
    unite(f"{sid}.P", f"{sid}.P-{ph}-porte", f"Porte de {ph}" + (" et porte du MVP" if ph == "P8" else " et porte de la V1" if ph == "P16" else ""),
          "C", "V", [sid, f"{sid}.*"], kind="porte_phase", phase=ph, fichier_phase=fich, points=points)


# ---------------------------------------------------------------- graphe

def deps_reelles(uid):
    out = []
    for d in U[uid]["apres"]:
        if d.endswith(".*"):
            base = d[:-2]
            out += [x for x in U if x.startswith(base + ".") and x != base + ".P"]
        else:
            out.append(d)
    return out


def ancetres(uid, memo={}):
    if uid in memo:
        return memo[uid]
    a = set()
    for d in deps_reelles(uid):
        a.add(d)
        a |= ancetres(d)
    memo[uid] = a
    return a


def independantes(uid):
    a = ancetres(uid)
    desc = {x for x in U if uid in ancetres(x)}
    return [x for x in U if x != uid and x not in a and x not in desc]


def niveaux():
    niv = {}
    for uid in U:
        niv[uid] = 1 + max([niv[d] for d in deps_reelles(uid)], default=0)
    return niv


def cochees(ids):
    return f"{', '.join(ids)} {'est cochée' if len(ids) == 1 else 'sont cochées'}"


def fmt_ids(ids, limite=None):
    if not ids:
        return "aucune"
    ids = list(ids)
    if limite and len(ids) > limite:
        return ", ".join(ids[:limite]) + f", et {len(ids) - limite} autres (voir SUIVI.md)"
    return ", ".join(ids)


# ---------------------------------------------------------------- rendu d'une fiche

def ligne_ctrl(c):
    return f"{c[0]}  {c[1]}   → {c[2]}"


def rendre(u):
    id, f = u["id"], u["f"]
    kind = u["kind"]
    apres = u["apres"]
    indep = independantes(id)
    br = f"tache/{f}"
    L = []
    L.append(f"# {id} — {u['titre']}\n")
    L.append("> Fiche d'exécution du mode autonome. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse : une autre IA doit pouvoir reprendre à la première case non cochée. Règles : `docs/construction/sequence.md`. Avancement global : `SUIVI.md`.\n")
    L.append("| Champ | Valeur |\n| --- | --- |")
    L.append(f"| Réalise | {ROLES[u['r']]} |")
    L.append(f"| Vérifie | {ROLES[u['v']]} (jamais l'auteur) |")
    L.append(f"| Commence après | {fmt_ids(apres) + ' (cochées dans `SUIVI.md`)' if apres else 'rien : peut commencer tout de suite'} |")
    L.append(f"| Indépendante de | {fmt_ids(indep, 14)} |")
    L.append(f"| Branche | `{br}` |")
    if u.get("guide"):
        L.append(f"| Fiche de conception | `docs/construction/{u['guide'][0]}`, section {u['guide'][1]} |")
    elif kind == "porte":
        L.append(f"| Fiche de conception | `docs/construction/etape-{u['etape']}.md`, points de contrôle |")
    elif kind in ("phase", "porte_phase"):
        L.append(f"| Fiche de conception | `docs/construction/{u['fichier_phase']}`, section {u['phase']} |")
    L.append(f"| Estimation | {u['creneaux']} créneau{'x' if u['creneaux'] > 1 else ''} |\n")
    L.append("**Séquentiel ou indépendant.** Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité elle-même peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.\n")

    if kind == "porte":
        L += rendre_porte(u, br)
    elif kind == "phase":
        L += rendre_phase(u, br)
    elif kind == "porte_phase":
        L += rendre_porte_phase(u, br)
    else:
        L += rendre_tache(u, br)

    L.append("## Pour la recette\n")
    rec = u.get("recette") or []
    L.append("\n".join(f"- {r}" for r in rec) if rec else "Rien de propre à cette unité.")
    L.append("")
    return "\n".join(L)


def bloc_entete(u, br):
    return (f"Tu es <ton nom d'IA>, au rôle {ROLES[u['r']]}. Tu réalises l'unité {u['id']} « {u['titre']} » du projet GODOT_DEV_MAPPER "
            f"(plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.\n\n"
            f"AVANT TOUT\n"
            f"1. git fetch origin. Lis REGLES_AGENTS.md s'il existe, puis la fiche suivi/{u['f']}.md.\n"
            f"2. Si la branche origin/{br} existe : reprends-la, relis rapports/{u['id']}.md et commence à la première sous-étape R non cochée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.\n"
            f"3. Sinon : " + (f"vérifie dans SUIVI.md, sur main, que {cochees(u['apres'])}, puis crée {br} depuis main.\n" if u['apres'] else f"crée {br} depuis main (aucun prérequis).\n"))


def bloc_fin(u, br):
    return (f"FIN DE CRÉNEAU, même si l'unité n'est pas finie\n"
            f"- Coche dans suivi/{u['f']}.md les sous-étapes faites et prouvées ; complète rapports/{u['id']}.md (sorties, section « Passation ») ; commite ; git push origin {br}.\n"
            f"- Ne laisse aucune modification non poussée.\n\n" + RAPPORT.replace("{id}", u["id"]))


def r0(u, br):
    return (f"R0 Prise en charge : `git fetch origin` ; {cochees(u['apres']) + ' dans `SUIVI.md`' if u['apres'] else 'aucun prérequis'} ; "
            f"branche `origin/{br}` absente, ou sans commit depuis deux créneaux, ou dernier verdict REFUSÉE ; créer ou reprendre la branche ; "
            f"`rapports/{u['id']}.md` avec « Statut : EN COURS » et « Auteur » ; commit ; push.")


def rfin(u, ids):
    return (f"R{len(u.get('R', [])) + 1} Contrôles finaux : {', '.join(ids) if ids else 'contrôles de la fiche'} exécutés dans une copie propre, sorties collées dans le rapport ; "
            "`tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » ; commit ; push.")


def fusion_steps(u, br):
    F = [f"F1 `git switch main && git pull --ff-only && git merge --no-ff origin/{br} -m \"Fusion {u['id']} : {u['titre']}\"`.",
         "F2 Sur `main` : `GODOT=\"$B\" tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK. Sinon : `git reset --hard ORIG_HEAD`, verdict « REFUSÉE (fusion) » poussé sur la branche, et arrêt de la fusion.",
         f"F3 Dans `SUIVI.md`, cocher la ligne **{u['id']}** et compléter « fait le <date> · auteur <IA> · vérifié par <IA> · <n> créneaux »."]
    for x in u.get("fusion", []):
        F.append(f"F{len(F) + 1} {x}")
    F.append(f"F{len(F) + 1} `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette.")
    F.append(f"F{len(F) + 1} Cocher les sous-étapes F de cette fiche ; `git commit` ; `git push origin main` (en cas de refus : `git pull --rebase`, puis push).")
    return F


def verif_prompt(u, br, ids, extra=""):
    return (f"Tu es <ton nom d'IA>, au rôle {ROLES[u['v']]}, vérificateur indépendant de l'unité {u['id']} « {u['titre']} » du projet GODOT_DEV_MAPPER.\n"
            f"Tu n'en es pas l'auteur : lis la ligne « Auteur » de rapports/{u['id']}.md ; si c'est toi, arrête-toi.\n"
            f"Tu ne modifies aucun fichier de l'unité. Tu écris ton verdict et tu coches les sous-étapes V, sur la branche.\n\n"
            f"COPIE NEUVE : git fetch origin && git worktree add --detach ../verif-{u['f']} origin/{br}\n"
            f"GODOT : même procédure que le prompt de réalisation.\n\n"
            f"1. PÉRIMÈTRE. git diff --name-only origin/main...origin/{br}. Autorisés : les « Fichiers autorisés » de la fiche, rapports/{u['id']}*.md et suivi/{u['f']}.md. Tout autre fichier : refus.\n"
            f"2. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : {', '.join(ids) if ids else 'ceux de la fiche'}.\n"
            f"3. CONTRE-ÉPREUVES. Applique chaque sabotage marqué (CE) dans la fiche et dans le travail technique ; vérifie que le contrôle échoue ; annule avec git checkout -- . && git clean -fd.\n"
            f"4. CONTOURNEMENTS. Cherche :\n   {CONTOURNEMENTS}\n"
            f"5. COHÉRENCE. {u.get('coherence', 'Contrat et invariants concernés.')}\n"
            + (extra + "\n" if extra else "") +
            f"\nVERDICT dans rapports/{u['id']}-verif-<tentative>.md :\n"
            f"- Verdict : ACCEPTÉE | REFUSÉE\n- Contrôles relancés : commande, code, attendu, obtenu\n- Contre-épreuves : sabotage, contrôle, détecté oui ou non\n"
            f"- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon\n- Doutes non bloquants : liste courte\n"
            f"Pousse le verdict sur la branche. Si ACCEPTÉE, fais les sous-étapes F de la fiche. Si REFUSÉE, arrête-toi : une IA au rôle de l'auteur reprendra.")


def rendre_tache(u, br):
    L = []
    g = u.get("guide")
    ids_guide = controles_guide(g[0], g[1]) if g and u.get("ids_guide", True) else []
    ctrls = u.get("controles", [])
    ids = [c[0] for c in ctrls] + [x for x in ids_guide if x not in [c[0] for c in ctrls]]
    if g and g[2] is not None and not u.get("prompt_perso"):
        tech = prompts_guide(g[0], g[1])[g[2]].rstrip("\n")
    else:
        tech = u["prompt_perso"].rstrip("\n")
    L.append("## Ce qu'il faut faire\n")
    L += [f"- {x}" for x in u["faire"]]
    L.append("\n## Fichiers autorisés\n")
    if u.get("fichiers"):
        L.append(u["fichiers"])
    elif g:
        L.append(re.sub(r"^Fichiers autorisés( dans le dépôt)? :\s*", lambda m: "Dans le dépôt : " if m.group(1) else "", fichiers_guide(g[0], g[1]) or "Voir la fiche du guide."))
    L.append("\nToujours autorisés en plus : `rapports/" + u["id"] + "*.md` et les cases de cette fiche.\n")
    if ctrls or u.get("ce"):
        L.append("## Contrôles propres à cette fiche\n")
        L += [f"- `{c[0]}` : `{c[1]}` → {c[2]}" if not c[1].startswith(("Rapport", "Le vérificateur", "(CE)", "Chaque", "Heure", "Tableau")) else f"- `{c[0]}` : {c[1]} → {c[2]}" for c in ctrls]
        L += [f"- {x}" for x in u.get("ce", [])]
        L.append("")
    L.append("## Prompt de réalisation\n")
    p = bloc_entete(u, br) + "\n" + GODOT + "\n\n" + REGLES.replace("{id}", u["id"]).replace("{f}", u["f"]) + "\n\n"
    p += DEBUT_GUIDE + (f" (docs/construction/{g[0]}, {g[1]})" if g and g[2] is not None and not u.get("prompt_perso") else " (rédigé pour le mode autonome)") + "\n"
    p += tech + "\n" + FIN_GUIDE + "\n\n"
    if ctrls:
        p += "CONTRÔLES DE LA FICHE\n" + "\n".join(ligne_ctrl(c) for c in ctrls) + "\n"
        if u.get("ce"):
            p += "\n".join(u["ce"]) + "\n"
        p += "\n"
    p += "ADAPTATIONS DU MODE AUTONOME\n" + ("\n".join(f"- {a}" for a in u.get("adapt", [])) or "- Aucune : suis le travail technique tel quel.") + "\n\n"
    p += "SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.\n\n" + bloc_fin(u, br)
    L.append("```text\n" + p + "\n```\n")
    L.append("## Sous-étapes de réalisation\n")
    L.append(f"- [ ] {r0(u, br)}")
    for i, x in enumerate(u["R"], 1):
        L.append(f"- [ ] R{i} {x}")
    L.append(f"- [ ] {rfin(u, ids)}\n")
    L.append("## Prompt de vérification\n")
    extra = u.get("verif_note", "")
    if u.get("verif_extra") is not None and g:
        extra = (extra + "\n" if extra else "") + "RELECTURE CROISÉE, prompt du guide :\n" + prompts_guide(g[0], g[1])[u["verif_extra"]].rstrip("\n")
    L.append("```text\n" + verif_prompt(u, br, ids, extra) + "\n```\n")
    L.append("## Sous-étapes de vérification\n")
    L.append(f"- [ ] V1 Prise en charge : pas l'auteur ; copie neuve `../verif-{u['f']}` sur `origin/{br}`.")
    L.append(f"- [ ] V2 Périmètre : `git diff --name-only origin/main...origin/{br}` ⊂ fichiers autorisés.")
    for i, x in enumerate(ids, 1):
        L.append(f"- [ ] V3.{i} Contrôle {x} relancé, résultat conforme.")
    L.append("- [ ] V4 Contre-épreuves (CE) appliquées et détectées, puis annulées.")
    L.append("- [ ] V5 Contournements cherchés.")
    L.append("- [ ] V6 Cohérence avec les contrats et les invariants.")
    L.append(f"- [ ] V7 Verdict écrit dans `rapports/{u['id']}-verif-<tentative>.md` et poussé.\n")
    L.append("## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)\n")
    L += [f"- [ ] {x}" for x in fusion_steps(u, br)]
    L.append("")
    return L


def rendre_porte(u, br):
    pcs = points_porte(u["etape"])
    adapt = u.get("adapt_pc", {})
    L = ["## Ce qu'il faut faire\n",
         f"- Exécuter chaque point de contrôle de l'étape {u['etape']} sur `main` à jour, et noter commande, attendu, obtenu, OK ou KO.",
         "- Décider selon la règle : **passer** si tout est OK (un point « sur ta machine » passe par son équivalent sous écran virtuel, l'humain le revoit à la recette) ; **corriger d'abord** si un point est KO.",
         "- Si un point est KO : ne pas cocher la porte ; écrire dans le rapport la correction attendue et l'unité fautive ; à la fusion du verdict, le vérificateur ajoute sous la porte, dans `SUIVI.md`, une ligne « " + u["id"] + ".c1 Correction : … » (réalise : rôle de l'unité fautive ; après : rien) et crée sa fiche depuis `suivi/_modele-correction.md`.",
         "\n## Fichiers autorisés\n", f"`rapports/{u['id']}.md`" + (", " + u["fichiers_porte"] if u.get("fichiers_porte") else "") + ".\n",
         "## Points de contrôle de l'étape (copie du guide)\n", "| ID | Contrôle | Commande ou preuve | Attendu | Adaptation |", "| --- | --- | --- | --- | --- |"]
    for pid, c, cmd, att in pcs:
        L.append(f"| {pid} | {c} | {cmd} | {att} | {adapt.get(pid, '—').replace('|', chr(92) + '|')} |")
    L.append("")
    porte = prompt_porte_guide().replace("{N}", str(u["etape"])).rstrip("\n")
    p = bloc_entete(u, br) + "\n" + GODOT + "\n\n" + REGLES.replace("{id}", u["id"]).replace("{f}", u["f"]) + "\n\n"
    p += DEBUT_GUIDE + " (docs/construction/README.md, prompt de porte d'étape)\n" + porte + "\n" + FIN_GUIDE + "\n\n"
    p += "ADAPTATIONS DU MODE AUTONOME\n- « Tu ne décides pas » : en mode autonome, tu appliques la règle de décision de la fiche (passer ou corriger d'abord).\n- Budget : en créneaux d'IA, comparés à l'estimation de docs/construction/sequence.md (§8). Au-delà de 50 % de dépassement, écris une revue courte dans docs/revues/ et continue, sauf arrêt obligatoire.\n"
    p += "".join(f"- {k} : {v}\n" for k, v in adapt.items())
    p += "\nSOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.\n\n" + bloc_fin(u, br)
    L += ["## Prompt de réalisation\n", "```text\n" + p + "\n```\n", "## Sous-étapes de réalisation\n", f"- [ ] {r0(u, br)}"]
    for i, (pid, *_r) in enumerate(pcs, 1):
        L.append(f"- [ ] R{i} {pid} exécuté et noté (adaptation de la fiche s'il y en a une).")
    L.append(f"- [ ] R{len(pcs) + 1} Décision écrite dans le rapport : passer, ou corriger d'abord avec l'unité fautive.")
    L.append(f"- [ ] R{len(pcs) + 2} « Statut : TERMINÉ » ; commit ; push.\n")
    ids = [p[0] for p in pcs]
    L += ["## Prompt de vérification\n", "```text\n" + verif_prompt(u, br, ids, "Relance chaque point automatisable toi-même ; pour les autres, vérifie la preuve citée. La décision suit-elle la règle ?") + "\n```\n",
          "## Sous-étapes de vérification\n", f"- [ ] V1 Prise en charge : pas l'auteur ; copie neuve sur `origin/{br}`."]
    for i, pid in enumerate(ids, 1):
        L.append(f"- [ ] V2.{i} {pid} relancé ou sa preuve vérifiée.")
    L.append("- [ ] V3 Décision conforme à la règle.")
    L.append(f"- [ ] V4 Verdict écrit dans `rapports/{u['id']}-verif-<tentative>.md` et poussé.\n")
    L += ["## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)\n"] + [f"- [ ] {x}" for x in fusion_steps(u, br)] + [""]
    return L


def rendre_phase(u, br):
    ph, fich = u["phase"], u["fichier_phase"]
    dec = prompt_decoupage()
    if fich == "v1.md":
        dec = dec.replace("docs/construction/mvp.md", "docs/construction/v1.md").replace("docs/construction/mvp-{Px}.md", "docs/construction/v1-{Px}.md")
        dec = dec.rstrip("\n") + "\n- Toute tâche qui produit une explication, une comparaison ou une suggestion inclut un contrôle qui vérifie que chaque affirmation affichée renvoie à une preuve.\n"
    dec = dec.replace("{Px}", ph).rstrip("\n")
    L = ["## Ce qu'il faut faire\n",
         f"- Découper la phase {ph} en 4 à 12 tâches avec le prompt de découpage de `docs/construction/{fich}`, en tenant compte des résultats du POC et des phases précédentes.",
         f"- Écrire `docs/construction/{'mvp' if fich == 'mvp.md' else 'v1'}-{ph}.md` (conception) et une fiche d'exécution par tâche, `suivi/{u['id']}.<k>-<nom>.md`, à partir de `suivi/_modele-tache.md`.",
         f"- Donner à chaque tâche ses prérequis réels : une tâche qui ne dépend que de la fin du découpage peut avancer en même temps que les autres.",
         f"- Écrire dans le rapport les lignes à ajouter à `SUIVI.md`, entre **{u['id']}** et **{u['id']}.P**, au format des autres lignes.",
         "\n## Fichiers autorisés\n",
         f"`docs/construction/{'mvp' if fich == 'mvp.md' else 'v1'}-{ph}.md`, `suivi/{u['id']}.*-*.md` (sauf la porte {u['id']}.P), `rapports/{u['id']}*.md`.\n"]
    p = bloc_entete(u, br) + "\n" + REGLES.replace("{id}", u["id"]).replace("{f}", u["f"]) + "\n\n"
    p += DEBUT_GUIDE + f" (docs/construction/{fich}, prompt de découpage)\n" + dec + "\n" + FIN_GUIDE + "\n\n"
    p += ("ADAPTATIONS DU MODE AUTONOME\n"
          f"- Budget : traduis les heures humaines de la phase en créneaux d'IA avec le ratio observé au POC (docs/revues/revue-poc.md).\n"
          f"- Pour chaque tâche, crée suivi/{u['id']}.<k>-<nom>.md en copiant suivi/_modele-tache.md et en remplissant toutes ses sections : prompt de réalisation complet, sous-étapes R, contrôles, prompt de vérification, sous-étapes V et F.\n"
          f"- Prérequis : {u['id']} pour toute tâche, plus les tâches de la phase dont elle dépend vraiment. Évite que deux tâches indépendantes modifient le même fichier.\n"
          "- Rôles : réalisation par le développeur, sauf contrat, protocole, façade ou format persisté (concepteur) ; vérification par le vérificateur, sauf ces mêmes sujets (concepteur, ou vérificateur si le concepteur est l'auteur).\n"
          f"- Écris dans le rapport les lignes SUIVI.md à insérer ; le vérificateur les insère à la fusion.\n"
          "- Contrôle final : python3 suivi/outil.py verifier → OK, une fois les lignes insérées (le vérificateur le relance après insertion).\n\n")
    p += "SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.\n\n" + bloc_fin(u, br)
    R = ["Lire la section de la phase, `docs/revues/revue-poc.md`, `PROJECT_STATE.md`, `SUIVI.md` et les rapports des phases précédentes.",
         f"Écrire `docs/construction/{'mvp' if fich == 'mvp.md' else 'v1'}-{ph}.md`.",
         f"Créer une fiche `suivi/{u['id']}.<k>-<nom>.md` par tâche, depuis `suivi/_modele-tache.md`, toutes sections remplies.",
         "Écrire dans le rapport les lignes à insérer dans `SUIVI.md`, avec leurs prérequis."]
    u["R"] = R
    L += ["## Prompt de réalisation\n", "```text\n" + p + "\n```\n", "## Sous-étapes de réalisation\n", f"- [ ] {r0(u, br)}"]
    L += [f"- [ ] R{i} {x}" for i, x in enumerate(R, 1)]
    L.append(f"- [ ] R{len(R) + 1} Contrôles finaux : chaque fiche créée a toutes ses sections ; « Statut : TERMINÉ » ; commit ; push.\n")
    L += ["## Prompt de vérification\n", "```text\n" + verif_prompt(u, br, [], "Vérifie le découpage : budget de la phase respecté, chaque tâche avec au moins une contre-épreuve, prérequis réels et sans cycle, aucune paire de tâches indépendantes sur le même fichier. Après insertion des lignes dans SUIVI.md à la fusion : python3 suivi/outil.py verifier → OK.") + "\n```\n",
          "## Sous-étapes de vérification\n",
          f"- [ ] V1 Prise en charge : pas l'auteur ; copie neuve sur `origin/{br}`.",
          "- [ ] V2 Budget de la phase respecté, ou dépassement signalé avec une proposition de retrait.",
          "- [ ] V3 Chaque fiche créée : toutes les sections, au moins une contre-épreuve, fichiers autorisés précis.",
          "- [ ] V4 Prérequis réels, sans cycle ; tâches indépendantes sans fichier commun.",
          f"- [ ] V5 Verdict écrit dans `rapports/{u['id']}-verif-<tentative>.md` et poussé.\n",
          "## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)\n"]
    u["fusion"] = [f"Insérer dans `SUIVI.md`, entre **{u['id']}** et **{u['id']}.P**, les lignes des tâches données par le rapport ; `python3 suivi/outil.py verifier` → OK."]
    L += [f"- [ ] {x}" for x in fusion_steps(u, br)] + [""]
    return L


def rendre_porte_phase(u, br):
    ph = u["phase"]
    pts = u["points"]
    L = ["## Ce qu'il faut faire\n",
         f"- Vérifier sur `main` à jour chaque point de contrôle de la phase {ph}" + (", puis la porte du MVP (plan §9)" if ph == "P8" else ", puis la porte de la V1" if ph == "P16" else "") + ".",
         "- Décider selon la règle : passer, ou corriger d'abord (ligne de correction dans `SUIVI.md`, fiche depuis `suivi/_modele-correction.md`).",
         "\n## Fichiers autorisés\n", f"`rapports/{u['id']}.md`.\n",
         f"## Points de contrôle de la phase (copie de `docs/construction/{u['fichier_phase']}`)\n"]
    L += [f"- {x}" for x in pts]
    extra = []
    if ph == "P8":
        extra = ["Porte du MVP : jeu réel de 300 scripts ou plus indexé sans instanciation ; test de cartographie (par substitution, l'humain le refait à la recette) ; session rechargée ; installation et désinstallation propres ; CI verte sur la fenêtre de support."]
    if ph == "P16":
        extra = ["Porte de la V1 : CAP-12 à CAP-18 démontrées ; deux versions stables supportées (si Godot 4.8 stable n'est pas sortie : point noté pour la recette, sans bloquer le reste) ; matrice publiée ; documentation testée par une installation à froid ; licence (D-06) : arrêt obligatoire n° 3."]
    L += [f"- {x}" for x in extra]
    L.append("")
    p = bloc_entete(u, br) + "\n" + GODOT + "\n\n" + REGLES.replace("{id}", u["id"]).replace("{f}", u["f"]) + "\n\n"
    p += DEBUT_GUIDE + " (docs/construction/README.md, prompt de porte d'étape)\n" + prompt_porte_guide().replace("{N}", ph).rstrip("\n") + "\n" + FIN_GUIDE + "\n\n"
    p += "ADAPTATIONS DU MODE AUTONOME\n- Les points de contrôle sont ceux de la fiche, copiés de " + u["fichier_phase"] + ".\n- « Tu ne décides pas » : tu appliques la règle de décision de la fiche.\n- Ce qui exige un humain passe à la liste de recette.\n\n"
    p += "SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.\n\n" + bloc_fin(u, br)
    L += ["## Prompt de réalisation\n", "```text\n" + p + "\n```\n", "## Sous-étapes de réalisation\n", f"- [ ] {r0(u, br)}"]
    allp = pts + extra
    for i, x in enumerate(allp, 1):
        L.append(f"- [ ] R{i} Point {i} vérifié et noté : {x[:90]}{'…' if len(x) > 90 else ''}")
    L.append(f"- [ ] R{len(allp) + 1} Décision écrite ; « Statut : TERMINÉ » ; commit ; push.\n")
    L += ["## Prompt de vérification\n", "```text\n" + verif_prompt(u, br, [], "Relance chaque point automatisable ; vérifie la preuve des autres ; la décision suit-elle la règle ?") + "\n```\n",
          "## Sous-étapes de vérification\n", f"- [ ] V1 Prise en charge : pas l'auteur ; copie neuve sur `origin/{br}`."]
    L += [f"- [ ] V2.{i} Point {i} relancé ou sa preuve vérifiée." for i in range(1, len(allp) + 1)]
    L += ["- [ ] V3 Décision conforme à la règle.", f"- [ ] V4 Verdict écrit dans `rapports/{u['id']}-verif-<tentative>.md` et poussé.\n",
          "## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)\n"]
    L += [f"- [ ] {x}" for x in fusion_steps(u, br)] + [""]
    return L


# ---------------------------------------------------------------- SUIVI.md

ETAPES = {0: "Étape 0 — Décisions et environnement", 1: "Étape 1 — Fondations", 2: "Étape 2 — Spikes", 3: "Étape 3 — Contrats",
          4: "Étape 4 — Implémentation sous contrat", 5: "Étape 5 — Intégration", 6: "Étape 6 — Interface et robustesse", 7: "Étape 7 — Valeur et revue"}


def ligne_suivi(u):
    apres = ", ".join(u["apres"]) if u["apres"] else "—"
    return f"- [ ] **{u['id']}** · {u['titre']} · réalise {u['r']} · vérifie {u['v']} · après {apres} · fiche `suivi/{u['f']}.md`"


def rendre_suivi():
    niv = niveaux()
    L = ["# Suivi de la construction\n",
         "Liste de progression du mode autonome. Une ligne par unité ; on la coche seulement à la fusion, sur `main`, quand l'unité est vérifiée et fusionnée. Le détail de chaque unité (ce qu'il faut faire, prompts, sous-étapes à cocher) est dans sa fiche `suivi/`. Règles : `docs/construction/sequence.md`.\n",
         "**Lecture d'une ligne.** `réalise` et `vérifie` : C concepteur, D développeur, V vérificateur. `après` : les unités qui doivent être cochées avant de commencer. Une unité dont tous les prérequis sont cochés peut commencer, même si d'autres unités de la liste sont encore ouvertes.\n",
         "**Contrôle de cohérence** : `python3 suivi/outil.py verifier`.\n",
         "## Ce qui se fait à la suite, et ce qui peut avancer en parallèle\n",
         "Les unités d'une même vague sont indépendantes entre elles : aucune n'attend une autre, et elles ne modifient pas les mêmes fichiers. Une unité peut commencer dès que ses propres prérequis sont cochés, sans attendre le reste de sa vague. Les vagues se suivent : chacune contient au moins une unité qui attend la vague précédente.\n",
         "| Vague | Unités indépendantes, réalisables en même temps |", "| --- | --- |"]
    vagues = {}
    for uid, n in niv.items():
        vagues.setdefault(n, []).append(uid)
    for n in sorted(vagues):
        L.append(f"| {n} | {', '.join(vagues[n])} |")
    L.append("")
    L.append("Chaînes strictement séquentielles du POC, où chaque unité attend la précédente :\n")
    L.append("- Socle : S04 → S05 → S06 → S11 → S13 → S14 → S15 → S16 → S17 → S18.")
    L.append("- Runtime : S15 → S19 → S20 → S21 → S22, puis S21 → S25 et S21 → S30.")
    L.append("- Éditeur : S18 et S20 → S24 → S28 → S29 → S31 → S32 → S34 → S35.")
    L.append("- Parties indépendantes : S07 (choix du banc) dès S01 ; S10 (SPIKE-01b) dès S02 ; S19 en même temps que S16 à S18 ; S22, S24, S25 en même temps ; S33 (injection des bugs) dès S25 ; au MVP, P6 et P7 en même temps que P4a à P5 ; en V1, P9, P10, P11 et P14 en même temps.\n")
    L.append("```mermaid\nflowchart LR")
    for uid in U:
        for d in deps_reelles(uid):
            L.append(f"  {d.replace('.', '_')} --> {uid.replace('.', '_')}")
    L.append("```\n")
    cur = None
    for uid, u in U.items():
        et = u.get("etape")
        titre = ETAPES.get(et) if u["kind"] not in ("phase", "porte_phase") else ("MVP — phases P4a à P8" if u["fichier_phase"] == "mvp.md" else "V1 — phases P9 à P16")
        if titre != cur:
            L.append(f"\n## {titre}\n")
            cur = titre
        L.append(ligne_suivi(u))
        if u["kind"] == "phase":
            L.append(f"  - Les tâches {uid}.1, {uid}.2… s'insèrent ici à la fusion du découpage.")
    L.append("\n## Recette finale, pour toi\n")
    rec = ["Décisions « adoptées par défaut » de `docs/DECISIONS.md` confirmées ou changées",
           "Mesures sur ta machine avec GPU : débit de SPIKE-01b, latence PC6.7, désactivation du plugin pendant une vraie collecte, jugement visuel",
           "Mesure de valeur humaine (T19 du guide), comparée à la mesure par substitution",
           "Test de cartographie du MVP, chronométré avec et sans l'outil",
           "Installation à froid en suivant la documentation, puis désinstallation",
           "Licence (D-06) et décision de diffusion",
           "Carte des scripts superposée au jeu (maquette) : entrée au plan ou non",
           "Éléments ajoutés pendant la construction à la liste de recette de `PROJECT_STATE.md`"]
    L += [f"- [ ] {r}" for r in rec]
    L.append("")
    return "\n".join(L)


# ---------------------------------------------------------------- modèles

MODELE_TACHE = """# Sxx.k — <titre de la tâche>

> Fiche d'exécution du mode autonome, créée par le découpage de la phase. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse.

| Champ | Valeur |
| --- | --- |
| Réalise | <Concepteur, Développeur ou Vérificateur> |
| Vérifie | <rôle, jamais l'auteur> |
| Commence après | <Sxx, et les tâches de la phase dont elle dépend vraiment> |
| Indépendante de | <tâches de la phase sans dépendance ni fichier commun> |
| Branche | `tache/Sxx.k-<nom>` |
| Fiche de conception | `docs/construction/<mvp|v1>-<Px>.md`, section <tâche> |
| Estimation | <n> créneau(x) |

## Ce qu'il faut faire

- <résultat attendu, précis, vérifiable>

## Fichiers autorisés

<liste exacte>. Toujours autorisés en plus : `rapports/Sxx.k*.md` et les cases de cette fiche.

## Contrôles propres à cette fiche

- `Sxx.k-a` : `<commande>` → <attendu>
- (CE) <sabotage> : <contrôle> échoue ; annuler.

## Prompt de réalisation

```text
<Copier l'en-tête, le bloc GODOT, les RÈGLES NON NÉGOCIABLES et la FIN DE CRÉNEAU d'une fiche de l'étape 4 (par exemple suivi/S17-T10-modele.md), en remplaçant l'identifiant, la branche et le titre ; puis écrire le travail technique complet : contexte à lire, objectif, fichiers, déroulé, contrôles, contre-épreuves.>
```

## Sous-étapes de réalisation

- [ ] R0 Prise en charge : prérequis cochés ; branche absente ou abandonnée ; rapport « EN COURS » ; push.
- [ ] R1 <étape>
- [ ] Rn Contrôles finaux ; « Statut : TERMINÉ » ; push.

## Prompt de vérification

```text
<Copier le prompt de vérification d'une fiche de l'étape 4 et l'adapter : identifiant, branche, contrôles, cohérence.>
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge : pas l'auteur ; copie neuve.
- [ ] V2 Périmètre.
- [ ] V3.1 Contrôle <id> relancé.
- [ ] V4 Contre-épreuves.
- [ ] V5 Contournements.
- [ ] V6 Cohérence.
- [ ] V7 Verdict écrit et poussé.

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 Fusion `--no-ff` dans `main`.
- [ ] F2 `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK, sinon annulation.
- [ ] F3 Ligne cochée dans `SUIVI.md`, avec date, auteur, vérificateur, créneaux.
- [ ] F4 `PROJECT_STATE.md` : mesures, liste de recette.
- [ ] F5 Cases F cochées ; commit ; push.

## Pour la recette

Rien de propre à cette unité.
"""

MODELE_CORRECTION = """# Sxx.cN — Correction demandée par la porte Sxx

> Fiche créée par le vérificateur d'une porte quand un point de contrôle est KO.

| Champ | Valeur |
| --- | --- |
| Réalise | <rôle de l'unité fautive> |
| Vérifie | <le vérificateur de l'unité fautive> |
| Commence après | rien |
| Branche | `tache/Sxx.cN-<nom>` |
| Unité fautive | <Syy> |
| Point KO | <PCx.y : commande, attendu, obtenu> |

## Ce qu'il faut faire

- Corriger le défaut qui fait échouer <PCx.y>, dans les fichiers autorisés de l'unité fautive.
- Rejouer les contrôles de l'unité fautive, puis le point de contrôle de la porte.

## Prompt de réalisation

```text
Tu corriges le défaut relevé par la porte Sxx du projet GODOT_DEV_MAPPER. Lis rapports/Sxx.md (point KO, correction attendue) et la fiche de l'unité fautive suivi/<Syy>.md : ses règles, ses fichiers autorisés et ses contrôles s'appliquent. Fais la plus petite correction qui rend le point OK sans affaiblir aucun test. Exécute les contrôles de l'unité fautive, puis le point de la porte, et colle leurs sorties dans rapports/Sxx.cN.md.
```

## Sous-étapes de réalisation

- [ ] R0 Prise en charge ; rapport « EN COURS » ; push.
- [ ] R1 Cause du point KO établie et écrite.
- [ ] R2 Correction faite.
- [ ] R3 Contrôles de l'unité fautive et point de la porte → OK ; « Statut : TERMINÉ » ; push.

## Sous-étapes de vérification

- [ ] V1 Pas l'auteur ; copie neuve.
- [ ] V2 Périmètre : fichiers de l'unité fautive seulement.
- [ ] V3 Contrôles relancés ; point de la porte OK.
- [ ] V4 Verdict écrit et poussé.

## Sous-étapes de fusion

- [ ] F1 Fusion, `run_all_checks.sh` sur `main`, ligne cochée dans `SUIVI.md`, push. La porte Sxx est ensuite rejouée.
"""


# ---------------------------------------------------------------- vérification

SECTIONS_TACHE = ["## Ce qu'il faut faire", "## Prompt de réalisation", "## Sous-étapes de réalisation", "## Prompt de vérification", "## Sous-étapes de vérification", "## Sous-étapes de fusion"]
RE_LIGNE = re.compile(r"^- \[( |x)\] \*\*(S\d\d(?:\.[0-9A-Za-z]+)?)\*\* · (.*?) · réalise ([CDV]) · vérifie ([CDV]) · après (.*?) · fiche `(suivi/[^`]+)`")


def lire_suivi():
    lignes = {}
    for l in SUIVI_MD.read_text(encoding="utf-8").splitlines():
        m = RE_LIGNE.match(l)
        if m:
            coche, uid, titre, r, v, apres, fiche = m.groups()
            dep = [] if apres.strip() == "—" else [x.strip() for x in apres.split(",")]
            lignes[uid] = dict(coche=coche == "x", titre=titre, r=r, v=v, apres=dep, fiche=fiche)
    return lignes


def verifier():
    err = []
    if not SUIVI_MD.exists():
        print("KO : SUIVI.md absent")
        return 1
    S = lire_suivi()
    ids = set(S)

    def reelles(uid):
        out = []
        for d in S[uid]["apres"]:
            if d.endswith(".*"):
                out += [x for x in ids if x.startswith(d[:-2] + ".") and x != d[:-2] + ".P"]
            else:
                out.append(d)
        return out

    for uid, s in S.items():
        for d in s["apres"]:
            if not d.endswith(".*") and d not in ids:
                err.append(f"{uid} : prérequis inconnu {d}")
        p = RACINE / s["fiche"]
        if not p.exists():
            err.append(f"{uid} : fiche absente {s['fiche']}")
            continue
        t = p.read_text(encoding="utf-8")
        for sec in SECTIONS_TACHE:
            if sec not in t and not (sec in ("## Prompt de vérification",) and ".c" in uid):
                err.append(f"{uid} : section manquante « {sec} »")
        m = re.search(r"\| Commence après \| (.*?)(?: \(cochées dans `SUIVI.md`\))? \|", t)
        if m and not uid.split(".")[-1].isdigit():
            dep_fiche = [] if m.group(1).startswith("rien") else [x.strip() for x in m.group(1).split(",")]
            if sorted(dep_fiche) != sorted(s["apres"]):
                err.append(f"{uid} : prérequis différents entre SUIVI.md ({s['apres']}) et la fiche ({dep_fiche})")
        if s["coche"]:
            for d in reelles(uid):
                if d in S and not S[d]["coche"]:
                    err.append(f"{uid} cochée alors que son prérequis {d} ne l'est pas")
            if "- [ ]" in t:
                err.append(f"{uid} cochée alors que sa fiche a des cases non cochées")
        g = re.search(re.escape(DEBUT_GUIDE) + r" \(docs/construction/([^,]+), ([^)]+)\)\n(.*?)\n" + re.escape(FIN_GUIDE), t, re.S)
        if g and g.group(1).startswith("etape-"):
            fichier, tache = g.group(1), g.group(2)
            blocs = [b.rstrip("\n") for b in prompts_guide(fichier, tache)]
            if g.group(3) not in blocs:
                err.append(f"{uid} : le travail technique ne correspond plus au guide ({fichier}, {tache}) : régénérer la fiche")
            for cid in controles_guide(fichier, tache):
                if cid not in t:
                    err.append(f"{uid} : contrôle du guide {cid} absent de la fiche")
    # cycles
    etat = {}

    def visite(u, pile):
        if etat.get(u) == 1:
            err.append("cycle : " + " → ".join(pile + [u]))
            return
        if etat.get(u) == 2:
            return
        etat[u] = 1
        for d in reelles(u):
            if d in S:
                visite(d, pile + [u])
        etat[u] = 2

    for u in S:
        visite(u, [])
    if err:
        print("KO")
        for e in err:
            print(" -", e)
        return 1
    faites = sum(1 for s in S.values() if s["coche"])
    print(f"OK : {len(S)} unités, {faites} cochées, dépendances sans cycle, fiches complètes et conformes au guide")
    return 0


def generer(force=False):
    SUIVI_DIR.mkdir(exist_ok=True)
    for uid, u in U.items():
        p = SUIVI_DIR / f"{u['f']}.md"
        if p.exists() and "- [x]" in p.read_text(encoding="utf-8") and not force:
            print(f"conservée (cases cochées) : {p.name}")
            continue
        p.write_text(rendre(u), encoding="utf-8")
    (SUIVI_DIR / "_modele-tache.md").write_text(MODELE_TACHE, encoding="utf-8")
    (SUIVI_DIR / "_modele-correction.md").write_text(MODELE_CORRECTION, encoding="utf-8")
    if SUIVI_MD.exists() and "- [x]" in SUIVI_MD.read_text(encoding="utf-8") and not force:
        print("SUIVI.md conservé (lignes cochées)")
    else:
        SUIVI_MD.write_text(rendre_suivi(), encoding="utf-8")
    print(f"{len(U)} fiches générées")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] not in ("verifier", "generer"):
        print(__doc__)
        sys.exit(2)
    if a[0] == "generer":
        generer("--force" in a)
        sys.exit(verifier())
    sys.exit(verifier())
