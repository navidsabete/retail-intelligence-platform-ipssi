# Projet fil rouge - Retail Intelligence Platform (IPSSI)

# J1

## Présentation

Ce dépôt regroupe les livrables réalisés lors de la première journée du projet Retail Intelligence, dans le cadre des UC-01 et UC-02.

- **UC-01 :** cadrage métier, définition des indicateurs, exploration et qualification des sources de données TPCx-BB.
- **UC-02 :** comparaison des architectures Data Warehouse, Data Lake et Lakehouse, conception de l'architecture cible, description des flux, positionnement des composants, gouvernance et comparaison local / cloud.

## Organisation du dépôt

```text
J1_Retail_Intelligence/
├── README.md
│
├── 01_UC01_besoin_exploration/
│   ├── UC01_cadrage_metier.pdf
│   ├── UC01_questions_decisionnelles.pdf
│   ├── UC01_dictionnaire_KPI.xlsx
│   ├── UC01_inventaire_sources.xlsx
│   ├── UC01_qualification_donnees.pdf
│   ├── UC01_limites_et_hypotheses.pdf
│   └── preuves/
│
└── 02_UC02_architecture/
    ├── UC02_comparaison_architectures.pdf
    ├── UC02_architecture_cible.pdf
    ├── UC02_schema_flux.pdf
    ├── UC02_positionnement_composants.pdf
    ├── UC02_gouvernance.pdf
    └── UC02_local_vers_azure.pdf
```

## Présentation des livrables

### UC-01 – Besoin et exploration

| Livrable | Contenu |
|---|---|
| `UC01_cadrage_metier.pdf` | Profils métier, responsabilités et besoins identifiés. |
| `UC01_questions_decisionnelles.pdf` | Questions métier, décisions associées et niveaux de priorité. |
| `UC01_dictionnaire_KPI.xlsx` | Définition des indicateurs : formules, unités, filtres, périodicité et sources. |
| `UC01_inventaire_sources.xlsx` | Recensement des fichiers, formats, volumes et caractéristiques observées. |
| `UC01_qualification_donnees.pdf` | Analyse de la structure, de la qualité, des anomalies et des relations candidates entre tables. |
| `UC01_limites_et_hypotheses.pdf` | Limites des données, KPI exploitables, hypothèses et données complémentaires nécessaires, réponses aux questions de recul |
| `preuves/` | Rapports et éléments permettant de justifier les constats présentés dans les livrables UC-01. |

### UC-02 – Architecture des données

| Livrable | Contenu |
|---|---|
| `UC02_comparaison_architectures.pdf` | Comparaison des architectures Data Warehouse, Data Lake et Lakehouse. |
| `UC02_architecture_cible.pdf` | Justification du choix retenu, schéma logique de l'architecture cible, ses composants et les zones de données. |
| `UC02_schema_flux.pdf` | Description des flux depuis les sources jusqu'aux données analytiques et aux indicateurs. |
| `UC02_positionnement_composants.pdf` | Rôle et statut pédagogique des technologies : obligatoires, facultatives ou étudiées. |
| `UC02_gouvernance.pdf` | Règles minimales de traçabilité, documentation, qualité, accès, sécurité, suivi et maîtrise des coûts. |
| `UC02_local_vers_azure.pdf` | Comparaison de l'environnement local Ubuntu avec la cible cloud Azure ADLS Gen2. |

Les preuves UC-02 sont intégrées directement dans les livrables PDF concernés : schémas annotés, tableaux, exemples de fichiers réellement traités et de traitements réellement effectués. Aucun dossier `UC02_preuves/` distinct n'est donc nécessaire dans cette organisation.

Les éléments décrivant une cible cloud non déployée sont présentés comme une conception logique et non comme un déploiement réel.

## Périmètre technique

L'exploration porte sur les répertoires `data/` et `data_refresh/` du jeu de données synthétique TPCx-BB.

