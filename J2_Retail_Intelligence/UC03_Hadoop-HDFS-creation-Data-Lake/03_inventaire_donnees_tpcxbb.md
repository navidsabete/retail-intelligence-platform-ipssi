# Inventaire des données TPCX-BB

L'inventaire a été réalisé en J1 à travers un script d'analyse automatique.

## Informations relevées pour chaque fichier

| Information | Élément relevé |
|---|---|
| **Nom** | Nom exact du fichier ou de la ressource. |
| **Chemin** | Chemin relatif réel dans le jeu de données fourni. La racine absolue n'est pas précisée dans les éléments du J1. |
| **Format** | Format constaté : DAT ou CSV. |
| **Taille** | Taille réelle relevée en octets. |
| **Structure** | Nombre de colonnes et noms des champs. Les fichiers DAT n'ayant pas d'en-tête, les champs sont désignés provisoirement par leur position (`colonne_1`, `colonne_2`, etc.). |
| **Types** | Types estimés lors du profilage ; les détails par colonne figurent dans le rapport de colonnes. |
| **Volume** | Nombre de lignes de données relevé. |
| **Provenance** | Jeu de données TPCX-BB, répertoires `data/` et `data_refresh/`. La version précise du kit : Version 1.7.0 (Juin 2025). |
| **Limites** | Champs vides, variations de structure ou autres anomalies signalées par le profilage. |

## Matrice d’inventaire

Les tailles sont exprimées en octets. Les fichiers DAT sont séparés par le caractère `|` et ne comportent pas d'en-tête. Les colonnes sont donc nommées par position.

| Fichier | Format | Taille (octets) | Lignes | Structure |
|---|---:|---:|---:|---|
| `data/customer/customer.dat` | DAT | 13 279 063 | 99 000 | 18 colonnes : `colonne_1` à `colonne_18` |
| `data/customer_address/customer_address.dat` | DAT | 5 387 229 | 49 500 | 13 colonnes : `colonne_1` à `colonne_13` |
| `data/customer_demographics/customer_demographics.dat` | DAT | 77 753 083 | 1 920 800 | 9 colonnes : `colonne_1` à `colonne_9` |
| `data/date_dim/date_dim.dat` | DAT | 15 395 800 | 109 573 | 28 colonnes : `colonne_1` à `colonne_28` |
| `data/household_demographics/household_demographics.dat` | DAT | 155 100 | 7 200 | 5 colonnes : `colonne_1` à `colonne_5` |
| `data/income_band/income_band.dat` | DAT | 327 | 20 | 3 colonnes : `colonne_1` à `colonne_3` |
| `data/inventory/inventory.dat` | DAT | 424 943 678 | 23 255 100 | 4 colonnes : `colonne_1` à `colonne_4` |
| `data/item/item.dat` | DAT | 6 799 286 | 17 820 | 22 colonnes : `colonne_1` à `colonne_22` |
| `data/item_marketprices/item_marketprices.dat` | DAT | 4 201 170 | 89 100 | 6 colonnes : `colonne_1` à `colonne_6` |
| `data/item_marketprices/item_marketprices_audit.csv` | CSV | 273 | 4 | Structure non reconnue par le script : 0 colonne détectée |
| `data/product_reviews/product_reviews.dat` | DAT | 56 355 389 | 89 601 | 8 colonnes : `colonne_1` à `colonne_8` |
| `data/promotion/promotion.dat` | DAT | 46 396 | 300 | 19 colonnes : `colonne_1` à `colonne_19` |
| `data/reason/reason.dat` | DAT | 3 105 | 35 | 3 colonnes : `colonne_1` à `colonne_3` |
| `data/ship_mode/ship_mode.dat` | DAT | 1 220 | 20 | 6 colonnes : `colonne_1` à `colonne_6` |
| `data/store/store.dat` | DAT | 3 386 | 12 | 29 colonnes : `colonne_1` à `colonne_29` |
| `data/store_returns/store_returns.dat` | DAT | 4 337 400 | 37 902 | 20 colonnes : `colonne_1` à `colonne_20` |
| `data/store_sales/store_sales.dat` | DAT | 92 764 700 | 667 579 | 23 colonnes : `colonne_1` à `colonne_23` |
| `data/time_dim/time_dim.dat` | DAT | 5 107 780 | 86 400 | 10 colonnes : `colonne_1` à `colonne_10` |
| `data/warehouse/warehouse.dat` | DAT | 584 | 5 | 14 colonnes : `colonne_1` à `colonne_14` |
| `data/web_clickstreams/web_clickstreams.dat` | DAT | 178 722 140 | 6 770 550 | 6 colonnes : `colonne_1` à `colonne_6` |
| `data/web_page/web_page.dat` | DAT | 8 040 | 60 | 14 colonnes : `colonne_1` à `colonne_14` |
| `data/web_returns/web_returns.dat` | DAT | 5 383 513 | 38 487 | 24 colonnes : `colonne_1` à `colonne_24` |
| `data/web_sales/web_sales.dat` | DAT | 133 790 574 | 668 052 | 34 colonnes : `colonne_1` à `colonne_34` |
| `data/web_site/web_site.dat` | DAT | 8 838 | 30 | 26 colonnes : `colonne_1` à `colonne_26` |
| `data_refresh/customer/customer.dat` | DAT | 134 360 | 1 000 | 18 colonnes : `colonne_1` à `colonne_18` |
| `data_refresh/customer_address/customer_address.dat` | DAT | 54 587 | 500 | 13 colonnes : `colonne_1` à `colonne_13` |
| `data_refresh/inventory/inventory.dat` | DAT | 4 292 915 | 234 900 | 4 colonnes : `colonne_1` à `colonne_4` |
| `data_refresh/item/item.dat` | DAT | 69 173 | 180 | 22 colonnes : `colonne_1` à `colonne_22` |
| `data_refresh/item_marketprices/item_marketprices.dat` | DAT | 42 547 | 900 | 6 colonnes : `colonne_1` à `colonne_6` |
| `data_refresh/item_marketprices/item_marketprices_audit.csv` | CSV | 151 009 | 17 985 | Structure non reconnue par le script : 0 colonne détectée |
| `data_refresh/product_reviews/product_reviews.dat` | DAT | 573 685 | 907 | 8 colonnes : `colonne_1` à `colonne_8` |
| `data_refresh/store_returns/store_returns.dat` | DAT | 48 825 | 426 | 20 colonnes : `colonne_1` à `colonne_20` |
| `data_refresh/store_sales/store_sales.dat` | DAT | 922 171 | 6 632 | 23 colonnes : `colonne_1` à `colonne_23` |
| `data_refresh/web_clickstreams/web_clickstreams.dat` | DAT | 1 821 864 | 68 988 | 6 colonnes : `colonne_1` à `colonne_6` |
| `data_refresh/web_returns/web_returns.dat` | DAT | 55 952 | 400 | 24 colonnes : `colonne_1` à `colonne_24` |
| `data_refresh/web_sales/web_sales.dat` | DAT | 1 378 425 | 6 879 | 34 colonnes : `colonne_1` à `colonne_34` |

