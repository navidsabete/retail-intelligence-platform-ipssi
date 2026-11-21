# Projet fil rouge – Retail Intelligence Platform (IPSSI)

# J4

## Présentation

Ce dépôt regroupe les travaux réalisés lors de la quatrième journée du projet Retail Intelligence Platform, dans la continuité des traitements et de la structuration des données effectués pendant le J3.

- **UC-08 :** réalisation d’analyses métier, production de visualisations et formulation de constats à partir des données préparées lors du J3.
- **UC-07 :** étude de la transposition de l’architecture de données vers une architecture cible Azure et comparaison avec des solutions de l’écosystème Open Source.

L’objectif du J4 est de valoriser les données préparées en produisant des analyses exploitables par les utilisateurs métier, puis d’étudier les correspondances entre l’environnement technique existant et une architecture cible orientée cloud.

Les travaux UC-08 s’appuient sur les données du projet TPCx-BB. Les analyses sont réalisées à partir des jeux de données préparés, sans modification des données sources du TP3.

Les travaux UC-07 reposent sur l’observation de l’environnement existant et sur une étude comparative des composants d’architecture. Ils ne constituent pas un déploiement effectif d’une plateforme Azure ou d’une architecture Open Source complète.

## Organisation du dépôt

Les livrables du J4 sont organisés autour des 2 UCs :

```text
J4_Retail_Intelligence/
├── README.md
│
├── UC08/
│   ├── 01_inventaire_donnees.md
│   ├── 02_verification_kpi.md
│   ├── 03_statistiques_descriptives.md
│   ├── 04_analyses_metier.md
│   └── 05-06_visualisations_constats_metiers.md
│
├── UC07/
│   ├── 00_choix_parcours.md
│   ├── 01_identification_composants_azure.md
│   ├── 02_organisation_adls.md
│   ├── 03_role_hns.md
│   ├── 04_mise_en_oeuvre.md
│   ├── 05_securite.md
│   ├── 06_adf_azure_synapse.md
│   ├── 07_schema_architecture_azure.md
│   ├── 08_declinaison_sans_azure.md
│   ├── 09_comparaison_responsabilites.md
│   └── schema-architecture-azure.png
│
└── retail-intelligence/tp4/
    ├── notebooks/
    │   ├── 01_inventaire_jeux_donnees.ipynb
    │   ├── 02_verification_kpi.ipynb
    │   ├── 03_statistiques_descriptives.ipynb
    │   ├── 04_analyses_metier.ipynb    
    │   └── 05_visualisations.ipynb
    │
    ├── visualisations/
    │   ├── ca_ttc_par_magasin.png
    │   ├── synthese_ca_par_magasin.csv
    │   ├── top10_produits_quantites.png

```

## Périmètre technique

Les travaux du J4 reposent sur deux environnements distincts.

### Environnement TP3

Le TP3 constitue la base de préparation des données. Les composants constatés dans cet environnement sont :

| Composant | Version ou caractéristique |
|---|---|
| Système | Linux |
| Python | 3.12.3 |
| Apache Spark | 4.3.0 |
| PySpark | 4.3.0 |
| Pandas | 3.1.1 |
| Stockage | Système de fichiers Linux local |
| Format analytique | Parquet |
| Compression observée | Snappy pour le jeu Gold |

Les données préparées sont conservées dans les répertoires Bronze, Silver, Silver-transformed et Gold. Les répertoires Quality et Quarantine servent aux contrôles et à la conservation des éléments concernés par les anomalies.

### Environnement TP4

L'environnement utilisé pour les travaux du J4 est distinct de celui du TP3.

Les versions constatées sont les suivantes :

| Composant | Version constatée |
|---|---|
| Python | 3.12.3 |
| Apache Spark | 4.3.0 |
| PySpark | 4.3.0 |
| Pandas | 3.1.1 |
| Matplotlib | 3.11.2 |
| JupyterLab | 4.6.6 |

Matplotlib a été installé et utilisé dans le cadre des visualisations de l'UC-08 du TP4. Son utilisation ne doit pas être attribuée au TP3.

## Prérequis

Pour comprendre et reproduire les travaux du J4, les éléments suivants sont nécessaires :

- Les données préparées lors du TP3.
- Un environnement Python compatible avec les versions constatées.
- Apache Spark et PySpark pour les traitements concernés.
- Pandas pour la manipulation des données.
- Matplotlib pour les visualisations réalisées dans le cadre de l'UC-08.
- JupyterLab pour l'environnement de travail du TP4.
- Les livrables documentaires nécessaires à l'étude comparative de l'architecture UC-07.

