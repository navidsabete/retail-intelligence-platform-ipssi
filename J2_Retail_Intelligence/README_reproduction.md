# README — Reproduction technique
## Retail Intelligence Platform — J2 : stockage et ingestion

> **Périmètre.** Ce document décrit la reproduction de l'environnement observé et des opérations documentées dans les fiches du TP. Il distingue les commandes exécutées des vérifications restant à réaliser. Les commandes supposent un terminal Ubuntu/WSL2 et les chemins constatés dans l'environnement pédagogique.

## 1. Environnement constaté

| Composant | Version / valeur constatée |
|---|---|
| Système | Ubuntu 24.04.5 LTS, environnement WSL2 indiqué dans la fiche NiFi |
| Architecture | Linux x86_64 |
| Java | OpenJDK 21.0.13.0.3 |
| Hadoop / HDFS | Hadoop 3.5.0 |
| Installation Hadoop | `/opt/hadoop` |
| Apache NiFi | 2.12.0 (version identifiée dans la fiche de découverte NiFi du 18/11/2026) |
| Installation NiFi | `/opt/nifi` |
| Python | 3.12.3 |
| `JAVA_HOME` | `/usr/lib/jvm/java-21-openjdk-amd64` |
| Interface NiFi | `https://localhost:8443/nifi` |

**Précision sur les relevés :** la fiche d'environnement du 17/11/2026 indiquait que la version de NiFi n'avait pas encore été relevée. La fiche de découverte du 18/11/2026 identifie ensuite NiFi 2.12.0 à partir des bibliothèques installées. Il ne s'agit donc pas de deux versions différentes, mais de deux dates de relevé.

## 2. Préparer le terminal

Les chemins suivants sont utilisés pour déclarer des variables d'environnements. Ils peuvent être exportés dans le terminal pour simplifier les commandes :

```bash
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export HADOOP_HOME=/opt/hadoop
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export NIFI_HOME=/opt/nifi
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
```

Vérifier les versions et les chemins :

```bash
java -version
hadoop version
python3 --version
ls -ld "$HADOOP_HOME" "$NIFI_HOME"
```

Résultats de référence consignés dans les fiches : Java 21.0.13.0.3, Hadoop 3.5.0 et Python 3.12.3.

## 3. Démarrer les services

### 3.1 HDFS

Dans un terminal Ubuntu :

```bash
start-dfs.sh
```

Contrôler les processus :

```bash
jps
```

Les processus attendus dans l'environnement documenté sont `NameNode`, `DataNode` et `SecondaryNameNode`.

Contrôler l'état du stockage :

```bash
hdfs dfsadmin -report
```

**État observé dans le TP :** un DataNode actif, sur `localhost` (`127.0.0.1:9866`), aucun bloc manquant ou corrompu signalé. Le déploiement est mono-nœud.

> Ne pas exécuter `hdfs namenode -format` pour démarrer ou dépanner un cluster déjà initialisé. Cette commande réinitialise les métadonnées du NameNode et peut rendre les données HDFS existantes inaccessibles.

### 3.2 Apache NiFi

Dans le terminal :

```bash
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export NIFI_HOME=/opt/nifi

"$NIFI_HOME/bin/nifi.sh" start
"$NIFI_HOME/bin/nifi.sh" status
```

Accéder à l'interface :

```text
https://localhost:8443/nifi
```

L'authentification est activée dans l'environnement observé. Utiliser les identifiants fournis ou configurés pour l'environnement de formation ; ne pas inscrire de mot de passe dans ce README.

Contrôler les paramètres HTTPS non sensibles :

```bash
grep -E '^(nifi.web.https.host|nifi.web.https.port|nifi.web.http.host|nifi.web.http.port)' \
  "$NIFI_HOME/conf/nifi.properties"
```

Valeurs observées :

```properties
nifi.web.http.host=
nifi.web.http.port=
nifi.web.https.host=0.0.0.0
nifi.web.https.port=8443
```

