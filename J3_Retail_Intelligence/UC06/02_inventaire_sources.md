# Étape 2 : Inventaire technique des sources

## 1. Présentation des sources retenues

Dans le cadre du projet **Retail Intelligence Platform**, deux sources ont été sélectionnées parmi les fichiers disponibles du jeu de données TPCX-BB version 1.7.0.

Le choix repose sur les besoins métier prioritaires identifiés au Jour 1 :

- Le pilotage du chiffre d'affaires et des ventes par magasin.
- Le suivi des quantités disponibles et l'identification des risques de rupture de stock.
- La préparation d'indicateurs permettant d'analyser les performances commerciales et les stocks.

Les deux sources retenues sont :

- `store_sales.dat` : données de ventes réalisées en magasin.
- `inventory.dat` : données de stock par produit, entrepôt et date.

Ces fichiers appartiennent au jeu de données principal `data/`. Ils sont retenus afin de conserver la cohérence avec les fichiers déjà transférés dans la zone Raw lors du Jour 2.

## 2. Inventaire technique des sources

| Information | Source 1 : store_sales.dat | Source 2 : inventory.dat |
|---|---|---|
| Nom réel du fichier | `store_sales.dat` | `inventory.dat` |
| Emplacement | `data/store_sales/` | `data/inventory/` |
| Format | DAT (texte délimité) | DAT (texte délimité) |
| Taille | 92 764 700 octets | 424 943 678 octets |
| Nombre de lignes | 667 579 | 23 255 100 |
| Nombre de colonnes | 23 | 4 |
| Séparateur | `\|` | `\|` |
| En-tête | Absent | Absent |
| Colonnes principales | `ss_sold_date_sk`, `ss_item_sk`, `ss_store_sk`, `ss_ticket_number`, `ss_quantity`, `ss_net_paid` | `inv_date_sk`, `inv_item_sk`, `inv_warehouse_sk`, `inv_quantity_on_hand` |
| Types observés | BIGINT, INTEGER, DECIMAL(7,2) | BIGINT, INTEGER |
| Clé candidate | `ss_sold_date_sk` + `ss_store_sk` + `ss_ticket_number` + `ss_item_sk` (non unique) | `inv_date_sk` + `inv_item_sk` + `inv_warehouse_sk` (unique sur les données contrôlées) |
| Granularité | Ligne de vente d'un article associé à un ticket, un magasin et une date | Quantité d'un article dans un entrepôt à une date donnée |
| Anomalies identifiées | 1 139 valeurs nulles réparties sur 4 colonnes ; 4 038 groupes en doublon sur la clé candidate complète | 5 999 valeurs nulles dans `inv_quantity_on_hand` |
| Quantités négatives | Aucune détectée dans `ss_quantity` | Aucune détectée dans `inv_quantity_on_hand` |

*Remarque : les volumes correspondent à l'inventaire initial des fichiers. Ils sont à considérer comme les volumes de référence de cette étape.*

## 3. Analyse détaillée des sources

### 3.1. Source 1 : store_sales.dat

Cette source contient les transactions de ventes réalisées dans les magasins.

Elle comporte 23 colonnes décrivant notamment la date de vente, le produit, le client, le magasin, les quantités vendues, les prix et les montants financiers.

Les colonnes particulièrement importantes pour les analyses métier sont :

- `ss_sold_date_sk` : identifiant de la date de vente.
- `ss_item_sk` : identifiant du produit vendu.
- `ss_store_sk` : identifiant du magasin.
- `ss_ticket_number` : numéro du ticket.
- `ss_quantity` : quantité vendue.
- `ss_net_paid` : montant net payé.
- `ss_net_profit` : bénéfice net associé à la vente.

Les types observés avec PySpark correspondent aux types attendus dans le schéma TPCX-BB :

- Identifiants : BIGINT.
- Quantité : INTEGER.
- Montants financiers : DECIMAL(7,2).

**Granularité**

Une ligne représente une ligne de vente d'un article associé à un ticket, un magasin et une date.

**Clé candidate et contrôle des doublons**

Une première clé candidate composée de `ss_item_sk` et `ss_ticket_number` avait été testée. Elle présentait 4 038 groupes en doublon.

