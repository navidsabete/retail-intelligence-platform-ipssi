# Étape 9 : Comparer les responsabilités, pas seulement les noms

## 1. Introduction et objectifs

### 1.1. Contexte

Dans le cadre du projet pédagogique **Retail Intelligence**, fondé sur des données synthétiques TPCx-BB, l'UC-07 porte sur la transposition de la plateforme analytique vers Microsoft Azure.

L'étape 8 a permis d'étudier une architecture alternative sans Azure, désignée comme le parcours local ou parcours B. Cette architecture repose sur un environnement Linux, Python, Apache Spark et un stockage de fichiers local.

L'étape 9 a pour objectif de compléter et d'analyser le tableau de correspondance Azure / Open Source présenté dans le sujet du TP.

L'enjeu n'est pas de rechercher un équivalent technique unique pour chaque service Azure, mais de comparer les responsabilités fonctionnelles couvertes par les différentes technologies.

Cette approche permet notamment de comprendre pourquoi un service intégré comme Azure Synapse Analytics peut nécessiter plusieurs composants Open Source pour reproduire ses différentes fonctions.

### 1.2. Objectifs

Les objectifs de cette étape sont les suivants :

- identifier les responsabilités architecturales de chaque fonction 
- analyser les correspondances entre les services Azure et les technologies Open Source 
- distinguer les composants réellement utilisés des technologies simplement étudiées 
- identifier les responsabilités partiellement couvertes ou non établies 
- expliquer la décomposition fonctionnelle d'Azure Synapse Analytics 
- présenter les limites d'équivalence entre les services cloud managés et les assemblages Open Source 
- proposer des évolutions architecturales cohérentes avec les besoins du projet.

### 1.3. Périmètre et règles de qualification

La comparaison repose sur deux architectures distinctes.

**Parcours Azure : architecture cible étudiée**

Les services Azure ont été examinés dans le cadre de la transposition théorique de la plateforme. Aucun déploiement Azure n'a été réalisé.

**Parcours local : environnement effectivement utilisé**

Les résultats de l'étape 8 constituent la référence pour identifier les composants réellement présents dans TP3.

Les statuts utilisés dans cette documentation sont :

| Statut | Signification |
|---|---|
| Réalisé | Composant ou fonction effectivement présent et vérifié dans le périmètre indiqué |
| Étudié | Technologie ou fonction examinée théoriquement |
| Proposé | Évolution architecturale envisagée |
| Non déployé | Absence de déploiement établie |
| Non établi | Les vérifications disponibles ne permettent pas de conclure |

Une distinction supplémentaire est appliquée lorsque cela est nécessaire entre les environnements TP3 et TP4. En particulier, l'utilisation de Matplotlib dans TP4, dans le cadre de l'UC-08, ne constitue pas une preuve de son utilisation dans TP3.


## 2. Présentation des responsabilités architecturales

Une plateforme analytique repose sur plusieurs responsabilités complémentaires. Ces responsabilités doivent être identifiées avant de comparer les technologies.

### 2.1. Stockage des données

Le stockage assure la persistance physique des données.

Il doit permettre de conserver les données brutes, intermédiaires et transformées, ainsi que de les organiser de manière cohérente.

Dans Retail Intelligence, cette responsabilité est assurée par le système de fichiers Linux local.

### 2.2. Format de fichiers et gestion des tables

Cette responsabilité concerne l'organisation physique et logique des données.

Il convient de distinguer :

- le format de fichiers, qui définit la représentation physique des données 
- le format de table, qui apporte des mécanismes de gestion des tables et de leurs métadonnées.

Parquet est un format de fichiers colonnaire. Apache Iceberg est un format de table qui peut utiliser Parquet pour stocker physiquement les données.

Ces deux technologies ne sont donc pas interchangeables.

### 2.3. Traitement distribué

Le traitement assure les opérations de nettoyage, de transformation, d'agrégation et de préparation des données.

Apache Spark constitue le moteur de traitement effectivement utilisé dans le projet.

### 2.4. Requêtes SQL

Cette responsabilité permet d'interroger les données analytiques au moyen du langage SQL.