L'environnement TP4 dispose de son propre environnement virtuel :

```text
~/retail-intelligence/tp4/retail_intel_tp4_venv/
```

Il reste distinct de l'environnement virtuel du TP3 :

```text
~/retail-intelligence/tp3/retail_intel_tp3_venv/
```

Cette séparation permet de conserver les dépendances et les contextes d'exécution propres à chaque journée.

## Emplacement et organisation des données

Les analyses métier du J4 exploitent les données préparées lors du TP3.

Deux jeux de données sont principalement mobilisés pour l'UC-08 :

| Jeu de données | Couche | Utilisation |
|---|---|---|
| `sales_performance_by_store` | Gold | Analyse des performances commerciales par magasin |
| `store_sales` | Silver | Analyse des produits vendus par magasin |

Le jeu `sales_performance_by_store` contient une ligne par magasin et regroupe les indicateurs nécessaires à l'analyse du chiffre d'affaires.

Le jeu `store_sales` permet de réaliser une analyse plus détaillée des quantités vendues par produit et par magasin.

Les visualisations utilisent également le jeu `sales_by_store_date` de la couche Silver transformée pour représenter le chiffre d'affaires par magasin.

Les données du TP3 sont exploitées sans modification. Les traitements et visualisations du J4 sont réalisés dans le contexte distinct du TP4.

## Paramètres nécessaires

Les analyses reposent sur plusieurs paramètres fonctionnels et techniques :

| Paramètre | Valeur ou description |
|---|---|
| Source principale des performances magasin | `sales_performance_by_store` |
| Source des ventes détaillées | `store_sales` |
| Source de la visualisation du CA par magasin | `sales_by_store_date` |
| Indicateur principal | Chiffre d'affaires TTC |
| Mesure complémentaire | Quantités vendues |
| Mesure complémentaire | Nombre de tickets |
| Regroupement principal | Magasin |
| Regroupement complémentaire | Magasin et produit |
| Classement des magasins | CA TTC décroissant |
| Classement des produits | Quantités vendues décroissantes |
| Bibliothèque de visualisation | Matplotlib |
| Environnement d'analyse | TP4 |

Les analyses portent sur la période complète disponible dans les jeux de données étudiés. Elles ne constituent donc pas une analyse d'évolution temporelle.

Pour l'UC-07, les paramètres de comparaison portent sur les responsabilités techniques de la plateforme : stockage, format de fichiers, gestion des tables, moteur de calcul, interrogation SQL, catalogue, orchestration, visualisation, sécurité et environnement d'exécution.

## Déroulement des travaux

Les travaux du J4 sont organisés selon les étapes des deux unités de compétences.

### UC-08 – Analyses métier et visualisations

#### 1. Réalisation des analyses métier

Trois analyses ont été réalisées à partir des données préparées lors du TP3.

**Analyse 1 – Quels magasins réalisent le meilleur chiffre d'affaires ?**

Cette analyse répond au besoin de la direction commerciale.

Elle utilise le jeu `sales_performance_by_store`, en couche Gold, et s'appuie notamment sur les champs :

- `store_sk`
- `total_revenue_inc_tax`
- `revenue_rank`
- `revenue_share_pct`

Les magasins sont classés selon leur chiffre d'affaires TTC décroissant. La part de chaque magasin est calculée par rapport au chiffre d'affaires TTC global.

Le chiffre d'affaires TTC global observé est de **1 202 218 083,00 unités monétaires**, réparti sur 12 magasins.

Le magasin 7 arrive en première position avec un chiffre d'affaires TTC de **103 384 198,80**, soit **8,60 %** du chiffre d'affaires global.

Le magasin 2 présente le chiffre d'affaires le plus faible, avec **98 249 685,02**, soit **8,17 %** du total.

Les résultats montrent une répartition relativement homogène du chiffre d'affaires entre les magasins.

**Analyse 2 – Quel est le chiffre d'affaires de mon magasin ?**

Cette analyse répond au besoin d'un responsable de magasin.

Elle utilise également le jeu `sales_performance_by_store`, avec les indicateurs suivants :

- `store_sk`
- `total_revenue_inc_tax`
- `total_net_paid`
- `total_quantity_sold`
- `number_of_tickets`

Le jeu Gold contient déjà une ligne par magasin. Les indicateurs peuvent donc être consultés directement, sans recalcul de l'agrégation.

L'analyse permet de comparer le chiffre d'affaires TTC, les quantités vendues et le nombre de tickets pour chacun des 12 magasins.

