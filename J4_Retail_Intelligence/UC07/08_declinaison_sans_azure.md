# Étape 8 : Décliner l'architecture sans Azure (Parcours B)

## 1. Introduction et objectifs

### 1.1. Contexte

Dans le cadre du cas d'utilisation UC-07 – Transposition de la plateforme sur Azure, cette étape étudie une architecture alternative reposant sur des technologies locales et open source.

Le parcours B consiste à identifier les composants qui assurent les fonctions de stockage, de traitement, d'interrogation, de gestion des métadonnées, d'orchestration et de sécurité, sans utiliser de services Azure.

L'environnement Retail Intelligence du TP3 constitue le socle technique de cette étude.

L'objectif est double :
- décrire l'architecture locale réellement utilisée 
- identifier les technologies qui pourraient compléter cette architecture dans une perspective d'évolution.

La démarche distingue systématiquement les composants effectivement présents des technologies uniquement étudiées ou proposées.

### 1.2. Objectifs techniques

Les huit activités du parcours B portent sur :

1. L'identification du stockage local ou objet.
2. L'organisation des zones Bronze, Silver et Gold.
3. La distinction entre Parquet et Apache Iceberg.
4. Le traitement des données avec Spark et PySpark.
5. Les requêtes analytiques avec Spark SQL ou Trino.
6. La gestion du catalogue et des métadonnées.
7. L'orchestration des traitements.
8. La sécurité locale et la séparation des environnements.

Le résultat attendu est une description argumentée de l'architecture locale, accompagnée d'un schéma et d'une démonstration fondée sur les traitements métier réellement utilisés dans le projet.


## 2. Environnement technique local

### 2.1. Système et environnement Python

Le projet est exécuté sous Linux.

L'environnement Python utilisé pour les vérifications du TP3 est un environnement virtuel indépendant, situé dans le répertoire du projet.

Les versions vérifiées sont :

| Composant | Version |
|---|---|
| Python | 3.12.3 |
| Apache Spark | 4.3.0 |
| PySpark | 4.3.0 |
| Pandas | 3.1.1 |

L'interpréteur Python TP3 est accessible depuis :

`~/retail-intelligence/tp3/retail_intel_tp3_venv/bin/python`

Jupyter Notebook est également utilisé pour les travaux d'exploration et de vérification.

### 2.2. Séparation TP3 et TP4

Le projet dispose de deux environnements virtuels distincts :

- TP3 : `~/retail-intelligence/tp3/retail_intel_tp3_venv/`
- TP4 : `~/retail-intelligence/tp4/retail_intel_tp4_venv/`

La séparation physique de ces environnements a été vérifiée.

L'interpréteur TP3 a été identifié et sa version confirmée.

Cette organisation permet :
- de séparer les dépendances Python 
- de limiter les conflits de versions 
- de préserver un environnement de travail indépendant pour chaque TP 
- de réduire les risques de modification accidentelle des dépendances d'un autre travail.

Cette séparation concerne les environnements Python. Elle ne constitue pas une isolation complète au niveau du système Linux.

### 2.3. Organisation générale du projet

Les principaux répertoires identifiés sont :

```text
retail-intelligence/
|
+-- tp3/
|   |
|   +-- data/
|   +-- notebooks/
|   +-- scripts/
|   +-- output/
|   +-- reports/
|   +-- logs/
|   +-- retail_intel_tp3_venv/
|
+-- tp4/
    |
    +-- notebooks/
    +-- scripts/
    +-- reports/
    +-- visualisations/
    +-- retail_intel_tp4_venv/
```

Les répertoires de TP3 et TP4 sont distincts.


## 3. Identification du stockage local

### 3.1. Support de stockage réellement utilisé

Le stockage de Retail Intelligence repose sur le système de fichiers Linux.

Le répertoire principal des données TP3 est :

`~/retail-intelligence/tp3/data/`

Les vérifications de l'arborescence ont confirmé que les données sont organisées en répertoires physiques.

Les fichiers sources identifiés dans Bronze sont :

- `data/bronze/store_sales/store_sales.dat`
- `data/bronze/inventory/inventory.dat`

Les résultats des traitements sont matérialisés sous forme de fichiers Parquet.

Le stockage est donc local et fondé sur le système de fichiers, et non sur un service de stockage objet.

### 3.2. Distinction entre stockage, organisation et formats

Il est important de distinguer quatre notions.

| Notion | Technologie ou organisation utilisée |
|---|---|
| Support de stockage | Système de fichiers Linux |
| Organisation logique | Répertoires Bronze, Silver, Silver-transformed et Gold |
| Format de fichiers | Apache Parquet |
| Format de table | Aucun format Iceberg établi |

Cette distinction permet de ne pas confondre un répertoire contenant des fichiers Parquet avec une table gérée par un format de table transactionnel.

### 3.3. MinIO : possibilité de stockage objet local

MinIO est une solution de stockage objet compatible avec l'API S3.

Elle permet de mettre à disposition des applications un stockage organisé en buckets, sans dépendre d'un service cloud externe.

Dans une architecture Retail Intelligence évoluée, MinIO pourrait remplacer ou compléter le stockage local actuel.

Les données pourraient alors être accessibles par les moteurs de traitement à travers une interface compatible S3.

Cependant, MinIO n'a pas été identifié comme installé ou déployé dans l'environnement TP3.

Le stockage effectivement utilisé reste le système de fichiers Linux.

### 3.4. Bilan du stockage

| Composant | Statut |
|---|---|
| Linux | Réalisé |
| Système de fichiers local | Réalisé |
| Répertoire `data/` | Réalisé |
| Fichiers sources `.dat` | Réalisé |
| Fichiers Parquet | Réalisé |
| Compression Snappy | Réalisé |
| MinIO | Non déployé |
| Stockage objet S3 | Étudié |
| ADLS Gen2 | Non déployé |



## 4. Organisation des zones de données