Un contrôle complémentaire a été réalisé avec une clé plus complète :

`ss_sold_date_sk + ss_store_sk + ss_ticket_number + ss_item_sk`

Le résultat fait apparaître :

- 4 038 groupes en doublon.
- 8 174 lignes appartenant à ces groupes en doublon.

La combinaison testée ne constitue donc pas une clé unique sur les données observées. Elle doit être considérée comme une clé candidate non validée.

Ces doublons devront être analysés avant de décider d'une éventuelle déduplication. Il ne faut pas supprimer automatiquement ces lignes, car elles peuvent correspondre à des particularités du jeu de données ou à des enregistrements répétés qu'il convient de comprendre.

**Valeurs nulles**

Les contrôles Spark ont identifié les valeurs nulles suivantes :

| Colonne | Nombre de valeurs nulles | Pourcentage |
|---|---:|---:|
| `ss_cdemo_sk` | 238 | 0,0357 % |
| `ss_hdemo_sk` | 295 | 0,0442 % |
| `ss_addr_sk` | 448 | 0,0671 % |
| `ss_promo_sk` | 158 | 0,0237 % |
| **Total** | **1 139** | |

Les autres colonnes ne présentent pas de valeurs nulles dans le contrôle effectué.

Les valeurs manquantes concernent principalement des informations démographiques, d'adresse et de promotion. Elles ne doivent pas être remplacées automatiquement par zéro : leur signification métier doit être vérifiée avant le nettoyage.

**Autres contrôles**

Aucune quantité négative n'a été détectée dans `ss_quantity`.

Cette source permettra notamment de calculer :

- Le chiffre d'affaires par magasin.
- Le chiffre d'affaires par produit.
- Les produits les plus vendus.
- L'évolution des ventes dans le temps.
- Les produits dont les ventes diminuent.

### 3.2. Source 2 : inventory.dat

Cette source contient les quantités disponibles par article, entrepôt et date.

Elle comporte quatre colonnes :

- `inv_date_sk` : identifiant de la date.
- `inv_item_sk` : identifiant du produit.
- `inv_warehouse_sk` : identifiant de l'entrepôt.
- `inv_quantity_on_hand` : quantité disponible en stock.

Les types observés avec PySpark correspondent aux types attendus :

- Identifiants : BIGINT.
- Quantité en stock : INTEGER.

**Granularité**

Une ligne représente la quantité disponible d'un produit dans un entrepôt à une date donnée.

**Clé candidate et contrôle des doublons**

La clé candidate retenue est la combinaison :

`inv_date_sk + inv_item_sk + inv_warehouse_sk`

Le contrôle effectué avec PySpark n'a détecté aucun groupe en doublon sur cette combinaison.

Cette clé candidate est donc unique sur les données contrôlées.

**Valeurs nulles**

Les contrôles Spark ont identifié :

| Colonne | Nombre de valeurs nulles | Pourcentage |
|---|---:|---:|
| `inv_date_sk` | 0 | 0 % |
| `inv_item_sk` | 0 | 0 % |
| `inv_warehouse_sk` | 0 | 0 % |
| `inv_quantity_on_hand` | 5 999 | 0,0258 % |

Les 5 999 valeurs nulles concernent la quantité disponible en stock.

Cette anomalie est importante pour les analyses de disponibilité. Une quantité inconnue ne doit pas être assimilée à un stock nul sans règle métier explicite.

**Autres contrôles**

Aucune quantité négative n'a été détectée dans `inv_quantity_on_hand`.

Cette source permettra notamment de :

- Suivre les quantités disponibles par produit et entrepôt.
- Identifier les stocks faibles.
- Comparer les stocks dans le temps.
- Préparer des indicateurs de risque de rupture.

## 4. Schémas techniques observés

Les fichiers ont été lus avec PySpark en utilisant un schéma défini explicitement à partir de la documentation TPCX-BB version 1.7.0.

Les fichiers étant dépourvus d'en-tête, les noms des colonnes ont été associés à leur position dans chaque fichier.

### 4.1. Schéma de store_sales.dat