Spark SQL est utilisé dans TP3 pour interroger les données produites dans la zone Gold.

Trino constitue une alternative étudiée, mais son installation n'a pas été établie.

### 2.5. Catalogue et métadonnées

Le catalogue permet de référencer les tables, leurs schémas et leurs emplacements.

Il facilite la découverte et l'utilisation des données par les différents moteurs.

Dans TP3, le catalogue vérifié est `spark_catalog`, avec une implémentation en mémoire.

### 2.6. Intégration et orchestration

L'orchestration organise l'exécution des différentes étapes du pipeline.

Elle permet notamment de gérer les dépendances, les déclenchements, les planifications, les erreurs et les relances.

Dans TP3, les traitements reposent sur plusieurs scripts Python exécutés manuellement.

Apache Airflow constitue une évolution possible, mais son déploiement n'est pas établi.

### 2.7. Visualisation

La visualisation permet de présenter les résultats analytiques sous forme de tableaux, graphiques et tableaux de bord.

Il faut distinguer les environnements :

- TP3 : aucun outil précis de visualisation n'a été suffisamment établi comme effectivement utilisé.
- TP4 / UC-08 : Matplotlib a été mis en place et effectivement utilisé.
- Parcours Azure : Power BI a été étudié, sans déploiement établi.

Matplotlib est donc une technologie effectivement utilisée dans le projet Retail Intelligence, mais dans le périmètre TP4 / UC-08 et non dans les vérifications TP3 effectuées dans l'UC-07.

### 2.8. Identités et permissions

Cette responsabilité concerne l'authentification des utilisateurs et le contrôle de leurs autorisations.

Dans TP3, les permissions du système de fichiers Linux ont été vérifiées.

Aucune gestion centralisée des identités ou des secrets n'a été établie.

### 2.9. Environnement d'exécution

L'environnement d'exécution fournit les ressources nécessaires au fonctionnement des traitements et des services.

Dans TP3, les traitements sont exécutés sous Linux, dans un environnement virtuel Python dédié.

L'utilisation de Docker ou Podman n'a pas été établie.


## 3. Tableau complet de correspondance Azure / Open Source

Le tableau suivant compare les responsabilités fonctionnelles et les composants associés.

| Fonction | Rôle fonctionnel | Parcours Azure étudié | Composant local réellement utilisé dans TP3 | Composant complémentaire étudié ou proposé | Statut TP3 |
|---|---|---|---|---|---|
| Stockage | Persistance physique des données | ADLS Gen2 | Système de fichiers Linux | MinIO | Réalisé |
| Format de fichiers | Organisation physique des données | Fichiers analytiques du Lakehouse | Parquet avec Snappy | — | Réalisé |
| Gestion des tables | Gestion logique et métadonnées des tables | Tables du Lakehouse | Organisation de fichiers et catalogue Spark | Apache Iceberg | Partiel |
| Traitement distribué | Nettoyage et transformation | Synapse Spark | Apache Spark / PySpark | — | Réalisé |
| Requêtes SQL | Interrogation analytique | Synapse SQL | Spark SQL | Trino | Réalisé |
| Catalogue | Référencement des tables et schémas | Métadonnées des services Azure | `spark_catalog` en mémoire | Hive Metastore, Nessie | Partiel |
| Orchestration | Coordination des traitements | Azure Data Factory | Scripts Python exécutés manuellement | Airflow, NiFi | Partiel |
| Visualisation | Présentation des résultats | Power BI | Utilisation non établie dans TP3 | Matplotlib, Superset | Non établi |
| Identités et permissions | Authentification et contrôle d'accès | Microsoft Entra ID, RBAC, ACL | Permissions Linux | Gestion centralisée des secrets | Partiel |
| Environnement d'exécution | Hébergement et ressources de calcul | Infrastructure cloud managée | Linux et environnement virtuel Python | Docker, Podman, machine virtuelle | Réalisé |

**Précision concernant la visualisation :** Matplotlib a été effectivement mis en place et utilisé dans TP4 / UC-08. Cette réalisation ne doit pas être reportée comme une utilisation TP3 dans le tableau de l'UC-07.

