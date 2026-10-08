"""Découpage provisoire des phases du MVP et de la V1 en tâches.

Écrit avant le POC, d'après docs/construction/mvp.md, v1.md et le plan directeur. Au début de chaque phase,
l'unité de revue (S36, S37…) le confronte aux résultats du POC et des phases précédentes : elle garde,
modifie, retire ou ajoute des tâches. Après cette revue, la fiche d'une tâche fait foi, plus ce fichier.

Chaque tâche : identifiant Sxx.k, nom court, titre, IA qui réalise et IA qui vérifie (C = IA 1, D = IA 2,
V = IA 3), prérequis, ce qu'il faut faire, fichiers autorisés, sous-étapes R, contrôles, contre-épreuves,
cohérence à vérifier, contexte à lire.
"""

RUN = '"$B" --headless --path . -s res://tests/run_all.gd 2>&1'
DEPS = ("python3 tools/check_deps.py; echo $?", "0, aucune violation")
PREVIEW = ('P=$(tools/ci/fetch_godot.sh "$(python3 -c \'import json; print(json.load(open("addons/godot_dev_mapper/compat/versions.json"))["preview"])\')") '
           '&& "$P" --headless --path . -s res://tests/run_all.gd 2>&1 | grep GDM_TESTS')
OUTILS_CONTRAT = ["tools/validate_fixtures.py (schéma et règles du nouveau format)", "tools/check_contracts.py (sections C-xx et fichiers docs/contracts/)"]


def tests(*noms):
    motif = "|".join(noms)
    return (f'{RUN} | grep -E "{motif}|GDM_TESTS"',
            f"une ligne PASS par test de {', '.join(n + '.gd' for n in noms)}, aucune FAIL ; GDM_TESTS … failed=0")


PHASES_INFO = {
    "P4a": dict(fichier="mvp.md", budget="6 à 12 h", oblig=[
        "Code jetable dans spikes/ ; rien dans addons/.",
        "Mesures avec version de Godot et machine, marquées « rendu logiciel » sous écran virtuel.",
        "Pour un outil tiers : licence, version épinglée, plan de sortie, passage obligé par une façade de syntaxe ; l'adopter est une décision humaine (D-04).",
    ]),
    "P4b": dict(fichier="mvp.md", budget="8 à 14 h", oblig=[
        "Erreurs isolées par fichier : un script illisible ne bloque pas l'inventaire.",
        "Appels dynamiques marqués « non résolus », jamais devinés.",
        "Aucune scène n'est instanciée pendant l'inventaire.",
        "Backend tiers uniquement derrière la façade de syntaxe.",
        "Tests d'abord, sur des fixtures maison ; puis tests de référence sur le banc d'essai.",
    ]),
    "P5": dict(fichier="mvp.md", budget="8 à 13 h", oblig=[
        "Expansion bornée : jamais de graphe complet affiché d'un coup.",
        "Toute relation affichée montre sa provenance et sa résolution.",
        "Les requêtes vivent dans projections/ et se testent sans interface ; l'interface suit le rendu choisi en P4a.",
        "Les états ne reposent jamais sur la couleur seule.",
    ]),
    "P6": dict(fichier="mvp.md", budget="10 à 16 h", oblig=[
        "Formats persistés versionnés et sauvegarde atomique (fichier temporaire, puis renommage).",
        "Refus explicite d'une version inconnue et d'un fichier tronqué, avec un message clair.",
        "Négociation de capacités dans le protocole ; frames et ticks physiques horodatés.",
        "Les sessions enregistrées du POC restent lisibles : elles deviennent des fixtures de compatibilité ascendante.",
        "Toute rupture d'un format persisté après une diffusion est un arrêt obligatoire.",
    ]),
    "P7": dict(fichier="mvp.md", budget="5 à 9 h", oblig=[
        "Seuls les blocs déclarés s'affichent, jamais des blocs inférés.",
        "Un bloc interrompu s'affiche « incomplet » ; le cycle de vie suit le plan §6.",
        "Contrat d'abord, puis projections testées, puis interface.",
    ]),
    "P8": dict(fichier="mvp.md", budget="6 à 10 h", oblig=[
        "L'outil de désinstallation liste les appels FlowTrace et refuse de retirer le dossier runtime s'il en reste.",
        "Les adaptateurs par version n'apparaissent que si une rupture est constatée.",
        "Toute rupture se corrige dans la frontière de compatibilité.",
    ]),
    "P9": dict(fichier="v1.md", budget="8 à 12 h", oblig=[
        "Chronologie, causalité et intention restent distinctes (INV-05) : aucune arête causale tirée de la seule proximité temporelle.",
        "L'ordre n'est garanti que par producteur.",
        "Toute tâche qui produit une explication, une comparaison ou une suggestion inclut un contrôle qui vérifie que chaque affirmation affichée renvoie à une preuve.",
    ]),
    "P10": dict(fichier="v1.md", budget="8 à 12 h", oblig=[
        "Définition, instance et occurrence restent distinctes (INV-02).",
        "Toute comparaison cite révision, configuration, scénario, fenêtre et couverture.",
        "Toute tâche qui produit une explication, une comparaison ou une suggestion inclut un contrôle qui vérifie que chaque affirmation affichée renvoie à une preuve.",
    ]),
    "P11": dict(fichier="v1.md", budget="12 à 20 h", oblig=[
        "« Dernière écriture connue », bornée et marquée comme telle, jamais « valeur certaine ».",
        "Provenance sur chaque maillon (INV-03).",
        "Toute tâche qui produit une explication, une comparaison ou une suggestion inclut un contrôle qui vérifie que chaque affirmation affichée renvoie à une preuve.",
    ]),
    "P12": dict(fichier="v1.md", budget="10 à 16 h", oblig=[
        "Non observé n'est pas non exécuté (INV-04).",
        "On montre la « première divergence connue », jamais « la cause ».",
        "Les attentes sont versionnées avec le projet.",
        "Toute tâche qui produit une explication, une comparaison ou une suggestion inclut un contrôle qui vérifie que chaque affirmation affichée renvoie à une preuve.",
    ]),
    "P13": dict(fichier="v1.md", budget="14 à 22 h", oblig=[
        "Aucune intention inventée.",
        "Chaque phrase d'explication renvoie à une preuve.",
        "Les suggestions sont marquées comme telles, et l'humain les valide.",
        "Toute tâche qui produit une explication, une comparaison ou une suggestion inclut un contrôle qui vérifie que chaque affirmation affichée renvoie à une preuve.",
    ]),
    "P14": dict(fichier="v1.md", budget="6 à 10 h", oblig=[
        "On ne prétend pas mesurer le temps CPU par fonction.",
        "Le coût de capture se mesure avec et sans collecte, et s'affiche.",
        "Une corrélation dans le temps n'est jamais présentée comme une cause.",
    ]),
    "P15": dict(fichier="v1.md", budget="5 à 8 h", oblig=[
        "Export local uniquement : aucun envoi réseau.",
        "Choix des champs, exclusion des données sensibles, aperçu avant partage.",
        "Les lacunes sont incluses dans l'export.",
    ]),
    "P16": dict(fichier="v1.md", budget="12 à 20 h", oblig=[
        "Aucune nouvelle fonctionnalité.",
        "Toute dette notée dans PROJECT_STATE.md est traitée, ou acceptée par écrit.",
        "Licence du plugin (D-06) décidée par l'humain avant toute diffusion : la tâche prépare le dossier, elle ne décide pas.",
    ]),
}

TACHES = []


def t(id, nom, titre, r, v, apres, faire, fichiers, R, controles, ce, coherence, contexte=(), recette=(), creneaux=1, fusion=()):
    TACHES.append(dict(id=id, nom=nom, titre=titre, r=r, v=v, apres=list(apres), faire=list(faire), fichiers=list(fichiers),
                       R=list(R), controles=list(controles), ce=list(ce), coherence=coherence, contexte=list(contexte),
                       recette=list(recette), creneaux=creneaux, fusion=list(fusion)))


# =====================================================================================================
# MVP — P4a Évaluations : rendu et backend statique (revue S36)
# =====================================================================================================

t("S36.1", "etalon-relations", "Étalon des relations attendues sur le banc d'essai", "V", "C", ["S36"],
  ["Écrire à la main, sur une partie du banc d'essai (au moins 15 scripts, dont les deux types d'ennemis), le fichier des relations attendues : appels directs, appels sur receveur typé, connexions et émissions de signaux, héritages, et appels dynamiques à marquer « non résolu ».",
   "Chaque relation : identifiant, type, source (fichier, ligne, fonction), cible ou `{\"unresolved\": raison}`, et la ligne du code qui la prouve.",
   "Écrire `tools/check_etalon.py` : valide le fichier (champs, unicité, fichiers et lignes existants dans la copie du banc à sa révision migrée) et affiche les comptes par type."],
  ["benches/<nom>/relations_attendues.json", "tools/check_etalon.py", "docs/benches/<nom>.md (section « Étalon des relations »)"],
  ["Copie de travail de `banc/<nom>-base` (procédure de S08) ; choisir les scripts de l'étalon et le noter.",
   "Relever les relations à la main, fichier par fichier, en citant la ligne de preuve.",
   "Marquer « non résolu » chaque appel dont la cible ne se lit pas dans le code (call, callv, Callable construit, receveur non typé).",
   "Écrire `tools/check_etalon.py`.",
   "Compléter `docs/benches/<nom>.md` : périmètre de l'étalon, comptes par type, cas douteux."],
  [("S36.1-a", "python3 tools/check_etalon.py benches/<nom>/relations_attendues.json --banc ../benches/<nom>; echo $?", "0, comptes par type affichés, au moins 150 relations"),
   ("S36.1-b", "python3 tools/check_etalon.py benches/<nom>/relations_attendues.json --banc ../benches/<nom> | grep -c unresolved", "au moins 10")],
  ["(CE) Dupliquer un identifiant de relation : S36.1-a sort en 1 et nomme le doublon ; annuler.",
   "(CE) Pointer une relation vers une ligne qui n'existe pas : S36.1-a sort en 1 ; annuler."],
  "Plan §5 (Relation, Evidence, résolution) ; INV-03 : la provenance « déclarée à la main » est écrite dans l'étalon.",
  contexte=["docs/plan-directeur.md §5", "docs/benches/<nom>.md", "benches/benches.json"])

t("S36.2", "spike03-rendu", "SPIKE-03, rendu du graphe : GraphEdit, canevas ou hybride", "C", "V", ["S36"],
  ["Construire dans `spikes/spike03_rendu/` un projet jetable qui affiche un graphe généré de 50, 300 et 1 000 éléments visibles selon trois options : GraphEdit, canevas dessiné (`_draw`), hybride (canevas pour les arêtes, contrôles pour les nœuds sélectionnés).",
   "Mesurer pour chaque option et chaque taille : temps de frame moyen et 95e centile pendant un défilement scripté, latence d'une sélection au clic simulé, mémoire.",
   "Écrire `docs/spikes/SPIKE-03.md` : méthode, chiffres (marqués « rendu logiciel, non représentatif d'un GPU »), limites, décision KEEP, REWRITE ou DISCARD pour chaque option, et option recommandée."],
  ["spikes/spike03_rendu/", "docs/spikes/SPIKE-03.md"],
  ["Générateur de graphes déterministe (graine fixe) à 50, 300 et 1 000 nœuds.",
   "Option GraphEdit.",
   "Option canevas dessiné.",
   "Option hybride.",
   "Scénario de mesure scripté et `spikes/spike03_rendu/run.sh`, qui lance tout sous xvfb-run et affiche une ligne par option et par taille.",
   "Écrire `docs/spikes/SPIKE-03.md` avec la recommandation."],
  [("S36.2-a", "GODOT=\"$B\" spikes/spike03_rendu/run.sh", "neuf lignes MESURE (3 options × 3 tailles) avec temps de frame et latence"),
   ("S36.2-b", "grep -cE \"KEEP|REWRITE|DISCARD\" docs/spikes/SPIKE-03.md", "au moins 3")],
  ["(CE) Forcer 3 000 éléments dans l'option recommandée : la mesure dépasse l'objectif de 16 ms et le rapport le signale ; annuler."],
  "Plan §7 (SPIKE-03, 300 éléments sans dégradation) et §8 ; états jamais portés par la seule couleur.",
  contexte=["docs/plan-directeur.md §7 et §8", "docs/construction/mvp.md, P4a"],
  recette=["SPIKE-03 sur ta machine, avec GPU : refaire la mesure de l'option retenue."], creneaux=2)

t("S36.3", "spike04-maison", "SPIKE-04, extraction maison des relations d'appel", "D", "C", ["S36.1"],
  ["Écrire dans `spikes/spike04_backend/maison/` un extracteur jetable en GDScript : lecture du texte des scripts, découpage en jetons, repérage des déclarations et des appels.",
   "Le lancer sur les scripts de l'étalon et compter, par type de relation : justes, fausses, manquées ; mesurer le temps sur tout le banc.",
   "Écrire `docs/spikes/SPIKE-04-maison.md` : résultats, constructions mal couvertes, coût estimé d'une version de production (S36.5 en fera la synthèse dans SPIKE-04.md)."],
  ["spikes/spike04_backend/maison/", "docs/spikes/SPIKE-04-maison.md"],
  ["Lecteur de jetons GDScript minimal (chaînes, commentaires, indentation).",
   "Repérage des déclarations (class_name, extends, func, signal).",
   "Repérage des appels et des signaux ; « non résolu » pour tout appel dynamique.",
   "Comparaison à l'étalon par `spikes/spike04_backend/maison/run.sh` : justes, fausses, manquées.",
   "Rédiger `docs/spikes/SPIKE-04-maison.md`."],
  [("S36.3-a", "GODOT=\"$B\" spikes/spike04_backend/maison/run.sh", "comptes justes, fausses, manquées par type ; temps total sur le banc"),
   ("S36.3-b", "grep -ciE \"justes|fausses|manquées\" docs/spikes/SPIKE-04-maison.md", "au moins 3")],
  ["(CE) Supprimer le marquage « non résolu » des appels `call(\"…\")` : le nombre de relations fausses augmente dans S36.3-a ; annuler."],
  "Objectif de P4a : 90 % des appels directs résolus, aucune relation certaine fausse.",
  contexte=["benches/<nom>/relations_attendues.json", "docs/construction/mvp.md, P4a"])

t("S36.4", "spike04-astflow", "SPIKE-04, évaluation de GDScript AST Flow", "C", "V", ["S36.1"],
  ["Vérifier l'existence, la licence (fichier LICENSE à une révision épinglée), la version de Godot visée et le mode d'exécution de GDScript AST Flow ; « non vérifié » écarte l'outil.",
   "L'exécuter hors du dépôt (cache local, version épinglée) sur les scripts de l'étalon et compter justes, fausses, manquées ; mesurer le temps.",
   "Estimer le coût d'intégration derrière une façade de syntaxe et écrire un plan de sortie ; ne rien ajouter au dépôt hors de `spikes/`."],
  ["spikes/spike04_backend/astflow/ (scripts seulement, aucun code tiers)", "docs/spikes/SPIKE-04-astflow.md"],
  ["Trouver le dépôt de l'outil ; épingler une révision ; vérifier la licence et la version de Godot visée.",
   "Écrire `spikes/spike04_backend/astflow/run.sh` : télécharge la révision épinglée dans un cache hors du dépôt, l'exécute, convertit sa sortie au format de l'étalon.",
   "Comparer à l'étalon ; mesurer le temps.",
   "Écrire `docs/spikes/SPIKE-04-astflow.md` : résultats, coût d'intégration, plan de sortie, risques (maintenance, licence)."],
  [("S36.4-a", "GODOT=\"$B\" spikes/spike04_backend/astflow/run.sh", "comptes justes, fausses, manquées, ou « outil indisponible » avec la raison"),
   ("S36.4-b", "git ls-files spikes/spike04_backend/astflow | grep -v -E \"\\.(sh|py|md)$\" | wc -l", "0 (aucun code tiers versionné)")],
  ["(CE) Changer la révision épinglée pour une valeur inexistante : run.sh échoue avec un message clair ; annuler."],
  "D-04 (politique de dépendances) ; plan §3 (outil existant) ; aucune dépendance ajoutée.",
  contexte=["docs/plan-directeur.md §3", "docs/DECISIONS.md (D-04)"])

t("S36.5", "decisions-p4a", "Décisions de rendu et de backend statique", "C", "V", ["S36.2", "S36.3", "S36.4"],
  ["Comparer les deux backends sur les critères de P4a (relations justes, fausses, manquées ; temps ; coût d'intégration) et écrire `docs/spikes/SPIKE-04.md` : synthèse de `SPIKE-04-maison.md` et `SPIKE-04-astflow.md`, comparaison et conclusion.",
   "Règle : l'extraction maison est retenue par défaut. Si AST Flow l'emporte nettement, la recommandation est écrite « proposée, décision humaine (D-04) » et passe à la recette ; le MVP continue avec l'extraction maison.",
   "Écrire dans le rapport les décisions à inscrire : option de rendu retenue (SPIKE-03), backend retenu (SPIKE-04), et les ajustements que cela demande aux fiches de P4b et de P5."],
  ["docs/spikes/SPIKE-04.md (synthèse)", "docs/spikes/SPIKE-03.md (conclusion seulement)"],
  ["Relire SPIKE-03, SPIKE-04-maison.md, SPIKE-04-astflow.md et l'étalon.",
   "Écrire la comparaison et la conclusion de SPIKE-04.",
   "Appliquer la règle de décision et l'écrire.",
   "Lister les ajustements pour les revues S37 et S38."],
  [("S36.5-a", "grep -E \"^Décision|KEEP|REWRITE|DISCARD\" docs/spikes/SPIKE-04.md | head", "une décision par backend"),
   ("S36.5-b", "grep -c \"objectif\" docs/spikes/SPIKE-04.md", "au moins 1 (objectif de P4a comparé aux chiffres)")],
  ["(CE) Le vérificateur recalcule les pourcentages de SPIKE-04 depuis les sorties de S36.3-a et S36.4-a : un écart de plus d'un point est un refus."],
  "Plan §3 et §9 (porte de P4a) ; sequence.md §5 (nouvelle dépendance : décision humaine).",
  contexte=["docs/spikes/SPIKE-03.md", "docs/spikes/SPIKE-04-maison.md", "docs/spikes/SPIKE-04-astflow.md", "docs/DECISIONS.md"],
  recette=["Confirmer le backend statique (D-04, SPIKE-04) et l'option de rendu (SPIKE-03)."],
  fusion=["Inscrire dans `docs/DECISIONS.md` les décisions de SPIKE-03 (rendu) et de SPIKE-04 (backend statique), au statut « adoptée par défaut » ; une recommandation d'outil tiers reste « proposée »."])


# =====================================================================================================
# MVP — P4b Backend statique et inventaire, CAP-08 et CAP-09 (revue S37)
# =====================================================================================================

