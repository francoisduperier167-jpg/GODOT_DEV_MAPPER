# Sxx.cN — Correction demandée par la porte Sxx

> Fiche créée par `python3 suivi/outil.py correction` quand un point de contrôle de la porte Sxx est KO. Chaque case se coche avec `python3 suivi/outil.py cocher Sxx.cN <sous-étape> --ia <n>`, juste après la sous-étape : la commande signe la case (IA, date, heure), commite et pousse.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 2 (développement) |
| Vérifie | IA 3 (vérification), jamais un auteur de l'unité |
| Piste | celle de la porte Sxx, juste avant elle |
| Commence après | rien : peut commencer tout de suite |
| Branche | `tache/Sxx.cN-correction` |
| Unité fautive | Syy |
| Correction | <correction attendue> |

## Ce qu'il faut faire

- Corriger le défaut relevé par la porte Sxx (voir `rapports/Sxx.md`), dans les fichiers autorisés de l'unité fautive Syy.
- Rejouer les contrôles de l'unité fautive, puis le point de contrôle KO de la porte.

## Fichiers autorisés

Les fichiers autorisés de la fiche de Syy. Toujours autorisés en plus : `rapports/Sxx.cN*.md` et les cases de cette fiche.

## Prompt de réalisation

```text
Tu corriges le défaut relevé par la porte Sxx du projet GODOT_DEV_MAPPER. Réalisation prévue : IA 2. Ton numéro d'IA est celui du prompt de créneau.
1. python3 suivi/outil.py prendre Sxx.cN --ia <n>   (code non nul : l'unité n'est pas pour toi maintenant)
2. Lis rapports/Sxx.md (point KO, correction attendue) et la fiche de Syy dans suivi/ : ses règles, son bloc GODOT, ses fichiers autorisés et ses contrôles s'appliquent.
3. Fais la plus petite correction qui rend le point OK sans affaiblir aucun test. Colle les sorties des contrôles dans rapports/Sxx.cN.md.
TRACE OBLIGATOIRE : après chaque sous-étape, git add des fichiers de la sous-étape, puis python3 suivi/outil.py cocher Sxx.cN <sous-étape> --ia <n>. Une sous-étape non cochée par cette commande est considérée comme non faite.
```

## Sous-étapes de réalisation

- [ ] R0 Prise en charge par `prendre` : branche `tache/Sxx.cN-correction`, rapport « EN COURS » ⟶ cochée par `prendre`
- [ ] R1 Cause du point KO établie et écrite dans le rapport ⟶ cocher Sxx.cN R1
- [ ] R2 Correction faite dans les fichiers autorisés de Syy ⟶ cocher Sxx.cN R2
- [ ] R3 Contrôles de Syy et point KO de la porte rejoués → OK, sorties collées ; « Statut : TERMINÉ » ⟶ cocher Sxx.cN R3

## Prompt de vérification

```text
Tu vérifies la correction Sxx.cN du projet GODOT_DEV_MAPPER. Vérification prévue : IA 3. Tu n'es jamais un auteur de l'unité.
1. python3 suivi/outil.py prendre Sxx.cN --ia <n> --verification, puis cd dans la copie neuve indiquée.
2. Périmètre : fichiers de Syy seulement. Relance les contrôles de Syy et le point KO de la porte Sxx.
3. Verdict dans rapports/Sxx.cN-verif-<tentative>.md ; dernière case : cocher Sxx.cN V4 --ia <n> --verdict ACCEPTÉE (ou REFUSÉE).
4. Si ACCEPTÉE : depuis ton clone principal, python3 suivi/outil.py fusionner Sxx.cN --ia <n> (Godot : la commande le trouve seule, par --godot, $GODOT, le cache du bloc GODOT ou tools/ci/fetch_godot.sh), puis, dans la copie de fusion, les cases F, puis python3 suivi/outil.py publier Sxx.cN --ia <n>. La porte Sxx redevient alors disponible : elle sera rejouée.
TRACE OBLIGATOIRE : python3 suivi/outil.py cocher Sxx.cN <sous-étape> --ia <n> après chaque sous-étape.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge par `prendre --verification` : pas un auteur ; copie neuve ⟶ cochée par `prendre`
- [ ] V2 Périmètre : fichiers de Syy seulement ⟶ cocher Sxx.cN V2
- [ ] V3 Contrôles relancés ; point KO de la porte OK ⟶ cocher Sxx.cN V3
- [ ] V4 Verdict écrit dans `rapports/Sxx.cN-verif-<tentative>.md` ⟶ cocher Sxx.cN V4 --verdict ACCEPTÉE ou REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `fusionner Sxx.cN --ia <n>` depuis le clone principal : verrou de `main`, fusion, contrôles sur `main` avec Godot, ligne cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 `PROJECT_STATE.md` : mesures de l'unité ⟶ cocher Sxx.cN F2
- [ ] F3 `publier` : `main` poussé, branche supprimée, verrou rendu ⟶ cochée par `publier`

## Pour la recette

Rien de propre à cette unité.
