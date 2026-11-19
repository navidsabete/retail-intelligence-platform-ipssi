# Étapes 5 et 6 – Transformations et production des données Silver

## 1. Organisation des chemins

Le projet distingue les sources originales, les données nettoyées et les données transformées.

| Élément | Chemin |
|---|---|
| Sources originales (Bronze) | `~/retail-intelligence/tp3/data/bronze/` |
| Racine du projet | `~/retail-intelligence/tp3/` |
| Données nettoyées de l'étape 4 (Silver) | `~/retail-intelligence/tp3/data/silver/` |
| Jeux transformés des étapes 5 et 6 | `~/retail-intelligence/tp3/data/silver-transformed/` |

Les fichiers originaux sont conservés dans la zone Bronze. Les données nettoyées de l'étape 4 sont utilisées comme entrées des transformations. Les résultats des étapes 5 et 6 sont enregistrés séparément dans `data/silver-transformed/`.

Cette organisation permet de distinguer les données brutes, les données nettoyées et les jeux transformés, tout en conservant la traçabilité entre les différentes étapes du pipeline.

## 2. Sources et prérequis

| Source | Entrée Parquet | Granularité source |
|---|---|---|
| Ventes | `data/silver/store_sales` | Ligne de vente d'un article sur un ticket, magasin et date |
| Stock | `data/silver/inventory` | Quantité d'un article dans un entrepôt à une date |

Les données utilisées proviennent exclusivement des sorties de l'étape 4.

Le script vérifie :
- la présence des répertoires d'entrée
- l'existence des colonnes nécessaires
- la compatibilité des types des mesures utilisées
- la cohérence des clés avant la jointure

Les volumes lus au démarrage sont :

| Source | Nombre de lignes |
|---|---:|
| `store_sales` | 667 579 |
| `inventory` | 23 249 101 |

## 3. Étape 5 – Transformations

### 3.1 Harmonisation et provenance

Les jeux détaillés nettoyés sont conservés avec leurs colonnes métier et leurs indicateurs techniques issus de l'étape 4.

Trois colonnes de traçabilité sont ajoutées :

| Colonne | Rôle |
|---|---|
| `_source_dataset` | Identifie la source métier |
| `_source_original_file` | Indique le chemin du fichier DAT original |
| `_processing_stage` | Identifie l'étape de traitement |

Les colonnes techniques issues du nettoyage sont conservées afin de maintenir la traçabilité des contrôles précédents.

Les jeux détaillés obtenus sont :
- `store_sales` : 667 579 lignes et 80 colonnes
- `inventory` : 23 249 101 lignes et 20 colonnes

### 3.2 Agrégation des ventes par magasin

**Question métier : quel est le chiffre d'affaires de chaque magasin et quels magasins réalisent les meilleures performances ?**

Source : `store_sales`

Clé de regroupement :
- `ss_store_sk`

Mesures calculées :
- somme de `ss_net_paid_inc_tax` : montant net payé TTC
- somme de `ss_net_paid` : montant net payé hors taxe
- somme de `ss_net_profit` : bénéfice net
- somme de `ss_quantity` : quantités vendues
- nombre de lignes de vente
- nombre distinct de tickets

**Granularité : une ligne par magasin.**

Résultat obtenu : **12 lignes et 11 colonnes**.

Les résultats permettent de comparer les magasins selon leur chiffre d'affaires TTC, leurs quantités vendues et leur bénéfice net.

Exemples issus de l'exécution :

| Magasin | Chiffre d'affaires TTC | Montant net HT | Quantités vendues |
|---:|---:|---:|---:|
| 7 | 103 384 198,80 | 98 950 137,76 | 2 915 053 |
| 4 | 101 130 648,13 | 96 770 105,59 | 2 832 572 |
| 9 | 101 109 360,86 | 96 748 356,68 | 2 830 684 |
| 0 | 101 047 840,24 | 96 727 851,94 | 2 830 581 |
| 8 | 100 916 146,68 | 96 578 622,89 | 2 821 869 |