| Position | Colonne | Type |
|---:|---|---|
| 1 | `ss_sold_date_sk` | BIGINT |
| 2 | `ss_sold_time_sk` | BIGINT |
| 3 | `ss_item_sk` | BIGINT |
| 4 | `ss_customer_sk` | BIGINT |
| 5 | `ss_cdemo_sk` | BIGINT |
| 6 | `ss_hdemo_sk` | BIGINT |
| 7 | `ss_addr_sk` | BIGINT |
| 8 | `ss_store_sk` | BIGINT |
| 9 | `ss_promo_sk` | BIGINT |
| 10 | `ss_ticket_number` | BIGINT |
| 11 | `ss_quantity` | INTEGER |
| 12 | `ss_wholesale_cost` | DECIMAL(7,2) |
| 13 | `ss_list_price` | DECIMAL(7,2) |
| 14 | `ss_sales_price` | DECIMAL(7,2) |
| 15 | `ss_ext_discount_amt` | DECIMAL(7,2) |
| 16 | `ss_ext_sales_price` | DECIMAL(7,2) |
| 17 | `ss_ext_wholesale_cost` | DECIMAL(7,2) |
| 18 | `ss_ext_list_price` | DECIMAL(7,2) |
| 19 | `ss_ext_tax` | DECIMAL(7,2) |
| 20 | `ss_coupon_amt` | DECIMAL(7,2) |
| 21 | `ss_net_paid` | DECIMAL(7,2) |
| 22 | `ss_net_paid_inc_tax` | DECIMAL(7,2) |
| 23 | `ss_net_profit` | DECIMAL(7,2) |

### 4.2. Schéma de inventory.dat

| Position | Colonne | Type |
|---:|---|---|
| 1 | `inv_date_sk` | BIGINT |
| 2 | `inv_item_sk` | BIGINT |
| 3 | `inv_warehouse_sk` | BIGINT |
| 4 | `inv_quantity_on_hand` | INTEGER |

*Remarque : le schéma affiché par Spark indique `nullable=true` pour les colonnes. Cela correspond à la métadonnée de nullabilité du DataFrame et ne signifie pas que toutes les lignes contiennent des valeurs nulles. Les contrôles de données ont été réalisés séparément pour mesurer les valeurs manquantes réellement présentes.*

## 5. Questions techniques

### Question 1. Les fichiers sont-ils structurés, semi-structurés ou non structurés ?

Les deux fichiers sont des **données structurées**.

Ils possèdent un nombre fixe de colonnes, un ordre défini et un séparateur commun (`|`). Leur structure est documentée dans le modèle de données TPCX-BB version 1.7.0.

Ils sont stockés sous forme de fichiers texte DAT, sans ligne d'en-tête.

### Question 2. Les colonnes sont-elles correctement typées ?

Oui. Les schémas ont été définis explicitement avec PySpark à partir de la documentation TPCX-BB.

Les types observés correspondent aux types attendus :

- BIGINT pour les identifiants.
- INTEGER pour les quantités.
- DECIMAL(7,2) pour les montants financiers de `store_sales.dat`.

La lecture des deux fichiers et la vérification de leurs schémas ont été réalisées avec succès.

Il reste toutefois nécessaire de contrôler les valeurs métier et les éventuelles conversions incorrectes lors des traitements futurs.

### Question 3. Certaines colonnes contiennent-elles des valeurs nulles ?

Oui.

Pour `store_sales.dat`, 1 139 valeurs nulles ont été détectées :

- 238 dans `ss_cdemo_sk`.
- 295 dans `ss_hdemo_sk`.
- 448 dans `ss_addr_sk`.
- 158 dans `ss_promo_sk`.

Pour `inventory.dat`, 5 999 valeurs nulles ont été détectées dans `inv_quantity_on_hand`.

Ces valeurs seront conservées à ce stade. Leur traitement sera défini lors de la transformation vers la couche Silver, en fonction de leur signification métier.

### Question 4. Les identifiants sont-ils uniques lorsque cela est attendu ?

Pour `inventory.dat`, la combinaison `inv_date_sk`, `inv_item_sk` et `inv_warehouse_sk` ne présente aucun groupe en doublon. Elle constitue une clé candidate unique sur les données contrôlées.

