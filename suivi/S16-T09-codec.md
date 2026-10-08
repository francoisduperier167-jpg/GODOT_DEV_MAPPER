# S16 — T09 Codec et validateur de l'enveloppe

> Fiche d'exécution du mode autonome. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse : une autre IA doit pouvoir reprendre à la première case non cochée. Règles : `docs/construction/sequence.md`. Avancement global : `SUIVI.md`.

| Champ | Valeur |
| --- | --- |
| Réalise | Développeur |
| Vérifie | Vérificateur (jamais l'auteur) |
| Commence après | S15 (cochées dans `SUIVI.md`) |
| Indépendante de | S19 |
| Branche | `tache/S16-T09-codec` |
| Fiche de conception | `docs/construction/etape-4.md`, section T09 |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité elle-même peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Encodage dans `addons/godot_dev_mapper_runtime/envelope.gd`, sans dépendance hors du dossier runtime.
- Décodage et validation dans `addons/godot_dev_mapper/protocol/envelope_codec.gd`, avec les codes d'erreur de C-04 (ordre des séquences, taille en octets compris).
- Activer les tests T09 en supprimant leurs marqueurs, sans modifier tests ni fixtures.

## Fichiers autorisés

`addons/godot_dev_mapper_runtime/envelope.gd`, `addons/godot_dev_mapper/protocol/envelope_codec.gd`, les marqueurs T09 de `tests/pending/` (suppression seulement).

Toujours autorisés en plus : `rapports/S16*.md` et les cases de cette fiche.

## Prompt de réalisation

```text
Tu es <ton nom d'IA>, au rôle Développeur. Tu réalises l'unité S16 « T09 Codec et validateur de l'enveloppe » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.

AVANT TOUT
1. git fetch origin. Lis REGLES_AGENTS.md s'il existe, puis la fiche suivi/S16-T09-codec.md.
2. Si la branche origin/tache/S16-T09-codec existe : reprends-la, relis rapports/S16.md et commence à la première sous-étape R non cochée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
3. Sinon : vérifie dans SUIVI.md, sur main, que S15 est cochée, puis crée tache/S16-T09-codec depuis main.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S16.md et les cases de suivi/S16-T09-codec.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu coches une case seulement quand elle est faite et prouvée. Tu commites et tu pousses après chaque case cochée.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-4.md, T09)
Tu réalises la tâche T09 du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.
CONTEXTE : docs/CONTRACTS.md, section C-04, y compris sa table des codes d'erreur ; contracts/schemas/envelope.v1.schema.json ; tests/contract/test_c04_envelope.gd et ses fixtures.
OBJECTIF : implémenter le codec de l'enveloppe C-04 v1.
- L'encodage va dans addons/godot_dev_mapper_runtime/envelope.gd, qui ne dépend de rien hors du dossier runtime.
- Le décodage et la validation vont dans addons/godot_dev_mapper/protocol/envelope_codec.gd. Le validateur renvoie les codes d'erreur du contrat, y compris les règles sémantiques : ordre des séquences, taille en octets.
DÉROULÉ
1. Supprime les marqueurs T09 de tests/pending/ ; lance le runner et montre l'échec.
2. Implémente jusqu'à faire passer ces tests, sans les modifier.
CONTRÔLES
T09-a  godot --headless --path . -s res://tests/run_all.gd ; echo $?   → 0, aucun marqueur T09 restant
T09-b  GODOT=<binaire> tools/ci/run_all_checks.sh ; echo $?            → 0
T09-c  Dans le rapport : aller-retour de l'identifiant 9223372036854775807 sans perte, avec la sortie du test qui le prouve
CONTRE-ÉPREUVE (CE) pour le vérificateur : passer la limite d'événements par lot à 257 → test_c04_envelope échoue.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

ADAPTATIONS DU MODE AUTONOME
- Aucune : suis le travail technique tel quel.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Coche dans suivi/S16-T09-codec.md les sous-étapes faites et prouvées ; complète rapports/S16.md (sorties, section « Passation ») ; commite ; git push origin tache/S16-T09-codec.
- Ne laisse aucune modification non poussée.

FORMAT DE rapports/S16.md
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

- [ ] R0 Prise en charge : `git fetch origin` ; S15 est cochée dans `SUIVI.md` ; branche `origin/tache/S16-T09-codec` absente, ou sans commit depuis deux créneaux, ou dernier verdict REFUSÉE ; créer ou reprendre la branche ; `rapports/S16.md` avec « Statut : EN COURS » et « Auteur » ; commit ; push.
- [ ] R1 Supprimer les marqueurs T09 de `tests/pending/` ; lancer le runner ; coller l'échec.
- [ ] R2 Implémenter l'encodage dans `envelope.gd`.
- [ ] R3 Implémenter le décodage et la validation dans `envelope_codec.gd`.
- [ ] R4 Faire passer les tests sans les modifier.
- [ ] R5 Prouver l'aller-retour de l'identifiant 9223372036854775807 (T09-c).
- [ ] R6 Contrôles finaux : T09-a, T09-b, T09-c exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » ; commit ; push.

## Prompt de vérification

```text
Tu es <ton nom d'IA>, au rôle Vérificateur, vérificateur indépendant de l'unité S16 « T09 Codec et validateur de l'enveloppe » du projet GODOT_DEV_MAPPER.
Tu n'en es pas l'auteur : lis la ligne « Auteur » de rapports/S16.md ; si c'est toi, arrête-toi.
Tu ne modifies aucun fichier de l'unité. Tu écris ton verdict et tu coches les sous-étapes V, sur la branche.

COPIE NEUVE : git fetch origin && git worktree add --detach ../verif-S16-T09-codec origin/tache/S16-T09-codec
GODOT : même procédure que le prompt de réalisation.

1. PÉRIMÈTRE. git diff --name-only origin/main...origin/tache/S16-T09-codec. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S16*.md et suivi/S16-T09-codec.md. Tout autre fichier : refus.
2. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : T09-a, T09-b, T09-c.
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
5. COHÉRENCE. C-04 ; INV-06 pour `envelope.gd`.

VERDICT dans rapports/S16-verif-<tentative>.md :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte
Pousse le verdict sur la branche. Si ACCEPTÉE, fais les sous-étapes F de la fiche. Si REFUSÉE, arrête-toi : une IA au rôle de l'auteur reprendra.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge : pas l'auteur ; copie neuve `../verif-S16-T09-codec` sur `origin/tache/S16-T09-codec`.
- [ ] V2 Périmètre : `git diff --name-only origin/main...origin/tache/S16-T09-codec` ⊂ fichiers autorisés.
- [ ] V3.1 Contrôle T09-a relancé, résultat conforme.
- [ ] V3.2 Contrôle T09-b relancé, résultat conforme.
- [ ] V3.3 Contrôle T09-c relancé, résultat conforme.
- [ ] V4 Contre-épreuves (CE) appliquées et détectées, puis annulées.
- [ ] V5 Contournements cherchés.
- [ ] V6 Cohérence avec les contrats et les invariants.
- [ ] V7 Verdict écrit dans `rapports/S16-verif-<tentative>.md` et poussé.

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `git switch main && git pull --ff-only && git merge --no-ff origin/tache/S16-T09-codec -m "Fusion S16 : T09 Codec et validateur de l'enveloppe"`.
- [ ] F2 Sur `main` : `GODOT="$B" tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK. Sinon : `git reset --hard ORIG_HEAD`, verdict « REFUSÉE (fusion) » poussé sur la branche, et arrêt de la fusion.
- [ ] F3 Dans `SUIVI.md`, cocher la ligne **S16** et compléter « fait le <date> · auteur <IA> · vérifié par <IA> · <n> créneaux ».
- [ ] F4 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette.
- [ ] F5 Cocher les sous-étapes F de cette fiche ; `git commit` ; `git push origin main` (en cas de refus : `git pull --rebase`, puis push).

## Pour la recette

Rien de propre à cette unité.