### 4.1. Organisation physique vérifiée

L'inspection du répertoire `data/` a permis de confirmer l'existence des espaces suivants.

```text
data/
|
+-- bronze/
|   +-- inventory/
|   |   +-- inventory.dat
|   |
|   +-- store_sales/
|       +-- store_sales.dat
|
+-- silver/
|   +-- inventory/
|   +-- store_sales/
|
+-- silver-transformed/
|   +-- inventory/
|   +-- inventory_by_item_date/
|   +-- sales_by_item_date/
|   +-- sales_by_store/
|   +-- sales_by_store_date/
|   +-- sales_inventory_by_item_date/
|   +-- store_sales/
|
+-- gold/
|   +-- sales_performance_by_store/
|
+-- quality/
|   +-- store_sales_duplicate_candidates/
|   +-- summary/
|
+-- quarantine/
    +-- inventory/
    +-- store_sales/
```

Les fichiers observés dans les zones de résultats sont des fichiers Parquet avec compression Snappy.

Des fichiers `_SUCCESS` et `.crc` sont également présents dans plusieurs répertoires.

Les fichiers `_SUCCESS` sont des marqueurs associés aux écritures Spark. Les fichiers `.crc` sont des fichiers de contrôle compatibles avec les mécanismes Hadoop.

Ils ne constituent pas des jeux de données analytiques supplémentaires.

### 4.2. Zone Bronze

La zone Bronze accueille les données sources brutes.

Dans le projet, elle contient :
- les données de ventes `store_sales.dat` 
- les données de stock `inventory.dat`.

Le script `etape4_nettoyage.py` lit ces deux fichiers à partir de leur emplacement Bronze.

Les données sont initialement lues en chaînes de caractères avec un séparateur `|`.

Cette lecture permet de conserver les valeurs brutes avant leur conversion vers les types attendus.

Les fichiers sources ne sont pas modifiés par les règles de nettoyage définies dans le script.

**Rôle architectural :** conserver les données d'entrée utilisées par les traitements analytiques.

### 4.3. Zone Silver

La zone Silver contient les données nettoyées et préparées.

Le script `etape4_nettoyage.py` réalise notamment :
- la conversion des colonnes vers les types attendus 
- la détection des valeurs obligatoires manquantes 
- la détection des erreurs de conversion 
- l'identification des quantités négatives 
- la détection de doublons potentiels sur les ventes 
- la séparation des données conservées et des données mises en quarantaine.

Les jeux de données Silver produits sont :
- `store_sales` 
- `inventory`.

Les données sont enregistrées au format Parquet.

### 4.4. Zone Silver-transformed

La zone Silver-transformed constitue un espace physique distinct de Silver.

Le script `etape5_6_transformations_silver.py` lit les deux jeux nettoyés :

- `data/silver/store_sales`
- `data/silver/inventory`

Il produit ensuite sept jeux de données :

| Jeu de données | Granularité ou fonction |
|---|---|
| `store_sales` | Ventes détaillées enrichies |
| `inventory` | Stock détaillé enrichi |
| `sales_by_store` | Agrégation des ventes par magasin |
| `sales_by_store_date` | Agrégation des ventes par magasin et date |
| `sales_by_item_date` | Agrégation des ventes par article et date |
| `inventory_by_item_date` | Agrégation du stock par article et date |
| `sales_inventory_by_item_date` | Rapprochement des ventes et du stock par article et date |

Les jeux de données détaillés comportent également des informations de provenance, notamment :
- `_source_dataset` 
- `_source_original_file` 
- `_processing_stage`.

Le script vérifie les colonnes nécessaires et les types numériques avant d'effectuer les transformations.

Il réalise également des contrôles de cardinalité lors du rapprochement entre les ventes et le stock.

Les résultats sont écrits en Parquet avec compression Snappy.

Après écriture, le script relit chaque jeu de données et vérifie :
- le nombre de lignes 
- le nombre de colonnes 
- la lisibilité du résultat 
- la conservation du schéma.

Cette organisation permet de distinguer les données nettoyées des données transformées et agrégées.

### 4.5. Zone Gold

La zone Gold contient les résultats analytiques destinés à une exploitation métier.

Le jeu de données effectivement identifié est :

`data/gold/sales_performance_by_store/`

Il correspond à une analyse des performances commerciales par magasin.

La question métier associée au traitement est :

**Quels magasins réalisent le meilleur chiffre d'affaires ?**

Le script `etape7_gold.py` utilise comme source :

`data/silver-transformed/sales_by_store/`

Il produit le jeu Gold `sales_performance_by_store`.

Les contrôles effectués dans le script portent notamment sur :
- la présence des colonnes nécessaires 
- l'absence de clés magasin nulles 
- l'unicité des magasins 
- la validité des indicateurs numériques 
- la cohérence du classement 
- la vérification des résultats après écriture.

Le jeu Gold est ensuite relu pour vérifier la conservation du nombre de lignes et des données.

### 4.6. Espaces Quality et Quarantine

Quality et Quarantine sont des espaces complémentaires.

Ils ne constituent pas des couches supplémentaires de la chaîne Bronze/Silver/Gold.

**Quality** contient notamment :
- les ventes signalées comme doublons potentiels 
- un résumé des volumes traités, conservés et mis en quarantaine.

Le script de nettoyage conserve les doublons potentiels de ventes dans Silver tout en produisant un jeu distinct destiné à leur examen.

Les données signalées ne sont donc pas automatiquement supprimées.

**Quarantine** contient les lignes écartées des jeux Silver à cause de problèmes bloquants.

Pour les ventes et les stocks, les principales conditions de mise en quarantaine sont :
- un champ obligatoire manquant 
- une conversion invalide 
- une quantité négative.

Cette organisation permet de séparer les données exploitables des données nécessitant un traitement particulier.

### 4.7. Flux métier réellement identifiés

L'analyse des scripts permet désormais de documenter les dépendances suivantes :

