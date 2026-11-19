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
Les dossiers `data/` ne sont pas **committées sur Git** car les données dépendent du contexte métier. Vous choisissez les fichiers de données correspondant à vos besoins.

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




## Questions de recul

### 1. Pourquoi est-il nécessaire de vérifier les schémas avant de commencer les transformations ?

La vérification des schémas permet de connaître précisément la structure des données avant de les exploiter : noms des colonnes, types, formats et éventuelles valeurs nulles.

Cette étape évite notamment les erreurs de traitement liées à des types incorrects, à des colonnes manquantes ou à une mauvaise interprétation des champs. Elle permet également de définir des règles de nettoyage et de transformation adaptées aux données réellement disponibles.

Dans ce projet, l'exploration des fichiers TPCx-BB a notamment permis d'identifier les colonnes des tables `store_sales` et `inventory`, ainsi que leurs types, avant leur traitement avec PySpark.

### 2. Quelle différence existe entre une donnée brute, une donnée Silver et une donnée Gold ?

Ces trois niveaux correspondent à des étapes différentes de préparation et de valorisation des données.

- **Bronze (donnée brute)** : contient les données récupérées depuis les sources, avec un minimum de modifications. L'objectif est de conserver les données d'origine pour pouvoir les retrouver et les retraiter.
- **Silver (donnée nettoyée et structurée)** : contient des données dont la structure a été contrôlée et qui ont subi des traitements de nettoyage, de typage et de validation. Les anomalies peuvent être identifiées et, selon les règles définies, certaines lignes peuvent être mises en quarantaine.
- **Gold (donnée métier)** : contient des données transformées et agrégées pour répondre à des besoins d'analyse et faciliter leur exploitation. Elles sont organisées selon une granularité et des indicateurs définis.

Dans le projet, la couche Gold `sales_performance_by_store` permet notamment de comparer les performances des magasins à partir du chiffre d'affaires, du classement et de la part de chiffre d'affaires de chaque magasin.

### 3. Pourquoi faut-il connaître la granularité d’une table avant de réaliser une agrégation ?

La granularité correspond au niveau de détail représenté par une ligne d'une table. Il est indispensable de la connaître pour choisir correctement les clés de regroupement et éviter les agrégations incorrectes.

Une mauvaise compréhension de la granularité peut entraîner des doublons, des comptages erronés ou une multiplication artificielle des montants.

Dans ce projet, les jeux de données transformés ne possèdent pas tous la même granularité : `sales_by_store` contient une ligne par magasin, tandis que `sales_by_store_date` contient une ligne par magasin et par date. Cette distinction est essentielle pour calculer correctement les indicateurs.

### 4. Quels risques présente une jointure réalisée sur une clé supposée ?

Une jointure réalisée sur une clé dont l'unicité ou la signification n'a pas été vérifiée peut produire plusieurs problèmes :

- multiplication du nombre de lignes lorsque plusieurs correspondances existent
- perte de lignes lorsqu'aucune correspondance n'est trouvée avec une jointure interne
- association de données qui ne correspondent pas réellement au même élément métier
- calculs et indicateurs faussés à la suite de ces associations incorrectes.

Il est donc nécessaire de vérifier les clés utilisées, leur unicité, les valeurs nulles et le nombre de correspondances avant et après la jointure.

Dans le projet, la jointure entre les ventes et les stocks a conservé les 565 428 lignes de ventes. Aucune multiplication de lignes n'a été constatée, mais seulement 80 727 lignes ont trouvé une correspondance, soit environ 14,28 %. Ce résultat montre qu'une jointure techniquement correcte ne garantit pas que toutes les données possèdent une correspondance métier.

### 5. Pourquoi ne faut-il pas supprimer automatiquement les valeurs atypiques ?

Une valeur atypique n'est pas nécessairement une erreur. Elle peut correspondre à une situation réelle, à une opération exceptionnelle, à un retour ou à une particularité du fonctionnement métier.

La supprimer automatiquement peut entraîner une perte d'information et modifier les résultats des analyses, notamment les sommes, les moyennes et les indicateurs de performance.

Il est donc préférable d'identifier ces valeurs, de les documenter et de comprendre leur origine avant de décider d'une éventuelle correction ou exclusion.

Dans ce projet, certaines valeurs négatives de profit ou certaines valeurs nulles de prix et de montants ont été signalées comme anomalies potentielles, sans être automatiquement supprimées. Leur interprétation nécessite des règles métier complémentaires.

### 6. Quels contrôles permettent de vérifier la cohérence d’un jeu de données transformé ?

Plusieurs contrôles complémentaires permettent de vérifier la qualité et la cohérence d'un jeu de données :

- **Contrôle du volume** : vérifier le nombre de lignes attendu après transformation.
- **Contrôle du schéma** : vérifier la présence des colonnes et la conformité de leurs types.
- **Contrôle de complétude** : identifier les valeurs nulles dans les champs importants.
- **Contrôle d'unicité** : vérifier l'absence de doublons sur les clés définies.
- **Contrôle des valeurs** : vérifier les plages autorisées et les règles de cohérence métier.
- **Contrôle des agrégations** : comparer les totaux avant et après transformation.
- **Contrôle des jointures** : vérifier le nombre de lignes, les correspondances et les éventuelles multiplications.
- **Contrôle de persistance** : relire les données enregistrées et vérifier qu'elles correspondent aux données attendues.

