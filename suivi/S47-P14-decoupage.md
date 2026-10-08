# S47 — P14 Performance corrélée : découpage

> Fiche d'exécution du mode autonome. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse : une autre IA doit pouvoir reprendre à la première case non cochée. Règles : `docs/construction/sequence.md`. Avancement global : `SUIVI.md`.

| Champ | Valeur |
| --- | --- |
| Réalise | Concepteur |
| Vérifie | Vérificateur (jamais l'auteur) |
| Commence après | S41.P (cochées dans `SUIVI.md`) |
| Indépendante de | S42, S42.P, S43, S43.P, S44, S44.P, S45, S45.P, S46, S46.P, S48, S48.P |
| Branche | `tache/S47-P14-decoupage` |
| Fiche de conception | `docs/construction/v1.md`, section P14 |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité elle-même peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Découper la phase P14 en 4 à 12 tâches avec le prompt de découpage de `docs/construction/v1.md`, en tenant compte des résultats du POC et des phases précédentes.
- Écrire `docs/construction/v1-P14.md` (conception) et une fiche d'exécution par tâche, `suivi/S47.<k>-<nom>.md`, à partir de `suivi/_modele-tache.md`.
- Donner à chaque tâche ses prérequis réels : une tâche qui ne dépend que de la fin du découpage peut avancer en même temps que les autres.
- Écrire dans le rapport les lignes à ajouter à `SUIVI.md`, entre **S47** et **S47.P**, au format des autres lignes.

## Fichiers autorisés

`docs/construction/v1-P14.md`, `suivi/S47.*-*.md` (sauf la porte S47.P), `rapports/S47*.md`.

## Prompt de réalisation

```text
Tu es <ton nom d'IA>, au rôle Concepteur. Tu réalises l'unité S47 « P14 Performance corrélée : découpage » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.

AVANT TOUT
1. git fetch origin. Lis REGLES_AGENTS.md s'il existe, puis la fiche suivi/S47-P14-decoupage.md.
2. Si la branche origin/tache/S47-P14-decoupage existe : reprends-la, relis rapports/S47.md et commence à la première sous-étape R non cochée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
3. Sinon : vérifie dans SUIVI.md, sur main, que S41.P est cochée, puis crée tache/S47-P14-decoupage depuis main.

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S47.md et les cases de suivi/S47-P14-decoupage.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu coches une case seulement quand elle est faite et prouvée. Tu commites et tu pousses après chaque case cochée.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/v1.md, prompt de découpage)
Tu découpes la phase P14 du projet GODOT_DEV_MAPPER en tâches exécutables, au format des fiches de docs/construction/etape-4.md.

ENTRÉES : docs/plan-directeur.md (§3, capacités {CAP} ; §9, porte de la phase) ; docs/construction/v1.md, section P14 ; docs/DECISIONS.md ; docs/spikes/ ; PROJECT_STATE.md (budget consommé, taux de réussite par modèle) ; docs/revues/revue-poc.md.

PRODUIS docs/construction/v1-P14.md :
- objectif, obligations, méthodologie, points de contrôle et cheminement d'amélioration de la phase, précisés par les résultats du POC ;
- de 4 à 12 tâches. Chacune avec : modèle, autonomie, dépendances, fichiers autorisés, pack de contexte, contrôles exécutables dont au moins une contre-épreuve, et prompt de réalisation rempli à partir du prompt universel.

RÈGLES
- Une tâche tient en 1 à 3 h de travail agent et en 1 h de relecture humaine au plus.
- Une tâche qui touche un format persisté, le protocole ou une façade est vérifiée par Opus.
- Les contrats et leurs tests précèdent l'implémentation, comme à l'étape 3. Une tâche qui révise un contrat liste explicitement `docs/CONTRACTS.md`, `contracts/` et `tests/contract/` dans ses fichiers autorisés ; Opus la réalise, Gemini la vérifie, tu la valides.
- Chaque tâche précise les marqueurs de `tests/pending/` qu'elle crée ou supprime, et les scripts de `tools/ci/checks.d/` qu'elle ajoute. Aucune ne modifie `PROJECT_STATE.md` ni `docs/DECISIONS.md`.
- Le total reste dans le budget de la phase ({budget} h humaines). Sinon, tu signales le dépassement et proposes quoi retirer.
- Ne réalise aucune tâche.
- Toute tâche qui produit une explication, une comparaison ou une suggestion inclut un contrôle qui vérifie que chaque affirmation affichée renvoie à une preuve.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

ADAPTATIONS DU MODE AUTONOME
- Budget : traduis les heures humaines de la phase en créneaux d'IA avec le ratio observé au POC (docs/revues/revue-poc.md).
- Pour chaque tâche, crée suivi/S47.<k>-<nom>.md en copiant suivi/_modele-tache.md et en remplissant toutes ses sections : prompt de réalisation complet, sous-étapes R, contrôles, prompt de vérification, sous-étapes V et F.
- Prérequis : S47 pour toute tâche, plus les tâches de la phase dont elle dépend vraiment. Évite que deux tâches indépendantes modifient le même fichier.
- Rôles : réalisation par le développeur, sauf contrat, protocole, façade ou format persisté (concepteur) ; vérification par le vérificateur, sauf ces mêmes sujets (concepteur, ou vérificateur si le concepteur est l'auteur).
- Écris dans le rapport les lignes SUIVI.md à insérer ; le vérificateur les insère à la fusion.
- Contrôle final : python3 suivi/outil.py verifier → OK, une fois les lignes insérées (le vérificateur le relance après insertion).

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Coche dans suivi/S47-P14-decoupage.md les sous-étapes faites et prouvées ; complète rapports/S47.md (sorties, section « Passation ») ; commite ; git push origin tache/S47-P14-decoupage.
- Ne laisse aucune modification non poussée.

FORMAT DE rapports/S47.md
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

- [ ] R0 Prise en charge : `git fetch origin` ; S41.P est cochée dans `SUIVI.md` ; branche `origin/tache/S47-P14-decoupage` absente, ou sans commit depuis deux créneaux, ou dernier verdict REFUSÉE ; créer ou reprendre la branche ; `rapports/S47.md` avec « Statut : EN COURS » et « Auteur » ; commit ; push.
- [ ] R1 Lire la section de la phase, `docs/revues/revue-poc.md`, `PROJECT_STATE.md`, `SUIVI.md` et les rapports des phases précédentes.
- [ ] R2 Écrire `docs/construction/v1-P14.md`.
- [ ] R3 Créer une fiche `suivi/S47.<k>-<nom>.md` par tâche, depuis `suivi/_modele-tache.md`, toutes sections remplies.
- [ ] R4 Écrire dans le rapport les lignes à insérer dans `SUIVI.md`, avec leurs prérequis.
- [ ] R5 Contrôles finaux : chaque fiche créée a toutes ses sections ; « Statut : TERMINÉ » ; commit ; push.

## Prompt de vérification

```text
Tu es <ton nom d'IA>, au rôle Vérificateur, vérificateur indépendant de l'unité S47 « P14 Performance corrélée : découpage » du projet GODOT_DEV_MAPPER.
Tu n'en es pas l'auteur : lis la ligne « Auteur » de rapports/S47.md ; si c'est toi, arrête-toi.
Tu ne modifies aucun fichier de l'unité. Tu écris ton verdict et tu coches les sous-étapes V, sur la branche.

COPIE NEUVE : git fetch origin && git worktree add --detach ../verif-S47-P14-decoupage origin/tache/S47-P14-decoupage
GODOT : même procédure que le prompt de réalisation.

1. PÉRIMÈTRE. git diff --name-only origin/main...origin/tache/S47-P14-decoupage. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S47*.md et suivi/S47-P14-decoupage.md. Tout autre fichier : refus.
2. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : ceux de la fiche.
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
5. COHÉRENCE. Contrat et invariants concernés.
Vérifie le découpage : budget de la phase respecté, chaque tâche avec au moins une contre-épreuve, prérequis réels et sans cycle, aucune paire de tâches indépendantes sur le même fichier. Après insertion des lignes dans SUIVI.md à la fusion : python3 suivi/outil.py verifier → OK.

VERDICT dans rapports/S47-verif-<tentative>.md :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte
Pousse le verdict sur la branche. Si ACCEPTÉE, fais les sous-étapes F de la fiche. Si REFUSÉE, arrête-toi : une IA au rôle de l'auteur reprendra.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge : pas l'auteur ; copie neuve sur `origin/tache/S47-P14-decoupage`.
- [ ] V2 Budget de la phase respecté, ou dépassement signalé avec une proposition de retrait.
- [ ] V3 Chaque fiche créée : toutes les sections, au moins une contre-épreuve, fichiers autorisés précis.
- [ ] V4 Prérequis réels, sans cycle ; tâches indépendantes sans fichier commun.
- [ ] V5 Verdict écrit dans `rapports/S47-verif-<tentative>.md` et poussé.

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `git switch main && git pull --ff-only && git merge --no-ff origin/tache/S47-P14-decoupage -m "Fusion S47 : P14 Performance corrélée : découpage"`.
- [ ] F2 Sur `main` : `GODOT="$B" tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK. Sinon : `git reset --hard ORIG_HEAD`, verdict « REFUSÉE (fusion) » poussé sur la branche, et arrêt de la fusion.
- [ ] F3 Dans `SUIVI.md`, cocher la ligne **S47** et compléter « fait le <date> · auteur <IA> · vérifié par <IA> · <n> créneaux ».
- [ ] F4 Insérer dans `SUIVI.md`, entre **S47** et **S47.P**, les lignes des tâches données par le rapport ; `python3 suivi/outil.py verifier` → OK.
- [ ] F5 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette.
- [ ] F6 Cocher les sous-étapes F de cette fiche ; `git commit` ; `git push origin main` (en cas de refus : `git pull --rebase`, puis push).

## Pour la recette

Rien de propre à cette unité.
