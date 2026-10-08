# S11 — T06 SPIKE-02, frontière de compatibilité

> Fiche d'exécution du mode autonome. Chaque case se coche avec `python3 suivi/outil.py cocher S11 <sous-étape> --ia <n>`, juste après la sous-étape : la commande vérifie l'ordre et l'identité de l'IA, signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite. Règles : `docs/construction/sequence.md`. Avancement : `SUIVI.md` et `suivi/tableau.html`.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 1 (conception) |
| Vérifie | IA 3 (vérification), jamais un auteur de l'unité |
| Piste | 2.B SPIKE-02, compatibilité : S11 (unité 1 sur 1) |
| Commence après | S06 (cochée dans `SUIVI.md`) |
| Indépendante de | S07, S08, S09, S10 |
| Branche | `tache/S11-T06-spike02` |
| Fiche de conception | `docs/construction/etape-2.md`, section T06 |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Cette unité est la 1re de la piste 2.B « SPIKE-02, compatibilité », dont les unités se font à la suite. Les autres pistes de la section (2.A) avancent en même temps, chacune de son côté. Elle attend S06, hors de la piste. Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Répondre, preuves à l'appui sur 4.7.2 et sur 4.8-dev7, aux quatre questions : détection de capacités, isolation de compilation, UID des scripts, inventaire des API sensibles.
- Écrire `spikes/spike02_compat/run.sh` (rejoue tout pour une version passée en argument) et `docs/spikes/SPIKE-02.md` avec une décision KEEP, REWRITE ou DISCARD sur la règle d'isolation (plan §4) et sur la clé de correspondance (plan §5).

## Fichiers autorisés

`spikes/spike02_compat/`, `docs/spikes/SPIKE-02.md`. Les décisions sont reportées dans `docs/DECISIONS.md` à la fusion.

Toujours autorisés en plus : `rapports/S11*.md` et les cases de cette fiche (par `cocher`).

## Prompt de réalisation

```text
Tu réalises l'unité S11 « T06 SPIKE-02, frontière de compatibilité » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.
Réalisation prévue : IA 1 (conception) ; vérification : IA 3 (vérification). Ton numéro d'IA est celui que te donne le prompt de créneau : tu le passes à --ia, et il signe chaque case que tu coches.

AVANT TOUT, depuis ton clone principal du dépôt
1. Lis REGLES_AGENTS.md s'il existe, puis cette fiche : suivi/S11-T06-spike02.md.
2. python3 suivi/outil.py prendre S11 --ia <n>
   - « PRISE » ou « REPRISE » : tu es sur la branche tache/S11-T06-spike02 ; commence à la sous-étape affichée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
   - « REFUSÉ » : l'unité n'est pas pour toi maintenant (déjà prise par une autre IA, S06 non cochée, autre IA prévue) : reviens au prompt de créneau et choisis autre chose.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S11.md et les cases de suivi/S11-T06-spike02.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status. Tu ne pousses jamais avec --force.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.
- Une décision réservée à l'humain (docs/construction/sequence.md §5) : arrêt obligatoire, rien d'autre : python3 suivi/outil.py arreter --ia <n> --unite S11 --raison "<raison>", puis fin du créneau.

TRACE OBLIGATOIRE, après CHAQUE sous-étape et avant la suivante
1. git add <les fichiers de la sous-étape> (jamais git add -A).
2. python3 suivi/outil.py cocher S11 <sous-étape> --ia <n>
   La commande vérifie l'ordre des cases et ton identité, coche la case dans suivi/S11-T06-spike02.md, la signe (IA, date, heure UTC), commite et pousse sur tache/S11-T06-spike02.
3. Une sous-étape faite mais non cochée par cette commande est considérée comme non faite : l'IA suivante la refera. Tu ne coches jamais une case à la main.
4. Tu ne modifies jamais SUIVI.md : il ne change qu'à la fusion, sous le verrou de main. Plusieurs IA le lisent en même temps ; aucune ne l'écrit hors de ce verrou.
5. Avant de cocher la dernière sous-étape R : « Statut : TERMINÉ » dans rapports/S11.md, puis git add.
6. Poussée refusée et non rattrapée par la commande : ne force jamais ; git pull --rebase origin tache/S11-T06-spike02, puis relance la commande.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-2.md, T06)
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
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

ADAPTATIONS DU MODE AUTONOME
- Aucune : suis le travail technique tel quel.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche ; après chacune, git add puis python3 suivi/outil.py cocher S11 R<k> --ia <n>.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Chaque sous-étape faite est cochée par `cocher`. Complète rapports/S11.md (sorties, « Passation » en cinq lignes au plus), git add, git commit, git push origin HEAD:tache/S11-T06-spike02.
- git status ne montre aucune modification non commitée ; rien ne reste non poussé.

FORMAT DE rapports/S11.md (créé par prendre ; tu le complètes)
- Statut : EN COURS | TERMINÉ | QUESTION | ESCALADE
- Auteurs : IA n (écrit par `prendre`) · Tentative : n · Créneaux utilisés : n
- Fichiers modifiés : liste
- Contrôles : pour chacun, commande, code de sortie, 10 dernières lignes de sortie
- Contre-épreuves faites : liste
- Écarts au contrat, au guide ou à la fiche : aucun, ou liste
- Hypothèses : aucune, ou liste
- Questions : aucune, ou liste
- Pour la recette : ce qu'un humain devra vérifier, ou « rien »
- Passation : cinq lignes au plus
```

