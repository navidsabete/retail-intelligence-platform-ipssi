# Étape 2 : Conception de l'organisation ADLS Gen2

## 1. Objectif

Cette deuxième étape du UC-07 consiste à proposer une organisation logique des données du projet Retail Intelligence dans Azure Data Lake Storage Gen2 (ADLS Gen2).

L'objectif est de définir une structure cohérente avec les principes de l'architecture Data Lake, en distinguant les zones Bronze, Silver et Gold selon le niveau de transformation et la finalité des données.

L'organisation doit également permettre de faciliter :
- la compréhension des données
- leur exploitation par les traitements analytiques
- la gestion des accès
- la traçabilité des transformations
- la conservation des données
- l'évolution future de la plateforme

Le parcours B (Local / Open Source) ayant été retenu, cette organisation constitue une proposition d'architecture cible. Aucun conteneur ni répertoire ADLS Gen2 n'a été effectivement créé.

## 2. Principes d'organisation retenus

La conception s'appuie sur l'organisation existante du projet Retail Intelligence et sur les datasets identifiés pendant les précédentes unités de compétence.

Les principes retenus sont les suivants :

**Séparation des niveaux de transformation**

Les données sont organisées selon trois zones principales :
- Bronze : données sources conservées dans leur état initial
- Silver : données nettoyées, structurées et transformées
- Gold : données agrégées et préparées pour les usages analytiques et métier

**Organisation par domaine fonctionnel**

Les données Silver sont regroupées selon leur domaine :
- ventes ;
- inventaire ;
- ventes et stocks.

Cette organisation permet de distinguer les différentes catégories de données et leurs granularités.

**Séparation des données et de la documentation**

Les contrôles qualité et les documents techniques sont placés dans des répertoires spécifiques afin de ne pas mélanger les données analytiques avec les éléments de suivi et de documentation.

**Traçabilité**

Chaque jeu de données doit pouvoir être associé à sa source, à son niveau de transformation et aux traitements ayant permis sa production.

## 3. Organisation logique proposée

Le conteneur ADLS Gen2 proposé est nommé `retail-intelligence`.

Les différentes zones sont organisées directement à sa racine.

```text
retail-intelligence/
|
+-- bronze/
|   |
|   +-- tpcxbb/
|
+-- silver/
|   |
|   +-- ventes/
|   |   |
|   |   +-- store_sales/
|   |   +-- sales_by_store/
|   |   +-- sales_by_store_date/
|   |   +-- sales_by_item_date/
|   |
|   +-- inventory/
|   |   |
|   |   +-- inventory/
|   |   +-- inventory_by_item_date/
|   |
|   +-- ventes_stocks/
|       |
|       +-- sales_inventory_by_item_date/
|
+-- gold/
|   |
|   +-- indicateurs/
|   |   |
|   |   +-- sales_performance_by_store/
|   |
|   +-- analyses/
|
+-- quality/
|
+-- documentation/
```

Cette organisation reprend les datasets déjà identifiés dans le projet, tout en proposant une structuration plus explicite par domaine fonctionnel.

Elle ne constitue pas une reproduction exacte de l'arborescence locale existante. Elle représente une organisation cible adaptée à ADLS Gen2.

## 4. Description des différentes zones

### 4.1. Zone Bronze

#### Fonction

La zone Bronze constitue le premier niveau de stockage du Data Lake.

Elle accueille les données provenant des sources initiales avant leur transformation dans les couches suivantes.

Son objectif est de préserver les données sources et de fournir une référence pour les traitements ultérieurs.

#### Données pouvant être déposées

Dans Retail Intelligence, cette zone est destinée à accueillir les données sources synthétiques issues de TPCx-BB.

Le répertoire proposé est :

`bronze/tpcxbb/`

Il pourra contenir les fichiers sources utilisés par les traitements du projet.

Les noms et les formats des fichiers seront conservés autant que possible afin de faciliter leur identification et leur rapprochement avec les sources d'origine.

Aucun nouveau fichier source n'est supposé ou ajouté dans le cadre de cette proposition.

#### Utilisateurs et traitements concernés

Les principaux intervenants sont :
- l'équipe d'ingestion des données
- l'équipe Data Engineering
- les traitements chargés de préparer les données Silver

L'équipe d'ingestion dispose de droits d'écriture contrôlés.

Les traitements de transformation disposent des droits de lecture nécessaires pour exploiter les données sources.

Les analystes métier n'ont pas vocation à accéder directement à cette zone.

#### Règles de nommage

Les règles proposées sont :
- utiliser des noms en minuscules
- utiliser le caractère `_` pour séparer les mots
- conserver les noms d'origine des datasets lorsque cela est pertinent
- éviter les espaces et les caractères spéciaux 
- identifier clairement la source des données

