# S16 — T09 Codec et validateur de l'enveloppe

> Fiche d'exécution du mode autonome. Chaque case se coche avec `python3 suivi/outil.py cocher S16 <sous-étape> --ia <n>`, juste après la sous-étape : la commande vérifie l'ordre et l'identité de l'IA, signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite. Règles : `docs/construction/sequence.md`. Avancement : `SUIVI.md` et `suivi/tableau.html`.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 2 (développement) |
| Vérifie | IA 3 (vérification), jamais un auteur de l'unité |
| Piste | 4.A Format, modèle et store : S16 → S17 → S18 (unité 1 sur 3) |
| Commence après | S15 (cochée dans `SUIVI.md`) |
| Indépendante de | S19 |
| Branche | `tache/S16-T09-codec` |
| Fiche de conception | `docs/construction/etape-4.md`, section T09 |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Cette unité est la 1re de la piste 4.A « Format, modèle et store », dont les unités se font à la suite. Les autres pistes de la section (4.B) avancent en même temps, chacune de son côté. Elle attend S15, hors de la piste. S17 l'attendra. Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Encodage dans `addons/godot_dev_mapper_runtime/envelope.gd`, sans dépendance hors du dossier runtime.
- Décodage et validation dans `addons/godot_dev_mapper/protocol/envelope_codec.gd`, avec les codes d'erreur de C-04 (ordre des séquences, taille en octets compris).
- Activer les tests T09 en supprimant leurs marqueurs, sans modifier tests ni fixtures.

## Fichiers autorisés

`addons/godot_dev_mapper_runtime/envelope.gd`, `addons/godot_dev_mapper/protocol/envelope_codec.gd`, les marqueurs T09 de `tests/pending/` (suppression seulement).

Toujours autorisés en plus : `rapports/S16*.md` et les cases de cette fiche (par `cocher`).

## Prompt de réalisation

```text
Tu réalises l'unité S16 « T09 Codec et validateur de l'enveloppe » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.
Réalisation prévue : IA 2 (développement) ; vérification : IA 3 (vérification). Ton numéro d'IA est celui que te donne le prompt de créneau : tu le passes à --ia, et il signe chaque case que tu coches.

AVANT TOUT, depuis ton clone principal du dépôt
1. Lis REGLES_AGENTS.md s'il existe, puis cette fiche : suivi/S16-T09-codec.md.
2. python3 suivi/outil.py prendre S16 --ia <n>
   - « PRISE » ou « REPRISE » : tu es sur la branche tache/S16-T09-codec ; commence à la sous-étape affichée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
   - « REFUSÉ » : l'unité n'est pas pour toi maintenant (déjà prise par une autre IA, S15 non cochée, autre IA prévue) : reviens au prompt de créneau et choisis autre chose.

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
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status. Tu ne pousses jamais avec --force.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.
- Une décision réservée à l'humain (docs/construction/sequence.md §5) : arrêt obligatoire, rien d'autre.

TRACE OBLIGATOIRE, après CHAQUE sous-étape et avant la suivante
1. git add <les fichiers de la sous-étape> (jamais git add -A).
2. python3 suivi/outil.py cocher S16 <sous-étape> --ia <n>
   La commande vérifie l'ordre des cases et ton identité, coche la case dans suivi/S16-T09-codec.md, la signe (IA, date, heure UTC), commite et pousse sur tache/S16-T09-codec.
3. Une sous-étape faite mais non cochée par cette commande est considérée comme non faite : l'IA suivante la refera. Tu ne coches jamais une case à la main.
4. Tu ne modifies jamais SUIVI.md : il ne change qu'à la fusion, sous le verrou de main. Plusieurs IA le lisent en même temps ; aucune ne l'écrit hors de ce verrou.
5. Avant de cocher la dernière sous-étape R : « Statut : TERMINÉ » dans rapports/S16.md, puis git add.
6. Poussée refusée et non rattrapée par la commande : ne force jamais ; git pull --rebase origin tache/S16-T09-codec, puis relance la commande.

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

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche ; après chacune, git add puis python3 suivi/outil.py cocher S16 R<k> --ia <n>.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Chaque sous-étape faite est cochée par `cocher`. Complète rapports/S16.md (sorties, « Passation » en cinq lignes au plus), git add, git commit, git push origin HEAD:tache/S16-T09-codec.
- git status ne montre aucune modification non commitée ; rien ne reste non poussé.

FORMAT DE rapports/S16.md (créé par prendre ; tu le complètes)
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

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher S16 R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre S16 --ia <n>` (prérequis cochés dans `SUIVI.md` : S15 ; branche `tache/S16-T09-codec` créée ou reprise ; `rapports/S16.md` au statut EN COURS) ⟶ cochée par `prendre`
- [ ] R1 Supprimer les marqueurs T09 de `tests/pending/` ; lancer le runner ; coller l'échec. ⟶ cocher S16 R1
- [ ] R2 Implémenter l'encodage dans `envelope.gd`. ⟶ cocher S16 R2
- [ ] R3 Implémenter le décodage et la validation dans `envelope_codec.gd`. ⟶ cocher S16 R3
- [ ] R4 Faire passer les tests sans les modifier. ⟶ cocher S16 R4
- [ ] R5 Prouver l'aller-retour de l'identifiant 9223372036854775807 (T09-c). ⟶ cocher S16 R5
- [ ] R6 Contrôles finaux : T09-a, T09-b, T09-c exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » dans le rapport ⟶ cocher S16 R6

