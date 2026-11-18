# Retail Intelligence Platform — Hadoop, HDFS, Data Lake et NiFi
## Questions de recul

Les réponses ci-dessous s'appuient sur les observations du TP et sur le fonctionnement des composants étudiés.

### 1. Quel est le rôle du NameNode dans HDFS ?

Le NameNode est le composant maître de HDFS. Il gère l'espace de noms du système de fichiers : arborescence des répertoires, noms des fichiers, permissions et métadonnées. Il mémorise notamment la correspondance entre les fichiers et les blocs qui les composent, ainsi que les emplacements des répliques sur les DataNodes.

Lorsqu'un client souhaite lire ou écrire un fichier, il contacte le NameNode pour obtenir les informations nécessaires.

Dans l'environnement du TP, le processus NameNode a été observé actif avec `jps`.

### 2. Quelle différence existe entre un NameNode et un DataNode ?

Le NameNode gère les métadonnées et l'organisation logique de HDFS. Le DataNode stocke physiquement les blocs de données sur son disque local et répond aux demandes de lecture et d'écriture des clients.

En résumé :
- **NameNode :** sait quels fichiers existent, quels blocs les composent et où ils sont stockés.
- **DataNode :** conserve les blocs et les met à disposition.

Le TP a identifié un NameNode et un seul DataNode local, annoncé à `127.0.0.1:9866` (`localhost`).

### 3. Pourquoi HDFS découpe-t-il les fichiers en blocs ?

Le découpage en blocs permet à HDFS de stocker de grands fichiers de manière distribuée sur plusieurs DataNodes. Les blocs peuvent être répartis sur différentes machines et répliqués indépendamment.

Cette organisation facilite :
- le stockage de fichiers volumineux au-delà de la capacité d'un seul disque ;
- la lecture parallèle de plusieurs blocs ;
- la répartition de la charge entre les nœuds ;
- la réplication et la récupération après la perte d'un nœud, si le cluster dispose de plusieurs nœuds.

Dans le TP, les fichiers `customer.dat` et `store_sales.dat` sont déposés dans HDFS. Le rapport HDFS permet notamment de consulter le nombre de blocs et l'état des répliques.

### 4. Quel est l'intérêt de la réplication ?

La réplication consiste à conserver plusieurs copies d'un bloc sur des DataNodes différents. Si un DataNode devient indisponible, une autre réplique peut permettre de continuer à lire les données. La réplication contribue donc à la tolérance aux pannes et à la disponibilité des données.

Elle peut également améliorer les possibilités de lecture parallèle. En contrepartie, elle consomme davantage d'espace de stockage.

La réplication n'apporte une véritable protection contre la panne d'une machine que si les répliques sont réparties sur plusieurs machines ou domaines de panne. Dans l'environnement du TP, un seul DataNode est observé : la configuration ne permet donc pas de démontrer une résilience physique entre plusieurs nœuds. Le facteur de réplication configuré n'a pas été relevé.

### 5. Pourquoi organiser un Data Lake en plusieurs zones ?

Les zones séparent les étapes du cycle de vie de la donnée et clarifient les responsabilités. Elles évitent de mélanger les fichiers d'origine, les données intégrées, les données nettoyées, les produits analytiques et les traces techniques.

L'organisation retenue pour Retail Intelligence est la suivante :

- **Raw :** copie de référence des données sources.
- **Bronze :** données prises en charge par l'ingestion, proches de la source et tracées.
- **Silver :** données nettoyées, contrôlées et harmonisées.
- **Gold :** données préparées pour les analyses et les usages métier.
- **Quality :** rapports de contrôle, anomalies et rejets.
- **Logs :** journaux des exécutions et incidents.
- **Workspace :** espace de travail technique temporaire, hors zones métier.

Cette organisation facilite la maintenance, les contrôles, la réutilisation des données et l'identification de l'étape où un problème est apparu.

### 6. Pourquoi conserver les données sources dans Raw ?

Cette conservation permet de revenir à la source, de rejouer une ingestion ou un traitement, de comparer les lots `initial` et `refresh` et de réaliser des audits. Elle évite également qu'une transformation ou une erreur de traitement ne fasse perdre l'information d'origine. Les résultats transformés doivent être écrits dans les zones suivantes plutôt que d'écraser la copie Raw.

Dans le TP, `customer.dat` et `store_sales.dat` du lot initial ont été copiés dans `/retail-lake/raw/tpcxbb/initial/`. Les sources locales ont été conservées.

### 7. Quel est le rôle d'un FlowFile dans NiFi ?

Le FlowFile est l'unité de données que NiFi transporte entre ses composants. Il comprend :
- un **contenu** (*Content*), par exemple les octets d'un fichier ;
- des **attributs** (*Attributes*), qui sont des métadonnées associées, par exemple le nom du fichier, sa taille, son chemin d'origine ou sa date.

Les processeurs manipulent les FlowFiles et peuvent créer, modifier, router ou envoyer leur contenu. Les attributs facilitent le routage, le suivi et la traçabilité.

Dans le TP, le fichier `customer.dat` pris en charge par `GetFile` est représenté par un FlowFile, ensuite envoyé vers `PutHDFS`.

### 8. Quelle différence existe entre un Processor et une Connection ?

Un **Processor** exécute une opération : lire un fichier, filtrer des données, transformer un contenu ou écrire vers une destination. Une **Connection** relie des composants et transporte les FlowFiles d'un composant vers le suivant. Elle comporte une file d'attente qui participe à la gestion du flux et de la pression exercée entre processeurs.

