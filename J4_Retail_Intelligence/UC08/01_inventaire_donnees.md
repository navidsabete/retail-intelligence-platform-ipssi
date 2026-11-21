## Étape 1 - Inventaire des jeux de données

## 1. Environnement technique

L'inventaire a été réalisé dans l'environnement virtuel `retail_intel_tp4_venv`, en utilisant les données produites lors du TP3.

| Composant | Version |
|---|---:|
| Python | 3.12.3 |
| Java | OpenJDK 21.0.13.1 |
| PySpark | 4.3.0 |
| Apache Spark | 4.3.0 |
| Pandas | 3.1.1 |
| Matplotlib | 3.11.2 |
| JupyterLab | 4.6.6 |

Le répertoire de données utilisé est `retail-intelligence/tp3/data`. Le TP4 consulte les données existantes sans les modifier ni les dupliquer.

## 2. Inventaire des jeux réellement disponibles

Les jeux ci-dessous ont été repérés dans les répertoires Silver, Silver transformé et Gold du TP3.

| Jeu de données | Zone | Format | Granularité | Usage prévu |
|---|---|---|---|---|
| `store_sales` | Silver | Parquet, fichiers Snappy observés | Une ligne de vente détaillée ; dimensions de vente, article, client, magasin, date et ticket | Source détaillée pour les analyses commerciales et la traçabilité des transformations |
| `inventory` | Silver | Parquet, fichiers Snappy observés | Une ligne de stock par date, article et entrepôt | Analyse des quantités en stock et source des indicateurs d'inventaire |
| `sales_by_store_date` | Silver transformé | Parquet, fichiers Snappy observés | Un magasin par date | Analyse de l'évolution des ventes et comparaison temporelle entre magasins |
| `sales_by_item_date` | Silver transformé | Parquet | Un article par date | Analyse des ventes par produit et de leur évolution |
| `inventory_by_item_date` | Silver transformé | Parquet | Un article par date, tous entrepôts agrégés | Analyse des quantités disponibles par article et par date |
| `sales_inventory_by_item_date` | Silver transformé | Parquet | Un article par date, ventes enrichies du stock | Analyse croisée des ventes et des stocks, sous réserve des limites de rapprochement constatées |
| `sales_by_store` | Silver transformé | Parquet | Un magasin | Agrégats commerciaux par magasin et source du jeu Gold |
| `sales_performance_by_store` | Gold | Parquet avec compression Snappy | Un magasin | Indicateurs de performance, classement et part du chiffre d'affaires |

**Jeux principaux sélectionnés pour le TP4 :**

- `sales_by_store_date` en Silver transformé : adapté à l'analyse temporelle des ventes par magasin.
- `sales_performance_by_store` en Gold : adapté à l'analyse comparative des performances commerciales et des KPI.

Les jeux `store_sales` et `inventory` sont conservés dans l'inventaire comme sources Silver disponibles. Ils permettent de documenter l'origine des transformations et de revenir aux données détaillées si nécessaire.

## 3. Jeu Silver sélectionné : `sales_by_store_date`

### 3.1 Nom exact et emplacement

- Nom exact : `sales_by_store_date`
- Zone : Silver transformé
- Chemin : `data/silver-transformed/sales_by_store_date/`
- Nombre de lignes observé : **21 430**
- Nombre de colonnes : **12**

### 3.2 Provenance

Ce jeu est issu des données de ventes `store_sales`, disponibles dans la zone Silver à l'emplacement :

`data/silver/store_sales/`

La source initiale du traitement est le jeu de ventes TPCx-BB, dont le fichier Bronze est identifié dans les métadonnées comme `store_sales.dat`.

Le jeu Silver transformé agrège les données de vente par magasin et par date. Les métadonnées observées indiquent notamment :

- `_source_dataset` : `store_sales`
- `_source_original_file` : fichier source de ventes
- `_processing_stage` : `TP3-Retail-Intelligence-Etapes5-6`

### 3.3 Format

Le jeu est stocké au format **Parquet**. Des fichiers portant l'extension `.snappy.parquet` ont été observés dans les données Silver transformées.

La lecture est réalisée avec PySpark à l'aide de `spark.read.parquet()`.

### 3.4 Schéma observé