Exemple :

`bronze/tpcxbb/`

#### Conservation et traçabilité

Les données Bronze doivent être conservées comme référence des sources utilisées.

Les principes suivants sont proposés :
- éviter toute modification directe des données sources après ingestion 
- conserver l'identification de la source 
- enregistrer la date et l'heure d'ingestion 
- identifier le traitement ou le processus d'ingestion 
- documenter les éventuelles nouvelles versions des données

La durée de conservation devra être définie selon les besoins du projet, les contraintes de stockage et les règles de gouvernance retenues.

Aucune durée chiffrée n'est imposée à ce stade.

### 4.2. Zone Silver

#### Fonction

La zone Silver accueille les données préparées et transformées à partir des données sources.

Elle constitue une couche intermédiaire entre les données initiales et les données destinées aux analyses métier.

Les traitements peuvent notamment comprendre :
- le nettoyage des données
- la gestion des valeurs manquantes
- les contrôles de qualité
- la standardisation des structures
- les jointures entre différentes sources
- les agrégations adaptées aux besoins analytiques

Les données doivent conserver une granularité clairement définie et documentée.

#### Données disponibles dans Retail Intelligence

L'organisation proposée distingue trois domaines.

**Domaine ventes**

Répertoire :

`silver/ventes/`

Datasets identifiés :
- `store_sales` ;
- `sales_by_store` ;
- `sales_by_store_date` ;
- `sales_by_item_date`.

Le dataset `sales_by_store_date` présente notamment une granularité magasin/date.

Il contient les principaux indicateurs de performance commerciale, notamment le chiffre d'affaires TTC, le montant net payé, le profit net, les quantités vendues, le nombre de lignes de vente et le nombre de tickets.

**Domaine inventaire**

Répertoire :

`silver/inventory/`

Datasets identifiés :
- `inventory` ;
- `inventory_by_item_date`.

Ces données permettent de représenter les informations relatives aux stocks et à leur évolution selon la granularité disponible.

**Domaine ventes et stocks**

Répertoire :

`silver/ventes_stocks/`

Dataset identifié :
- `sales_inventory_by_item_date`.

Ce jeu de données rapproche les informations de ventes et d'inventaire.

Son exploitation doit tenir compte des limites de couverture du rapprochement identifiées pendant le UC-08.

En particulier, les valeurs NULL associées à `total_quantity_on_hand` ne doivent pas être interprétées automatiquement comme des stocks nuls.

#### Utilisateurs et traitements concernés

Les principaux intervenants sont :
- l'équipe Data Engineering
- les traitements PySpark ou Spark
- les processus de contrôle qualité
- les traitements préparant les données Gold

L'équipe Data Engineering dispose de droits de lecture et d'écriture selon les besoins des traitements.

Les analystes métier peuvent obtenir un accès en lecture à certains jeux Silver lorsque cela est justifié.

#### Règles de nommage

Les conventions proposées sont :
- noms de répertoires en minuscules
- utilisation de `snake_case`
- noms explicites correspondant au domaine métier
- conservation des noms de datasets déjà utilisés
- distinction entre les données détaillées et les données agrégées

Exemples :

`silver/ventes/sales_by_store_date/`

`silver/inventory/inventory_by_item_date/`

`silver/ventes_stocks/sales_inventory_by_item_date/`

Les noms des datasets ne doivent pas masquer leur granularité.

#### Conservation et traçabilité

La zone Silver doit permettre de retrouver l'origine des données et les transformations appliquées.

Les informations de traçabilité recommandées sont :
- la référence au dataset source
- la date et l'heure du traitement 
- la version du traitement 
- la définition du schéma 
- la granularité du dataset 
- les résultats des contrôles qualité 
- le nombre de lignes produites

Les transformations doivent être reproductibles autant que possible.

Les anciennes versions ne doivent pas être supprimées sans vérification de leurs dépendances et des règles de conservation.

### 4.3. Zone Gold

#### Fonction

La zone Gold constitue la couche destinée à l'exploitation analytique et métier.

Elle contient des données consolidées, agrégées et préparées pour répondre à des besoins de pilotage.

Les jeux Gold doivent présenter :
- une structure stable 
- des indicateurs définis 
- une granularité documentée 
- des contrôles de cohérence 
- une signification métier clairement établie

#### Données disponibles dans Retail Intelligence

Le dataset Gold actuellement identifié est :

`gold/sales_performance_by_store/`

Il contient :
- 12 lignes 
- une ligne par magasin 
- 14 colonnes 
- un classement des magasins par chiffre d'affaires 
- la part de chaque magasin dans le chiffre d'affaires global

