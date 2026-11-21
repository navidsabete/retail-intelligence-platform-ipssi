# Étape 3 : Rôle du Hierarchical Namespace (HNS) dans ADLS Gen2

## 1. Objectif

Cette troisième étape du UC-07 consiste à expliquer le fonctionnement et les avantages du Hierarchical Namespace (HNS) dans Azure Data Lake Storage Gen2.

Le HNS constitue une fonctionnalité importante pour les architectures Data Lake, car il permet d'organiser les données selon une structure hiérarchique composée de répertoires et de fichiers.

L'objectif est notamment de comprendre :
- l'organisation hiérarchique des données
- les opérations réalisées sur les chemins et les répertoires
- la gestion des permissions au niveau des répertoires et des fichiers
- les différences entre ADLS Gen2 avec HNS et un stockage objet classique sans espace de noms hiérarchique

Cette étude sera mise en relation avec l'organisation Bronze, Silver et Gold proposée pour le projet Retail Intelligence pendant l'étape précédente.

Le parcours B (Local / Open Source) ayant été retenu, le HNS est étudié dans une perspective de transposition vers Azure. Aucune configuration Azure n'est réalisée.

## 2. Présentation du Hierarchical Namespace

### 2.1. Définition

Le Hierarchical Namespace (HNS) est une fonctionnalité d'Azure Data Lake Storage Gen2 qui permet d'organiser les données dans une structure hiérarchique de répertoires et de fichiers.

Il apporte au stockage Azure Blob des capacités de gestion adaptées aux usages analytiques et aux traitements Big Data.

Dans une organisation classique de stockage objet, les objets sont principalement identifiés par leur nom au sein d'un conteneur. Les séparateurs utilisés dans les noms, comme `/`, peuvent donner l'apparence d'une organisation en dossiers sans nécessairement correspondre à de véritables répertoires.

Avec le HNS activé, les répertoires et les fichiers sont gérés comme des éléments d'un espace de noms hiérarchique.

Cette organisation permet notamment :
- de créer et supprimer des répertoires
- de parcourir une arborescence
- de déplacer et renommer des répertoires et des fichiers 
- de gérer des permissions à différents niveaux de l'arborescence
- de faciliter l'intégration avec les moteurs de traitement de données distribuées

Le HNS constitue ainsi une fonctionnalité particulièrement adaptée aux Data Lakes qui manipulent de nombreux fichiers répartis dans différentes zones de stockage.

### 2.2. Activation du HNS

Le HNS est une caractéristique du compte de stockage Azure.

Pour bénéficier des fonctionnalités d'ADLS Gen2, le compte de stockage doit être configuré avec l'espace de noms hiérarchique activé.

Cette activation permet de disposer des fonctionnalités spécifiques de gestion des répertoires, des chemins et des ACL.

Le HNS n'est donc pas une option qui doit être activée individuellement sur chaque répertoire ou conteneur.

Dans le cadre de Retail Intelligence, un compte de stockage configuré avec le HNS permettrait d'organiser les données selon les zones Bronze, Silver et Gold définies précédemment.

## 3. Organisation hiérarchique des répertoires

### 3.1. Principe de fonctionnement

Le HNS permet de représenter les données sous forme d'une arborescence.

Chaque répertoire peut contenir :
- des sous-répertoires
- des fichiers
- d'autres niveaux de répertoires

Cette organisation facilite la structuration logique des données et leur séparation selon différents critères :
- le domaine métier 
- le niveau de transformation 
- la source 
- le type de données 
- les besoins d'exploitation

Les chemins permettent d'identifier précisément l'emplacement d'un fichier dans cette hiérarchie.

### 3.2. Exemple appliqué à Retail Intelligence

L'organisation proposée pendant l'étape 2 peut être représentée ainsi :

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
|   |   +-- sales_by_store_date/
|   |   +-- sales_by_item_date/
|   |
|   +-- inventory/
|   |   |
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

Cette organisation permet de distinguer clairement les différents niveaux de transformation.

Par exemple, le chemin :

`silver/ventes/sales_by_store_date/`

désigne un emplacement destiné au dataset Silver `sales_by_store_date`.

Le chemin :

`gold/indicateurs/sales_performance_by_store/`

désigne l'emplacement du jeu Gold consacré aux performances commerciales par magasin.

Les chemins deviennent ainsi un élément important de l'organisation et de la compréhension du Data Lake.