| Colonne | Type Spark | Description |
|---|---|---|
| `store_sk` | long | Identifiant technique du magasin |
| `date_sk` | long | Identifiant technique de la date |
| `total_revenue_inc_tax` | decimal(17,2) | Chiffre d'affaires TTC agrégé |
| `total_net_paid` | decimal(17,2) | Montant net payé agrégé |
| `total_net_profit` | decimal(17,2) | Profit net agrégé |
| `total_quantity_sold` | long | Quantité totale vendue |
| `number_of_sales_lines` | long | Nombre de lignes de vente |
| `number_of_tickets` | long | Nombre de tickets |
| `_grain` | string | Description de la granularité |
| `_source_dataset` | string | Jeu source |
| `_source_original_file` | string | Fichier d'origine |
| `_processing_stage` | string | Étape de traitement |

### 3.5 Granularité

La granularité observée est :

**Une ligne par magasin et par date.**

La combinaison `(store_sk, date_sk)` a été testée comme clé candidate. Le contrôle de doublons a retourné **0 combinaison dupliquée**.

Ce résultat confirme l'absence de doublons sur cette combinaison dans le test réalisé. Le contrôle des valeurs nulles sur les deux colonnes doit également être conservé dans les vérifications finales avant de considérer cette clé comme définitivement validée.

### 3.6 Contrôles qualité disponibles

Les contrôles et éléments de traçabilité disponibles sont :

- présence des colonnes métier et des métadonnées
- typage des mesures financières en `decimal` et des compteurs en `long`
- description de la granularité dans `_grain` 
- identification de la source dans `_source_dataset` 
- test de doublons sur `(store_sk, date_sk)`, avec zéro doublon observé.

Les contrôles de qualité détaillés du jeu Silver transformé ne sont pas documentés ici par un rapport chiffré dédié. Il ne faut donc pas assimiler le test de doublons réalisé à une validation complète de toutes les règles métier.

### 3.7 Pertinence pour l'analyse

Ce jeu est adapté à une analyse de l'évolution des ventes dans le temps, car il associe les indicateurs commerciaux à un magasin et à une date.

Il permet notamment de :

- suivre le chiffre d'affaires TTC par magasin et par date 
- comparer les volumes de ventes entre magasins 
- étudier l'évolution des quantités vendues 
- analyser les montants nets payés et les profits nets agrégés 
- préparer des visualisations temporelles et comparatives

Il constitue ainsi le jeu Silver principal pour les analyses temporelles du TP4.

## 4. Jeu Gold sélectionné : `sales_performance_by_store`

### 4.1 Nom exact et emplacement

- Nom exact : `sales_performance_by_store`
- Zone : Gold
- Chemin : `data/gold/sales_performance_by_store/`
- Nombre de lignes observé : **12**
- Nombre de colonnes : **14**

### 4.2 Provenance

Selon la documentation de l'étape 7 du TP3 (`UC06/07_jeu_gold.md`), le jeu Gold est construit à partir du jeu Silver transformé :

`data/silver-transformed/sales_by_store/`

La source contient les agrégations commerciales par magasin. Le traitement Gold reprend ces mesures et ajoute des indicateurs analytiques permettant de comparer les magasins.

Cette provenance est également cohérente avec le script `quality_check_gold.py`, qui compare explicitement le jeu Gold à `sales_by_store`.

### 4.3 Format

Le jeu est enregistré au format **Parquet avec compression Snappy**.

La documentation du TP3 indique que le jeu a été relu après écriture et que le nombre de lignes ainsi que les données ont été comparés avec le résultat avant écriture.

### 4.4 Schéma observé

| Colonne | Type Spark | Description |
|---|---|---|
| `store_sk` | long | Identifiant technique du magasin |
| `revenue_rank` | integer | Rang du magasin selon le chiffre d'affaires TTC |
| `is_best_revenue_store` | boolean | Indique si le magasin est classé premier |
| `total_revenue_inc_tax` | decimal(17,2) | Chiffre d'affaires TTC du magasin |
| `global_revenue_inc_tax` | decimal(27,2) | Chiffre d'affaires TTC global |
| `revenue_share_pct` | double | Part du magasin dans le chiffre d'affaires global |
| `total_net_paid` | decimal(17,2) | Montant net payé |
| `total_net_profit` | decimal(17,2) | Profit net agrégé |
| `total_quantity_sold` | long | Quantité totale vendue |
| `number_of_sales_lines` | long | Nombre de lignes de vente |
| `number_of_tickets` | long | Nombre de tickets |
| `_gold_dataset` | string | Nom du jeu Gold |
| `_business_grain` | string | Description de la granularité métier |
| `_processing_stage` | string | Couche de traitement |

