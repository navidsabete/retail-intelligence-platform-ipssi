# Étape 5 – Étudier la sécurité et définir les droits d'accès

## 1. Objectif de l'étape

La sécurité constitue un élément essentiel de l'architecture d'une plateforme Data Lake. Elle permet de protéger les données, de limiter les accès non autorisés et de garantir que chaque utilisateur ou service intervient uniquement dans le périmètre nécessaire à ses missions.

Dans le cadre du projet Retail Intelligence, la sécurité est étudiée pour une architecture cible reposant sur Azure Data Lake Storage Gen2 (ADLS Gen2).

Le projet suivant le Parcours B – Local / Open Source, aucune permission Azure n'est effectivement configurée. Les règles présentées dans cette section constituent donc une proposition de politique de sécurité pour une éventuelle évolution vers Azure.

Les objectifs sont les suivants :
- définir les droits d'accès selon les profils utilisateurs 
- distinguer les rôles Azure RBAC des ACL du Data Lake 
- comprendre la gestion des identités et l'authentification 
- identifier les bonnes pratiques de protection des secrets 
- appliquer le principe du moindre privilège

## 2. Principe général de sécurité

La gestion des accès doit respecter le principe du moindre privilège.

Chaque utilisateur ou service doit disposer uniquement des autorisations nécessaires à l'exécution de ses tâches.

Ce principe permet notamment :
- d'éviter les modifications accidentelles de données 
- de limiter les risques de suppression ou de divulgation 
- de séparer les responsabilités entre les équipes 
- de contrôler les opérations de transformation et de publication 
- de réduire les conséquences d'une compromission de compte

Les droits doivent être attribués de préférence à des groupes plutôt qu'individuellement à chaque utilisateur. Cela facilite leur administration et leur évolution.

## 3. Matrice des droits d'accès proposée

La matrice suivante présente une organisation cible pour les principales équipes susceptibles d'intervenir sur la plateforme Retail Intelligence.

| Profil | Bronze | Silver | Gold |
|---|---|---|---|
| Équipe ingestion | Écriture contrôlée | Aucun accès par défaut | Aucun accès par défaut |
| Équipe Data Engineering | Lecture selon besoin | Lecture / écriture selon mission | Écriture contrôlée |
| Analyste métier | Aucun accès par défaut | Lecture selon besoin | Lecture |
| Administrateur plateforme | Gestion selon habilitation | Gestion selon habilitation | Gestion selon habilitation |

### 3.1 Équipe ingestion

L'équipe ingestion est responsable de l'intégration des données dans la plateforme.

Ses droits seraient limités à l'écriture dans la zone Bronze, afin de permettre le dépôt des données entrantes.

Elle ne disposerait pas d'un accès général aux zones Silver et Gold, sauf nécessité technique justifiée.

Cette séparation permet de limiter les possibilités de modification des données transformées ou des indicateurs métiers.

### 3.2 Équipe Data Engineering

L'équipe Data Engineering assure les traitements, les transformations et la préparation des données.

Elle aurait :
- un accès en lecture à Bronze pour consulter les données sources nécessaires 
- des droits de lecture et d'écriture sur Silver pour réaliser les transformations 
- des droits d'écriture contrôlée sur Gold pour publier les résultats validés

Les droits sur Gold seraient limités aux traitements et aux répertoires dont l'équipe a la responsabilité.

### 3.3 Analyste métier

L'analyste métier exploite les données préparées pour produire des analyses et des indicateurs.

Il disposerait :
- d'aucun accès par défaut à Bronze
- d'un accès en lecture à certains jeux de données Silver si son activité le nécessite 
- d'un accès en lecture à Gold pour consulter les indicateurs validés

Il ne disposerait pas de droits d'écriture sur les données de production.

### 3.4 Administrateur plateforme

L'administrateur assure l'administration technique et la gestion des accès.

Ses droits seraient définis selon ses responsabilités :
- administration des ressources Azure 
- gestion des identités et des autorisations 
- supervision de la plateforme 
- intervention sur les zones de données lorsque cela est nécessaire et autorisé

Le rôle d'administrateur ne doit pas conduire à attribuer automatiquement tous les droits à tous les comptes techniques ou utilisateurs. Les opérations d'administration et les opérations de manipulation des données doivent être distinguées autant que possible.

## 4. Différence entre Azure RBAC et les ACL du Data Lake

Azure propose deux mécanismes complémentaires de gestion des autorisations : les rôles RBAC et les ACL.

### 4.1 Azure RBAC

Azure RBAC signifie *Role-Based Access Control*.