Dans le flux du TP :
- `GetFile` est le Processor qui lit le répertoire local `/data/nifi/input` ;
- `PutHDFS` est le Processor qui écrit vers HDFS ;
- la Connection associée à la relation `success` transporte le FlowFile de `GetFile` vers `PutHDFS`.

### 9. Pourquoi la provenance est-elle importante ?

La provenance permet de reconstituer le parcours d'un FlowFile dans NiFi : événements, composants traversés, dates, tailles et opérations effectuées. Elle facilite le diagnostic, l'audit, le suivi des traitements et la recherche de l'origine d'un incident.

Dans le TP, un même UUID a été associé à un événement `RECEIVE` sur `GetFile` à 11:26:42.501 CET et à un événement `SEND` sur `PutHDFS` à 11:26:43.123 CET, le 18 novembre 2026. La taille indiquée était de 12,66 MB pour les deux événements. L'identifiant commun relie les deux étapes du parcours.

### 10. Comment distinguer un échec technique d'un rejet métier ?

Un **échec technique** empêche le traitement de fonctionner correctement. Exemples : répertoire source inexistant, droits de lecture insuffisants, HDFS indisponible, erreur réseau ou processeur mal configuré.

Un **rejet métier ou qualité** concerne une donnée qui a pu être lue techniquement, mais qui ne respecte pas une règle attendue. Exemples : date impossible, identifiant obligatoire absent, valeur hors domaine ou incohérence entre champs.

La distinction est importante pour orienter la correction :
- un échec technique demande une action sur l'environnement, les accès ou la configuration ;
- un rejet métier demande une analyse de la donnée et de la règle de validation, puis une conservation du rejet et de son motif dans les espaces Quality prévus.

Le test contrôlé du TP est un échec technique : `GetFile` pointait vers un répertoire inexistant. La correction a été de rétablir `/data/nifi/input`.

### 11. Quels risques apparaissent si un flux est relancé sans contrôle des doublons ?

Une relance non contrôlée peut déposer plusieurs fois le même fichier ou réingérer les mêmes enregistrements. Cela peut entraîner :
- un double comptage des ventes
- des indicateurs commerciaux et financiers incorrects
- une augmentation inutile du stockage
- des résultats incohérents entre lots
- des traitements répétés et des coûts supplémentaires
- une difficulté à distinguer une nouvelle livraison d'une simple relance.

La stratégie `fail` configurée dans `PutHDFS` évite de remplacer silencieusement un fichier existant, mais elle ne remplace pas un contrôle métier des doublons.

### 12. Quelles limites présente un environnement mono-nœud ?

Un environnement mono-nœud place les services et le stockage sur une seule machine. Il est pratique pour apprendre, développer et tester les commandes, mais il ne représente pas les propriétés d'un cluster distribué de production.

Ses principales limites sont :
- absence de répartition réelle des données sur plusieurs machines ;
- absence de tolérance à la panne d'un serveur de stockage ;
- impossibilité de démontrer une réplication entre hôtes indépendants ;
- ressources CPU, mémoire, disque et réseau concentrées sur une seule machine ;
- capacité limitée à tester la montée en charge et la concurrence ;
- risque qu'une panne de la machine rende l'ensemble du service indisponible.

Le TP constate un seul DataNode sur `localhost`. Il faut donc présenter l'environnement comme une plateforme pédagogique locale, et non comme un cluster hautement disponible.

### 13. Pourquoi une copie locale ne constitue-t-elle pas une preuve de dépôt HDFS ?

Une copie locale prouve seulement que le fichier existe sur le système de fichiers Linux. Elle ne démontre pas qu'il a été transféré dans HDFS, que le chemin de destination est correct, ni que le contenu distant est lisible et complet.

Pour prouver le dépôt HDFS, il faut vérifier directement le système cible, par exemple avec :
- `hdfs dfs -ls` pour constater la présence du fichier ;
- `hdfs dfs -du -h` pour consulter sa taille ;
- `hdfs dfs -cat` pour vérifier qu'il est lisible ;
- une comparaison SHA-256 entre le fichier local et le contenu relu depuis HDFS pour contrôler l'identité du contenu.

Dans le TP, ces contrôles ont été documentés pour `customer.dat` et `store_sales.dat` et `/retail-lake/raw/nifi` dans Raw.

### 14. Quelles informations doivent être conservées pour reproduire une ingestion ?

Il faut conserver suffisamment d'informations pour identifier précisément la source, reconstituer la configuration et vérifier le résultat.

1. **Source :** nom du fichier, chemin, système ou jeu de données d'origine, version et lot (`initial` ou `refresh`).
2. **Caractéristiques :** format, encodage, séparateur, présence ou absence d'en-tête, taille, nombre de lignes et schéma attendu.
3. **Intégrité :** empreinte SHA-256 calculée avant et après transfert.
4. **Horodatage :** dates et heures de début et de fin, avec fuseau horaire.
5. **Identification :** identifiant de lot, identifiant d'exécution et UUID du FlowFile si NiFi est utilisé.
6. **Configuration :** versions des composants, paramètres non sensibles des processeurs, chemins source et destination, stratégie de conflit et ressources de configuration.
7. **Résultat :** destination HDFS, nombre et taille des fichiers écrits, volumes lus et rejetés, statut final.
8. **Qualité et incidents :** contrôles exécutés, résultats, anomalies, motifs de rejet et journaux utiles.
9. **Reproductibilité :** version des scripts ou traitements et description des transformations appliquées.