# S02 — 0.B Squelettes et règles des agents

> Fiche d'exécution du mode autonome. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse : une autre IA doit pouvoir reprendre à la première case non cochée. Règles : `docs/construction/sequence.md`. Avancement global : `SUIVI.md`.

| Champ | Valeur |
| --- | --- |
| Réalise | Concepteur |
| Vérifie | Vérificateur (jamais l'auteur) |
| Commence après | S01 (cochées dans `SUIVI.md`) |
| Indépendante de | S07 |
| Branche | `tache/S02-0B-squelettes` |
| Fiche de conception | `docs/construction/etape-0.md`, section 0.B |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité elle-même peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Créer `docs/SPEC.md`, `docs/ARCHITECTURE.md` (avec la liste des API sensibles), `docs/CONTRACTS.md` (sept sections C-01 à C-07, sept rubriques chacune, contenu « à rédiger en T07 » ou « en T08 »), `docs/COMPATIBILITY.md`, `docs/TEST_PLAN.md`. Chacun commence par « Statut : proposé · date ».
- Créer `PROJECT_STATE.md` : mis à jour seulement à la fusion ; sections Mesures, Dette, Versions de Godot testées, Liste de recette (reprise du §7 de `sequence.md`). L'avancement des unités est dans `SUIVI.md` : ne pas le recopier.
- Créer `REGLES_AGENTS.md`, 150 lignes au plus : règles non négociables, règles de cochage des fiches `suivi/`, format de rapport, INV-01 à INV-09 en une ligne chacun, commandes de contrôle vérifiées, renvoi à `sequence.md` et à `SUIVI.md`.
- Créer `tools/sync_rules.sh` : copie `REGLES_AGENTS.md` vers `CLAUDE.md` et `GEMINI.md` ; avec `--check`, compare sans écrire et sort en 1 si une copie diffère.

## Fichiers autorisés

`docs/SPEC.md`, `docs/ARCHITECTURE.md`, `docs/CONTRACTS.md`, `docs/COMPATIBILITY.md`, `docs/TEST_PLAN.md`, `PROJECT_STATE.md`, `REGLES_AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `tools/sync_rules.sh`.

Toujours autorisés en plus : `rapports/S02*.md` et les cases de cette fiche.

## Contrôles propres à cette fiche

- `S02-a` : `for f in docs/SPEC.md docs/ARCHITECTURE.md docs/CONTRACTS.md docs/COMPATIBILITY.md docs/TEST_PLAN.md PROJECT_STATE.md REGLES_AGENTS.md; do test -s "$f" || echo "manque $f"; done` → aucune sortie
- `S02-b` : `grep -L "^Statut" docs/SPEC.md docs/ARCHITECTURE.md docs/CONTRACTS.md docs/COMPATIBILITY.md docs/TEST_PLAN.md` → aucune sortie
- `S02-c` : `tools/sync_rules.sh && tools/sync_rules.sh --check; echo $?` → 0
- `S02-d` : `wc -l < REGLES_AGENTS.md` → 150 au plus
- `S02-e` : `for c in C-01 C-02 C-03 C-04 C-05 C-06 C-07; do grep -c "^## $c" docs/CONTRACTS.md; done` → 1 pour chacun
- `S02-f` : `grep -c "SUIVI.md" REGLES_AGENTS.md PROJECT_STATE.md` → au moins 1 dans chaque fichier
- (CE) `echo x >> CLAUDE.md; tools/sync_rules.sh --check; echo $?` → 1, puis `tools/sync_rules.sh` pour rétablir.

## Prompt de réalisation

```text
Tu es <ton nom d'IA>, au rôle Concepteur. Tu réalises l'unité S02 « 0.B Squelettes et règles des agents » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.

AVANT TOUT
1. git fetch origin. Lis REGLES_AGENTS.md s'il existe, puis la fiche suivi/S02-0B-squelettes.md.
2. Si la branche origin/tache/S02-0B-squelettes existe : reprends-la, relis rapports/S02.md et commence à la première sous-étape R non cochée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
3. Sinon : vérifie dans SUIVI.md, sur main, que S01 est cochée, puis crée tache/S02-0B-squelettes depuis main.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S02.md et les cases de suivi/S02-0B-squelettes.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu coches une case seulement quand elle est faite et prouvée. Tu commites et tu pousses après chaque case cochée.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-0.md, 0.B)
Tu crées les squelettes de documents du projet GODOT_DEV_MAPPER. Tu n'écris aucun code du plugin.
Sources : docs/plan-directeur.md, docs/methodologie.md, docs/DECISIONS.md, docs/construction/README.md.