Les composants Azure mentionnés correspondent à une architecture étudiée et non à une infrastructure effectivement déployée.


## 4. Analyse détaillée des correspondances

### 4.1. Stockage : ADLS Gen2 et système de fichiers Linux

Azure Data Lake Storage Gen2 fournit un espace de stockage adapté aux architectures analytiques.

Il permet notamment :

- le stockage de fichiers 
- l'organisation hiérarchique des données 
- la gestion des accès 
- l'intégration avec les services analytiques Azure.

Dans TP3, le stockage est assuré par le système de fichiers Linux.

Les répertoires suivants ont été identifiés :

- `bronze/`
- `silver/`
- `silver-transformed/`
- `gold/`
- `quality/`
- `quarantine/`

Les données sources Bronze comprennent notamment :

- `inventory.dat`
- `store_sales.dat`

Les autres zones contiennent des fichiers Parquet.

La distinction entre Silver et Silver-transformed est physiquement vérifiée.

Quality et Quarantine constituent des espaces complémentaires et non des couches supplémentaires de la chaîne Bronze/Silver/Gold.

**Limites de l'équivalence**

Le système de fichiers Linux assure la persistance des données, mais ne fournit pas automatiquement les fonctionnalités d'un stockage cloud managé.

Il ne garantit pas à lui seul :

- la réplication géographique 
- la haute disponibilité 
- la montée en charge du stockage 
- la gestion centralisée des accès 
- la résilience d'une infrastructure cloud.

MinIO a été étudié comme alternative de stockage objet, mais son déploiement n'a pas été établi.

ADLS Gen2 n'a pas été déployé.

### 4.2. Format de fichiers et gestion des tables : Parquet et Iceberg

Dans le parcours local, Parquet est effectivement utilisé pour stocker les données analytiques.

Les fichiers observés utilisent la compression Snappy.

Parquet est un format de stockage colonnaire particulièrement adapté aux traitements analytiques.

Apache Iceberg répond à un besoin différent.

Il s'agit d'un format de table qui apporte notamment :

- la gestion des métadonnées 
- le suivi des versions des tables 
- l'évolution des schémas 
- des mécanismes de gestion des modifications 
- des possibilités de gestion transactionnelle selon les moteurs et catalogues associés.

Iceberg peut utiliser Parquet comme format de stockage physique.

Il ne remplace donc pas Parquet.

**Statuts :**

- Parquet : réalisé dans TP3.
- Snappy : compression observée dans TP3.
- Apache Iceberg : étudié, utilisation non établie.

**Limites de l'équivalence**

La présence de fichiers Parquet ne démontre pas l'existence d'une gestion transactionnelle des tables.

L'utilisation d'Iceberg nécessiterait également une configuration adaptée du catalogue et des moteurs compatibles.

Iceberg ne constitue pas un équivalent d'Azure Synapse Analytics.

### 4.3. Traitement distribué : Synapse Spark et Apache Spark

Azure Synapse Analytics permet d'exécuter des traitements distribués à l'aide de pools Apache Spark.

Dans TP3, cette responsabilité est assurée par Apache Spark et PySpark.

Les versions vérifiées sont :

- Apache Spark : 4.3.0 
- PySpark : 4.3.0.

Une lecture réelle du jeu Gold `sales_performance_by_store` a été réalisée avec succès.

Le résultat contient 12 lignes et 14 colonnes.

**Limites de l'équivalence**

L'utilisation du même moteur de traitement ne signifie pas que les infrastructures sont équivalentes.

Dans Azure, les ressources de calcul peuvent être fournies et administrées par les services cloud.

Dans TP3, l'exécution dépend de l'environnement Linux et des ressources disponibles localement.

La présence de Spark ne démontre donc pas une infrastructure distribuée hautement disponible ni une montée en charge comparable à celle d'un service cloud managé.

### 4.4. Requêtes SQL : Synapse SQL, Spark SQL et Trino

Synapse propose plusieurs capacités SQL, notamment des pools SQL serverless et dédiés.

Dans TP3, les requêtes analytiques sont réalisées avec Spark SQL.