Il est également possible d'attribuer des permissions différentes à certains répertoires selon les responsabilités des utilisateurs et des traitements.

## 4. Opérations sur les chemins et les répertoires

### 4.1. Création de répertoires

Avec le HNS, les répertoires peuvent être créés explicitement.

Par exemple, l'organisation de Retail Intelligence nécessite la création des répertoires :

- `bronze/`
- `silver/`
- `gold/`
- `quality/`
- `documentation/`

Des sous-répertoires peuvent ensuite être créés pour organiser les données par domaine.

Cette approche facilite la préparation de l'espace de stockage avant le dépôt des données.

### 4.2. Parcours de l'arborescence

Les répertoires peuvent être parcourus afin d'identifier les fichiers et les sous-répertoires disponibles.

Cette possibilité facilite :
- l'inventaire des données
- l'identification des datasets
- la recherche de fichiers
- l'organisation des traitements
- la vérification des emplacements de stockage

Dans Retail Intelligence, un traitement pourrait par exemple parcourir le répertoire Silver pour identifier les jeux de données disponibles avant de réaliser une analyse.

### 4.3. Renommage et déplacement

Le HNS apporte une gestion efficace des opérations de renommage et de déplacement des fichiers et des répertoires.

Dans un stockage objet classique, un déplacement peut nécessiter une opération de copie suivie d'une suppression de l'objet d'origine.

Avec le HNS, les opérations de renommage et de déplacement au sein du même système de fichiers peuvent être réalisées au niveau des métadonnées de l'espace de noms, sans devoir recopier individuellement l'ensemble des données concernées.

Cela est particulièrement intéressant lorsque les répertoires contiennent un grand nombre de fichiers.

Dans Retail Intelligence, cette fonctionnalité pourrait faciliter certaines opérations d'organisation des données entre les différentes étapes d'un traitement.

Toutefois, les déplacements entre zones doivent rester contrôlés afin de préserver la traçabilité et la cohérence des traitements.

### 4.4. Suppression de fichiers et de répertoires

Le HNS permet également de gérer la suppression des fichiers et des répertoires.

Les opérations peuvent être réalisées à différents niveaux de l'arborescence, sous réserve des autorisations nécessaires.

Une suppression de répertoire peut concerner l'ensemble de son contenu.

Dans une architecture Data Lake, ces opérations doivent être encadrées par des règles de sécurité et de conservation.

Pour Retail Intelligence, les données sources Bronze doivent notamment être protégées contre les suppressions accidentelles.

### 4.5. Intérêt pour les traitements distribués

Les moteurs de traitement distribués, comme Apache Spark, manipulent fréquemment des volumes importants de fichiers.

Dans ce contexte, les opérations sur les chemins et les répertoires peuvent représenter une part significative des interactions avec le stockage.

Le HNS améliore la gestion de ces opérations et facilite l'utilisation d'ADLS Gen2 par les outils compatibles avec les environnements analytiques.

Il constitue donc un avantage pour les architectures combinant un Data Lake et des moteurs de traitement distribués.

## 5. Gestion des permissions au niveau des répertoires et des fichiers

### 5.1. Principe général

Le HNS permet de gérer des permissions directement au niveau des répertoires et des fichiers grâce aux Access Control Lists (ACL).

Ces permissions permettent de contrôler les opérations qu'une identité est autorisée à effectuer sur les données.

La gestion des permissions repose notamment sur trois droits fondamentaux :

| Permission | Signification |
|---|---|
| Read (R) | Lire un fichier ou consulter le contenu d'un répertoire |
| Write (W) | Modifier un fichier ou créer et supprimer des éléments dans un répertoire |
| Execute (X) | Accéder à un répertoire et le traverser pour atteindre ses éléments |

La signification exacte des droits dépend du type d'élément concerné.

Pour un fichier, la lecture permet de consulter son contenu et l'écriture permet de le modifier.

Pour un répertoire, la lecture permet de lister son contenu, l'écriture permet de créer ou supprimer des éléments et l'exécution permet de le traverser.

### 5.2. Permissions sur les répertoires

Les permissions peuvent être définies à différents niveaux de l'arborescence.

Par exemple, dans Retail Intelligence :

`bronze/`

Le répertoire Bronze pourrait être accessible en écriture à l'équipe d'ingestion et en lecture aux traitements Data Engineering.