```text
                    FICHIERS BRONZE
                    /             \
                   /               \
                  v                 v
             store_sales.dat   inventory.dat
                  |                 |
                  +--------+--------+
                           |
                           v
                 ETAPE 4 - NETTOYAGE
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
           SILVER       QUARANTINE     QUALITY
             |                           |
             |                           |
             v                           |
       ETAPES 5 ET 6                     |
       TRANSFORMATIONS                   |
             |                           |
             v                           |
      SILVER-TRANSFORMED                 |
             |                           |
             v                           |
        ETAPE 7 - GOLD                   |
             |                           |
             v                           |
       sales_performance                 |
          _by_store                       |
             |                           |
             +-------------+-------------+
                           |
                           v
                 ETAPE 9 - CONTROLES
                           |
                           v
                 RAPPORT DE QUALITE
```

Le schéma représente les dépendances fonctionnelles principales.

Il faut toutefois distinguer les flux de données des mécanismes de contrôle :

- Quality et Quarantine sont produits dès l'étape de nettoyage 
- l'étape 9 effectue des contrôles complémentaires sur Gold et ses sources 
- le rapport de l'étape 9 est un fichier CSV distinct des jeux Parquet stockés dans `data/quality`.

Les traitements ne sont pas pilotés par un orchestrateur central.



## 5. Apache Parquet et Apache Iceberg

### 5.1. Parquet : format de fichiers utilisé

Apache Parquet est un format de stockage en colonnes conçu pour les traitements analytiques.

Il permet :
- de lire sélectivement les colonnes nécessaires 
- de réduire les volumes grâce à la compression 
- de faciliter les échanges entre moteurs analytiques 
- de structurer les données pour les traitements distribués.

Dans Retail Intelligence, Parquet est effectivement utilisé pour matérialiser les résultats des traitements Spark.

Les fichiers observés portent l'extension `.snappy.parquet`.

La compression Snappy permet de réduire la taille des données tout en conservant de bonnes performances de lecture et d'écriture.

### 5.2. Apache Iceberg : format de table étudié

Apache Iceberg est un format de table destiné aux architectures analytiques de type lakehouse.

Il apporte une couche de gestion des métadonnées au-dessus des fichiers de données.

Ses principales fonctionnalités comprennent :
- la gestion des snapshots 
- le suivi des versions 
- l'évolution du schéma 
- la gestion des modifications de données 
- la cohérence des opérations sur les tables 
- l'accès aux tables par plusieurs moteurs compatibles.

Iceberg ne remplace pas obligatoirement Parquet.

Dans une architecture Iceberg, les données peuvent rester stockées physiquement dans des fichiers Parquet, tandis qu'Iceberg gère les métadonnées et l'état logique de la table.

### 5.3. Comparaison

| Critère | Parquet | Iceberg |
|---|---|---|
| Nature | Format de fichiers | Format de table |
| Stockage physique | Oui | Utilise des fichiers de données |
| Organisation en colonnes | Oui | Dépend du format sous-jacent |
| Gestion des métadonnées de table | Non, pas au niveau transactionnel | Oui |
| Snapshots | Non | Oui |
| Évolution du schéma | Gestion par les outils consommateurs | Gestion au niveau de la table |
| Transactions de table | Non | Oui, selon les opérations prises en charge |
| Utilisation dans TP3 | Réalisée | Non établie |

### 5.4. Positionnement dans Retail Intelligence

Parquet répond actuellement aux besoins de stockage et de traitement du projet.

Iceberg pourrait être introduit si la plateforme devait évoluer vers :
- plusieurs moteurs d'accès 
- une gestion des versions des données 
- des opérations de mise à jour plus avancées 
- une meilleure gouvernance des tables 
- des mécanismes de reprise à partir de snapshots.

Son installation n'est pas nécessaire pour démontrer l'architecture actuellement utilisée.

**Bilan : Parquet est réalisé  Iceberg est étudié et non déployé.**



## 6. Traitements avec Apache Spark et PySpark

### 6.1. Apache Spark

Apache Spark est le moteur de traitement utilisé dans Retail Intelligence.

Il prend en charge les lectures, transformations, agrégations, jointures et écritures des données.

La version vérifiée dans l'environnement TP3 est 4.3.0.

Spark permet notamment de traiter les données sources, de produire les jeux Silver et de construire le résultat Gold.

### 6.2. PySpark

PySpark constitue l'interface Python utilisée pour développer les traitements Spark.

Les scripts métier utilisent notamment :
- `SparkSession` pour initialiser Spark 
- les DataFrames pour manipuler les jeux de données 
- `pyspark.sql.functions` pour les transformations 
- les fonctions d'agrégation 
- les fonctions de fenêtrage 
- les opérations de lecture et d'écriture Parquet.

Les traitements utilisent le moteur Spark tout en conservant une logique de développement Python.

### 6.3. Traitement métier : nettoyage des données

Le script `etape4_nettoyage.py` constitue la première étape métier documentée.

Il lit les deux fichiers sources Bronze :

- `store_sales.dat` 
- `inventory.dat`.

Les données sont initialement lues avec des colonnes de type chaîne.

Les conversions sont ensuite réalisées vers les types attendus.

Pour les ventes, les principales conversions concernent :
- les clés de date, magasin, article et client 
- les identifiants de tickets 
- les quantités 
- les valeurs financières au format décimal.

Pour les stocks, les conversions concernent :
- la clé de date 
- la clé article 
- la clé entrepôt 
- la quantité disponible.

Le script ajoute des indicateurs de qualité pour identifier les anomalies.

Pour les ventes, les contrôles comprennent notamment :
- les champs obligatoires manquants 
- les erreurs de conversion 
- les quantités négatives 
- les prix nuls 
- les montants nets nuls 
- les bénéfices négatifs 
- les doublons potentiels.

Les doublons potentiels de ventes sont identifiés à partir de la combinaison :