Une vue temporaire `sales_performance_by_store` a été créée dans une session Spark.

La requête exécutée était :

```sql
SELECT
    store_sk,
    revenue_rank,
    total_revenue_inc_tax,
    revenue_share_pct
FROM sales_performance_by_store
ORDER BY revenue_rank
```

Elle a retourné les 12 magasins classés par chiffre d'affaires.

Le premier magasin présente les valeurs suivantes :

| Indicateur | Valeur |
|---|---:|
| `store_sk` | 7 |
| `revenue_rank` | 1 |
| `total_revenue_inc_tax` | 103384198.80 |
| `revenue_share_pct` | 8.6 |

Trino a également été étudié comme moteur SQL distribué alternatif.

Son installation n'a toutefois pas été établie.

**Limites de l'équivalence**

Spark SQL est étroitement intégré à l'environnement Spark.

Trino est notamment conçu pour interroger différentes sources de données au moyen d'un moteur SQL distribué.

Ces deux solutions répondent à des besoins proches sur certains usages, mais ne présentent pas les mêmes caractéristiques architecturales.

### 4.5. Catalogue et métadonnées : catalogue Azure et Spark Catalog

La gestion des métadonnées permet de référencer les tables, leurs schémas et leurs emplacements.

Dans TP3, la configuration Spark vérifiée est :

```text
spark.sql.catalogImplementation = in-memory
spark.sql.defaultCatalog = spark_catalog
spark.sql.warehouse.dir = file:/home/[user]/retail-intelligence/tp3/notebooks/spark-warehouse
```

Le seul catalogue visible était `spark_catalog`.

Il s'agit du catalogue intégré à Spark, avec une implémentation en mémoire.

Les technologies suivantes ont été examinées comme possibilités complémentaires :

- Hive Metastore 
- Project Nessie 
- catalogue associé à Apache Iceberg.

Leur déploiement n'a pas été établi.

**Limites de l'équivalence**

Un catalogue Spark en mémoire ne doit pas être assimilé à un catalogue externe et persistant partagé entre plusieurs moteurs.

Il ne démontre pas non plus la présence d'un catalogue Iceberg.

### 4.6. Intégration et orchestration : Data Factory et Airflow

Azure Data Factory permet de construire et de coordonner des pipelines d'intégration et de traitement.

Dans TP3, les traitements sont répartis entre plusieurs scripts Python :

- `etape4_nettoyage.py`
- `etape5_6_transformations_silver.py`
- `etape7_gold.py`
- `etape9_quality_control.py`

Les scripts sont distincts et leur enchaînement est effectué manuellement.

Aucun script central orchestrant automatiquement l'ensemble du pipeline n'a été identifié.

Aucune planification cron propre au projet n'a été établie.

Apache Airflow constitue une solution possible pour organiser les workflows, leurs dépendances et leurs déclenchements.

Apache NiFi a également été envisagé comme solution complémentaire d'intégration et de circulation des données.

**Statuts :**

- Scripts Python métier : réalisés.
- Apache Airflow : non déployé.
- Apache NiFi : option étudiée.
- Azure Data Factory : étudié, non déployé.

**Limites de l'équivalence**

L'exécution de scripts indépendants ne couvre pas l'ensemble des responsabilités d'un orchestrateur.

Les fonctions de planification, de supervision, de gestion des dépendances et de relance restent notamment à compléter.

### 4.7. Visualisation : Power BI et outils Open Source

La visualisation permet de rendre les résultats analytiques accessibles aux utilisateurs.

Dans le parcours Azure, Power BI constitue la solution étudiée pour produire des rapports et tableaux de bord décisionnels.

Pour le parcours local, il faut distinguer les résultats TP3 et TP4.

**TP3 – UC-07**

Aucune preuve suffisante n'a été collectée pour établir l'utilisation effective d'un outil précis de visualisation dans cet environnement.

La présence de notebooks Jupyter ne suffit pas à démontrer l'utilisation de Matplotlib ou d'un outil de Business Intelligence.

**TP4 – UC-08**

Matplotlib a été mis en place et effectivement utilisé.

