# Étape 1 : Identification des composants Azure

## 1. Objectif

Cette première étape du UC-07 consiste à identifier les principaux composants de Microsoft Azure intervenant dans la mise en place d'une plateforme Data reposant sur Azure Data Lake Storage Gen2 (ADLS Gen2).

L'objectif est de comprendre le rôle de chaque composant, ses interactions avec les autres services Azure et son utilité potentielle dans le projet Retail Intelligence.

Dans le cadre de cette UC-07, le parcours B (Local / Open Source) a été retenu. Les services Azure sont donc étudiés dans une perspective de transposition de l'architecture existante, sans déploiement effectif de ressources cloud.

## 2. Présentation des composants Azure

### 2.1. Abonnement Azure

L'abonnement Azure constitue le cadre administratif et financier dans lequel sont créées et utilisées les ressources cloud.

Il permet notamment :
- de gérer les ressources Azure associées
- de contrôler les coûts et la facturation
- d'associer des mécanismes de gestion des accès
- de définir des limites et des politiques d'utilisation.

Dans le contexte de Retail Intelligence, un abonnement Azure serait nécessaire pour provisionner les ressources destinées à héberger et traiter les données du projet.

**Application au projet :** aucun abonnement Azure n'est utilisé dans le cadre du parcours B. Ce composant est uniquement étudié en vue d'une éventuelle évolution future vers le cloud.

### 2.2. Groupe de ressources (Resource Group)

Un groupe de ressources est un conteneur logique permettant de regrouper et de gérer plusieurs ressources Azure appartenant à une même solution ou à un même périmètre fonctionnel.

Il facilite :
- l'organisation des ressources
- la gestion des autorisations
- le suivi des coûts 
- l'application de politiques de gestion 
- les opérations de déploiement et de suppression.

Pour Retail Intelligence, un groupe de ressources pourrait regrouper les composants nécessaires à la plateforme Data, notamment le compte de stockage ADLS Gen2 et, si nécessaire, les services d'intégration et d'analyse.

**Exemple de nommage proposé :** `rg-retail-intelligence`.

Ce nom constitue une proposition de conception et ne correspond pas à une ressource effectivement créée.

### 2.3. Compte de stockage (Storage Account)

Le compte de stockage Azure représente la ressource qui fournit les capacités de stockage des données.

Il peut notamment prendre en charge différents services de stockage Azure. Dans notre contexte, il serait configuré pour utiliser les capacités d'Azure Data Lake Storage Gen2.

Il constitue le niveau de gestion du stockage auquel sont associés :
- les paramètres de configuration
- les caractéristiques de redondance
- les mécanismes de sécurité
- les règles réseau
- les paramètres de performance et de facturation

Pour Retail Intelligence, ce compte hébergerait les données organisées selon les différentes zones de l'architecture Data Lake.

**Exemple de nommage proposé :** `stretailintelligence`.

Il s'agit d'un exemple de convention de nommage et non d'un compte existant.

### 2.4. Conteneur (Container)

Un conteneur est un espace logique de stockage créé dans un compte de stockage Azure Blob.

Dans ADLS Gen2, il constitue le point de départ de l'organisation des données. Il contient les répertoires et les fichiers associés.

Pour Retail Intelligence, un conteneur pourrait être nommé `retail-intelligence` et accueillir l'ensemble des zones de données du projet :

- Bronze
- Silver
- Gold
- Quality
- Documentation

Ce choix permet de regrouper les données dans un même espace logique tout en organisant les accès à différents niveaux.

### 2.5. Azure Data Lake Storage Gen2 (ADLS Gen2)

Azure Data Lake Storage Gen2 est une solution de stockage de données construite sur Azure Blob Storage et enrichie de fonctionnalités adaptées aux usages analytiques et aux traitements Big Data.

Elle permet de stocker des données de différentes natures :
- données structurées
- données semi-structurées
- données non structurées

ADLS Gen2 est particulièrement adapté à une architecture Data Lake, car il permet de centraliser les données et de les organiser selon différentes zones de traitement.

Dans Retail Intelligence, ADLS Gen2 pourrait accueillir :
- les données sources TPCx-BB dans la zone Bronze
- les données nettoyées et transformées dans la zone Silver
- les jeux de données agrégés et les indicateurs dans la zone Gold

