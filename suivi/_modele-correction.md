# Sxx.cN — Correction demandée par la porte Sxx

> Fiche créée par le vérificateur d'une porte quand un point de contrôle est KO.

| Champ | Valeur |
| --- | --- |
| Réalise | <rôle de l'unité fautive> |
| Vérifie | <le vérificateur de l'unité fautive> |
| Commence après | rien |
| Branche | `tache/Sxx.cN-<nom>` |
| Unité fautive | <Syy> |
| Point KO | <PCx.y : commande, attendu, obtenu> |

## Ce qu'il faut faire

- Corriger le défaut qui fait échouer <PCx.y>, dans les fichiers autorisés de l'unité fautive.
- Rejouer les contrôles de l'unité fautive, puis le point de contrôle de la porte.

## Prompt de réalisation

```text
Tu corriges le défaut relevé par la porte Sxx du projet GODOT_DEV_MAPPER. Lis rapports/Sxx.md (point KO, correction attendue) et la fiche de l'unité fautive suivi/<Syy>.md : ses règles, ses fichiers autorisés et ses contrôles s'appliquent. Fais la plus petite correction qui rend le point OK sans affaiblir aucun test. Exécute les contrôles de l'unité fautive, puis le point de la porte, et colle leurs sorties dans rapports/Sxx.cN.md.
```

## Sous-étapes de réalisation

- [ ] R0 Prise en charge ; rapport « EN COURS » ; push.
- [ ] R1 Cause du point KO établie et écrite.
- [ ] R2 Correction faite.
- [ ] R3 Contrôles de l'unité fautive et point de la porte → OK ; « Statut : TERMINÉ » ; push.

## Sous-étapes de vérification

- [ ] V1 Pas l'auteur ; copie neuve.
- [ ] V2 Périmètre : fichiers de l'unité fautive seulement.
- [ ] V3 Contrôles relancés ; point de la porte OK.
- [ ] V4 Verdict écrit et poussé.

## Sous-étapes de fusion

- [ ] F1 Fusion, `run_all_checks.sh` sur `main`, ligne cochée dans `SUIVI.md`, push. La porte Sxx est ensuite rejouée.
