# Étape 7 à 9 — Flux GetFile vers PutHDFS avec NiFi

## 1. Objectif

L'objectif de cette étape est de mettre en place un flux d'ingestion automatisé avec NiFi afin de transférer le fichier `customer.dat` depuis un répertoire local vers HDFS.

Le transfert est réalisé à l'aide de deux processeurs :
- `GetFile` : lecture du fichier depuis le système local.
- `PutHDFS` : écriture du fichier dans le Data Lake HDFS.

## 2. Schéma du flux

Le flux réalisé est le suivant :

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

**Preuve :** `01_flux_getfile_puthdfs.png`

## 3. Configuration des processeurs

### 3.1 GetFile

| Propriété | Valeur |
|---|---|
| Input Directory | `/data/nifi/input` |
| Keep Source File | `false` |
| Recurse Subdirectories | `false` |

**Preuve :** `02_configuration_getfile.png`

### 3.2 PutHDFS

| Propriété | Valeur |
|---|---|
| Hadoop Configuration Resources | `/opt/hadoop/etc/hadoop/core-site.xml` & `/opt/hadoop/etc/hadoop/hdfs-site.xml` |
| Directory | `/retail-lake/raw/nifi` |
| Conflict Resolution Strategy | `fail` |

**Preuve :** `03_configuration_puthdfs-1.png` & `03_configuration_puthdfs-2.png`

## 4. Exécution du flux

Le processeur `PutHDFS` a été démarré avant `GetFile`. Le flux a ensuite été exécuté afin de transférer le fichier `customer.dat`.

**Preuve :** `04_execution_nifi.png`

## 5. Vérification dans HDFS

La présence du fichier dans le répertoire cible a été vérifiée avec les commandes :

```bash
hdfs dfs -ls -h /retail-lake/raw/nifi
hdfs dfs -du -h /retail-lake/raw/nifi
```

**Résultat :** À compléter avec la sortie réelle des commandes.

**Preuve :** `05_presence_fichier_hdfs.png`