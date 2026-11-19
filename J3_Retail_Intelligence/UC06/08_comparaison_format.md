# Étape 8 : Utilisation du format Apache Parquet

### 1. Objectif

L'objectif de cette étape est de comprendre l'intérêt d'un format de stockage orienté colonnes pour les traitements de données et les usages analytiques.

Dans le cadre du projet Retail Intelligence Platform, Apache Parquet est utilisé pour enregistrer les données transformées avec Apache Spark. Il permet de conserver les résultats des différentes étapes du pipeline dans un format adapté aux lectures analytiques.

Cette étape a été en grande partie intégrée aux traitements précédents : les données Silver, les jeux de données Silver transformés et le jeu analytique Gold ont déjà été enregistrés au format Parquet, puis relus pour vérifier leur exploitabilité.

### 2. Mise en œuvre et vérifications

Le format Parquet a été utilisé à plusieurs niveaux du pipeline :

- **Silver :** stockage des données nettoyées et contrôlées
- **Silver transformé :** stockage des données enrichies et des agrégations analytiques
- **Gold :** stockage du jeu de données final `sales_performance_by_store`

Le jeu Gold retenu pour illustrer cette étape est enregistré dans le répertoire :

`data/gold/sales_performance_by_store/`

Il contient 12 lignes, correspondant aux 12 magasins, avec 14 colonnes comprenant les mesures commerciales, les indicateurs de classement et les métadonnées du jeu de données.

Les données ont été enregistrées au format Parquet avec compression Snappy. Le répertoire produit a ensuite été relu avec Spark.

Les contrôles réalisés ont permis de vérifier :

- le bon fonctionnement de la lecture Parquet
- la conservation des colonnes et de leurs types
- la cohérence du nombre de lignes : 12 lignes avant écriture et 12 lignes après relecture
- l'égalité des données avant et après écriture, vérifiée par comparaison des lignes
- la réconciliation des six mesures commerciales entre la source Silver transformée et le résultat Gold

La réconciliation des mesures a notamment confirmé les égalités suivantes :

| Mesure | Valeur réconciliée |
|---|---:|
| Chiffre d'affaires TTC | 1 202 218 083,00 |
| Montant net payé | 1 150 529 586,37 |
| Profit net | -552 553 374,82 |
| Quantité vendue | 33 755 474 |
| Nombre de lignes de vente | 667 579 |
| Nombre de tickets | 89 100 |

Les contrôles ont confirmé que les résultats étaient cohérents avant et après leur enregistrement en Parquet.

### 3. Comparaison des formats de stockage

Les formats considérés dans le projet sont DAT, CSV, JSON et Parquet. Les fichiers DAT, CSV et JSON sont des formats textuels ou semi-structurés, tandis que Parquet est un format binaire organisé en colonnes.

Il convient de distinguer les formats effectivement manipulés des formats uniquement étudiés : les données sources ont été fournies principalement sous forme de fichiers DAT séparés par le caractère `|`. Le CSV a été utilisé ou étudié lors de la phase initiale Bronze. Le JSON n'a pas été utilisé dans les traitements réalisés. Parquet a été utilisé pour les données Silver, Silver transformées et Gold.

#### Comparaison générale

| Critère | CSV | JSON | Parquet |
|---|---|---|---|
| Organisation | Texte tabulaire, une ligne par enregistrement et valeurs séparées par un délimiteur | Texte structuré sous forme d'objets, tableaux et propriétés | Format binaire orienté colonnes |
| Lisibilité | Facile à lire dans un éditeur de texte | Lisible et adapté aux structures imbriquées | Peu lisible directement sans outil adapté |
| Gestion des types | Types généralement interprétés à la lecture ; les valeurs sont représentées sous forme textuelle | Types élémentaires représentés dans la structure JSON, avec interprétation par le lecteur | Types stockés dans le schéma du fichier |
| Stockage | Dépend du contenu et de la représentation textuelle | Peut être verbeux, notamment avec des objets contenant de nombreuses propriétés | Adapté au stockage analytique ; compression et encodage des colonnes possibles |
| Usages adaptés | Échanges simples, import/export tabulaire, interopérabilité | Échanges entre applications et données semi-structurées | Entrepôts de données, traitements distribués et analyses avec Spark |
| Avantages | Simple, universel et facilement inspectable | Flexible, lisible et adapté aux structures complexes | Lecture sélective de colonnes, schéma typé et compression |
| Limites | Typage limité, absence de structure complexe native, répétition des valeurs | Structure potentiellement volumineuse et lecture nécessitant l'interprétation du document | Format binaire nécessitant un moteur ou un outil compatible |