## Sous-étapes de réalisation

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher S11 R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre S11 --ia <n>` (prérequis cochés dans `SUIVI.md` : S06 ; branche `tache/S11-T06-spike02` créée ou reprise ; `rapports/S11.md` au statut EN COURS) ⟶ cochée par `prendre`
- [ ] R1 Obtenir les binaires 4.7.2-stable et 4.8-dev7 avec `tools/ci/fetch_godot.sh`. ⟶ cocher S11 R1
- [ ] R2 Q1 Détection de capacités : script, commande, sortie sur les deux versions. ⟶ cocher S11 R2
- [ ] R3 Q2 Isolation de compilation : `--check-only` et exécution réelle sur les deux versions. ⟶ cocher S11 R3
- [ ] R4 Q3 UID des scripts : fichier `.uid`, `ResourceLoader.get_resource_uid`, déplacement avec et sans `.uid`. ⟶ cocher S11 R4
- [ ] R5 Q4 Inventaire des API sensibles de `docs/ARCHITECTURE.md` : tableau par version. ⟶ cocher S11 R5
- [ ] R6 Écrire `spikes/spike02_compat/run.sh`. ⟶ cocher S11 R6
- [ ] R7 Écrire `docs/spikes/SPIKE-02.md` avec les deux décisions. ⟶ cocher S11 R7
- [ ] R8 Contrôles finaux : T06-a, T06-b, T06-c, T06-d exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » dans le rapport ⟶ cocher S11 R8

## Prompt de vérification

```text
Tu vérifies l'unité S11 « T06 SPIKE-02, frontière de compatibilité » du projet GODOT_DEV_MAPPER. Vérification prévue : IA 3 (vérification). Ton numéro d'IA est celui du prompt de créneau. Tu n'es jamais un auteur de l'unité : la commande de prise le contrôle.

PRISE, depuis ton clone principal
python3 suivi/outil.py prendre S11 --ia <n> --verification
- « VÉRIFICATION PRISE » : copie neuve ../verif-S11-T06-spike02 créée sur origin/tache/S11-T06-spike02, verdict EN COURS écrit, V1 cochée. cd ../verif-S11-T06-spike02 : toute la vérification se fait dans ce dossier.
- « REFUSÉ » : une autre IA vérifie déjà, tu es auteur, ou l'unité n'est pas terminée : reviens au prompt de créneau.
- Créneau fini avant le verdict : au créneau suivant, etat te propose la même commande ; elle recrée la copie (« VÉRIFICATION REPRISE ») et tu reprends à la première case V ouverte.
GODOT : même procédure que le prompt de réalisation.
Tu ne modifies aucun fichier de l'unité. Tu écris seulement ton verdict et tes cases V.

TRACE OBLIGATOIRE : après chaque sous-étape V, git add du fichier de verdict, puis python3 suivi/outil.py cocher S11 <V…> --ia <n>. Pour la dernière : --verdict ACCEPTÉE ou --verdict REFUSÉE, identique à la ligne « Verdict » du fichier. Une sous-étape non cochée par cette commande est considérée comme non faite.

1. TRAÇABILITÉ. Chaque case R cochée est signée « — IA n · date » et a son commit sur la branche (git log --oneline origin/main..HEAD). Case cochée sans travail prouvé dans le rapport : refus.
2. PÉRIMÈTRE. git diff --name-only origin/main...HEAD. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S11*.md et suivi/S11-T06-spike02.md. Tout autre fichier : refus.
3. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : T06-a, T06-b, T06-c, T06-d.
4. CONTRE-ÉPREUVES. Applique chaque sabotage marqué (CE) dans la fiche et dans le travail technique ; vérifie que le contrôle échoue ; annule avec git checkout -- . && git clean -fd (jamais sur rapports/).
5. CONTOURNEMENTS. Cherche :
   - test sans assertion, ou toujours vrai ;
   - test désactivé, renommé ou sorti du runner ;
   - valeur attendue recopiée depuis la sortie du code ;
   - marqueur supprimé de tests/pending/ sans test qui passe ;
   - fixture invalide rejetée pour un autre motif que celui de son nom ;
   - API Godot inventée ou non vérifiée ;
   - dépendance interdite entre modules ; API sensible hors de la frontière de compatibilité ;
   - affirmation du rapport sans sortie qui la prouve.
