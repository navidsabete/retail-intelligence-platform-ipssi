# Étape 4 — Dépôt des données TPCx-BB
## Preuves du dépôt et des contrôles de stockage

**Projet :** Retail Intelligence Platform  
**Technologie :** HDFS  
**Zone :** Raw  
**Lot :** Initial  
**Date des vérifications HDFS :** 17 novembre 2026


## 1. Objectif

Cette étape consiste à sélectionner des fichiers réellement présents dans le jeu TPCX-BB, à vérifier leurs caractéristiques et leur lisibilité, puis à les déposer dans HDFS.

Deux fichiers ont été sélectionnés :
- `customer.dat` : données relatives aux clients ;
- `store_sales.dat` : données relatives aux ventes en magasin.

Ils proviennent du répertoire local `retail_project/data/`, correspondant au lot initial.

## 2. Inventaire des fichiers sources

Les fichiers ont été vérifiés avec `ls -l`, puis examinés avec `realpath`, `file`, `stat`, `wc -l`, `test -r`, `awk` et `head`.

| Caractéristique | `customer.dat` | `store_sales.dat` |
|---|---:|---:|
| Domaine | Clients | Ventes en magasin |
| Chemin local relatif | `retail_project/data/customer/customer.dat` | `retail_project/data/store_sales/store_sales.dat` |
| Chemin local absolu | `/home/[user]/retail_project/data/customer/customer.dat` | `/home/[user]/retail_project/data/store_sales/store_sales.dat` |
| Format | Texte UTF-8 | Texte ASCII |
| Fin de ligne | CRLF | CRLF |
| Taille exacte | 13 279 063 octets | 92 764 700 octets |
| Nombre de lignes | 99 000 | 667 579 |
| Champs sur la première ligne | 18 | 23 |
| Lisibilité locale | OK | OK |
| Provenance | TPCX-BB, lot initial (`data/`) | TPCX-BB, lot initial (`data/`) |

Le nom du compte utilisateur a été remplacé par `[user]` dans les chemins absolus.

**Structure :** les fichiers sont des fichiers texte délimités par `|`, sans en-tête. Le nombre de champs indiqué correspond à la première ligne. Les noms métier détaillés des colonnes ne sont pas déduits ici ; ils devront être associés à partir du schéma TPCX-BB ou d'une documentation fiable. En attendant, des noms provisoires peuvent être utilisés : `colonne_1` à `colonne_18` pour `customer.dat`, et `colonne_1` à `colonne_23` pour `store_sales.dat`.

## 3. Contrôles avant le dépôt

Pour chaque fichier, les contrôles ont confirmé :
- l'existence du fichier au chemin indiqué ;
- le format texte et l'encodage détectés ;
- la taille exacte en octets ;
- le nombre de lignes ;
- le nombre de champs sur la première ligne ;
- l'accès en lecture (`LISIBILITE : OK`).

La commande `head -n 3` a permis d'examiner les premières lignes. Les valeurs ont été masquées dans les éléments transmis et ne sont donc pas reproduites dans ce document.

Les deux fichiers comportent des fins de ligne CRLF.

## 4. Dépôt dans HDFS

### 4.1 Destination

Le répertoire de destination est :

```text
/retail-lake/raw/tpcxbb/initial/
```

La commande suivante a confirmé son existence :

```bash
hdfs dfs -ls -d /retail-lake/raw/tpcxbb/initial
```

Sortie communiquée :

```text
0 2026-11-17 21:14 /retail-lake/raw/tpcxbb/initial
```

### 4.2 Commandes de dépôt

Les commandes utilisées sont :

```bash
hdfs dfs -put ./retail_project/data/customer/customer.dat \
  /retail-lake/raw/tpcxbb/initial/

hdfs dfs -put ./retail_project/data/store_sales/store_sales.dat \
  /retail-lake/raw/tpcxbb/initial/
```

Les fichiers sources locaux ont été conservés. Aucune suppression de ces fichiers n'a été effectuée.

## 5. Vérifications après dépôt

### 5.1 Présence dans HDFS

Commande exécutée :

```bash
hdfs dfs -ls -h /retail-lake/raw/tpcxbb/initial/
```

Sortie obtenue :

```text
12.7 M 2026-11-17 21:14 /retail-lake/raw/tpcxbb/initial/customer.dat
88.5 M 2026-11-17 21:14 /retail-lake/raw/tpcxbb/initial/store_sales.dat
```

Les deux fichiers apparaissent dans le répertoire HDFS prévu.

### 5.2 Comparaison des tailles

Tailles locales relevées :

```text
./retail_project/data/customer/customer.dat : 13279063 octets
./retail_project/data/store_sales/store_sales.dat : 92764700 octets
```

