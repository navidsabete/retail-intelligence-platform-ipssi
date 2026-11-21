# Étape 7 – Produire le schéma d'architecture Azure

## 1. Objectif

Cette étape consiste à présenter une architecture cible permettant de transposer la plateforme Retail Intelligence vers Microsoft Azure.

Le schéma doit représenter les sources de données, les mécanismes d'ingestion, le stockage, les traitements, les jeux de données analytiques et les principes de sécurité.

Le projet suit le Parcours B – Local / Open Source. Il est donc essentiel de distinguer les composants réellement utilisés dans l'environnement local des services Azure étudiés ou envisagés pour une évolution future.

## 2. Sources de données

La source principale du projet est le jeu de données synthétique TPCx-BB.

Il alimente les traitements réalisés dans le cadre de Retail Intelligence et permet de produire les données organisées dans les zones Bronze, Silver et Gold.

Aucune source de données complémentaire distincte n'a été identifiée dans les éléments documentés du projet.

Une éventuelle source complémentaire pourrait être ajoutée ultérieurement, à condition de préciser son origine, son format, son utilité et les conditions de son utilisation. Elle devrait rester clairement séparée des données TPCx-BB.

## 3. Environnement local réellement utilisé

L'environnement local constitue la base technique effectivement utilisée pour le projet.

Il repose notamment sur :
- Linux 
- Python 
- Apache Spark et PySpark 
- Pandas 
- Jupyter Notebook 
- des fichiers Parquet avec compression Snappy 
- une organisation des données en Bronze, Silver et Gold

Les données produites dans les travaux précédents comprennent notamment :
- les données de ventes détaillées 
- les agrégations de ventes par magasin et par date 
- les agrégations par produit et par date 
- les données d'inventaire 
- les données rapprochant ventes et stocks 
- le jeu Gold `sales_performance_by_store`

Les traitements locaux permettent de préparer les données, de réaliser les agrégations et de produire des indicateurs exploitables.

Les résultats et visualisations produits précédemment constituent des exemples d'usages analytiques locaux.

## 4. Architecture Azure cible

L'architecture Azure proposée repose sur plusieurs services complémentaires.

### 4.1 Ingestion

Azure Data Factory pourrait être utilisé pour organiser les flux d'ingestion.

Il permettrait de récupérer les données sources autorisées, de les déplacer vers le stockage cible et d'orchestrer les traitements suivants.

### 4.2 Stockage : ADLS Gen2

Azure Data Lake Storage Gen2 constituerait le stockage central de la plateforme.

Le Hierarchical Namespace serait activé afin de permettre une organisation hiérarchique des répertoires.

Le conteneur `retail-intelligence` accueillerait les trois zones principales :

- **Bronze** : conservation des données sources 
- **Silver** : données préparées, nettoyées et transformées 
- **Gold** : indicateurs et jeux de données destinés aux usages analytiques

Les répertoires `quality` et `documentation` pourraient compléter cette organisation.

### 4.3 Traitements

Azure Synapse Analytics pourrait fournir l'environnement de traitement et d'analyse.

Un pool Apache Spark permettrait d'exécuter des notebooks PySpark pour reproduire les opérations de préparation, de transformation et d'agrégation déjà réalisées localement.

Les résultats seraient ensuite enregistrés dans les zones Silver et Gold d'ADLS Gen2.

### 4.4 Usages analytiques

Les données Gold pourraient être interrogées avec les capacités SQL de Synapse ou exploitées par des outils décisionnels compatibles.

Le jeu `sales_performance_by_store` constitue un exemple de résultat destiné à l'analyse des performances commerciales par magasin.

Les usages pourraient inclure :
- le suivi du chiffre d'affaires 
- la comparaison des performances entre magasins 
- l'analyse des ventes par période 
- la consultation d'indicateurs agrégés

Ces usages sont des possibilités de transposition et non des services analytiques Azure effectivement déployés.

## 5. Principes de sécurité

La sécurité serait organisée autour de Microsoft Entra ID, Azure RBAC et des ACL d'ADLS Gen2.

- Microsoft Entra ID assurerait la gestion des identités et l'authentification.
- Azure RBAC permettrait d'attribuer les rôles sur les ressources et les données selon les portées retenues.
- Les ACL permettraient de préciser les autorisations au niveau des répertoires et des fichiers.
- Azure Key Vault pourrait protéger les secrets utilisés par les traitements et les applications.

Les accès seraient définis selon le principe du moindre privilège. Les droits seraient adaptés aux responsabilités des équipes ingestion, Data Engineering, analyse métier et administration.

Ces mécanismes sont étudiés dans le cadre du projet, mais ne sont pas configurés sur un environnement Azure réel.

## 6. Distinction entre composants réalisés, étudiés et proposés

| Composant | Statut | Justification |
|---|---|---|
| Données TPCx-BB | Utilisées | Source du projet |
| Environnement Linux | Réalisé | Environnement local utilisé |
| Python et PySpark | Utilisés | Traitements locaux |
| Apache Spark | Utilisé | Moteur de traitement local |
| Parquet Snappy | Utilisé | Format de stockage des résultats |
| Zones Bronze, Silver et Gold locales | Réalisées | Organisation des données du projet |
| ADLS Gen2 et HNS | Étudiés | Stockage cible Azure |
| Azure Data Factory | Étudié | Intégration et orchestration envisagées |
| Azure Synapse Analytics | Étudié | Environnement analytique cible |
| Spark Pools Azure | Étudiés | Calcul distribué dans Synapse |
| Synapse SQL | Étudié | Exploration et interrogation des données |
| Microsoft Entra ID, RBAC et ACL | Étudiés | Sécurité cible |
| Azure Key Vault | Proposé | Gestion future des secrets |
| Architecture Azure complète | Proposée | Évolution possible de la plateforme |

## 7. Limites et perspectives

L'architecture présentée est une architecture cible. Elle ne constitue pas la description d'une plateforme Azure actuellement déployée.

Aucun compte de stockage ADLS Gen2, pipeline Data Factory, Workspace Synapse ou Spark Pool Azure n'a été créé dans le cadre de ce Parcours B.

L'intérêt de cette architecture est de montrer comment les traitements existants pourraient être transposés vers le cloud, tout en conservant la logique Bronze/Silver/Gold et les principes de sécurité définis précédemment.

Une évolution vers Azure pourrait être envisagée ultérieurement.

## 8. Conclusion

Le schéma d'architecture présente une trajectoire possible entre l'environnement local actuel de Retail Intelligence et une future plateforme Azure.

L'environnement local fournit les traitements et les résultats déjà réalisés. Les services Azure étudiés permettraient, dans une évolution future, de centraliser le stockage avec ADLS Gen2, d'automatiser l'ingestion avec Data Factory et de réaliser les traitements et analyses avec Synapse.

La distinction entre composants réellement utilisés, services étudiés et composants proposés garantit une présentation fidèle de l'état d'avancement du projet.

**Azure constitue une perspective d'évolution future et non un environnement déployé dans le cadre de ce travail.**