6. COHÉRENCE. Plan §4 (isolation) et §5 (clé de correspondance) ; liste des API sensibles.

VERDICT dans rapports/S11-verif-<tentative>.md (créé par la prise) :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte

SI ACCEPTÉE — FUSION, depuis ton clone principal (cd hors de ../verif-S11-T06-spike02)
1. python3 suivi/outil.py fusionner S11 --ia <n>
   Elle trouve Godot (--godot, $GODOT, cache du bloc GODOT ou tools/ci/fetch_godot.sh ; sans Godot : REFUSÉ, verdict inchangé), prend le verrou de main (et attend s'il est pris), revérifie l'unité, fusionne dans ../fusion-S11-T06-spike02, lance run_all_checks.sh, coche la ligne dans SUIVI.md et la case F1. Si les contrôles échouent : verdict passé à REFUSÉE, main inchangée, verrou rendu ; arrête-toi sur cette unité. La fusion te revient parce que tu as signé le verdict ; une autre IA ne la fait qu'après 12 h.
2. cd ../fusion-S11-T06-spike02 ; fais les sous-étapes F suivantes de la fiche, et coche chacune : python3 suivi/outil.py cocher S11 F<k> --ia <n> (commit local, sans poussée).
3. python3 suivi/outil.py publier S11 --ia <n> : dernière case cochée, verifier relancé, main poussée, branche supprimée, verrou rendu.
SI REFUSÉE : arrête-toi sur cette unité ; son auteur la reprendra avec prendre.
```

## Sous-étapes de vérification

Dans `../verif-S11-T06-spike02`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher S11 V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre S11 --ia <n> --verification` (pas un auteur ; copie neuve `../verif-S11-T06-spike02` sur `origin/tache/S11-T06-spike02` ; verdict EN COURS) ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R cochée porte une signature « — IA n · date » et un commit sur la branche (`git log --oneline origin/main..HEAD`) ⟶ cocher S11 V2
- [ ] V3 Périmètre : `git diff --name-only origin/main...HEAD` ⊂ fichiers autorisés. ⟶ cocher S11 V3
- [ ] V4.1 Contrôle T06-a relancé, résultat conforme. ⟶ cocher S11 V4.1
- [ ] V4.2 Contrôle T06-b relancé, résultat conforme. ⟶ cocher S11 V4.2
- [ ] V4.3 Contrôle T06-c relancé, résultat conforme. ⟶ cocher S11 V4.3
- [ ] V4.4 Contrôle T06-d relancé, résultat conforme. ⟶ cocher S11 V4.4
- [ ] V5 Contre-épreuves (CE) appliquées et détectées, puis annulées. ⟶ cocher S11 V5
- [ ] V6 Contournements cherchés. ⟶ cocher S11 V6
- [ ] V7 Cohérence avec les contrats et les invariants. ⟶ cocher S11 V7
- [ ] V8 Verdict écrit dans `rapports/S11-verif-<tentative>.md` ⟶ cocher S11 V8 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

F1 et la dernière se cochent par `fusionner` et `publier` ; les autres, dans `../fusion-S11-T06-spike02`, par `python3 suivi/outil.py cocher S11 F<k> --ia <n>` (commit local).

- [ ] F1 Fusion, depuis le clone principal : `python3 suivi/outil.py fusionner S11 --ia <n>` : Godot trouvé seul (--godot, $GODOT, cache du bloc GODOT ou fetch_godot.sh), verrou de `main`, fusion `--no-ff` dans `../fusion-S11-T06-spike02`, `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK s'il existe (sinon fusion annulée et verdict passé à REFUSÉE), ligne **S11** cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 Inscrire dans `docs/DECISIONS.md` les deux décisions de SPIKE-02 (règle d'isolation, clé de correspondance), au statut « adoptée par défaut », avec la date. ⟶ cocher S11 F2
- [ ] F3 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette ⟶ cocher S11 F3
- [ ] F4 Publication : `python3 suivi/outil.py publier S11 --ia <n>` (verifier OK, `main` poussée, branche `tache/S11-T06-spike02` supprimée, verrou rendu) ⟶ cochée par `publier`

## Pour la recette

Rien de propre à cette unité.