Les deux répertoires sont étudiés séparément. Leurs contenus ne sont pas fusionnés automatiquement, car les fichiers de rafraîchissement peuvent correspondre à des ajouts, des mises à jour ou à un périmètre différent.

Les fichiers `.DAT` utilisent le séparateur `|` et ne comportent pas d'en-têtes détectés. L'identification des colonnes repose donc provisoirement sur leur position. Les noms et significations métier doivent être confirmés à l'aide du dictionnaire de données.

Les principales familles de données concernent les clients, produits, magasins, ventes physiques et web, retours, stocks et navigation web. Les formats principalement observés sont `.DAT` et `.CSV`.

## Architecture cible – UC-02

L'architecture proposée est une approche **Lakehouse**, organisée en trois zones :

- **Bronze :** conservation des données brutes et de leur provenance.
- **Silver :** nettoyage, contrôle, harmonisation et préparation des données.
- **Gold :** tables analytiques et indicateurs destinés aux usages métier.

Cette architecture répond aux besoins de suivi des ventes, des produits, des magasins et des stocks, tout en tenant compte des limites de qualité et de granularité identifiées dans l'UC-01.

Les traitements sont envisagés principalement en batch. Une fréquence quotidienne peut être étudiée comme hypothèse, mais elle reste à confirmer selon les modalités réelles d'alimentation des sources.

## Positionnement des composants

| Composant | Positionnement dans le parcours |
|---|---|
| Linux / Ubuntu | Obligatoire – environnement local de référence. |
| Python | Obligatoire – exploration et scripts. |
| Hadoop / HDFS | Obligatoire – stockage distribué local. |
| Apache NiFi | Obligatoire – ingestion et orchestration. |
| Apache Spark / PySpark | Obligatoire – traitements distribués. |
| Parquet | Format de référence pour le stockage analytique. |
| HBase | Facultatif – approfondissement NoSQL. |
| PDGF | Selon disponibilité du kit. |
| Delta Lake | Facultatif – approfondissement Lakehouse. |
| ADLS Gen2 | Objectif obligatoire – déclinaison cloud du stockage. |
| Azure Data Factory | Présentation et étude. |
| Azure Synapse | Présentation et étude. |

Les composants facultatifs ne conditionnent pas la validation du socle pédagogique. La cible Azure est étudiée au niveau logique si aucun déploiement cloud n'est réalisé.

## Gouvernance et qualité

Les règles proposées prévoient :

- la traçabilité des sources, des dates d'arrivée et des traitements
- la documentation des fichiers, colonnes et tables
- les contrôles de valeurs manquantes, doublons, types et relations
- la gestion des accès selon les rôles métier
- la protection des données sensibles
- le suivi des exécutions, erreurs et volumes traités
- la maîtrise des coûts, du stockage et de la conservation des données.

La présence d'un fichier ou d'une colonne ne garantit pas à elle seule que l'information est exploitable pour un indicateur métier.

## Comparaison local / cloud

L'environnement local repose sur Linux / Ubuntu, Hadoop / HDFS, NiFi, Python et Spark.

La cible cloud s'appuie notamment sur Azure Data Lake Storage Gen2, avec une organisation Bronze, Silver et Gold. La gestion des identités et des accès repose sur Microsoft Entra ID, Azure RBAC et les ACL.

Cette comparaison constitue une conception logique de la cible cloud lorsque les services Azure ne sont pas effectivement déployés.

## Questions de recul – UC-02

**1. Pourquoi une architecture Data Lake peut-elle compléter un Data Warehouse ?**

Un Data Lake conserve des données brutes et variées, y compris lorsqu'elles ne sont pas encore structurées. Le Data Warehouse organise des données préparées et structurées pour les analyses et le reporting. Les deux approches peuvent donc être complémentaires : le Lake conserve la matière première et le Warehouse facilite les analyses métier.

**2. Dans quels cas une architecture Lakehouse peut-elle être pertinente ?**