Cette réalisation confirme l'utilisation de cette bibliothèque dans le projet Retail Intelligence, mais dans le périmètre TP4 / UC-08.

**Technologies complémentaires :**

| Technologie | Fonction | Statut |
|---|---|---|
| Matplotlib | Production de graphiques Python | Réalisé dans TP4 / UC-08 |
| Jupyter Notebook | Exploration et présentation interactive | Présent dans TP3  visualisation spécifique non établie |
| Apache Superset | Tableaux de bord décisionnels | Non établi |
| Power BI | Visualisation décisionnelle Azure | Étudié |

**Limites de l'équivalence**

Matplotlib est une bibliothèque de visualisation Python. Elle permet de produire des graphiques, mais ne fournit pas à elle seule les fonctions d'une plateforme complète de Business Intelligence.

Apache Superset, par exemple, répond davantage à un besoin de tableaux de bord interactifs accessibles aux utilisateurs.

Power BI propose également des fonctions intégrées de création, de publication et de partage de rapports.

Il faut donc distinguer une bibliothèque de graphiques d'une plateforme décisionnelle.

### 4.8. Identités et permissions : Entra ID, RBAC, ACL et Linux

Microsoft Entra ID permet la gestion des identités dans l'environnement Azure.

RBAC et les ACL permettent de définir les autorisations d'accès aux ressources.

Dans TP3, les permissions Linux suivantes ont été vérifiées :

| Élément | Permission |
|---|---:|
| Répertoires TP3 | `755` |
| Scripts Python | `644` |
| Fichiers sources Bronze | `644` |

Les environnements virtuels TP3 et TP4 sont physiquement distincts.

Aucun fichier de configuration `.env`, `.yaml`, `.yml`, `.ini`, `.conf` ou `.toml` n'a été identifié dans le périmètre recherché.

Aucune référence aux mots-clés de secrets examinés n'a été détectée dans les scripts et notebooks.

Aucune gestion centralisée des secrets n'a été établie.

**Limites de l'équivalence**

Les permissions Linux permettent de contrôler l'accès aux fichiers et répertoires, mais ne remplacent pas un système centralisé de gestion des identités et des autorisations.

Une architecture Open Source plus complète nécessiterait des mécanismes complémentaires adaptés aux services utilisés.

### 4.9. Environnement d'exécution : cloud et infrastructure locale

Dans Azure, les services analytiques reposent sur une infrastructure cloud dont une partie de l'administration est prise en charge par Microsoft.

Dans TP3, l'environnement est Linux avec :

- Python 3.12.3 
- Apache Spark 4.3.0 
- PySpark 4.3.0 
- Pandas 3.1.1 
- Jupyter Notebook.

L'environnement virtuel TP3 est :

`~/retail-intelligence/tp3/retail_intel_tp3_venv/`

L'environnement TP4 est distinct :

`~/retail-intelligence/tp4/retail_intel_tp4_venv/`

Docker et Podman ont été envisagés comme solutions de conteneurisation, mais leur utilisation dans TP3 n'a pas été établie.

**Limites de l'équivalence**

Une infrastructure locale implique une responsabilité directe concernant les ressources, les installations, les mises à jour, la disponibilité et la maintenance.

Les services cloud managés prennent en charge une partie de ces responsabilités.


## 5. Décomposition fonctionnelle d'Azure Synapse Analytics

### 5.1. Pourquoi Synapse ne possède pas un équivalent Open Source unique

Azure Synapse Analytics est une plateforme analytique intégrée qui regroupe plusieurs capacités.

Selon l'architecture et les services retenus, elle peut associer :

- traitement distribué avec Spark 
- interrogation SQL 
- intégration et orchestration 
- accès au stockage analytique 
- gestion des métadonnées 
- intégration avec les autres services Azure.

Il serait donc incorrect de rechercher un seul composant Open Source qui reproduirait toutes ces fonctions.

Une architecture Open Source repose plutôt sur l'association de plusieurs briques spécialisées.

### 5.2. Correspondance par responsabilité