Résultat de `hdfs dfs -du -h /retail-lake/raw/tpcxbb/initial/` :

```text
12.7 M  12.7 M  /retail-lake/raw/tpcxbb/initial/customer.dat
88.5 M  88.5 M  /retail-lake/raw/tpcxbb/initial/store_sales.dat
```

Les tailles HDFS affichées de manière arrondie sont cohérentes avec les tailles locales exactes :
- `customer.dat` : 13 279 063 octets, soit environ 12,7 MiB ;
- `store_sales.dat` : 92 764 700 octets, soit environ 88,5 MiB.

### 5.3 Accessibilité et intégrité

Les commandes de lecture HDFS ont été exécutées :

```bash
hdfs dfs -cat /retail-lake/raw/tpcxbb/initial/customer.dat | head -n 3
hdfs dfs -cat /retail-lake/raw/tpcxbb/initial/store_sales.dat | head -n 3
```

Les deux fichiers ont été déclarés accessibles. Les empreintes SHA-256 calculées sur les fichiers locaux et sur le contenu relu depuis HDFS ont été comparées. Selon les résultats communiqués, les empreintes sont identiques pour chacun des deux fichiers.

Les valeurs hexadécimales des empreintes n'ayant pas été fournies, elles ne sont pas reproduites ici. Leur égalité confirme que le contenu relu depuis HDFS correspond au contenu source pour les deux fichiers.

### 5.4 Synthèse des contrôles

| Vérification | `customer.dat` | `store_sales.dat` |
|---|---|---|
| Présence dans HDFS | Confirmée | Confirmée |
| Destination correcte | Oui | Oui |
| Taille cohérente | Oui | Oui |
| Lecture depuis HDFS | Accessible | Accessible |
| Empreinte SHA-256 identique | Oui, selon résultat communiqué | Oui, selon résultat communiqué |
| Source locale conservée | Oui | Oui |

## 6. Provenance et conservation des sources

Les fichiers déposés proviennent du lot initial du jeu TPCX-BB :

```text
./retail_project/data/customer/customer.dat
./retail_project/data/store_sales/store_sales.dat
```

Ils ont été copiés vers :

```text
/retail-lake/raw/tpcxbb/initial/customer.dat
/retail-lake/raw/tpcxbb/initial/store_sales.dat
```

Le sous-répertoire `initial` permet de distinguer ces données du lot `refresh`, qui pourra être déposé séparément dans `/retail-lake/raw/tpcxbb/refresh/`.

La conservation des fichiers locaux maintient une source de référence. La comparaison des empreintes SHA-256 apporte une vérification supplémentaire de l'intégrité entre les sources locales et les copies HDFS.


## 7. Conclusion

Deux fichiers réels du jeu TPCX-BB ont été contrôlés et déposés dans HDFS :
- `customer.dat` : 99 000 lignes, 18 champs sur la première ligne et 13 279 063 octets ;
- `store_sales.dat` : 667 579 lignes, 23 champs sur la première ligne et 92 764 700 octets.

Les vérifications communiquées confirment leur présence dans `/retail-lake/raw/tpcxbb/initial/`, la cohérence de leurs tailles, leur accessibilité depuis HDFS et l'identité de leurs empreintes SHA-256 avec les sources locales.

Les fichiers locaux originaux ont été conservés. Ce dépôt constitue une première preuve d'alimentation de la zone Raw du Data Lake avec des données TPCX-BB réelles.

---

## Annexe — Commandes récapitulatives

```bash
# Dépôt
hdfs dfs -put ./retail_project/data/customer/customer.dat \
  /retail-lake/raw/tpcxbb/initial/

hdfs dfs -put ./retail_project/data/store_sales/store_sales.dat \
  /retail-lake/raw/tpcxbb/initial/

# Présence et tailles HDFS
hdfs dfs -ls -h /retail-lake/raw/tpcxbb/initial/
hdfs dfs -du -h /retail-lake/raw/tpcxbb/initial/

# Lecture depuis HDFS
hdfs dfs -cat /retail-lake/raw/tpcxbb/initial/customer.dat | head -n 3
hdfs dfs -cat /retail-lake/raw/tpcxbb/initial/store_sales.dat | head -n 3

# Comparaison des empreintes
sha256sum ./retail_project/data/customer/customer.dat
hdfs dfs -cat /retail-lake/raw/tpcxbb/initial/customer.dat | sha256sum

sha256sum ./retail_project/data/store_sales/store_sales.dat
hdfs dfs -cat /retail-lake/raw/tpcxbb/initial/store_sales.dat | sha256sum
```
