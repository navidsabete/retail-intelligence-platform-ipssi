# Étape 2 – Découverte des commandes HDFS

## 1. Objectif

Cette étape consiste à découvrir et vérifier le fonctionnement de HDFS dans l'environnement préparé pour la formation. Les opérations portent sur l'état du système, les nœuds, les répertoires, la création d'un espace de travail, les permissions et la taille des données stockées.

## 2. Environnement utilisé

| Élément | Information |
|---|---|
| Système d'exploitation | Ubuntu 24.04.5 LTS |
| Hadoop | 3.5.0 |
| Java | OpenJDK 21.0.13 |
| Répertoire d'installation Hadoop | `/opt/hadoop` |
| NameNode | Actif |
| DataNode | Actif |
| SecondaryNameNode | Actif |
| Nombre de DataNodes | 1 |
| Mode de déploiement constaté | Mono-nœud |

## 3. Consultation de l'état du système HDFS

### Commande exécutée

```bash
hdfs dfsadmin -report
```

### Résultats relevés

| Indicateur | Résultat |
|---|---:|
| Capacité configurée | 1 006,85 Go |
| Capacité présente | 947,34 Go |
| Espace restant | 947,34 Go |
| Espace utilisé par HDFS | 32 Ko |
| Utilisation HDFS | 0,00 % |
| Espace restant | 94,09 % |
| DataNodes actifs | 1 |
| Blocs sous-répliqués | 0 |
| Blocs corrompus | 0 |
| Blocs manquants | 0 |

### Analyse

Le système HDFS répond correctement. Un DataNode est actif et aucun bloc manquant, corrompu ou sous-répliqué n'a été signalé. L'espace HDFS est disponible.

## 4. Informations sur les nœuds Hadoop

### Commande exécutée

```bash
jps
```

### Résultat obtenu

```text
25408 NameNode
25970 BootstrapProcess
25798 SecondaryNameNode
25544 DataNode
25994 NiFi
26236 Jps
```

### Analyse

Les processus `NameNode`, `DataNode` et `SecondaryNameNode` sont présents. Le processus NiFi est également actif. Le rapport HDFS indique un seul DataNode, identifié par `127.0.0.1:9866` : l'installation est donc mono-nœud.

## 5. Affichage des répertoires disponibles

### Commande exécutée

```bash
hdfs dfs -ls /
```

### Résultat obtenu

```text
Found 1 items
drwxr-xr-x   - [user] [group]          0 2026-11-17 15:32 /retail-lake
```

La racine HDFS contient un seul élément : `/retail-lake`.

### Consultation de l'espace Retail Lake

Commande exécutée :

```bash
hdfs dfs -ls /retail-lake
```

Résultat obtenu après création du répertoire de travail :

```text
Found 7 items
drwxr-xr-x   - [user] [group]          0 2026-11-17 15:32 /retail-lake/bronze
drwxr-xr-x   - [user] [group]          0 2026-11-17 15:32 /retail-lake/gold
drwxr-xr-x   - [user] [group]          0 2026-11-17 15:32 /retail-lake/logs
drwxr-xr-x   - [user] [group]          0 2026-11-17 15:32 /retail-lake/quality
drwxr-xr-x   - [user] [group]          0 2026-11-17 15:32 /retail-lake/raw
drwxr-xr-x   - [user] [group]          0 2026-11-17 15:32 /retail-lake/silver
drwxr-xr-x   - [user] [group]          0 2026-11-17 17:23 /retail-lake/workspace
```

### Analyse

Le répertoire `/retail-lake` contient les zones `raw`, `bronze`, `silver`, `gold`, `quality` et `logs`, ainsi que le répertoire de travail `workspace`.

## 6. Création d'un répertoire de travail

### Commande exécutée

La commande exécutée pour créer le répertoire de travail est :

```bash
hdfs dfs -mkdir -p /retail-lake/workspace
```

### Vérification

```bash
hdfs dfs -ls /retail-lake
```

Le résultat précédent confirme la présence de `/retail-lake/workspace`. Le répertoire a donc été créé avec succès.

## 7. Vérification des permissions

### Commandes exécutées

```bash
hdfs dfs -ls -d /retail-lake
hdfs dfs -ls -d /retail-lake/workspace
```

### Résultats obtenus

Pour `/retail-lake` :

```text
drwxr-xr-x   - [user] [group]          0 2026-11-17 17:23 /retail-lake
```

Pour `/retail-lake/workspace` :

```text
drwxr-xr-x   - [user] [group]          0 2026-11-17 17:23 /retail-lake/workspace
```

### Interprétation

| Élément | Valeur observée |
|---|---|
| Permissions | `drwxr-xr-x` |
| Propriétaire | `[user]` |
| Groupe | `[group]` |

