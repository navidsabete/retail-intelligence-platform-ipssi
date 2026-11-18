# Projet fil rouge – Retail Intelligence Platform (IPSSI)

# J2

## Présentation

Ce dépôt regroupe les livrables réalisés lors de la deuxième journée du projet Retail Intelligence Platform, dans le cadre des UC-03 et UC-04.

- **UC-03 :** mise en place de l'environnement de stockage Hadoop / HDFS, découverte des commandes HDFS, organisation du Data Lake en zones, dépôt des données TPCx-BB et vérification du stockage.
- **UC-04 :** découverte d'Apache NiFi, conception et exécution de flux d'ingestion, transfert de fichiers vers HDFS, gestion des erreurs et traçabilité des traitements.

Cette deuxième journée s'appuie sur les travaux du J1, notamment l'inventaire des données TPCX-BB et l'architecture cible définie pour Retail Intelligence.

## Organisation du dépôt

```text
J2_Retail_Intelligence/
├── README.md
├── README_reproduction.md
├── questions_de_recul.md
│
├── UC03_Hadoop-HDFS-creation-Data-Lake/
│   ├── 01_fiche_environnement_technique.md
│   ├── 02_decouverte_hadoop_hdfs.md
│   ├── 03_inventaire_donnees_tpcxbb.md
│   ├── 04_commandes_resultats_hdfs.md
│   ├── 05_arborescence_data_lake.md
│   ├── 06_depot_donnees_tpcxbb.md
│   ├── 07_verification_stockage.md
│
└── UC04_Ingestion-orchestration-avec-ApacheNiFi/
    ├── 08_fiche_decouverte_nifi.md
    ├── 09_flux_getfile_puthdfs.md
    ├── 10_erreur_controlee.md
    ├── 11_tracabilite_provenance.md
    └── preuves/
```


## Présentation des livrables

### UC-03 – Stockage et organisation du Data Lake

| Livrable | Contenu |
|---|---|
| `01_fiche_environnement_technique.md` | Versions des composants, configuration et état de l'environnement technique. |
| `02_decouverte_hadoop_hdfs.md` | Découverte de Hadoop, rôle des nœuds et vérification du fonctionnement HDFS. |
| `03_inventaire_donnees_tpcxbb.md` | Inventaire des fichiers sources TPCX-BB et caractéristiques observées. |
| `04_commandes_resultats_hdfs.md` | Commandes HDFS exécutées et résultats des vérifications. |
| `05_arborescence_data_lake.md` | Organisation du Data Lake et description des zones Raw, Bronze, Silver, Gold, Quality et Logs. |
| `06_depot_donnees_tpcxbb.md` | Sélection, contrôle et dépôt de fichiers TPCX-BB dans HDFS. |
| `07_verification_stockage.md` | Contrôle de présence, tailles, permissions, accessibilité et intégrité des fichiers stockés. |

### UC-04 – Ingestion et orchestration avec NiFi

| Livrable | Contenu |
|---|---|
| `08_fiche_decouverte_nifi.md` | Présentation de NiFi, environnement, interface, composants et concepts principaux. |
| `09_flux_getfile_puthdfs.md` | Configuration du flux d'ingestion GetFile vers PutHDFS pour transférer un fichier local dans HDFS. |
| `10_erreur_controlee.md` | Simulation d'une erreur de chemin source, identification et correction. |
| `11_tracabilite_provenance.md` | Consultation des événements de provenance et suivi du parcours d'un FlowFile. |

Les preuves des manipulations sont présentes dans le dossier `preuves/` de l'UC-03 ou de l'UC-04 lorsqu'il existe. En l'absence de dossier dédié, les captures d'écran, sorties de commandes et éléments justificatifs sont intégrés directement dans les fiches documentaires concernées.

## Périmètre technique

L'environnement pédagogique repose sur Ubuntu 24.04.5 LTS, avec les composants suivants :

| Composant | Version constatée |
|---|---|
| Java | OpenJDK 21.0.13 |
| Hadoop / HDFS | 3.5.0 |
| Apache NiFi | 2.12.0 |
| Python | 3.12.3 |

Hadoop est installé sous `/opt/hadoop` et NiFi sous `/opt/nifi`.

L'environnement HDFS est configuré en mono-nœud, avec un NameNode et un DataNode local.

Les données utilisées proviennent du jeu synthétique TPCX-BB, notamment des répertoires `data/` et `data_refresh/`.

## Organisation du Data Lake

Le stockage HDFS repose sur la racine `/retail-lake`, organisée en plusieurs zones :

- **Raw :** conservation des fichiers sources dans leur format d'origine.
- **Bronze :** données ingérées et accompagnées de leur traçabilité technique.
- **Silver :** données nettoyées, contrôlées et harmonisées.
- **Gold :** données préparées pour les usages analytiques et métier.
- **Quality :** rapports de contrôle et données rejetées.
- **Logs :** journaux d'ingestion et de traitement.

Les lots `initial` et `refresh` sont conservés séparément dans les zones Raw, Bronze et Silver afin de préserver leur provenance.

## Ingestion avec Apache NiFi

Un premier flux d'ingestion a été construit pour transférer un fichier local vers HDFS :

`GetFile → PutHDFS`

- **GetFile :** récupération d'un fichier depuis `/data/nifi/input`.
- **PutHDFS :** dépôt du fichier dans `/retail-lake/raw/nifi`.

Le fonctionnement des processeurs, les connexions, la gestion des erreurs et les événements de provenance ont été étudiés.

Un test d'erreur contrôlée a également été réalisé en configurant volontairement un répertoire source inexistant, puis en corrigeant le chemin.

La consultation de la provenance permet de suivre les événements associés à un FlowFile, notamment sa réception par GetFile et son envoi par PutHDFS.

## Questions de recul

Les questions de recul relatives à cette journée sont présentes dans `questions_de_recul.md`.

## Continuité du projet

Le J2 constitue la première mise en œuvre technique de l'architecture étudiée au J1.

Il permet de passer de la conception à la mise en place du stockage et des premiers flux d'ingestion.

Les données déposées dans HDFS et les mécanismes de traçabilité mis en place constituent une première base pour les prochaines étapes du projet : contrôles qualité, transformations, structuration analytique et alimentation des zones Silver et Gold.