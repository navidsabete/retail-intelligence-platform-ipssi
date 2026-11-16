# Projet fil rouge - Retail Intelligence Platform (IPSSI)

# J1

## Présentation

Ce dépôt regroupe les livrables réalisés lors de la première journée du projet Retail Intelligence, dans le cadre de l'UC-01.

Il rassemble les travaux de cadrage métier, de définition des indicateurs, d'exploration des sources de données, de qualification et d'analyse des limites du jeu de données TPCx-BB.

## Organisation du dépôt

```text
J1_Retail_Intelligence/
├── README.md
└── 01_UC01_besoin_exploration/
    ├── UC01_cadrage_metier.pdf
    ├── UC01_questions_decisionnelles.pdf
    ├── UC01_dictionnaire_KPI.xlsx
    ├── UC01_inventaire_sources.xlsx
    ├── UC01_qualification_donnees.pdf
    ├── UC01_limites_et_hypotheses.pdf
    └── preuves/
```

## Présentation des livrables

| Livrable | Contenu |
|---|---|
| `UC01_cadrage_metier.pdf` | Profils métier, responsabilités et besoins identifiés. |
| `UC01_questions_decisionnelles.pdf` | Questions métier, décisions associées et niveaux de priorité. |
| `UC01_dictionnaire_KPI.xlsx` | Définition des indicateurs : formules, unités, filtres, périodicité, sources et données éventuellement manquantes. |
| `UC01_inventaire_sources.xlsx` | Recensement des fichiers, formats, volumes et caractéristiques observées. |
| `UC01_qualification_donnees.pdf` | Analyse de la structure, de la qualité des données, des anomalies et des relations candidates entre tables. |
| `UC01_limites_et_hypotheses.pdf` | Prise de recul sur les besoins couverts, les KPI exploitables, les hypothèses, les limites et les données complémentaires nécessaires. |
| `preuves/` | Rapports et éléments permettant de justifier les constats présentés dans les livrables. |

## Périmètre technique

L'exploration porte sur les répertoires `data/` et `data_refresh/` du jeu de données synthétique TPCx-BB.

Les deux répertoires sont étudiés séparément. Leurs contenus ne sont pas fusionnés automatiquement, car les fichiers de rafraîchissement peuvent correspondre à des ajouts, des mises à jour ou à un périmètre différent.

Les fichiers `.DAT` utilisent le séparateur `|` et ne comportent pas d'en-têtes détectés. L'identification des colonnes repose donc provisoirement sur leur position. Les noms et significations métier doivent être confirmés à l'aide du dictionnaire de données.

## Méthode et traçabilité

L'analyse s'appuie sur un inventaire automatisé, une description des colonnes et un rapport d'anomalies.

Les constats présentés dans les livrables doivent être interprétés selon leur niveau de validation :

- **Observé :** information directement relevée dans les fichiers ou les rapports.
- **Estimé :** résultat produit par une détection ou une classification automatique.
- **Hypothèse :** interprétation cohérente avec le modèle TPCx-BB, mais non démontrée.
- **À confirmer :** information nécessitant une vérification complémentaire.
- **Non vérifié :** contrôle qui n'a pas encore été réalisé.

Les relations entre tables sont considérées comme candidates tant que les clés, les doublons et les références sans correspondance n'ont pas été contrôlés par des jointures.

Les rapports d'analyse et les éventuels extraits utiles sont conservés dans `UC01_preuves/` afin de faciliter la traçabilité des résultats.