À CRÉER
- docs/SPEC.md : vision, scénarios et capacités, extraits des §1 à 3 du plan ; renvoie au plan pour le détail.
- docs/ARCHITECTURE.md : modules, dépendances autorisées et interdites, frontière de compatibilité, liste des API sensibles (plan §4).
- docs/CONTRACTS.md : une section par contrat C-01 à C-07, avec sept rubriques : objet, format ou API, exemples valides, exemples invalides, comportement en erreur, version, tests de contrat. Contenu : « à rédiger en T07 » ou « à rédiger en T08 ».
- docs/COMPATIBILITY.md : fenêtre de support issue de D-01 et D-07.
- docs/TEST_PLAN.md : types de tests, commandes de contrôle vérifiées (reprises du guide), principe des contre-épreuves.
- PROJECT_STATE.md : tableau des tâches T00 à T20, T13 découpée en T13a, T13b et T13c, au statut « À faire », avec en tête la mention « mis à jour seulement à l'étape de fusion » ; budget de chaque étape ; mesures à tenir (heures humaines, temps agent, capacités acceptées, réussite par modèle).
- REGLES_AGENTS.md : 150 lignes au plus. Il contient les règles non négociables et le format de rapport du prompt universel de réalisation, les invariants INV-01 à INV-09 en une ligne chacun, et les commandes de contrôle.
- tools/sync_rules.sh : copie REGLES_AGENTS.md vers CLAUDE.md et GEMINI.md. Avec --check, il compare sans rien écrire et renvoie 1 si une copie diffère.

RÈGLES
Chaque document normatif commence par « Statut : proposé · 8 octobre 2026 » (ou la date du jour). Une définition n'existe qu'à un seul endroit ; ailleurs, on y renvoie.

CONTRÔLES (exécute-les et colle les sorties)
1. for f in docs/SPEC.md docs/ARCHITECTURE.md docs/CONTRACTS.md docs/COMPATIBILITY.md docs/TEST_PLAN.md PROJECT_STATE.md REGLES_AGENTS.md; do test -s "$f" || echo "manque $f"; done   → aucune sortie
2. grep -L "^Statut" docs/SPEC.md docs/ARCHITECTURE.md docs/CONTRACTS.md docs/COMPATIBILITY.md docs/TEST_PLAN.md   → aucune sortie
3. tools/sync_rules.sh && tools/sync_rules.sh --check; echo $?   → 0
4. (CE) echo x >> CLAUDE.md; tools/sync_rules.sh --check; echo $?   → 1, puis tools/sync_rules.sh pour rétablir
5. wc -l < REGLES_AGENTS.md   → 150 au plus
6. for c in C-01 C-02 C-03 C-04 C-05 C-06 C-07; do grep -c "^## $c" docs/CONTRACTS.md; done   → 1 pour chacun

Rapport au format du prompt universel de réalisation.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

CONTRÔLES DE LA FICHE
S02-a  for f in docs/SPEC.md docs/ARCHITECTURE.md docs/CONTRACTS.md docs/COMPATIBILITY.md docs/TEST_PLAN.md PROJECT_STATE.md REGLES_AGENTS.md; do test -s "$f" || echo "manque $f"; done   → aucune sortie
S02-b  grep -L "^Statut" docs/SPEC.md docs/ARCHITECTURE.md docs/CONTRACTS.md docs/COMPATIBILITY.md docs/TEST_PLAN.md   → aucune sortie
S02-c  tools/sync_rules.sh && tools/sync_rules.sh --check; echo $?   → 0
S02-d  wc -l < REGLES_AGENTS.md   → 150 au plus
S02-e  for c in C-01 C-02 C-03 C-04 C-05 C-06 C-07; do grep -c "^## $c" docs/CONTRACTS.md; done   → 1 pour chacun
S02-f  grep -c "SUIVI.md" REGLES_AGENTS.md PROJECT_STATE.md   → au moins 1 dans chaque fichier
(CE) `echo x >> CLAUDE.md; tools/sync_rules.sh --check; echo $?` → 1, puis `tools/sync_rules.sh` pour rétablir.

ADAPTATIONS DU MODE AUTONOME
- `PROJECT_STATE.md` ne contient pas le tableau des tâches T00 à T20 demandé par le guide : l'avancement vit dans `SUIVI.md`. Il contient les mesures, la dette, les versions testées et la liste de recette.
- `REGLES_AGENTS.md` ajoute les règles de cochage : une case cochée seulement quand elle est faite et prouvée, un push après chaque case, reprise à la première case non cochée.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Coche dans suivi/S02-0B-squelettes.md les sous-étapes faites et prouvées ; complète rapports/S02.md (sorties, section « Passation ») ; commite ; git push origin tache/S02-0B-squelettes.
- Ne laisse aucune modification non poussée.

FORMAT DE rapports/S02.md
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

