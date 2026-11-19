# Projet fil rouge – Retail Intelligence Platform (IPSSI)

# J3

## Présentation

Ce dépôt regroupe les livrables réalisés lors de la troisième journée du projet Retail Intelligence Platform, dans le cadre de UC-06. Cette troisième journée s'inscrit dans la continuité des travaux réalisés lors du J1 et du J2.

- **UC-06 :** préparation des données avec Python et PySpark, structuration des couches Bronze, Silver et Gold, transformations analytiques, contrôles qualité et stockage au format Parquet.

L'objectif du J3 est de construire une chaîne de traitement permettant de passer des fichiers sources bruts à des jeux de données structurés et exploitables pour l'analyse métier.

## Organisation du dépôt

```text
J3_Retail_Intelligence/
├── README.md
│
├── UC06/
│   ├── 01_verification_environnement.md
│   ├── 02_inventaire_sources.md
│   ├── 03_exploration_donnees_pyspark.md
│   ├── 04_regles_nettoyage.md
│   ├── 05_bilan_execution_traitement_nettoyage.md
│   ├── 06_transformations_silver.md
│   ├── 07_jeu_gold.md
│   ├── 08_comparaison_format.md
│   ├── 09_controle_qualite.md
│   └── 10_organisation_traitements.md
│
└── retail-intelligence/tp3/
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
    ├── scripts/
    │   ├── etape4_nettoyage
    │   ├── etape5_6_transformations_silver.py
    │   ├── etape7_gold.py
    │   ├── etape9_quality_control.py
    │   └── quality_check_gold.py
    │
    └── reports/
        └── quality/
            └── quality_report_gold.csv
```

Les dossiers `data/` regroupent les différentes couches de données produites pendant les traitements. Les dossiers `notebooks/` et `scripts/` accueillent les éléments de manipulation, de transformation et de contrôle. Le dossier `reports/quality/` conserve les rapports de validation.

## Périmètre technique

L'environnement de travail repose sur Ubuntu 24.04.5 LTS et utilise Python, Java et Spark pour les traitements.

### Versions constatées

Les versions relevées dans l'environnement sont les suivantes :

| Composant | Commande de vérification | Version constatée |
|---|---|---|
| Python | `python3 --version` | Python 3.12.3 |
| Java | `java -version` | OpenJDK 21.0.13 |
| PySpark | `pyspark --version` | 4.3.0 |
| Apache Spark | `spark-submit --version` | 4.3.0 |

Les commandes suivantes permettent de vérifier les versions avant de reproduire les traitements :

```bash
python3 --version
java -version
pyspark --version
spark-submit --version
```


## Prérequis

Pour exécuter les traitements du J3, les éléments suivants sont nécessaires :

- Un environnement Ubuntu 24.04.5 LTS ou un environnement Linux compatible.
- Python 3.12.3.
- OpenJDK 21.0.13.
- Apache Spark 4.3.0.
- PySpark 4.3.0.
- Les fichiers sources du jeu de données synthétique TPCx-BB.
- Un espace disque suffisant pour conserver les données sources et les différentes couches produites.

Les chemins de données sont définis par rapport au répertoire du traitement des données :

```text
~/retail-intelligence/tp3/
```

Il est nécessaire de disposer des droits de lecture et d'écriture sur ce répertoire.


### Environnement virtuel Python

Le projet utilise un environnement virtuel Python afin d'isoler ses dépendances de celles installées sur le système.

L'environnement virtuel est créé dans le répertoire du traitement de données sous le nom `retail_intel_tp3_venv/`.

Depuis le répertoire `~/retail-intelligence/tp3/`, les commandes suivantes permettent de le créer et de l'activer :

```bash
# Se placer dans le répertoire du traitement de données
cd ~/retail-intelligence/tp3/

# Créer l'environnement virtuel
python3 -m venv retail_intel_tp3_venv

# Activer l'environnement virtuel
source retail_intel_tp3_venv/bin/activate
```

Une fois activé, le nom `(retail_intel_tp3_venv)` apparaît au début de l'invite de commande.

Pour vérifier que Python utilise bien l'environnement virtuel :

```bash
which python
python --version
```

Pour mettre à jour l'outil d'installation des dépendances :

```bash
python -m pip install --upgrade pip
```

Pour consulter les dépendances installées dans l'environnement :

```bash
pip list
```

Pour quitter l'environnement virtuel :

```bash
deactivate
```

L'environnement virtuel permet d'isoler les bibliothèques Python du projet. Java et Spark restent des composants installés et configurés au niveau du système.