t("S37.1", "contrat-c08", "Contrat C-08 : inventaire du projet et relations d'appel", "C", "V", ["S37"],
  ["Écrire `docs/contracts/C-08.md` (un fichier par nouveau contrat, renvoyé depuis l'index de `docs/CONTRACTS.md`), avec ses sept rubriques : ProgramSnapshot complet (scripts, scènes, ressources, autoloads, classes globales, révision, couverture), relations extraites (call, signal_connect, signal_emit, extends, preload, instantiates), preuve « extraite », résolution (resolved, partial, unresolved avec raison), diagnostics par fichier à codes stables.",
   "Écrire `contracts/schemas/program_snapshot.v1.schema.json`, des fixtures valides et invalides (`invalid_<CODE>__*`) dans `tests/contract/fixtures/program_snapshot/`, et les tests de contrat `tests/contract/test_c08_*.gd` avec leurs marqueurs `tests/pending/` au nom des tâches qui les activeront (S37.6 et S37.7).",
   "Étendre `tools/check_contracts.py` aux contrats C-xx, qu'ils soient une section de `docs/CONTRACTS.md` ou un fichier `docs/contracts/C-xx.md`, et `tools/validate_fixtures.py` au kind program_snapshot (schéma et règles de niveau 2)."],
  ["docs/contracts/C-08.md", "docs/CONTRACTS.md (index : lien vers C-08)", "contracts/schemas/program_snapshot.v1.schema.json", "tests/contract/fixtures/program_snapshot/", "tests/contract/test_c08_snapshot.gd", "tests/contract/test_c08_relations.gd", "tests/pending/test_c08_*.pending"] + OUTILS_CONTRAT,
  ["Relire C-01, C-02, C-05, SPIKE-04 et la revue S37.",
   "Rédiger C-08 : objet, format, exemples valides, exemples invalides, comportement en erreur, version, tests de contrat.",
   "Écrire le schéma et au moins cinq fixtures invalides (référence inconnue, résolution absente, diagnostic sans code, ligne hors du fichier, relation certaine vers une cible non résolue).",
   "Écrire les deux tests de contrat et leurs marqueurs (S37.6 et S37.7).",
   "Étendre `tools/check_contracts.py` (fichiers docs/contracts/C-xx.md) et `tools/validate_fixtures.py` (kind program_snapshot)."],
  [("S37.1-a", "python3 tools/validate_fixtures.py; echo $?", "0 ; fixtures program_snapshot comprises, chaque fixture invalide rejetée avec le code de son nom"),
   ("S37.1-b", "python3 tools/check_contracts.py C-08; echo $?", "0, C-08 a ses sept rubriques"),
   ("S37.1-c", f"{RUN} | grep GDM_TESTS", "failed=0, pending augmenté du nombre de tests C-08")],
  ["(CE) Retirer le champ « resolution » d'une fixture valide : S37.1-a la rejette ; annuler.",
   "(CE) Retirer la rubrique « comportement en erreur » de docs/contracts/C-08.md : S37.1-b sort en 1 ; annuler."],
  "C-05 et C-01 non modifiés ; plan §5 (Relation, Evidence) ; INV-03.",
  contexte=["docs/CONTRACTS.md (C-01, C-02, C-05)", "docs/spikes/SPIKE-04.md", "docs/plan-directeur.md §3 et §5"])

t("S37.2", "facades-introspection-syntaxe", "Façades d'introspection et de syntaxe", "D", "C", ["S37"],
  ["`compat/introspection_facade.gd` : liste des fichiers de res:// (en ignorant .godot/ et les dossiers exclus), dépendances d'une ressource, autoloads, classes globales, état d'une scène empaquetée lu sans l'instancier.",
   "`compat/syntax_facade.gd` : texte source d'un script et identifiant stable (UID si SPIKE-02 l'a validé, sinon chemin) ; point d'entrée unique d'un futur backend tiers.",
   "Chaque API moteur utilisée est d'abord vérifiée par un script de trois lignes sur 4.7.2 et sur la préversion ; elle s'ajoute à la liste des API sensibles de `tools/deps_rules.json`."],
  ["addons/godot_dev_mapper/compat/introspection_facade.gd", "addons/godot_dev_mapper/compat/syntax_facade.gd", "tools/deps_rules.json (API sensibles)", "tests/unit/test_introspection_facade.gd", "tests/fixtures/mini_projet/"],
  ["Vérifier chaque API candidate sur 4.7.2 et la préversion ; coller les sorties.",
   "Écrire `tests/fixtures/mini_projet/` : quelques scripts, deux scènes, une ressource, un autoload.",
   "Écrire les tests, les voir échouer.",
   "Écrire `introspection_facade.gd`.",
   "Écrire `syntax_facade.gd`.",
   "Ajouter les API à `tools/deps_rules.json`."],
  [("S37.2-a",) + tests("test_introspection_facade"),
   ("S37.2-b",) + DEPS,
   ("S37.2-c", PREVIEW, "ligne GDM_TESTS sur la préversion, rapportée sans bloquer")],
  ["(CE) Appeler une API sensible depuis `acquisition/` : S37.2-b sort en 1 ; annuler.",
   "(CE) Instancier une scène dans la façade : le test « aucune instance créée » échoue ; annuler."],
  "C-03 (façades) ; INV-09 ; règles d'isolation de SPIKE-02.",
  contexte=["docs/CONTRACTS.md (C-03)", "docs/spikes/SPIKE-02.md", "docs/ARCHITECTURE.md (API sensibles)"])

t("S37.3", "fixtures-syntaxe", "Fixtures de syntaxe GDScript et relations attendues", "V", "D", ["S37.1"],
  ["Écrire `tests/fixtures/syntaxe/` : un script par construction ciblée (appel direct, self, super, receveur typé, receveur non typé, appel statique sur class_name, Callable, call et callv, signal connecté par les deux syntaxes, emit, await, lambda, classe interne, annotations, chaînes multilignes, commentaires trompeurs).",
   "Ajouter un script à syntaxe inconnue et un fichier illisible, qui doivent produire un diagnostic sans plantage.",
   "Écrire `tests/fixtures/syntaxe/attendu.json` : déclarations et relations attendues, au format de C-08, avec la résolution attendue de chacune."],
  ["tests/fixtures/syntaxe/"],
  ["Lister les constructions ciblées et les écrire, une par fichier.",
   "Écrire les deux fichiers d'erreur.",
   "Écrire `attendu.json`, en marquant « non résolu » tout appel dynamique.",
   "Valider `attendu.json` contre le schéma de C-08."],
  [("S37.3-a", "python3 tools/validate_fixtures.py --file tests/fixtures/syntaxe/attendu.json; echo $?", "0"),
   ("S37.3-b", "ls tests/fixtures/syntaxe/*.gd | wc -l", "au moins 16"),
   ("S37.3-c", "\"$B\" --headless --path tests/fixtures/syntaxe --check-only -s res://appel_direct.gd; echo $?", "0 (les fixtures valides compilent)")],
  ["(CE) Marquer « resolved » un appel `call(\"nom\")` dans attendu.json : le vérificateur montre que cela contredit C-08 ; annuler."],
  "C-08 ; plan §3 (CAP-09 : appels dynamiques non résolus).",
  contexte=["docs/contracts/C-08.md", "benches/<nom>/relations_attendues.json"])

t("S37.4", "lexeur-gdscript", "Lexeur GDScript", "D", "V", ["S37.2", "S37.3"],
  ["`acquisition/gd_lexer.gd` : jetons avec ligne et colonne, chaînes simples, doubles et multilignes, StringName et NodePath, commentaires, indentation et dédentation, continuations de ligne.",
   "Un caractère ou une construction inconnus produisent un diagnostic à code stable et la lecture continue."],
  ["addons/godot_dev_mapper/acquisition/gd_lexer.gd", "tests/unit/test_gd_lexer.gd"],
  ["Écrire les tests sur les fixtures de syntaxe ; les voir échouer.",
   "Écrire le lexeur.",
   "Mesurer le temps sur tous les scripts du banc d'essai et le noter."],
  [("S37.4-a",) + tests("test_gd_lexer"), ("S37.4-b",) + DEPS],
  ["(CE) Ignorer les chaînes multilignes : le test correspondant échoue ; annuler."],
  "Module acquisition : dépend de core et compat seulement (plan §4).",
  contexte=["tests/fixtures/syntaxe/", "docs/contracts/C-08.md"])

t("S37.5", "declarations", "Extraction des déclarations et de leurs ancrages", "D", "V", ["S37.4"],
  ["`acquisition/gd_declarations.gd` : class_name, extends, classes internes, func (statiques ou non), signal, var et const (exportées ou non), avec leur SourceAnchor (path, script_uid, line_start, line_end, range_hash).",
   "Les identifiants de définition suivent la clé de correspondance de C-01 et SPIKE-02 (UID et nom qualifié, ou chemin)."],
  ["addons/godot_dev_mapper/acquisition/gd_declarations.gd", "tests/unit/test_gd_declarations.gd"],
  ["Écrire les tests sur `attendu.json` (déclarations) ; les voir échouer.",
   "Écrire l'extracteur.",
   "Vérifier les ancrages contre C-02 (range_hash calculé comme au POC)."],
  [("S37.5-a",) + tests("test_gd_declarations"), ("S37.5-b",) + DEPS],
  ["(CE) Décaler line_end d'une ligne : le test des ancrages échoue ; annuler."],
  "C-01 (identités), C-02 (ancrage), C-08.",
  contexte=["docs/CONTRACTS.md (C-01, C-02)", "docs/contracts/C-08.md"])

t("S37.6", "relations-appel", "Extraction des relations d'appel et de signal", "D", "V", ["S37.5"],
  ["`acquisition/call_extractor.gd` : appels directs, self, super, receveur typé, appel statique sur class_name ; connexions et émissions de signaux ; héritage et preload.",
   "Tout appel dont la cible ne se lit pas dans le code (call, callv, Callable construit, receveur non typé) devient une relation vers `{\"unresolved\": raison}`.",
   "Activer les tests de contrat C-08 sur les relations (supprimer leurs marqueurs)."],
  ["addons/godot_dev_mapper/acquisition/call_extractor.gd", "tests/unit/test_call_extractor.gd", "tests/pending/test_c08_relations.pending (suppression)"],
  ["Supprimer le marqueur de `test_c08_relations` ; coller l'échec.",
   "Écrire les tests sur `attendu.json` (relations).",
   "Écrire l'extracteur.",
   "Faire passer les tests sans les modifier."],
  [("S37.6-a",) + tests("test_call_extractor", "test_c08_relations"),
   ("S37.6-b", f"{RUN} | grep -c \"relation certaine fausse\"", "0")],
  ["(CE) Résoudre un appel sur receveur non typé par son nom de méthode : un test signale une relation certaine fausse ; annuler."],
  "C-08 ; CAP-09 (appels dynamiques non résolus) ; INV-03.",
  contexte=["docs/contracts/C-08.md", "tests/fixtures/syntaxe/attendu.json"])

t("S37.7", "inventaire", "Inventaire du projet sans instanciation", "D", "V", ["S37.2", "S37.6"],
  ["`acquisition/project_inventory.gd` : parcourt res:// par la façade d'introspection, lit chaque script (déclarations et relations), chaque scène (nœuds, scripts attachés, connexions déclarées dans le .tscn) et chaque ressource, sans rien instancier.",
   "Un fichier illisible produit un diagnostic à code stable et l'inventaire continue ; le résultat est un ProgramSnapshot au format C-08, avec sa couverture.",
   "Activer les tests de contrat C-08 sur l'instantané."],
  ["addons/godot_dev_mapper/acquisition/project_inventory.gd", "tests/unit/test_project_inventory.gd", "tests/pending/test_c08_snapshot.pending (suppression)"],
  ["Supprimer le marqueur de `test_c08_snapshot` ; coller l'échec.",
   "Écrire les tests sur `tests/fixtures/mini_projet/`, dont un fichier illisible.",
   "Écrire l'inventaire.",
   "Mesurer le temps sur le banc d'essai."],
  [("S37.7-a",) + tests("test_project_inventory", "test_c08_snapshot"), ("S37.7-b",) + DEPS],
  ["(CE) Lever une erreur au premier fichier illisible au lieu d'un diagnostic : le test d'isolation échoue ; annuler.",
   "(CE) Instancier une scène pendant l'inventaire : le test « aucune instance créée » échoue ; annuler."],
  "C-08 ; CAP-08 (sans instancier le projet) ; plan §8 (15 s pour 300 scripts).",
  contexte=["docs/contracts/C-08.md", "docs/construction/mvp.md, P4b"])

t("S37.8", "resolution-provenance", "Résolution entre scripts et fusion avec le graphe déclaré", "D", "C", ["S37.7"],
  ["`acquisition/resolver.gd` : résout les cibles d'appel entre scripts par la table des class_name, les types déclarés et les autoloads ; garde « partiel » quand plusieurs cibles sont possibles.",
   "Fusionne l'instantané extrait avec le graphe déclaré `.flow.json` : chaque relation garde sa provenance (extraite ou déclarée) ; une réindexation n'écrase jamais une annotation humaine."],
  ["addons/godot_dev_mapper/acquisition/resolver.gd", "tests/unit/test_resolver.gd", "tests/fixtures/resolution/"],
  ["Écrire les fixtures de résolution (héritage, autoload, cible ambiguë, déclaration contradictoire).",
   "Écrire les tests ; les voir échouer.",
   "Écrire la résolution.",
   "Écrire la fusion avec le graphe déclaré."],
  [("S37.8-a",) + tests("test_resolver"), ("S37.8-b",) + DEPS],
  ["(CE) Donner la priorité à la relation extraite sur la relation déclarée contradictoire : le test de provenance échoue ; annuler."],
  "INV-03 (provenance conservée) ; plan §5 (annotations jamais écrasées) ; C-05 et C-08.",
  contexte=["docs/CONTRACTS.md (C-05)", "docs/contracts/C-08.md", "docs/plan-directeur.md §5"])

t("S37.9", "cache-index", "Cache d'index par révision de fichier", "D", "V", ["S37.7"],
  ["`acquisition/index_cache.gd` : cache régénérable dans le dossier de cache du projet (non versionné), clé = empreinte du contenu de chaque fichier ; un fichier inchangé n'est pas relu ; un fichier modifié ou supprimé est réindexé ou retiré.",
   "Version du format de cache : une version inconnue invalide le cache sans erreur."],
  ["addons/godot_dev_mapper/acquisition/index_cache.gd", "tests/unit/test_index_cache.gd"],
  ["Écrire les tests (inchangé, modifié, supprimé, version inconnue) ; les voir échouer.",
   "Écrire le cache.",
   "Mesurer le second inventaire du banc d'essai (cache chaud) et le noter."],
  [("S37.9-a",) + tests("test_index_cache"), ("S37.9-b",) + DEPS],
  ["(CE) Ne pas invalider l'entrée d'un fichier modifié : le test « modifié » échoue ; annuler."],
  "Plan §8 (caches d'index : régénérables, non versionnés).",
  contexte=["docs/plan-directeur.md §8"])

t("S37.10", "grand-projet", "Grand projet de mesure : 300 scripts ou plus", "V", "C", ["S37"],
  ["Si le banc d'essai compte moins de 300 scripts : choisir un second jeu Godot 4.x open source de 300 scripts ou plus, dont les licences permettent de redistribuer une copie modifiée, à une révision épinglée.",
   "Le copier dans la branche orpheline `banc/<grand>-base`, l'importer avec Godot 4.7.2, corriger seulement la migration ; l'ajouter à `benches/benches.json`.",
   "Si le banc d'essai compte déjà 300 scripts ou plus : le noter, et la tâche se limite au contrôle S37.10-a."],
  ["benches/benches.json", "docs/benches/<grand>.md", "tools/check_benches.py (comptage des scripts, licence « non vérifié » refusée)", "branche orpheline banc/<grand>-base (hors de main)"],
  ["Compter les scripts du banc d'essai ; décider si un second jeu est nécessaire.",
   "Chercher et vérifier les candidats (licences, version, nombre de scripts), à une révision épinglée.",
   "Créer et pousser `banc/<grand>-base` (procédure de S08).",
   "Importer et corriger la migration, un commit par correction.",
   "Mettre à jour `benches/benches.json` et écrire `docs/benches/<grand>.md`.",
   "Étendre `tools/check_benches.py` : nombre de scripts .gd de chaque banc (lu dans benches.json, champ scripts, relevé par la tâche), sortie 1 si aucun banc n'atteint 300 ou si une licence vaut « non vérifié »."],
  [("S37.10-a", "python3 tools/check_benches.py; echo $?", "0, un jeu de 300 scripts ou plus référencé"),
   ("S37.10-b", "git ls-remote origin \"refs/heads/banc/*-base\" | wc -l", "1 ou 2")],
  ["(CE) Remplacer une licence par « non vérifié » dans benches.json : S37.10-a sort en 1 ; annuler."],
  "Porte du MVP (300 scripts indexés) ; règle des licences des bancs d'essai.",
  contexte=["docs/benches/selection.md", "benches/benches.json"])

t("S37.11", "golden-banc", "Tests de référence sur le banc d'essai et contrôle CI", "V", "D", ["S37.8", "S37.9", "S37.10"],
  ["`tests/integration/run_inventory_bench.sh` : récupère la copie du banc, lance l'inventaire, compare les relations à l'étalon de S36.1 : aucune relation certaine fausse, taux d'appels directs résolus affiché ; mesure le temps sur le grand projet.",
   "`tools/ci/checks.d/70-inventory.sh` : OK, KO, ou IGNORÉ si les branches de banc sont absentes, jamais un faux OK.",
   "Chaque faux positif découvert devient une fixture de `tests/fixtures/syntaxe/`."],
  ["tests/integration/run_inventory_bench.sh", "tools/ci/checks.d/70-inventory.sh", "tests/fixtures/syntaxe/ (ajouts seulement)", "docs/benches/<nom>.md (section « Inventaire »)"],
  ["Écrire le script de comparaison à l'étalon.",
   "Ajouter la mesure de temps sur le grand projet (objectif : 15 s au plus pour 300 scripts).",
   "Écrire `70-inventory.sh`.",
   "Transformer chaque faux positif en fixture."],
  [("S37.11-a", "GODOT=\"$B\" tests/integration/run_inventory_bench.sh; echo $?", "0 ; « relations certaines fausses : 0 » ; temps affiché"),
   ("S37.11-b", "GODOT=\"$B\" tools/ci/run_all_checks.sh | grep inventory", "CHECK inventory OK ou IGNORÉ")],
  ["(CE) Ajouter une relation fausse au résultat avant comparaison : S37.11-a sort en 1 ; annuler."],
  "CAP-08, CAP-09 ; porte du MVP ; INV-07 (limites explicites).",
  contexte=["benches/<nom>/relations_attendues.json", "docs/benches/<grand>.md"],
  recette=["Relire le fichier de relations attendues du banc d'essai (étalon de S36.1)."])


# =====================================================================================================
# MVP — P5 Navigation et arborescence res://, CAP-10 (revue S38)
# =====================================================================================================

