# Sxx.k — <titre de la tâche>

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
