# S11 — T06 SPIKE-02, frontière de compatibilité

> Fiche d'exécution du mode autonome. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse : une autre IA doit pouvoir reprendre à la première case non cochée. Règles : `docs/construction/sequence.md`. Avancement global : `SUIVI.md`.

| Champ | Valeur |
| --- | --- |
| Réalise | Concepteur |
| Vérifie | Vérificateur (jamais l'auteur) |
| Commence après | S06 (cochées dans `SUIVI.md`) |
| Indépendante de | S07, S08, S09, S10 |
| Branche | `tache/S11-T06-spike02` |
| Fiche de conception | `docs/construction/etape-2.md`, section T06 |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité elle-même peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Répondre, preuves à l'appui sur 4.7.2 et sur 4.8-dev7, aux quatre questions : détection de capacités, isolation de compilation, UID des scripts, inventaire des API sensibles.
- Écrire `spikes/spike02_compat/run.sh` (rejoue tout pour une version passée en argument) et `docs/spikes/SPIKE-02.md` avec une décision KEEP, REWRITE ou DISCARD sur la règle d'isolation (plan §4) et sur la clé de correspondance (plan §5).

## Fichiers autorisés

`spikes/spike02_compat/`, `docs/spikes/SPIKE-02.md`. Les décisions sont reportées dans `docs/DECISIONS.md` à la fusion.

Toujours autorisés en plus : `rapports/S11*.md` et les cases de cette fiche.

## Prompt de réalisation

```text
Tu es <ton nom d'IA>, au rôle Concepteur. Tu réalises l'unité S11 « T06 SPIKE-02, frontière de compatibilité » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.

AVANT TOUT
1. git fetch origin. Lis REGLES_AGENTS.md s'il existe, puis la fiche suivi/S11-T06-spike02.md.
2. Si la branche origin/tache/S11-T06-spike02 existe : reprends-la, relis rapports/S11.md et commence à la première sous-étape R non cochée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
3. Sinon : vérifie dans SUIVI.md, sur main, que S06 est cochée, puis crée tache/S11-T06-spike02 depuis main.

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
- Tu coches une case seulement quand elle est faite et prouvée. Tu commites et tu pousses après chaque case cochée.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.

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

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Coche dans suivi/S11-T06-spike02.md les sous-étapes faites et prouvées ; complète rapports/S11.md (sorties, section « Passation ») ; commite ; git push origin tache/S11-T06-spike02.
- Ne laisse aucune modification non poussée.

FORMAT DE rapports/S11.md
- Statut : EN COURS | TERMINÉ | QUESTION | ESCALADE
- Auteur : <ton nom d'IA> · Tentative : n · Créneaux utilisés : n
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

- [ ] R0 Prise en charge : `git fetch origin` ; S06 est cochée dans `SUIVI.md` ; branche `origin/tache/S11-T06-spike02` absente, ou sans commit depuis deux créneaux, ou dernier verdict REFUSÉE ; créer ou reprendre la branche ; `rapports/S11.md` avec « Statut : EN COURS » et « Auteur » ; commit ; push.
- [ ] R1 Obtenir les binaires 4.7.2-stable et 4.8-dev7 avec `tools/ci/fetch_godot.sh`.
- [ ] R2 Q1 Détection de capacités : script, commande, sortie sur les deux versions.
- [ ] R3 Q2 Isolation de compilation : `--check-only` et exécution réelle sur les deux versions.
- [ ] R4 Q3 UID des scripts : fichier `.uid`, `ResourceLoader.get_resource_uid`, déplacement avec et sans `.uid`.
- [ ] R5 Q4 Inventaire des API sensibles de `docs/ARCHITECTURE.md` : tableau par version.
- [ ] R6 Écrire `spikes/spike02_compat/run.sh`.
- [ ] R7 Écrire `docs/spikes/SPIKE-02.md` avec les deux décisions.
- [ ] R8 Contrôles finaux : T06-a, T06-b, T06-c, T06-d exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » ; commit ; push.

## Prompt de vérification

```text
Tu es <ton nom d'IA>, au rôle Vérificateur, vérificateur indépendant de l'unité S11 « T06 SPIKE-02, frontière de compatibilité » du projet GODOT_DEV_MAPPER.
Tu n'en es pas l'auteur : lis la ligne « Auteur » de rapports/S11.md ; si c'est toi, arrête-toi.
Tu ne modifies aucun fichier de l'unité. Tu écris ton verdict et tu coches les sous-étapes V, sur la branche.

COPIE NEUVE : git fetch origin && git worktree add --detach ../verif-S11-T06-spike02 origin/tache/S11-T06-spike02
GODOT : même procédure que le prompt de réalisation.

1. PÉRIMÈTRE. git diff --name-only origin/main...origin/tache/S11-T06-spike02. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S11*.md et suivi/S11-T06-spike02.md. Tout autre fichier : refus.
2. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : T06-a, T06-b, T06-c, T06-d.
3. CONTRE-ÉPREUVES. Applique chaque sabotage marqué (CE) dans la fiche et dans le travail technique ; vérifie que le contrôle échoue ; annule avec git checkout -- . && git clean -fd.
4. CONTOURNEMENTS. Cherche :
   - test sans assertion, ou toujours vrai ;
   - test désactivé, renommé ou sorti du runner ;
   - valeur attendue recopiée depuis la sortie du code ;
   - marqueur supprimé de tests/pending/ sans test qui passe ;
   - fixture invalide rejetée pour un autre motif que celui de son nom ;
   - API Godot inventée ou non vérifiée ;
   - dépendance interdite entre modules ; API sensible hors de la frontière de compatibilité ;
   - affirmation du rapport sans sortie qui la prouve.
5. COHÉRENCE. Plan §4 (isolation) et §5 (clé de correspondance) ; liste des API sensibles.

VERDICT dans rapports/S11-verif-<tentative>.md :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte
Pousse le verdict sur la branche. Si ACCEPTÉE, fais les sous-étapes F de la fiche. Si REFUSÉE, arrête-toi : une IA au rôle de l'auteur reprendra.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge : pas l'auteur ; copie neuve `../verif-S11-T06-spike02` sur `origin/tache/S11-T06-spike02`.
- [ ] V2 Périmètre : `git diff --name-only origin/main...origin/tache/S11-T06-spike02` ⊂ fichiers autorisés.
- [ ] V3.1 Contrôle T06-a relancé, résultat conforme.
- [ ] V3.2 Contrôle T06-b relancé, résultat conforme.
- [ ] V3.3 Contrôle T06-c relancé, résultat conforme.
- [ ] V3.4 Contrôle T06-d relancé, résultat conforme.
- [ ] V4 Contre-épreuves (CE) appliquées et détectées, puis annulées.
- [ ] V5 Contournements cherchés.
- [ ] V6 Cohérence avec les contrats et les invariants.
- [ ] V7 Verdict écrit dans `rapports/S11-verif-<tentative>.md` et poussé.

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `git switch main && git pull --ff-only && git merge --no-ff origin/tache/S11-T06-spike02 -m "Fusion S11 : T06 SPIKE-02, frontière de compatibilité"`.
- [ ] F2 Sur `main` : `GODOT="$B" tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK. Sinon : `git reset --hard ORIG_HEAD`, verdict « REFUSÉE (fusion) » poussé sur la branche, et arrêt de la fusion.
- [ ] F3 Dans `SUIVI.md`, cocher la ligne **S11** et compléter « fait le <date> · auteur <IA> · vérifié par <IA> · <n> créneaux ».
- [ ] F4 Inscrire dans `docs/DECISIONS.md` les deux décisions de SPIKE-02 (règle d'isolation, clé de correspondance), au statut « adoptée par défaut », avec la date.
- [ ] F5 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette.
- [ ] F6 Cocher les sous-étapes F de cette fiche ; `git commit` ; `git push origin main` (en cas de refus : `git pull --rebase`, puis push).

## Pour la recette

Rien de propre à cette unité.