Les résultats correspondent à des cumuls sur la période complète disponible. Ils ne sont pas ventilés par jour ou par mois.

**Analyse complémentaire – Quels produits sont les plus vendus dans chaque magasin ?**

Cette analyse répond à un besoin complémentaire des responsables de magasin.

Elle utilise le jeu `store_sales`, en couche Silver, et s'appuie sur les champs :

- `ss_store_sk`
- `ss_item_sk`
- `ss_quantity`
- `ss_net_paid_inc_tax`

Les données sont regroupées par magasin et par produit. Les quantités vendues et les montants nets payés TTC sont ensuite agrégés pour établir les classements.

Les quatre références les plus vendues au niveau global sont :

| Rang | Produit | Quantités vendues |
|---:|---:|---:|
| 1 | 10000 | 454 954 |
| 2 | 10003 | 439 086 |
| 3 | 10001 | 420 138 |
| 4 | 10002 | 377 027 |

Ces quatre références occupent également les premières positions dans chacun des 12 magasins.

Les résultats montrent une forte présence des mêmes références dans les classements locaux. Le produit 10000 arrive en tête dans la majorité des magasins, tandis que le produit 10003 arrive en première position dans les magasins 1, 8, 10 et 11.

#### 2. Production des visualisations

Trois supports de visualisation ont été réalisés avec Matplotlib.

| Visualisation | Source | Objectif |
|---|---|---|
| Diagramme en barres verticales | `sales_by_store_date` | Comparer le chiffre d'affaires TTC des magasins |
| Diagramme en barres horizontales | `store_sales` | Identifier les dix produits les plus vendus |
| Tableau de synthèse | `sales_by_store_date` | Présenter le classement, le chiffre d'affaires et la part de chaque magasin |

Le premier graphique représente le chiffre d'affaires TTC cumulé par magasin. Il met en évidence le magasin 7 comme premier magasin et le magasin 2 comme dernier.

Le deuxième graphique présente les dix produits ayant enregistré les plus grandes quantités vendues. Il permet de distinguer les quatre premières références des produits suivants.

Le tableau de synthèse complète les graphiques en donnant accès aux valeurs exactes, au classement et à la part de chaque magasin dans le chiffre d'affaires global.

Ces supports facilitent la lecture des résultats et leur interprétation. Ils ne constituent toutefois pas, à eux seuls, un tableau de bord décisionnel complet.

#### 3. Formulation des constats métier

Les analyses permettent de formuler trois constats principaux.

**Constat 1 – Des chiffres d'affaires relativement proches entre les magasins**

Le magasin 7 réalise le chiffre d'affaires TTC le plus élevé, avec 103,38 millions d'unités monétaires. Le magasin 2 réalise le chiffre d'affaires le plus faible, avec 98,25 millions.

L'écart entre les deux magasins est de **5 134 513,78**.

Les parts de chiffre d'affaires restent proches, entre 8,17 % et 8,60 %. Cette répartition suggère une homogénéité relative des résultats commerciaux sur la période étudiée.

Une analyse complémentaire par période, par nombre de tickets, par quantités vendues et par coûts serait nécessaire pour expliquer les différences observées.

**Constat 2 – Quatre produits concentrent les plus grands volumes de vente**

Les références 10000, 10003, 10001 et 10002 occupent les quatre premières positions du classement global.

Le produit 10000 atteint 454 954 unités vendues, devant le produit 10003 avec 439 086 unités.

Ces références représentent les principaux volumes observés dans le jeu étudié. Il serait pertinent de rapprocher ces résultats du référentiel produit et des données de stock afin d'approfondir l'analyse.

**Constat 3 – Les classements locaux présentent des similitudes**

Les quatre références principales apparaissent dans les premières positions des classements de chacun des 12 magasins.

Cette observation montre que les produits les plus vendus au niveau global sont également très présents dans les résultats locaux.

Une analyse complémentaire par magasin et par période permettrait de mieux comprendre les variations de comportement entre les points de vente.

### UC-07 – Étude de la transposition de l'architecture

#### 4. Examen de l'architecture existante

L'environnement du TP3 repose sur un système de fichiers Linux local et sur des traitements réalisés avec Python, Spark et PySpark.

Les données sont organisées en plusieurs répertoires :

- `bronze/` : conservation des fichiers sources.
- `silver/` : données nettoyées et contrôlées.
- `silver-transformed/` : données transformées et agrégées.
- `gold/` : jeux de données orientés vers les besoins analytiques.
- `quality/` : éléments liés aux contrôles qualité.
- `quarantine/` : données mises à l'écart selon les règles de contrôle.

