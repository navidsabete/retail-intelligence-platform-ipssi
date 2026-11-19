# Étape 3 : Exploration des données avec PySpark

## 1. Objectif de l'exploration

Après avoir réalisé l'inventaire technique des sources à l'étape 2, une exploration approfondie des deux fichiers retenus a été effectuée avec PySpark.

Cette étape a pour objectif de vérifier la structure réelle des données, d'examiner leur contenu et d'identifier les éventuelles anomalies avant leur transformation dans la couche Silver.

Les deux sources explorées sont :

- `store_sales.dat` : données de ventes en magasin.
- `inventory.dat` : données de stock par produit, entrepôt et date.

L'exploration a été réalisée à partir des fichiers du jeu de données TPCX-BB version 1.7.0.

## 2. Environnement et méthode de lecture

Les fichiers ont été chargés dans des DataFrames PySpark.

La lecture a été adaptée à leur format réel :

- Format : DAT (texte délimité).
- Séparateur : `|`.
- Présence d'un en-tête : non.
- Schéma : défini explicitement à partir de la documentation TPCX-BB version 1.7.0.

L'utilisation d'un schéma explicite permet de garantir la cohérence des types de données et d'éviter les erreurs potentielles liées à l'inférence automatique.

Les deux fichiers ont été chargés avec succès.

## 3. Résultats de l'exploration

### 3.1. Source store_sales.dat

**Caractéristiques générales**

| Contrôle | Résultat |
|---|---|
| Fichier | `store_sales.dat` |
| Nombre de lignes | 667 579 |
| Nombre de colonnes | 23 |
| Lecture PySpark | Réussie |
| Affichage du schéma | Réussi |
| Affichage d'un échantillon | Réussi |
| Types observés | BIGINT, INTEGER, DECIMAL(7,2) |

**Échantillon de données**

Un échantillon de cinq lignes a été affiché avec PySpark afin de vérifier la bonne lecture des colonnes et la cohérence des valeurs.

Les premiers enregistrements présentent notamment des identifiants de dates, de produits, de clients et de magasins, ainsi que des quantités et des montants financiers.

Les données sont correctement réparties dans les 23 colonnes attendues.

**Colonnes numériques, dates et identifiants**

Les colonnes numériques sont notamment :

- `ss_quantity` : quantité vendue.
- `ss_wholesale_cost` : coût de gros unitaire.
- `ss_list_price` : prix catalogue.
- `ss_sales_price` : prix de vente.
- `ss_ext_discount_amt` : montant total des remises.
- `ss_ext_sales_price` : montant total des ventes.
- `ss_ext_wholesale_cost` : coût de gros total.
- `ss_ext_list_price` : prix catalogue total.
- `ss_ext_tax` : montant des taxes.
- `ss_coupon_amt` : montant des coupons.
- `ss_net_paid` : montant net payé.
- `ss_net_paid_inc_tax` : montant net payé avec taxes.
- `ss_net_profit` : bénéfice net.

Les colonnes d'identification comprennent notamment :

- `ss_sold_date_sk` : identifiant de date.
- `ss_sold_time_sk` : identifiant de temps.
- `ss_item_sk` : identifiant de produit.
- `ss_customer_sk` : identifiant de client.
- `ss_store_sk` : identifiant de magasin.
- `ss_ticket_number` : numéro de ticket.

Les colonnes `ss_sold_date_sk` et `ss_sold_time_sk` sont des clés de référence temporelles et non des dates ou heures directement interprétables. Leur conversion nécessite les tables de dimension correspondantes, notamment `date_dim.dat` et `time_dim.dat`.

**Valeurs manquantes**

Le contrôle des valeurs nulles a donné les résultats suivants :

| Colonne | Valeurs nulles |
|---|---:|
| `ss_cdemo_sk` | 238 |
| `ss_hdemo_sk` | 295 |
| `ss_addr_sk` | 448 |
| `ss_promo_sk` | 158 |
| **Total** | **1 139** |