Les contrôles de réconciliation réalisés pendant le UC-08 ont confirmé la cohérence des principaux indicateurs avec les données Silver utilisées.

Le répertoire suivant est également proposé :

`gold/analyses/`

Il pourra accueillir ultérieurement des résultats analytiques validés et destinés à être réutilisés dans des rapports ou des tableaux de bord.

Il s'agit d'un emplacement réservé à de futurs usages, et non de l'affirmation que des datasets supplémentaires y existent déjà.

#### Utilisateurs et traitements concernés

Les principaux utilisateurs sont :
- les analystes métier
- les responsables de pilotage
- les outils de visualisation
- les traitements produisant les indicateurs consolidés

L'accès est principalement prévu en lecture pour les utilisateurs métier.

L'écriture est réservée aux traitements autorisés et aux responsables de la production des données Gold.

#### Règles de nommage

Les conventions proposées sont :
- utiliser des noms explicites
- privilégier les termes métier
- conserver la granularité dans la documentation
- identifier clairement la nature des indicateurs

Exemple :

`gold/indicateurs/sales_performance_by_store/`

#### Conservation et traçabilité

Les données Gold doivent être conservées en fonction de leur utilité analytique et des dépendances avec les rapports et analyses.

Les informations de traçabilité recommandées comprennent :
- les datasets Silver utilisés en entrée
- les règles de calcul des indicateurs
- la date de production 
- la version des traitements 
- les contrôles de réconciliation 
- la définition métier des indicateurs

Une modification des règles de calcul doit être documentée afin de garantir la comparabilité des résultats dans le temps.

### 4.4. Zone Quality

#### Fonction

La zone Quality est destinée à regrouper les éléments produits par les contrôles de qualité des données.

Elle permet de séparer les résultats de validation des jeux de données eux-mêmes.

#### Données pouvant être déposées

Cette zone pourrait accueillir :
- les rapports de contrôles qualité
- les résultats des contrôles de doublons
- les rapports de détection des valeurs NULL
- les contrôles de cohérence des clés
- les résultats des réconciliations entre Silver et Gold
- les synthèses des anomalies détectées

Les contrôles réalisés pendant le UC-08 constituent des exemples de contenus qui pourraient être documentés dans cette zone.

Il ne s'agit pas d'affirmer que ces rapports y sont actuellement stockés.

#### Utilisateurs et traitements concernés

Les principaux intervenants sont :
- l'équipe Data Engineering
- les responsables de la qualité des données
- les traitements automatisés de validation

Les analystes peuvent consulter les résultats de qualité lorsque cela est nécessaire à l'interprétation des indicateurs.

#### Règles de nommage

Les noms doivent permettre d'identifier :
- le dataset contrôlé
- le type de contrôle
- la date d'exécution
- éventuellement la version du traitement

Exemple de convention :

`quality/nom_dataset/type_controle/`

#### Conservation et traçabilité

Les rapports doivent être associés au dataset et à la version contrôlée.

Les anomalies identifiées, les corrections effectuées et les éventuelles limites doivent rester documentées.

Les durées de conservation seront définies selon les besoins de suivi et d'audit du projet.

### 4.5. Zone Documentation

#### Fonction

La zone Documentation est destinée à conserver les informations techniques et fonctionnelles nécessaires à la compréhension et à la maintenance de la plateforme.

Elle constitue un espace de référence pour les utilisateurs et les équipes techniques.

#### Données pouvant être déposées

Cette zone pourrait accueillir :
- les dictionnaires de données
- les descriptions des schémas
- les documentations des traitements
- les conventions de nommage
- les descriptions des architectures
- les procédures d'exploitation
- les règles métier
- les documents de traçabilité

Les documents produits pendant les différentes unités de compétence pourraient y être référencés.

#### Utilisateurs et traitements concernés

Les principaux utilisateurs sont :
- l'équipe Data Engineering
- les administrateurs de la plateforme
- les analystes métier
- les responsables de projet

Les droits d'écriture doivent être limités aux personnes chargées de maintenir la documentation.

#### Règles de nommage

Les noms doivent être explicites et cohérents.

Exemples de conventions :
- `architecture_data_lake.md`
- `dictionnaire_donnees.md`
- `conventions_nommage.md`
- `documentation_traitements.md`

#### Conservation et traçabilité

La documentation doit être versionnée afin de conserver l'historique des évolutions.

Chaque document important doit préciser :
- son objectif
- sa date de mise à jour
- sa version
- son périmètre
- les éléments techniques auxquels il se rapporte

Les versions précédentes doivent pouvoir être retrouvées lorsque cela est nécessaire.

## 5. Conventions générales de nommage