Les fichiers Parquet utilisés dans l'architecture locale pourraient également être conservés dans ADLS Gen2.

**Rôle dans l'architecture :** ADLS Gen2 assure le stockage des données. Il ne constitue pas, à lui seul, un moteur de transformation ou d'analyse.

### 2.6. Hierarchical Namespace (HNS)

Le Hierarchical Namespace est une fonctionnalité d'ADLS Gen2 qui permet de gérer les données à travers une organisation hiérarchique de répertoires et de fichiers.

Contrairement à une organisation classique de stockage objet reposant principalement sur des noms de blobs et des préfixes, le HNS permet de manipuler les répertoires et les fichiers comme des éléments d'un espace de noms hiérarchique.

Il apporte notamment :
- une organisation logique en répertoires et sous-répertoires
- des opérations de gestion des chemins adaptées aux traitements analytiques
- la possibilité de gérer des permissions au niveau des répertoires et des fichiers à travers des ACL
- une meilleure intégration avec les outils et moteurs de traitement Big Data compatibles

Dans Retail Intelligence, le HNS faciliterait la représentation des zones Bronze, Silver et Gold ainsi que la gestion des accès aux différentes parties du Data Lake.

Le HNS est une caractéristique essentielle d'ADLS Gen2 pour les usages Data Lake. Il doit être activé sur le compte de stockage lors de sa configuration.

### 2.7. Microsoft Entra ID

Microsoft Entra ID est le service de gestion des identités et des accès de Microsoft.

Il permet d'identifier et d'authentifier les utilisateurs, les groupes et les applications qui souhaitent accéder aux ressources Azure.

Il intervient notamment dans :
- l'authentification des utilisateurs
- la gestion des identités applicatives
- l'utilisation des identités managées
- l'association des identités aux rôles et permissions

Dans Retail Intelligence, Microsoft Entra ID pourrait permettre d'identifier différents profils :
- administrateur de la plateforme
- équipe Data Engineering
- équipe d'ingestion
- analystes métier

Chaque profil pourrait disposer d'autorisations adaptées à ses responsabilités.

**Rôle dans l'architecture :** Microsoft Entra ID permet de gérer les identités utilisées pour accéder aux services Azure.

### 2.8. Azure RBAC

Azure Role-Based Access Control (Azure RBAC) est le mécanisme de gestion des autorisations basé sur les rôles dans Azure.

Il permet d'attribuer des permissions à des utilisateurs, groupes ou identités applicatives sur différentes ressources Azure.

Les rôles sont associés à un périmètre d'application appelé scope, qui peut notamment correspondre :
- à un abonnement
- à un groupe de ressources
- à un compte de stockage
- à un autre périmètre de ressource pris en charge.

Quelques exemples de rôles intégrés :
- Reader : consultation des ressources sans modification de leur configuration
- Contributor : gestion de nombreuses ressources sans attribution de rôles
- Storage Blob Data Reader : lecture des données Blob 
- Storage Blob Data Contributor : lecture, écriture et suppression des données Blob

Il est important de distinguer les rôles de gestion des ressources Azure des rôles permettant d'accéder aux données stockées.

Dans Retail Intelligence, Azure RBAC permettrait de définir les autorisations générales d'accès aux ressources et aux données selon les responsabilités des différents utilisateurs.

### 2.9. ACL (Access Control Lists)

Les ACL sont des listes de contrôle d'accès permettant de gérer les permissions sur les répertoires et les fichiers d'ADLS Gen2.

Elles permettent de définir les droits associés à différentes identités :
- lecture (Read) 
- écriture (Write) 
- exécution ou traversée d'un répertoire (Execute)

Les ACL peuvent être configurées pour les utilisateurs, les groupes et les autres identités pris en charge.

Elles permettent ainsi une gestion plus fine des accès aux données que les autorisations générales définies au niveau des ressources.

Dans Retail Intelligence, les ACL pourraient notamment permettre :
- à l'équipe d'ingestion d'écrire dans Bronze
- à l'équipe Data Engineering de lire Bronze et de produire les données Silver
- aux analystes métier de consulter les jeux de données Gold
- de limiter l'accès aux données sources lorsque cela n'est pas nécessaire

