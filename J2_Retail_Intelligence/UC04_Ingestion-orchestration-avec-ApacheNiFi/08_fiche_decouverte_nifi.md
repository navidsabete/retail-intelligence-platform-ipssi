# Étape 6 — Découverte de l'environnement NiFi
# Fiche de découverte de NiFi

**Projet :** Retail Intelligence Platform    
**Date :** 18 novembre 2026

---

## 1. Présentation et objectifs

Apache NiFi est une plateforme open source permettant d'automatiser le déplacement, la transformation et le suivi des données entre différentes sources et destinations.

Cette première étape consiste à découvrir l'environnement NiFi, vérifier son fonctionnement et identifier les principaux composants nécessaires à la construction des futurs flux d'ingestion.

Les objectifs de cette découverte sont les suivants :

- Vérifier l'installation et le fonctionnement de NiFi.
- Identifier la version utilisée et les paramètres techniques.
- Vérifier l'accès à l'interface web.
- Identifier les composants disponibles.
- Comprendre les principaux concepts de NiFi.
- Examiner les Controller Services et le Provenance Repository.
- Identifier les répertoires de stockage.
- Vérifier les éventuelles erreurs dans les journaux d'exécution.

## 2. Environnement technique

L'environnement utilisé repose sur Ubuntu 24.04 exécuté dans WSL2 sous Windows.

Les composants techniques identifiés sont les suivants :

| Élément | Information relevée |
|---|---|
| Système d'exploitation | Ubuntu 24.04 |
| Environnement | WSL2 |
| Java | OpenJDK 21.0.13 |
| Apache NiFi | Version 2.12.0 |
| Répertoire d'installation | `/opt/nifi` |
| JAVA_HOME | `/usr/lib/jvm/java-21-openjdk-amd64` |
| NIFI_HOME | `/opt/nifi` |
| Interface web | HTTPS |
| Port HTTPS | 8443 |

### 2.1 Vérification de Java

La commande suivante a été exécutée :

```bash
java -version
```

Résultat :

```text
openjdk version "21.0.13.0.3" 2026-10-24
OpenJDK Runtime Environment
OpenJDK 64-Bit Server VM
```

La variable d'environnement JAVA_HOME a également été vérifiée :

```bash
echo $JAVA_HOME
```

Résultat :

```text
/usr/lib/jvm/java-21-openjdk-amd64
```

Java 21 est donc installé et correctement référencé dans l'environnement.

### 2.2 Vérification de l'installation de NiFi

La commande suivante permet de vérifier la présence du répertoire d'installation :

```bash
ls -ld /opt/nifi
```

Le répertoire `/opt/nifi` est présent.

Son contenu comprend notamment les répertoires suivants :

- `bin` : scripts de démarrage et d'administration.
- `conf` : fichiers de configuration.
- `lib` : bibliothèques de NiFi.
- `logs` : journaux d'exécution.
- `extensions` : extensions disponibles.
- `flowfile_repository` : stockage des métadonnées et de l'état des FlowFiles.
- `content_repository` : stockage du contenu des FlowFiles.
- `provenance_repository` : stockage des événements de provenance.
- `database_repository` : stockage des données internes de la base de données de NiFi.
- `state` : stockage des états des composants.

La présence de ces répertoires confirme que l'installation dispose de son arborescence technique principale.

### 2.3 Vérification de l'état du service

La commande utilisée est :

```bash
/opt/nifi/bin/nifi.sh status
```

Résultat obtenu :

```text
JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
NIFI_HOME=/opt/nifi

Application Process [25994]
Command Status [SUCCESS] HTTP 200
Status: UP
```

Le résultat confirme que le service Apache NiFi est démarré et opérationnel au moment du contrôle.

La commande retourne un statut HTTP 200 ainsi que l'état `UP`.

### 2.4 Identification de la version

La recherche des bibliothèques dans le répertoire `/opt/nifi/lib` a permis d'identifier :

```text
nifi-framework-api-2.12.0.jar
nifi-framework-nar-2.12.0.nar
```

La version installée est donc Apache NiFi 2.12.0.

## 3. Accès à l'interface web et sécurité

L'interface web de NiFi est accessible à l'adresse suivante :

https://localhost:8443/nifi