## 4. Vérifier et préparer le Data Lake HDFS

### 4.1 Vérifier l'espace projet

```bash
hdfs dfs -ls /
hdfs dfs -ls -R /retail-lake
hdfs dfs -du -h /retail-lake
```

La racine du Data Lake est :

```text
/retail-lake
```

### 4.2 Créer l'arborescence logique

La commande `-mkdir -p` crée les répertoires parents manquants et peut être relancée sans supprimer les contenus existants.

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

Arborescence cible :

```text
/retail-lake/
├── raw/tpcxbb/{initial,refresh}/
├── bronze/tpcxbb/{initial,refresh}/
├── silver/tpcxbb/{initial,refresh}/
├── gold/tpcxbb/{business,analytics}/
├── quality/tpcxbb/{reports,rejected}/
├── logs/tpcxbb/{ingestion,processing}/
└── workspace/
```

`workspace` est un espace de travail technique et non une zone métier du Data Lake.

### 4.3 Rôle des zones

| Zone | Responsabilité |
|---|---|
| Raw | Conservation de la copie source, sans modification du contenu |
| Bronze | Données prises en charge par l'ingestion, proches du format source et accompagnées de métadonnées techniques |
| Silver | Données nettoyées, contrôlées et harmonisées |
| Gold | Données préparées pour les usages métier, indicateurs et analyses |
| Quality | Rapports de contrôles, anomalies et données rejetées |
| Logs | Journaux techniques des exécutions et traitements |

Les lots `initial` et `refresh` sont séparés dans Raw, Bronze et Silver pour préserver leur distinction. Gold est organisée par usage métier ou analytique.

## 5. Déposer les fichiers TPCX-BB dans Raw

### 5.1 Fichiers réellement déposés et contrôlés

Deux fichiers du lot initial ont été utilisés :

| Fichier | Domaine | Taille locale | Lignes | Champs |
|---|---|---:|---:|---:|
| `customer.dat` | Clients | 13 279 063 octets | 99 000 | 18 |
| `store_sales.dat` | Ventes magasin | 92 764 700 octets | 667 579 | 23 |

Les fichiers sont des textes délimités par `|`, sans ligne d'en-tête. Les champs sont provisoirement repérés par position (`colonne_1`, etc.) tant que le schéma métier n'a pas été associé.

Les chemins relatifs observés dans le jeu de données sont :

```text
retail_project/data/customer/customer.dat
retail_project/data/store_sales/store_sales.dat
```

### 5.3 Copier les fichiers dans HDFS

La destination Raw du lot initial est :

```text
/retail-lake/raw/tpcxbb/initial/
```

Commandes de dépôt documentées :

```bash
hdfs dfs -put ./retail_project/data/customer/customer.dat \
  /retail-lake/raw/tpcxbb/initial/

hdfs dfs -put ./retail_project/data/store_sales/store_sales.dat \
  /retail-lake/raw/tpcxbb/initial/
```

Les fichiers locaux ont été conservés lors de cette opération.

**Attention aux relances :** `-put` peut échouer si le fichier de destination existe déjà. Ne pas supprimer ou écraser une copie Raw sans procédure de contrôle. Vérifier d'abord la présence du fichier et comparer son contenu.

### 5.4 Vérifier le dépôt et l'intégrité

```bash
hdfs dfs -ls -h /retail-lake/raw/tpcxbb/initial/
hdfs dfs -du -h /retail-lake/raw/tpcxbb/initial/

hdfs dfs -cat /retail-lake/raw/tpcxbb/initial/customer.dat | head -n 3
hdfs dfs -cat /retail-lake/raw/tpcxbb/initial/store_sales.dat | head -n 3
```

Comparer les empreintes SHA-256 locales et celles du contenu relu depuis HDFS :

```bash
sha256sum ./retail_project/data/customer/customer.dat
hdfs dfs -cat /retail-lake/raw/tpcxbb/initial/customer.dat | sha256sum

sha256sum ./retail_project/data/store_sales/store_sales.dat
hdfs dfs -cat /retail-lake/raw/tpcxbb/initial/store_sales.dat | sha256sum
```

