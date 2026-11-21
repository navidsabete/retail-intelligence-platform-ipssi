# Étape 6 – Étudier Azure Data Factory et Azure Synapse Analytics

## 1. Objectif de l'étape

Cette étape consiste à étudier les services Azure qui pourraient intervenir dans l'intégration, le traitement et l'analyse des données de la plateforme Retail Intelligence.

Les services étudiés sont :
- Azure Data Factory 
- Azure Synapse Analytics 
- Synapse Studio 
- les pools Apache Spark 
- les capacités SQL et les fonctionnalités d'exploration des données

L'objectif est de comprendre le rôle de chaque composant et la manière dont ils pourraient fonctionner ensemble dans une architecture Data Lake.

Le projet suit le **Parcours B – Local / Open Source**. Cette étape relève donc de l'étude et de la présentation : aucun pipeline Azure Data Factory ni espace de travail Azure Synapse n'est créé.

## 2. Présentation générale des responsabilités

Les services étudiés répondent à des responsabilités différentes et complémentaires.

| Composant | Responsabilité principale |
|---|---|
| ADLS Gen2 | Stocker les données et organiser les zones Bronze, Silver et Gold |
| Azure Data Factory | Intégrer, déplacer et orchestrer les flux de données |
| Azure Synapse Analytics | Fournir un environnement d'analyse et de traitement |
| Synapse Studio | Permettre de développer, explorer, exécuter et superviser les traitements |
| Apache Spark | Exécuter des traitements distribués sur les données |
| Synapse SQL | Interroger et analyser les données avec le langage SQL |

Il est important de ne pas confondre le stockage, l'orchestration et le calcul.

ADLS Gen2 conserve les fichiers. Data Factory organise les opérations qui permettent de les déplacer et de déclencher des traitements. Synapse met à disposition différentes capacités analytiques, notamment SQL et Spark.

## 3. Azure Data Factory (ADF)

### 3.1 Rôle général

Azure Data Factory est un service cloud d'intégration de données et d'orchestration.

Il permet de construire des flux de travail automatisés afin de :
- récupérer des données provenant de différentes sources
- déplacer les données vers un espace de stockage centralisé 
- déclencher des transformations 
- organiser l'exécution des différentes étapes 
- planifier et superviser les traitements.

ADF est particulièrement utile lorsque les traitements doivent être exécutés régulièrement ou lorsqu'ils dépendent les uns des autres.

### 3.2 Notion de pipeline

Dans Azure Data Factory, un pipeline est un ensemble logique d'activités qui réalisent une tâche.

Un pipeline peut notamment contenir :
- une activité de copie de données 
- une activité de transformation 
- une activité de contrôle 
- une opération déclenchant un autre pipeline 
- des conditions permettant d'adapter le déroulement du traitement

Les activités peuvent être exécutées successivement ou en parallèle selon les dépendances définies.

### 3.3 Exemple d'utilisation dans Retail Intelligence

Dans une future architecture Azure, un pipeline ADF pourrait organiser le flux suivant :

1. Récupérer les fichiers sources autorisés du projet.
2. Les déposer dans la zone Bronze d'ADLS Gen2.
3. Déclencher un traitement de préparation des données.
4. Attendre la fin du traitement et contrôler son résultat.
5. Déclencher les transformations nécessaires à la production des données Silver.
6. Organiser la publication des indicateurs dans la zone Gold.
7. Superviser l'exécution et signaler les éventuelles erreurs.

Cet exemple décrit un scénario cible. Il ne correspond pas à un pipeline effectivement développé ou exécuté dans le cadre du projet.

### 3.4 Notions techniques principales

ADF s'appuie notamment sur les composants suivants :

| Composant | Rôle |
|---|---|
| Pipeline | Regroupe les étapes d'un traitement |
| Activité | Représente une opération à effectuer |
| Jeu de données (Dataset) | Décrit les données utilisées en entrée ou en sortie |
| Service lié (Linked Service) | Définit les informations de connexion à une source, une destination ou un service |
| Runtime d'intégration | Fournit l'environnement de connexion et d'exécution nécessaire aux activités |

ADF permet également de planifier des pipelines, de les déclencher selon des événements et de suivre leur état d'exécution.

## 4. Azure Synapse Analytics

### 4.1 Rôle général

Azure Synapse Analytics est un environnement analytique Azure qui regroupe plusieurs capacités destinées au traitement et à l'analyse des données.

Il propose notamment :
- des capacités SQL 
- des environnements Apache Spark 
- des fonctionnalités d'intégration de données et d'orchestration 
- des outils d'exploration et de supervision

Synapse permet ainsi de travailler sur les données stockées dans un Data Lake et de mettre à disposition des résultats exploitables pour les analyses et les usages décisionnels.

Il ne remplace pas le rôle d'ADLS Gen2 : les données peuvent rester dans le stockage tandis que les moteurs analytiques les interrogent ou les transforment.

### 4.2 Espace de travail Synapse

L'espace de travail (*Workspace*) constitue le point central de l'environnement Synapse.