### 3.1 Configuration réseau

La commande utilisée pour examiner la configuration est :

```bash
grep -E '^(nifi.web.https.host|nifi.web.https.port|nifi.web.http.host|nifi.web.http.port)' /opt/nifi/conf/nifi.properties
```

Résultat obtenu :

```properties
nifi.web.http.host=
nifi.web.http.port=
nifi.web.https.host=0.0.0.0
nifi.web.https.port=8443
```

### 3.2 Vérification de l'accès

Les vérifications effectuées dans le navigateur ont confirmé :

- L'interface web est accessible.
- L'authentification fonctionne.
- Le canvas NiFi est accessible.
- Un avertissement lié au certificat ou à la sécurité est observé dans le navigateur.

L'authentification permet de protéger l'accès à l'interface et aux fonctionnalités d'administration de NiFi.

HTTPS permet de chiffrer les échanges entre le navigateur et le serveur. L'avertissement observé doit néanmoins être pris en compte : la validité et la confiance accordée au certificat doivent être vérifiées avant une utilisation en production.

## 4. Découverte des composants NiFi

L'exploration de l'interface a permis d'identifier les composants principaux.

| Composant | Disponibilité |
|---|---|
| Processor | Disponible |
| Input Port | Disponible |
| Output Port | Disponible |
| Process Group | Disponible |
| Remote Process Group | Disponible |
| Funnel | Disponible |
| Connection | Disponible |
| Label | Disponible |

### 4.1 Processor

Un Processor est un composant qui réalise une opération sur les données.

Il peut notamment :

- Lire des fichiers.
- Récupérer des données depuis une source.
- Transformer des données.
- Filtrer des informations.
- Écrire des données vers une destination.

Dans Retail Intelligence, les Processors pourront être utilisés pour récupérer les fichiers TPCX-BB, contrôler leur contenu et les transférer vers le Data Lake.

Exemple : lecture d'un fichier CSV contenant des informations de ventes.

### 4.2 FlowFile

Le FlowFile est l'unité de données manipulée et transportée par NiFi.

Il est constitué de deux éléments principaux :

- Un contenu (Content), qui correspond aux données transportées.
- Des attributs (Attributes), qui contiennent des métadonnées associées au contenu.

Exemples d'attributs :

- Nom du fichier.
- Taille du fichier.
- Date de création.
- Type de contenu.
- Chemin d'origine.

Dans Retail Intelligence, un fichier contenant les ventes pourra être représenté par un FlowFile.

Les attributs permettront notamment de conserver des informations sur son origine et son traitement.

### 4.3 Connection

Une Connection représente une liaison entre deux composants NiFi.

Elle permet de transporter les FlowFiles d'un Processor vers un autre.

Elle joue également un rôle dans la gestion des files d'attente et du transfert des données.

Dans Retail Intelligence, une Connection pourra relier un Processor chargé de lire les fichiers de ventes à un autre Processor chargé de vérifier leur format.

### 4.4 Process Group

Un Process Group est un conteneur permettant de regrouper plusieurs composants et d'organiser les flux.

Il facilite la structuration des traitements et leur maintenance.

Dans Retail Intelligence, plusieurs Process Groups pourront être créés pour séparer les domaines fonctionnels :

- Ingestion des ventes.
- Ingestion des produits.
- Ingestion des clients.
- Ingestion des stocks.

Cette organisation permettra de rendre les flux plus lisibles et plus faciles à maintenir.

### 4.5 Controller Service

Un Controller Service est un service partagé pouvant être utilisé par plusieurs composants NiFi.

Il permet notamment de centraliser certaines configurations et fonctionnalités techniques.

Exemples :

- Gestion des connexions à une base de données.
- Configuration de services de lecture et d'écriture.
- Gestion de formats d'enregistrement.
- Accès à certaines ressources externes.

Dans le cadre de Retail Intelligence, ces services pourront faciliter les connexions aux systèmes de stockage et aux différentes sources de données.

**Observation :** la liste des Controller Services consultée dans l'interface est actuellement vide.

Cela signifie qu'aucun service n'est déclaré dans le périmètre consulté. Des services pourront être ajoutés en fonction des besoins des futurs flux d'ingestion.