Le magasin 7 présente le chiffre d'affaires TTC le plus élevé parmi les résultats affichés.

Attention : les montants de bénéfice net agrégés affichés pour les magasins sont négatifs. Il ne faut pas en déduire immédiatement une anomalie du traitement. Les règles de calcul et la signification métier de `ss_net_profit` doivent être vérifiées avant de tirer une conclusion financière.

### 3.3 Agrégation des ventes par magasin et date

**Question métier : comment évoluent le chiffre d'affaires, les quantités vendues et le bénéfice d'un magasin au fil des dates ?**

Source : `store_sales`

Clés de regroupement :
- `ss_store_sk` 
- `ss_sold_date_sk`

Mesures calculées :
- somme de `ss_net_paid_inc_tax`
- somme de `ss_net_paid`
- somme de `ss_net_profit` 
- somme de `ss_quantity` 
- nombre de lignes de vente
- nombre distinct de tickets

**Granularité : une ligne par magasin et date de vente.**

Résultat obtenu : **21 430 lignes et 12 colonnes**.

La clé `date_sk` reste une clé technique de dimension. Elle devra être reliée à `date_dim` pour obtenir des dates calendaires et effectuer des analyses par jour, mois, trimestre ou année.

Ce jeu permet notamment de suivre l'évolution du chiffre d'affaires d'un magasin et de comparer ses performances entre périodes.

### 3.4 Agrégation des ventes par article et date

**Questions métier : quels produits se vendent le plus rapidement ? Quels produits connaissent une baisse des ventes ?**

Source : `store_sales`

Clés de regroupement :
- `ss_item_sk` 
- `ss_sold_date_sk`

Mesures calculées :
- somme de `ss_net_paid_inc_tax` 
- somme de `ss_net_paid` 
- somme de `ss_net_profit` 
- somme de `ss_quantity` 
- nombre de lignes de vente 
- nombre distinct de couples magasin/ticket

**Granularité : une ligne par article et date de vente.**

Résultat obtenu : **565 428 lignes et 12 colonnes**.

Ce jeu permet de :
- classer les articles selon les quantités vendues 
- comparer le chiffre d'affaires généré par article
- suivre les ventes d'un produit au fil des dates 
- préparer une analyse des tendances commerciales

Les résultats affichés montrent notamment que l'article `10003` atteint 845 unités vendues à la date technique `38509`, sur 13 lignes de vente.

Pour identifier les produits qui connaissent une baisse des ventes, il faudra enrichir ce jeu avec la dimension calendrier et comparer des périodes successives. L'agrégation actuelle fournit les mesures nécessaires, mais ne calcule pas encore directement un taux de baisse.

### 3.5 Agrégation du stock par article et date

**Question métier : quelle est la quantité totale de stock observée pour chaque article et chaque date ?**

Source : `inventory`

Clés initiales :
- `inv_item_sk` 
- `inv_date_sk`

Mesures calculées :
- somme de `inv_quantity_on_hand` 
- nombre d'entrepôts distincts 
- nombre d'enregistrements d'inventaire

**Granularité : une ligne par article et date, tous entrepôts confondus.**

Résultat obtenu : **4 661 999 lignes et 9 colonnes**.

Le stock est agrégé sur les entrepôts avant la jointure avec les ventes. Cette opération produit une clé unique `(item_sk, date_sk)`.

La somme suppose que les quantités des différents entrepôts correspondent à des stocks distincts et additionnables.

Ce jeu permet de consulter les quantités de stock observées par article et date. Il ne permet pas encore, à lui seul, de déterminer les ruptures de stock : il faut notamment définir un seuil de stock minimum et vérifier la couverture des données.

## 4. Jointure vérifiée : ventes et stock par article/date

### 4.1 Sources, clés et nature de la jointure

Deux jeux agrégés sont utilisés :

- Ventes : agrégées par `ss_item_sk` et `ss_sold_date_sk`, puis harmonisées en `item_sk` et `date_sk`.
- Stock : agrégé par `inv_item_sk` et `inv_date_sk`, puis harmonisé en `item_sk` et `date_sk`.