Il s'agit d'un système de gestion des accès fondé sur l'attribution de rôles à des identités, à différents niveaux de ressources Azure.

Un rôle définit les opérations qu'une identité est autorisée à effectuer.

Les rôles peuvent être attribués à différentes portées :
- abonnement
- groupe de ressources
- compte de stockage
- conteneur, selon les rôles et ressources concernés

Il faut distinguer les rôles d'administration des ressources Azure des rôles permettant d'accéder aux données stockées.

Exemples :
- **Reader** : permet de consulter les ressources Azure sans les modifier 
- **Contributor** : permet de gérer certaines ressources, sans accorder automatiquement tous les droits d'administration des accès 
- **Storage Blob Data Reader** : permet de lire les données Blob 
- **Storage Blob Data Contributor** : permet de lire, écrire et supprimer des données Blob 
- **Storage Blob Data Owner** : permet notamment de gérer les données et les ACL

Les rôles doivent être attribués à la portée la plus restreinte possible.

Un rôle de gestion des ressources Azure ne donne pas nécessairement accès au contenu des fichiers. Inversement, un rôle de données peut autoriser la lecture ou la modification des fichiers sans donner le droit d'administrer l'ensemble du compte de stockage.

**Point de vigilance :** certains rôles Azure de données, lorsqu'ils sont attribués à une portée suffisamment large, accordent des droits d'accès qui peuvent prendre le dessus sur les restrictions définies par les ACL. Il faut donc éviter les attributions trop larges et vérifier les effets réels des rôles choisis.

### 4.2 ACL du Data Lake

Les ACL (*Access Control Lists*) permettent de définir des permissions plus fines au niveau des répertoires et des fichiers d'ADLS Gen2.

Elles permettent notamment de gérer trois types de droits :

| Permission | Signification |
|---|---|
| Read (R) | Lire un fichier ou consulter le contenu d'un répertoire |
| Write (W) | Modifier un fichier ou créer et supprimer des éléments dans un répertoire |
| Execute (X) | Traverser un répertoire pour accéder à un chemin |

Les permissions peuvent être définies pour :
- le propriétaire
- le groupe propriétaire
- les utilisateurs nommés 
- les groupes nommés 
- les autres utilisateurs

Les ACL permettent ainsi de contrôler les accès à des emplacements précis dans le Data Lake.

Par exemple, un analyste métier pourrait disposer d'un droit de lecture sur le répertoire Gold contenant les indicateurs de performance des magasins, sans obtenir de droits de modification sur ces données.

ADLS Gen2 permet également de définir des ACL par défaut sur les répertoires. Elles servent de modèle pour les permissions des nouveaux éléments créés à l'intérieur de ces répertoires.

Pour accéder à un fichier, il faut également disposer des permissions de traversée nécessaires sur les répertoires parents.

### 4.3 Complémentarité entre RBAC et ACL

Les deux mécanismes répondent à des besoins différents.

| Critère | Azure RBAC | ACL |
|---|---|---|
| Objectif | Gérer les autorisations sur les ressources et les données selon les rôles | Contrôler finement l'accès aux répertoires et fichiers |
| Niveau d'application | Ressources Azure et données selon le rôle | Répertoires et fichiers |
| Attribution | Rôle associé à une identité ou à un groupe | Permissions associées aux utilisateurs et groupes |
| Exemple | Autoriser une équipe à lire les données d'un conteneur | Autoriser un analyste à lire un répertoire Gold précis |

Dans une architecture ADLS Gen2, RBAC et ACL doivent être conçus ensemble.

Une attribution RBAC trop permissive peut rendre inefficaces les restrictions que l'on pensait appliquer uniquement avec les ACL. Il est donc nécessaire de contrôler les rôles de données accordés à chaque identité.

## 5. Identités et mécanismes d'authentification

### 5.1 Microsoft Entra ID

Microsoft Entra ID est le service de gestion des identités utilisé dans l'environnement Azure.

Il permet d'identifier les utilisateurs, les groupes et les applications qui souhaitent accéder aux ressources.

Dans le projet Retail Intelligence, les identités pourraient correspondre à :
- des utilisateurs de l'équipe Data Engineering
- des analystes métier
- des administrateurs
- des applications ou traitements automatisés

Les groupes Entra ID permettraient de regrouper les utilisateurs selon leurs responsabilités et de simplifier l'attribution des rôles.

### 5.2 Authentification

L'authentification permet de vérifier l'identité d'un utilisateur ou d'un service avant de lui permettre d'accéder à une ressource.