- [ ] R0 Prise en charge : `git fetch origin` ; S01 est cochée dans `SUIVI.md` ; branche `origin/tache/S02-0B-squelettes` absente, ou sans commit depuis deux créneaux, ou dernier verdict REFUSÉE ; créer ou reprendre la branche ; `rapports/S02.md` avec « Statut : EN COURS » et « Auteur » ; commit ; push.
- [ ] R1 Lire le plan, la méthode, `docs/DECISIONS.md`, `docs/construction/README.md` et `docs/construction/sequence.md`.
- [ ] R2 Créer les cinq documents normatifs, chacun avec sa ligne de statut.
- [ ] R3 Créer `PROJECT_STATE.md` selon la fiche (pas de tableau des tâches : il renvoie à `SUIVI.md`).
- [ ] R4 Créer `REGLES_AGENTS.md` (150 lignes au plus) avec les règles de cochage des fiches `suivi/`.
- [ ] R5 Créer `tools/sync_rules.sh`, le rendre exécutable, l'exécuter pour produire `CLAUDE.md` et `GEMINI.md`.
- [ ] R6 Contrôles finaux : S02-a, S02-b, S02-c, S02-d, S02-e, S02-f exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » ; commit ; push.

## Prompt de vérification

```text
Tu es <ton nom d'IA>, au rôle Vérificateur, vérificateur indépendant de l'unité S02 « 0.B Squelettes et règles des agents » du projet GODOT_DEV_MAPPER.
Tu n'en es pas l'auteur : lis la ligne « Auteur » de rapports/S02.md ; si c'est toi, arrête-toi.
Tu ne modifies aucun fichier de l'unité. Tu écris ton verdict et tu coches les sous-étapes V, sur la branche.

COPIE NEUVE : git fetch origin && git worktree add --detach ../verif-S02-0B-squelettes origin/tache/S02-0B-squelettes
GODOT : même procédure que le prompt de réalisation.

1. PÉRIMÈTRE. git diff --name-only origin/main...origin/tache/S02-0B-squelettes. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S02*.md et suivi/S02-0B-squelettes.md. Tout autre fichier : refus.
2. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : S02-a, S02-b, S02-c, S02-d, S02-e, S02-f.
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
5. COHÉRENCE. Aucune définition à deux endroits ; chaque règle du plan présente et non déformée ; INV-01 à INV-09 complets ; commandes identiques à celles du guide ; décisions de `docs/DECISIONS.md` reprises (prompt de relecture du guide, ci-dessous).
RELECTURE CROISÉE, prompt du guide :
Relis les squelettes créés à l'étape 0 du projet GODOT_DEV_MAPPER : docs/SPEC.md, docs/ARCHITECTURE.md, docs/CONTRACTS.md, docs/COMPATIBILITY.md, docs/TEST_PLAN.md, PROJECT_STATE.md, REGLES_AGENTS.md. Compare-les à docs/plan-directeur.md.
Cherche : une définition présente à deux endroits ; une règle du plan déformée ou absente ; un invariant manquant ; une commande de contrôle différente de celle du guide ; une décision de docs/DECISIONS.md non reprise.
Ne modifie rien. Rapport : liste numérotée avec fichier, passage, écart, correction proposée ; « aucun écart » sinon.

VERDICT dans rapports/S02-verif-<tentative>.md :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte
Pousse le verdict sur la branche. Si ACCEPTÉE, fais les sous-étapes F de la fiche. Si REFUSÉE, arrête-toi : une IA au rôle de l'auteur reprendra.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge : pas l'auteur ; copie neuve `../verif-S02-0B-squelettes` sur `origin/tache/S02-0B-squelettes`.
- [ ] V2 Périmètre : `git diff --name-only origin/main...origin/tache/S02-0B-squelettes` ⊂ fichiers autorisés.
- [ ] V3.1 Contrôle S02-a relancé, résultat conforme.
- [ ] V3.2 Contrôle S02-b relancé, résultat conforme.
- [ ] V3.3 Contrôle S02-c relancé, résultat conforme.
- [ ] V3.4 Contrôle S02-d relancé, résultat conforme.
- [ ] V3.5 Contrôle S02-e relancé, résultat conforme.
- [ ] V3.6 Contrôle S02-f relancé, résultat conforme.
- [ ] V4 Contre-épreuves (CE) appliquées et détectées, puis annulées.
- [ ] V5 Contournements cherchés.
- [ ] V6 Cohérence avec les contrats et les invariants.
- [ ] V7 Verdict écrit dans `rapports/S02-verif-<tentative>.md` et poussé.

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `git switch main && git pull --ff-only && git merge --no-ff origin/tache/S02-0B-squelettes -m "Fusion S02 : 0.B Squelettes et règles des agents"`.
- [ ] F2 Sur `main` : `GODOT="$B" tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK. Sinon : `git reset --hard ORIG_HEAD`, verdict « REFUSÉE (fusion) » poussé sur la branche, et arrêt de la fusion.
- [ ] F3 Dans `SUIVI.md`, cocher la ligne **S02** et compléter « fait le <date> · auteur <IA> · vérifié par <IA> · <n> créneaux ».
- [ ] F4 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette.
- [ ] F5 Cocher les sous-étapes F de cette fiche ; `git commit` ; `git push origin main` (en cas de refus : `git pull --rebase`, puis push).

## Pour la recette

Rien de propre à cette unité.