## Types observés ou estimés

Le profilage fourni décrit **522 colonnes**. Les types sont des estimations réalisées à partir des valeurs échantillonnées : `ENTIER`, `NUMERIQUE`, `DATE_PROBABLE`, `TEXTE` ou `VIDE`.

Les fichiers DAT n'ayant pas d'en-tête, les noms métier des champs ne sont pas disponibles dans le relevé fourni. Les types détaillés doivent être consultés dans `UC01_inventaire_sources.xlsx - Qualité colonnes`. À titre d'exemple, pour `data/customer/customer.dat`, les 18 champs sont estimés comme suit :

| Champ | Type estimé |
|---|---|
| `colonne_1` | ENTIER |
| `colonne_2` | TEXTE |
| `colonne_3` | ENTIER |
| `colonne_4` | ENTIER |
| `colonne_5` | ENTIER |
| `colonne_6` | ENTIER |
| `colonne_7` | ENTIER |
| `colonne_8` | TEXTE |
| `colonne_9` | TEXTE |
| `colonne_10` | TEXTE |
| `colonne_11` | TEXTE |
| `colonne_12` | ENTIER |
| `colonne_13` | ENTIER |
| `colonne_14` | ENTIER |
| `colonne_15` | TEXTE |
| `colonne_16` | TEXTE |
| `colonne_17` | TEXTE |
| `colonne_18` | TEXTE |

## Limites et anomalies constatées

Le bilan du profilage transmis indique **94 signalements d'anomalies**, principalement liés à des valeurs vides. Les anomalies détaillées sont consignées dans `UC01_inventaire_sources.xlsx - Compte-rendu anomalies`.

Principaux constats issus du rapport :

- Des valeurs vides sont signalées dans plusieurs fichiers, notamment `customer`, `customer_address`, `customer_demographics`, `inventory`, `item`, `store_sales`, `web_clickstreams`, `web_returns` et `web_sales`, ainsi que dans certains fichiers de `data_refresh/`.
- Dans `data/web_clickstreams/web_clickstreams.dat`, le rapport signale 6 102 498 valeurs vides en `colonne_3` et 2 853 461 en `colonne_6`.
- Dans `data/time_dim/time_dim.dat`, 50 400 valeurs vides sont signalées en `colonne_10`.
- Dans `data/inventory/inventory.dat`, 5 999 valeurs vides sont signalées en `colonne_4`.
- Les deux fichiers CSV d'audit (`data/item_marketprices/item_marketprices_audit.csv` et `data_refresh/item_marketprices/item_marketprices_audit.csv`) présentent une structure que le script n'a pas correctement interprétée : 0 colonne détectée, avec respectivement 4 et 17 985 lignes signalées comme ayant un nombre de colonnes variable. Ils nécessitent une inspection spécifique avant toute conclusion sur leur structure.
- Les types sont estimés automatiquement à partir d'échantillons de valeurs ; ils ne constituent pas un schéma métier validé.
- Les noms des champs des fichiers DAT restent provisoires tant qu'ils n'ont pas été rapprochés du schéma de référence TPCx-BB.

## Synthèse de l'inventaire

| Indicateur | Résultat |
|---|---:|
| Fichiers recensés | 36 |
| Colonnes décrites | 522 |
| Anomalies signalées | 94 |
| Formats principaux | DAT et CSV |
| Séparateur des fichiers DAT | `|` |
| En-têtes des fichiers DAT | Absents ; champs repérés par position |
| Fichiers d'audit à vérifier | 2 |