Les clés de jointure sont :

`(item_sk, date_sk)`

Le type de jointure utilisé est une jointure gauche (`left`), les ventes constituant le jeu de référence.

### 4.2 Cardinalité attendue

Après agrégation, chaque côté doit contenir au plus une ligne par couple article/date.

Le script vérifie l'unicité des clés des deux jeux avant la jointure.

La relation attendue est **1 vers 0 ou 1** depuis une ligne de ventes agrégées vers le stock correspondant.

Une absence de stock ne supprime pas la ligne de ventes grâce à la jointure gauche.

Résultat des contrôles d'unicité :
- Clés dupliquées côté ventes : 0.
- Clés dupliquées côté stock : 0.

### 4.3 Résultats de la jointure

| Indicateur | Résultat |
|---|---:|
| Lignes avant jointure | 565 428 |
| Lignes après jointure | 565 428 |
| Lignes sans correspondance stock | 484 701 |
| Lignes avec correspondance stock | 80 727 |

Le nombre de lignes est identique avant et après la jointure. Celle-ci n'a donc ni multiplié ni supprimé les lignes agrégées de ventes.

Environ **85,72 %** des couples article/date de ventes ne possèdent pas de correspondance dans le jeu de stock agrégé. Environ **14,28 %** possèdent une correspondance.

### 4.4 Interprétation des non-correspondances

Le nombre important de lignes sans correspondance nécessite une analyse complémentaire.

Plusieurs explications sont possibles :
- l'article vendu n'est pas présent dans le fichier d'inventaire 
- la date de vente ne correspond à aucune date d'observation du stock 
- les périodes couvertes par les deux sources sont différentes 
- certaines clés article ou date ne sont pas communes aux deux jeux

Une absence de correspondance ne signifie pas automatiquement une rupture de stock.

Il est donc nécessaire de vérifier la couverture temporelle et les clés communes avant de tirer une conclusion métier sur les niveaux de stock.

### 4.5 Limites d'interprétation

La jointure compare les ventes d'un article à une date au stock total de cet article à cette date, tous entrepôts confondus.

Elle ne permet pas d'attribuer le stock à un magasin, car aucune relation magasin-entrepôt vérifiée n'est disponible.

Le résultat ne doit donc pas être interprété comme le stock disponible dans le magasin ayant réalisé la vente.

De plus, les deux sources ne garantissent pas nécessairement que le stock observé correspond à l'instant précis de la vente.

## 5. Correspondance avec les questions métier du Jour 1

Le tableau suivant distingue les questions auxquelles les jeux produits répondent directement de celles qui nécessitent encore des transformations ou des sources complémentaires.

| Question métier | Jeu ou source disponible | État après les étapes 5 et 6 |
|---|---|---|
| Quels produits risquent d'être en rupture de stock ? | `inventory_by_item_date` et `sales_inventory_by_item_date` | Partiellement préparé. Les quantités sont disponibles, mais la couverture de jointure est faible et aucun seuil de rupture n'est défini. |
| Quels produits se vendent le plus rapidement ? | `sales_by_item_date` | Données préparées. Un classement par quantité vendue est possible ; une notion de vitesse nécessite une période d'analyse définie. |
| Quels fichiers présentent des données manquantes ? | Résultats de l'étape 4, indicateurs conservés dans les jeux détaillés | Contrôle réalisé à l'étape 4. Les jeux détaillés conservent les indicateurs de qualité. |
| Quelles sources doivent être intégrées quotidiennement ? | Sources Bronze et sorties des étapes précédentes | Non résolu par ce script. Cela relève de la conception et de l'orchestration du pipeline quotidien. |
| Quel est le chiffre d'affaires de mon magasin ? | `sales_by_store` et `sales_by_store_date` | Répondu au niveau des clés techniques de magasin, avec les montants TTC et HT. |
| Quels produits sont les plus vendus dans mon magasin ? | `sales_by_item_date` | Partiellement préparé. Le jeu est agrégé tous magasins confondus ; une agrégation par magasin et article sera nécessaire. |
| Quels magasins réalisent le meilleur chiffre d'affaires ? | `sales_by_store` | Répondu. Le classement par chiffre d'affaires TTC est disponible. |
| Quels produits connaissent une baisse des ventes ? | `sales_by_item_date` | Données préparées, mais l'analyse de baisse nécessite un enrichissement calendrier et une comparaison de périodes. |