`ss_sold_date_sk + ss_store_sk + ss_ticket_number + ss_item_sk`

Ils sont conservés dans Silver et également exportés dans le jeu Quality dédié.

Pour les stocks, les contrôles portent notamment sur les valeurs obligatoires, les erreurs de conversion et les quantités négatives.

Le script produit :
- les deux jeux Silver 
- les deux espaces Quarantine 
- le jeu des doublons potentiels de ventes 
- le résumé des contrôles qualité.

### 6.4. Transformations métier : étapes 5 et 6

Le script `etape5_6_transformations_silver.py` lit les jeux Silver.

Il vérifie les colonnes et les types nécessaires avant de produire les jeux transformés.

Les traitements comprennent notamment :
- l'ajout des informations de provenance 
- l'agrégation des ventes par magasin 
- l'agrégation des ventes par magasin et date 
- l'agrégation des ventes par article et date 
- l'agrégation du stock par article et date 
- le rapprochement des ventes et des stocks.

Le rapprochement ventes-stock comporte des vérifications de cardinalité afin de détecter les risques de multiplication des lignes.

Les sept résultats sont écrits en Parquet avec compression Snappy.

Le script effectue une relecture de chaque résultat et compare les nombres de lignes et les schémas.

Cette étape matérialise le passage des données nettoyées vers des jeux transformés adaptés aux analyses métier.

### 6.5. Production du jeu Gold : étape 7

Le script `etape7_gold.py` répond à la question :

**Quels magasins réalisent le meilleur chiffre d'affaires ?**

Il lit le jeu :

`data/silver-transformed/sales_by_store/`

Puis produit :

`data/gold/sales_performance_by_store/`

Le résultat comporte des indicateurs de performance commerciale par magasin.

Le schéma précédemment vérifié contient notamment :
- l'identifiant du magasin 
- son rang de chiffre d'affaires 
- l'indicateur du meilleur magasin 
- le chiffre d'affaires TTC 
- le chiffre d'affaires global 
- la part du chiffre d'affaires 
- les montants nets payés et les bénéfices 
- les quantités vendues 
- les nombres de lignes de vente et de tickets.

Le script vérifie la présence des colonnes, l'unicité des magasins, les valeurs numériques et la cohérence des données avant de produire le résultat.

Une relecture après écriture permet de vérifier le nombre de lignes et l'identité des données avant et après matérialisation.

### 6.6. Contrôle qualité : étape 9

Le script `etape9_quality_control.py` complète la validation du résultat Gold.

Il contrôle notamment :
- le volume attendu de 12 magasins 
- la présence des colonnes obligatoires 
- l'absence de valeurs nulles 
- les types des colonnes 
- l'unicité des clés magasin 
- la validité du classement 
- la cohérence de l'indicateur du meilleur magasin 
- la cohérence des montants et des parts de chiffre d'affaires 
- la réconciliation avec `sales_by_store` 
- l'intégrité référentielle avec les ventes Silver.

Les contrôles sont enregistrés sous forme de résultats PASS, FAIL, WARN ou INFO.

Le script produit un rapport CSV :

`reports/quality/quality_report_gold.csv`

Ce rapport est distinct des jeux Parquet de la zone `data/quality/`.

Le script de contrôle constitue donc une étape de validation supplémentaire après la production de Gold.

### 6.7. Synthèse du traitement métier

| Étape | Script | Entrée principale | Sortie principale |
|---|---|---|---|
| 4 | `etape4_nettoyage.py` | Bronze | Silver, Quality, Quarantine |
| 5 et 6 | `etape5_6_transformations_silver.py` | Silver | Silver-transformed |
| 7 | `etape7_gold.py` | `sales_by_store` | Gold |
| 9 | `etape9_quality_control.py` | Gold et sources Silver | Rapport CSV |

Ces scripts représentent les traitements métier réels du projet.

Ils sont distincts et leur enchaînement est manuel.

### 6.8. Vérification effective de Spark

Une vérification indépendante a été effectuée sur le jeu Gold :

`data/gold/sales_performance_by_store/`

Spark a réussi à lire les fichiers Parquet.

Les résultats observés sont :
- 12 lignes 
- 14 colonnes 
- lecture sans erreur.

Cette vérification confirme le fonctionnement effectif de Spark sur un résultat Gold matérialisé.



## 7. Requêtes analytiques : Spark SQL et Trino

### 7.1. Spark SQL

Spark SQL permet d'interroger les DataFrames Spark à l'aide du langage SQL.

Une démonstration a été réalisée sur le jeu Gold `sales_performance_by_store`.

Les données ont été chargées dans Spark puis exposées sous la forme d'une vue temporaire :

`sales_performance_by_store`

La requête exécutée est :

```sql
SELECT
    store_sk,
    revenue_rank,
    total_revenue_inc_tax,
    revenue_share_pct
FROM sales_performance_by_store
ORDER BY revenue_rank
```

La requête a retourné les 12 magasins classés par chiffre d'affaires.

Le premier magasin du classement présente les valeurs suivantes :

| Indicateur | Valeur |
|---|---:|
| `store_sk` | 7 |
| `revenue_rank` | 1 |
| `total_revenue_inc_tax` | 103384198.80 |
| `revenue_share_pct` | 8.6 |

La requête s'est exécutée correctement.

La vue est temporaire : elle est limitée à la session Spark et ne constitue pas une table persistante.

Cette démonstration confirme l'utilisation effective de Spark SQL dans l'environnement TP3.

### 7.2. Trino

Trino est un moteur de requêtes SQL distribué indépendant de Spark.

Il permet d'interroger différentes sources de données au travers de connecteurs.

Dans une architecture analytique plus avancée, il pourrait être utilisé pour :
- interroger plusieurs sources depuis une interface SQL commune 
- faciliter l'accès aux données par des outils de BI 
- séparer les requêtes analytiques des traitements de transformation 
- accéder à des tables gérées par un catalogue partagé.

