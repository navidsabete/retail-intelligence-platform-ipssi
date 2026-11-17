# Fiche de découverte Hadoop et HDFS

**Projet :** Retail Intelligence Platform  
**Date du relevé :** 17/11/2026  
**Environnement :** Ubuntu 24.04.5 LTS — machine locale

## 1. Objectif

Vérifier la disponibilité de Hadoop et de HDFS, identifier les démons actifs, déterminer le type de déploiement et contrôler l'espace de stockage avant l'ingestion des données Retail Intelligence.

## 2. Versions observées

| Composant | Version / résultat |
|---|---|
| Ubuntu | 24.04.5 LTS (Noble Numbat) |
| Java | OpenJDK 21.0.13.0.3 |
| Hadoop | 3.5.0 |
| Python | 3.12.3 |
| NiFi | Version non relevée ; statut UP |

Le chemin du JAR Hadoop indiqué par la commande `hadoop version` est `/opt/hadoop/share/hadoop/common/hadoop-common-3.5.0.jar`, ce qui permet de situer l'installation Hadoop sous `/opt/hadoop`.

## 3. Composants Hadoop observés

La commande `jps` a retourné :

```text
25408 NameNode
25970 BootstrapProcess
25798 SecondaryNameNode
25544 DataNode
25994 NiFi
26236 Jps
```

| Processus | Rôle | État constaté |
|---|---|---|
| NameNode | Gère les métadonnées et l'espace de noms HDFS | Présent |
| DataNode | Stocke les blocs de données HDFS | Présent |
| SecondaryNameNode | Réalise périodiquement des points de contrôle des métadonnées | Présent |
| BootstrapProcess | Processus de bootstrap de NiFi | Présent |
| NiFi | Orchestration des flux de données | Présent |
| Jps | Outil Java qui affiche les processus Java | Présent pendant la commande |

Le SecondaryNameNode n'est pas un NameNode de secours assurant automatiquement la haute disponibilité. Sa fonction principale est d'aider à produire des points de contrôle des métadonnées.

## 4. Rôle du NameNode et des DataNodes

### NameNode

Le NameNode est le composant maître de HDFS. Il gère l'espace de noms (répertoires, fichiers, permissions) et les métadonnées qui indiquent où sont stockés les blocs. Il coordonne les opérations d'accès aux fichiers et suit l'état des DataNodes.

Le NameNode ne stocke normalement pas le contenu courant des fichiers utilisateur : les blocs de données sont stockés sur les DataNodes.

### DataNode

Les DataNodes stockent les blocs des fichiers HDFS sur leurs disques locaux. Ils répondent aux opérations de lecture et d'écriture et communiquent périodiquement au NameNode leur état, notamment au moyen de signaux de vie et de rapports de blocs.

### Fonctionnement simplifié

1. Un client demande au NameNode les métadonnées nécessaires pour accéder à un fichier.
2. Le NameNode indique au client où se trouvent les blocs ou comment les placer.
3. Le client échange les données directement avec les DataNodes.
4. HDFS peut répliquer les blocs selon le facteur de réplication configuré.
5. Le NameNode suit les blocs et l'état des DataNodes.

## 5. État du cluster selon `hdfs dfsadmin -report`

| Indicateur | Valeur observée |
|---|---:|
| DataNodes actifs | 1 |
| DataNodes morts | 0 signalé |
| Capacité configurée | 1 006,85 GB |
| Capacité présente | 947,34 GB |
| Espace restant HDFS | 947,34 GB |
| Espace utilisé HDFS | 32 KB |
| Espace restant (%) | 94,09 % |
| Blocs sous-répliqués | 0 |
| Blocs corrompus | 0 |
| Blocs manquants | 0 |
| Blocs sur le DataNode | 0 |

Le DataNode est joignable à `127.0.0.1:9866` et son nom d'hôte est `localhost`. Son statut de décommissionnement est `Normal`.

**Analyse :** le rapport est obtenu sans erreur et un DataNode est actif. Aucun problème de blocs n'est signalé. Le nombre de blocs égal à zéro indique qu'aucun bloc de données HDFS n'est actuellement comptabilisé sur ce DataNode au moment du relevé.

## 6. Type de déploiement

- [x] Environnement mono-nœud / local (un seul DataNode sur localhost)
- [ ] Cluster distribué multi-machines
- [ ] Indéterminé

**Justification :** le rapport HDFS annonce un seul DataNode, à l'adresse `127.0.0.1`, avec le nom d'hôte `localhost`. Les processus NameNode et DataNode sont présents sur l'environnement local. Les éléments fournis ne montrent pas de nœuds de stockage distants.

Cet environnement est adapté à l'apprentissage et à la validation des opérations HDFS. Il ne doit pas être présenté comme un cluster de production hautement disponible.

## 7. Vérification de l'espace projet

La commande `hdfs dfs -ls /retail-lake` a réussi :

```text
Found 6 items
/retail-lake/bronze
/retail-lake/gold
/retail-lake/logs
/retail-lake/quality
/retail-lake/raw
/retail-lake/silver
```

Les six répertoires existent. Cette commande liste les répertoires mais ne démontre pas que les fichiers de données TPCx-BB ont déjà été transférés.

## 8. Architecture HDFS constatée

```text
Machine locale Ubuntu 24.04.5
│
├── NameNode
│   └── Métadonnées et espace de noms HDFS
│
├── SecondaryNameNode
│   └── Points de contrôle des métadonnées
│
├── DataNode (localhost / 127.0.0.1:9866)
│   └── Stockage des blocs HDFS
│
└── Répertoire HDFS du projet : /retail-lake
    ├── bronze/
    ├── gold/
    ├── logs/
    ├── quality/
    ├── raw/
    └── silver/
```

## 9. Précaution de sécurité

Ne pas exécuter `hdfs namenode -format` pour diagnostiquer un problème ou simplement démarrer Hadoop. Le formatage initialise les métadonnées du NameNode et peut rendre inaccessible un espace HDFS existant. Il ne doit être envisagé que lors d'une toute première initialisation, après confirmation de l'enseignant et vérification qu'aucune donnée à conserver n'existe.

## 10. Conclusion

Les vérifications confirment que Hadoop 3.5.0 et HDFS sont accessibles sur Ubuntu 24.04.5 LTS avec Java 21.0.13.0.3. Le NameNode, le DataNode et le SecondaryNameNode sont actifs. Le rapport HDFS indique un DataNode vivant, environ 947,34 Go disponibles et aucun bloc manquant ou corrompu.

Le déploiement est mono-nœud, car le seul DataNode annoncé est local (`localhost`). Le répertoire `/retail-lake` et ses six sous-répertoires sont déjà créés.