Les étapes 5 et 6 répondent donc directement à la question du chiffre d'affaires par magasin et au classement des magasins. Elles préparent également les analyses par produit, les tendances de ventes et le suivi des stocks, sans prétendre résoudre les questions qui nécessitent encore des dimensions ou des règles métier supplémentaires.

## 6. Étape 6 – Jeux de données produits

Les sept jeux sont enregistrés au format Parquet avec compression Snappy.

Répertoire de sortie :

`data/silver-transformed/`

| Répertoire | Contenu | Granularité |
|---|---|---|
| `store_sales/` | Ventes nettoyées détaillées avec provenance | Ligne de vente |
| `inventory/` | Stock nettoyé détaillé avec provenance | Article / entrepôt / date |
| `sales_by_store/` | Agrégats de ventes | Magasin |
| `sales_by_store_date/` | Agrégats de ventes | Magasin / date |
| `sales_by_item_date/` | Agrégats de ventes | Article / date |
| `inventory_by_item_date/` | Stock agrégé tous entrepôts | Article / date |
| `sales_inventory_by_item_date/` | Ventes enrichies du stock agrégé | Article / date |

Seuls les domaines effectivement disponibles et traités sont créés. Aucun jeu `products`, `stores`, `customers` ou `returns` n'est fabriqué sans source correspondante.

### 6.1 Convention de nommage

- Répertoires en minuscules et `snake_case`.
- Colonnes techniques de provenance préfixées par `_`.
- Clés de dimension conservées avec leur suffixe `_sk` dans les jeux détaillés.
- Dans les jeux agrégés, les clés sont harmonisées en `store_sk`, `item_sk` et `date_sk` selon le besoin.
- Mesures agrégées nommées explicitement (`total_...`, `number_of_...`).
- Indicateurs de contrôle préfixés par `flag_`.

### 6.2 Bilan des schémas et volumes

| Jeu de données | Nombre de lignes | Nombre de colonnes |
|---|---:|---:|
| `store_sales` | 667 579 | 80 |
| `inventory` | 23 249 101 | 20 |
| `sales_by_store` | 12 | 11 |
| `sales_by_store_date` | 21 430 | 12 |
| `sales_by_item_date` | 565 428 | 12 |
| `inventory_by_item_date` | 4 661 999 | 9 |
| `sales_inventory_by_item_date` | 565 428 | 16 |

Les nombres de colonnes incluent les informations de provenance et de granularité lorsqu'elles sont ajoutées par le script.

### 6.3 Structure fonctionnelle des jeux agrégés

#### `sales_by_store`

| Colonne | Signification |
|---|---|
| `store_sk` | Clé du magasin |
| `total_revenue_inc_tax` | Chiffre d'affaires net TTC |
| `total_net_paid` | Montant net payé hors taxe |
| `total_net_profit` | Bénéfice net agrégé |
| `total_quantity_sold` | Quantités vendues |
| `number_of_sales_lines` | Nombre de lignes de vente |
| `number_of_tickets` | Nombre de tickets distincts |
| `_grain` | Description de la granularité |
| `_source_dataset` | Source métier |
| `_source_original_file` | Fichier original |
| `_processing_stage` | Étape de traitement |

#### `sales_by_store_date`