En revanche, les analystes métier pourraient ne pas disposer d'un accès direct à cette zone.

Pour le répertoire :

`gold/indicateurs/`

Les analystes métier pourraient disposer de droits de lecture afin de consulter les indicateurs produits.

Cette organisation permet d'adapter les permissions aux responsabilités des différents profils.

### 5.3. Permissions sur les fichiers

Les ACL peuvent également être définies directement sur les fichiers.

Cela permet de gérer les accès à un élément particulier sans nécessairement appliquer les mêmes permissions à tous les fichiers d'un répertoire.

Par exemple, certains fichiers contenant des données intermédiaires pourraient être accessibles uniquement aux traitements techniques.

Les permissions doivent cependant rester cohérentes avec celles des répertoires parents, notamment parce que l'accès à un fichier nécessite de pouvoir traverser les répertoires de son chemin.

### 5.4. ACL par défaut et héritage des permissions

ADLS Gen2 permet également de définir des ACL par défaut sur les répertoires.

Ces ACL par défaut servent de modèle pour les permissions des nouveaux fichiers et sous-répertoires créés dans le répertoire concerné.

Elles facilitent l'application de règles cohérentes lors de la création de nouveaux éléments.

Il est important de distinguer :
- les ACL d'accès, qui définissent les permissions sur l'élément concerné
- les ACL par défaut, qui servent à définir les permissions initiales des futurs éléments créés

Cette distinction permet de mieux gérer les permissions dans un Data Lake dont l'arborescence évolue régulièrement.

### 5.5. Complémentarité entre Azure RBAC et ACL

Les ACL ne remplacent pas Azure RBAC.

Les deux mécanismes interviennent à des niveaux complémentaires.

Azure RBAC permet notamment d'attribuer des rôles à des identités sur des périmètres de ressources Azure.

Les ACL permettent de contrôler plus finement l'accès aux répertoires et aux fichiers dans ADLS Gen2.

Il faut également tenir compte du fait que certains rôles Azure de données accordent des permissions suffisamment larges pour donner accès aux données indépendamment des ACL définies.

Il est donc nécessaire de contrôler les rôles attribués et leurs périmètres afin d'éviter des autorisations trop importantes.

Dans Retail Intelligence, la combinaison des deux mécanismes permettrait de mettre en œuvre une séparation des accès entre :
- l'équipe d'ingestion
- l'équipe Data Engineering
- les analystes métier
- les administrateurs

Cette gestion devra respecter le principe du moindre privilège.

## 6. Différences entre un stockage objet classique et ADLS Gen2 avec HNS

### 6.1. Stockage objet sans HNS

Dans un stockage objet classique, les données sont organisées principalement sous forme d'objets identifiés par leur nom.

Les conteneurs permettent de regrouper ces objets.

Il est possible d'utiliser des séparateurs comme `/` dans les noms afin de simuler une arborescence.

Par exemple :

`silver/ventes/sales_by_store_date/part-00000.parquet`

Ce nom donne l'impression que le fichier est situé dans plusieurs répertoires.

Cependant, dans un espace de noms, les répertoires ne correspondent pas nécessairement à des entités gérées indépendamment. Les séparateurs servent principalement à structurer les noms des objets.

Les opérations de déplacement ou de renommage peuvent alors nécessiter des opérations de copie et de suppression.

### 6.2. Stockage objet avec HNS

Avec le HNS activé, les répertoires et les fichiers sont gérés dans une véritable structure hiérarchique.

Les répertoires deviennent des éléments de l'espace de noms et peuvent être manipulés directement.

Cela apporte notamment :
- une gestion hiérarchique des chemins
- des opérations de renommage et de déplacement plus efficaces
- des permissions au niveau des répertoires et des fichiers
- une meilleure adaptation aux traitements analytiques nécessitant une organisation structurée des données

### 6.3. Tableau comparatif

| Critère | Stockage objet sans HNS | ADLS Gen2 avec HNS |
|---|---|---|
| Organisation | Espace de noms principalement plat | Espace de noms hiérarchique |
| Répertoires | Généralement simulés par des préfixes | Répertoires gérés explicitement |
| Fichiers | Objets identifiés par leur nom | Fichiers organisés dans une hiérarchie |
| Navigation | Basée sur les noms et préfixes | Basée sur les chemins et répertoires |
| Renommage | Peut nécessiter copie et suppression | Opération de renommage au niveau des métadonnées dans les cas pris en charge |
| Déplacement | Peut nécessiter copie et suppression | Gestion hiérarchique plus efficace dans les cas pris en charge |
| Permissions | Principalement basées sur les mécanismes d'accès au stockage objet | RBAC et ACL détaillées |
| Usage analytique | Possible selon les outils utilisés | Adapté aux traitements Big Data et analytiques |

