# Sxx.k — <titre de la tâche>

> Fiche d'exécution du mode autonome, créée par le découpage de la phase. Chaque case se coche avec `python3 suivi/outil.py cocher Sxx.k <sous-étape> --ia <n>`, juste après la sous-étape : la commande signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite.

| Champ | Valeur |
| --- | --- |
| Réalise | <IA 1 (conception), IA 2 (développement) ou IA 3 (vérification)> |
| Vérifie | <IA n (rôle)>, jamais un auteur de l'unité |
| Piste | <celle de la phase Sxx ; sous-piste : les tâches de la phase qui s'enchaînent> |
| Commence après | <Sxx, et les tâches de la phase dont elle dépend vraiment> |
| Indépendante de | <tâches de la phase sans dépendance ni fichier commun> |
| Branche | `tache/Sxx.k-<nom>` |
| Fiche de conception | `docs/construction/<mvp|v1>-<Px>.md`, section <tâche> |
| Estimation | <n> créneau(x) |

## Ce qu'il faut faire

- <résultat attendu, précis, vérifiable>

## Fichiers autorisés

<liste exacte>. Toujours autorisés en plus : `rapports/Sxx.k*.md` et les cases de cette fiche (par `cocher`).

## Contrôles propres à cette fiche

- `Sxx.k-a` : `<commande>` → <attendu>
- (CE) <sabotage> : <contrôle> échoue ; annuler.

## Prompt de réalisation

```text
<Copier l'en-tête (avec PRISE par `prendre`), le bloc GODOT, les RÈGLES NON NÉGOCIABLES, la TRACE OBLIGATOIRE et la FIN DE CRÉNEAU d'une fiche de l'étape 4 (par exemple suivi/S17-T10-modele.md), en remplaçant l'identifiant, la branche et le titre ; puis écrire le travail technique complet : contexte à lire, objectif, fichiers, déroulé, contrôles, contre-épreuves.>
```

## Sous-étapes de réalisation

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher Sxx.k R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre Sxx.k --ia <n>` ⟶ cochée par `prendre`
- [ ] R1 <étape> ⟶ cocher Sxx.k R1
- [ ] R2 Contrôles finaux ; « Statut : TERMINÉ » dans le rapport ⟶ cocher Sxx.k R2

## Prompt de vérification

```text
<Copier le prompt de vérification d'une fiche de l'étape 4 et l'adapter : identifiant, branche, contrôles, cohérence. Il garde la PRISE par `prendre --verification`, la TRACE OBLIGATOIRE et la FUSION par `fusionner` puis `publier`.>
```

## Sous-étapes de vérification

Dans `../verif-Sxx.k-<nom>`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher Sxx.k V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre Sxx.k --ia <n> --verification` ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R signée, avec son commit ⟶ cocher Sxx.k V2
- [ ] V3 Périmètre ⟶ cocher Sxx.k V3
- [ ] V4.1 Contrôle <id> relancé ⟶ cocher Sxx.k V4.1
- [ ] V5 Contre-épreuves ⟶ cocher Sxx.k V5
- [ ] V6 Contournements ⟶ cocher Sxx.k V6
- [ ] V7 Cohérence ⟶ cocher Sxx.k V7
- [ ] V8 Verdict écrit ⟶ cocher Sxx.k V8 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 Fusion : `python3 suivi/outil.py fusionner Sxx.k --ia <n> --godot "$B"` ⟶ cochée par `fusionner`
- [ ] F2 `PROJECT_STATE.md` : mesures, liste de recette ⟶ cocher Sxx.k F2
- [ ] F3 Publication : `python3 suivi/outil.py publier Sxx.k --ia <n>` ⟶ cochée par `publier`

## Pour la recette

Rien de propre à cette unité.