Il regroupe les ressources et les éléments nécessaires aux activités analytiques, par exemple :
- les scripts SQL 
- les notebooks 
- les pipelines 
- les pools SQL 
- les pools Apache Spark 
- les connexions aux espaces de stockage

Un espace de travail peut donc servir de cadre commun aux différents profils techniques qui interviennent sur la plateforme.

## 5. Synapse Studio

### 5.1 Rôle général

Synapse Studio est l'interface de travail intégrée à Azure Synapse Analytics.

Elle permet aux utilisateurs de développer, d'explorer, d'exécuter et de superviser les activités analytiques depuis un environnement commun.

Elle donne notamment accès à :
- l'exploration des données
- la rédaction et l'exécution de scripts SQL
- la création et l'exécution de notebooks Spark
- la conception de pipelines
- la supervision des traitements
- la gestion des ressources analytiques

### 5.2 Utilisation dans Retail Intelligence

Dans une future architecture Retail Intelligence, Synapse Studio pourrait être utilisé par l'équipe Data Engineering pour :
- explorer les données présentes dans ADLS Gen2
- développer les transformations nécessaires
- exécuter des traitements PySpark
- interroger les données avec SQL
- contrôler les résultats des traitements
- préparer les données destinées à l'analyse métier

Les analystes pourraient également utiliser les capacités SQL pour consulter les données préparées, sous réserve des autorisations définies.

Synapse Studio est donc une interface de développement et d'administration analytique. Ce n'est pas, à lui seul, un moteur de stockage ou de calcul.

## 6. Spark Pools

### 6.1 Rôle d'Apache Spark

Apache Spark est un moteur de traitement distribué.

Il permet de répartir les calculs sur plusieurs ressources de calcul afin de traiter des volumes importants de données.

Il est notamment adapté à :
- la préparation des données
- le nettoyage
- les jointures
- les agrégations
- les transformations complexes
- certains traitements de machine learning

Spark prend en charge plusieurs interfaces de programmation, notamment Python avec PySpark, Scala et SQL.

### 6.2 Rôle des Spark Pools dans Synapse

Dans Azure Synapse Analytics, un pool Apache Spark fournit un environnement de calcul destiné à l'exécution des applications Spark.

Il permet notamment d'exécuter des notebooks et des traitements distribués sur les données stockées dans Azure Storage ou ADLS Gen2.

Les traitements peuvent utiliser les données du Data Lake sans que le moteur Spark devienne lui-même le système de stockage permanent des données.

Il faut donc distinguer :
- **Apache Spark** : le moteur de traitement distribué ;
- **Spark Pool** : les ressources de calcul mises à disposition pour exécuter les traitements Spark dans Synapse.

### 6.3 Exemple d'utilisation dans Retail Intelligence

Un notebook PySpark exécuté sur un pool Spark pourrait réaliser les opérations suivantes :

1. Lire les fichiers de ventes depuis la zone Silver.
2. Contrôler les types et la qualité des données.
3. Réaliser des agrégations par magasin et par date.
4. Calculer les indicateurs de performance.
5. Écrire les résultats validés dans la zone Gold.

Ce scénario reprend les types de traitements déjà réalisés dans l'environnement local avec PySpark.

Il s'agit d'une transposition conceptuelle : aucun pool Spark Azure ni notebook Synapse n'a été créé ou exécuté dans ce projet.

## 7. Capacités SQL et exploration des données

Azure Synapse Analytics propose plusieurs possibilités d'analyse SQL.

Il est notamment important de distinguer le pool SQL serverless du pool SQL dédié.

### 7.1 Pool SQL serverless

Le pool SQL serverless permet d'interroger des données stockées dans un Data Lake, notamment dans des formats tels que Parquet, CSV ou Delta Lake.

Il permet d'utiliser une syntaxe SQL de type T-SQL pour explorer les fichiers sans devoir systématiquement les charger dans un entrepôt relationnel dédié.

Ses usages possibles sont :
- explorer rapidement les données
- consulter des fichiers Parquet
- effectuer des filtres et des agrégations
- créer des vues logiques
- mettre les données à disposition d'outils d'analyse compatibles

Dans Retail Intelligence, il pourrait servir à consulter directement les résultats Silver ou Gold stockés dans ADLS Gen2.

### 7.2 Pool SQL dédié

Le pool SQL dédié fournit un environnement d'entreposage de données reposant sur des ressources de calcul provisionnées.

Il est destiné aux scénarios d'analyse relationnelle et d'entreposage de données nécessitant des capacités de calcul dédiées.

Il peut être pertinent lorsqu'une architecture nécessite de charger et d'organiser des données dans un entrepôt analytique relationnel.

Il n'est toutefois pas indispensable pour tous les projets Data Lake. Son intérêt doit être évalué selon les volumes, les performances attendues et les usages analytiques.

### 7.3 Comparaison des capacités SQL