Le HNS apporte donc une organisation plus adaptée aux Data Lakes nécessitant une gestion structurée des fichiers, des chemins et des permissions.

## 7. Intérêt du HNS pour le projet Retail Intelligence

L'utilisation d'ADLS Gen2 avec HNS pourrait apporter plusieurs avantages à Retail Intelligence.

**Organisation des zones de données**

Le HNS permettrait de matérialiser clairement les zones Bronze, Silver et Gold.

Chaque zone pourrait contenir des répertoires correspondant aux domaines fonctionnels et aux différents datasets.

**Gestion des traitements**

Les traitements Spark pourraient accéder aux fichiers à travers des chemins structurés.

Les opérations de gestion des répertoires faciliteraient certaines étapes d'organisation des données.

**Gestion des accès**

Les ACL permettraient de différencier les permissions selon les responsabilités des utilisateurs et des traitements.

Les données sources Bronze pourraient ainsi être protégées, tandis que les jeux Gold seraient accessibles en lecture aux analystes métier.

**Évolutivité**

L'organisation hiérarchique permettrait d'ajouter de nouveaux domaines fonctionnels et de nouveaux jeux de données sans remettre en cause la séparation des zones existantes.

**Traçabilité**

Une arborescence cohérente facilite l'identification des sources, des transformations et des résultats analytiques.

Le HNS ne garantit toutefois pas à lui seul la traçabilité. Celle-ci doit également être assurée par les conventions de nommage, les métadonnées et la documentation des traitements.

## 8. Limites et points de vigilance

Malgré ses avantages, le HNS ne remplace pas les autres mécanismes nécessaires à une architecture Data Lake.

Plusieurs points doivent être pris en compte :

- Le HNS ne réalise pas automatiquement le nettoyage ou la transformation des données.
- Il ne remplace pas un moteur de traitement comme Apache Spark.
- Il ne constitue pas un catalogue de données.
- Il ne garantit pas la qualité des données.
- Les ACL doivent être correctement configurées et maintenues.
- Les permissions sur les répertoires parents doivent être cohérentes avec celles des fichiers.
- Les opérations de suppression et de déplacement doivent respecter les règles de gouvernance.
- Une activation du HNS doit être anticipée lors de la conception du compte de stockage.

Le HNS est donc une fonctionnalité de gestion du stockage et de l'espace de noms, et non une solution complète de gouvernance ou de traitement des données.

## 9. Statut dans le cadre du UC-07

Le parcours B ayant été retenu, le HNS est étudié dans une perspective de transposition vers Azure.

| Élément | Statut |
|---|---|
| Étude du HNS | Réalisée dans cette documentation |
| Organisation hiérarchique cible | Proposée |
| Activation du HNS | Non réalisée |
| Création de répertoires ADLS Gen2 | Non réalisée |
| Configuration des ACL | Non réalisée |
| Vérification des permissions Azure | Non réalisée |

Aucune capture d'écran ou preuve de déploiement Azure n'est donc attendue pour cette étape dans le cadre du parcours retenu.

## 10. Conclusion

Le Hierarchical Namespace constitue une fonctionnalité essentielle d'Azure Data Lake Storage Gen2 pour les architectures nécessitant une organisation hiérarchique des données.

Il permet de gérer explicitement les répertoires et les fichiers, de faciliter les opérations sur les chemins et d'appliquer des permissions détaillées au niveau des éléments du Data Lake.

Par rapport à un stockage objet classique sans HNS, il apporte une meilleure adaptation aux usages analytiques et aux traitements distribués manipulant de nombreux fichiers.

Dans le projet Retail Intelligence, cette fonctionnalité permettrait de structurer les zones Bronze, Silver et Gold et de renforcer la gestion des accès selon les responsabilités des utilisateurs.

Le HNS complète ainsi les mécanismes de stockage et de sécurité d'ADLS Gen2 et constitue un élément important dans la perspective d'une future évolution de la plateforme locale vers Microsoft Azure.