t("S38.1", "contrat-c09", "Contrat C-09 : requêtes de navigation", "C", "V", ["S38"],
  ["Écrire `docs/contracts/C-09.md` : search(texte, types, limite), definition_at(chemin, ligne), callers et callees (définition, profondeur, limite), res_tree(dossier), elements_of(fichier) ; chaque résultat porte sa provenance et sa résolution ; toute expansion est bornée et signale « tronqué ».",
   "Écrire les tests de contrat `tests/contract/test_c09_*.gd` sur un instantané de fixture, avec leurs marqueurs au nom de S38.2 à S38.4."],
  ["docs/contracts/C-09.md", "docs/CONTRACTS.md (index : lien vers C-09)", "tests/contract/fixtures/navigation_query/", "tests/contract/test_c09_search.gd", "tests/contract/test_c09_calls.gd", "tests/contract/test_c09_res_tree.gd", "tests/pending/test_c09_*.pending"] + OUTILS_CONTRAT,
  ["Relire C-08 et le parcours J2 et J3 du plan §7.",
   "Rédiger C-09 et ses sept rubriques.",
   "Écrire l'instantané de fixture (cycle d'appels, relation non résolue, 2 000 définitions pour la borne).",
   "Écrire les trois tests de contrat et leurs marqueurs."],
  [("S38.1-a", "python3 tools/check_contracts.py C-09 && python3 tools/validate_fixtures.py; echo $?", "0, C-09 a ses sept rubriques ; fixtures navigation_query validées"),
   ("S38.1-b", f"{RUN} | grep GDM_TESTS", "failed=0, trois tests C-09 en attente")],
  ["(CE) Ajouter la fixture `tests/contract/fixtures/navigation_query/invalid_UNBOUNDED__sans_limite.json` (requête sans limite) puis retirer la règle de borne de validate_fixtures.py : S38.1-a sort en 1 ; remettre la règle : la fixture est rejetée avec ce code ; garder la fixture."],
  "Plan §7 (J2, J3) ; P5 (expansion bornée, provenance).",
  contexte=["docs/contracts/C-08.md", "docs/plan-directeur.md §7"])

t("S38.2", "index-recherche", "Index de recherche des définitions", "D", "V", ["S38.1"],
  ["`projections/search_index.gd` : recherche par nom, nom qualifié, fichier et type ; préfixe et sous-chaîne, sans tenir compte de la casse ; classement stable (correspondance exacte, puis préfixe, puis sous-chaîne) ; limite et « tronqué ».",
   "Activer `test_c09_search`."],
  ["addons/godot_dev_mapper/projections/search_index.gd", "tests/unit/test_search_index.gd", "tests/pending/test_c09_search.pending (suppression)"],
  ["Supprimer le marqueur ; coller l'échec.", "Écrire les tests unitaires.", "Écrire l'index.", "Mesurer une recherche sur l'instantané du grand projet."],
  [("S38.2-a",) + tests("test_search_index", "test_c09_search"),
   ("S38.2-b", f"{RUN} | grep \"search_index temps\"", "50 ms au plus par recherche sur 300 scripts")],
  ["(CE) Supprimer la limite : le test de borne échoue ; annuler."],
  "C-09 ; projections dépend de core et store seulement.",
  contexte=["docs/contracts/C-09.md"])

t("S38.3", "appelants-appeles", "Appelants et appelés, expansion bornée", "D", "V", ["S38.1"],
  ["`projections/call_queries.gd` : callers et callees en largeur, profondeur et nombre bornés, cycles détectés, relations non résolues montrées comme telles, provenance sur chaque arête.",
   "Activer `test_c09_calls`."],
  ["addons/godot_dev_mapper/projections/call_queries.gd", "tests/unit/test_call_queries.gd", "tests/pending/test_c09_calls.pending (suppression)"],
  ["Supprimer le marqueur ; coller l'échec.", "Écrire les tests (cycle, borne, non résolu, provenance).", "Écrire les requêtes."],
  [("S38.3-a",) + tests("test_call_queries", "test_c09_calls"), ("S38.3-b",) + DEPS],
  ["(CE) Compter une relation non résolue comme un appelant certain : le test correspondant échoue ; annuler."],
  "C-09 ; INV-03 ; P5 (expansion bornée).",
  contexte=["docs/contracts/C-08.md", "docs/contracts/C-09.md"])

t("S38.4", "arborescence-res", "Arborescence res:// et correspondance fichier ↔ éléments", "D", "V", ["S38.1"],
  ["`projections/res_tree.gd` : arbre de res:// avec, pour chaque fichier, le nombre de définitions, de relations et de diagnostics ; elements_of(fichier) et definition_at(chemin, ligne).",
   "Activer `test_c09_res_tree`."],
  ["addons/godot_dev_mapper/projections/res_tree.gd", "tests/unit/test_res_tree.gd", "tests/pending/test_c09_res_tree.pending (suppression)"],
  ["Supprimer le marqueur ; coller l'échec.", "Écrire les tests.", "Écrire la projection."],
  [("S38.4-a",) + tests("test_res_tree", "test_c09_res_tree"), ("S38.4-b",) + DEPS],
  ["(CE) Renvoyer la définition suivante quand la ligne tombe entre deux fonctions : le test definition_at échoue ; annuler."],
  "C-09 ; C-02 (ancrages).",
  contexte=["docs/CONTRACTS.md (C-02)", "docs/contracts/C-09.md"])

t("S38.5", "vue-graphe", "Vue de graphe bornée, selon SPIKE-03", "D", "V", ["S38.3"],
  ["`ui/graph_view.gd` et `.tscn`, selon l'option retenue par SPIKE-03 : voisinage d'une définition, expansion à la demande, 300 éléments visibles au plus, provenance et résolution affichées par texte ou icône (jamais la couleur seule), navigation au clavier.",
   "L'interface ne calcule rien : elle lit les projections."],
  ["addons/godot_dev_mapper/ui/graph_view.gd", "addons/godot_dev_mapper/ui/graph_view.tscn", "tests/unit/test_graph_view_model.gd", "tools/harness/ui_load.gd"],
  ["Relire la décision de SPIKE-03.", "Écrire le modèle de vue et ses tests (bornes, expansion, libellés).", "Écrire la vue.",
   "Écrire `tools/harness/ui_load.gd` : charge une vue avec N éléments générés et affiche FRAME_MS (moyenne et 95e centile).",
   "Charger la vue sous écran virtuel avec 300 éléments ; mesurer le temps de frame et le noter."],
  [("S38.5-a",) + tests("test_graph_view_model"),
   ("S38.5-b", "xvfb-run -a \"$B\" --path . --rendering-driver opengl3 -s res://tools/harness/ui_load.gd -- graph_view 300 2>&1 | grep FRAME_MS", "temps de frame mesuré, rendu logiciel")],
  ["(CE) Afficher l'état « non résolu » par la seule couleur : le test des libellés échoue ; annuler."],
  "Plan §7 (SPIKE-03, 300 éléments) ; module ui : lit les projections seulement.",
  contexte=["docs/spikes/SPIKE-03.md", "docs/contracts/C-09.md"],
  recette=["Lisibilité de la vue de graphe, sur ta machine."])

t("S38.6", "panneau-navigation", "Onglet de navigation : recherche, appelants, res://", "D", "V", ["S38.2", "S38.4", "S38.5", "S39.12"],
  ["`ui/vues/navigation/` : champ de recherche, résultats, liste des appelants et des appelés, arbre res://, ouverture du code par `editor/source_opener.gd` ; parcours J2 et J3.",
   "L'onglet s'ajoute par son seul dossier : `ui/vues/navigation/vue.gd` le décrit, le panneau principal de S39.12 le découvre ; aucun fichier commun modifié. L'index se construit par l'inventaire de P4b, avec le cache."],
  ["addons/godot_dev_mapper/ui/vues/navigation/", "addons/godot_dev_mapper/editor/index_service.gd", "tests/unit/test_index_service.gd", "rapports/S38.6/"],
  ["Écrire `editor/index_service.gd` (inventaire, cache, mise à jour à la sauvegarde d'un script) et ses tests.", "Écrire l'onglet dans `ui/vues/navigation/`.",
   "Écrire `ui/vues/navigation/vue.gd` (titre, ordre, scène) ; vérifier que l'onglet apparaît.", "Charger l'éditeur sans interface avec le plugin : aucune erreur ; capture de l'onglet."],
  [("S38.6-a",) + tests("test_index_service"),
   ("S38.6-b", "\"$B\" --headless --editor --path . --quit-after 120 2>&1 | grep -cE \"SCRIPT ERROR|ERROR:\"", "0"),
   ("S38.6-c", "GODOT=\"$B\" tools/harness/editor_driver/capture_onglet.sh navigation rapports/S38.6/navigation.png; echo $?", "0, capture écrite")],
  ["(CE) Faire appeler le store directement par le panneau : `check_deps.py` signale la dépendance interdite ; annuler."],
  "Plan §4 (ui → projections) ; C-09.",
  contexte=["docs/contracts/C-09.md", "addons/godot_dev_mapper/editor/source_opener.gd"])

t("S38.7", "requetes-cli", "Requêtes de navigation en ligne de commande", "D", "V", ["S38.2", "S38.3", "S38.4"],
  ["Étendre `tools/gdm_query.gd` : `index <projet>` (instantané en JSON), `search <texte>`, `callers <définition>`, `callees <définition>`, `file <chemin>` ; sortie texte stable, provenance sur chaque ligne.",
   "Il sert aux agents (mesure par substitution) et aux tests d'intégration."],
  ["tools/gdm_query.gd", "tests/integration/run_query.sh"],
  ["Écrire `tests/integration/run_query.sh` sur `tests/fixtures/mini_projet/` ; le voir échouer.", "Ajouter les sous-commandes.", "Vérifier la sortie sur le banc d'essai."],
  [("S38.7-a", "GODOT=\"$B\" tests/integration/run_query.sh; echo $?", "0"),
   ("S38.7-b", "\"$B\" --headless --path . -s res://tools/gdm_query.gd -- callers inconnue 2>&1 | tail -1", "« définition inconnue », code 1, sans plantage")],
  ["(CE) Retirer la provenance des lignes de sortie : run_query.sh échoue ; annuler."],
  "C-09 ; même code de requêtes que l'interface.",
  contexte=["tools/gdm_query.gd (S34)", "docs/contracts/C-09.md"])

t("S38.8", "essai-navigation", "Essai de navigation sous écran virtuel (J2 et J3)", "V", "D", ["S38.6"],
  ["Étendre `tools/harness/editor_driver/` d'un scénario de navigation : rechercher une fonction du banc d'essai, ouvrir ses appelants, ouvrir le code, cliquer un fichier de res:// et retrouver son élément.",
   "`tests/integration/run_navigation.sh` lance le scénario sous xvfb-run sur une copie du banc et produit des captures dans `rapports/S38.8/`."],
  ["tools/harness/editor_driver/ (scénario de navigation)", "tests/integration/run_navigation.sh", "rapports/S38.8/", "tools/ci/checks.d/75-navigation.sh"],
  ["Écrire le scénario.", "Écrire `run_navigation.sh` (ligne OPEN avec fichier et ligne attendus).", "Produire les captures.", "Écrire `75-navigation.sh` (OK, KO ou IGNORÉ si xvfb-run est absent)."],
  [("S38.8-a", "GODOT=\"$B\" tests/integration/run_navigation.sh; echo $?", "0 et une ligne OPEN conforme"),
   ("S38.8-b", "ls rapports/S38.8/*.png | wc -l", "au moins 3")],
  ["(CE) Faire ouvrir par la passerelle la ligne de l'appelant au lieu de celle de la définition : S38.8-a échoue ; annuler."],
  "Parcours J2 et J3 du plan §7 ; le vérificateur décrit chaque capture.",
  contexte=["tools/harness/editor_driver/ (S26, S31)"])

t("S38.9", "cartographie-substitution", "Test de cartographie par substitution", "V", "C", ["S38.7", "S38.8"],
  ["Mesurer deux tâches de cartographie sur le banc d'essai, avec et sans l'outil : retrouver tous les appelants d'une fonction choisie au hasard ; expliquer un système inconnu (par exemple les états d'un ennemi).",
   "Avec l'outil : `gdm_query` et captures du panneau. Sans : lecture du code et recherche texte. Compter exécutions, lectures, temps, et la justesse contre l'étalon.",
   "Écrire `docs/mesures/cartographie-mvp-substitution.md` (signal pour un agent, pas pour une personne) ; la mesure humaine se fait à la recette."],
  ["docs/mesures/cartographie-mvp-substitution.md"],
  ["Tirer la fonction et le système au hasard, avec la graine notée.", "Tâche 1 sans l'outil, puis avec.", "Tâche 2 sans l'outil, puis avec.", "Comparer à l'étalon et écrire la conclusion."],
  [("S38.9-a", "grep -c \"pas pour une personne\" docs/mesures/cartographie-mvp-substitution.md", "1"),
   ("S38.9-b", "grep -cE \"^\\| (avec|sans)\" docs/mesures/cartographie-mvp-substitution.md", "au moins 4")],
  ["(CE) Le vérificateur rejoue la tâche 1 avec l'outil : même liste d'appelants."],
  "Porte du MVP (test de cartographie gagnant) ; plan §9 (mesure de valeur élargie).",
  contexte=["docs/construction/mvp.md, P5", "benches/<nom>/relations_attendues.json"],
  recette=["Test de cartographie chronométré, par toi, avec et sans l'outil."])


# =====================================================================================================
# MVP — P6 Historique, persistance, protocole MVP, CAP-11 et CAP-07 complet (revue S39)
# =====================================================================================================

t("S39.1", "contrats-c04-c06-v2", "Révision des contrats C-04, C-06 et C-07 en version 2", "C", "V", ["S39"],
  ["Étendre C-04 (enveloppe), C-06 (Event Store) et C-07 (protocole de session : négociation de capacités, connexion tardive, reconnexion) en version 2 : marqueurs de lacune explicites, frames et ticks physiques, doublons, références tardives, export ; la version 1 reste lisible.",
   "Mettre à jour les schémas, ajouter les fixtures v2 (valides et invalides) dans `tests/contract/fixtures/<kind>/`, rendre les sessions enregistrées du POC fixtures de compatibilité ascendante, écrire les tests de contrat v2 avec leurs marqueurs au nom des tâches qui les activent : S39.3 (codec), S39.4 (FlowTrace), S39.6 (réception), S39.7 (store)."],
  ["docs/CONTRACTS.md (C-04, C-06, C-07)", "contracts/", "tests/contract/", "tests/pending/"] + OUTILS_CONTRAT,
  ["Relire C-04, C-06, C-07, les sessions enregistrées et le plan §6 (contrat runtime du MVP).",
   "Rédiger C-04 v2 avec l'analyse d'impact sur la v1.", "Rédiger C-06 v2 et C-07 v2 (capacités, connexion tardive, reconnexion).", "Écrire schémas et fixtures v2 ; étendre `tools/validate_fixtures.py` si les règles de niveau 2 changent.",
   "Écrire les tests de contrat v2 et leurs marqueurs (S39.3, S39.4, S39.6, S39.7).", "Écrire l'analyse d'impact dans le rapport."],
  [("S39.1-a", "python3 tools/validate_fixtures.py; echo $?", "0, fixtures v1 et v2 validées"),
   ("S39.1-b", "python3 tools/check_contracts.py; echo $?", "0"),
   ("S39.1-c", f"{RUN} | grep GDM_TESTS", "failed=0 ; tests v2 en attente")],
  ["(CE) Supprimer la compatibilité v1 dans le schéma : une session du POC est rejetée par S39.1-a ; annuler."],
  "Plan §6 (contrat runtime MVP) ; gel des contrats (S15) : changement de version et accord d'IA 1 et d'IA 3. Versions cibles : C-04 v2, C-06 v2, C-07 v2 (S40.1 les complète pour les blocs ; la V1 ouvre la v3).",
  contexte=["docs/CONTRACTS.md (C-04, C-06, C-07)", "tests/contract/fixtures/sessions/", "docs/plan-directeur.md §6"], creneaux=2)

t("S39.2", "contrat-c10-session", "Contrat C-10 : format de session persistée", "C", "V", ["S39"],
  ["Écrire `docs/contracts/C-10.md` : fichier de session en JSON par lots, avec schema_version, en-tête (session, révision, profil moteur, configuration de capture), lots, lacunes, marqueur de fin ; emplacement selon D-08 ; sauvegarde atomique ; refus explicite d'une version inconnue et d'un fichier tronqué.",
   "Schéma, fixtures dans `tests/contract/fixtures/session_file/` (valide, tronqué, version inconnue, lot dans le désordre) et tests de contrat avec marqueurs."],
  ["docs/contracts/C-10.md", "docs/CONTRACTS.md (index : lien vers C-10)", "contracts/schemas/session_file.v1.schema.json", "tests/contract/fixtures/session_file/", "tests/contract/test_c10_session_file.gd", "tests/pending/test_c10_session_file.pending"] + OUTILS_CONTRAT,
  ["Relire D-08 et le plan §8 (données et emplacements).", "Rédiger C-10.", "Écrire schéma et fixtures.", "Écrire le test de contrat et son marqueur (S39.8)."],
  [("S39.2-a", "python3 tools/validate_fixtures.py; echo $?", "0 ; fixtures session_file comprises, le fichier tronqué rejeté avec son code"),
   ("S39.2-b", "python3 tools/check_contracts.py C-10; echo $?", "0")],
  ["(CE) Accepter un fichier sans marqueur de fin dans le schéma : la fixture tronquée passe à tort ; annuler."],
  "Plan §8 (sauvegarde atomique, versions) ; INV-07, INV-08.",
  contexte=["docs/plan-directeur.md §8", "docs/DECISIONS.md (D-08)"])

t("S39.3", "codec-v2", "Codec de l'enveloppe v2, lecture de la v1", "D", "C", ["S39.1"],
  ["`addons/godot_dev_mapper_runtime/envelope.gd` et `protocol/envelope_codec.gd` en v2 : nouveaux champs (frame, tick physique, capacités, marqueurs de lacune) ; décodage de la v1 conservé ; version inconnue rejetée.",
   "Activer les tests de contrat v2 du codec."],
  ["addons/godot_dev_mapper_runtime/envelope.gd", "addons/godot_dev_mapper/protocol/envelope_codec.gd", "tests/pending/ (suppression des marqueurs du codec)"],
  ["Supprimer les marqueurs du codec ; coller l'échec.", "Encodage v2.", "Décodage v2 et v1.", "Faire passer les tests sans les modifier."],
  [("S39.3-a",) + tests("test_c04"), ("S39.3-b",) + DEPS],
  ["(CE) Décoder une version 3 comme une version 2 : le test de version inconnue échoue ; annuler."],
  "C-04 v2 ; INV-06 pour envelope.gd.",
  contexte=["docs/CONTRACTS.md (C-04)"])

t("S39.4", "flowtrace-v2", "FlowTrace v2 : capacités, frames, ticks, nouveaux événements", "D", "C", ["S39.3"],
  ["`flow_trace.gd` : annonce de capacités au « prêt », numéro de frame et tick physique sur chaque lot, événements tree_entered et tree_exited (helper facultatif), signal_emit, signal_received et state_change.",
   "Le chemin désactivé reste au coût mesuré par SPIKE-05 ; aucune construction de chaîne au point d'appel."],
  ["addons/godot_dev_mapper_runtime/flow_trace.gd", "addons/godot_dev_mapper_runtime/runtime_facade.gd", "tests/unit/test_flow_trace_internals.gd", "tests/pending/ (suppression des marqueurs FlowTrace v2)"],
  ["Supprimer les marqueurs ; coller l'échec.", "Capacités et horodatage par frame et tick.", "Nouveaux événements.", "Relancer la mesure du chemin désactivé (tools/bench/flow_trace_cost) et la comparer à SPIKE-05."],
  [("S39.4-a",) + tests("test_flow_trace_internals", "test_c07"),
   ("S39.4-b", "GODOT=\"$B\" tools/bench/flow_trace_cost/run.sh | grep desactive", "coût du chemin désactivé dans la marge de SPIKE-05")],
  ["(CE) Construire la clé par concaténation au point d'appel dans le banc de mesure : le coût désactivé dépasse la marge ; annuler."],
  "C-07 ; plan §6 (coût du chemin désactivé) ; INV-06.",
  contexte=["docs/CONTRACTS.md (C-04, C-07)", "docs/spikes/SPIKE-05.md"])

