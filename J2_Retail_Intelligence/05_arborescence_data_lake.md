# Étape 3 — Arborescence du Data Lake
## Organisation des répertoires HDFS et schéma explicatif

**Projet :** Retail Intelligence Platform  
**Technologie de stockage :** HDFS  
**Racine du Data Lake :** `/retail-lake`

---

## 1. Objectif

Cette étape consiste à organiser le Data Lake dans HDFS afin de séparer clairement les données sources, les données préparées pour les traitements, les données analytiques, les contrôles qualité et les journaux techniques.

L'organisation retenue reprend les zones suivantes : **Raw, Bronze, Silver, Gold, Quality et Logs**. Elle conserve également une séparation des jeux de données TPCx-BB selon leur lot d'origine (`initial` et `refresh`).

## 2. Arborescence cible

L'arborescence logique retenue est la suivante :

```text
/retail-lake/
├── raw/
│   └── tpcxbb/
│       ├── initial/
│       └── refresh/
├── bronze/
│   └── tpcxbb/
│       ├── initial/
│       └── refresh/
├── silver/
│   └── tpcxbb/
│       ├── initial/
│       └── refresh/
├── gold/
│   └── tpcxbb/
│       ├── business/
│       └── analytics/
├── quality/
│   └── tpcxbb/
│       ├── reports/
│       └── rejected/
├── logs/
│   └── tpcxbb/
│       ├── ingestion/
│       └── processing/
└── workspace/
```

Le répertoire `workspace` est conservé comme espace de travail technique. Il ne constitue pas une zone de données métier du Data Lake.

Les sous-répertoires `initial` et `refresh` sont prévus dans **Raw, Bronze et Silver** pour permettre de suivre les lots tout au long des traitements. Dans **Gold**, les données sont organisées par usage métier ou analytique plutôt que par lot source, car cette zone est destinée à présenter des données préparées pour la consommation.

## 3. État constaté avant la création de l'arborescence cible

Lors de l'étape précédente, les commandes HDFS ont montré que les répertoires suivants existaient déjà :

```text
/retail-lake/
├── bronze/
│   └── tpcxbb/
├── gold/
├── logs/
├── quality/
├── raw/
│   └── tpcxbb/
│       └── initial/
├── silver/
└── workspace/
```

La liste récursive communiquée à l'étape 2 ne montrait que des répertoires et aucun fichier de données. La commande `hdfs dfs -du -h /retail-lake` indiquait également une taille de zéro pour les répertoires listés.

**Point important :** cette étape documente l'organisation des répertoires. La présence d'un répertoire ne signifie pas que les données correspondantes ont déjà été copiées ou transformées dans HDFS.

## 4. Commandes de création de l'arborescence

Les commandes suivantes permettent de créer les sous-répertoires manquants sans supprimer les répertoires déjà présents. L'option `-p` permet de créer les parents nécessaires et ne provoque pas d'erreur si un répertoire existe déjà.

```bash
hdfs dfs -mkdir -p /retail-lake/raw/tpcxbb/initial
hdfs dfs -mkdir -p /retail-lake/raw/tpcxbb/refresh

hdfs dfs -mkdir -p /retail-lake/bronze/tpcxbb/initial
hdfs dfs -mkdir -p /retail-lake/bronze/tpcxbb/refresh

hdfs dfs -mkdir -p /retail-lake/silver/tpcxbb/initial
hdfs dfs -mkdir -p /retail-lake/silver/tpcxbb/refresh

hdfs dfs -mkdir -p /retail-lake/gold/tpcxbb/business
hdfs dfs -mkdir -p /retail-lake/gold/tpcxbb/analytics

hdfs dfs -mkdir -p /retail-lake/quality/tpcxbb/reports
hdfs dfs -mkdir -p /retail-lake/quality/tpcxbb/rejected

hdfs dfs -mkdir -p /retail-lake/logs/tpcxbb/ingestion
hdfs dfs -mkdir -p /retail-lake/logs/tpcxbb/processing

hdfs dfs -mkdir -p /retail-lake/workspace
```