Les autres colonnes ne présentent aucune valeur nulle dans le contrôle effectué.

Les valeurs manquantes concernent principalement les informations démographiques, d'adresse et de promotion.

**Recherche de doublons**

Une clé candidate complète a été testée à partir des colonnes :

`ss_sold_date_sk + ss_store_sk + ss_ticket_number + ss_item_sk`

Résultats :

- 4 038 groupes en doublon.
- 8 174 lignes appartenant à ces groupes.

La clé candidate ne garantit donc pas l'unicité des lignes.

Une investigation complémentaire sera nécessaire pour comprendre l'origine de ces répétitions avant toute éventuelle déduplication.

**Recherche de valeurs atypiques et analyse des montants financiers**

Un contrôle des quantités négatives a été effectué sur `ss_quantity`.

Résultat : aucune quantité négative détectée.

Une analyse complémentaire des montants financiers a ensuite été réalisée à l'aide des fonctions `MIN` et `MAX` de PySpark afin d'identifier les valeurs extrêmes.

Les résultats obtenus sont les suivants :

| Colonne | Minimum | Maximum |
|---|---:|---:|
| `ss_wholesale_cost` | 1,00 | 100,00 |
| `ss_list_price` | 1,00 | 200,00 |
| `ss_sales_price` | 0,00 | 199,30 |
| `ss_ext_discount_amt` | 0,00 | 18 984,00 |
| `ss_ext_sales_price` | 0,00 | 18 745,00 |
| `ss_ext_wholesale_cost` | 1,00 | 9 997,00 |
| `ss_ext_list_price` | 1,20 | 19 814,00 |
| `ss_ext_tax` | 0,00 | 1 637,80 |
| `ss_coupon_amt` | 0,00 | 14 371,66 |
| `ss_net_paid` | 0,00 | 18 745,00 |
| `ss_net_paid_inc_tax` | 0,00 | 19 869,70 |
| `ss_net_profit` | -9 866,60 | 9 134,00 |

Les résultats montrent notamment :

- Des prix de vente pouvant être égaux à zéro.
- Des montants de ventes et de paiements pouvant être égaux à zéro.
- Des montants de remises et de coupons élevés.
- Des bénéfices nets négatifs, dont le minimum atteint -9 866,60.

Ces valeurs constituent des points de vigilance et nécessitent une analyse métier. Un bénéfice négatif n'est pas automatiquement une anomalie : il peut correspondre à une vente réalisée à perte ou à une combinaison de remises et de coûts.

**Analyse des ventes les plus déficitaires**

Une extraction des dix lignes présentant les bénéfices nets les plus faibles a été réalisée en triant `ss_net_profit` par ordre croissant.

Les résultats montrent des bénéfices compris entre -9 866,60 et -9 628,00 pour les dix premières lignes.

Quelques exemples :

| Date (clé) | Magasin | Produit | Quantité | Prix de vente unitaire | Montant des ventes | Montant net payé | Bénéfice net |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 37257 | 1 | 10003 | 100 | 7,04 | 704,00 | 70,40 | -9 866,60 |
| 37505 | 2 | 10002 | 99 | 0,00 | 0,00 | 0,00 | -9 802,98 |
| 38084 | 6 | 13546 | 98 | 4,20 | 411,60 | 4,12 | -9 730,22 |
| 37952 | 8 | 16561 | 100 | 3,61 | 361,00 | 198,55 | -9 720,45 |
| 37379 | 8 | 17405 | 100 | 1,01 | 101,00 | 101,00 | -9 688,00 |

Cette analyse met en évidence des lignes présentant un bénéfice très négatif malgré des montants de ventes relativement faibles.

Ces situations méritent une vérification particulière, notamment lorsque le montant du coût de gros est très supérieur au montant net payé.