t("S39.5", "connexion-tardive-jeu", "Connexion tardive et reconnexion, côté jeu", "D", "C", ["S39.4"],
  ["Côté runtime : un éditeur qui se connecte en cours de partie reçoit l'état initial (registre des instances) et la séquence courante ; après une coupure puis une reconnexion, la session continue avec un marqueur de lacune explicite couvrant l'intervalle perdu.",
   "Le bail et la réserve de contrôle restent valides."],
  ["addons/godot_dev_mapper_runtime/flow_trace.gd", "tests/unit/test_flow_trace_reconnect.gd"],
  ["Écrire les tests (horloge factice, transport de substitution) ; les voir échouer.", "Connexion tardive.", "Reconnexion et marqueur de lacune.", "Vérifier bail et réserve."],
  [("S39.5-a",) + tests("test_flow_trace_reconnect"), ("S39.5-b",) + DEPS],
  ["(CE) Reprendre la séquence à zéro après reconnexion : le test de lacune explicite échoue ; annuler."],
  "C-04 v2, C-07 ; plan §6 (MVP : connexion tardive, reconnexion).",
  contexte=["docs/CONTRACTS.md (C-04, C-07)"])

t("S39.6", "reception-v2", "Réception v2 côté éditeur", "D", "C", ["S39.3", "S39.7"],
  ["`editor/session_controller.gd` : négociation de capacités, connexion tardive (état initial), reconnexion, doublons écartés par séquence, références tardives conservées et marquées, marqueurs de lacune transmis au store.",
   "Les sessions enregistrées v1 et v2 se rejouent toutes."],
  ["addons/godot_dev_mapper/editor/session_controller.gd", "tests/unit/test_session_controller.gd", "tests/fixtures/sessions_v2/", "tests/pending/ (suppression des marqueurs de réception v2)"],
  ["Supprimer les marqueurs de réception v2 ; coller l'échec.", "Écrire les sessions v2 enregistrées (tardive, reconnexion, doublons, référence tardive).", "Écrire les tests ; les voir échouer.", "Implémenter, en transmettant les lacunes à l'API de lacunes explicites du store v2 (S39.7).", "Rejouer aussi les sessions v1."],
  [("S39.6-a",) + tests("test_session_controller"), ("S39.6-b",) + DEPS],
  ["(CE) Accepter un lot en double : le test des doublons échoue ; annuler."],
  "C-04 v2, C-06 v2, C-07 ; compatibilité ascendante.",
  contexte=["docs/CONTRACTS.md (C-04, C-06, C-07)"])

t("S39.7", "store-v2", "Event Store v2 : lacunes explicites, doublons, frames", "D", "V", ["S39.1"],
  ["`store/` : lacunes explicites (raison, intervalle), doublons ignorés, index par frame et tick, rétention inchangée avec son marqueur « tronqué avant seq N », requête de fenêtre par frame.",
   "Activer les tests de contrat C-06 v2."],
  ["addons/godot_dev_mapper/store/", "tests/unit/test_event_store.gd", "tests/pending/ (suppression des marqueurs C-06 v2)"],
  ["Supprimer les marqueurs ; coller l'échec.", "Lacunes explicites et doublons.", "Index par frame et tick.", "Faire passer les tests sans les modifier."],
  [("S39.7-a",) + tests("test_event_store", "test_c06"), ("S39.7-b",) + DEPS],
  ["(CE) Fusionner deux lacunes adjacentes de raisons différentes : le test de lacunes échoue ; annuler."],
  "C-06 v2 ; INV-04, INV-07.",
  contexte=["docs/CONTRACTS.md (C-06)"])

t("S39.8", "persistance-session", "Sauvegarde atomique et rechargement des sessions", "D", "C", ["S39.2", "S39.7", "S37.2"],
  ["`persistence/session_writer.gd` : écriture par fichier temporaire puis renommage, par la façade éditeur si l'API est sensible ; `persistence/session_reader.gd` : validation à l'import, refus clair d'une version inconnue et d'un fichier tronqué.",
   "Activer `test_c10_session_file`."],
  ["addons/godot_dev_mapper/persistence/session_writer.gd", "addons/godot_dev_mapper/persistence/session_reader.gd", "addons/godot_dev_mapper/compat/engine_facade.gd (renommage atomique, si nécessaire)", "tools/deps_rules.json (API de renommage, si elle est sensible)", "tests/unit/test_session_persistence.gd", "tests/pending/test_c10_session_file.pending (suppression)"],
  ["Supprimer le marqueur ; coller l'échec.", "Écrire l'écriture atomique.", "Écrire la lecture et ses refus.", "Tester une coupure au milieu d'une écriture : l'ancien fichier reste intact."],
  [("S39.8-a",) + tests("test_session_persistence", "test_c10_session_file"), ("S39.8-b",) + DEPS],
  ["(CE) Écrire directement dans le fichier final : le test de coupure laisse un fichier tronqué et échoue ; annuler.",
   "(CE) Charger un fichier tronqué : refus avec un message qui nomme le fichier et l'endroit."],
  "C-10 ; plan §8 (sauvegarde atomique) ; INV-09 pour l'API de renommage.",
  contexte=["docs/contracts/C-10.md", "docs/plan-directeur.md §8"])

t("S39.9", "relecture", "Relecture d'une session sans le jeu", "D", "V", ["S39.6", "S39.8", "S39.12"],
  ["Ouvrir une session enregistrée dans l'éditeur, sans jeu : le store se remplit depuis le fichier, les projections et le panneau du POC l'affichent comme une session terminée ; une session du POC se recharge.",
   "Commande « Ouvrir une session » dans l'onglet journal ; la session vivante et les sessions relues ne se mélangent jamais."],
  ["addons/godot_dev_mapper/editor/session_library.gd", "addons/godot_dev_mapper/ui/vues/journal/ (commande d'ouverture)", "tests/unit/test_session_library.gd"],
  ["Écrire les tests (session v2, session du POC, deux sessions ouvertes) ; les voir échouer.", "Écrire `session_library.gd`.", "Ajouter la commande au panneau."],
  [("S39.9-a",) + tests("test_session_library"), ("S39.9-b",) + DEPS],
  ["(CE) Ajouter les événements relus à la session vivante : le test de séparation échoue ; annuler."],
  "CAP-11 ; plan §6 (ancienne session archivée à part).",
  contexte=["docs/CONTRACTS.md (C-06)", "docs/contracts/C-10.md"])

t("S39.10", "banc-reconnexion", "Banc de reconnexion sans éditeur", "V", "C", ["S39.5", "S39.6"],
  ["Étendre `tools/harness/fake_editor.gd` de scénarios : connexion tardive, coupure puis reconnexion, doublon injecté.",
   "`tests/integration/run_reconnect.sh` et `tools/ci/checks.d/66-reconnect.sh` : chaque scénario vérifié de bout en bout, lacune explicite comprise."],
  ["tools/harness/fake_editor.gd", "tests/integration/run_reconnect.sh", "tools/ci/checks.d/66-reconnect.sh"],
  ["Écrire les scénarios.", "Écrire `run_reconnect.sh`.", "Écrire `66-reconnect.sh`."],
  [("S39.10-a", "GODOT=\"$B\" tests/integration/run_reconnect.sh; echo $?", "0, trois scénarios OK"),
   ("S39.10-b", "GODOT=\"$B\" tools/ci/run_all_checks.sh | grep reconnect", "CHECK reconnect OK")],
  ["(CE) Faire perdre le marqueur de lacune par la passerelle : le scénario de reconnexion échoue ; annuler."],
  "Porte de P6 (reconnexion testée sur le banc sans éditeur).",
  contexte=["tools/harness/fake_editor.gd", "docs/CONTRACTS.md (C-07)"])

t("S39.11", "export-session", "Export d'une fenêtre de session", "D", "V", ["S39.8"],
  ["Exporter une fenêtre bornée d'une session (intervalle de séquence ou de frames) dans un fichier au format C-10, lacunes et métadonnées comprises ; l'export se relit."],
  ["addons/godot_dev_mapper/persistence/session_export.gd", "tests/unit/test_session_export.gd"],
  ["Écrire les tests (fenêtre, lacune à cheval, relecture) ; les voir échouer.", "Écrire l'export."],
  [("S39.11-a",) + tests("test_session_export"), ("S39.11-b",) + DEPS],
  ["(CE) Omettre une lacune qui chevauche la fenêtre : le test échoue ; annuler."],
  "C-10 ; INV-07 (pertes visibles).",
  contexte=["docs/contracts/C-10.md"])

t("S39.12", "panneau-onglets", "Panneau principal à onglets découverts et capture d'un onglet", "D", "V", ["S39"],
  ["`ui/main_panel.gd` et `.tscn` : panneau principal à onglets. Au chargement, il découvre chaque dossier `addons/godot_dev_mapper/ui/vues/<nom>/` qui contient `vue.gd` (descripteur : titre, ordre, scène de l'onglet) et en fait un onglet, dans l'ordre déclaré. Une vue qui échoue au chargement donne un onglet « erreur » qui nomme le fichier, sans bloquer les autres.",
   "Le journal du POC devient l'onglet `ui/vues/journal/` (il reprend `poc_panel`) ; `plugin.gd` charge le panneau principal au lieu de `poc_panel`. Ensuite, chaque nouvelle vue s'ajoute par son seul dossier `ui/vues/<nom>/` : aucune tâche ne modifie plus `plugin.gd` ni le panneau principal pour ajouter un onglet.",
   "`tools/harness/editor_driver/capture_onglet.sh <onglet> <fichier.png>` : copie temporaire du projet, éditeur sous écran virtuel avec le plugin et le pilote de S26, sélection de l'onglet, attente de 60 frames, capture PNG ; sortie 1 si l'onglet n'existe pas.",
   "Écrire la convention dans `addons/godot_dev_mapper/ui/vues/README.md`."],
  ["addons/godot_dev_mapper/ui/main_panel.gd", "addons/godot_dev_mapper/ui/main_panel.tscn", "addons/godot_dev_mapper/ui/vues/journal/", "addons/godot_dev_mapper/ui/vues/README.md",
   "addons/godot_dev_mapper/plugin.gd (chargement du panneau principal)", "tools/harness/editor_driver/ (option de capture d'un onglet, capture_onglet.sh)", "tests/unit/test_main_panel.gd", "rapports/S39.12/"],
  ["Écrire les tests de découverte (ordre, dossier sans vue.gd ignoré, vue en erreur isolée) ; les voir échouer.",
   "Écrire `main_panel.gd` et `.tscn`.",
   "Déplacer le journal du POC dans `ui/vues/journal/` ; faire charger le panneau principal par `plugin.gd`.",
   "Écrire `capture_onglet.sh` et l'option de sélection d'onglet du pilote.",
   "Écrire `ui/vues/README.md` ; capturer l'onglet journal."],
  [("S39.12-a",) + tests("test_main_panel"),
   ("S39.12-b", "\"$B\" --headless --editor --path . --quit-after 120 2>&1 | grep -cE \"SCRIPT ERROR|ERROR:\"", "0"),
   ("S39.12-c", "GODOT=\"$B\" tools/harness/editor_driver/capture_onglet.sh journal rapports/S39.12/journal.png; echo $?", "0, capture écrite ; le vérificateur y lit l'onglet journal")],
  ["(CE) Ajouter `ui/vues/essai/vue.gd` qui lève une erreur au chargement : l'onglet « erreur » apparaît et le journal reste ; retirer le dossier.",
   "(CE) Renommer `ui/vues/journal/vue.gd` : l'onglet disparaît sans autre modification, et S39.12-c sort en 1 ; annuler."],
  "Plan §4 (module ui : lit les projections seulement) ; INV-06 (le jeu ne voit rien de l'interface).",
  contexte=["addons/godot_dev_mapper/ui/poc_panel.gd", "addons/godot_dev_mapper/plugin.gd", "tools/harness/editor_driver/"])


# =====================================================================================================
# MVP — P7 Logique et Game Flow annoté, CAP-12 annoté (revue S40)
# =====================================================================================================

t("S40.1", "contrat-c11-blocs", "Contrat C-11 : blocs temporels déclarés", "C", "V", ["S40"],
  ["Écrire `docs/contracts/C-11.md` : TemporalBlockDefinition dans le graphe déclaré (`.flow.json` version 2, la version 1 restant lisible), événements block_begin et block_end (clé de bloc, occurrence, parent), cycle de vie (non démarré, actif, suspendu, terminé, échoué, abandonné, incomplet) et règles de transition ; un bloc ouvert à la fin de session ou touché par une lacune est « incomplet ».",
   "Réviser dans `docs/CONTRACTS.md` : C-05 en version 2 (`.flow.json` avec blocs), C-04 et C-07 (événements block_begin et block_end dans l'enveloppe v2, règles d'appel de block_begin et block_end) ; analyse d'impact dans le rapport.",
   "Schéma, fixtures dans `tests/contract/fixtures/<kind>/` et tests de contrat avec marqueurs (S40.3 pour la projection, S40.7 pour le chargeur v2)."],
  ["docs/contracts/C-11.md", "docs/CONTRACTS.md (C-04, C-05, C-07 ; index : lien vers C-11)", "contracts/", "tests/contract/fixtures/", "tests/contract/test_c11_blocks.gd", "tests/contract/test_c05_flow_v2.gd", "tests/pending/test_c11_blocks.pending", "tests/pending/test_c05_flow_v2.pending"] + OUTILS_CONTRAT,
  ["Relire C-04, C-05, C-07 et le plan §6 (temporalité).", "Rédiger C-11 et la version 2 de C-05.", "Ajouter block_begin et block_end à C-04 et à C-07 (règles d'appel).", "Écrire schéma et fixtures (imbriqués, interrompus, sans fin, .flow.json v1 et v2).", "Écrire les tests de contrat et leurs marqueurs (S40.3, S40.7)."],
  [("S40.1-a", "python3 tools/validate_fixtures.py; echo $?", "0"), ("S40.1-b", "python3 tools/check_contracts.py C-04 C-05 C-07 C-11; echo $?", "0")],
  ["(CE) Autoriser la transition actif → terminé sans block_end dans la table : la fixture « sans fin » passe à tort ; annuler."],
  "Plan §5 (TemporalBlock) et §6 (cycle de vie) ; INV-05.",
  contexte=["docs/CONTRACTS.md (C-04, C-05, C-07)", "docs/plan-directeur.md §5 et §6"])

t("S40.2", "flowtrace-blocs", "FlowTrace : déclaration des blocs", "D", "C", ["S40.1"],
  ["`FlowTrace.block_begin(clé)` et `FlowTrace.block_end(clé, statut)` : pile de blocs par producteur, occurrence identifiée, parent ; coût désactivé inchangé.",
   "Règles d'appel ajoutées à C-07 par S40.1, appliquées ici ; block_begin et block_end encodés et décodés par l'enveloppe et le codec (C-04 révisée par S40.1)."],
  ["addons/godot_dev_mapper_runtime/flow_trace.gd", "addons/godot_dev_mapper_runtime/envelope.gd", "addons/godot_dev_mapper/protocol/envelope_codec.gd", "tests/unit/test_flow_trace_blocks.gd"],
  ["Écrire les tests ; les voir échouer.", "Encoder et décoder block_begin et block_end (enveloppe et codec).", "Écrire l'API et la pile.", "Mesurer le coût désactivé."],
  [("S40.2-a",) + tests("test_flow_trace_blocks"), ("S40.2-b",) + DEPS],
  ["(CE) Ne pas dépiler sur block_end : le test d'imbrication échoue ; annuler."],
  "C-04, C-07, C-11 ; INV-06.",
  contexte=["docs/CONTRACTS.md (C-04, C-07)", "docs/contracts/C-11.md"])

t("S40.3", "projection-blocs", "Projection des blocs et de leurs occurrences", "D", "V", ["S40.1"],
  ["`projections/block_projection.gd` : occurrences reconstruites depuis les événements, imbrication, statut calculé selon C-11 ; jamais de bloc inféré.",
   "Activer `test_c11_blocks`."],
  ["addons/godot_dev_mapper/projections/block_projection.gd", "tests/unit/test_block_projection.gd", "tests/pending/test_c11_blocks.pending (suppression)"],
  ["Supprimer le marqueur ; coller l'échec.", "Écrire les tests (imbriqués, interrompu, lacune, fin de session).", "Écrire la projection."],
  [("S40.3-a",) + tests("test_block_projection", "test_c11_blocks"), ("S40.3-b",) + DEPS],
  ["(CE) Marquer « terminé » un bloc sans fin : le test échoue (contre-épreuve de la porte de P7) ; annuler."],
  "C-11 ; P7 (blocs déclarés seulement) ; INV-04.",
  contexte=["docs/contracts/C-11.md"])

t("S40.4", "projection-logique", "Projection logique : décisions et états", "D", "V", ["S40"],
  ["`projections/logic_projection.gd` : pour une définition de décision, nombre d'observations de chaque branche par instance ; pour une instance, suite de ses state_change ; chaque chiffre avec sa fenêtre et sa couverture.",
   "Une branche jamais observée s'affiche « non observée », jamais « jamais prise »."],
  ["addons/godot_dev_mapper/projections/logic_projection.gd", "tests/unit/test_logic_projection.gd"],
  ["Écrire les tests ; les voir échouer.", "Écrire la projection."],
  [("S40.4-a",) + tests("test_logic_projection"), ("S40.4-b",) + DEPS],
  ["(CE) Afficher « jamais prise » pour une branche sans observation : le test du libellé échoue ; annuler."],
  "INV-04 ; plan §6 (limites de preuve).",
  contexte=["docs/plan-directeur.md §6"])

t("S40.5", "vues-gameflow-logique", "Vues Game Flow annoté et Logique", "D", "V", ["S40.3", "S40.4", "S40.7"],
  ["Onglet `ui/vues/game_flow/` : arbre des blocs déclarés (lus par le chargeur v2 de S40.7), occurrences, statut écrit en toutes lettres (« incomplet », « actif »…) avec une icône ; onglet `ui/vues/logique/` : décisions et états d'une instance.",
   "Chaque onglet s'ajoute par son dossier et son `vue.gd` (convention de S39.12) ; captures sous écran virtuel sur une session de fixture."],
  ["addons/godot_dev_mapper/ui/vues/game_flow/", "addons/godot_dev_mapper/ui/vues/logique/", "rapports/S40.5/"],
  ["Écrire les deux vues.", "Écrire leurs `vue.gd` : les onglets apparaissent sans autre fichier modifié.", "Captures par `capture_onglet.sh`."],
  [("S40.5-a", "\"$B\" --headless --editor --path . --quit-after 120 2>&1 | grep -cE \"SCRIPT ERROR|ERROR:\"", "0"),
   ("S40.5-b", "for o in game_flow logique; do GODOT=\"$B\" tools/harness/editor_driver/capture_onglet.sh $o rapports/S40.5/$o.png || exit 1; done; ls rapports/S40.5/*.png | wc -l", "2")],
  ["(CE) Retirer le libellé texte du statut : le vérificateur constate sur la capture que l'état ne se lit qu'à la couleur ; annuler."],
  "Plan §7 (états jamais portés par la seule couleur) ; module ui.",
  contexte=["docs/contracts/C-11.md"])

