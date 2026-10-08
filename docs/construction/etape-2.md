# Étape 2 — Spikes

Tâches : file A : T05 · file B : T06 · Budget : 4 à 6 h humaines · Prérequis : 0.B accepté pour T05, T03 accepté pour T06

## Objectif

Lever les deux dernières inconnues techniques avant d'écrire les contrats :
- la partie éditeur du canal du débogueur (SPIKE-01b), la partie jeu étant établie par SPIKE-01a ;
- la frontière de compatibilité (SPIKE-02) : détection de capacités, isolation de compilation, UID des scripts, inventaire des API sensibles.

## Obligations

- Code jetable, uniquement dans `spikes/`, jamais copié dans `addons/`.
- Chaque affirmation d'un rapport s'appuie sur une exécution ou une mesure, avec la version de Godot, la machine et la date.
- Durée bornée : 3 heures humaines par spike. À l'échéance, on décide avec ce qu'on sait.
- Décision explicite : KEEP, REWRITE ou DISCARD. Si elle change le plan, l'amendement est proposé, puis validé par toi.

## Méthodologie

- Pour chaque question : hypothèse, expérience minimale, mesure, décision.
- T05 reprend le code de SPIKE-01a (`spikes/spike01_debugger/`). Opus le conduit ; toi, tu fais les manipulations dans l'éditeur, car il faut le rendu et l'interface.
- T06 se fait entièrement sans interface, sur 4.7.2 et sur la préversion. Il peut tourner dans un environnement distant, sans ta machine.

## Points de contrôle

| ID | Contrôle | Preuve | Attendu |
| --- | --- | --- | --- |
| PC2.1 | Partie éditeur du canal | Section SPIKE-01b de `docs/spikes/SPIKE-01.md` | Six critères marqués atteint ou non, chacun avec sa preuve |
| PC2.2 | Frontière de compatibilité | `docs/spikes/SPIKE-02.md` | Quatre questions, chacune avec commande et sortie sur les deux versions |
| PC2.3 | Reproductibilité | `spikes/spike02_compat/run.sh`, relancé par le vérificateur | Mêmes conclusions |
| PC2.4 | Décisions consignées | `docs/DECISIONS.md` | KEEP, REWRITE ou DISCARD pour chaque spike |
| PC2.5 | Plan à jour | Diff proposé de `docs/plan-directeur.md` | Validé par toi, ou « aucun changement » justifié |
| PC2.6 | Isolation des spikes | `grep -rn "spikes/" addons` | Aucune ligne |

## Cheminement d'amélioration

- **Débit insuffisant avec rendu (T05).** Lots bornés en octets, par exemple 64 Ko, plutôt qu'en nombre d'événements ; échantillonnage des événements continus ; nouvelle mesure.
- **API d'éditeur différente de l'attendu (T05).** On adapte la passerelle mince côté éditeur ; le contrat ne bouge pas.
- **UID indisponibles ou instables (T06).** Clé de correspondance fondée sur le chemin, avec détection des renommages par suggestion.
- **Isolation de compilation qui échoue (T06).** Tout code propre à une version passe obligatoirement par un script chargé par chemin, sans `class_name`.
- **Spike sans réponse au bout de 3 h.** On consigne ce qui est su et on retient l'option la plus prudente.

## T05 — SPIKE-01b : partie éditeur du canal

Opus et toi · A0 · file A · sur ta machine · vérification : Gemini relit le rapport ; tu rejoues un critère · contexte : `docs/spikes/SPIKE-01.md`, `spikes/spike01_debugger/`, fiche T05 de `docs/orchestration.md`

Fichiers autorisés : `spikes/spike01_debugger/editor/`, `docs/spikes/SPIKE-01.md`. La décision KEEP, REWRITE ou DISCARD est reportée dans `docs/DECISIONS.md` à la fusion.