Les couches Bronze, Silver et Gold constituent les principales couches de traitement. Quality et Quarantine sont des espaces complémentaires et ne représentent pas des couches supplémentaires.

Le format Parquet est effectivement utilisé pour les données analytiques. Le catalogue Spark observé repose sur `spark_catalog` avec une implémentation en mémoire.

Les requêtes SQL sont réalisées avec Spark SQL. Une vue temporaire `sales_performance_by_store` a notamment été utilisée pour interroger les indicateurs du jeu Gold.

Les traitements sont répartis entre plusieurs scripts Python et notebooks. Leur enchaînement reste manuel : aucune orchestration automatique complète du projet n'a été établie.

#### 5. Comparaison des composants et étude de la cible Azure

L'étude UC-07 consiste à comparer les responsabilités de l'environnement existant avec des composants pouvant répondre aux mêmes besoins dans une architecture cible.

| Responsabilité | Environnement existant | Cible ou solution étudiée | État constaté |
|---|---|---|---|
| Stockage | Système de fichiers Linux local | Azure Data Lake Storage Gen2 | Azure étudié, non déployé |
| Format de fichiers | Parquet | Parquet | Parquet utilisé |
| Format de table | Jeux de données Parquet | Apache Iceberg | Iceberg étudié, usage non établi |
| Calcul distribué | Apache Spark / PySpark | Spark et services Azure associés | Spark utilisé |
| Requêtes SQL | Spark SQL | Trino ou services SQL Azure | Spark SQL utilisé ; Trino étudié |
| Catalogue | `spark_catalog` | Hive Metastore ou Project Nessie | Solutions étudiées, non établies comme déployées |
| Orchestration | Scripts Python et exécution manuelle | Apache Airflow ou Azure Data Factory | Solutions étudiées, non déployées |
| Visualisation | Matplotlib dans le TP4 | Power BI ou Apache Superset | Matplotlib utilisé en TP4 ; autres solutions non établies |
| Sécurité | Permissions Linux et environnements virtuels séparés | Microsoft Entra ID, RBAC et ACL | Modèle Azure étudié, non configuré |
| Environnement d'exécution | Linux local | Services Azure ou infrastructure Open Source | Architecture cible étudiée |

Cette comparaison permet de distinguer les composants effectivement utilisés des solutions envisagées pour une évolution de la plateforme.

Il est important de ne pas confondre les responsabilités des différents composants. Par exemple, Parquet est un format de fichier colonnaire, tandis qu'Iceberg est un format de table apportant notamment une gestion des métadonnées et des évolutions de tables.

De même, Matplotlib est une bibliothèque de visualisation graphique. Elle ne remplace pas directement une plateforme décisionnelle complète comme Power BI ou Superset.

#### 6. Documentation de la transposition vers Azure

La documentation de l'étape 9 formalise les correspondances entre l'environnement existant et les composants de l'architecture cible.

Les principaux services Azure étudiés sont :

- Azure Data Lake Storage Gen2 pour le stockage des données.
- Microsoft Entra ID pour la gestion des identités.
- Azure RBAC et les ACL pour la gestion des accès.
- Azure Data Factory pour l'orchestration des traitements.
- Azure Synapse Analytics pour les capacités analytiques et SQL.

Cette étude permet d'identifier les responsabilités que la future architecture devra couvrir.

Aucun compte de stockage Azure, conteneur ADLS Gen2, pipeline Azure Data Factory, workspace Synapse ou rôle RBAC configuré n'a été établi comme déployé dans le cadre des travaux documentés.

La transposition constitue donc une étude d'architecture et une documentation de correspondance, et non une migration ou un déploiement effectif.

## Sorties produites

Les travaux du J4 produisent des résultats analytiques, des visualisations et des éléments de documentation.

| Unité de compétence | Sortie | Description |
|---|---|---|
| UC-08 | Analyse des performances par magasin | Classement des magasins selon le chiffre d'affaires TTC |
| UC-08 | Analyse du chiffre d'affaires magasin | Consultation des indicateurs commerciaux par magasin |
| UC-08 | Classement des produits | Identification des produits les plus vendus |
| UC-08 | Diagramme en barres verticales | Comparaison du CA TTC par magasin |
| UC-08 | Diagramme en barres horizontales | Top 10 des produits par quantité vendue |
| UC-08 | Tableau de synthèse | Classement et parts de chiffre d'affaires par magasin |
| UC-08 | Constats métier | Synthèse des observations et pistes d'approfondissement |
| UC-07 | Comparaison d'architecture | Mise en correspondance des responsabilités techniques |
| UC-07 | Documentation de transposition | Étude des composants d'une architecture cible Azure |