## Prompt de vérification

```text
Tu vérifies l'unité S16 « T09 Codec et validateur de l'enveloppe » du projet GODOT_DEV_MAPPER. Vérification prévue : IA 3 (vérification). Ton numéro d'IA est celui du prompt de créneau. Tu n'es jamais un auteur de l'unité : la commande de prise le contrôle.

PRISE, depuis ton clone principal
python3 suivi/outil.py prendre S16 --ia <n> --verification
- « VÉRIFICATION PRISE » : copie neuve ../verif-S16-T09-codec créée sur origin/tache/S16-T09-codec, verdict EN COURS écrit, V1 cochée. cd ../verif-S16-T09-codec : toute la vérification se fait dans ce dossier.
- « REFUSÉ » : une autre IA vérifie déjà, tu es auteur, ou l'unité n'est pas terminée : reviens au prompt de créneau.
GODOT : même procédure que le prompt de réalisation.
Tu ne modifies aucun fichier de l'unité. Tu écris seulement ton verdict et tes cases V.

TRACE OBLIGATOIRE : après chaque sous-étape V, git add du fichier de verdict, puis python3 suivi/outil.py cocher S16 <V…> --ia <n>. Pour la dernière : --verdict ACCEPTÉE ou --verdict REFUSÉE, identique à la ligne « Verdict » du fichier. Une sous-étape non cochée par cette commande est considérée comme non faite.

1. TRAÇABILITÉ. Chaque case R cochée est signée « — IA n · date » et a son commit sur la branche (git log --oneline origin/main..HEAD). Case cochée sans travail prouvé dans le rapport : refus.
2. PÉRIMÈTRE. git diff --name-only origin/main...HEAD. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S16*.md et suivi/S16-T09-codec.md. Tout autre fichier : refus.
3. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : T09-a, T09-b, T09-c.
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
6. COHÉRENCE. C-04 ; INV-06 pour `envelope.gd`.

VERDICT dans rapports/S16-verif-<tentative>.md (créé par la prise) :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte

SI ACCEPTÉE — FUSION, depuis ton clone principal
1. python3 suivi/outil.py fusionner S16 --ia <n> --godot "$B"
   Elle prend le verrou de main (et attend s'il est pris), fusionne dans ../fusion-S16-T09-codec, lance run_all_checks.sh, coche la ligne dans SUIVI.md et la case F1. Si les contrôles échouent : verdict passé à REFUSÉE, main inchangée, verrou rendu ; arrête-toi sur cette unité.
2. cd ../fusion-S16-T09-codec ; fais les sous-étapes F suivantes de la fiche, et coche chacune : python3 suivi/outil.py cocher S16 F<k> --ia <n> (commit local, sans poussée).
3. python3 suivi/outil.py publier S16 --ia <n> : dernière case cochée, verifier relancé, main poussée, branche supprimée, verrou rendu.
SI REFUSÉE : arrête-toi sur cette unité ; son auteur la reprendra avec prendre.
```

## Sous-étapes de vérification

Dans `../verif-S16-T09-codec`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher S16 V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre S16 --ia <n> --verification` (pas un auteur ; copie neuve `../verif-S16-T09-codec` sur `origin/tache/S16-T09-codec` ; verdict EN COURS) ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R cochée porte une signature « — IA n · date » et un commit sur la branche (`git log --oneline origin/main..HEAD`) ⟶ cocher S16 V2
- [ ] V3 Périmètre : `git diff --name-only origin/main...HEAD` ⊂ fichiers autorisés. ⟶ cocher S16 V3
- [ ] V4.1 Contrôle T09-a relancé, résultat conforme. ⟶ cocher S16 V4.1
- [ ] V4.2 Contrôle T09-b relancé, résultat conforme. ⟶ cocher S16 V4.2
- [ ] V4.3 Contrôle T09-c relancé, résultat conforme. ⟶ cocher S16 V4.3
- [ ] V5 Contre-épreuves (CE) appliquées et détectées, puis annulées. ⟶ cocher S16 V5
- [ ] V6 Contournements cherchés. ⟶ cocher S16 V6
- [ ] V7 Cohérence avec les contrats et les invariants. ⟶ cocher S16 V7
- [ ] V8 Verdict écrit dans `rapports/S16-verif-<tentative>.md` ⟶ cocher S16 V8 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

F1 et la dernière se cochent par `fusionner` et `publier` ; les autres, dans `../fusion-S16-T09-codec`, par `python3 suivi/outil.py cocher S16 F<k> --ia <n>` (commit local).

- [ ] F1 Fusion : `python3 suivi/outil.py fusionner S16 --ia <n> --godot "$B"` : verrou de `main`, fusion `--no-ff` dans `../fusion-S16-T09-codec`, `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK s'il existe (sinon fusion annulée et verdict passé à REFUSÉE), ligne **S16** cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette ⟶ cocher S16 F2
- [ ] F3 Publication : `python3 suivi/outil.py publier S16 --ia <n>` (verifier OK, `main` poussée, branche `tache/S16-T09-codec` supprimée, verrou rendu) ⟶ cochée par `publier`

## Pour la recette

Rien de propre à cette unité.
