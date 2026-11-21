# Étape 4 – Documenter une mise en œuvre simulée sur Azure

## 1. Objectif de l’étape

Cette étape consiste à décrire la mise en œuvre de l'organisation des données Retail Intelligence dans un environnement Azure Data Lake Storage Gen2 (ADLS Gen2).

Le projet suit le **Parcours B – Local / Open Source**. Aucun environnement Azure n'est déployé dans le cadre de cette étape. La mise en œuvre est donc présentée sous la forme d'une simulation documentaire.

Cette démarche permet de préciser les ressources nécessaires, les opérations à effectuer et les contrôles à réaliser, sans créer de ressources cloud ni engager de coûts liés à un abonnement Azure.

## 2. Organisation cible

L'organisation proposée à l'étape 2 est conservée. Elle repose sur un conteneur dédié au projet, dans lequel les données sont réparties selon les trois zones Bronze, Silver et Gold.

```text
Compte de stockage ADLS Gen2
|
+-- Conteneur : retail-intelligence
    |
    +-- bronze/
    |   +-- tpcxbb/
    |
    +-- silver/
    |   +-- ventes/
    |   |   +-- store_sales/
    |   |   +-- sales_by_store/
    |   |   +-- sales_by_store_date/
    |   |   +-- sales_by_item_date/
    |   |
    |   +-- inventory/
    |   |   +-- inventory/
    |   |   +-- inventory_by_item_date/
    |   |
    |   +-- ventes_stocks/
    |       +-- sales_inventory_by_item_date/
    |
    +-- gold/
    |   +-- indicateurs/
    |   |   +-- sales_performance_by_store/
    |   |
    |   +-- analyses/
    |
    +-- quality/
    |
    +-- documentation/
```

Cette arborescence constitue une **organisation logique cible**. Elle ne représente pas des répertoires réellement créés dans Azure.

Les données Silver et Gold déjà produites dans le projet local pourraient servir de référence pour préparer un échantillon de démonstration, sous réserve des autorisations nécessaires.

Les données sources du TP3 doivent rester préservées : toute éventuelle préparation d'un échantillon pour un transfert serait effectuée sur une copie de travail autorisée, sans modification des données d'origine.

## 3. Ressources Azure nécessaires

Pour réaliser cette mise en œuvre, les ressources suivantes seraient nécessaires :

| Ressource | Fonction dans le projet |
|---|---|
| Abonnement Azure | Fournir le contexte administratif et financier des ressources |
| Groupe de ressources | Regrouper les ressources Azure du projet |
| Compte de stockage | Héberger les données du Data Lake |
| ADLS Gen2 avec HNS activé | Fournir un espace de stockage avec une organisation hiérarchique |
| Conteneur `retail-intelligence` | Accueillir les zones de données du projet |
| Microsoft Entra ID | Gérer les identités et l'authentification |
| Azure RBAC et ACL | Contrôler les accès aux ressources et aux données |

Le compte de stockage devrait disposer de la fonctionnalité **Hierarchical Namespace (HNS)** activée afin de bénéficier des capacités propres à ADLS Gen2.

Aucune de ces ressources n'a été créée dans le cadre du Parcours B.

## 4. Opérations de création et de dépôt envisagées

Dans un environnement Azure autorisé, la mise en œuvre suivrait les opérations suivantes.

### 4.1 Identifier le compte de stockage

Il faudrait commencer par identifier le compte de stockage mis à disposition ou créé dans le cadre du projet.

Les informations à relever seraient :
- le nom du compte de stockage
- le groupe de ressources auquel il appartient
- l'abonnement associé
- le type de compte et ses caractéristiques
- l'état d'activation du HNS

### 4.2 Vérifier les caractéristiques ADLS Gen2

Il faudrait vérifier que le compte dispose bien des caractéristiques attendues pour ADLS Gen2.

Le contrôle principal porterait sur l'activation du Hierarchical Namespace.

Cette vérification permettrait de s'assurer que le stockage prend en charge une véritable organisation hiérarchique des répertoires et les mécanismes associés.

### 4.3 Identifier ou créer le conteneur

Le conteneur `retail-intelligence` serait identifié ou créé selon les consignes du formateur.

Il servirait de point d'entrée pour l'organisation des zones Bronze, Silver et Gold.

### 4.4 Créer l'organisation des répertoires

Les répertoires seraient créés conformément à l'arborescence définie précédemment.

L'organisation serait construite progressivement :
- création des répertoires principaux `bronze`, `silver` et `gold`
- création des sous-répertoires correspondant aux domaines fonctionnels
- création éventuelle des répertoires `quality` et `documentation`