Pour garantir la cohérence de l'organisation, les conventions suivantes sont proposées.

| Élément | Convention |
|---|---|
| Répertoires | Minuscules |
| Séparation des mots | `snake_case` |
| Espaces | À éviter |
| Caractères spéciaux | À éviter |
| Noms de datasets | Explicites et fonctionnels |
| Noms de fichiers | Descriptifs |
| Formats de données | Identifiés dans la documentation |
| Granularité | Documentée pour chaque dataset |

Le format Parquet avec compression Snappy est conservé comme référence pour les datasets analytiques, puisqu'il est déjà utilisé dans le projet.

Il ne faut toutefois pas supposer que tous les fichiers de toutes les zones doivent obligatoirement être au format Parquet.

Le format doit être adapté à la nature des données et à leur utilisation.

Pour les données organisées en répertoires de datasets Parquet, les noms des fichiers générés par les moteurs de traitement peuvent être conservés, à condition que le jeu de données soit correctement identifié à son niveau de répertoire.

## 6. Règles de conservation et de traçabilité

La conservation des données doit tenir compte de leur niveau de transformation et de leur importance dans les traitements.

Les principes proposés sont les suivants :

| Zone | Conservation | Traçabilité |
|---|---|---|
| Bronze | Préservation des données sources et conservation selon la politique retenue | Source, date d'ingestion, version |
| Silver | Conservation des données transformées utiles aux traitements | Sources, schéma, traitement, granularité |
| Gold | Conservation des indicateurs nécessaires aux usages analytiques | Règles métier, version, contrôles |
| Quality | Conservation des résultats de validation selon les besoins de suivi | Dataset contrôlé, anomalies, date |
| Documentation | Conservation et versionnement des documents de référence | Auteur ou responsable, version, date |

La traçabilité doit permettre de comprendre le cheminement d'une donnée depuis sa source jusqu'à son exploitation analytique.

Pour cela, les traitements devraient enregistrer des informations telles que :
- l'identifiant du traitement
- la date et l'heure d'exécution
- les sources utilisées
- les datasets produits
- les versions des scripts
- le nombre de lignes en entrée et en sortie
- les résultats des contrôles qualité

Les durées exactes de conservation ne sont pas définies dans le cadre de cette proposition. Elles devront faire l'objet d'une politique spécifique tenant compte des besoins métier, des coûts et des contraintes applicables.

## 7. Adaptation à l'architecture locale existante

L'organisation proposée s'appuie sur les datasets identifiés dans le projet Retail Intelligence.

Elle reprend notamment :
- les données détaillées de ventes `store_sales`
- les données d'inventaire `inventory`
- les agrégations commerciales par magasin et par date
- les agrégations par produit et par date
- le rapprochement entre ventes et inventaire
- le jeu Gold `sales_performance_by_store`

Cette organisation permet de conserver les responsabilités fonctionnelles des différents jeux de données tout en proposant une structure adaptée à ADLS Gen2.

Il est important de noter que l'arborescence cible n'impose pas une modification de l'organisation locale existante.

Les données du TP3 restent inchangées et sont uniquement utilisées comme référence pour concevoir l'architecture cible.

## 8. Statut de réalisation

Dans le cadre du parcours B, l'organisation ADLS Gen2 est uniquement conçue et documentée.

| Élément | Statut |
|---|---|
| Conteneur `retail-intelligence` | Proposé, non créé |
| Zone Bronze | Organisation proposée |
| Zone Silver | Organisation proposée |
| Zone Gold | Organisation proposée |
| Zone Quality | Organisation proposée |
| Zone Documentation | Organisation proposée |
| Dépôt de fichiers dans ADLS Gen2 | Non réalisé |
| Gestion des permissions ADLS Gen2 | À étudier dans l'étape consacrée à la sécurité |

Les datasets mentionnés proviennent de l'inventaire réalisé précédemment. Leur présence dans l'organisation cible ne signifie pas qu'ils ont été transférés dans Azure.

## 9. Conclusion

Cette deuxième étape a permis de concevoir une organisation logique du Data Lake adaptée au projet Retail Intelligence.

La séparation entre Bronze, Silver et Gold permet de distinguer les données sources, les données transformées et les données destinées aux usages analytiques.

L'ajout des zones Quality et Documentation complète cette organisation en facilitant le suivi de la qualité des données et la gestion des connaissances techniques.

La structure proposée s'appuie sur les jeux de données réellement identifiés pendant le UC-08, notamment les datasets de ventes, d'inventaire et de performance commerciale par magasin.

Cette organisation constitue une proposition cohérente pour une future transposition vers Azure Data Lake Storage Gen2, tout en préservant l'architecture locale existante et les principes de séparation des environnements du projet.