## Emplacement et organisation des données

Les données utilisées proviennent du jeu synthétique TPCx-BB.

Les fichiers sources sont initialement fournis au format DAT, avec des champs séparés par le caractère `|` et sans ligne d'en-tête.

Deux fichiers principaux ont été utilisés pour les traitements :

| Fichier source | Volume observé |
|---|---:|
| `store_sales.dat` | 667 579 lignes |
| `inventory.dat` | 23 255 100 lignes |

Les données sont organisées selon une logique de couches :

- **Bronze :** conservation des données sources brutes dans leur format initial.
- **Silver :** données lues, typées et contrôlées, avec identification des lignes mises en quarantaine.
- **Silver-transformed :** jeux de données transformés et agrégés pour préparer les analyses.
- **Gold :** données enrichies et orientées vers un besoin analytique ou métier.

Les couches Silver et suivantes sont stockées au format Parquet.

## Paramètres nécessaires

Les traitements reposent sur plusieurs paramètres techniques et fonctionnels :

| Paramètre | Valeur ou description |
|---|---|
| Répertoire du traitement de données | `~/retail-intelligence/tp3/` |
| Répertoire Bronze | `data/bronze/` |
| Répertoire Silver | `data/silver/` |
| Répertoire Silver transformé | `data/silver-transformed/` |
| Répertoire Gold | `data/gold/` |
| Répertoire des rapports qualité | `reports/quality/` |
| Séparateur des fichiers sources | `|` |
| Format des données transformées | Parquet |
| Compression Parquet Gold | Snappy |

Les chemins d'entrée et de sortie doivent correspondre à l'emplacement réel des données sur la machine.

Les traitements doivent également conserver les paramètres de lecture adaptés aux fichiers DAT, notamment le séparateur et les schémas de données attendus.

Les règles de nettoyage et les agrégations doivent rester cohérentes avec la granularité de chaque jeu de données.

## Ordre d'exécution des traitements

La chaîne de traitement suit l'ordre logique suivant :

```text
Fichiers sources TPCx-BB
        |
        v
      BRONZE
Données brutes conservées
        |
        v
      SILVER
Nettoyage et contrôles
        |
        v
SILVER-TRANSFORMED
Transformations et agrégations
        |
        v
       GOLD
Enrichissement analytique
        |
        v
Contrôles qualité et rapport
```

### 1. Vérification de l'environnement

Le notebook `01_verification_environnement.ipynb` permet de vérifier l'environnement technique et les composants nécessaires aux traitements.

### 2. Inventaire des sources

Le notebook `02_inventaire_sources.ipynb` permet de caractériser les fichiers sources avant leur traitement : volumes, structure et organisation des données.

### 3. Préparation de la couche Bronze

Les fichiers sources sont déposés dans `data/bronze/` afin de conserver une première copie de travail des données brutes.

### 4. Nettoyage et constitution de la couche Silver

Le traitement de nettoyage prépare les données pour leur exploitation analytique.

Les principales opérations comprennent :
- la lecture des fichiers DAT 
- l'application des schémas 
- le contrôle des types 
- l'identification des valeurs nulles 
- l'identification des doublons candidats 
- la mise en quarantaine des lignes non conformes selon les règles retenues 
- la conservation des anomalies nécessitant une interprétation métier

Les résultats sont stockés dans `data/silver/`.

### 5. Transformations Silver

Le script `etape5_6_transformations_silver.py` réalise les transformations et agrégations nécessaires à la constitution des jeux de données analytiques.

Les jeux produits sont les suivants :

| Jeu de données | Granularité |
|---|---|
| `store_sales` | Une ligne par vente détaillée |
| `inventory` | Une ligne par enregistrement de stock |
| `sales_by_store` | Une ligne par magasin |
| `sales_by_store_date` | Une ligne par magasin et par date |
| `sales_by_item_date` | Une ligne par article et par date |
| `inventory_by_item_date` | Une ligne par article et par date, tous entrepôts confondus |
| `sales_inventory_by_item_date` | Une ligne par article et par date, avec rapprochement ventes-stocks |

Les résultats sont enregistrés dans `data/silver-transformed/`.

### 6. Construction de la couche Gold

Le traitement `etape7_gold.py` construit le jeu de données :

```text
data/gold/sales_performance_by_store/
```

Ce jeu présente les performances commerciales par magasin.

Il conserve les principales mesures de ventes et ajoute des indicateurs analytiques :

- classement des magasins selon le chiffre d'affaires 
- identification du magasin ayant le meilleur chiffre d'affaires 
- chiffre d'affaires global 
- part du chiffre d'affaires de chaque magasin

