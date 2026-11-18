# Fiche d'environnement technique

**Projet :** Retail Intelligence Platform  
**Date du relevé :** 17/11/2026

## 1. Synthèse de l'environnement

| Élément | Valeur constatée | Preuve/Commande |
|---|---|---|
| Système d'exploitation | Ubuntu 24.04.5 LTS (Noble Numbat) | `cat /etc/os-release` |
| Architecture | Linux x86_64 | Compilation Hadoop indiquée `linux-x86_64` |
| Java | OpenJDK 21.0.13.0.3 | `java -version` |
| Hadoop | 3.5.0 | `hadoop version` |
| NiFi | Version non relevée ; processus actif et statut UP | `/opt/nifi/bin/nifi.sh status` |
| Python | 3.12.3 | `python3 --version` |

## 2. Chemins d'installation

| Composant | Chemin / variable constaté | Commentaire |
|---|---|---|
| Java | `/usr/lib/jvm/java-21-openjdk-amd64` (`JAVA_HOME`) | Défini pour la commande de statut NiFi |
| Hadoop | `/opt/hadoop` | Déduit du chemin du JAR affiché par `hadoop version` : `/opt/hadoop/share/hadoop/common/...` |
| NiFi | `/opt/nifi` (`NIFI_HOME`) | Chemin utilisé pour exécuter `nifi.sh` |
| Python | Chemin exact non relevé | Version 3.12.3 ; relever avec `which python3` si nécessaire |

## 3. État des services

| Composant | État observé | Preuve / remarque |
|---|---|---|
| NameNode | Actif | Présent dans `jps` |
| DataNode | Actif | Présent dans `jps` et 1 DataNode live dans le rapport HDFS |
| SecondaryNameNode | Actif | Présent dans `jps` |
| NiFi | UP | `nifi.sh status` : `Command Status [SUCCESS] HTTP 200`, `Status: UP` |
| BootstrapProcess | Présent | Processus de démarrage NiFi visible dans `jps` |
| ResourceManager / NodeManager | Non observés | Absents de la sortie `jps` fournie ; YARN n'est pas démontré comme actif |

## 4. État HDFS

La commande `hdfs dfsadmin -report` a répondu correctement.

| Indicateur | Valeur observée |
|---|---:|
| DataNodes actifs | 1 |
| DataNodes morts | 0 signalé |
| Capacité configurée | 1 006,85 Go |
| Capacité présente | 947,34 Go |
| Espace HDFS restant | 947,34 Go |
| Espace HDFS utilisé | 32 Ko |
| Pourcentage utilisé | 0,00 % (arrondi par Hadoop) |
| Pourcentage restant | 94,09 % |
| Blocs sous-répliqués | 0 |
| Blocs avec répliques corrompues | 0 |
| Blocs manquants | 0 |
| Nombre de blocs du DataNode | 0 |

Le DataNode annoncé est `127.0.0.1:9866` (`localhost`).

**Interprétation :** HDFS répond et un DataNode est enregistré. Le rapport ne signale aucun bloc manquant ou corrompu. Le nombre de blocs égal à zéro et l'utilisation de 32 Ko indiquent que le système HDFS est encore quasiment vide au moment de la mesure.

## 5. Répertoires HDFS du projet

La commande `hdfs dfs -ls /retail-lake` a réussi et a retourné six répertoires :

```text
/retail-lake/bronze
/retail-lake/gold
/retail-lake/logs
/retail-lake/quality
/retail-lake/raw
/retail-lake/silver
```

Cette observation confirme que la racine `/retail-lake` et ses six sous-répertoires existent dans HDFS. Elle ne prouve pas encore que des fichiers de données y ont été ingérés.

## 6. Configuration et contraintes

| Élément | Valeur |
|---|---|
| `JAVA_HOME` utilisé pour NiFi | `/usr/lib/jvm/java-21-openjdk-amd64` |
| `HADOOP_HOME` | Non relevé directement ; installation repérée sous `/opt/hadoop` |
| `NIFI_HOME` | `/opt/nifi` |
| `fs.defaultFS` | Non relevé |
| `dfs.replication` | Non relevé |
| Répertoire de métadonnées NameNode | Non relevé |
| Répertoire de stockage DataNode | Non relevé |
| Ressources CPU / RAM | Non relevées |
| Contraintes réseau / permissions | Non relevées |

## 7. Conclusion

L'environnement repose sur Ubuntu 24.04.5 LTS, OpenJDK 21.0.13.0.3, Hadoop 3.5.0 et Python 3.12.3. NiFi est installé sous `/opt/nifi` et son statut est `UP` (HTTP 200). Hadoop est installé sous `/opt/hadoop` et les processus NameNode, DataNode et SecondaryNameNode sont actifs.

HDFS est accessible, avec un seul DataNode local (`localhost`). Il s'agit donc d'un environnement mono-nœud adapté à l'apprentissage et aux tests, mais qui ne fournit pas la haute disponibilité d'un cluster de production. La racine `/retail-lake` contient déjà les répertoires `bronze`, `gold`, `logs`, `quality`, `raw` et `silver`.