Elle peut s'appuyer sur différents mécanismes :
- authentification interactive des utilisateurs 
- authentification multifacteur (MFA) 
- identités managées pour les services Azure compatibles 
- identités d'application, par exemple les principaux de service

L'authentification ne doit pas être confondue avec l'autorisation :

- **Authentification :** vérifier qui demande l'accès
- **Autorisation :** déterminer ce que cette identité a le droit de faire

Une identité correctement authentifiée ne dispose donc pas automatiquement de droits sur toutes les données.

## 6. Secrets et informations sensibles

Les secrets sont des informations confidentielles permettant notamment d'authentifier un utilisateur ou un service.

Ils peuvent inclure :
- mots de passe 
- clés d'accès 
- chaînes de connexion 
- jetons 
- secrets d'application 
- certificats et clés privées

Ces informations doivent être protégées, car leur divulgation peut permettre à un tiers d'accéder aux ressources ou aux données.

### 6.1 Bonnes pratiques

Les principales règles de sécurité sont les suivantes :

- ne jamais inscrire de mot de passe ou de clé d'accès directement dans un notebook 
- ne pas publier de secrets dans un dépôt Git 
- éviter de placer des informations sensibles dans les fichiers de configuration partagés 
- limiter le nombre de personnes autorisées à consulter les secrets 
- renouveler ou révoquer les secrets lorsqu'ils sont compromis 
- privilégier les identités managées lorsqu'elles sont adaptées au contexte 
- utiliser un coffre-fort de secrets, tel qu'Azure Key Vault, dans une architecture Azure

### 6.2 Rôle d'Azure Key Vault

Azure Key Vault est un service permettant de stocker et de gérer des informations sensibles.

Il peut notamment héberger :
- des secrets 
- des clés cryptographiques 
- des certificats

Dans une architecture future de Retail Intelligence, Key Vault pourrait être utilisé pour centraliser la protection des secrets nécessaires aux traitements automatisés.

L'accès à ces informations devrait lui-même être soumis à des autorisations strictes.

## 7. Application du principe du moindre privilège à Retail Intelligence

Pour appliquer concrètement le principe du moindre privilège, plusieurs règles seraient retenues :

1. Attribuer les droits aux groupes correspondant aux fonctions des équipes.
2. Limiter les accès aux seules zones nécessaires.
3. Privilégier la lecture pour les profils qui consomment les données sans les transformer.
4. Réserver les droits d'écriture aux équipes responsables de l'ingestion ou des transformations.
5. Limiter les droits d'administration aux personnes habilitées.
6. Éviter les rôles trop larges attribués au niveau de l'abonnement ou du compte de stockage.
7. Vérifier régulièrement les autorisations et retirer les droits devenus inutiles.
8. Protéger les secrets et utiliser des mécanismes d'authentification adaptés.

Ces règles permettent de séparer les responsabilités et de limiter les risques liés à une erreur humaine ou à la compromission d'un compte.

## 8. Bilan : sécurité étudiée

Le projet suit le Parcours B. La sécurité Azure est donc étudiée et documentée, mais aucun rôle RBAC ni aucune ACL Azure n'a été configuré dans un environnement cloud.

| Élément | Statut |
|---|---|
| Identification des profils utilisateurs | Réalisée sur le plan documentaire |
| Proposition d'une matrice des droits | Réalisée sur le plan documentaire |
| Étude des rôles Azure RBAC | Réalisée sur le plan documentaire |
| Étude des ACL ADLS Gen2 | Réalisée sur le plan documentaire |
| Étude de Microsoft Entra ID et de l'authentification | Réalisée sur le plan documentaire |
| Étude de la protection des secrets et d'Azure Key Vault | Réalisée sur le plan documentaire |
| Création de groupes Entra ID | Non exécutée |
| Attribution de rôles RBAC | Non exécutée |
| Configuration des ACL | Non exécutée |
| Vérification des accès sur un compte Azure réel | Non exécutée |

## 9. Conclusion

Cette étape a permis de définir une politique de sécurité cible pour la plateforme Retail Intelligence.

La matrice proposée distingue les responsabilités des équipes ingestion, Data Engineering, analyse métier et administration. Elle repose sur une séparation des zones Bronze, Silver et Gold et sur le principe du moindre privilège.

L'étude met également en évidence la complémentarité entre Azure RBAC et les ACL d'ADLS Gen2, ainsi que l'importance de la gestion des identités, de l'authentification et de la protection des secrets.

Même si ces mécanismes n'ont pas été configurés dans Azure dans le cadre du Parcours B, leur étude permet de préparer une éventuelle évolution de la plateforme vers un environnement cloud sécurisé.