Le jeu Gold obtenu contient 12 lignes, soit une ligne par magasin, et 14 colonnes.

### 7. Contrôles qualité

Les traitements de contrôle vérifient notamment :
- la présence et la structure des colonnes 
- la complétude des champs 
- la conformité des types 
- l'unicité des clés 
- la cohérence du classement 
- la cohérence des parts de chiffre d'affaires 
- la réconciliation des mesures entre Silver transformé et Gold 
- la cohérence des données avant et après écriture Parquet

Le rapport final est enregistré dans :

```text
reports/quality/quality_report_gold.csv
```

## Sorties produites

Les traitements du J3 produisent plusieurs jeux de données et éléments de contrôle.

| Couche | Sortie | Description |
|---|---|---|
| Bronze | Fichiers sources DAT | Conservation des données brutes |
| Silver | `store_sales` | Ventes nettoyées et contrôlées |
| Silver | `inventory` | Stocks nettoyés et contrôlés |
| Silver transformé | `store_sales` | Données de ventes enrichies |
| Silver transformé | `inventory` | Données de stocks enrichies |
| Silver transformé | `sales_by_store` | Agrégation des ventes par magasin |
| Silver transformé | `sales_by_store_date` | Agrégation par magasin et date |
| Silver transformé | `sales_by_item_date` | Agrégation par article et date |
| Silver transformé | `inventory_by_item_date` | Agrégation des stocks par article et date |
| Silver transformé | `sales_inventory_by_item_date` | Rapprochement ventes-stocks |
| Gold | `sales_performance_by_store` | Indicateurs de performance commerciale par magasin |
| Quality | `quality_report_gold.csv` | Résultats des contrôles qualité |

Les couches Silver et suivantes sont conservées au format Parquet. Le jeu Gold utilise une compression Snappy.

### Résultats principaux observés

Les volumes obtenus pendant les traitements sont les suivants :

| Jeu de données | Nombre de lignes |
|---|---:|
| `store_sales` Silver transformé | 667 579 |
| `inventory` Silver transformé | 23 249 101 |
| `sales_by_store` | 12 |
| `sales_by_store_date` | 21 430 |
| `sales_by_item_date` | 565 428 |
| `inventory_by_item_date` | 4 661 999 |
| `sales_inventory_by_item_date` | 565 428 |
| `sales_performance_by_store` Gold | 12 |

Pour le jeu Gold, le chiffre d'affaires TTC global observé est de :

```text
1 202 218 083,00
```

Le magasin numéro 7 arrive en première position avec un chiffre d'affaires TTC de :

```text
103 384 198,80
```

Sa part du chiffre d'affaires global est de 8,60 %.

Ces résultats correspondent à l'exécution réalisée sur le jeu synthétique TPCx-BB utilisé pendant le J3.

## Contrôles qualité disponibles

Les contrôles qualité permettent de vérifier la cohérence des données tout au long de leur préparation.

### Contrôles Silver

Les contrôles réalisés portent notamment sur :
- les volumes de données 
- les valeurs nulles 
- les types de colonnes 
- les doublons candidats 
- les lignes mises en quarantaine 
- les anomalies détectées dans les mesures

Pour `store_sales`, les 667 579 lignes ont été conservées, sans mise en quarantaine. Des doublons candidats ont été signalés, mais conservés afin de ne pas supprimer automatiquement des lignes potentiellement légitimes.

Pour `inventory`, 23 255 100 lignes ont été lues. Parmi elles, 5 999 ont été mises en quarantaine, principalement en raison de valeurs nulles dans `inv_quantity_on_hand`.

### Contrôles des transformations

Les transformations font également l'objet de vérifications portant sur :
- le respect de la granularité attendue 
- l'absence de multiplication des lignes lors des jointures 
- la conservation des volumes attendus 
- la cohérence des agrégations

Pour le rapprochement ventes-stocks, le nombre de lignes reste identique avant et après la jointure : 565 428 lignes.

Le taux de correspondance observé est de 14,28 %. Cette absence de correspondance pour une partie des ventes ne démontre pas, à elle seule, une rupture de stock.

### Contrôles Gold

Le contrôle qualité final du jeu Gold a produit le bilan suivant :

| Résultat | Nombre |
|---|---:|
| PASS | 44 |
| FAIL | 0 |
| WARN | 1 |
| INFO | 0 |