Trino pourrait notamment être étudié en complément de Spark et d'Iceberg.

Cependant, aucune installation ou utilisation effective de Trino n'a été établie dans le TP3.

### 7.3. Positionnement

| Composant | Statut |
|---|---|
| Spark SQL | Réalisé |
| Requête analytique sur Gold | Réalisé |
| Vue temporaire Spark | Réalisé |
| Trino | Étudié |
| Trino installé | Non déployé |

Spark SQL répond actuellement aux besoins de démonstration et d'interrogation des données du projet.

Trino représente une évolution possible si plusieurs moteurs ou outils doivent accéder aux mêmes données.



## 8. Catalogue et gestion des métadonnées

### 8.1. Catalogue Spark intégré

Une vérification de la configuration Spark a permis d'obtenir :

```text
spark.sql.catalogImplementation = in-memory
spark.sql.defaultCatalog = spark_catalog
```

Le catalogue visible est :

```text
spark_catalog
```

Le warehouse Spark est configuré sur un emplacement local :

`~/retail-intelligence/tp3/notebooks/spark-warehouse`

Ces résultats confirment que l'environnement utilise le catalogue intégré Spark en mémoire.

Le catalogue permet de gérer les métadonnées des objets enregistrés dans Spark.

La vue temporaire utilisée pour la démonstration SQL appartient à la session Spark et ne constitue pas une table persistante.

La présence du chemin warehouse dans la configuration ne suffit pas à prouver l'existence de tables persistantes dans ce répertoire.

### 8.2. Hive Metastore

Hive Metastore est un service externe permettant de centraliser les métadonnées des tables.

Il peut être utile lorsque plusieurs moteurs analytiques doivent accéder à des définitions de tables communes.

Dans une architecture Retail Intelligence plus avancée, Hive Metastore pourrait être envisagé pour faciliter le partage des métadonnées entre Spark et d'autres moteurs compatibles.

Aucun service Hive Metastore externe n'a été identifié dans l'environnement vérifié.

### 8.3. Project Nessie

Project Nessie est une solution de catalogue versionné, notamment adaptée aux architectures utilisant Apache Iceberg.

Elle apporte des mécanismes de branchement et de gestion de versions des métadonnées.

Elle pourrait être intéressante si le projet évolue vers :
- plusieurs environnements analytiques 
- plusieurs branches de données 
- une gestion versionnée des tables 
- des mécanismes de collaboration et de gouvernance.

Nessie n'a pas été identifié comme déployé dans le TP3.

### 8.4. Comparaison

| Solution | Fonction | Situation |
|---|---|---|
| `spark_catalog` | Catalogue intégré Spark | Réalisé |
| Hive Metastore | Catalogue externe centralisé | Non déployé |
| Project Nessie | Catalogue versionné | Non déployé |
| Apache Iceberg | Format de table | Non établi |

Le catalogue intégré Spark est actuellement suffisant pour les traitements et démonstrations réalisés.

L'ajout d'un catalogue externe ne serait justifié que par des besoins supplémentaires de partage, de gouvernance ou d'interopérabilité.



## 9. Orchestration des traitements

### 9.1. Organisation actuelle

Les traitements sont organisés en scripts Python indépendants.

Les fichiers identifiés sont :

```text
scripts/
|
+-- etape4_nettoyage.py
+-- etape5_6_transformations_silver.py
+-- etape7_gold.py
+-- etape9_quality_control.py
+-- test_spark.py
```

Chaque script correspond à une étape distincte.

Les traitements sont destinés à être exécutés dans un ordre cohérent avec leurs dépendances.

Il n'existe toutefois pas de script central qui pilote automatiquement l'ensemble de la chaîne.

L'enchaînement des traitements est actuellement manuel.

### 9.2. Mécanisme d'exécution

Les scripts peuvent être exécutés en invoquant explicitement l'interpréteur Python de TP3.

Par exemple :

```bash
cd ~/retail-intelligence/tp3

./retail_intel_tp3_venv/bin/python scripts/etape4_nettoyage.py
```

Cette commande illustre le mode d'exécution possible du script. Elle ne doit pas être interprétée comme une nouvelle exécution effectuée pendant la documentation.

Les scripts ne possèdent pas le bit d'exécution Linux (`644`), mais cela n'empêche pas leur lancement avec l'interpréteur Python.

### 9.3. Absence d'orchestration centralisée

Les vérifications réalisées ont confirmé :
- l'existence de scripts indépendants 
- l'absence d'appel central entre les scripts métier dans les recherches effectuées 
- l'absence de tâche cron propre au projet 
- l'absence de timer systemd lié à Retail Intelligence.

Un timer systemd utilisateur a été observé, mais il concerne le nettoyage du cache Launchpadlib et n'est pas lié aux traitements du TP3.

L'orchestration actuelle est donc manuelle et non automatisée.

### 9.4. Apache Airflow

Apache Airflow est une plateforme open source d'orchestration de workflows.

Elle permet de définir des DAG, c'est-à-dire des graphes de dépendances entre tâches.

Dans Retail Intelligence, Airflow pourrait être utilisé pour organiser les étapes :

```text
Nettoyage
   |
   v
Transformations Silver
   |
   v
Production Gold
   |
   v
Contrôle qualité
```

Airflow permettrait notamment :
- de programmer les exécutions 
- de suivre les dépendances 
- de consulter les journaux 
- de détecter les erreurs 
- de faciliter les reprises après échec.

Airflow n'est pas installé dans l'environnement vérifié.

### 9.5. Comparaison des mécanismes

| Mécanisme | Rôle | Statut |
|---|---|---|
| Scripts Python indépendants | Exécution des traitements | Réalisé |
| Enchaînement manuel | Ordonnancement actuel | Réalisé |
| Script central | Orchestration globale | Non présent |
| Cron | Planification périodique | Non utilisé pour le projet |
| systemd | Gestion de services et timers | Étudié |
| Apache Airflow | Orchestration de workflows | Non déployé |