| Colonne | Signification |
|---|---|
| `store_sk` | Clé du magasin |
| `date_sk` | Clé de la date de vente |
| `total_revenue_inc_tax` | Montant net payé TTC |
| `total_net_paid` | Montant net payé hors taxe |
| `total_net_profit` | Bénéfice net |
| `total_quantity_sold` | Quantités vendues |
| `number_of_sales_lines` | Nombre de lignes de vente |
| `number_of_tickets` | Nombre de tickets distincts |
| `_grain` | Description de la granularité |
| `_source_dataset` | Source métier |
| `_source_original_file` | Fichier original |
| `_processing_stage` | Étape de traitement |

#### `sales_by_item_date`

| Colonne | Signification |
|---|---|
| `item_sk` | Clé de l'article |
| `date_sk` | Clé de la date de vente |
| `total_revenue_inc_tax` | Montant net payé TTC |
| `total_net_paid` | Montant net payé hors taxe |
| `total_net_profit` | Bénéfice net |
| `total_quantity_sold` | Quantités vendues |
| `number_of_sales_lines` | Nombre de lignes de vente |
| `number_of_tickets` | Nombre de couples magasin/ticket distincts |
| `_grain` | Description de la granularité |
| `_source_dataset` | Source métier |
| `_source_original_file` | Fichier original |
| `_processing_stage` | Étape de traitement |

#### `inventory_by_item_date`

| Colonne | Signification |
|---|---|
| `item_sk` | Clé de l'article |
| `date_sk` | Clé de la date |
| `total_quantity_on_hand` | Quantité totale observée tous entrepôts |
| `number_of_warehouses` | Nombre d'entrepôts distincts |
| `number_of_inventory_records` | Nombre d'enregistrements source |
| `_grain` | Description de la granularité |
| `_source_dataset` | Source métier |
| `_source_original_file` | Fichier original |
| `_processing_stage` | Étape de traitement |

#### `sales_inventory_by_item_date`

Ce jeu reprend les mesures de `sales_by_item_date` et ajoute :

- `total_quantity_on_hand` ;
- `number_of_warehouses` ;
- `number_of_inventory_records` ;
- `flag_inventory_not_matched`.

Cet indicateur permet d'identifier les couples article/date de ventes sans correspondance dans le stock.

Les types physiques exacts sont ceux produits par Spark à partir des types de l'étape 4 et des fonctions d'agrégation.

## 7. Contrôles après écriture

### 7.1 Vérification des volumes

Pour chaque jeu, le script compare le nombre de lignes attendu au nombre de lignes relu depuis le répertoire Parquet.

| Jeu | Lignes attendues | Lignes relues | Résultat |
|---|---:|---:|---|
| `store_sales` | 667 579 | 667 579 | Conforme |
| `inventory` | 23 249 101 | 23 249 101 | Conforme |
| `sales_by_store` | 12 | 12 | Conforme |
| `sales_by_store_date` | 21 430 | 21 430 | Conforme |
| `sales_by_item_date` | 565 428 | 565 428 | Conforme |
| `inventory_by_item_date` | 4 661 999 | 4 661 999 | Conforme |
| `sales_inventory_by_item_date` | 565 428 | 565 428 | Conforme |

Les sept jeux ont été relus sans différence de comptage après leur écriture.

### 7.2 Vérification des schémas

Les nombres de colonnes relus sont :

- `store_sales` : 80 colonnes 
- `inventory` : 20 colonnes 
- `sales_by_store` : 11 colonnes 
- `sales_by_store_date` : 12 colonnes 
- `sales_by_item_date` : 12 colonnes 
- `inventory_by_item_date` : 9 colonnes 
- `sales_inventory_by_item_date` : 16 colonnes

Le script compare également les noms et l'ordre des colonnes après relecture.

### 7.3 Contrôle de la jointure

Les contrôles de cardinalité ont donné les résultats suivants :

- aucune clé dupliquée côté ventes agrégées 
- aucune clé dupliquée côté stock agrégé 
- 565 428 lignes avant jointure 
- 565 428 lignes après jointure

La jointure est donc conforme à la cardinalité attendue.

Le nombre élevé de couples sans correspondance reste toutefois un point de vigilance métier.

### 7.4 Avertissement Spark

Pendant l'exécution, Spark a affiché le message :

