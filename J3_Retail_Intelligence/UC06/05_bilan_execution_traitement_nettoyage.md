# Étape 4 : Règles de nettoyage et bilan d’exécution

## 1. Objectif

Cette étape applique des règles de qualité aux sources `store_sales` et `inventory` du jeu de données TPCx-BB. Les fichiers sources Raw sont conservés intacts. Les données traitées sont écrites en Parquet dans les zones Silver, quarantaine et qualité.

Le traitement distingue les anomalies bloquantes des valeurs atypiques qui doivent être conservées et examinées. Il ne supprime donc pas automatiquement les ventes à prix nul, les montants nets nuls, les bénéfices négatifs ou les lignes appartenant à des groupes de doublons potentiels.

## 2. Règles appliquées

### 2.1 Ventes – `store_sales`

- Les champs nécessaires à l’identification d’une vente (date, heure, article, magasin, ticket et quantité) doivent être renseignés et convertibles.
- Les champs démographiques et promotionnels facultatifs (`ss_cdemo_sk`, `ss_hdemo_sk`, `ss_addr_sk`, `ss_promo_sk`) peuvent rester nuls.
- Les quantités négatives, si elles existent, sont signalées pour examen et orientées vers la quarantaine.
- Les prix de vente nuls, les montants nets nuls et les bénéfices négatifs sont conservés et signalés : ils peuvent correspondre à des promotions, gratuités ou ventes à perte.
- La clé candidate composée de `ss_sold_date_sk`, `ss_store_sk`, `ss_ticket_number` et `ss_item_sk` n’étant pas unique, les lignes appartenant à des groupes répétés sont conservées dans Silver et signalées dans un jeu de revue dédié. Aucune suppression automatique n’est effectuée.

### 2.2 Stock – `inventory`

- Les champs `inv_date_sk`, `inv_item_sk`, `inv_warehouse_sk` et `inv_quantity_on_hand` doivent être renseignés et convertibles.
- Les quantités nulles sont mises en quarantaine.
- Les quantités négatives, si elles existent, sont mises en quarantaine pour examen.
- La clé candidate composée de `inv_date_sk`, `inv_item_sk` et `inv_warehouse_sk` est contrôlée. Les groupes dupliqués doivent être isolés pour revue plutôt que supprimés silencieusement.
- Les identifiants égaux à zéro ne sont pas rejetés sur le seul critère de positivité.

## 3. Résultats observés lors de l’exécution

| Source | Lignes lues | Lignes Silver | Quarantaine | Lignes signalées pour revue des doublons |
|---|---:|---:|---:|---:|
| `store_sales` | 667 579 | 667 579 | 0 | 8 174 |
| `inventory` | 23 255 100 | 23 249 101 | 5 999 | 0 |

### 3.1 Réconciliation des volumes

- Ventes : `667 579 = 667 579 + 0`.
- Stock : `23 255 100 = 23 249 101 + 5 999`.

Les volumes lus sont donc réconciliés avec les volumes Silver et quarantaine pour les deux sources.

### 3.2 Analyse des ventes

Aucune ligne de vente n'a été mise en quarantaine. Les 667 579 lignes ont été conservées dans Silver.

Le traitement a signalé 8 174 lignes comme appartenant à des groupes de doublons potentiels. Ce nombre désigne les lignes membres de groupes répétés, et non le nombre de groupes distincts ni le nombre de doublons à supprimer. L’exploration précédente avait identifié 4 038 groupes dupliqués sur la clé candidate. Les lignes concernées sont conservées afin d'éviter la suppression de ventes potentiellement légitimes.

### 3.3 Analyse du stock

Sur les 23 255 100 lignes source, 5 999 ont été mises en quarantaine et 23 249 101 conservées dans Silver.

Le nombre de lignes en quarantaine correspond au nombre de valeurs nulles de `inv_quantity_on_hand` relevé pendant l’exploration. Cette concordance est cohérente avec la règle définie pour les quantités de stock manquantes.

Aucune ligne n’est indiquée dans la colonne de revue des doublons du bilan d'exécution.

## 4. Avertissement Spark

Le message `WARN SparkStringUtils: Truncated the string representation of a plan since it was too large` indique que Spark a raccourci l’affichage textuel d’un plan d’exécution trop volumineux. Il ne constitue pas, à lui seul, une erreur de traitement. Le journal fourni indique que le traitement a atteint `Traitement terminé` et a affiché le bilan des sorties.

## 5. Emplacements des sorties

- Silver ventes : `data/silver/store_sales`
- Silver stock : `data/silver/inventory`
- Quarantaine ventes : `data/quarantine/store_sales`
- Quarantaine stock : `data/quarantine/inventory`
- Revue des doublons ventes : `data/quality/store_sales_duplicate_candidates`
- Synthèse qualité : `data/quality/summary`

## 6. Conclusion

L’étape 4 a été exécutée jusqu’à son terme. Les 667 579 lignes de ventes ont été conservées dans Silver, avec 8 174 lignes signalées pour revue des doublons potentiels. Pour le stock, 23 249 101 lignes ont été conservées dans Silver et 5 999 lignes ont été mises en quarantaine en raison de valeurs manquantes, conformément aux constats de l’étape d’exploration.

La séparation entre données conservées, données en quarantaine et lignes à examiner permet de préserver les données sources tout en rendant les problèmes de qualité visibles et traçables.