t("S40.6", "blocs-banc", "Blocs déclarés dans le banc d'essai", "V", "D", ["S40.2", "S40.3", "S40.7"],
  ["Sur `banc/<nom>-instrumentation` (rebasée sur la branche distante avant de pousser, jamais --force) : déclarer trois à cinq blocs (par exemple entrée dans une pièce jusqu'à la fin du combat) dans `benches/<nom>/flow.json` v2 et dans le code ; mesurer le temps passé par bloc déclaré.",
   "Test d'intégration : une partie interrompue au milieu d'un bloc donne « incomplet »."],
  ["benches/<nom>/flow.json", "tests/integration/run_blocks_bench.sh", "docs/benches/<nom>.md (section « Blocs »)", "branche banc/<nom>-instrumentation (hors de main)"],
  ["Choisir et déclarer les blocs dans le banc ; pousser la branche.", "Mettre à jour flow.json.", "Écrire `run_blocks_bench.sh`.", "Noter le coût de déclaration."],
  [("S40.6-a", "GODOT=\"$B\" tests/integration/run_blocks_bench.sh; echo $?", "0 ; un bloc « incomplet » après interruption"),
   ("S40.6-b", "python3 tools/check_probe_keys.py; echo $?", "0, aucune clé orpheline")],
  ["(CE) Retirer un block_end du banc : le bloc correspondant passe « incomplet » dans S40.6-a ; annuler."],
  "C-11 ; P7 (coût de déclaration mesuré).",
  contexte=["docs/benches/<nom>.md", "benches/<nom>/flow.json"],
  recette=["Coût de déclaration des blocs, jugé par toi."])

t("S40.7", "chargeur-flow-v2", "Chargeur du graphe déclaré .flow.json en version 2", "D", "V", ["S40.1"],
  ["Le chargeur de `core/` (C-05, écrit par S17 en v1) lit la version 2 : définitions de blocs temporels, parent, clés de bloc uniques ; la version 1 reste lisible ; une version inconnue est rejetée avec son code.",
   "Activer `test_c05_flow_v2`."],
  ["addons/godot_dev_mapper/core/", "tests/unit/test_flow_loader_v2.gd", "tests/pending/test_c05_flow_v2.pending (suppression)"],
  ["Supprimer le marqueur ; coller l'échec.", "Écrire les tests (v1, v2 avec blocs imbriqués, clé dupliquée, version inconnue) ; les voir échouer.", "Étendre le chargeur."],
  [("S40.7-a",) + tests("test_flow_loader_v2", "test_c05_flow_v2"), ("S40.7-b",) + DEPS,
   ("S40.7-c", f"{RUN} | grep GDM_TESTS", "failed=0 ; les tests v1 du chargeur (S17) passent toujours")],
  ["(CE) Accepter deux blocs de même clé : le test de clé dupliquée échoue ; annuler.",
   "(CE) Refuser la version 1 : un test de S17 échoue ; annuler."],
  "C-05 v2, C-11 ; compatibilité ascendante (P6, formats persistés).",
  contexte=["docs/CONTRACTS.md (C-05)", "docs/contracts/C-11.md"])


# =====================================================================================================
# MVP — P8 Compatibilité MVP et stabilisation, CAP-13 (revue S41)
# =====================================================================================================

t("S41.1", "matrice-compat", "Matrice de compatibilité générée par la CI", "D", "C", ["S41"],
  ["`tools/ci/compat_matrix.py` : exécute ou collecte la suite de tests pour chaque version de `compat/versions.json`, puis écrit `compat/matrix.json` et le bloc généré de `docs/COMPATIBILITY.md` (version, résultat, date, niveau de support).",
   "Le workflow CI régénère la matrice et la publie comme artefact."],
  ["tools/ci/compat_matrix.py", "addons/godot_dev_mapper/compat/matrix.json", "docs/COMPATIBILITY.md (bloc généré)", ".github/workflows/ci.yml"],
  ["Écrire le script et ses tests sur des résultats simulés.", "Générer la matrice en local pour 4.7.2 et la préversion.", "Mettre à jour le workflow."],
  [("S41.1-a", "python3 tools/ci/compat_matrix.py --godot-stable \"$B\" --sortie /tmp/matrice.json; echo $?", "0, une ligne par version"),
   ("S41.1-b", "python3 tools/ci/compat_matrix.py --verifier docs/COMPATIBILITY.md; echo $?", "0 : le bloc généré correspond à matrix.json")],
  ["(CE) Modifier à la main une ligne du bloc généré : S41.1-b sort en 1 ; annuler."],
  "CAP-13 ; versions seulement dans versions.json (T03).",
  contexte=["docs/COMPATIBILITY.md", "addons/godot_dev_mapper/compat/versions.json"])

t("S41.2", "bascule-48", "Bascule vers Godot 4.8 stable", "C", "V", ["S41.1", "S41.3"],
  ["Si Godot 4.8 stable est publiée : l'ajouter à `versions.json` comme version bloquante, relancer toute la suite, corriger chaque rupture dans la frontière de compatibilité seulement, un test de compatibilité par rupture.",
   "Si elle n'est pas publiée : le constater (lien des publications officielles), écrire « en attente » dans le rapport, et la porte du MVP le note pour la recette sans bloquer."],
  ["addons/godot_dev_mapper/compat/", "tests/unit/test_compat_*.gd", "docs/COMPATIBILITY.md", ".github/workflows/ci.yml (job stable par version de versions.json)", "tools/ci/fetch_godot.sh (si le format de version change)"],
  ["Vérifier les publications officielles de Godot.", "Si 4.8 stable existe : la télécharger par fetch_godot.sh, l'ajouter à versions.json et à la CI comme version bloquante (4.7.2 le reste), et lancer la suite.", "Corriger chaque rupture dans compat/, avec son test.", "Écrire le résultat."],
  [("S41.2-a", "python3 -c \"import json; print(json.load(open('addons/godot_dev_mapper/compat/versions.json')))\"", "4.8 stable listée si elle est publiée ; sinon « en attente » écrit dans le rapport"),
   ("S41.2-b",) + DEPS],
  ["(CE) Corriger une rupture hors de compat/ : check_deps.py signale l'API sensible ; annuler."],
  "INV-09 ; plan §4 (adaptateurs seulement si rupture constatée).",
  contexte=["docs/COMPATIBILITY.md", "docs/spikes/SPIKE-02.md"],
  recette=["Si 4.8 stable n'était pas sortie : bascule à faire après sa sortie."])

t("S41.3", "tri-preversion", "Tri des échecs de la préversion", "D", "C", ["S41"],
  ["Lancer toute la suite sur la dernière préversion de 4.8 ; classer chaque échec (changement d'API, bug de la préversion, test fragile) ; un changement d'API devient un test de compatibilité et une correction dans compat/.",
   "Écrire `docs/compat/tri-P8.md`."],
  ["docs/compat/tri-P8.md", "addons/godot_dev_mapper/compat/*.gd (adaptateurs ; ni versions.json ni matrix.json)", "tests/unit/test_compat_*.gd"],
  ["Lancer la suite sur la préversion inscrite dans versions.json, et sur la dernière préversion publiée si elle est plus récente (le noter).", "Classer chaque échec.", "Corriger ou documenter."],
  [("S41.3-a", PREVIEW, "résultat de la préversion ; chaque échec restant est expliqué dans tri-P8.md"),
   ("S41.3-b",) + DEPS],
  ["(CE) Le vérificateur relance un échec classé « bug de la préversion » et confirme sa cause par le changelog ou un script de trois lignes."],
  "INV-09 ; CI non bloquante sur la préversion (D-07).",
  contexte=["docs/COMPATIBILITY.md"])

t("S41.4", "desinstallation-instrumentation", "Outil de désinstallation de l'instrumentation", "D", "V", ["S41"],
  ["`tools/uninstall_instrumentation.gd` : liste les appels FlowTrace d'un projet (fichier et ligne) ; refuse de retirer `addons/godot_dev_mapper_runtime/` s'il en reste ; option d'essai à blanc.",
   "Tests sur un projet de fixture avec et sans appels."],
  ["tools/uninstall_instrumentation.gd", "tests/integration/run_uninstall.sh", "tests/fixtures/projet_instrumente/"],
  ["Écrire la fixture.", "Écrire `run_uninstall.sh` ; le voir échouer.", "Écrire l'outil."],
  [("S41.4-a", "GODOT=\"$B\" tests/integration/run_uninstall.sh; echo $?", "0 : appels listés, retrait refusé, puis accepté une fois les appels retirés")],
  ["(CE) Retirer le dossier runtime malgré des appels restants : run_uninstall.sh échoue ; annuler."],
  "Plan §8 (désinstaller l'instrumentation) ; P8.",
  contexte=["docs/plan-directeur.md §8"])

t("S41.5", "installation-propre", "Installation et désinstallation propres du plugin", "V", "D", ["S41.4"],
  ["`tests/integration/run_install.sh` : copie neuve du banc d'essai, ajout du plugin, activation, ouverture de l'éditeur, désactivation, retrait ; aucun résidu (fichiers, clés de project.godot, réglages de l'éditeur) d'après un diff avant et après.",
   "Premier jet de `docs/utilisateur/installation.md`."],
  ["tests/integration/run_install.sh", "docs/utilisateur/installation.md", "tools/ci/checks.d/80-install.sh"],
  ["Écrire le script et son diff.", "Écrire la documentation d'installation.", "Écrire `80-install.sh`."],
  [("S41.5-a", "GODOT=\"$B\" tests/integration/run_install.sh; echo $?", "0, diff vide après désinstallation")],
  ["(CE) Laisser une clé de réglage du plugin dans project.godot : le diff n'est plus vide et S41.5-a échoue ; annuler."],
  "Porte du MVP (installation et désinstallation propres).",
  contexte=["docs/plan-directeur.md §8"],
  recette=["Installation à froid sur ta machine, en suivant docs/utilisateur/installation.md."])

t("S41.6", "mesures-mvp", "Mesures du MVP et dette", "C", "V", ["S41.1", "S41.3"],
  ["Mesurer les objectifs du plan §8 sur le MVP : indexation de 300 scripts, éléments visibles, surcoût de capture, délai réception → affichage ; écrire `docs/mesures/mvp.md` (rendu logiciel marqué).",
   "Lister la dette constatée et, pour chaque dépassement, la correction proposée ou l'acceptation motivée."],
  ["docs/mesures/mvp.md"],
  ["Relancer chaque mesure avec sa commande.", "Comparer aux objectifs.", "Écrire la dette et les propositions."],
  [("S41.6-a", "grep -cE \"objectif\" docs/mesures/mvp.md", "au moins 4"),
   ("S41.6-b", "grep -c \"rendu logiciel\" docs/mesures/mvp.md", "au moins 1")],
  ["(CE) Le vérificateur relance une mesure au hasard : même ordre de grandeur."],
  "Plan §8 ; critère d'arrêt : dépassement de 50 % d'un budget.",
  contexte=["docs/plan-directeur.md §8", "docs/mesures/"])

t("S41.7", "demo-mvp", "Démonstration du MVP sous écran virtuel", "D", "V", ["S41.5"],
  ["`tests/integration/run_demo_mvp.sh` : sur le banc d'essai, inventaire, recherche, appelants, ouverture du code, session enregistrée rechargée, Game Flow annoté ; captures dans `rapports/S41.7/`."],
  ["tests/integration/run_demo_mvp.sh", "tools/harness/editor_driver/ (scénario MVP)", "rapports/S41.7/"],
  ["Écrire le scénario.", "Produire les captures.", "Décrire chaque capture dans le rapport."],
  [("S41.7-a", "GODOT=\"$B\" tests/integration/run_demo_mvp.sh; echo $?", "0"), ("S41.7-b", "ls rapports/S41.7/*.png | wc -l", "au moins 5")],
  ["(CE) Empêcher le rechargement de la session : S41.7-a échoue sur l'étape correspondante ; annuler."],
  "Porte du MVP du plan §9.",
  contexte=["docs/construction/mvp.md, Porte du MVP"],
  recette=["Démonstration du MVP sur ta machine, avec GPU."])


# =====================================================================================================
# V1 — P9 Timeline du Game Flow, CAP-12 complet (revue S42)
# =====================================================================================================

t("S42.1", "contrat-c12-timeline", "Contrat C-12 : timeline et corrélation à travers await", "C", "V", ["S42"],
  ["Écrire `docs/contracts/C-12.md` : intervalles d'occurrences de blocs par instance (couloirs), niveaux d'imbrication, interruptions, regroupement par niveau, zoom sémantique ; l'ordre n'est garanti que par producteur ; aucune arête causale.",
   "Ouvrir la version 3 de C-07 dans `docs/CONTRACTS.md` : l'identifiant d'invocation renvoyé par `enter` peut être passé explicitement à travers un `await` ; les règles et la compatibilité sont écrites. S44.1 puis S47.1 complètent cette même version 3, dans cet ordre.",
   "Fixtures dans `tests/contract/fixtures/<kind>/` et tests de contrat avec marqueurs."],
  ["docs/contracts/C-12.md", "docs/CONTRACTS.md (C-07 v3 ; index : lien vers C-12)", "contracts/", "tests/contract/fixtures/", "tests/contract/test_c12_timeline.gd", "tests/contract/test_c07_await.gd", "tests/pending/"] + OUTILS_CONTRAT,
  ["Relire C-07, C-11 et le plan §6 (V1 : corrélation à travers await).", "Rédiger C-12.", "Rédiger C-07 v3, avec l'analyse d'impact.", "Écrire fixtures et tests de contrat, marqueurs au nom de S42.3 (timeline) et S42.6 (await)."],
  [("S42.1-a", "python3 tools/check_contracts.py C-07 C-12; echo $?", "0"), ("S42.1-b", "python3 tools/validate_fixtures.py; echo $?", "0")],
  ["(CE) Ajouter à une fixture une arête « causes » entre deux occurrences proches : la validation la rejette ; annuler."],
  "INV-05 ; plan §6 (limites de preuve, V1).",
  contexte=["docs/CONTRACTS.md (C-07)", "docs/contracts/C-11.md", "docs/plan-directeur.md §6"])

t("S42.2", "fixtures-timeline", "Fixtures d'occurrences entrelacées", "V", "D", ["S42.1"],
  ["`tests/fixtures/timeline/` : sessions d'occurrences entrelacées entre instances, imbriquées, interrompues, touchées par une lacune, et un générateur déterministe de 1 000 occurrences.",
   "Pour chaque fixture, le résultat attendu de la projection, sans aucune relation causale."],
  ["tests/fixtures/timeline/", "tools/gen_timeline_fixture.py"],
  ["Écrire les fixtures à la main.", "Écrire le générateur à graine fixe.", "Écrire les résultats attendus.", "Valider les fixtures contre C-12."],
  [("S42.2-a", "for f in tests/fixtures/timeline/*.json; do python3 tools/validate_fixtures.py --file \"$f\" || exit 1; done; echo $?", "0"),
   ("S42.2-b", "python3 tools/gen_timeline_fixture.py --n 1000 --graine 7 | sha256sum", "même empreinte à chaque exécution")],
  ["(CE) Changer la graine : l'empreinte change ; la remettre."],
  "C-12 ; INV-05.",
  contexte=["docs/contracts/C-12.md"])

t("S42.3", "projection-timeline", "Projection timeline", "D", "V", ["S42.2"],
  ["`projections/timeline_projection.gd` : couloirs par instance, intervalles d'occurrences, interruptions et lacunes marquées, imbrication ; aucune arête causale produite.",
   "Activer `test_c12_timeline`."],
  ["addons/godot_dev_mapper/projections/timeline_projection.gd", "tests/unit/test_timeline_projection.gd", "tests/pending/test_c12_timeline.pending (suppression)"],
  ["Supprimer le marqueur ; coller l'échec.", "Écrire les tests sur les fixtures.", "Écrire la projection."],
  [("S42.3-a",) + tests("test_timeline_projection", "test_c12_timeline"), ("S42.3-b",) + DEPS],
  ["(CE) Relier deux occurrences successives d'instances différentes : le test « aucune arête causale » échoue ; annuler."],
  "C-12 ; INV-05.",
  contexte=["docs/contracts/C-12.md"])

t("S42.4", "zoom-semantique", "Regroupement par niveau et zoom sémantique", "D", "V", ["S42.3"],
  ["Regrouper les occurrences par niveau de bloc et par fenêtre selon le zoom ; 1 000 occurrences projetées en 20 ms au plus (objectif à valider) ; le regroupement montre le nombre d'occurrences et d'interruptions qu'il cache."],
  ["addons/godot_dev_mapper/projections/timeline_projection.gd", "tests/unit/test_timeline_zoom.gd"],
  ["Écrire les tests (comptes cachés, bornes de temps) ; les voir échouer.", "Écrire le regroupement.", "Mesurer sur la fixture de 1 000 occurrences."],
  [("S42.4-a",) + tests("test_timeline_zoom"), ("S42.4-b", f"{RUN} | grep \"timeline_zoom temps\"", "20 ms au plus pour 1 000 occurrences")],
  ["(CE) Cacher une interruption dans un groupe sans la compter : le test des comptes échoue ; annuler."],
  "V1 P9 (amélioration : regroupement avant effets visuels).",
  contexte=["docs/construction/v1.md, P9"])

t("S42.5", "vue-timeline", "Vue timeline", "D", "V", ["S42.4"],
  ["Onglet `ui/vues/timeline/` (timeline_view.gd et .tscn, et son vue.gd selon la convention de S39.12) : couloirs, zoom et défilement, sélection d'une occurrence avec ses preuves, « incomplet » écrit en toutes lettres ; tenue à 1 000 occurrences mesurée sous écran virtuel."],
  ["addons/godot_dev_mapper/ui/vues/timeline/", "rapports/S42.5/"],
  ["Écrire la vue.", "Écrire `vue.gd` : l'onglet apparaît sans autre fichier modifié.", "Mesurer avec `tools/harness/ui_load.gd` à 1 000 occurrences.", "Captures par `capture_onglet.sh`."],
  [("S42.5-a", "xvfb-run -a \"$B\" --path . --rendering-driver opengl3 -s res://tools/harness/ui_load.gd -- timeline_view 1000 2>&1 | grep FRAME_MS", "temps de frame mesuré, rendu logiciel"),
   ("S42.5-b", "GODOT=\"$B\" tools/harness/editor_driver/capture_onglet.sh timeline rapports/S42.5/timeline.png && ls rapports/S42.5/*.png | wc -l", "au moins 2")],
  ["(CE) Tracer une flèche entre deux occurrences voisines : le vérificateur la voit sur la capture et refuse ; annuler."],
  "INV-05 ; plan §7 (états jamais portés par la seule couleur).",
  contexte=["docs/contracts/C-12.md"],
  recette=["Lisibilité de la timeline, sur ta machine."])