| Critère | Pool SQL serverless | Pool SQL dédié |
|---|---|---|
| Fonction principale | Interroger les données du Data Lake | Fournir un entrepôt analytique relationnel |
| Ressources | Sans gestion de cluster dédié par l'utilisateur | Ressources de calcul provisionnées |
| Données | Lecture de fichiers dans le stockage | Données chargées dans l'environnement SQL dédié |
| Usage principal | Exploration et interrogation ponctuelle | Analyses relationnelles et entreposage |
| Adaptation au projet | Explorer les fichiers Silver et Gold | Évolution possible si un entrepôt relationnel devient nécessaire |

Le choix entre ces capacités dépendrait des besoins réels de la plateforme. Il n'est pas nécessaire de déployer les deux pour exploiter un Data Lake.

## 8. Exemple de fonctionnement global dans Retail Intelligence

Les services pourraient être associés dans une architecture cible selon le déroulement suivant :

1. Les données sources autorisées sont déposées dans ADLS Gen2, dans la zone Bronze.
2. Azure Data Factory organise les opérations d'ingestion et déclenche les traitements.
3. Les traitements de préparation sont exécutés avec les capacités retenues, par exemple des notebooks PySpark sur un pool Spark Synapse.
4. Les données transformées sont enregistrées dans la zone Silver.
5. Les agrégations et indicateurs validés sont publiés dans la zone Gold.
6. Les utilisateurs consultent les données avec les capacités SQL ou leurs outils décisionnels.

### Schéma logique simplifié

```text
Données sources autorisées
          |
          v
     ADLS Gen2
       Bronze
          |
          v
 Azure Data Factory
 Intégration et orchestration
          |
          v
 Azure Synapse Analytics
          |
     +----+----+
     |         |
     v         v
 Spark      SQL
 Traitement Exploration
 distribué  et analyse
     |         |
     +----+----+
          |
          v
     ADLS Gen2
       Silver
          |
          v
     Traitements
     et agrégations
          |
          v
     ADLS Gen2
        Gold
          |
          v
 Analyse métier
 et décisionnel
```

Ce schéma présente une possibilité d'architecture et non une architecture déployée.

Il faut également noter qu'ADF et Synapse disposent de capacités d'intégration et d'orchestration qui peuvent se recouper. Le choix entre une instance ADF distincte et les pipelines intégrés à un espace de travail Synapse dépendrait de l'organisation retenue. Les deux services ne sont donc pas nécessairement obligatoires ensemble.

## 9. Mise en relation avec l'environnement local existant

Le projet Retail Intelligence dispose déjà d'un environnement local qui permet de réaliser plusieurs des opérations étudiées.

| Besoin | Environnement local actuel | Équivalent ou possibilité Azure étudiée |
|---|---|---|
| Stockage des données | Système de fichiers local et Parquet | ADLS Gen2 |
| Organisation des zones | Bronze / Silver / Gold | Conteneur ADLS Gen2 avec HNS |
| Traitement distribué | Apache Spark / PySpark | Pools Apache Spark dans Synapse |
| Interrogation des données | Spark SQL / outils Python | Synapse SQL |
| Orchestration | Scripts et exécutions locales selon les traitements | Azure Data Factory ou pipelines Synapse |
| Développement analytique | Jupyter Notebook | Synapse Studio et notebooks |
| Analyse des résultats | Pandas, PySpark et visualisations | SQL, Synapse et outils décisionnels |

Cette comparaison porte sur les responsabilités fonctionnelles. Les outils ne sont pas strictement interchangeables : les services Azure sont intégrés à un environnement cloud administré, tandis que les outils locaux sont exécutés et gérés dans l'environnement Linux du projet.

## 10. Bilan : éléments étudiés et éléments non déployés

| Élément | Statut |
|---|---|
| Rôle d'Azure Data Factory | Étudié et documenté |
| Notions de pipeline et d'activités ADF | Étudiées et documentées |
| Rôle d'Azure Synapse Analytics | Étudié et documenté |
| Rôle de Synapse Studio | Étudié et documenté |
| Fonctionnement des Spark Pools | Étudié et documenté |
| Capacités SQL serverless et dédiées | Étudiées et documentées |
| Exemple d'architecture cible | Proposé sur le plan documentaire |
| Création d'une instance Azure Data Factory | Non exécutée |
| Création d'un Workspace Synapse | Non exécutée |
| Création d'un Spark Pool Azure | Non exécutée |
| Création d'un pipeline ADF ou Synapse | Non exécutée |
| Exécution d'un notebook dans Synapse | Non exécutée |
| Exécution d'une requête sur un pool SQL Azure | Non exécutée |

## 11. Conclusion

Cette étape a permis d'identifier les rôles complémentaires des services Azure étudiés.

ADLS Gen2 constitue le stockage des données. Azure Data Factory permet d'organiser leur intégration, leur déplacement et l'orchestration des traitements. Azure Synapse Analytics fournit un environnement analytique qui regroupe notamment des capacités SQL et Apache Spark. Synapse Studio constitue l'interface permettant de travailler avec ces différents composants.

Pour Retail Intelligence, cette architecture pourrait permettre de transposer les traitements locaux déjà réalisés avec PySpark et Parquet vers un environnement cloud intégré.

Dans le cadre du Parcours B, ces services ont été étudiés mais aucun déploiement Azure n'a été effectué. **Azure reste une perspective d'évolution future**.