| Responsabilité | Parcours Azure | Brique Open Source correspondante | Rôle |
|---|---|---|---|
| Stockage | ADLS Gen2 | Système de fichiers, MinIO | Hébergement physique des données |
| Format de fichiers | Fichiers analytiques | Parquet | Stockage colonnaire |
| Gestion des tables | Tables du Lakehouse | Apache Iceberg | Gestion logique et métadonnées des tables |
| Calcul | Synapse Spark | Apache Spark | Traitement distribué |
| SQL | Synapse SQL | Spark SQL ou Trino | Interrogation des données |
| Catalogue | Métadonnées Azure | Hive Metastore ou catalogue compatible | Référencement des tables |
| Orchestration | Azure Data Factory | Apache Airflow | Coordination des workflows |
| Visualisation | Power BI | Matplotlib ou Apache Superset | Présentation des résultats |
| Sécurité | Entra ID, RBAC et ACL | Permissions Linux et mécanismes complémentaires | Contrôle des accès |
| Exécution | Infrastructure cloud | Linux, conteneurs ou machines virtuelles | Hébergement des composants |

Cette correspondance est fonctionnelle et non une équivalence parfaite.

### 5.3. Rôle et limites des composants

**Parquet**

Parquet stocke physiquement les données sous forme colonnaire. Il ne fournit pas de moteur de calcul ou d'orchestration.

**Apache Iceberg**

Iceberg gère les tables et leurs métadonnées. Il peut s'appuyer sur Parquet pour stocker les données physiques. Il ne remplace pas Synapse Analytics.

**Apache Spark**

Spark assure les traitements distribués et peut exécuter des requêtes SQL avec Spark SQL.

Il ne fournit pas automatiquement toutes les fonctions d'une plateforme analytique intégrée.

**Trino**

Trino fournit un moteur de requêtes SQL distribué et peut interroger plusieurs sources de données.

Il ne remplace ni le stockage ni l'orchestration.

**Hive Metastore**

Hive Metastore fournit un catalogue externe de métadonnées.

Il ne réalise pas les traitements analytiques.

**Apache Airflow**

Airflow coordonne les workflows et les dépendances entre traitements.

Il ne réalise pas lui-même les calculs Spark.

**Apache Superset et Matplotlib**

Superset permet de construire des tableaux de bord décisionnels.

Matplotlib permet de produire des graphiques avec Python.

Leurs responsabilités sont donc différentes et leurs usages ne sont pas strictement équivalents.

### 5.4. Avantages et contraintes d'une architecture modulaire

L'assemblage de composants Open Source présente plusieurs avantages :

- liberté de choix technologique 
- possibilité d'adapter chaque composant aux besoins 
- indépendance vis-à-vis d'un fournisseur cloud 
- possibilité de faire évoluer séparément les différents services 
- maîtrise de l'infrastructure locale.

Il implique également plusieurs contraintes :

- intégration technique entre les composants 
- configuration des interfaces 
- gestion des versions et des compatibilités 
- administration de plusieurs services 
- supervision centralisée à mettre en place 
- gestion des identités et des secrets 
- maintenance et mises à jour 
- gestion de la disponibilité et des sauvegardes.

Une architecture modulaire peut donc couvrir les responsabilités d'une plateforme intégrée, mais elle demande un travail supplémentaire d'intégration et d'exploitation.

---

## 6. Schéma comparatif des architectures

### 6.1. Parcours Azure : architecture cible étudiée

```text
                  UTILISATEURS
                       |
                       v
                 Power BI
                       |
                       v
          +-------------------------+
          | Azure Synapse Analytics|
          |                         |
          | - Synapse Spark         |
          | - Synapse SQL           |
          | - Capacités analytiques |
          +-------------------------+
                       |
                       v
                 ADLS Gen2
                       |
                       v
              Données analytiques

          Azure Data Factory
          Orchestration et intégration

          Microsoft Entra ID
          RBAC et ACL
          Gestion des accès
```

**Statut : architecture étudiée, non déployée.**

### 6.2. Parcours local : architecture réellement exécutée dans TP3