t("S42.6", "await-runtime", "Corrélation à travers await, côté jeu et côté éditeur", "D", "C", ["S42.1"],
  ["`FlowTrace` : un identifiant d'invocation passé explicitement après un `await` rattache les événements suivants à la bonne invocation ; sans lui, « corrélation non garantie » reste affiché.",
   "Activer `test_c07_await` ; instrumenter un cas d'`await` dans le banc d'essai."],
  ["addons/godot_dev_mapper_runtime/flow_trace.gd", "addons/godot_dev_mapper/projections/observed_path.gd", "tests/unit/test_flow_trace_await.gd", "tests/pending/test_c07_await.pending (suppression)",
   "benches/<nom>/flow.json (clé de sonde du cas d'await)", "branche banc/<nom>-instrumentation (hors de main ; rebasée sur la branche distante avant de pousser)"],
  ["Supprimer le marqueur ; coller l'échec.", "Écrire les tests ; les voir échouer.", "Côté jeu.", "Côté chemin observé.", "Instrumenter un cas d'`await` dans le banc ; ajouter sa clé à flow.json ; pousser la branche du banc."],
  [("S42.6-a",) + tests("test_flow_trace_await", "test_c07_await"), ("S42.6-b",) + DEPS],
  ["(CE) Rattacher les événements d'après un `await` sans identifiant à l'invocation précédente : le test « non garantie » échoue ; annuler."],
  "C-07 v3 ; plan §6 (V1) ; INV-05.",
  contexte=["docs/CONTRACTS.md (C-07)", "docs/benches/<nom>.md"])

t("S42.7", "essai-timeline", "Essai de la timeline sur le banc d'essai", "V", "D", ["S42.5", "S42.6"],
  ["Sur une session du banc avec blocs entrelacés : afficher la timeline sous écran virtuel ; vérifier qu'aucune fausse causalité n'apparaît et que l'affichage tient à 1 000 occurrences.",
   "`tests/integration/run_timeline.sh` et captures dans `rapports/S42.7/`."],
  ["tests/integration/run_timeline.sh", "tools/harness/editor_driver/ (scénario timeline)", "rapports/S42.7/"],
  ["Enregistrer la session du banc.", "Écrire le scénario et le script.", "Captures et description."],
  [("S42.7-a", "GODOT=\"$B\" tests/integration/run_timeline.sh; echo $?", "0")],
  ["(CE) Rejouer avec une lacune au milieu d'un bloc : la timeline montre « incomplet » ; le vérificateur le constate sur la capture."],
  "Porte de P9 ; INV-05.",
  contexte=["docs/construction/v1.md, P9"])


# =====================================================================================================
# V1 — P10 Instances et comparaison (revue S43)
# =====================================================================================================

t("S43.1", "affirmations-preuves", "Affirmations et preuves : socle commun de la V1", "C", "V", ["S43"],
  ["`projections/claims.gd` : une affirmation affichée est un objet (texte, liste de preuves, portée) ; une affirmation sans preuve ne peut pas être construite.",
   "`tests/unit/claims_audit.gd` : fonction réutilisable qui parcourt la sortie d'une projection et échoue sur toute affirmation sans preuve ; elle servira à P10, P11, P12 et P13."],
  ["addons/godot_dev_mapper/projections/claims.gd", "tests/unit/claims_audit.gd", "tests/unit/test_claims.gd"],
  ["Écrire les tests ; les voir échouer.", "Écrire `claims.gd`.", "Écrire l'audit réutilisable."],
  [("S43.1-a",) + tests("test_claims"), ("S43.1-b",) + DEPS],
  ["(CE) Construire une affirmation sans preuve : le test échoue ; annuler."],
  "Règle de v1.md (chaque affirmation renvoie à une preuve) ; INV-03.",
  contexte=["docs/construction/v1.md", "docs/plan-directeur.md §6 (limites de preuve)"])

t("S43.2", "contrat-c13-comparaison", "Contrat C-13 : comparaison d'instances", "C", "V", ["S43"],
  ["Écrire `docs/contracts/C-13.md` : requête (définition, deux instances, fenêtre de chacune), alignement explicite des fenêtres, résultat (branches prises, états, fréquences), chaque différence avec ses preuves, et les métadonnées obligatoires : révision, configuration, scénario, fenêtre, couverture.",
   "Fenêtres inégales : signalées avant tout affichage. Fixtures et tests de contrat avec marqueurs."],
  ["docs/contracts/C-13.md", "docs/CONTRACTS.md (index : lien vers C-13)", "contracts/", "tests/contract/fixtures/", "tests/contract/test_c13_compare.gd", "tests/pending/test_c13_compare.pending"] + OUTILS_CONTRAT,
  ["Rédiger C-13.", "Écrire fixtures (deux ennemis, fenêtres égales et inégales).", "Écrire le test de contrat et son marqueur (S43.4)."],
  [("S43.2-a", "python3 tools/check_contracts.py C-13; echo $?", "0"), ("S43.2-b", "python3 tools/validate_fixtures.py; echo $?", "0")],
  ["(CE) Retirer la couverture d'une fixture valide : la validation la rejette ; annuler."],
  "INV-02 ; plan §6 (toute comparaison cite révision, configuration, scénario, fenêtre, couverture).",
  contexte=["docs/CONTRACTS.md (C-01, C-06)"])

t("S43.3", "couverture", "Couverture et fenêtres d'observation", "D", "V", ["S43.2"],
  ["`projections/coverage.gd` : pour une instance et une fenêtre, sondes posées, pertes, lacunes, début et fin ; réutilisé par la comparaison, l'attendu contre observé et l'export."],
  ["addons/godot_dev_mapper/projections/coverage.gd", "tests/unit/test_coverage.gd"],
  ["Écrire les tests ; les voir échouer.", "Écrire la projection."],
  [("S43.3-a",) + tests("test_coverage"), ("S43.3-b",) + DEPS],
  ["(CE) Ignorer une lacune dans le calcul : le test échoue ; annuler."],
  "INV-04, INV-07.",
  contexte=["docs/CONTRACTS.md (C-06)", "docs/contracts/C-13.md"])

t("S43.4", "projection-comparaison", "Projection de comparaison d'instances", "D", "V", ["S43.1", "S43.3"],
  ["`projections/instance_compare.gd` : différences de branches, d'états et de fréquences entre deux instances d'une même définition, chacune en affirmation avec ses preuves ; fenêtres inégales signalées ; activer `test_c13_compare`.",
   "L'audit des affirmations passe sur toutes les fixtures."],
  ["addons/godot_dev_mapper/projections/instance_compare.gd", "tests/unit/test_instance_compare.gd", "tests/pending/test_c13_compare.pending (suppression)"],
  ["Supprimer le marqueur ; coller l'échec.", "Écrire les tests, audit des affirmations compris.", "Écrire la projection."],
  [("S43.4-a",) + tests("test_instance_compare", "test_c13_compare"), ("S43.4-b",) + DEPS],
  ["(CE) Comparer deux fenêtres différentes sans le signaler : le test échoue (contre-épreuve de la porte de P10) ; annuler."],
  "C-13 ; INV-02 ; règle des affirmations de v1.md.",
  contexte=["docs/contracts/C-13.md"])

t("S43.5", "vue-comparaison", "Vue de comparaison", "D", "V", ["S43.4"],
  ["Onglet `ui/vues/comparaison/` (compare_view.gd et .tscn, et son vue.gd selon la convention de S39.12) : deux colonnes, différences en tête, chaque différence ouvre ses preuves, métadonnées toujours visibles ; jamais la couleur seule."],
  ["addons/godot_dev_mapper/ui/vues/comparaison/", "rapports/S43.5/"],
  ["Écrire la vue.", "Écrire `vue.gd` : l'onglet apparaît sans autre fichier modifié.", "Captures par `capture_onglet.sh`."],
  [("S43.5-a", "\"$B\" --headless --editor --path . --quit-after 120 2>&1 | grep -cE \"SCRIPT ERROR|ERROR:\"", "0"),
   ("S43.5-b", "GODOT=\"$B\" tools/harness/editor_driver/capture_onglet.sh comparaison rapports/S43.5/comparaison.png && ls rapports/S43.5/*.png | wc -l", "au moins 1")],
  ["(CE) Masquer les métadonnées : le vérificateur le constate sur la capture et refuse ; annuler."],
  "C-13 ; plan §7.",
  contexte=["docs/contracts/C-13.md"])

t("S43.6", "comparaison-banc", "Deux ennemis du banc d'essai comparés", "V", "D", ["S43.4"],
  ["Sur `banc/<nom>-instrumentation` (rebasée sur la branche distante avant de pousser) : un scénario où deux ennemis d'un même type prennent des branches différentes ; session enregistrée en fixture ; `tests/integration/run_compare_bench.sh` montre la différence de branche avec ses preuves."],
  ["tests/integration/run_compare_bench.sh", "tests/fixtures/sessions_reelles/", "branche banc/<nom>-instrumentation (hors de main)"],
  ["Écrire le scénario dans le banc ; pousser la branche.", "Enregistrer la session.", "Écrire le test d'intégration."],
  [("S43.6-a", "GODOT=\"$B\" tests/integration/run_compare_bench.sh; echo $?", "0, une différence de branche avec preuves")],
  ["(CE) Rejouer avec une fenêtre plus courte pour l'une des instances : l'alerte de fenêtre apparaît."],
  "Porte de P10.",
  contexte=["docs/benches/<nom>.md"])


# =====================================================================================================
# V1 — P11 Data Flow, CAP-14 (revue S44)
# =====================================================================================================

t("S44.1", "contrat-c14-parametres", "Contrat C-14 : origine et usages d'un paramètre", "C", "V", ["S44", "S42.1"],
  ["Écrire `docs/contracts/C-14.md` : définition de paramètre, quatre sources distinguées (défaut du script, ressource, surcharge dans une scène, valeur observée), lecteurs et écrivains (extraits ou observés), « dernière écriture connue » bornée par la fenêtre et marquée comme telle, provenance sur chaque maillon.",
   "Compléter la version 3 de C-04 et C-07, ouverte par S42.1, d'un événement d'écriture observée (clé, valeur primitive, instance) ; fixtures et tests de contrat avec marqueurs."],
  ["docs/contracts/C-14.md", "docs/CONTRACTS.md (C-04 et C-07 v3 ; index : lien vers C-14)", "contracts/", "tests/contract/fixtures/", "tests/contract/test_c14_parametres.gd", "tests/pending/"] + OUTILS_CONTRAT,
  ["Rédiger C-14.", "Étendre C-04 et C-07, avec l'analyse d'impact.", "Écrire fixtures et tests de contrat, marqueurs au nom des tâches de P11."],
  [("S44.1-a", "python3 tools/check_contracts.py C-04 C-07 C-14; echo $?", "0"), ("S44.1-b", "python3 tools/validate_fixtures.py; echo $?", "0")],
  ["(CE) Écrire « valeur certaine » dans une fixture valide : la validation la rejette ; annuler."],
  "INV-03 ; plan §3 (CAP-14) et §7 (J4).",
  contexte=["docs/CONTRACTS.md (C-04, C-07)", "docs/contracts/C-08.md", "docs/plan-directeur.md §3 et §7"])

t("S44.2", "declarations-parametres", "Déclarations de paramètres et valeurs par défaut", "D", "V", ["S44.1"],
  ["`acquisition/param_extractor.gd` : variables exportées, constantes et variables membres, avec type, valeur par défaut lue dans le source et ancrage."],
  ["addons/godot_dev_mapper/acquisition/param_extractor.gd", "tests/unit/test_param_extractor.gd", "tests/fixtures/parametres/"],
  ["Écrire les fixtures et les tests ; les voir échouer.", "Écrire l'extracteur."],
  [("S44.2-a",) + tests("test_param_extractor"), ("S44.2-b",) + DEPS],
  ["(CE) Prendre la valeur d'une expression calculée pour un défaut certain : le test « défaut non littéral » échoue ; annuler."],
  "C-14 ; C-02 (ancrages).",
  contexte=["docs/contracts/C-14.md"])

t("S44.3", "valeurs-ressources", "Valeurs des ressources .tres et .res", "D", "C", ["S44.1"],
  ["Lire les valeurs de propriétés des ressources par la façade d'introspection, sans instancier de scène ; relier chaque valeur au paramètre qu'elle alimente."],
  ["addons/godot_dev_mapper/acquisition/resource_values.gd", "addons/godot_dev_mapper/compat/introspection_facade.gd (lecture de ressource)", "tools/deps_rules.json (API de lecture de ressource)", "tests/unit/test_resource_values.gd"],
  ["Vérifier les API de lecture sur 4.7.2 et la préversion.", "Ajouter ces API à la liste des API sensibles de `tools/deps_rules.json`.", "Écrire les tests ; les voir échouer.", "Écrire la lecture."],
  [("S44.3-a",) + tests("test_resource_values"), ("S44.3-b",) + DEPS],
  ["(CE) Lire la ressource hors de la façade : check_deps.py signale l'API sensible ; annuler."],
  "INV-09 ; C-14.",
  contexte=["docs/CONTRACTS.md (C-03)", "docs/contracts/C-14.md"])

t("S44.4", "surcharges-scenes", "Surcharges de paramètres dans les scènes", "D", "V", ["S44.1"],
  ["Lire, dans l'état des scènes empaquetées, les propriétés surchargées par nœud ; relier chaque surcharge au paramètre et au nœud."],
  ["addons/godot_dev_mapper/acquisition/scene_overrides.gd", "tests/unit/test_scene_overrides.gd"],
  ["Écrire les tests (surcharge présente, retirée, scène héritée) ; les voir échouer.", "Écrire la lecture."],
  [("S44.4-a",) + tests("test_scene_overrides"), ("S44.4-b",) + DEPS],
  ["(CE) Retirer une surcharge de la fixture : l'origine calculée change, sinon le test échoue (contre-épreuve de la porte de P11)."],
  "C-14 ; CAP-14 (override distingué).",
  contexte=["docs/contracts/C-14.md"])

t("S44.5", "lecteurs-ecrivains", "Lecteurs et écrivains statiques d'un paramètre", "D", "V", ["S44.2"],
  ["Étendre l'extraction : lectures et écritures des variables membres (self.x, x =, obj.x sur receveur typé) ; receveur non typé : « non résolu »."],
  ["addons/godot_dev_mapper/acquisition/def_use.gd", "tests/unit/test_def_use.gd"],
  ["Écrire les tests ; les voir échouer.", "Écrire l'extraction."],
  [("S44.5-a",) + tests("test_def_use"), ("S44.5-b",) + DEPS],
  ["(CE) Attribuer une écriture sur receveur non typé : le test « non résolu » échoue ; annuler."],
  "C-14 ; CAP-09 (non résolu jamais deviné).",
  contexte=["docs/contracts/C-08.md", "docs/contracts/C-14.md"])

t("S44.6", "valeur-observee", "Valeur observée : écritures instrumentées", "D", "C", ["S44.1", "S42.6"],
  ["`FlowTrace` : écriture observée d'un paramètre (clé littérale, valeur primitive, instance) ; chemin désactivé au coût mesuré ; réception et rangement côté éditeur."],
  ["addons/godot_dev_mapper_runtime/flow_trace.gd", "addons/godot_dev_mapper_runtime/envelope.gd", "addons/godot_dev_mapper/protocol/envelope_codec.gd", "tests/unit/test_flow_trace_values.gd", "tests/pending/"],
  ["Supprimer les marqueurs concernés ; coller l'échec.", "Côté jeu.", "Codec.", "Mesure du chemin désactivé."],
  [("S44.6-a",) + tests("test_flow_trace_values", "test_c04"), ("S44.6-b",) + DEPS],
  ["(CE) Accepter une valeur non primitive : le test de validation échoue ; annuler."],
  "C-04, C-07, C-14 ; INV-06.",
  contexte=["docs/CONTRACTS.md (C-04, C-07)", "docs/contracts/C-14.md"])

t("S44.7", "projection-origine", "Projection de l'origine d'un paramètre", "D", "V", ["S44.3", "S44.4", "S44.5", "S44.6"],
  ["`projections/param_origin.gd` : chaîne défaut → ressource → surcharge de scène → valeur observée, avec lecteurs, écrivains et portée ; « dernière écriture connue » bornée ; chaque maillon en affirmation avec preuve, audit compris."],
  ["addons/godot_dev_mapper/projections/param_origin.gd", "tests/unit/test_param_origin.gd", "tests/pending/test_c14_parametres.pending (suppression)"],
  ["Supprimer le marqueur ; coller l'échec.", "Écrire les tests, audit des affirmations compris.", "Écrire la projection."],
  [("S44.7-a",) + tests("test_param_origin", "test_c14_parametres"), ("S44.7-b",) + DEPS],
  ["(CE) Afficher une valeur observée hors de la fenêtre comme actuelle : le test de borne échoue ; annuler."],
  "C-14 ; INV-03 ; règle des affirmations de v1.md.",
  contexte=["docs/contracts/C-14.md"])

t("S44.8", "vue-data-flow", "Vue Data Flow (parcours J4)", "D", "V", ["S44.7"],
  ["Onglet `ui/vues/data_flow/` (data_flow_view.gd et .tscn, et son vue.gd selon la convention de S39.12) : choisir un paramètre ; voir les quatre sources, les lecteurs et les écrivains, la portée ; ouvrir le code de chaque maillon."],
  ["addons/godot_dev_mapper/ui/vues/data_flow/", "rapports/S44.8/"],
  ["Écrire la vue.", "Écrire `vue.gd` : l'onglet apparaît sans autre fichier modifié.", "Captures par `capture_onglet.sh`."],
  [("S44.8-a", "\"$B\" --headless --editor --path . --quit-after 120 2>&1 | grep -cE \"SCRIPT ERROR|ERROR:\"", "0"),
   ("S44.8-b", "GODOT=\"$B\" tools/harness/editor_driver/capture_onglet.sh data_flow rapports/S44.8/data_flow.png && ls rapports/S44.8/*.png | wc -l", "au moins 1")],
  ["(CE) Fusionner surcharge et défaut en une seule ligne : le vérificateur le constate et refuse ; annuler."],
  "Plan §7 (J4) ; C-14.",
  contexte=["docs/contracts/C-14.md"])

t("S44.9", "parametre-banc", "Paramètre du banc d'essai suivi de bout en bout", "V", "D", ["S44.7"],
  ["Sur le banc : un paramètre (par exemple la cadence d'attaque) suivi de sa déclaration à sa valeur observée ; écriture instrumentée ajoutée à `banc/<nom>-instrumentation` (rebasée sur la branche distante avant de pousser) ; `tests/integration/run_param_bench.sh`."],
  ["tests/integration/run_param_bench.sh", "benches/<nom>/flow.json", "branche banc/<nom>-instrumentation (hors de main)"],
  ["Instrumenter l'écriture dans le banc ; pousser la branche.", "Écrire le test d'intégration.", "Vérifier les quatre sources distinguées."],
  [("S44.9-a", "GODOT=\"$B\" tests/integration/run_param_bench.sh; echo $?", "0, quatre sources distinguées")],
  ["(CE) Retirer la surcharge de scène dans la copie du banc : l'origine affichée change, sinon S44.9-a échoue."],
  "Porte de P11.",
  contexte=["docs/benches/<nom>.md"],
  recette=["Parcours J4 (paramètre, origine, lecteurs, portée) sur ta machine."])


# =====================================================================================================
# V1 — P12 Attendu contre observé, CAP-15 (revue S45)
# =====================================================================================================