Il est toutefois nécessaire de distinguer les valeurs atypiques des erreurs avérées : les données seules ne permettent pas encore de déterminer si ces situations résultent de remises importantes, de règles de calcul particulières ou d'anomalies dans les enregistrements.

**Analyse des écarts entre les montants financiers**

Une analyse complémentaire a été effectuée sur les dix lignes les plus déficitaires afin de comparer les montants suivants :

- `ss_ext_sales_price` : montant total des ventes.
- `ss_ext_wholesale_cost` : coût de gros total.
- `ss_ext_discount_amt` : montant total des remises.
- `ss_coupon_amt` : montant des coupons.
- `ss_net_paid` : montant net payé.
- `ss_net_profit` : bénéfice net.

Les résultats montrent des écarts importants entre les coûts, les ventes et les montants effectivement payés.

Par exemple, pour une ligne de vente :

- Quantité vendue : 100.
- Montant des ventes : 704,00.
- Coût de gros total : 9 937,00.
- Remise totale : 11 022,00.
- Montant des coupons : 633,60.
- Montant net payé : 70,40.
- Bénéfice net : -9 866,60.

Ces écarts montrent que certaines lignes présentent des montants financiers très atypiques.

Ils devront être examinés plus précisément avant toute correction. Il ne faut notamment pas supposer que les colonnes de remises, de coupons et de prix suivent une formule arithmétique simple sans vérifier les règles de calcul définies par le modèle TPCX-BB.

**Contrôle de cohérence des montants financiers**

Trois contrôles complémentaires ont été exécutés sur l'ensemble des 667 579 lignes :

| Contrôle | Nombre de lignes concernées |
|---|---:|
| Nombre total de lignes analysées | 667 579 |
| Écarts de bénéfice détectés selon la règle testée | 0 |
| Montant net supérieur au montant des ventes | 0 |
| Prix de vente unitaire égal à zéro | 3 324 |
| Montant net payé égal à zéro | 3 954 |

Les résultats indiquent que :

- Aucun écart de bénéfice n'a été détecté selon la règle de calcul utilisée dans le contrôle.
- Aucun montant net payé supérieur au montant total des ventes n'a été détecté.
- 3 324 lignes présentent un prix de vente unitaire nul.
- 3 954 lignes présentent un montant net payé nul.

Les prix de vente nuls et les montants nets nuls constituent des situations à examiner. Ils peuvent notamment être associés à des opérations promotionnelles, des gratuités ou des situations particulières de vente.

**Conclusion sur les valeurs atypiques**

L'exploration des montants financiers a permis d'identifier plusieurs points de vigilance :

- Des bénéfices nets fortement négatifs.
- Des prix de vente nuls.
- Des montants nets payés nuls.
- Des écarts importants entre les coûts de gros, les remises et les montants encaissés.

Ces constats seront conservés pour la phase de nettoyage dans la couche Silver. Aucune valeur n'a été supprimée ou corrigée à ce stade.


### 3.2. Source inventory.dat

**Caractéristiques générales**

| Contrôle | Résultat |
|---|---|
| Fichier | `inventory.dat` |
| Nombre de lignes | 23 255 100 |
| Nombre de colonnes | 4 |
| Lecture PySpark | Réussie |
| Affichage du schéma | Réussi |
| Affichage d'un échantillon | Réussi |
| Types observés | BIGINT, INTEGER |

**Échantillon de données**

Un échantillon de cinq lignes a été affiché avec PySpark.

Les premiers enregistrements présentent des identifiants de date, de produit et d'entrepôt, associés à une quantité disponible.

La structure observée correspond aux quatre colonnes attendues.

**Colonnes numériques, dates et identifiants**

Les colonnes d'identification sont :

- `inv_date_sk` : identifiant de date.
- `inv_item_sk` : identifiant de produit.
- `inv_warehouse_sk` : identifiant d'entrepôt.

La colonne numérique représentant une quantité est :

- `inv_quantity_on_hand` : quantité disponible en stock.

