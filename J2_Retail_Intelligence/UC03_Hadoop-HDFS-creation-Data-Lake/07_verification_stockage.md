# Étape 5 — Vérification du stockage HDFS
## Rapport de vérification du stockage et de l'intégrité des données

**Projet :** Retail Intelligence Platform  
**Technologie :** Hadoop Distributed File System (HDFS)  
**Répertoire vérifié :** `/retail-lake/raw/tpcxbb/initial/`  
**Date des contrôles :** 17 novembre 2026

---

## 1. Objectif

Cette étape vise à vérifier que les fichiers TPCX-BB déposés lors de l'étape 4 sont correctement stockés dans HDFS, accessibles et conformes aux fichiers sources locaux.

Les contrôles portent sur :

- la présence des répertoires attendus
- la présence des fichiers déposés
- la cohérence des tailles
- les permissions des répertoires et des fichiers
- l'accessibilité des fichiers depuis HDFS
- la comparaison entre les sources locales et les copies HDFS
- la vérification de l'intégrité par somme de contrôle SHA-256

Deux fichiers sont concernés :

- `customer.dat`
- `store_sales.dat`

## 2. Vérification de la présence des répertoires

La commande suivante a été utilisée pour consulter les répertoires de la zone Raw :

```bash
hdfs dfs -ls -d \
/retail-lake \
/retail-lake/raw \
/retail-lake/raw/tpcxbb \
/retail-lake/raw/tpcxbb/initial
```

### Résultats obtenus

```text
drwxr-xr-x   2026-11-17 17:23 /retail-lake
drwxr-xr-x   2026-11-17 15:32 /retail-lake/raw
drwxr-xr-x   2026-11-17 20:49 /retail-lake/raw/tpcxbb
drwxr-xr-x   2026-11-17 21:14 /retail-lake/raw/tpcxbb/initial
```

Les quatre répertoires sont présents dans HDFS.

Le chemin de destination utilisé pour le dépôt est donc correctement créé :

`/retail-lake/raw/tpcxbb/initial/`

## 3. Vérification de la présence des fichiers

La commande utilisée est :

```bash
hdfs dfs -ls -h /retail-lake/raw/tpcxbb/initial/
```

### Résultats obtenus

```text
12.7 M 2026-11-17 21:14 /retail-lake/raw/tpcxbb/initial/customer.dat
88.5 M 2026-11-17 21:14 /retail-lake/raw/tpcxbb/initial/store_sales.dat
```

Les deux fichiers déposés lors de l'étape 4 sont présents dans le répertoire HDFS prévu.

## 4. Vérification de la taille des fichiers

Les tailles exactes des fichiers sources locaux ont été relevées avec :

```bash
stat -c '%n : %s octets' \
./retail_project/data/customer/customer.dat \
./retail_project/data/store_sales/store_sales.dat
```

### Résultats locaux

```text
./retail_project/data/customer/customer.dat : 13279063 octets
./retail_project/data/store_sales/store_sales.dat : 92764700 octets
```

Les tailles dans HDFS ont été consultées avec :

```bash
hdfs dfs -du -h /retail-lake/raw/tpcxbb/initial/
```

### Résultats HDFS

```text
12.7 M  12.7 M  /retail-lake/raw/tpcxbb/initial/customer.dat
88.5 M  88.5 M  /retail-lake/raw/tpcxbb/initial/store_sales.dat
```

### Comparaison

| Fichier | Taille locale exacte | Taille affichée dans HDFS | Résultat |
|---|---:|---:|---|
| `customer.dat` | 13 279 063 octets | 12,7 MB environ | Cohérente |
| `store_sales.dat` | 92 764 700 octets | 88,5 MB environ | Cohérente |

Les valeurs HDFS sont affichées avec l'option `-h`, qui utilise une unité lisible et arrondie. Elles sont cohérentes avec les tailles exactes relevées localement.

## 5. Vérification des permissions

Les permissions ont été consultées avec les commandes :

```bash
echo "=== Répertoires ==="
hdfs dfs -ls -d \
/retail-lake \
/retail-lake/raw \
/retail-lake/raw/tpcxbb \
/retail-lake/raw/tpcxbb/initial

echo "=== Permissions des fichiers ==="
hdfs dfs -ls /retail-lake/raw/tpcxbb/initial/
```

### Résultats obtenus

```text
=== Répertoires ===
drwxr-xr-x   2026-11-17 17:23 /retail-lake
drwxr-xr-x   2026-11-17 15:32 /retail-lake/raw
drwxr-xr-x   2026-11-17 20:49 /retail-lake/raw/tpcxbb
drwxr-xr-x   2026-11-17 21:14 /retail-lake/raw/tpcxbb/initial

=== Permissions des fichiers ===
Found 2 items
-rw-r--r--   2026-11-17 21:14 /retail-lake/raw/tpcxbb/initial/customer.dat
-rw-r--r--   2026-11-17 21:14 /retail-lake/raw/tpcxbb/initial/store_sales.dat
```