```text
                 DONNEES SOURCES
                       |
                       v
              SYSTEME DE FICHIERS
                       |
                       v
                    BRONZE
                       |
                       v
              Scripts Python métier
                       |
                       v
               APACHE SPARK
                  / PySpark
                       |
                       v
               SILVER / GOLD
                       |
                       v
                  PARQUET
                       |
                       v
                 SPARK SQL
                       |
                       v
             RESULTATS ANALYTIQUES
```

Les zones Quality et Quarantine constituent des espaces complémentaires.

Le catalogue Spark intégré en mémoire est utilisé dans l'environnement vérifié.

L'exécution des scripts est manuelle.

**Statut : architecture locale effectivement utilisée dans TP3.**

### 6.3. Composants complémentaires proposés

```text
Stockage objet
    MinIO

Gestion des tables
    Apache Iceberg

Catalogue partagé
    Hive Metastore

Moteur SQL complémentaire
    Trino

Orchestration
    Apache Airflow

Visualisation
    Apache Superset

Sécurité
    Gestion centralisée des identités et secrets

Environnement
    Docker / Podman
```

**Statut : composants complémentaires envisagés, non présentés comme déployés dans TP3.**

---

## 7. Tableau récapitulatif des statuts

| Technologie ou mécanisme | Statut | Périmètre et observation |
|---|---|---|
| Système de fichiers Linux | Réalisé | TP3, stockage local |
| Parquet | Réalisé | TP3, stockage analytique |
| Snappy | Réalisé | TP3, compression observée |
| Apache Spark | Réalisé | TP3, version 4.3.0 |
| PySpark | Réalisé | TP3, version 4.3.0 |
| Spark SQL | Réalisé | TP3, requête Gold validée |
| `spark_catalog` | Réalisé | TP3, catalogue en mémoire |
| Scripts Python métier | Réalisé | TP3, exécution manuelle |
| Permissions Linux | Réalisé | TP3, droits vérifiés |
| Matplotlib | Réalisé | TP4 / UC-08, mise en place et utilisation effectives |
| ADLS Gen2 | Étudié | Architecture Azure, non déployé |
| Azure Synapse Analytics | Étudié | Architecture Azure, non déployée |
| Azure Data Factory | Étudié | Architecture Azure, non déployée |
| Power BI | Étudié | Visualisation Azure, non déployée |
| Apache Iceberg | Étudié | Utilisation dans TP3 non établie |
| Trino | Étudié | Installation non établie |
| Apache NiFi | Étudié | Option d'intégration |
| MinIO | Non établi | Déploiement non démontré |
| Hive Metastore | Non établi | Catalogue externe non démontré |
| Project Nessie | Non établi | Déploiement non démontré |
| Apache Airflow | Non déployé | Aucun déploiement établi |
| Apache Superset | Non établi | Déploiement non démontré |
| Docker / Podman | Non établi | Utilisation dans TP3 non démontrée |
| Gestion centralisée des secrets | Non établie | Aucun mécanisme identifié dans le périmètre vérifié |

---

## 8. Analyse des limites de l'équivalence

### 8.1. Intégration des services

Les services Azure peuvent bénéficier d'intégrations natives.

Dans une architecture Open Source, les différents composants doivent être configurés et connectés.

L'utilisation conjointe de Spark, Iceberg, Trino, Hive Metastore et Airflow nécessite notamment de définir les interfaces et les mécanismes d'accès aux données.

### 8.2. Gestion opérationnelle

Les services Azure managés prennent en charge une partie de l'exploitation.

Dans une architecture locale, l'administration doit assurer :

- l'installation des composants 
- les mises à jour 
- la gestion des dépendances 
- la configuration 
- la supervision 
- la maintenance 
- les sauvegardes.

### 8.3. Sécurité

Azure propose une gestion intégrée des identités et des autorisations.

Dans TP3, les permissions Linux sont effectivement utilisées, mais aucune gestion centralisée des secrets n'a été établie.

Une architecture Open Source plus complète nécessiterait des mécanismes supplémentaires de gestion des identités et des accès.

### 8.4. Haute disponibilité et montée en charge

Un système de fichiers local dépend de la machine qui l'héberge.

Il ne possède pas automatiquement les mécanismes de réplication et de disponibilité d'un service cloud.