### 4.6 Provenance Repository

Le Provenance Repository permet de conserver l'historique des événements associés aux FlowFiles.

Il contribue à assurer la traçabilité des traitements réalisés dans NiFi.

Il permet notamment de retrouver des informations sur :

- La création d'un FlowFile.
- Son transfert entre composants.
- Les traitements appliqués.
- Son éventuel archivage ou envoi vers une destination.

Dans Retail Intelligence, la provenance permettra de suivre le parcours des données depuis leur ingestion jusqu'à leur destination dans le Data Lake.

**Observation :** la page Data Provenance est accessible, mais aucun événement n'est actuellement affiché.

Cela est cohérent avec l'absence de flux d'ingestion exécuté et ne constitue pas nécessairement une anomalie.

## 5. Configuration technique et stockage

NiFi utilise plusieurs espaces de stockage internes pour assurer son fonctionnement.

La configuration a été examinée dans le fichier :

```text
/opt/nifi/conf/nifi.properties
```

La commande utilisée est :

```bash
grep -E '^(nifi.flowfile.repository.directory|nifi.content.repository.directory|nifi.provenance.repository.directory|nifi.database.directory)' /opt/nifi/conf/nifi.properties
```

Résultat obtenu :

```properties
nifi.database.directory=./database_repository
nifi.flowfile.repository.directory=./flowfile_repository
nifi.content.repository.directory.default=./content_repository
nifi.provenance.repository.directory.default=./provenance_repository
```

Les chemins sont relatifs au répertoire d'installation de NiFi.

Les répertoires correspondent aux fonctions suivantes :

| Répertoire | Fonction |
|---|---|
| database_repository | Stockage des données internes de la base de données NiFi |
| flowfile_repository | Conservation des informations nécessaires à la gestion des FlowFiles |
| content_repository | Conservation du contenu des FlowFiles |
| provenance_repository | Conservation de l'historique des événements de provenance |

Ces espaces sont indispensables au fonctionnement de NiFi.

Il est important de distinguer ces espaces de stockage internes du Data Lake destiné à accueillir les données métier de Retail Intelligence.

## 6. Analyse des journaux d'exécution

Les journaux de NiFi ont été examinés à l'aide de la commande :

```bash
tail -n 30 /opt/nifi/logs/nifi-app.log
```

Les dernières lignes consultées contiennent principalement des messages de niveau INFO.

Plusieurs opérations normales ont été observées :

- Sauvegarde du Flow Controller.
- Checkpoint du FlowFile Repository.
- Nettoyage des archives du Content Repository.
- Gestion des espaces de stockage.

Exemple :

```text
Successfully checkpointed FlowFile Repository
with 0 records in 0 milliseconds
```

Ce message indique que NiFi a effectué une opération de checkpoint du FlowFile Repository sans rencontrer de difficulté dans l'extrait consulté.

Un autre message observé :

```text
Archive cleanup completed for container default
```

Il indique que le mécanisme de nettoyage des archives a terminé son opération.

Les logs indiquent également :

```text
Bytes used = 60.58 GB
Bytes free = 946.27 GB
Capacity = 1,006.85 GB
```

Ces informations correspondent aux compteurs du conteneur de stockage concerné dans NiFi.

**Bilan :** aucun message d'erreur n'a été identifié dans les 30 dernières lignes consultées. Les opérations affichées sont des opérations normales de maintenance et de gestion interne.

Cette vérification reste limitée à l'extrait consulté et ne garantit pas l'absence d'erreurs antérieures.

## 7. Synthèse des observations

Le tableau suivant récapitule les vérifications réalisées.

| Élément contrôlé | Résultat |
|---|---|
| Installation Java | Conforme |
| Version Java | OpenJDK 21.0.13 |
| Installation NiFi | Présente |
| Version NiFi | 2.12.0 |
| État du service | UP |
| Interface HTTPS | Accessible |
| Authentification | Fonctionnelle |
| Canvas NiFi | Accessible |
| Composants principaux | 8 disponibles |
| Controller Services | Liste vide |
| Provenance Repository | Accessible |
| Événements de provenance | Aucun événement |
| Répertoires de stockage | Identifiés |
| Logs récents | Aucun message d'erreur identifié dans l'extrait |