Cette organisation faciliterait la navigation, la séparation des usages et la gestion des droits d'accès.

### 4.5 Déposer un fichier de démonstration

Un fichier de démonstration autorisé pourrait être sélectionné parmi les résultats du projet Retail Intelligence.

Par exemple, un échantillon issu d'un jeu de données Silver ou Gold pourrait illustrer le dépôt dans le Data Lake.

Le choix du fichier devrait tenir compte :
- des autorisations de réutilisation
- de son intérêt pour la démonstration
- de sa taille
- de son format
- de l'absence de données sensibles ou non autorisées

Le fichier serait ensuite déposé dans le répertoire correspondant à sa zone et à son domaine fonctionnel.

**Dans le cadre du présent Parcours B, aucun fichier n'a été transféré vers Azure. Aucun fichier de démonstration précis n'est donc déclaré comme déposé.**

## 5. Contrôles qui seraient réalisés

Après la création de l'organisation et le dépôt du fichier, plusieurs contrôles permettraient de vérifier le bon fonctionnement de l'environnement.

| Contrôle | Vérification attendue |
|---|---|
| Compte de stockage | Le compte identifié correspond à celui prévu pour le projet |
| Activation du HNS | La fonctionnalité est activée |
| Conteneur | Le conteneur `retail-intelligence` existe et est accessible |
| Arborescence | Les répertoires attendus sont présents |
| Dépôt du fichier | Le fichier apparaît dans le chemin de destination |
| Accessibilité | Un utilisateur autorisé peut consulter ou lire le fichier |
| Permissions | Les droits d'accès correspondent aux autorisations prévues |
| Traçabilité | Le chemin, le nom du fichier et les informations de dépôt peuvent être relevés |

L'accessibilité devrait être vérifiée avec une identité disposant des droits nécessaires. La présence d'un fichier dans le stockage ne suffit pas, à elle seule, à démontrer que tous les utilisateurs autorisés peuvent y accéder.

## 6. Chemins et preuves de réalisation

Dans le cas d'un déploiement réel, les éléments suivants seraient conservés comme preuves :
- nom du compte de stockage
- nom du conteneur
- chemin complet du fichier déposé
- capture de l'arborescence des répertoires 
- capture ou relevé de l'état d'activation du HNS 
- capture du fichier présent dans son répertoire 
- résultat d'un contrôle d'accès réalisé avec une identité autorisée

Exemple de chemin cible, donné à titre illustratif :

```text
retail-intelligence/gold/indicateurs/
sales_performance_by_store/
```

Ce chemin est une proposition d'organisation et non un chemin Azure effectivement vérifié.

Dans le cadre de cette simulation, aucune capture d'écran Azure ni aucun relevé de dépôt ne peut être fourni comme preuve d'exécution. Les éléments précédents constituent la liste des preuves à recueillir si un environnement Azure devient disponible.

## 7. Bilan : actions réalisées et actions non exécutées

Il est important de distinguer les travaux de conception effectivement réalisés des opérations qui nécessiteraient un accès à Azure.

| Action | Statut |
|---|---|
| Définition de l'organisation cible Bronze/Silver/Gold | Réalisée sur le plan documentaire |
| Identification des ressources Azure nécessaires | Réalisée sur le plan documentaire |
| Description des opérations de création | Réalisée sur le plan documentaire |
| Définition des contrôles à effectuer | Réalisée sur le plan documentaire |
| Identification d'un compte de stockage Azure réel | Non exécutée |
| Vérification de l'activation du HNS sur un compte réel | Non exécutée |
| Création ou identification effective du conteneur | Non exécutée |
| Création effective des répertoires dans Azure | Non exécutée |
| Dépôt d'un fichier dans Azure | Non exécuté |
| Vérification effective de l'accessibilité du fichier | Non exécutée |
| Collecte de captures d'écran et de preuves Azure | Non exécutée |

## 8. Conclusion

Cette étape a permis de formaliser une procédure de mise en œuvre de l'organisation Retail Intelligence dans Azure Data Lake Storage Gen2.

La simulation décrit les ressources nécessaires, l'organisation des répertoires, les opérations de dépôt et les contrôles qui permettraient de valider le fonctionnement de l'environnement.

Aucun déploiement Azure n'a été effectué dans le cadre de ce travail, conformément au choix du Parcours B. Cette approche permet de poursuivre le projet dans l'environnement local existant, sans dépendance immédiate à un abonnement cloud.

**Azure reste néanmoins une perspective d'évolution possible.** Une transposition future vers ADLS Gen2 pourrait être envisagée.