# TP3 – Retail Intelligence Platform
## Fiche de vérification de l'environnement
 
**Date :** 18/11/2026
**Système d'exploitation :** Ubuntu Linux  
**Projet :** Retail Intelligence Platform  
**Objectif :** Vérifier la disponibilité de l'environnement Python et Spark avant la réalisation des traitements de données.

### 1. Environnement technique

| Composant | Information |
|---|---|
| Système d'exploitation | Ubuntu Linux |
| Langage | Python |
| Version Python | 3.12.3 |
| Apache Spark | 4.3.0 |
| Version PySpark | 4.3.0 |
| Version Java | OpenJDK 21.0.13.0.3 |
| Mode d'exécution | Local (`local[*]`) |
| Interface de travail | Jupyter Notebook / Terminal |

### 2. Organisation des répertoires

Les données sources du projet sont stockées dans :

`/home/[utilisateur]/retail_project/`

Le répertoire de travail du TP3 est :

`/home/[utilisateur]/retail-intelligence/tp3/`

Organisation retenue :

- `notebooks/` : notebooks Python et PySpark.
- `output/` : répertoire de sortie pour résultats des traitements.
- `logs/` : traces et informations d'exécution.
- `test/` : fichiers de test.

Les données sources originales sont conservées et ne sont pas modifiées.

### 3. Accès aux données

Les données du projet sont disponibles localement sur le poste de travail.

Le projet s'appuie principalement sur le jeu de données synthétique TPCX-BB.

Les fichiers disponibles sont identifiés à l'aide des commandes Linux `ls` et `find`.

Le traitement est effectué en mode local. Aucun accès HDFS n'est nécessaire pour cette séance.

### 4. Vérification de Spark

Une session Spark a été créée avec les paramètres suivants :

- Application : `TP3-Retail-Intelligence`
- Mode : `local[*]`
- Framework : Apache Spark / PySpark.

Un premier fichier DAT de test a été chargé dans un DataFrame Spark.

Les opérations suivantes ont été vérifiées :

- Lecture du fichier DAT.
- Affichage des premières lignes.
- Identification du schéma.
- Vérification du nombre d'enregistrements.
- Écriture des données au format Parquet.
- Relecture du fichier Parquet.