# S14 — T08 Contrats C-03, C-04, C-06, C-07

> Fiche d'exécution du mode autonome. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse : une autre IA doit pouvoir reprendre à la première case non cochée. Règles : `docs/construction/sequence.md`. Avancement global : `SUIVI.md`.

| Champ | Valeur |
| --- | --- |
| Réalise | Concepteur |
| Vérifie | Vérificateur (jamais l'auteur) |
| Commence après | S10, S12, S13 (cochées dans `SUIVI.md`) |
| Indépendante de | aucune |
| Branche | `tache/S14-T08-contrats` |
| Fiche de conception | `docs/construction/etape-3.md`, section T08 |
| Estimation | 2 créneaux |

**Séquentiel ou indépendant.** Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité elle-même peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Remplir les sept rubriques de C-03 (façades), C-04 (enveloppe et limites), C-06 (Event Store, lacunes, fin inconnue, chemin observé) et C-07 (API FlowTrace, table d'états du protocole de session, frontière de frame, bail, chemin désactivé).
- Écrire le schéma de l'enveloppe, ses fixtures, les sessions enregistrées, et les quatre tests de contrat avec leurs marqueurs (T09, T11, T12, T13a).

## Fichiers autorisés

- `docs/CONTRACTS.md`, sections C-03, C-04, C-06 et C-07 ;
- `contracts/schemas/envelope.v1.schema.json` ;
- `tests/contract/fixtures/envelope/`, `tests/contract/fixtures/sessions/` ;
- `tests/contract/test_c03_facades.gd`, `test_c04_envelope.gd`, `test_c06_store.gd`, `test_c07_flowtrace.gd` ;
- les marqueurs T09, T11, T12 et T13a de `tests/pending/`.

Toujours autorisés en plus : `rapports/S14*.md` et les cases de cette fiche.

## Prompt de réalisation

```text
Tu es <ton nom d'IA>, au rôle Concepteur. Tu réalises l'unité S14 « T08 Contrats C-03, C-04, C-06, C-07 » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.

AVANT TOUT
1. git fetch origin. Lis REGLES_AGENTS.md s'il existe, puis la fiche suivi/S14-T08-contrats.md.
2. Si la branche origin/tache/S14-T08-contrats existe : reprends-la, relis rapports/S14.md et commence à la première sous-étape R non cochée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
3. Sinon : vérifie dans SUIVI.md, sur main, que S10, S12, S13 sont cochées, puis crée tache/S14-T08-contrats depuis main.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S14.md et les cases de suivi/S14-T08-contrats.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu coches une case seulement quand elle est faite et prouvée. Tu commites et tu pousses après chaque case cochée.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-3.md, T08)
Tu rédiges les contrats C-03, C-04, C-06 et C-07 du projet GODOT_DEV_MAPPER, et les tests qui les jugeront. Tu n'écris aucune implémentation. C-01 est validé : appuie-toi dessus sans le modifier.

SOURCES NORMATIVES
docs/plan-directeur.md §4 (façades), §6 (protocole de session, garanties, champs par type, chemin observé) et §8 (budgets, cycle de vie) ; docs/spikes/SPIKE-01.md, parties 01a et 01b ; docs/spikes/SPIKE-02.md.

DANS docs/CONTRACTS.md, les sept rubriques pour chaque contrat :
- C-03 Façades : pour chaque façade (runtime, débogueur, éditeur), la liste des opérations avec leur signature GDScript, leur comportement en erreur et la capacité qu'elles requièrent. La façade runtime accepte un transport de substitution pour les tests.
- C-04 Enveloppe : format des lots, champs communs et hérités, champs requis par type, limites (1 Ko par charge, 256 événements et 64 Ko par lot), réserve de contrôle de 64 places, identifiants 64 bits en chaîne, rejet d'une version inconnue.
- C-06 Event Store : sessions, lacunes déduites des séquences, rétention et marqueur « tronqué avant seq N », fin de session et « fin inconnue », requête « chemin observé » à trois états.
- C-07 FlowTrace : API statique (init, register, enter, exit, decision, enabled, shutdown) ; table d'états du protocole de session (inerte, prêt, collecte, arrêt demandé, arrêté, bail expiré, capture interrompue) avec toutes les transitions ; commandes appliquées à la frontière de frame ; bail de 2 s renouvelé toutes les 250 ms ; messages du moteur ignorés ; règles du chemin désactivé ; limite au périmètre synchrone.

À PRODUIRE AUSSI
- contracts/schemas/envelope.v1.schema.json et tests/contract/fixtures/envelope/ avec des fichiers valid_* et invalid_<CODE>__<description>. Au minimum : version de protocole inconnue, séquence non croissante dans un lot, décision sans payload.result, function_enter sans inv, lot de 257 événements, charge de plus de 1 Ko, identifiant 64 bits écrit comme nombre. La séquence non croissante et la charge de plus de 1 Ko, mesurée en octets, relèvent du niveau 2.
- tests/contract/fixtures/sessions/ : des sessions enregistrées au format de l'enveloppe. Au minimum : normale ; coupée sans fin ; avec trous ; mêlée de messages du moteur ; avec commande reçue en réentrance.
- Les quatre tests de contrat, chacun avec son marqueur dans tests/pending/ : C-04 → T09, C-06 → T11, C-03 → T12, C-07 → T13a.

RÈGLES
- Chaque transition de la table d'états de C-07 a au moins un test.
- Les constats de SPIKE-01a et 01b sont repris tels quels ; s'ils contredisent le plan, signale l'écart.
- Tout écart avec le plan est listé en tête de ton rapport.

CONTRÔLES
T08-a  python3 tools/check_contracts.py ; echo $?                            → 0 (sept contrats)
T08-b  python3 tools/validate_fixtures.py ; echo $?                          → 0
T08-b2 python3 tools/validate_fixtures.py --plan-examples ; echo $?   → 0 (tous les exemples du plan)
T08-c  (CE) remplace un identifiant chaîne par un nombre dans une fixture valide de l'enveloppe, relance T08-b   → 1 ; annule
T08-d  Tableau croisé dans le rapport : chaque transition de C-07 avec le test qui la couvre   → aucune transition sans test
T08-e  godot --headless --path . -s res://tests/run_all.gd ; echo $?         → 0, pending=6
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

ADAPTATIONS DU MODE AUTONOME
- Aucune : suis le travail technique tel quel.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Coche dans suivi/S14-T08-contrats.md les sous-étapes faites et prouvées ; complète rapports/S14.md (sorties, section « Passation ») ; commite ; git push origin tache/S14-T08-contrats.
- Ne laisse aucune modification non poussée.

FORMAT DE rapports/S14.md
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

- [ ] R0 Prise en charge : `git fetch origin` ; S10, S12, S13 sont cochées dans `SUIVI.md` ; branche `origin/tache/S14-T08-contrats` absente, ou sans commit depuis deux créneaux, ou dernier verdict REFUSÉE ; créer ou reprendre la branche ; `rapports/S14.md` avec « Statut : EN COURS » et « Auteur » ; commit ; push.
- [ ] R1 Lire le plan §4, §6 et §8, `docs/spikes/SPIKE-01.md` (01a et 01b), `docs/spikes/SPIKE-02.md` et C-01 validé.
- [ ] R2 Rédiger C-03.
- [ ] R3 Rédiger C-04.
- [ ] R4 Rédiger C-06.
- [ ] R5 Rédiger C-07, avec la table d'états complète et le constat de SPIKE-01b sur la file de commandes s'il existe.
- [ ] R6 Écrire le schéma de l'enveloppe et ses fixtures (au moins les sept invalides de la fiche).
- [ ] R7 Écrire les sessions enregistrées (au moins les cinq de la fiche).
- [ ] R8 Écrire les quatre tests de contrat et leurs marqueurs.
- [ ] R9 Écrire le tableau croisé transition → test de C-07 dans le rapport.
- [ ] R10 Contrôles finaux : T08-a, T08-b, T08-b2, T08-c, T08-d, T08-e exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » ; commit ; push.

## Prompt de vérification

```text
Tu es <ton nom d'IA>, au rôle Vérificateur, vérificateur indépendant de l'unité S14 « T08 Contrats C-03, C-04, C-06, C-07 » du projet GODOT_DEV_MAPPER.
Tu n'en es pas l'auteur : lis la ligne « Auteur » de rapports/S14.md ; si c'est toi, arrête-toi.
Tu ne modifies aucun fichier de l'unité. Tu écris ton verdict et tu coches les sous-étapes V, sur la branche.

COPIE NEUVE : git fetch origin && git worktree add --detach ../verif-S14-T08-contrats origin/tache/S14-T08-contrats
GODOT : même procédure que le prompt de réalisation.

1. PÉRIMÈTRE. git diff --name-only origin/main...origin/tache/S14-T08-contrats. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S14*.md et suivi/S14-T08-contrats.md. Tout autre fichier : refus.
2. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : T08-a, T08-b, T08-b2, T08-c, T08-d, T08-e.
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
5. COHÉRENCE. Plan §4, §6 et §8 ; constats de SPIKE-01a et 01b repris tels quels ; C-01 non modifié.

VERDICT dans rapports/S14-verif-<tentative>.md :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte
Pousse le verdict sur la branche. Si ACCEPTÉE, fais les sous-étapes F de la fiche. Si REFUSÉE, arrête-toi : une IA au rôle de l'auteur reprendra.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge : pas l'auteur ; copie neuve `../verif-S14-T08-contrats` sur `origin/tache/S14-T08-contrats`.
- [ ] V2 Périmètre : `git diff --name-only origin/main...origin/tache/S14-T08-contrats` ⊂ fichiers autorisés.
- [ ] V3.1 Contrôle T08-a relancé, résultat conforme.
- [ ] V3.2 Contrôle T08-b relancé, résultat conforme.
- [ ] V3.3 Contrôle T08-b2 relancé, résultat conforme.
- [ ] V3.4 Contrôle T08-c relancé, résultat conforme.
- [ ] V3.5 Contrôle T08-d relancé, résultat conforme.
- [ ] V3.6 Contrôle T08-e relancé, résultat conforme.
- [ ] V4 Contre-épreuves (CE) appliquées et détectées, puis annulées.
- [ ] V5 Contournements cherchés.
- [ ] V6 Cohérence avec les contrats et les invariants.
- [ ] V7 Verdict écrit dans `rapports/S14-verif-<tentative>.md` et poussé.

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `git switch main && git pull --ff-only && git merge --no-ff origin/tache/S14-T08-contrats -m "Fusion S14 : T08 Contrats C-03, C-04, C-06, C-07"`.
- [ ] F2 Sur `main` : `GODOT="$B" tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK. Sinon : `git reset --hard ORIG_HEAD`, verdict « REFUSÉE (fusion) » poussé sur la branche, et arrêt de la fusion.
- [ ] F3 Dans `SUIVI.md`, cocher la ligne **S14** et compléter « fait le <date> · auteur <IA> · vérifié par <IA> · <n> créneaux ».
- [ ] F4 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette.
- [ ] F5 Cocher les sous-étapes F de cette fiche ; `git commit` ; `git push origin main` (en cas de refus : `git pull --rebase`, puis push).

## Pour la recette

Rien de propre à cette unité.