Les fiches indiquent que les empreintes locales et HDFS ont été identiques pour les deux fichiers.

Les tailles HDFS relevées avec `-h` étaient environ 12,7 MiB pour `customer.dat` et 88,5 MiB pour `store_sales.dat`, cohérentes avec les tailles locales exactes.

## 6. Flux NiFi GetFile → PutHDFS

### 6.1 Principe et paramètres documentés

Le flux prévu pour transférer `customer.dat` est :

```text
/data/nifi/input
       |
       v
    GetFile
       |
    success
       |
       v
    PutHDFS
       |
       v
/retail-lake/raw/nifi
```

Configuration de `GetFile` :

| Propriété | Valeur |
|---|---|
| Input Directory | `/data/nifi/input` |
| Keep Source File | `false` |
| Recurse Subdirectories | `false` |

Configuration de `PutHDFS` :

| Propriété | Valeur |
|---|---|
| Hadoop Configuration Resources | `/opt/hadoop/etc/hadoop/core-site.xml` et `/opt/hadoop/etc/hadoop/hdfs-site.xml` |
| Directory | `/retail-lake/raw/nifi` |
| Conflict Resolution Strategy | `fail` |

Le processeur `PutHDFS` a été démarré avant `GetFile`, puis le flux a été exécuté.

### 6.2 Préparer le répertoire d'entrée et la destination

```bash
sudo mkdir -p /data/nifi/input
hdfs dfs -mkdir -p /retail-lake/raw/nifi
```

Copier le fichier de test dans le répertoire local surveillé, en adaptant le chemin source si nécessaire :

```bash
sudo cp ./retail_project/data/customer/customer.dat /data/nifi/input/
```

Vérifier que l'utilisateur exécutant NiFi peut lire le fichier et accéder au répertoire.

### 6.3 Configurer et exécuter dans l'interface

1. Ouvrir `https://localhost:8443/nifi`.
2. Ajouter un processeur `GetFile` et renseigner les propriétés ci-dessus.
3. Ajouter un processeur `PutHDFS` et renseigner les propriétés ci-dessus.
4. Relier la relation `success` de `GetFile` à `PutHDFS`.
5. Vérifier que la destination HDFS existe et que NiFi dispose des droits nécessaires.
6. Démarrer `PutHDFS`, puis `GetFile`.
7. Examiner les compteurs, les files d'attente et les bulletins des processeurs.

**Paramètre à manier avec précaution :** `Keep Source File=false` signifie que GetFile peut supprimer le fichier local après sa prise en charge réussie. Pour des essais reproductibles, envisager `true` ou utiliser une copie de travail.

### 6.4 Contrôle obligatoire après exécution

```bash
hdfs dfs -ls -h /retail-lake/raw/nifi
hdfs dfs -du -h /retail-lake/raw/nifi
```

## 7. Commandes de vérification récapitulatives

```bash
# Processus Java
jps

# État HDFS
hdfs dfsadmin -report

# Arborescence et fichiers du Data Lake
hdfs dfs -ls -R /retail-lake

# Volumes stockés
hdfs dfs -du -h /retail-lake

# État NiFi
/opt/nifi/bin/nifi.sh status

# Derniers journaux NiFi (extrait seulement)
tail -n 50 /opt/nifi/logs/nifi-app.log
```

## 8. Arrêter les services

Arrêter d'abord les flux NiFi depuis l'interface si nécessaire, puis arrêter NiFi :

```bash
/opt/nifi/bin/nifi.sh stop
/opt/nifi/bin/nifi.sh status
```

Arrêter ensuite HDFS :

```bash
stop-dfs.sh
```

Vérifier les processus :

```bash
jps
```

L'arrêt ne supprime pas les données HDFS. Ne pas supprimer les répertoires de métadonnées Hadoop ou les répertoires de dépôt NiFi pour effectuer un arrêt normal.