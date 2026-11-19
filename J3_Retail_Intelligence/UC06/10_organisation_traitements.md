# Étape 10 - Organisation des traitements

Afin de faciliter la compréhension, la maintenance et la reproduction du pipeline Data Engineering, les traitements du projet Retail Intelligence Platform sont organisés selon les différentes étapes de transformation des données.

L'organisation retenue suit une architecture en plusieurs couches : Bronze, Silver, Silver transformé et Gold. Chaque couche possède un rôle précis et produit des données destinées à l'étape suivante.

#### A. Organisation générale du projet

Les traitements et les données sont répartis selon l'organisation suivante :

```text
retail-intelligence/tp3/
│
├── data/
│   ├── bronze/
│   │   └── Données sources brutes
│   │
│   ├── silver/
│   │   └── Données nettoyées et contrôlées
│   │
│   ├── silver-transformed/
│   │   ├── store_sales/
│   │   ├── inventory/
│   │   ├── sales_by_store/
│   │   ├── sales_by_store_date/
│   │   ├── sales_by_item_date/
│   │   ├── inventory_by_item_date/
│   │   └── sales_inventory_by_item_date/
│   │
│   └── gold/
│       └── sales_performance_by_store/
│
├── notebooks/
│   ├── 01_verification_environnement.ipynb
│   └── 02_inventaire_sources.ipynb
│
│
├── scripts/
│   ├── etape4_nettoyage.py
│   ├── etape5_6_transformations_silver.py
│   ├── etape7_gold.py
│   ├── etape9_quality_control.py
│   └── quality_check_gold.py
│
└── reports/
    └── quality/
        └── quality_report_gold.csv
```

Cette arborescence représente l'organisation logique du projet.

#### B. Séparation des responsabilités

Les traitements sont organisés de manière à séparer autant que possible les différentes responsabilités techniques.

| Élément | Responsabilité | Application dans le projet |
|---|---|---|
| Paramètres | Définir les configurations nécessaires aux traitements | Noms des jeux de données, chemins, paramètres Spark |
| Chemins d'entrée et de sortie | Centraliser les emplacements des données | Répertoires Bronze, Silver, Silver transformé et Gold |
| Lecture | Charger les données et leurs schémas | Lecture des fichiers sources DAT et des fichiers Parquet |
| Transformations | Nettoyer, enrichir et agréger les données | Traitements Silver et Silver transformé |
| Contrôles qualité | Vérifier la cohérence et la validité des résultats | Contrôles Silver, réconciliations Gold et script `quality_check_gold.py` |
| Écritures | Enregistrer les résultats dans les couches correspondantes | Écriture des jeux Silver, Silver transformés et Gold en Parquet |
| Journaux et résultats | Conserver les informations d'exécution et les bilans | Logs Spark et rapport `quality_report_gold.csv` |

Cette séparation permet de distinguer les opérations de lecture, de transformation, de validation et d'écriture. Elle facilite également l'identification de l'origine d'une anomalie lorsqu'un contrôle échoue.

#### C. Ordre d'exécution des traitements

Le pipeline suit un ordre d'exécution logique, chaque étape dépendant des résultats de la précédente.

1. **Bronze – Ingestion des données**

   Les fichiers sources sont récupérés et placés dans la couche Bronze. Cette étape conserve les données dans leur état initial afin de disposer d'une base de travail identifiable.

2. **Silver – Nettoyage et contrôle**

   Les données Bronze sont lues, structurées et contrôlées. Les anomalies sont identifiées et les enregistrements non conformes sont, lorsque la règle le prévoit, mis en quarantaine.

3. **Silver transformé – Enrichissement et agrégation**

   Les données Silver sont utilisées pour produire les jeux analytiques. Les transformations comprennent notamment les agrégations par magasin, par date et par article, ainsi que la préparation des données de ventes et de stocks.

4. **Gold – Production du jeu métier**

   Le jeu `sales_performance_by_store` est construit à partir de `sales_by_store`. Il enrichit les mesures commerciales avec un classement des magasins, un indicateur du meilleur chiffre d'affaires et la part de chiffre d'affaires de chaque magasin.

5. **Contrôle qualité – Vérification des résultats**

   Le script `quality_check_gold.py` lit le jeu Gold et effectue les contrôles de complétude, d'unicité, de types, de cohérence, de volume et de réconciliation. Il génère un rapport CSV.

6. **Exploitation des résultats**

   Les jeux Parquet produits peuvent ensuite être relus par Spark et exploités pour les analyses métier.

#### D. Organisation des lectures et écritures

Les traitements utilisent les chemins de données correspondant à leur couche.

| Couche | Entrée principale | Sortie |
|---|---|---|
| Bronze | Fichiers sources TPCx-BB | Données brutes dans `data/bronze/` |
| Silver | Données Bronze | Données nettoyées dans `data/silver/` |
| Silver transformé | Données Silver | Jeux analytiques dans `data/silver-transformed/` |
| Gold | `sales_by_store/` | `sales_performance_by_store/` |
| Contrôle qualité | `data/gold/sales_performance_by_store/` et sources de comparaison | `reports/quality/quality_report_gold.csv` |

Les jeux analytiques sont enregistrés en Parquet, avec compression Snappy pour le jeu Gold étudié.

Les écritures utilisent des répertoires de destination dédiés. Le mode `overwrite` est utilisé avec précaution afin de remplacer uniquement les résultats générés par les traitements, sans modifier les données sources.

#### E. Organisation des contrôles et des résultats

Les contrôles qualité sont réalisés au plus près des traitements concernés, puis regroupés dans un bilan complémentaire pour le jeu Gold.

Les résultats connus comprennent notamment :

- les volumes de données lues, conservées et mises en quarantaine dans Silver
- les vérifications de granularité et de clés avant les jointures 
- les réconciliations des mesures entre Silver transformé et Gold 
- la comparaison des données avant et après écriture Parquet 
- le rapport qualité Gold comportant 44 contrôles conformes, aucun échec et un avertissement relatif à l'intégrité référentielle

Cette organisation permet de conserver une trace des contrôles effectués et de distinguer les anomalies détectées des limites des vérifications disponibles.

#### F. Bilan de l'organisation

Les traitements du projet suivent une chaîne de transformation cohérente, depuis les fichiers sources jusqu'au jeu Gold destiné à l'analyse métier.

La séparation par couches facilite la compréhension du rôle de chaque traitement et permet de retrouver les données produites à chaque étape.

La démarche repose sur les principes suivants :

- séparer les données brutes des données transformées 
- isoler les traitements de nettoyage, d'agrégation et d'enrichissement 
- utiliser des chemins de sortie distincts 
- conserver les résultats analytiques au format Parquet 
- associer des contrôles qualité aux principales transformations 
- produire des journaux et des rapports permettant de suivre les exécutions

L'organisation constitue une base pour améliorer progressivement la modularité et la reproductibilité du pipeline.