Pour la couche Gold du projet, les contrôles ont notamment permis d'obtenir 44 tests réussis, aucun échec et un avertissement. Cet avertissement concerne l'impossibilité de vérifier l'intégrité référentielle de `store_sk` avec la source disponible, car la colonne nécessaire n'était pas présente dans le jeu de données utilisé pour ce contrôle.

### 7. Pourquoi Parquet est-il adapté aux usages analytiques ?

Parquet est un format de stockage en colonnes particulièrement adapté aux traitements analytiques.

Contrairement à un format organisé principalement en lignes, il permet de lire uniquement les colonnes nécessaires à une requête. Cela peut réduire les volumes de données lus et améliorer les performances lorsque les traitements portent sur un sous-ensemble de colonnes.

Parquet prend également en charge la compression et conserve les types des données dans son schéma. Il est ainsi adapté aux traitements distribués avec Apache Spark et aux architectures Data Lake.

Dans ce projet, les données des couches Silver et Gold sont stockées au format Parquet. La couche Gold utilise également la compression Snappy.

### 8. Pourquoi Parquet seul ne fournit-il pas les garanties d’une table transactionnelle Lakehouse ?

Parquet est un format de fichiers : il définit la manière dont les données sont organisées et stockées. En revanche, il ne fournit pas à lui seul les mécanismes nécessaires à la gestion transactionnelle d'une table.

Il ne garantit notamment pas nativement :
- les transactions ACID 
- la gestion des écritures concurrentes 
- le contrôle des modifications et des versions 
- la gestion cohérente des mises à jour et suppressions 
- la possibilité de revenir à un état précédent de la table

Une architecture Lakehouse peut donc utiliser Parquet comme format de stockage tout en s'appuyant sur une couche supplémentaire, comme Delta Lake, Apache Iceberg ou Apache Hudi, pour apporter ces fonctionnalités.

Ainsi, utiliser Parquet dans le projet permet de stocker efficacement les données analytiques, mais ne suffit pas à mettre en place une gestion transactionnelle complète.

### 9. Dans quels cas une base NoSQL pourrait-elle compléter une architecture Data Lake ?

Une base NoSQL peut compléter un Data Lake lorsque l'application nécessite des accès rapides, des structures de données flexibles ou une gestion de données qui ne se prête pas facilement à un modèle relationnel classique.

Elle peut notamment être pertinente pour :
- stocker des données semi-structurées ou très variables
- gérer des événements et des données générées en continu
- répondre à des requêtes opérationnelles à faible latence 
- gérer des volumes importants avec des besoins de distribution et de scalabilité 
- fournir un accès rapide à des données utilisées par une application

Dans une architecture globale, le Data Lake peut conserver les données historiques et alimenter les traitements analytiques, tandis que la base NoSQL peut servir les besoins opérationnels de certaines applications.

Ces deux composants ont donc des rôles complémentaires et ne répondent pas exactement aux mêmes besoins.

### 10. Quelles limites des données TPCx-BB doivent être prises en compte lors de l’interprétation des résultats ?

Les données TPCx-BB utilisées dans ce projet constituent un jeu de données synthétique destiné à représenter un contexte de distribution. Elles permettent de travailler sur des volumes importants et de mettre en œuvre des traitements de données, mais elles ne doivent pas être considérées comme une représentation exacte d'une activité commerciale réelle.

Plusieurs limites doivent être prises en compte :

- **Données synthétiques** : les résultats ne décrivent pas nécessairement le comportement de véritables magasins ou clients.
- **Contexte métier limité** : certaines règles métier ne sont pas disponibles ou ne peuvent pas être déduites uniquement des données.
- **Valeurs atypiques** : des valeurs nulles, négatives ou inhabituelles peuvent nécessiter une interprétation avant toute correction.
- **Relations entre tables** : une clé présente dans plusieurs jeux de données ne garantit pas automatiquement une correspondance métier complète.
- **Périmètre des données** : les indicateurs calculés dépendent des tables, des colonnes et des périodes effectivement disponibles.
- **Interprétation des indicateurs** : un chiffre d'affaires, un montant net payé ou un profit calculé ne doit pas être interprété sans connaître précisément sa définition métier.

Par exemple, la couche Gold fait ressortir le magasin 7 comme premier magasin en chiffre d'affaires, avec environ 103,38 millions, soit 8,60 % du chiffre d'affaires global. Ce résultat est valable dans le périmètre des données traitées, mais ne permet pas à lui seul de conclure qu'il s'agit du magasin le plus performant dans une situation commerciale réelle.

De même, les profits nets agrégés négatifs observés doivent être interprétés avec prudence : sans définition métier complémentaire, il n'est pas possible de déterminer s'ils traduisent une anomalie, une particularité du jeu synthétique ou une règle de calcul spécifique.

Ces limites rappellent que la qualité technique des traitements ne suffit pas à garantir la pertinence métier des conclusions. L'interprétation des résultats doit toujours tenir compte de la provenance, de la structure et du contexte des données.