Elle est pertinente lorsque l'on doit gérer des données variées et volumineuses, conserver les données brutes, effectuer des traitements distribués et fournir des données fiables pour les analyses. Elle combine la flexibilité du Data Lake avec des capacités de structuration et de gouvernance proches du Data Warehouse.

**3. Pourquoi conserver les données brutes ?**

Pour préserver les données d'origine, pouvoir reprendre les traitements, comparer les versions, corriger les transformations et assurer la traçabilité. Cela évite également de perdre des informations lors d'un nettoyage initial.

**4. Pourquoi organiser les données en zones ?**

Les zones séparent les étapes du traitement : conservation des données d'origine en Bronze, nettoyage et harmonisation en Silver, puis préparation des données métier en Gold. Cette séparation facilite le contrôle, la maintenance et la compréhension des flux.

**5. Quelles garanties ne sont pas apportées par le seul stockage de fichiers Parquet ?**

Parquet est un format de stockage colonnaire efficace, mais il ne garantit pas à lui seul la qualité des données, leur cohérence métier, la gestion des accès, la traçabilité, les transactions ou la gouvernance. Ces garanties nécessitent des traitements et des mécanismes complémentaires.

**6. Quels risques apparaissent lorsque la gouvernance est insuffisante ?**

Des données incohérentes ou mal documentées, des indicateurs erronés, des accès non autorisés, une perte de traçabilité, des traitements difficiles à reproduire et des coûts de stockage ou de traitement mal maîtrisés.

**7. Quels composants sont indispensables au socle du parcours et lesquels relèvent de l'approfondissement ?**

Le socle obligatoire comprend Linux / Ubuntu, Python, Hadoop / HDFS, NiFi et Spark / PySpark. Parquet est le format de référence. HBase et Delta Lake sont facultatifs ; PDGF dépend du kit disponible. ADLS Gen2 constitue l'objectif cloud obligatoire du parcours, tandis qu'Azure Data Factory et Azure Synapse sont étudiés sans déploiement complet.

## Documentation officielle complémentaire

Les ressources suivantes ont été utilisées pour documenter la déclinaison Azure :

- [Microsoft Learn – Présentation d'Azure Data Lake Storage Gen2](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction) : fonctionnement et espace de noms hiérarchique.
- [Microsoft Learn – Créer un compte de stockage ADLS Gen2](https://learn.microsoft.com/en-us/azure/storage/blobs/create-data-lake-storage-account) : configuration du compte et activation de l'espace de noms hiérarchique.
- [Microsoft Learn – Modèle de contrôle d'accès ADLS Gen2](https://learn.microsoft.com/fr-fr/azure/storage/blobs/data-lake-storage-access-control-model) : rôles RBAC et ACL.
- [Microsoft Learn – Sécurité du stockage Azure](https://learn.microsoft.com/en-us/azure/storage/common/secure-storage) : sécurisation des comptes et des accès.
- [Microsoft Learn – Optimisation des coûts Azure Blob Storage](https://learn.microsoft.com/en-us/azure/storage/blobs/blob-cost-optimization-services) : niveaux de stockage et gestion du cycle de vie.
- [Microsoft Learn – Objectifs d'évolutivité du stockage Azure](https://learn.microsoft.com/en-us/azure/storage/common/storage-scalability-targets) : limites de capacité et de performance.

## Méthode et traçabilité

L'UC-01 s'appuie sur un inventaire automatisé, une description des colonnes et un rapport d'anomalies. Les rapports d'analyse et les extraits utiles sont conservés dans `preuves/`.

L'UC-02 s'appuie sur les constats de l'UC-01 pour justifier les choix d'architecture. Les schémas, tableaux de positionnement, règles de gouvernance, comparaisons et preuves de manipulation sont intégrés aux six livrables PDF correspondants.

Les hypothèses et limites sont explicitement signalées, notamment lorsque les volumes, les règles métier, la fréquence d'alimentation ou les conditions de déploiement cloud ne sont pas confirmés.