Pour `store_sales.dat`, la combinaison `ss_sold_date_sk`, `ss_store_sk`, `ss_ticket_number` et `ss_item_sk` présente 4 038 groupes en doublon, représentant 8 174 lignes. Cette combinaison ne garantit donc pas l'unicité des enregistrements.

Une investigation complémentaire sera nécessaire avant de définir une règle de déduplication. Les doublons ne seront pas supprimés sans justification métier.

### Question 5. La granularité est-elle connue ?

Oui.

- `store_sales.dat` : une ligne représente une ligne de vente d'un article associé à un ticket, un magasin et une date.
- `inventory.dat` : une ligne représente la quantité disponible d'un article dans un entrepôt à une date donnée.

La connaissance de cette granularité est indispensable pour éviter les erreurs d'agrégation lors des analyses.

### Question 6. Les données sont-elles adaptées aux questions métier sélectionnées au Jour 1 ?

Oui, les deux sources sont complémentaires et répondent à plusieurs besoins métier prioritaires.

| Besoin métier | Source mobilisée | Pertinence |
|---|---|---|
| Calculer le chiffre d'affaires d'un magasin | `store_sales.dat` | Adaptée |
| Identifier les magasins réalisant le meilleur chiffre d'affaires | `store_sales.dat` | Adaptée |
| Identifier les produits les plus vendus | `store_sales.dat` | Adaptée |
| Identifier les produits dont les ventes diminuent | `store_sales.dat` | Adaptée, avec une analyse temporelle |
| Identifier les produits présentant un risque de rupture | `inventory.dat` | Adaptée, avec des seuils métier à définir |
| Identifier les produits vendus rapidement | `store_sales.dat` | Adaptée, en combinant les ventes et les périodes |
| Contrôler les données manquantes | Les deux sources | Adaptées |
| Définir les sources à intégrer quotidiennement | Les deux sources | Adaptées, sous réserve de définir les règles d'alimentation |

Certaines analyses nécessiteront des informations complémentaires. Par exemple, les noms des produits, les catégories et les autres attributs descriptifs devront être récupérés dans des tables de référence comme `item.dat`. De même, l'analyse détaillée des dates pourra nécessiter l'utilisation de `date_dim.dat`.

## 6. Synthèse des anomalies et des contrôles réalisés

| Contrôle | store_sales.dat | inventory.dat |
|---|---|---|
| Lecture PySpark | Réussie | Réussie |
| Conformité du nombre de colonnes | 23 colonnes | 4 colonnes |
| Types conformes au schéma attendu | Oui | Oui |
| Valeurs nulles | 1 139 | 5 999 |
| Doublons sur la clé candidate testée | 4 038 groupes | 0 groupe |
| Lignes concernées par les doublons | 8 174 | 0 |
| Quantités négatives | 0 | 0 |

À l'issue de cette étape, les constats principaux sont les suivants :

- Les deux fichiers sont lisibles et leur structure est conforme au schéma attendu.
- Des valeurs nulles sont présentes dans les deux sources.
- La clé candidate de la table de stock est unique sur les données contrôlées.
- La clé candidate testée pour les ventes n'est pas unique.
- Aucune quantité négative n'a été détectée dans les deux sources.

Aucune opération de nettoyage ou de suppression de doublons n'a encore été effectuée. Les anomalies sont documentées afin de conserver la traçabilité des données avant leur transformation.

## 7. Conclusion

L'inventaire technique confirme que `store_sales.dat` et `inventory.dat` sont deux sources structurées pertinentes pour le projet Retail Intelligence Platform.

`store_sales.dat` constitue la source principale pour l'analyse des ventes, du chiffre d'affaires et des performances commerciales par magasin et par produit.

`inventory.dat` constitue la source principale pour le suivi des stocks et l'identification des risques de rupture.

Les schémas ont été définis et vérifiés avec PySpark. Les premiers contrôles ont permis d'identifier des valeurs nulles et des groupes de doublons, qui devront être traités ou justifiés lors de la prochaine étape.

Cet inventaire technique actualisé constitue une base pour la transformation des données vers la couche **Silver**, où seront réalisées les opérations de nettoyage, de validation et de standardisation avant la construction des indicateurs métier dans la couche **Gold**.