### Interprétation

Les répertoires possèdent les permissions `drwxr-xr-x` :

- le propriétaire dispose des droits de lecture, écriture et traversée
- le groupe dispose des droits de lecture et traversée
- les autres utilisateurs disposent également des droits de lecture et traversée

Les fichiers possèdent les permissions `-rw-r--r--` :

- le propriétaire dispose des droits de lecture et écriture
- le groupe dispose du droit de lecture
- les autres utilisateurs disposent également du droit de lecture

### Observation de sécurité

Les permissions constatées permettent la lecture des fichiers par les utilisateurs autres que le propriétaire, sous réserve de leurs droits d'accès à HDFS.

Pour un environnement de production contenant des données sensibles, il serait préférable de définir des droits plus restrictifs, adaptés aux rôles des utilisateurs et aux exigences de confidentialité.

Aucune modification des permissions n'a été effectuée dans le cadre de cette vérification.

## 6. Vérification de l'accessibilité des fichiers

La lecture des fichiers depuis HDFS a été testée avec :

```bash
hdfs dfs -cat /retail-lake/raw/tpcxbb/initial/customer.dat | head -n 3

hdfs dfs -cat /retail-lake/raw/tpcxbb/initial/store_sales.dat | head -n 3
```

Les deux fichiers ont été déclarés accessibles et leur contenu a pu être consulté depuis HDFS.

Cette vérification confirme que les fichiers ne sont pas seulement listés dans le système de fichiers : ils peuvent également être lus.

## 7. Comparaison et contrôle d'intégrité SHA-256

La comparaison des empreintes SHA-256 a été utilisée pour vérifier l'identité du contenu entre les fichiers locaux et les fichiers stockés dans HDFS.

Les commandes utilisées sont :

```bash
sha256sum ./retail_project/data/customer/customer.dat

hdfs dfs -cat /retail-lake/raw/tpcxbb/initial/customer.dat | sha256sum
```

Puis :

```bash
sha256sum ./retail_project/data/store_sales/store_sales.dat

hdfs dfs -cat /retail-lake/raw/tpcxbb/initial/store_sales.dat | sha256sum
```

### Résultats

Les empreintes SHA-256 locales et celles calculées à partir du contenu relu depuis HDFS ont été comparées.

Les résultats communiqués indiquent que les empreintes sont identiques pour les deux fichiers.

Les valeurs hexadécimales n'étant pas disponibles dans les éléments transmis, elles ne sont pas reproduites dans ce rapport.

L'identité des empreintes confirme que le contenu des fichiers stockés dans HDFS correspond aux fichiers sources locaux.

## 8. Conservation des fichiers sources

Les fichiers originaux sont conservés dans le répertoire local :

```text
./retail_project/data/customer/customer.dat
./retail_project/data/store_sales/store_sales.dat
```

Les copies HDFS sont disponibles dans :

```text
/retail-lake/raw/tpcxbb/initial/customer.dat
/retail-lake/raw/tpcxbb/initial/store_sales.dat
```

Le dépôt a été réalisé par copie avec `hdfs dfs -put`. Les sources locales n'ont pas été supprimées.

Cette conservation permet de garder une référence d'origine et de comparer ultérieurement les données sources avec les données stockées ou transformées.

## 9. Synthèse des contrôles

| Contrôle | `customer.dat` | `store_sales.dat` |
|---|---|---|
| Répertoire de destination présent | Oui | Oui |
| Fichier présent dans HDFS | Oui | Oui |
| Taille cohérente | Oui | Oui |
| Permissions consultées | Oui | Oui |
| Lecture depuis HDFS | Réussie | Réussie |
| Empreinte SHA-256 identique | Oui | Oui |
| Source locale conservée | Oui | Oui |

## 10. Conclusion

Les vérifications effectuées confirment que les deux fichiers TPCX-BB déposés lors de l'étape 4 sont correctement stockés dans HDFS.

Les répertoires attendus sont présents, les fichiers apparaissent dans le chemin de destination prévu et leurs tailles sont cohérentes avec celles relevées localement.

Les permissions ont été consultées et documentées. Les deux fichiers sont accessibles en lecture depuis HDFS. Enfin, la comparaison des empreintes SHA-256 confirme l'identité du contenu entre les sources locales et les copies HDFS.

L'étape de vérification du stockage est donc considérée comme réalisée pour les deux fichiers contrôlés.

**Périmètre de validation :** cette conclusion concerne `customer.dat` et `store_sales.dat` dans `/retail-lake/raw/tpcxbb/initial/`. Elle ne signifie pas que tous les fichiers du jeu TPCx-BB ont été déposés ou vérifiés.