### Vérification après création

Exécuter les commandes suivantes après la création :

```bash
hdfs dfs -ls -R /retail-lake
hdfs dfs -du -h /retail-lake
```

La première commande permet de vérifier la présence de l'arborescence. La seconde permet d'observer l'espace occupé. Tant que les fichiers n'ont pas été déposés, les tailles peuvent rester nulles.


## 5. Rôle des différentes zones

### 5.1 Raw — conservation des données sources

La zone Raw conserve les fichiers tels qu'ils ont été reçus depuis leur source, sans modification du contenu.

Pour le jeu TPCx-BB, les lots `initial` et `refresh` sont conservés séparément. Cette conservation permet notamment de :

- garder une copie de référence des données d'origine
- pouvoir rejouer une ingestion ou un traitement
- comparer les lots initiaux et les lots de rafraîchissement
- faciliter les audits et les vérifications
- éviter qu'une transformation ultérieure ne fasse perdre l'information source

La zone Raw est donc la référence historique des données reçues. Les fichiers qui y sont déposés ne doivent pas être écrasés par les résultats des transformations.

### 5.2 Bronze — données ingérées et tracées

La zone Bronze contient les données intégrées dans le Data Lake après ingestion. Elle constitue la première zone de traitement.

Les données restent proches de leur format source, mais peuvent être accompagnées de métadonnées techniques ou avoir subi des opérations nécessaires à l'ingestion : normalisation de l'encodage, ajout d'informations de lot, contrôle du format ou conversion technique documentée.

La différence essentielle est donc la suivante :

- **Raw :** copie de référence des fichiers reçus, préservée sans transformation ;
- **Bronze :** données effectivement prises en charge par la plateforme, avec traçabilité de l'ingestion et éventuelles adaptations techniques documentées.

Bronze ne doit pas être confondue avec une zone de nettoyage métier approfondi.

### 5.3 Silver — données nettoyées et harmonisées

La zone Silver contient des données préparées pour être utilisées de manière fiable dans les traitements analytiques.

Les opérations possibles comprennent notamment :

- contrôle et harmonisation des types
- traitement documenté des valeurs manquantes
- détection et gestion des doublons
- normalisation des formats et des valeurs
- validation des règles de cohérence entre tables
- mise à disposition de données structurées et homogènes.


### 5.4 Gold — données prêtes pour les usages métier

La zone Gold contient des données organisées pour répondre aux besoins d'analyse et de pilotage.

Elle peut accueillir, par exemple :

- des indicateurs de vente
- des agrégats par période, magasin ou produit
- des tables de faits et de dimensions préparées pour l'analyse
- des jeux de données destinés aux tableaux de bord et aux analyses métier.

La zone Gold privilégie la lisibilité et l'efficacité pour les utilisateurs analytiques. Elle est construite à partir des données fiabilisées de Silver, et non directement à partir des fichiers bruts.

### 5.5 Quality — contrôles et résultats qualité

La zone Quality est réservée aux éléments permettant de mesurer et de suivre la qualité des données.

Elle peut contenir :

- les rapports de validation
- les statistiques de valeurs manquantes
- les résultats de contrôles de schéma et de types
- les anomalies détectées
- les références ou copies des enregistrements rejetés, selon les règles de conservation définies.

Séparer cette zone des données métier évite de mélanger les résultats de contrôle avec les tables utilisées pour l'analyse.

### 5.6 Logs — journaux techniques

La zone Logs conserve les traces techniques des opérations de la plateforme, par exemple :

- les exécutions d'ingestion
- les traitements et transformations
- les dates de début et de fin
- les volumes lus et écrits
- les erreurs et avertissements
- les identifiants d'exécution.

Les journaux facilitent le diagnostic des incidents, le suivi des traitements et l'audit des opérations. Ils sont distincts des rapports de qualité : les logs décrivent le déroulement technique, tandis que Quality décrit l'état et la conformité des données.