### 4.5 Granularité

La granularité métier est :

**Une ligne par magasin, identifié par `store_sk`.**

Le jeu contient 12 lignes correspondant aux 12 magasins présents dans le jeu Silver source.

Les contrôles qualité ont confirmé :

- l'absence de valeurs nulles sur `store_sk` 
- l'unicité de `store_sk` 
- l'absence de doublons à la granularité d'un magasin.

`store_sk` est donc la clé candidate du jeu Gold, validée par les contrôles exécutés.

### 4.6 Indicateurs et règles de calcul

Les indicateurs analytiques ajoutés sont :

- `revenue_rank` : classement des magasins par chiffre d'affaires TTC décroissant 
- `is_best_revenue_store` : indicateur du magasin classé premier 
- `global_revenue_inc_tax` : somme des chiffres d'affaires TTC de tous les magasins 
- `revenue_share_pct` : part du chiffre d'affaires du magasin dans le chiffre d'affaires global.

La part du chiffre d'affaires est calculée selon la formule :

Part (%) = (CA TTC du magasin / CA TTC global) × 100.

Le classement est calculé avec la fonction `rank()` de PySpark. En cas d'égalité, plusieurs magasins peuvent donc obtenir le même rang.

### 4.7 Contrôles qualité disponibles

Le rapport `reports/quality/quality_report_gold.csv` contient **44 contrôles PASS et 1 contrôle WARN**, sans contrôle FAIL signalé dans le bilan communiqué.

Les contrôles PASS portent notamment sur :

- le volume attendu de 12 lignes 
- la présence des colonnes obligatoires 
- la complétude des colonnes métier contrôlées 
- la validité des types 
- l'unicité et la non-nullité de `store_sk` 
- la validité des rangs 
- la cohérence de l'indicateur `is_best_revenue_store` 
- la cohérence du chiffre d'affaires global 
- la somme des parts de chiffre d'affaires, proche de 100 % 
- la réconciliation des six mesures entre Silver transformé et Gold 
- la comparaison des mesures par magasin, sans écart observé.

Le contrôle WARN concerne l'intégrité référentielle avec les ventes Silver.

**Explication du WARN :** le script `quality_check_gold.py` recherche une colonne nommée `store_sk` dans `data/silver/store_sales/`. Or le schéma réellement observé de ce jeu Silver contient la colonne `ss_store_sk`, et non `store_sk`. Le contrôle ne peut donc pas effectuer la comparaison avec le nom de colonne attendu.

Ce WARN révèle une incompatibilité de nommage dans le contrôle, et non la preuve d'une incohérence entre les magasins. Pour compléter la vérification, il faudra adapter le script afin d'utiliser `ss_store_sk` ou de le renommer en `store_sk` dans une vue de contrôle, puis relancer le test.

### 4.8 Résultats observés et pertinence métier

Le chiffre d'affaires TTC global des 12 magasins est de **1 202 218 083,00**.

Le classement observé est notamment le suivant :

- Magasin 7 : premier, avec 103 384 198,80 de chiffre d'affaires TTC 
- Magasin 4 : deuxième, avec 101 130 648,13 
- Magasin 9 : troisième, avec 101 109 360,86 
- Magasin 2 : dernier, avec 98 249 685,02.

Le magasin 7 représente environ 8,60 % du chiffre d'affaires TTC global.

Ce jeu est adapté à une analyse métier orientée décision, car il permet de comparer directement les magasins et d'identifier ceux qui contribuent le plus au chiffre d'affaires.

Il permet notamment de construire :

- un classement des magasins par chiffre d'affaires 
- un KPI de chiffre d'affaires global 
- un KPI de part du chiffre d'affaires par magasin 
- un indicateur identifiant le magasin en première position 
- un tableau de bord de comparaison des performances commerciales.

Le classement porte sur le chiffre d'affaires TTC. Il ne constitue pas un classement de rentabilité. Le profit net agrégé est négatif dans les résultats communiqués ; son interprétation doit s'appuyer sur la définition métier et la formule utilisées dans le TP3.

## 5. Autres jeux Silver disponibles et points de vigilance

### 5.1 Source détaillée des ventes : `store_sales`