t("S45.1", "contrat-c15-attentes", "Contrat C-15 : attentes et première divergence", "C", "V", ["S45"],
  ["Écrire `docs/contracts/C-15.md` : format des attentes, versionné avec le projet (suite d'étapes déclarées, ou session de référence avec sa fenêtre et sa couverture), points d'alignement déclarés, résultat (conforme, première divergence connue, indéterminé), jamais « cause ».",
   "Schéma, fixtures et tests de contrat avec marqueurs."],
  ["docs/contracts/C-15.md", "docs/CONTRACTS.md (index : lien vers C-15)", "contracts/schemas/expectations.v1.schema.json", "tests/contract/fixtures/expectations/", "tests/contract/test_c15_*.gd", "tests/pending/"] + OUTILS_CONTRAT,
  ["Rédiger C-15.", "Écrire schéma et fixtures (conforme, divergente, trou → indéterminé).", "Écrire les tests de contrat et leurs marqueurs."],
  [("S45.1-a", "python3 tools/check_contracts.py C-15; echo $?", "0"), ("S45.1-b", "python3 tools/validate_fixtures.py; echo $?", "0 ; fixtures expectations comprises")],
  ["(CE) Ajouter un champ « cause » à une fixture de résultat : la validation la rejette ; annuler."],
  "INV-04, INV-05 ; plan §6 (diagnostic V1).",
  contexte=["docs/CONTRACTS.md (C-06)", "docs/contracts/C-13.md", "docs/plan-directeur.md §6"])

t("S45.2", "persistance-attentes", "Lecture et écriture des attentes", "D", "C", ["S45.1"],
  ["`persistence/expectations.gd` : sauvegarde atomique, validation à l'import, refus d'une version inconnue ; fichier versionné dans le dossier du projet analysé."],
  ["addons/godot_dev_mapper/persistence/expectations.gd", "tests/unit/test_expectations_io.gd"],
  ["Écrire les tests ; les voir échouer.", "Écrire la lecture et l'écriture."],
  [("S45.2-a",) + tests("test_expectations_io"), ("S45.2-b",) + DEPS],
  ["(CE) Accepter une version inconnue : le test échoue ; annuler."],
  "C-15 ; plan §8 (formats versionnés).",
  contexte=["docs/contracts/C-10.md", "docs/contracts/C-15.md"])

t("S45.3", "session-reference", "Session de référence", "D", "V", ["S45.2"],
  ["Marquer une session enregistrée comme référence d'un scénario ; en dériver une attente avec sa fenêtre, sa configuration et sa couverture."],
  ["addons/godot_dev_mapper/projections/reference_session.gd", "tests/unit/test_reference_session.gd"],
  ["Écrire les tests ; les voir échouer.", "Écrire la dérivation."],
  [("S45.3-a",) + tests("test_reference_session"), ("S45.3-b",) + DEPS],
  ["(CE) Dériver une attente sans couverture : le test échoue ; annuler."],
  "C-15 ; INV-04.",
  contexte=["docs/contracts/C-15.md"])

t("S45.4", "alignement", "Alignement des étapes attendues et observées", "D", "V", ["S45.1"],
  ["`projections/step_alignment.gd` : aligne les étapes par clé de sonde et structure d'invocation, puis par les points d'alignement déclarés ; une étape sans correspondance reste « non observée », jamais « non exécutée »."],
  ["addons/godot_dev_mapper/projections/step_alignment.gd", "tests/unit/test_step_alignment.gd"],
  ["Écrire les tests (alignement simple, boucle, point déclaré, étape manquante) ; les voir échouer.", "Écrire l'alignement."],
  [("S45.4-a",) + tests("test_step_alignment"), ("S45.4-b",) + DEPS],
  ["(CE) Aligner par la seule proximité temporelle : le test de boucle échoue ; annuler."],
  "INV-04, INV-05 ; C-15.",
  contexte=["docs/contracts/C-15.md"])

t("S45.5", "premiere-divergence", "Première divergence connue", "D", "V", ["S45.3", "S45.4"],
  ["`projections/divergence.gd` : première divergence connue avec ses preuves ; une lacune avant elle rend le résultat « indéterminé » ; activer les tests C-15 ; audit des affirmations."],
  ["addons/godot_dev_mapper/projections/divergence.gd", "tests/unit/test_divergence.gd", "tests/pending/test_c15_*.pending (suppression)"],
  ["Supprimer les marqueurs ; coller l'échec.", "Écrire les tests, audit compris.", "Écrire la projection."],
  [("S45.5-a",) + tests("test_divergence", "test_c15"), ("S45.5-b",) + DEPS],
  ["(CE) Ignorer une lacune dans la session fautive : le résultat devrait être « indéterminé » et le test échoue (contre-épreuve de la porte de P12) ; annuler."],
  "C-15 ; INV-04 ; règle des affirmations de v1.md.",
  contexte=["docs/contracts/C-15.md"])

t("S45.6", "vue-attendu", "Vue Attendu contre observé", "D", "V", ["S45.5"],
  ["Onglet `ui/vues/attendu/` (expected_view.gd et .tscn, et son vue.gd selon la convention de S39.12) : attente et session côte à côte, première divergence connue mise en tête avec ses preuves, état « indéterminé » expliqué par les lacunes ; déclaration d'un point d'alignement depuis la vue."],
  ["addons/godot_dev_mapper/ui/vues/attendu/", "rapports/S45.6/"],
  ["Écrire la vue.", "Écrire `vue.gd` : l'onglet apparaît sans autre fichier modifié.", "Captures par `capture_onglet.sh`."],
  [("S45.6-a", "\"$B\" --headless --editor --path . --quit-after 120 2>&1 | grep -cE \"SCRIPT ERROR|ERROR:\"", "0"),
   ("S45.6-b", "GODOT=\"$B\" tools/harness/editor_driver/capture_onglet.sh attendu rapports/S45.6/attendu.png && ls rapports/S45.6/*.png | wc -l", "au moins 2")],
  ["(CE) Libeller la divergence « cause » : le vérificateur refuse ; annuler."],
  "C-15 ; INV-05.",
  contexte=["docs/contracts/C-15.md"])

t("S45.7", "attendu-banc", "Sessions de référence et fautive du banc d'essai", "V", "D", ["S45.5"],
  ["Enregistrer une session de référence du banc et une session fautive (une branche de bug de T19) ; `tests/integration/run_expected_bench.sh` situe la divergence avec ses preuves."],
  ["tests/integration/run_expected_bench.sh", "tests/fixtures/sessions_reelles/", "benches/<nom>/attentes/"],
  ["Enregistrer les deux sessions.", "Écrire l'attente versionnée.", "Écrire le test d'intégration."],
  [("S45.7-a", "GODOT=\"$B\" tests/integration/run_expected_bench.sh; echo $?", "0, divergence située avec preuves")],
  ["(CE) Retirer un lot de la session fautive : le résultat devient « indéterminé »."],
  "Porte de P12.",
  contexte=["docs/benches/<nom>.md", "rapports/S33.md"])


# =====================================================================================================
# V1 — P13 Diagnostic, Explain, Tune, CAP-16 (revue S46)
# =====================================================================================================

t("S46.1", "contrat-c16-explain", "Contrat C-16 : explication, suggestions, points d'intervention", "C", "V", ["S46"],
  ["Écrire `docs/contracts/C-16.md` : explication = phrases, chacune avec ses preuves ; inconnues listées ; vérification suggérée, marquée comme suggestion, avec statut (proposée, acceptée, refusée par l'humain) ; point d'intervention = fichier, fonction, paramètre et portée (définitions et instances touchées).",
   "Aucune intention inventée : une phrase sans preuve est invalide. Fixtures et tests de contrat avec marqueurs."],
  ["docs/contracts/C-16.md", "docs/CONTRACTS.md (index : lien vers C-16)", "contracts/", "tests/contract/fixtures/", "tests/contract/test_c16_*.gd", "tests/pending/"] + OUTILS_CONTRAT,
  ["Rédiger C-16.", "Écrire fixtures (valide, phrase sans preuve, suggestion non marquée).", "Écrire les tests de contrat et leurs marqueurs."],
  [("S46.1-a", "python3 tools/check_contracts.py C-16; echo $?", "0"), ("S46.1-b", "python3 tools/validate_fixtures.py; echo $?", "0")],
  ["(CE) Retirer les preuves d'une phrase dans une fixture valide : la validation la rejette ; annuler."],
  "Plan §3 (CAP-16) et §6 ; règle des affirmations de v1.md.",
  contexte=["docs/contracts/C-13.md", "docs/contracts/C-14.md", "docs/contracts/C-15.md"])

t("S46.2", "points-intervention", "Points d'intervention et portée", "D", "V", ["S46.1"],
  ["`projections/intervention_points.gd` : à partir d'une divergence, d'une décision ou d'un paramètre, les fichiers, fonctions et paramètres où intervenir, avec la portée calculée par les appelants (P5) et les instances (P10)."],
  ["addons/godot_dev_mapper/projections/intervention_points.gd", "tests/unit/test_intervention_points.gd"],
  ["Écrire les tests ; les voir échouer.", "Écrire la projection."],
  [("S46.2-a",) + tests("test_intervention_points"), ("S46.2-b",) + DEPS],
  ["(CE) Omettre les appelants d'une fonction dans la portée : le test échoue ; annuler."],
  "C-16 ; CAP-16 (fichier, fonction, paramètre et portée affichés).",
  contexte=["docs/contracts/C-09.md", "docs/contracts/C-13.md", "docs/contracts/C-16.md"])

t("S46.3", "explications", "Explications fondées sur les preuves", "D", "C", ["S46.1"],
  ["`projections/explain.gd` : phrases construites à partir des faits du modèle (divergence, décisions observées, paramètres, lacunes), chacune avec ses preuves ; inconnues listées ; aucune intention ni cause affirmée ; audit des affirmations sur toutes les fixtures."],
  ["addons/godot_dev_mapper/projections/explain.gd", "tests/unit/test_explain.gd", "tests/pending/test_c16_*.pending (suppression)"],
  ["Supprimer les marqueurs ; coller l'échec.", "Écrire les tests, audit compris.", "Écrire le générateur de phrases."],
  [("S46.3-a",) + tests("test_explain", "test_c16"), ("S46.3-b",) + DEPS],
  ["(CE) Produire une phrase « l'ennemi voulait fuir » : l'audit la rejette (intention inventée) ; annuler."],
  "C-16 ; INV-05.",
  contexte=["docs/contracts/C-16.md"])

t("S46.4", "verifications-suggerees", "Vérifications suggérées", "D", "V", ["S46.1"],
  ["`projections/suggest_checks.gd` : suggestions marquées comme telles (poser une sonde, enregistrer un scénario, comparer deux instances, déclarer un point d'alignement), chacune justifiée par une lacune ou une inconnue précise."],
  ["addons/godot_dev_mapper/projections/suggest_checks.gd", "tests/unit/test_suggest_checks.gd"],
  ["Écrire les tests ; les voir échouer.", "Écrire les suggestions."],
  [("S46.4-a",) + tests("test_suggest_checks"), ("S46.4-b",) + DEPS],
  ["(CE) Produire une suggestion sans justification : le test échoue ; annuler."],
  "C-16 ; P13 (suggestions marquées, validées par l'humain).",
  contexte=["docs/contracts/C-16.md"])

t("S46.5", "annotations", "Annotations et validation humaine", "D", "C", ["S46.1"],
  ["`persistence/annotations.gd` : annotations et suggestions avec auteur, date et statut ; sauvegarde atomique ; une réindexation n'écrase jamais une annotation humaine."],
  ["addons/godot_dev_mapper/persistence/annotations.gd", "tests/unit/test_annotations.gd"],
  ["Écrire les tests (réindexation, renommage de fonction, version inconnue) ; les voir échouer.", "Écrire la persistance."],
  [("S46.5-a",) + tests("test_annotations"), ("S46.5-b",) + DEPS],
  ["(CE) Réindexer en remplaçant les annotations : le test échoue ; annuler."],
  "Plan §5 (annotations jamais écrasées) ; C-16.",
  contexte=["docs/plan-directeur.md §5", "docs/contracts/C-16.md"])

t("S46.6", "vue-explain-tune", "Vue Explain et Tune", "D", "V", ["S46.2", "S46.3", "S46.4", "S46.5"],
  ["Onglet `ui/vues/explain/` (explain_view.gd et .tscn, et son vue.gd selon la convention de S39.12) : explication, chaque phrase avec ses preuves ; vérifications suggérées à accepter ou refuser ; points d'intervention avec portée et ouverture du code."],
  ["addons/godot_dev_mapper/ui/vues/explain/", "rapports/S46.6/"],
  ["Écrire la vue.", "Écrire `vue.gd` : l'onglet apparaît sans autre fichier modifié.", "Captures par `capture_onglet.sh`."],
  [("S46.6-a", "\"$B\" --headless --editor --path . --quit-after 120 2>&1 | grep -cE \"SCRIPT ERROR|ERROR:\"", "0"),
   ("S46.6-b", "GODOT=\"$B\" tools/harness/editor_driver/capture_onglet.sh explain rapports/S46.6/explain.png && ls rapports/S46.6/*.png | wc -l", "au moins 2")],
  ["(CE) Accepter une suggestion sans action humaine : le vérificateur refuse ; annuler."],
  "C-16 ; plan §7.",
  contexte=["docs/contracts/C-16.md"])

t("S46.7", "bugs-v1", "Nouveaux bugs injectés à l'aveugle", "V", "C", ["S46"],
  ["Créer `banc/<nom>-bug-4` à `-bug-6` depuis l'instrumentation la plus récente, un bug par branche, de difficulté comparable, et une enveloppe scellée dans la branche orpheline `banc/<nom>-enveloppe-2` ; seuls les symptômes vont dans `rapports/S46.7.md`.",
   "Règle pour toutes les IA : celle qui réalisera S46.8 ne récupère pas l'enveloppe avant la fin de ses diagnostics."],
  ["rapports/S46.7.md", "branches banc/<nom>-bug-4 à -bug-6 et banc/<nom>-enveloppe-2 (hors de main)"],
  ["Créer chaque branche de bug ; vérifier que son symptôme se reproduit ; pousser.", "Écrire l'enveloppe ; pousser.", "Écrire les symptômes seulement."],
  [("S46.7-a", "git ls-remote origin \"refs/heads/banc/*-bug-[456]\" | wc -l", "3"),
   ("S46.7-b", "grep -cE \"\\.gd:[0-9]+\" rapports/S46.7.md", "0 (aucune cause divulguée)")],
  ["(CE) Ajouter une ligne « fichier.gd:12 » au rapport : S46.7-b donne 1 ; annuler."],
  "Règles des bugs de T19.",
  contexte=["docs/construction/etape-7.md, T19", "rapports/S33.md"])

t("S46.8", "mesure-diagnostic-v1", "Mesure du diagnostic assisté, par substitution", "D", "C", ["S46.6", "S46.7"],
  ["Diagnostiquer les bugs 4 à 6 (et rejouer un bug de T19) : avec le diagnostic assisté (explication, divergence, points d'intervention), puis sans, en alternant ; compter exécutions, lectures, temps, justesse ; ouvrir l'enveloppe seulement après.",
   "Chaque explication fausse ou trompeuse devient un cas de test avec la preuve qui aurait dû l'empêcher.",
   "Écrire `docs/mesures/valeur-v1-substitution.md` (signal pour un agent, pas pour une personne)."],
  ["docs/mesures/valeur-v1-substitution.md", "tests/unit/test_explain_regressions.gd", "tests/fixtures/explain/"],
  ["Diagnostics, dans l'ordre fixé, avec les comptes.", "Ouvrir l'enveloppe ; noter l'heure ; comparer les causes.", "Transformer chaque explication trompeuse en test.", "Écrire la mesure."],
  [("S46.8-a", "grep -c \"pas pour une personne\" docs/mesures/valeur-v1-substitution.md", "1"),
   ("S46.8-b",) + tests("test_explain_regressions")],
  ["(CE) Le vérificateur relit le tableau contre l'enveloppe : concordance des causes."],
  "Porte de P13 (temps jusqu'à la cause réduit ; aucune affirmation sans preuve).",
  contexte=["docs/mesures/valeur-poc-substitution.md", "rapports/S46.7.md"],
  recette=["Mesure humaine du diagnostic assisté, sur de nouveaux bugs."], creneaux=2)


# =====================================================================================================
# V1 — P14 Performance corrélée, CAP-17 (revue S47)
# =====================================================================================================

t("S47.1", "contrat-metric", "Contrat : événement metric et coût de capture", "C", "V", ["S47", "S44.1"],
  ["Compléter la version 3 de C-04 et C-07, après S42.1 et S44.1 : événement metric (moniteur, valeur, frame), configuration de l'échantillonneur (moniteurs, période), événement de coût de capture (temps passé dans FlowTrace par frame) ; corrélation dans le temps jamais présentée comme une cause.",
   "Fixtures et tests de contrat avec marqueurs."],
  ["docs/CONTRACTS.md (C-04 et C-07 v3)", "contracts/", "tests/contract/fixtures/", "tests/contract/test_c04_metric.gd", "tests/pending/"] + OUTILS_CONTRAT,
  ["Rédiger les extensions et l'analyse d'impact.", "Écrire fixtures et tests de contrat, marqueur au nom de S47.2."],
  [("S47.1-a", "python3 tools/check_contracts.py C-04 C-07; echo $?", "0"), ("S47.1-b", "python3 tools/validate_fixtures.py; echo $?", "0")],
  ["(CE) Ajouter « temps CPU par fonction » à une fixture valide : la validation la rejette ; annuler."],
  "Plan §3 (CAP-17 : pas de temps CPU par fonction) ; INV-05.",
  contexte=["docs/CONTRACTS.md (C-04, C-07)"])

t("S47.2", "echantillonneur", "Échantillonneur de moniteurs, côté jeu", "D", "C", ["S47.1", "S44.6", "S44.3"],
  ["Échantillonner les moniteurs de Godot par la façade runtime (API sensible), à une période configurable, et émettre des événements metric ; coût désactivé inchangé.",
   "Activer les tests de contrat de l'événement metric."],
  ["addons/godot_dev_mapper_runtime/flow_trace.gd", "addons/godot_dev_mapper_runtime/runtime_facade.gd", "addons/godot_dev_mapper_runtime/envelope.gd", "addons/godot_dev_mapper/protocol/envelope_codec.gd",
   "tools/deps_rules.json (API des moniteurs)", "tests/unit/test_metric_sampler.gd", "tests/pending/test_c04_metric.pending (suppression)"],
  ["Vérifier l'API des moniteurs sur 4.7.2 et la préversion ; l'ajouter aux API sensibles de `tools/deps_rules.json`.", "Supprimer le marqueur ; coller l'échec.", "Encoder et décoder l'événement metric (enveloppe et codec).", "Écrire l'échantillonneur.", "Mesurer le chemin désactivé."],
  [("S47.2-a",) + tests("test_metric_sampler", "test_c04_metric"), ("S47.2-b",) + DEPS],
  ["(CE) Lire les moniteurs hors de la façade runtime : check_deps.py le signale ; annuler."],
  "INV-06, INV-09 ; C-04, C-07.",
  contexte=["docs/CONTRACTS.md (C-03, C-04, C-07)"])

t("S47.3", "cout-capture", "Coût de capture avec et sans collecte", "D", "V", ["S47.2"],
  ["Mesurer et émettre le coût de capture par frame ; étendre `tools/bench/flow_trace_cost/` pour comparer avec et sans collecte, cinq répétitions ; écrire `docs/mesures/cout-capture-v1.md`."],
  ["addons/godot_dev_mapper_runtime/flow_trace.gd", "tools/bench/flow_trace_cost/", "docs/mesures/cout-capture-v1.md"],
  ["Émettre le coût par frame.", "Étendre le banc de mesure.", "Mesurer et écrire."],
  [("S47.3-a", "GODOT=\"$B\" tools/bench/flow_trace_cost/run.sh | grep -E \"avec|sans\"", "coûts avec et sans collecte"),
   ("S47.3-b", "grep -c \"5 %\" docs/mesures/cout-capture-v1.md", "au moins 1 (budget comparé)")],
  ["(CE) Le vérificateur relance la mesure : même ordre de grandeur."],
  "Plan §8 (surcoût de capture : 5 % au plus).",
  contexte=["docs/spikes/SPIKE-05.md"])