Les ACL doivent être définies en respectant le principe du moindre privilège.

## 3. Relations entre les composants Azure

Les différents composants interviennent à plusieurs niveaux de l'architecture.

Leur organisation peut être représentée de la manière suivante :

```text
Abonnement Azure
|
+-- Groupe de ressources
    |
    +-- Compte de stockage
        |
        +-- ADLS Gen2
            |
            +-- HNS activé
            |
            +-- Conteneur : retail-intelligence
                |
                +-- bronze/
                |
                +-- silver/
                |
                +-- gold/
                |
                +-- quality/
                |
                +-- documentation/
```

La gestion des identités et des autorisations intervient transversalement :

```text
Microsoft Entra ID
|
+-- Utilisateurs
+-- Groupes
+-- Identités applicatives
|
+-- Azure RBAC
|   |
|   +-- Autorisations sur les ressources Azure
|
+-- ACL ADLS Gen2
    |
    +-- Permissions sur les répertoires
    +-- Permissions sur les fichiers
```

L'abonnement constitue le cadre administratif et financier. Le groupe de ressources permet d'organiser les ressources associées à la solution.

Le compte de stockage héberge ADLS Gen2, dans lequel les données sont organisées à l'intérieur de conteneurs.

Le HNS apporte les fonctionnalités de gestion hiérarchique des chemins et des permissions au niveau des répertoires et fichiers.

Enfin, Microsoft Entra ID intervient dans l'identification des utilisateurs et des applications. Azure RBAC et les ACL permettent ensuite de contrôler leurs autorisations selon les périmètres concernés.

## 4. Application à l'architecture Retail Intelligence

Dans le cadre d'une éventuelle transposition vers Azure, l'organisation pourrait être la suivante :

| Composant Azure | Fonction dans Retail Intelligence |
|---|---|
| Abonnement Azure | Cadre administratif et financier |
| Groupe de ressources | Regroupement des ressources du projet |
| Compte de stockage | Hébergement du Data Lake |
| Conteneur | Espace logique du projet |
| ADLS Gen2 | Stockage centralisé des données |
| HNS | Organisation hiérarchique des données |
| Microsoft Entra ID | Gestion des identités |
| Azure RBAC | Autorisations sur les ressources et les données selon les rôles |
| ACL | Permissions détaillées sur les répertoires et fichiers |

Cette architecture permettrait de conserver les principes fonctionnels déjà appliqués dans le projet local : séparation des zones, organisation des données, contrôle des accès et traçabilité.

## 5. Statut des composants dans le cadre du UC-07

Le parcours B ayant été retenu, aucun des composants Azure présentés dans cette étape n'est déclaré comme effectivement déployé.

| Composant | Statut |
|---|---|
| Abonnement Azure | Étudié, non utilisé |
| Groupe de ressources | Étudié, non créé |
| Compte de stockage | Étudié, non créé |
| Conteneur | Étudié, non créé |
| ADLS Gen2 | Étudié, non déployé |
| HNS | Étudié, non activé |
| Microsoft Entra ID | Étudié, non configuré pour le projet |
| Azure RBAC | Étudié, non configuré |
| ACL | Étudiées, non configurées |

Les noms de ressources et l'organisation présentés dans cette étape sont des propositions de conception.

Ils ne constituent pas des preuves de déploiement.

## 6. Conclusion

Cette première étape a permis d'identifier les principaux composants nécessaires à la conception d'une architecture Data sur Microsoft Azure.

ADLS Gen2 constitue le socle de stockage, tandis que le Hierarchical Namespace apporte une organisation hiérarchique adaptée aux usages Data Lake.

Microsoft Entra ID, Azure RBAC et les ACL assurent les mécanismes de gestion des identités et des autorisations.

La compréhension des relations entre ces composants constitue un prérequis pour concevoir une organisation des zones Bronze, Silver et Gold cohérente avec l'architecture Retail Intelligence existante.

Dans le cadre du parcours B, cette architecture reste une proposition documentaire. Elle constitue néanmoins une base pour envisager une future évolution vers Azure, sans remettre en cause les traitements et les données actuellement exploités dans l'environnement local.