### 9.6. Évolution proposée

Une évolution consisterait à conserver les scripts métier existants et à introduire un mécanisme central d'orchestration.

Airflow pourrait être étudié si le projet nécessite une gestion plus avancée des dépendances, des reprises et du suivi.

Pour un environnement pédagogique plus simple, un script Python central ou une planification système pourrait également être envisagé.

Il s'agit de possibilités d'évolution et non de composants actuellement utilisés.



## 10. Sécurité locale

### 10.1. Permissions des répertoires

Les permissions des principaux répertoires TP3 ont été vérifiées.

Les répertoires suivants présentent tous les permissions `755` :

- répertoire principal TP3 
- `data/` 
- `data/bronze/` 
- `data/silver/` 
- `data/silver-transformed/` 
- `data/gold/` 
- `data/quality/` 
- `data/quarantine/` 
- `notebooks/` 
- `scripts/`.

La permission `755` signifie :

| Catégorie | Droits |
|---|---|
| Propriétaire | Lecture, écriture et traversée |
| Groupe | Lecture et traversée |
| Autres | Lecture et traversée |

### 10.2. Permissions des fichiers

Les scripts Python inspectés présentent les permissions `644`.

Les deux fichiers sources Bronze présentent également les permissions `644` :

- `store_sales.dat` 
- `inventory.dat`.

La permission `644` signifie :

| Catégorie | Droits |
|---|---|
| Propriétaire | Lecture et écriture |
| Groupe | Lecture seule |
| Autres | Lecture seule |

Les fichiers sont donc accessibles en lecture aux autres utilisateurs, mais leur modification n'est pas autorisée par ces permissions pour les utilisateurs autres que le propriétaire.

Cela constitue une protection élémentaire contre les modifications effectuées par d'autres comptes.

Il ne s'agit cependant pas d'une protection absolue : le propriétaire conserve ses droits de modification.

### 10.3. Gestion des comptes Linux

L'environnement repose sur les permissions classiques du système de fichiers Linux.

Les vérifications ne permettent pas d'établir l'existence :
- de comptes dédiés aux différentes zones 
- de groupes Linux spécifiques à chaque couche 
- d'une politique formalisée de séparation des responsabilités.

Une évolution pourrait consister à mettre en place des groupes distincts pour les traitements, les utilisateurs analytiques et l'administration.

Les permissions pourraient alors être adaptées aux responsabilités de chacun.

### 10.4. Gestion des secrets

Une recherche a été effectuée dans les fichiers de configuration, les scripts et les notebooks TP3.

Aucun fichier correspondant aux noms et extensions recherchés n'a été identifié dans le périmètre inspecté.

Aucune référence aux mots-clés suivants n'a été détectée :

- `password` 
- `passwd` 
- `secret` 
- `api_key` 
- `access_token` 
- `client_secret` 
- `credentials`.

Cette recherche ne démontre pas l'absence absolue de secrets. Elle indique seulement qu'aucune gestion explicite correspondant aux recherches effectuées n'a été identifiée.

Une évolution pourrait prévoir :
- l'utilisation de variables d'environnement 
- la séparation des paramètres de configuration et du code 
- la limitation des permissions sur les fichiers sensibles 
- l'utilisation d'un gestionnaire de secrets lorsque des services externes seront intégrés.

### 10.5. Séparation des environnements

Les environnements Python TP3 et TP4 sont situés dans deux répertoires distincts.

Cette séparation limite les risques de conflits entre dépendances.

Elle permet également de conserver l'environnement TP3 indépendant des évolutions effectuées dans TP4.

Il s'agit d'une séparation des environnements d'exécution Python et non d'une isolation complète des données ou des utilisateurs.

### 10.6. Sauvegardes

Une recherche de répertoires dédiés aux sauvegardes a été effectuée dans le projet.

Aucun répertoire explicitement nommé `backup`, `backups`, `sauvegarde` ou `archive` n'a été identifié dans le périmètre inspecté.

Les répertoires `output`, `reports` et `logs` sont présents, mais leur existence ne constitue pas une preuve de sauvegarde.

Aucune stratégie de sauvegarde automatisée ni aucun mécanisme de restauration testé n'a été établi.

Une évolution pourrait prévoir :
- des sauvegardes périodiques des données 
- la conservation des scripts et notebooks 
- une copie sur un support distinct 
- une politique de rétention 
- des tests de restauration.

### 10.7. Bilan de sécurité

| Élément | Situation |
|---|---|
| Permissions Linux des répertoires | Réalisé |
| Permissions Linux des fichiers inspectés | Réalisé |
| Séparation des environnements Python | Réalisé |
| Gestion centralisée des secrets | Non établie |
| Comptes dédiés aux différentes zones | Non établis |
| Sauvegardes automatisées | Non établies |
| Tests de restauration | Non établis |

---

## 11. Démonstration du traitement local utilisé dans le projet

### 11.1. Objectif

Le socle obligatoire du parcours B demande une démonstration du traitement local déjà utilisé.

Les scripts métier transmis permettent de décrire cette démonstration à partir du traitement réel de Retail Intelligence.

La démonstration s'appuie sur la chaîne suivante :

1. Lecture des données sources.
2. Nettoyage et contrôle qualité.
3. Transformation des données.
4. Production du jeu Gold.
5. Contrôle du résultat analytique.

Il est important de distinguer la démonstration du fonctionnement du code et les résultats d'exécution effectivement vérifiés.

### 11.2. Lecture et nettoyage

Le script utilisé est :

`etape4_nettoyage.py`

Il lit les fichiers Bronze et applique les conversions et contrôles qualité.

Les sorties sont matérialisées dans :
- Silver 
- Quarantine 
- Quality.

Le script contient des instructions d'écriture en mode `overwrite`.

Il ne doit donc pas être relancé uniquement pour illustrer le traitement sans autorisation explicite, car il pourrait remplacer les résultats existants.