```text
Tu conduis SPIKE-01b du projet GODOT_DEV_MAPPER : la partie éditeur du canal du débogueur. La partie jeu est établie : lis docs/spikes/SPIKE-01.md et le code de spikes/spike01_debugger/.

CONTRAINTES
- Code jetable dans spikes/spike01_debugger/editor/ uniquement ; rien dans addons/godot_dev_mapper/.
- Vérifie par exécution chaque API d'éditeur avant de t'y fier : EditorDebuggerPlugin et ses méthodes _has_capture, _capture et _setup_session ; EditorDebuggerSession et send_message.

CONSTRUIS un plugin jetable qui :
- enregistre un EditorDebuggerPlugin ;
- reçoit les messages « flowspike:* » envoyés par la classe FlowSpike du jeu ;
- envoie par la session start, stop et un ping de bail toutes les 250 ms ;
- affiche ses compteurs dans la sortie de l'éditeur.

MESURE, avec le rendu actif, les six critères de la fiche T05 :
1. « prêt » reçu par le plugin ;
2. « started » reçu avant tout lot ;
3. arrêt avant la désactivation du plugin : « stopped » reçu en une seconde au plus, et aucun lot ensuite ;
4. coupure (jeu tué, ou plugin retiré sans arrêt) : le bail arrête la collecte côté jeu ; l'éditeur conclut « fin inconnue » ;
5. cinq lancements successifs depuis l'éditeur, sans erreur ;
6. débit et cadence à 1 200 et 10 000 événements par seconde.
Le critère des instances enregistrées avant le démarrage relève du runtime : il est vérifié en T13a, pas ici.
Pour chaque critère : manipulation exacte, observation, chiffre, atteint ou non.

LES MANIPULATIONS À FAIRE À LA MAIN (lancer, arrêter, désactiver le plugin), donne-les-moi une par une et attends mon retour avant de continuer.

À LA FIN
- Complète docs/spikes/SPIKE-01.md, section SPIKE-01b.
- Propose KEEP, REWRITE ou DISCARD.
- Si nécessaire, rédige le changement exact à faire dans docs/plan-directeur.md §6, sans l'appliquer.
```

**Contrôles**

| ID | Contrôle | Attendu |
| --- | --- | --- |
| T05-a | Rapport : six critères, chacun avec manipulation, observation et chiffre | Complet |
| T05-b | Tu rejoues le critère 3 seul, en suivant le rapport | Même observation |
| T05-c | (CE) Tu désactives le plugin sans envoyer l'arrêt | Le jeu arrête seul sa collecte en 2 s au plus ; le rapport le montre |

## T06 — SPIKE-02 : frontière de compatibilité

Opus · A0 · file B · dépend de T03 · sans interface, possible à distance · vérification : Gemini relance `run.sh` · contexte : plan §4 et §5, `docs/ARCHITECTURE.md` (API sensibles)

Fichiers autorisés : `spikes/spike02_compat/`, `docs/spikes/SPIKE-02.md`. Les décisions sont reportées dans `docs/DECISIONS.md` à la fusion.

```text
Tu conduis SPIKE-02 du projet GODOT_DEV_MAPPER. Tu travailles sans interface, sur Godot 4.7.2 et sur la préversion inscrite dans addons/godot_dev_mapper/compat/versions.json ; tools/ci/fetch_godot.sh fournit les deux binaires. Code jetable dans spikes/spike02_compat/ uniquement.

Réponds, preuves à l'appui, à quatre questions.

Q1 DÉTECTION DE CAPACITÉS
Peut-on choisir un chemin de code avec ClassDB.class_exists et ClassDB.class_has_method, sans comparer de numéros de version ?
Trouve une classe ou une méthode présente dans la préversion et absente de 4.7.2. Piste : FuzzySearch, exposée selon les notes de 4.8 dev 1 ; à vérifier.
Montre la détection sur les deux versions.

Q2 ISOLATION DE COMPILATION
Un script qui nomme cette API échoue-t-il à la compilation en 4.7.2 ?
Un code partagé qui charge ce script par son chemin, seulement après détection, reste-t-il sans erreur sur les deux versions ?
Prouve-le avec --check-only et avec une exécution réelle.

Q3 UID DES SCRIPTS
Chaque script a-t-il un UID stable ? Regarde le fichier .uid, ResourceLoader.get_resource_uid et ResourceUID.id_to_text.
Que devient l'UID quand on déplace le script avec son fichier .uid ? Et sans lui ?

Q4 INVENTAIRE
Pour chaque API sensible prévue au POC (liste dans docs/ARCHITECTURE.md), vérifie sa présence et ses méthodes sur les deux versions avec ClassDB. Produis un tableau : API, présente en 4.7.2, présente en préversion, différence de signature constatée.

POUR CHAQUE QUESTION : le script exécuté, la commande, la sortie sur chaque version, la conclusion.
Ajoute spikes/spike02_compat/run.sh, qui rejoue tout pour une version passée en argument.
Écris docs/spikes/SPIKE-02.md avec une décision KEEP, REWRITE ou DISCARD pour deux points du plan : la règle d'isolation (§4) et la clé de correspondance des définitions (§5).
```

**Contrôles**

| ID | Contrôle | Attendu |
| --- | --- | --- |
| T06-a | `spikes/spike02_compat/run.sh <binaire 4.7.2>`, puis la même commande avec la préversion | Sorties identiques à celles du rapport |
| T06-b | Rapport : quatre sections, avec sorties sur les deux versions | Complet |
| T06-c | (CE) Le vérificateur retire la détection devant le chargement du script propre à la préversion | Erreur sur 4.7.2, comme le rapport le prédit |
| T06-d | Décisions proposées dans le rapport, puis reportées à la fusion dans `docs/DECISIONS.md` | Présentes et datées |