- Chemin : `data/silver/store_sales/`
- Volume observé : **667 579 lignes**
- Nombre de colonnes : **77**
- Format : Parquet, fichiers Snappy observés.

Le schéma comprend notamment les clés de date, d'article, de client et de magasin (`ss_sold_date_sk`, `ss_item_sk`, `ss_customer_sk`, `ss_store_sk`), les informations de ticket et les mesures de vente.

Il contient également des colonnes techniques de contrôle : valeurs brutes `_raw_*`, indicateurs `invalid_cast_*` et drapeaux tels que `flag_missing_required`, `flag_invalid_cast`, `flag_quantity_negative`, `flag_zero_unit_sales_price`, `flag_zero_net_paid`, `flag_profit_negative` et `flag_duplicate_candidate`.

Ce jeu constitue la source détaillée des agrégations de ventes. Il est utile pour les analyses au niveau des lignes de vente et pour examiner les règles de nettoyage.

### 5.2 Source détaillée des stocks : `inventory`

- Chemin : `data/silver/inventory/`
- Volume observé : **23 249 101 lignes**
- Nombre de colonnes : **17**
- Format : Parquet, fichiers Snappy observés.

Les principales colonnes métier sont :

- `inv_date_sk`
- `inv_item_sk`
- `inv_warehouse_sk`
- `inv_quantity_on_hand`.

Le schéma comprend également les colonnes `_raw_*`, les indicateurs `invalid_cast_*` et les drapeaux `flag_missing_required`, `flag_invalid_cast`, `flag_quantity_negative` et `flag_duplicate_candidate`.

La granularité attendue au regard des dimensions disponibles est une observation de stock par date, article et entrepôt. Cette granularité doit être confirmée par un test de doublons sur la combinaison de ces trois clés si le jeu est utilisé directement dans une analyse.

### 5.3 Jeu croisé ventes et stocks : `sales_inventory_by_item_date`

Ce jeu comporte **565 428 lignes et 16 colonnes**. Il associe des indicateurs de ventes et de stocks au niveau article/date.

Un contrôle communiqué a donné les résultats suivants :

| Indicateur | Nombre de lignes |
|---|---:|
| Total | 565 428 |
| `flag_inventory_not_matched = true` | 484 701 |
| `flag_inventory_not_matched = false` | 80 727 |
| `total_quantity_on_hand` nul | 484 701 |

Ainsi, **484 701 lignes, soit environ 85,7 %**, sont signalées comme non rapprochées avec un stock et présentent une quantité en stock nulle au sens SQL (`NULL`).

Ces valeurs `NULL` ne doivent pas être interprétées comme un stock égal à zéro. Elles indiquent ici une absence de correspondance dans le rapprochement réalisé.

Ce jeu peut être utile pour une analyse ventes/stocks, mais son utilisation comme source principale de KPI de disponibilité ou de rupture doit être précédée d'une investigation sur les clés de jointure, la couverture des dates et des articles, ainsi que sur la signification des non-correspondances.

## 6. Synthèse de sélection pour le TP4

| Rôle | Jeu retenu | Justification |
|---|---|---|
| Silver principal | `sales_by_store_date` | Granularité magasin/date, indicateurs commerciaux agrégés, adapté aux analyses temporelles |
| Gold principal | `sales_performance_by_store` | Granularité magasin, classement, chiffre d'affaires global et part du CA, contrôles qualité documentés |

Cette sélection permet de couvrir deux niveaux d'analyse complémentaires :

1. **Analyse temporelle :** étudier l'évolution des ventes par magasin à partir de Silver.
2. **Analyse comparative :** comparer les performances commerciales des magasins à partir de Gold.

Les jeux détaillés `store_sales` et `inventory` restent des sources de référence pour approfondir les contrôles et expliquer les transformations. Le jeu croisé `sales_inventory_by_item_date` reste un candidat secondaire en raison du taux important de non-correspondances observé.

## 7. Conclusion

Les jeux `sales_by_store_date` et `sales_performance_by_store` sont les deux jeux retenus pour le TP4. Leur nom, leur emplacement, leur format, leur schéma, leur granularité et leur intérêt métier sont documentés à partir des données et des éléments du TP3 effectivement communiqués. Les limites de contrôle identifiées sont explicitement signalées afin de ne pas présenter comme validés des tests qui restent à effectuer.