### 11.3. Transformations métier

Le script utilisé est :

`etape5_6_transformations_silver.py`

Il lit les données Silver et produit les sept jeux transformés.

Il utilise également le mode `overwrite` lors de l'écriture des résultats.

Le script comprend une vérification par relecture des fichiers Parquet produits.

### 11.4. Production Gold

Le script utilisé est :

`etape7_gold.py`

Il lit le jeu `sales_by_store` et produit `sales_performance_by_store`.

Le résultat est contrôlé après écriture par une relecture et une comparaison des données.

Le jeu Gold déjà présent dans l'environnement a été lu avec Spark sans erreur.

Le nombre de lignes vérifié est de 12.

### 11.5. Contrôle qualité final

Le script utilisé est :

`etape9_quality_control.py`

Il vérifie notamment la cohérence des indicateurs Gold, les clés magasin et la réconciliation avec les données sources.

Le script génère un rapport CSV dans `reports/quality/`.

Il comporte des opérations d'écriture de rapport et de création de répertoire.

Il doit donc être considéré comme un traitement actif et non comme une simple commande de consultation.

### 11.6. Résultat de la démonstration Spark SQL

Une démonstration complémentaire a déjà été exécutée avec Spark SQL.

Le jeu Gold a été chargé et exposé sous forme de vue temporaire.

La requête suivante a été exécutée :

```sql
SELECT
    store_sk,
    revenue_rank,
    total_revenue_inc_tax,
    revenue_share_pct
FROM sales_performance_by_store
ORDER BY revenue_rank
```

Les 12 magasins ont été retournés dans l'ordre de leur classement.

Le magasin classé premier possède :
- la clé magasin 7 
- le rang 1 
- un chiffre d'affaires TTC de 103384198.80 
- une part de chiffre d'affaires de 8.6 %.

Cette démonstration confirme le fonctionnement du moteur Spark SQL sur les résultats Gold.

### 11.7. Synthèse des preuves

| Démonstration | Résultat |
|---|---|
| Lecture des données Bronze par le code métier | Définie dans le script |
| Nettoyage des données | Défini dans le script |
| Production de Silver | Définie dans le script |
| Production de Silver-transformed | Définie dans le script |
| Production de Gold | Définie dans le script |
| Contrôle qualité final | Défini dans le script |
| Lecture effective du jeu Gold | Vérifiée |
| Schéma Gold | Vérifié |
| Nombre de lignes Gold | 12, vérifié |
| Requête Spark SQL | Exécutée avec succès |

La consultation des scripts et la vérification du résultat Gold ne doivent pas être confondues avec une nouvelle exécution complète du pipeline.

Aucune nouvelle exécution destructive n'a été effectuée pour produire cette documentation.


## 12. Schéma argumenté de l'architecture locale

### 12.1. Architecture réellement utilisée

L'architecture actuelle repose sur les composants suivants :

```text
                 ENVIRONNEMENT LINUX
                         |
                         v
              SYSTEME DE FICHIERS LOCAL
                         |
                         v
                  DATA TP3
                         |
             +-----------+-----------+
             |                       |
             v                       v
           BRONZE                 AUTRES ZONES
             |
             v
      ETAPE 4 - NETTOYAGE
             |
       +-----+---------+
       |       |       |
       v       v       v
     SILVER QUALITY QUARANTINE
       |
       v
 ETAPES 5 ET 6 - TRANSFORMATIONS
       |
       v
 SILVER-TRANSFORMED
       |
       v
 ETAPE 7 - PRODUCTION GOLD
       |
       v
     GOLD
       |
       v
 ETAPE 9 - CONTROLE QUALITE
       |
       v
 RAPPORT CSV

   MOTEUR DE TRAITEMENT :
   APACHE SPARK / PYSPARK

   REQUETES ANALYTIQUES :
   SPARK SQL

   CATALOGUE :
   SPARK_CATALOG (IN-MEMORY)

   FORMAT DE FICHIERS :
   PARQUET / SNAPPY

   ORCHESTRATION :
   ENCHAINEMENT MANUEL
```

### 12.2. Justification des choix

Le système de fichiers Linux constitue le support de stockage réellement disponible et utilisé.

L'organisation en répertoires permet de matérialiser les différentes étapes de traitement.

Parquet permet de conserver les résultats analytiques dans un format adapté à Spark.

Spark et PySpark assurent les transformations et les agrégations métier.

Spark SQL permet d'interroger les jeux de données sans nécessiter un moteur SQL externe.

Le catalogue intégré Spark fournit le mécanisme de gestion des métadonnées utilisé dans l'environnement vérifié.

Enfin, les scripts indépendants permettent de réaliser les différentes étapes du traitement, même en l'absence d'un orchestrateur central.

### 12.3. Architecture cible proposée

Une évolution possible pourrait intégrer :

- MinIO pour le stockage objet 
- Iceberg pour la gestion des tables 
- Hive Metastore ou Nessie pour le catalogue 
- Trino pour les requêtes SQL indépendantes 
- Airflow pour l'orchestration.

Ces composants ne sont pas nécessaires pour démontrer le fonctionnement de l'architecture actuelle.

Ils permettraient néanmoins d'envisager une plateforme plus évolutive, mieux centralisée et adaptée à plusieurs moteurs analytiques.


## 13. Tableau récapitulatif des composants