Les contrôles ont notamment confirmé :
- les 12 lignes attendues 
- la présence des colonnes requises 
- l'absence de valeurs nulles dans les champs contrôlés 
- l'unicité de `store_sk` 
- la cohérence du classement des magasins 
- l'identification d'un seul meilleur magasin
- la cohérence des parts de chiffre d'affaires 
- la réconciliation des six mesures avec la source Silver transformée 
- la conservation des données après écriture et relecture Parquet

Un avertissement concerne le contrôle d'intégrité référentielle avec `store_sales` : la colonne `store_sk` n'étant pas disponible dans cette source, ce contrôle n'a pas pu être effectué.

Le rapport détaillé est disponible dans `reports/quality/quality_report_gold.csv`.

## Limites connues

Plusieurs limites ont été identifiées pendant les traitements.

### Qualité des données sources

Certaines valeurs nulles et anomalies sont présentes dans les fichiers TPCx-BB.

Par exemple :
- 3 324 prix unitaires nuls 
- 3 954 montants nets payés nuls 
- des marges et profits négatifs 
- 5 999 lignes de stock mises en quarantaine

Ces anomalies ne sont pas systématiquement corrigées automatiquement. Leur interprétation dépend des règles métier et de la signification des données.

### Doublons candidats

Des doublons candidats ont été identifiés dans les données de ventes : 8 174 lignes réparties dans 4 038 groupes.

Ils ont été conservés, car une répétition de valeurs ne suffit pas à démontrer qu'une vente est réellement dupliquée.

### Rapprochement ventes-stocks

Le taux de correspondance entre ventes et stocks agrégés est de 14,28 %.

Les stocks étant agrégés par article et date, tous entrepôts confondus, aucune relation directe entre un magasin et un entrepôt n'a été établie.

Il n'est donc pas possible de conclure automatiquement à une rupture de stock à partir de l'absence de correspondance.

### Interprétation des indicateurs métier

Les profits nets agrégés présentent des valeurs négatives.

Ces résultats doivent être interprétés avec prudence, en tenant compte de la définition des mesures et du caractère synthétique du jeu de données.

Le classement Gold repose sur le chiffre d'affaires TTC et ne constitue pas, à lui seul, une évaluation globale de la performance économique des magasins.

### Comparaison des formats

Le format Parquet a été utilisé pour les couches analytiques, avec compression Snappy pour le jeu Gold.

En revanche, aucune comparaison complète des temps de lecture, d'écriture et des tailles de fichiers entre CSV, JSON et Parquet n'a été réalisée. Il n'est donc pas possible de quantifier un gain de performance sur la base des traitements effectués.

## Reproduction des traitements

Pour reproduire les traitements, il faut disposer des prérequis techniques, des fichiers sources TPCx-BB et de l'arborescence du projet.

Depuis le répertoire du projet :

```bash
cd ~/retail-intelligence/tp3/
```

Activer l'environnement virtuel Python avant de lancer les traitements :

```bash
source retail_intel_tp3_venv/bin/activate
```

Vérifier que l'environnement virtuel est bien actif :

```bash
which python
python --version
```


Vérifier l'environnement :

```bash
python3 --version
java -version
pyspark --version
spark-submit --version
```

Vérifier la présence des fichiers sources dans la couche Bronze :

```bash
ls -lh data/bronze/
```

Lancer ensuite les traitements dans l'ordre logique suivant :

1. Vérification de l'environnement.
2. Inventaire des sources.
3. Préparation et nettoyage Silver.
4. Transformations Silver.
5. Construction de la couche Gold.
6. Contrôles qualité Gold.

Les scripts doivent être lancés depuis le répertoire du projet ou avec des chemins adaptés à leur emplacement réel.

Exemple de lancement d'un script PySpark :

```bash
spark-submit scripts/nom_du_script.py
```

Le nom du script doit être remplacé par celui du fichier effectivement présent dans le dépôt.

Après exécution, vérifier la présence des jeux de données dans `data/` et du rapport final dans `reports/quality/`.

Les scripts doivent être exécutés dans l'ordre prévu, car chaque couche dépend des résultats produits par la précédente.

## Continuité du projet

Le J3 constitue une étape importante dans la construction de la Retail Intelligence Platform.

Après la mise en place du stockage et des mécanismes d'ingestion lors du J2, les traitements du J3 permettent de transformer les fichiers sources en données structurées, contrôlées et adaptées aux analyses.

La séparation entre Bronze, Silver et Gold facilite la compréhension des traitements, la traçabilité des données et la réutilisation des jeux produits.

La couche Gold fournit une première vue analytique des performances commerciales par magasin, les contrôles qualité permettent de vérifier la cohérence des résultats obtenus.