De même, la présence de Spark ne démontre pas la mise en place d'une infrastructure de calcul hautement disponible.

### 8.5. Sauvegardes et restauration

Aucun répertoire explicitement dédié aux sauvegardes n'a été identifié dans le périmètre inspecté.

Aucune stratégie de sauvegarde automatique ou procédure de restauration testée n'a été établie.

Cette responsabilité représente un point d'amélioration important.

### 8.6. Synthèse des écarts

| Dimension | Parcours local TP3 | Écart par rapport à la cible Azure |
|---|---|---|
| Stockage | Fichiers Linux | Absence de stockage cloud managé |
| Tables analytiques | Parquet | Gestion transactionnelle des tables non établie |
| Calcul | Spark / PySpark | Infrastructure distribuée managée non établie |
| SQL | Spark SQL | Absence de service SQL managé Azure |
| Catalogue | Spark en mémoire | Catalogue externe partagé non établi |
| Orchestration | Scripts manuels | Orchestration centralisée absente |
| Visualisation | Usage spécifique non établi dans TP3 | Chaîne décisionnelle non démontrée |
| Sécurité | Permissions Linux | Gestion centralisée des identités et secrets non établie |
| Exécution | Linux local | Infrastructure cloud managée absente |
| Résilience | Non établie | Sauvegardes et restauration non démontrées |

La réalisation de Matplotlib dans TP4 / UC-08 constitue une capacité de visualisation effectivement acquise dans le projet, mais ne modifie pas le constat spécifique concernant l'environnement TP3.


## 9. Conclusion

L'analyse comparative des responsabilités architecturales montre que l'environnement local Retail Intelligence couvre effectivement plusieurs fonctions fondamentales d'une plateforme analytique.

Le stockage repose sur le système de fichiers Linux et les données analytiques sont enregistrées au format Parquet avec compression Snappy.

Les transformations sont réalisées avec Apache Spark et PySpark. Les résultats analytiques peuvent être interrogés avec Spark SQL.

L'environnement dispose également d'un catalogue Spark intégré en mémoire et de scripts Python permettant d'exécuter les différentes étapes du pipeline.

La visualisation a par ailleurs été mise en place et utilisée avec Matplotlib dans TP4, dans le cadre de l'UC-08. Cette réalisation confirme l'acquisition d'une capacité de visualisation Python dans le projet, sans permettre d'affirmer que Matplotlib était utilisé dans TP3.

Plusieurs responsabilités restent néanmoins partiellement couvertes ou non établies dans TP3. C'est notamment le cas de la gestion centralisée des métadonnées, de l'orchestration automatisée, de la visualisation décisionnelle dans cet environnement, de la gestion centralisée des secrets et des mécanismes de sauvegarde et de restauration.

La comparaison met également en évidence qu'Azure Synapse Analytics ne possède pas d'équivalent direct dans un unique composant Open Source.

Sa transposition nécessite un assemblage de technologies complémentaires : stockage, format de table, moteur de calcul, moteur SQL, catalogue, orchestration et outils de visualisation.

Cette approche modulaire offre davantage de liberté technologique, mais implique également une responsabilité accrue en matière d'intégration, d'administration, de sécurité, de supervision et de maintenance.

Le parcours local constitue donc une implémentation fonctionnelle de plusieurs responsabilités analytiques étudiées dans le parcours Azure, mais ne représente pas une reproduction complète de l'environnement managé Azure.

Les évolutions envisageables pourraient notamment porter sur :

- l'intégration d'un catalogue externe 
- la mise en place d'un orchestrateur 
- l'adoption d'un format de table comme Apache Iceberg 
- l'ajout d'un moteur SQL complémentaire 
- l'intégration d'un outil de visualisation décisionnelle 
- l'amélioration de la gestion des identités et des secrets 
- la définition d'une stratégie de sauvegarde et de restauration.

Ces évolutions restent des propositions architecturales et ne doivent pas être confondues avec les composants effectivement déployés dans TP3.

**La principale conclusion de cette étape est qu'une architecture doit être comparée par les responsabilités qu'elle couvre, et non par une simple équivalence de noms entre produits.**