Comme pour les ventes, `inv_date_sk` est une clé de dimension temporelle et non une date directement exploitable. Elle pourra être associée à `date_dim.dat` pour obtenir une date calendaire.

**Valeurs manquantes**

Le contrôle des valeurs nulles a donné les résultats suivants :

| Colonne | Valeurs nulles |
|---|---:|
| `inv_date_sk` | 0 |
| `inv_item_sk` | 0 |
| `inv_warehouse_sk` | 0 |
| `inv_quantity_on_hand` | 5 999 |

Les 5 999 valeurs manquantes concernent la quantité disponible.

Cette anomalie doit être prise en compte lors du calcul des indicateurs de stock. Une quantité inconnue ne doit pas être automatiquement interprétée comme un stock nul.

**Recherche de doublons**

La clé candidate testée est :

`inv_date_sk + inv_item_sk + inv_warehouse_sk`

Résultat : aucun groupe en doublon détecté.

Cette combinaison est donc unique sur les données contrôlées.

**Recherche de valeurs atypiques**

Un contrôle des quantités négatives a été effectué sur `inv_quantity_on_hand`.

Résultat : aucune quantité négative détectée.

Les valeurs nulles restent néanmoins à examiner avant de calculer les indicateurs de disponibilité.

## 4. Synthèse des contrôles réalisés

| Contrôle | store_sales.dat | inventory.dat |
|---|---|---|
| Lecture du fichier | Réussie | Réussie |
| Affichage du schéma | Réussi | Réussi |
| Échantillon de lignes | 5 lignes affichées | 5 lignes affichées |
| Nombre d'enregistrements | 667 579 | 23 255 100 |
| Nombre de colonnes | 23 | 4 |
| Types conformes au schéma attendu | Oui | Oui |
| Valeurs nulles | 1 139 | 5 999 |
| Groupes en doublon sur la clé candidate | 4 038 | 0 |
| Lignes appartenant aux groupes en doublon | 8 174 | 0 |
| Quantités négatives | 0 | 0 |
| Valeurs financières atypiques | Oui | Non applicable |
| Prix de vente unitaire nul | 3 324 lignes | Non applicable |
| Montant net payé nul | 3 954 lignes | Non applicable |
| Bénéfice net négatif | Présent | Non applicable |

Les contrôles réalisés confirment que les deux fichiers sont correctement chargés et que leur structure correspond au schéma attendu.

L'analyse approfondie de `store_sales.dat` a également permis de mettre en évidence des situations financières atypiques, notamment des bénéfices fortement négatifs, des prix de vente nuls et des montants nets payés nuls.

Ces situations devront être étudiées avant de définir les règles de nettoyage et de transformation.

Aucune opération de suppression ou de remplacement des valeurs n'a été effectuée à cette étape.

## 5. Réponses aux questions techniques

### Question 1. Quelles colonnes sont numériques ?

Dans `store_sales.dat`, les colonnes numériques comprennent les quantités, les prix, les remises, les taxes, les montants encaissés et les bénéfices.

Les identifiants sont également stockés sous forme numérique, mais ils représentent des clés de référence et ne doivent pas être utilisés comme des mesures.

Dans `inventory.dat`, `inv_quantity_on_hand` est la mesure numérique principale. Les trois autres colonnes sont des identifiants numériques.

### Question 2. Quelles colonnes représentent des dates ?

Les colonnes temporelles sont :

- `ss_sold_date_sk` dans `store_sales.dat`.
- `ss_sold_time_sk` dans `store_sales.dat`.
- `inv_date_sk` dans `inventory.dat`.

Il s'agit de clés de référence vers des dimensions temporelles, et non de dates ou heures directement stockées sous forme lisible.

Une jointure avec les dimensions `date_dim.dat` et `time_dim.dat` permettra d'obtenir des informations calendaires exploitables.

### Question 3. Quelles colonnes sont des identifiants ?