#### Cas du format DAT

Les fichiers sources TPCx-BB manipulés dans le projet utilisent principalement le format DAT, avec des champs séparés par le caractère `|` et sans ligne d'en-tête.

Ce format a été traité lors de la phase Bronze. Il nécessite de définir explicitement le schéma et le séparateur lors de la lecture. Il est donc proche d'un fichier texte délimité, mais son extension et sa convention de séparation ne correspondent pas nécessairement à celles d'un fichier CSV classique.

#### Cas du format JSON

Le JSON n'a pas été utilisé dans le pipeline réalisé. Il est néanmoins intéressant de le considérer comme un format d'échange pour des données structurées ou semi-structurées.

Sa souplesse permet notamment de représenter des objets imbriqués et des tableaux. En revanche, il ne présente pas la même organisation orientée colonnes que Parquet.

Les différences de taille, de temps de lecture et de performances entre JSON et Parquet n'ont pas été mesurées dans ce TP.

#### Volume de stockage observé et comparaison expérimentale

Les données Silver, Silver transformées et Gold ont été enregistrées en Parquet, avec compression Snappy pour le jeu Gold. En revanche, aucune expérience comparative contrôlée n'a été menée pour enregistrer exactement le même jeu de données en CSV, JSON et Parquet.

Il n'est donc pas possible de conclure, à partir des seuls résultats du projet, à un taux de réduction précis du stockage ou à un gain chiffré de performances.

Une perspective d'amélioration consisterait à sélectionner un même échantillon de données, à l'enregistrer dans les trois formats avec des paramètres comparables, puis à mesurer :

- la taille totale des fichiers produits
- le temps d'écriture 
- le temps de lecture 
- le temps nécessaire pour sélectionner quelques colonnes 
- la conservation des types et des valeurs

Cette expérimentation permettrait de valider quantitativement les avantages attendus de Parquet dans le contexte du projet.

### 4. Intérêt de Parquet pour le projet

L'utilisation de Parquet est cohérente avec l'architecture mise en place.

Les étapes Silver, Silver transformée et Gold produisent des jeux de données destinés à être relus, agrégés et exploités par des traitements analytiques. Le stockage en colonnes est particulièrement adapté à ce type d'utilisation, car un traitement peut ne lire que les colonnes nécessaires à son calcul.

Parquet conserve également un schéma typé, ce qui facilite la manipulation des données avec Spark et évite de devoir réinterpréter systématiquement toutes les valeurs.

Ces avantages sont cohérents avec les besoins du projet. Toutefois, les gains réels de temps de lecture et de stockage n'ont pas été mesurés expérimentalement dans ce TP.

### 5. Limite : Parquet et les garanties transactionnelles

Parquet est un format de fichiers colonne. Il ne constitue pas, à lui seul, un format de table transactionnel garantissant les propriétés ACID.

Dans le projet, les répertoires Parquet représentent des jeux de données enregistrés et relus par Spark. Ils ne doivent donc pas être présentés comme des tables transactionnelles Lakehouse.

Des technologies complémentaires, telles que Delta Lake, Apache Iceberg ou Apache Hudi, peuvent ajouter une couche de gestion de tables et des mécanismes transactionnels au-dessus des fichiers de données.

Ces technologies ne font cependant pas partie de la mise en œuvre réalisée dans cette étape.

### 6. Conclusion

Plusieurs jeux de données Silver, Silver transformés et Gold ont été enregistrés au format Parquet puis relus avec Spark.

Le jeu Gold `sales_performance_by_store` constitue un exemple vérifié : les 12 lignes ont été retrouvées après relecture, le schéma a été conservé et les mesures commerciales ont été réconciliées avec les données sources.

La comparaison théorique des formats permet de justifier le choix de Parquet pour les traitements analytiques. En revanche, aucune comparaison expérimentale des tailles de fichiers ou des temps de traitement entre CSV, JSON et Parquet n'a été effectuée. Ces mesures constituent une perspective d'amélioration et devront être validées par une expérimentation dédiée.