t("S47.4", "projection-perf", "Projection de corrélation performance ↔ événements", "D", "V", ["S47.1"],
  ["`projections/perf_correlation.gd` : courbes de moniteurs et de coût de capture, pics de temps de frame, fenêtre d'événements autour de chaque pic ; libellé « dans la même fenêtre », jamais « à cause de » ; audit des affirmations."],
  ["addons/godot_dev_mapper/projections/perf_correlation.gd", "tests/unit/test_perf_correlation.gd"],
  ["Écrire les tests, audit compris ; les voir échouer.", "Écrire la projection."],
  [("S47.4-a",) + tests("test_perf_correlation"), ("S47.4-b",) + DEPS],
  ["(CE) Libeller un pic « causé par » un événement : l'audit le rejette ; annuler."],
  "INV-05 ; CAP-17.",
  contexte=["docs/CONTRACTS.md (C-04)"])

t("S47.5", "vue-perf", "Vue performance", "D", "V", ["S47.3", "S47.4"],
  ["Onglet `ui/vues/performance/` (perf_view.gd et .tscn, et son vue.gd selon la convention de S39.12) : courbes, coût de capture affiché, pic sélectionné avec sa fenêtre d'événements ; collecte désactivée : la courbe de coût disparaît."],
  ["addons/godot_dev_mapper/ui/vues/performance/", "rapports/S47.5/"],
  ["Écrire la vue.", "Écrire `vue.gd` : l'onglet apparaît sans autre fichier modifié.", "Captures par `capture_onglet.sh`, collecte active puis désactivée."],
  [("S47.5-a", "\"$B\" --headless --editor --path . --quit-after 120 2>&1 | grep -cE \"SCRIPT ERROR|ERROR:\"", "0"),
   ("S47.5-b", "GODOT=\"$B\" tools/harness/editor_driver/capture_onglet.sh performance rapports/S47.5/performance.png && ls rapports/S47.5/*.png | wc -l", "au moins 2")],
  ["(CE) Laisser la courbe de coût collecte désactivée : le vérificateur le constate et refuse (contre-épreuve de la porte de P14) ; annuler."],
  "CAP-17 ; plan §7.",
  contexte=["docs/construction/v1.md, P14"])

t("S47.6", "pic-banc", "Pic de frame corrélé sur le banc d'essai", "V", "D", ["S47.3", "S47.4"],
  ["Sur le banc (`banc/<nom>-instrumentation`, rebasée sur la branche distante avant de pousser) : un scénario qui provoque un pic de temps de frame ; `tests/integration/run_perf_bench.sh` retrouve la fenêtre d'événements du pic."],
  ["tests/integration/run_perf_bench.sh", "branche banc/<nom>-instrumentation (hors de main)"],
  ["Écrire le scénario dans le banc ; pousser la branche.", "Écrire le test d'intégration."],
  [("S47.6-a", "GODOT=\"$B\" tests/integration/run_perf_bench.sh; echo $?", "0, pic et fenêtre d'événements trouvés")],
  ["(CE) Désactiver la collecte : le test constate l'absence de la courbe de coût."],
  "Porte de P14.",
  contexte=["docs/benches/<nom>.md"])


# =====================================================================================================
# V1 — P15 AI Snapshot, CAP-18 (revue S48)
# =====================================================================================================

t("S48.1", "contrat-c17-snapshot", "Contrat C-17 : AI Snapshot", "C", "V", ["S48"],
  ["Écrire `docs/contracts/C-17.md` : JSON d'export (sous-graphe, tranche de trace, lacunes, métadonnées : révision, configuration, scénario, fenêtre, couverture ; liste des champs exclus) et image PNG associée ; export local seulement.",
   "Schéma, fixtures et tests de contrat avec marqueurs."],
  ["docs/contracts/C-17.md", "docs/CONTRACTS.md (index : lien vers C-17)", "contracts/schemas/ai_snapshot.v1.schema.json", "tests/contract/fixtures/ai_snapshot/", "tests/contract/test_c17_snapshot.gd", "tests/pending/test_c17_snapshot.pending"] + OUTILS_CONTRAT,
  ["Rédiger C-17.", "Écrire schéma et fixtures (sans lacunes : invalide).", "Écrire le test de contrat et son marqueur (S48.2)."],
  [("S48.1-a", "python3 tools/check_contracts.py C-17; echo $?", "0"), ("S48.1-b", "python3 tools/validate_fixtures.py; echo $?", "0 ; fixtures ai_snapshot comprises")],
  ["(CE) Retirer les lacunes d'une fixture valide : la validation la rejette ; annuler."],
  "Plan §8 (exports V1) ; CAP-18 ; INV-07.",
  contexte=["docs/plan-directeur.md §8", "docs/CONTRACTS.md (C-06)", "docs/contracts/C-13.md"])

t("S48.2", "export-json", "Export JSON : choix des champs et exclusions", "D", "C", ["S48.1"],
  ["`persistence/ai_snapshot.gd` : choix des champs, exclusion des données sensibles (chemins hors du projet, noms d'utilisateur, valeurs de charge marquées sensibles), lacunes toujours incluses ; validation par le schéma ; écriture locale atomique.",
   "Activer `test_c17_snapshot`."],
  ["addons/godot_dev_mapper/persistence/ai_snapshot.gd", "tests/unit/test_ai_snapshot.gd", "tests/pending/test_c17_snapshot.pending (suppression)"],
  ["Supprimer le marqueur ; coller l'échec.", "Écrire les tests (champ exclu absent partout).", "Écrire l'export."],
  [("S48.2-a",) + tests("test_ai_snapshot", "test_c17_snapshot"), ("S48.2-b",) + DEPS],
  ["(CE) Laisser un champ exclu dans les métadonnées : le test « absent partout » échoue (contre-épreuve de la porte de P15) ; annuler."],
  "C-17 ; export local seulement.",
  contexte=["docs/contracts/C-17.md"])

t("S48.3", "export-png", "Image PNG cohérente avec le JSON", "D", "V", ["S48.2"],
  ["Rendre la vue courante (sous-graphe et trace) en PNG, avec la même sélection que le JSON ; identifiant commun dans les deux fichiers."],
  ["addons/godot_dev_mapper/ui/snapshot_render.gd", "tests/integration/run_snapshot_png.sh"],
  ["Écrire le rendu.", "Écrire le test d'intégration sous écran virtuel."],
  [("S48.3-a", "GODOT=\"$B\" tests/integration/run_snapshot_png.sh; echo $?", "0, PNG et JSON portent le même identifiant")],
  ["(CE) Changer la sélection entre les deux exports : le test d'identifiant commun échoue ; annuler."],
  "C-17 ; CAP-18 (JSON et PNG cohérents).",
  contexte=["docs/contracts/C-17.md"])

t("S48.4", "apercu", "Aperçu avant partage", "D", "V", ["S48.2"],
  ["Onglet `ui/vues/apercu/` (snapshot_preview.gd et .tscn, et son vue.gd selon la convention de S39.12) : montre exactement ce qui sera exporté (champs, exclusions, lacunes) ; l'export ne se fait qu'après confirmation ; aucun envoi réseau."],
  ["addons/godot_dev_mapper/ui/vues/apercu/", "rapports/S48.4/"],
  ["Écrire l'aperçu.", "Écrire `vue.gd` : l'onglet apparaît sans autre fichier modifié.", "Captures par `capture_onglet.sh`."],
  [("S48.4-a", "grep -rnE \"HTTPRequest|HTTPClient|StreamPeerTCP\" addons/godot_dev_mapper/ | wc -l", "0 (aucun envoi réseau)"),
   ("S48.4-b", "GODOT=\"$B\" tools/harness/editor_driver/capture_onglet.sh apercu rapports/S48.4/apercu.png && ls rapports/S48.4/*.png | wc -l", "au moins 1")],
  ["(CE) Exporter sans passer par l'aperçu : le vérificateur le constate et refuse ; annuler."],
  "P15 (aperçu avant partage, export local).",
  contexte=["docs/contracts/C-17.md"])

t("S48.5", "snapshot-essai-ia", "Essai de l'export sur des diagnostics réels", "V", "C", ["S48.3", "S48.4"],
  ["Exporter l'AI Snapshot de deux bugs déjà diagnostiqués (T19 ou P13) ; le donner, dans une conversation neuve, à l'une des trois IA avec la seule question « où est le bug ? » ; noter ce qui lui a manqué.",
   "Écrire `docs/mesures/ai-snapshot.md` : réponses, justesse, champs manquants, champs inutiles."],
  ["docs/mesures/ai-snapshot.md", "rapports/S48.5/ (exports utilisés)"],
  ["Produire les deux exports.", "Mener les deux essais.", "Écrire la mesure et les améliorations proposées."],
  [("S48.5-a", "ls rapports/S48.5/*.json | wc -l", "2"),
   ("S48.5-b", "for f in rapports/S48.5/*.json; do python3 tools/validate_fixtures.py --file \"$f\" || exit 1; done; echo $?", "0")],
  ["(CE) Le vérificateur cherche un champ exclu dans les deux exports : absent."],
  "P15 (amélioration : essai avec une IA).",
  contexte=["docs/mesures/valeur-v1-substitution.md"])


# =====================================================================================================
# V1 — P16 Durcissement et documentation (revue S49)
# =====================================================================================================

t("S49.1", "deux-stables", "Deux versions stables dans la CI", "D", "C", ["S49"],
  ["`compat/versions.json` : 4.7.2 et la dernière 4.8 stable, toutes deux bloquantes ; CI, matrice et `docs/COMPATIBILITY.md` régénérés.",
   "Si 4.8 stable n'est pas sortie : le constater, garder la préversion non bloquante, et le noter pour la recette."],
  ["addons/godot_dev_mapper/compat/versions.json", ".github/workflows/ci.yml", "addons/godot_dev_mapper/compat/matrix.json", "docs/COMPATIBILITY.md"],
  ["Vérifier les publications officielles.", "Mettre à jour versions.json et le workflow.", "Lancer la suite sur les deux versions.", "Régénérer la matrice."],
  [("S49.1-a", "python3 tools/ci/compat_matrix.py --verifier docs/COMPATIBILITY.md; echo $?", "0"),
   ("S49.1-b", "grep -c \"stable\" addons/godot_dev_mapper/compat/matrix.json", "au moins 2, ou « en attente » écrit dans le rapport")],
  ["(CE) Marquer bloquante une version qui échoue : la CI locale échoue ; annuler."],
  "Porte de la V1 (deux versions stables, matrice publiée).",
  contexte=["docs/COMPATIBILITY.md"],
  recette=["Si 4.8 stable n'était pas sortie : rejouer S49.1 après sa sortie."])

t("S49.2", "dette", "Traitement de la dette", "C", "V", ["S49"],
  ["Pour chaque dette de `PROJECT_STATE.md` : la traiter si elle tient dans les fichiers autorisés, sinon l'accepter par écrit avec sa raison et son risque ; écrire `docs/revues/dette-v1.md`.",
   "Une dette qui demande une modification hors des fichiers autorisés devient une unité de correction, demandée par la porte de P16."],
  ["docs/revues/dette-v1.md"],
  ["Lister la dette.", "Classer : traitée, acceptée, à corriger.", "Écrire le document."],
  [("S49.2-a", "grep -cE \"^\\| \" docs/revues/dette-v1.md", "au moins une ligne par dette de PROJECT_STATE.md")],
  ["(CE) Le vérificateur compare la liste à PROJECT_STATE.md : aucune dette oubliée."],
  "P16 (dette traitée ou acceptée par écrit).",
  contexte=["PROJECT_STATE.md"])

t("S49.3", "doc-installation", "Documentation : installation et premiers pas", "V", "D", ["S49"],
  ["`docs/utilisateur/installation.md` et `premiers-pas.md` : prérequis, installation, activation, instrumentation minimale (FlowTrace, flow.json), première session, désinstallation ; chaque commande testée."],
  ["docs/utilisateur/installation.md", "docs/utilisateur/premiers-pas.md", "tools/check_doc_snippets.py"],
  ["Écrire les deux pages.", "Écrire `tools/check_doc_snippets.py` : extrait les blocs de code GDScript et JSON et vérifie qu'ils compilent ou se valident.", "Faire passer le contrôle."],
  [("S49.3-a", "python3 tools/check_doc_snippets.py docs/utilisateur/; echo $?", "0")],
  ["(CE) Introduire une faute dans un extrait GDScript : S49.3-a sort en 1 ; annuler."],
  "Porte de la V1 (documentation testée).",
  contexte=["docs/utilisateur/installation.md (S41.5)"])

t("S49.4", "doc-modes", "Documentation des modes", "V", "D", ["S49.3"],
  ["`docs/utilisateur/modes.md` : Map, Game Flow, Logic, Data Flow, Runtime, Debug, Explain et Tune, Performance, AI Context ; pour chacun : question à laquelle il répond, limites de preuve, capture."],
  ["docs/utilisateur/modes.md", "docs/utilisateur/images/"],
  ["Écrire une section par mode.", "Ajouter les captures des démonstrations.", "Écrire les limites de preuve de chaque mode."],
  [("S49.4-a", "grep -c \"^## \" docs/utilisateur/modes.md", "au moins 9"), ("S49.4-b", "python3 tools/check_doc_snippets.py docs/utilisateur/; echo $?", "0")],
  ["(CE) Le vérificateur cherche « cause » présenté comme un résultat de l'outil : aucune occurrence."],
  "Plan §3 (modes = projections des capacités) ; INV-04, INV-05.",
  contexte=["docs/plan-directeur.md §3"])

t("S49.5", "doc-instrumentation", "Guide d'instrumentation", "V", "D", ["S49.3"],
  ["`docs/utilisateur/instrumentation.md` : règles d'appel de FlowTrace (clés littérales, `if FlowTrace.enabled:`), blocs, paramètres, await, coût, désinstallation ; exemples vérifiés par le contrôle des extraits."],
  ["docs/utilisateur/instrumentation.md"],
  ["Écrire le guide.", "Vérifier chaque exemple."],
  [("S49.5-a", "python3 tools/check_doc_snippets.py docs/utilisateur/; echo $?", "0")],
  ["(CE) Écrire un exemple qui construit une clé par concaténation : le vérificateur le signale comme contraire à C-07 ; annuler."],
  "C-07 (règles d'appel) ; plan §6.",
  contexte=["docs/CONTRACTS.md (C-07)"])

t("S49.6", "installation-froid", "Installation à froid par la documentation seule", "C", "D", ["S49.4", "S49.5", "S49.8", "S49.9"],
  ["Dans un projet Godot vierge et un environnement neuf, suivre la seule documentation, sans lire le code ; noter chaque blocage, chaque commande à deviner, chaque écart.",
   "Corriger la documentation ; ce qui demande du code devient une unité de correction."],
  ["docs/utilisateur/", "docs/mesures/installation-froid.md"],
  ["Préparer l'environnement neuf.", "Suivre la documentation pas à pas.", "Noter et corriger."],
  [("S49.6-a", "grep -cE \"^\\| \" docs/mesures/installation-froid.md", "une ligne par étape suivie"),
   ("S49.6-b", "python3 tools/check_doc_snippets.py docs/utilisateur/; echo $?", "0")],
  ["(CE) Le vérificateur rejoue l'installation dans un autre environnement neuf : même résultat."],
  "Porte de la V1 (installation à froid).",
  contexte=["docs/utilisateur/"],
  recette=["Installation à froid par toi, ou par une personne extérieure, en suivant la documentation."])

t("S49.7", "demos-v1", "Démonstrations de CAP-12 à CAP-18 rejouées", "D", "V", ["S49.1"],
  ["`tests/integration/run_demo_v1.sh` : une démonstration par capacité, de CAP-12 à CAP-18, sur le banc d'essai, sous écran virtuel ; captures dans `rapports/S49.7/` ; chacune décrite dans le rapport."],
  ["tests/integration/run_demo_v1.sh", "tools/harness/editor_driver/ (scénario V1)", "rapports/S49.7/"],
  ["Écrire les scénarios.", "Produire les captures.", "Décrire chaque capture."],
  [("S49.7-a", "GODOT=\"$B\" tests/integration/run_demo_v1.sh; echo $?", "0, sept démonstrations OK"), ("S49.7-b", "ls rapports/S49.7/*.png | wc -l", "au moins 7")],
  ["(CE) Casser une démonstration (par exemple retirer la surcharge de scène) : son étape échoue."],
  "Porte de la V1 (CAP-12 à CAP-18 démontrées).",
  contexte=["docs/construction/v1.md, Porte de la V1"],
  recette=["Démonstrations de la V1 sur ta machine, avec GPU."])

t("S49.8", "desinstallation-v1", "Installation et désinstallation propres de la V1", "V", "D", ["S49.3", "S49.7"],
  ["Rejouer `tests/integration/run_install.sh` avec toutes les fonctions de la V1 utilisées : caches retirés, fichiers versionnés du projet (graphes déclarés, attentes, annotations) conservés et listés, aucun autre résidu."],
  ["tests/integration/run_install.sh", "docs/utilisateur/installation.md (section désinstallation)"],
  ["Étendre le scénario.", "Lancer et comparer.", "Documenter ce qui reste volontairement."],
  [("S49.8-a", "GODOT=\"$B\" tests/integration/run_install.sh --v1; echo $?", "0")],
  ["(CE) Oublier de retirer le cache d'index : le diff le montre et S49.8-a échoue ; annuler."],
  "Plan §8 (cycle de vie) ; porte de la V1.",
  contexte=["docs/plan-directeur.md §8"])

t("S49.9", "mesures-v1", "Mesures finales et limites", "C", "V", ["S49.7"],
  ["Relancer toutes les mesures du plan §8 sur la V1, écrire `docs/mesures/v1.md` (rendu logiciel marqué) et la liste des limites connues, reprise dans la documentation utilisateur."],
  ["docs/mesures/v1.md", "docs/utilisateur/limites.md"],
  ["Relancer chaque mesure.", "Comparer aux objectifs.", "Écrire les limites."],
  [("S49.9-a", "grep -c \"objectif\" docs/mesures/v1.md", "au moins 6")],
  ["(CE) Le vérificateur relance une mesure au hasard : même ordre de grandeur."],
  "Plan §8 ; INV-07.",
  contexte=["docs/mesures/"])

t("S49.10", "dossier-licence", "Dossier de décision : licence et diffusion", "C", "V", ["S49"],
  ["Préparer pour l'humain la décision D-06 : options de licence, compatibilité avec les dépendances et les bancs d'essai, conséquences ; et la décision de diffusion. La tâche ne décide rien : la porte de la V1 déclenche l'arrêt obligatoire n° 3."],
  ["docs/revues/licence-diffusion.md"],
  ["Lister les options et leurs conséquences.", "Vérifier les licences de tout ce qui est embarqué.", "Écrire le dossier."],
  [("S49.10-a", "grep -c \"Option\" docs/revues/licence-diffusion.md", "au moins 2")],
  ["(CE) Le vérificateur cherche une décision prise dans le dossier : aucune."],
  "D-06 ; sequence.md §5 (décision réservée à l'humain).",
  contexte=["docs/DECISIONS.md (D-06)"],
  recette=["Décider la licence (D-06) et la diffusion."])