Dans `store_sales.dat`, les identifiants comprennent notamment :

- `ss_sold_date_sk`
- `ss_sold_time_sk`
- `ss_item_sk`
- `ss_customer_sk`
- `ss_cdemo_sk`
- `ss_hdemo_sk`
- `ss_addr_sk`
- `ss_store_sk`
- `ss_promo_sk`
- `ss_ticket_number`

Dans `inventory.dat` :

- `inv_date_sk`
- `inv_item_sk`
- `inv_warehouse_sk`

### Question 4. Quels champs présentent des valeurs manquantes ?

Dans `store_sales.dat`, les valeurs manquantes sont présentes dans `ss_cdemo_sk`, `ss_hdemo_sk`, `ss_addr_sk` et `ss_promo_sk`, pour un total de 1 139 valeurs nulles.

Dans `inventory.dat`, 5 999 valeurs nulles ont été détectées dans `inv_quantity_on_hand`.

Ces valeurs devront être traitées selon leur signification métier lors de la préparation de la couche Silver.

### Question 5. Existe-t-il des doublons ?

Oui, dans `store_sales.dat`, la clé candidate testée présente 4 038 groupes en doublon, représentant 8 174 lignes.

Dans `inventory.dat`, aucun doublon n'a été détecté sur la combinaison `inv_date_sk`, `inv_item_sk` et `inv_warehouse_sk`.

Les doublons des ventes doivent être analysés avant toute suppression.

### Question 6. Certaines valeurs sont-elles incohérentes au regard de leur signification ?

Oui, plusieurs situations atypiques ont été identifiées.

Pour les deux sources, aucune quantité négative n'a été détectée.

Dans `store_sales.dat`, les contrôles financiers ont toutefois mis en évidence :

- 3 324 lignes présentant un prix de vente unitaire nul.
- 3 954 lignes présentant un montant net payé nul.
- Des bénéfices nets négatifs, avec une valeur minimale de -9 866,60.
- Des écarts importants entre les coûts de gros, les montants de vente, les remises et les montants encaissés.

L'analyse des dix lignes les plus déficitaires confirme la présence de situations qui nécessitent une investigation complémentaire.

Ces valeurs ne sont pas nécessairement erronées. Elles peuvent correspondre à des promotions, des gratuités ou à des règles particulières de calcul des prix et des remises.

Dans `inventory.dat`, les 5 999 valeurs nulles de `inv_quantity_on_hand` constituent également un point de vigilance, car elles empêchent de connaître précisément la quantité disponible pour les combinaisons concernées.

Les anomalies identifiées seront conservées et documentées avant leur traitement dans la couche Silver.

## 6. Conclusion de l'étape 3

L'exploration avec PySpark a permis de vérifier la lisibilité des deux sources retenues, leur structure, leurs types de données et leurs premiers indicateurs de qualité.

Les contrôles ont mis en évidence :

- Des valeurs manquantes dans les deux fichiers.
- Des groupes de doublons dans `store_sales.dat`.
- Une clé candidate unique pour `inventory.dat`.
- Aucune quantité négative dans les deux sources.
- Des prix de vente et des montants nets payés nuls dans certaines lignes de ventes.
- Des bénéfices nets fortement négatifs et des écarts financiers importants.
- Des clés temporelles nécessitant une association avec les dimensions correspondantes pour obtenir des dates exploitables.

L'analyse des montants financiers constitue un complément important aux contrôles structurels. Elle permet de repérer des situations qui pourraient affecter les indicateurs de chiffre d'affaires et de rentabilité.

Les résultats sont conservés dans le notebook d'exploration PySpark, qui constitue le livrable technique de cette étape.

Aucune correction destructive n'a été appliquée à ce stade. Les valeurs atypiques, les valeurs manquantes et les doublons sont documentés afin de préserver la traçabilité des données.

Ces constats serviront de base à l'étape suivante : la préparation et la transformation des données dans la couche Silver.