| Composant | Fonction | Statut |
|---|---|---|
| Linux | Système d'exploitation | Réalisé |
| Système de fichiers local | Stockage | Réalisé |
| Bronze | Données sources | Réalisé |
| Silver | Données nettoyées | Réalisé |
| Silver-transformed | Données transformées | Réalisé |
| Gold | Résultats analytiques | Réalisé |
| Quality | Résultats de contrôle | Réalisé |
| Quarantine | Données mises à l'écart | Réalisé |
| Apache Parquet | Format de fichiers | Réalisé |
| Snappy | Compression | Réalisé |
| MinIO | Stockage objet | Non déployé |
| Apache Iceberg | Format de table | Étudié |
| Apache Spark | Moteur de traitement | Réalisé |
| PySpark | Interface Python | Réalisé |
| Spark SQL | Requêtes analytiques | Réalisé |
| Trino | Moteur SQL indépendant | Étudié |
| spark_catalog | Catalogue Spark | Réalisé |
| Hive Metastore | Catalogue externe | Non déployé |
| Project Nessie | Catalogue versionné | Non déployé |
| Scripts Python | Traitements métier | Réalisé |
| Orchestration manuelle | Enchaînement des scripts | Réalisé |
| Apache Airflow | Orchestration automatisée | Non déployé |
| Cron | Planification du projet | Non utilisé |
| Permissions Linux | Contrôle d'accès | Réalisé |
| Gestionnaire de secrets | Protection centralisée | Non établi |
| Sauvegarde automatisée | Protection des données | Non établie |

---

## 14. Comparaison entre le parcours local et la cible Azure

Les parcours local et Azure répondent au même objectif : construire une plateforme permettant de stocker, transformer et exploiter des données analytiques.

La différence réside principalement dans les services et infrastructures utilisés.

| Fonction | Parcours B local | Cible Azure étudiée |
|---|---|---|
| Stockage | Système de fichiers Linux | Azure Data Lake Storage Gen2 |
| Organisation des données | Répertoires locaux | Conteneurs et répertoires ADLS |
| Traitement | Apache Spark / PySpark | Services de traitement Azure étudiés |
| Requêtes SQL | Spark SQL | Azure Synapse Analytics |
| Orchestration | Scripts manuels | Azure Data Factory |
| Catalogue | spark_catalog | Catalogue à définir selon la cible |
| Identité | Comptes Linux | Microsoft Entra ID |
| Autorisations | Permissions Linux | RBAC et ACL |
| Exploitation | Environnement local | Infrastructure cloud |

### 14.1. Parcours local

Le parcours local s'appuie sur des composants déjà disponibles.

Il permet de réaliser les traitements analytiques sans nécessiter de déploiement cloud.

Il présente notamment les avantages suivants :
- maîtrise de l'environnement 
- absence de dépendance obligatoire à Azure 
- utilisation de technologies open source 
- possibilité de réaliser les traitements hors cloud 
- maîtrise directe des fichiers et des répertoires.

Ses limites concernent notamment l'absence d'orchestration centralisée, de catalogue externe et de stratégie de sauvegarde établie.

### 14.2. Parcours Azure

Les étapes précédentes de l'UC-07 ont étudié une architecture reposant sur ADLS Gen2, Azure Data Factory, Synapse Analytics et les mécanismes de sécurité Azure.

Cette architecture constitue une cible théorique.

Aucun compte de stockage, conteneur, pipeline, workspace Synapse, rôle RBAC ou ACL n'a été effectivement déployé dans le cadre des vérifications documentées.

Le parcours Azure ne doit donc pas être présenté comme une infrastructure opérationnelle.

### 14.3. Complémentarité des parcours

Le parcours local permet de comprendre et de démontrer les principes techniques de stockage, de transformation et d'analyse.

Le parcours Azure montre comment ces mêmes fonctions pourraient être transposées vers des services cloud managés.

Les deux approches sont complémentaires : les traitements et l'organisation logique des données étudiés localement constituent une base pour réfléchir à leur transposition vers Azure.


## 15. Conclusion

L'étude de l'étape 8 du cas d'utilisation UC-07 a permis de décrire une architecture analytique locale fondée sur Linux, Apache Spark, PySpark, Spark SQL et le stockage Parquet.

Le système de fichiers Linux constitue le support de stockage effectivement utilisé. Les données sont organisées dans des répertoires correspondant aux espaces Bronze, Silver, Silver-transformed et Gold, auxquels s'ajoutent les espaces complémentaires Quality et Quarantine.

L'analyse des scripts métier a permis de préciser les responsabilités des différentes étapes du pipeline.

Le nettoyage transforme les fichiers sources en jeux Silver et isole les anomalies dans Quarantine. Les transformations suivantes produisent plusieurs jeux de données agrégés et enrichis. L'étape Gold répond à une question métier portant sur la performance commerciale des magasins. Enfin, une étape de contrôle qualité vérifie la cohérence des résultats.

Le fonctionnement de Spark a été confirmé par la lecture effective du jeu Gold, comportant 12 lignes et 14 colonnes. Une requête Spark SQL a également permis d'obtenir le classement des magasins selon leur chiffre d'affaires.

La configuration du catalogue confirme l'utilisation de `spark_catalog` avec une implémentation en mémoire.

L'organisation actuelle des traitements repose sur des scripts Python indépendants dont l'enchaînement est manuel. Aucun orchestrateur central ni mécanisme de planification propre au projet n'a été établi.

Les vérifications de sécurité ont mis en évidence des permissions Linux classiques et une séparation physique des environnements Python TP3 et TP4. En revanche, aucune gestion centralisée des secrets ni stratégie de sauvegarde automatisée n'a été établie.

MinIO, Apache Iceberg, Trino, Hive Metastore, Nessie et Airflow constituent des possibilités d'évolution étudiées, mais ne font pas partie des composants effectivement déployés dans l'environnement vérifié.

En conclusion, le parcours local démontre qu'une plateforme analytique peut fonctionner avec des composants open source, sans dépendre obligatoirement de services cloud.

Il constitue une base technique fonctionnelle pour le projet Retail Intelligence et permet d'identifier plusieurs pistes d'industrialisation : stockage objet, gestion avancée des tables, catalogue partagé, moteur SQL indépendant, orchestration automatisée et renforcement de la sécurité.

La cible Azure étudiée dans les étapes précédentes représente une évolution possible de cette architecture, mais ne correspond pas à un déploiement effectivement réalisé.