Les jeux de données du TP3 restent les sources des analyses. Les travaux du J4 ne modifient pas les couches de données préparées précédemment.

## Résultats principaux observés

Les analyses de l'UC-08 mettent en évidence les résultats suivants :

| Indicateur | Résultat |
|---|---:|
| Nombre de magasins étudiés | 12 |
| Chiffre d'affaires TTC global | 1 202 218 083,00 |
| Meilleur magasin | Magasin 7 |
| CA TTC du magasin 7 | 103 384 198,80 |
| Part du magasin 7 | 8,60 % |
| Magasin au CA le plus faible | Magasin 2 |
| CA TTC du magasin 2 | 98 249 685,02 |
| Écart entre les deux magasins | 5 134 513,78 |
| Produit le plus vendu | Produit 10000 |
| Quantités vendues du produit 10000 | 454 954 |

Les résultats correspondent au jeu de données synthétique TPCx-BB utilisé dans le projet.

Pour l'UC-07, l'étude a permis de caractériser l'environnement local, d'identifier les responsabilités techniques existantes et de documenter les composants pouvant être mobilisés dans une architecture cible Azure.

## Limites connues

Plusieurs limites doivent être prises en compte dans l'interprétation des travaux.

### Limites des analyses métier

Les identifiants des magasins et des produits sont des clés techniques. Ils ne permettent pas, à eux seuls, d'identifier les magasins ou les références commerciales correspondantes.

Les analyses reposent sur des agrégats cumulés sur la période complète disponible. Elles ne permettent donc pas de mesurer directement les évolutions temporelles, les tendances ou la saisonnalité.

Le chiffre d'affaires ne constitue pas une mesure de rentabilité. Une analyse économique plus complète nécessiterait notamment de prendre en compte les coûts et les marges.

Le nombre de tickets correspond à la somme des décomptes distincts par magasin et par date. Il doit être interprété selon cette granularité.

Le montant net payé TTC ne représente pas une marge commerciale. Le classement des produits repose principalement sur les quantités vendues.

### Limites des visualisations

Les graphiques facilitent la comparaison des magasins et des produits, mais ne remplacent pas un outil décisionnel complet.

Les visualisations restent dépendantes des données et des agrégations utilisées. Elles ne permettent pas de répondre seules à des questions portant sur les causes des écarts observés.

### Limites de l'étude d'architecture

La comparaison UC-07 repose sur l'environnement local constaté et sur l'étude de solutions cibles.

Les composants Azure et certaines solutions Open Source ont été étudiés, mais leur déploiement n'est pas établi.

Il n'est donc pas possible de présenter les solutions étudiées comme des services opérationnels du projet.

La comparaison ne démontre pas non plus une équivalence fonctionnelle ou une parité automatique entre les services Azure et les composants Open Source.

### Limites liées aux données

Le jeu de données TPCx-BB est synthétique et utilisé dans un contexte pédagogique.

Les résultats permettent de travailler sur des analyses et des indicateurs, mais ils ne doivent pas être présentés comme les observations d'une entreprise réelle.

Les constats établissent des observations sur les données disponibles. Ils ne démontrent pas de relations de causalité.

## Continuité du projet

Le J4 s'inscrit dans la continuité du travail réalisé lors des journées précédentes.

Le J3 a permis de préparer, nettoyer, transformer et structurer les données afin de les rendre exploitables pour les analyses.

Le J4 valorise ces données en répondant à des questions métier, en produisant des visualisations et en formulant des constats à partir des résultats obtenus.

En parallèle, l'UC-07 apporte une réflexion sur l'évolution possible de l'architecture technique. L'étude de transposition permet d'identifier les composants nécessaires à une future plateforme reposant sur des services cloud ou des solutions Open Source.

Les travaux réalisés constituent ainsi une étape entre la préparation des données, leur exploitation métier et l'étude d'une architecture cible.

Les prolongements possibles concernent notamment :

- l'enrichissement des analyses avec un référentiel des magasins et des produits ;
- l'ajout d'analyses temporelles ;
- le rapprochement des ventes avec les stocks et les coûts ;
- la mise en place d'une orchestration automatisée ;
- l'approfondissement des mécanismes de sécurité et de sauvegarde ;
- l'expérimentation progressive des services Azure étudiés.