## 6. Séparation des responsabilités

| Zone | Contenu principal | Finalité |
|---|---|---|
| Raw | Fichiers sources d'origine | Conservation et possibilité de rejouer les traitements |
| Bronze | Données ingérées, proches de la source | Traçabilité et première prise en charge technique |
| Silver | Données nettoyées et harmonisées | Fiabilité et réutilisation |
| Gold | Données métier, agrégats et indicateurs | Analyse et aide à la décision |
| Quality | Rapports, contrôles et rejets | Mesure et suivi de la qualité |
| Logs | Journaux d'exécution | Supervision, diagnostic et audit |
| Workspace | Fichiers de travail temporaires | Préparation technique, hors zones métier |

Cette séparation rend l'architecture plus lisible et limite les confusions entre données, résultats de contrôle et informations techniques.

## 7. Conservation de la provenance

La provenance doit permettre de retrouver l'origine d'un jeu de données et de comprendre les transformations qu'il a subies.

La convention proposée consiste à conserver, à chaque étape, les informations suivantes dans les métadonnées, les manifestes ou les journaux associés :

- le nom du fichier source
- le lot d'origine (`initial` ou `refresh`)
- la zone et le chemin d'origine
- la date et l'heure d'ingestion
- l'identifiant du traitement ou de l'exécution
- le format et, si possible, la taille du fichier source
- les transformations appliquées et leur version
- les contrôles qualité exécutés et leurs résultats
- la destination produite dans la zone suivante.

Exemple de chaîne de traçabilité :

```text
Fichier source TPCX-BB
        |
        v
/raw/tpcxbb/initial/
        |
        | ingestion + identifiant de lot
        v
/bronze/tpcxbb/initial/
        |
        | nettoyage + harmonisation
        v
/silver/tpcxbb/initial/
        |
        | agrégation et préparation métier
        v
/gold/tpcxbb/business/
```

Les journaux correspondants sont conservés sous `/retail-lake/logs/tpcxbb/` et les résultats des contrôles sous `/retail-lake/quality/tpcxbb/`.

## 8. Schéma synthétique de l'architecture

```text
                         SOURCES TPCX-BB
                      (initial / refresh)
                               |
                               v
                    +----------------------+
                    |         RAW          |
                    | Fichiers d'origine   |
                    | conservés à l'identique
                    +----------------------+
                               |
                               v
                    +----------------------+
                    |        BRONZE        |
                    | Données ingérées     |
                    | Traçabilité technique|
                    +----------------------+
                               |
                               v
                    +----------------------+
                    |        SILVER        |
                    | Données nettoyées    |
                    | et harmonisées      |
                    +----------------------+
                               |
                               v
                    +----------------------+
                    |         GOLD         |
                    | Données métier       |
                    | et analytiques       |
                    +----------------------+

       +----------------------+  +----------------------+
       |       QUALITY        |  |         LOGS         |
       | Contrôles, rapports  |  | Exécutions, erreurs  |
       | et données rejetées  |  | et suivi technique   |
       +----------------------+  +----------------------+
          Suit la qualité          Trace les opérations
          des données              de la plateforme
```

Quality et Logs sont des zones transversales : elles accompagnent les différentes étapes du cycle de vie des données, sans se substituer aux zones Raw, Bronze, Silver et Gold.

## 9. Bilan et conclusion

L'arborescence proposée organise le Data Lake en zones ayant chacune une responsabilité précise. Raw préserve les sources, Bronze matérialise leur ingestion, Silver fiabilise les données, et Gold les prépare pour les usages métier. Quality et Logs assurent respectivement le suivi de la qualité et la traçabilité technique.

La séparation des lots `initial` et `refresh` permet de conserver leur origine tout au long des premières étapes du pipeline. La provenance sera renforcée par des métadonnées d'ingestion, des identifiants de lots, des manifestes et des journaux de traitement.