`WARN SparkStringUtils: Truncated the string representation of a plan since it was too large`

Cet avertissement indique que Spark a raccourci l'affichage textuel d'un plan d'exécution trop volumineux.

Il ne constitue pas une erreur bloquante. Le traitement s'est terminé avec le message `Étapes 5 et 6 terminées avec succès`, et les sept jeux ont été écrits puis relus avec des volumes identiques.

## 8. Limites et évolutions possibles

### 8.1 Enrichissement par les dimensions

Si les dimensions correspondantes sont disponibles dans Bronze et que leurs clés sont vérifiées, des enrichissements pourront être ajoutés :

| Dimension | Apport attendu |
|---|---|
| `item.dat` | Attributs et libellés des produits |
| `date_dim.dat` | Dates calendaires et périodes |
| `store.dat` | Attributs et noms des magasins |
| `warehouse.dat` | Informations sur les entrepôts |

Avant toute jointure dimensionnelle, il faudra :
- vérifier l'unicité de la clé côté dimension 
- mesurer les clés non rapprochées 
- comparer les nombres de lignes avant et après jointure 
- analyser les éventuelles correspondances multiples

Aucune relation magasin-entrepôt n'est supposée dans le présent traitement.

### 8.2 Analyse des ruptures de stock

Pour répondre précisément à la question des risques de rupture, il faudra :
- vérifier la couverture des dates entre ventes et inventaire 
- étudier les 484 701 couples article/date sans correspondance 
- définir un seuil métier de stock minimum 
- comparer les quantités disponibles aux ventes et à leur évolution 
- intégrer les informations d'entrepôt et, si possible, la relation avec les magasins

L'absence de correspondance ne doit pas être assimilée à une quantité nulle.

### 8.3 Analyse des produits en baisse

Pour identifier les produits dont les ventes diminuent, il faudra :
- enrichir `date_sk` avec les dates calendaires 
- définir des périodes comparables 
- agréger les quantités par période 
- calculer les écarts et taux d'évolution 
- distinguer les baisses ponctuelles des tendances durables

### 8.4 Doublons potentiels des ventes

À l'étape 4, 8 174 lignes appartenant à des groupes de doublons potentiels ont été conservées pour revue.

Ces lignes sont donc présentes dans les jeux détaillés et prises en compte dans les agrégations actuelles.

Avant de considérer les montants et quantités agrégés comme des indicateurs définitifs, il faudra examiner ces groupes et déterminer si certaines lignes représentent des doublons réels ou des ventes distinctes.

Aucune suppression automatique n'a été réalisée dans les étapes 5 et 6.

## 9. Conclusion

Les étapes 5 et 6 ont été exécutées avec succès.

Les données nettoyées de l'étape 4 ont été transformées en **sept jeux Parquet exploitables** :

- deux jeux détaillés conservant les données nettoyées 
- une agrégation des ventes par magasin 
- une agrégation des ventes par magasin et date 
- une agrégation des ventes par article et date 
- une agrégation du stock par article et date 
- un jeu enrichi rapprochant les ventes et le stock à une granularité commune

Les contrôles après écriture confirment que les sept jeux ont été relus avec les mêmes nombres de lignes que ceux annoncés à l'écriture.

Les transformations répondent directement à la question du chiffre d'affaires par magasin et permettent de classer les magasins. Elles préparent également les analyses par produit, les tendances de ventes et le suivi des stocks.

La jointure ventes-stock conserve les 565 428 lignes agrégées de ventes, sans multiplication ni perte de lignes. Cependant, 484 701 couples article/date ne trouvent pas de correspondance dans l'inventaire. Cette situation devra être étudiée avant toute interprétation en termes de disponibilité ou de rupture de stock.

Enfin, les indicateurs financiers et commerciaux devront être interprétés en tenant compte des doublons potentiels conservés à l'étape 4 et des limites de rapprochement entre les sources.

Les jeux produits constituent ainsi une base structurée pour les analyses métier ultérieures et les prochaines étapes de la plateforme Retail Intelligence.