Les permissions `rwxr-xr-x` indiquent que le propriétaire dispose des droits de lecture, écriture et traversée sur le répertoire. Le groupe et les autres utilisateurs disposent des droits de lecture et de traversée, mais pas du droit d'écriture.

Aucune erreur de permission n'a été signalée lors des opérations exécutées.

## 8. Consultation de la taille des données stockées

### Commande exécutée

```bash
hdfs dfs -du -h /retail-lake
```

### Résultat obtenu

```text
0  0  /retail-lake/bronze
0  0  /retail-lake/gold
0  0  /retail-lake/logs
0  0  /retail-lake/quality
0  0  /retail-lake/raw
0  0  /retail-lake/silver
0  0  /retail-lake/workspace
```

### Analyse

La taille affichée est nulle pour chacun des sous-répertoires de premier niveau. Aucun fichier n'est donc actuellement comptabilisé directement dans ces répertoires par cette commande. La liste récursive ci-dessous confirme que les éléments présents sont des répertoires et qu'aucun fichier n'a été affiché.

## 9. Vérification récursive de l'arborescence

### Commande exécutée

```bash
hdfs dfs -ls -R /retail-lake
```

### Résultat obtenu

```text
drwxr-xr-x   - [user] [group]          0 2026-11-17 15:32 /retail-lake/bronze
drwxr-xr-x   - [user] [group]          0 2026-11-17 15:32 /retail-lake/bronze/tpcxbb
drwxr-xr-x   - [user] [group]          0 2026-11-17 15:32 /retail-lake/gold
drwxr-xr-x   - [user] [group]          0 2026-11-17 15:32 /retail-lake/logs
drwxr-xr-x   - [user] [group]          0 2026-11-17 15:32 /retail-lake/quality
drwxr-xr-x   - [user] [group]          0 2026-11-17 15:32 /retail-lake/raw
drwxr-xr-x   - [user] [group]          0 2026-11-17 15:32 /retail-lake/raw/tpcxbb
drwxr-xr-x   - [user] [group]          0 2026-11-17 15:32 /retail-lake/raw/tpcxbb/initial
drwxr-xr-x   - [user] [group]          0 2026-11-17 15:32 /retail-lake/silver
drwxr-xr-x   - [user] [group]          0 2026-11-17 17:23 /retail-lake/workspace
```

### Analyse

L'arborescence contient également les répertoires suivants :

- `/retail-lake/bronze/tpcxbb`
- `/retail-lake/raw/tpcxbb`
- `/retail-lake/raw/tpcxbb/initial`

Ces répertoires existent, mais la sortie ne montre aucun fichier à l'intérieur. Il ne faut donc pas en déduire que les données TPCx-BB ont déjà été transférées dans HDFS.

## 10. Bilan des opérations

| Opération | Commande | Résultat |
|---|---|---|
| État général HDFS | `hdfs dfsadmin -report` | Réussi ; 1 DataNode actif, aucun bloc manquant ou corrompu |
| Processus Hadoop | `jps` | NameNode, DataNode et SecondaryNameNode présents |
| Liste de la racine | `hdfs dfs -ls /` | Réussi ; `/retail-lake` présent |
| Liste de Retail Lake | `hdfs dfs -ls /retail-lake` | Réussi ; 7 sous-répertoires |
| Création du répertoire de travail | `hdfs dfs -mkdir -p /retail-lake/workspace` | Réussi |
| Vérification des permissions | `hdfs dfs -ls -d ...` | Réussi ; permissions `drwxr-xr-x` |
| Taille des données | `hdfs dfs -du -h /retail-lake` | Réussi ; tailles affichées à 0 |
| Liste récursive | `hdfs dfs -ls -R /retail-lake` | Réussi ; arborescence présente, aucun fichier listé |

## 11. Erreurs rencontrées

Aucune erreur de commande ni erreur de permission n'a été communiquée pour les opérations présentées dans ce livrable.

## 12. Conclusion

Les commandes de découverte HDFS ont permis de vérifier le bon fonctionnement de l'environnement Hadoop 3.5.0. Le NameNode et le DataNode sont actifs, le système ne signale aucun bloc manquant ou corrompu et l'espace HDFS disponible est d'environ 947,34 Go.

L'arborescence `/retail-lake` est en place. Elle comprend les zones `raw`, `bronze`, `silver`, `gold`, `quality` et `logs`, ainsi que les répertoires de préparation TPCx-BB et le répertoire de travail `workspace`. Les permissions observées sont `drwxr-xr-x`, avec `[user]` comme propriétaire et `[group]` comme groupe.

Enfin, les commandes de taille et de parcours récursif ne montrent aucun fichier de données dans cette arborescence à ce stade. L'environnement HDFS est donc prêt pour les prochaines opérations d'ingestion des données TPCx-BB.