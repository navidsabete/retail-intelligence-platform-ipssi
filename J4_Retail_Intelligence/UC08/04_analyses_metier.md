# Étape 4 – Réaliser des analyses métier

Deux analyses métier ont été réalisées à partir des données préparées lors du TP3. Elles répondent à des besoins identifiés dans le TP UC-01 : le suivi du chiffre d'affaires des magasins et la comparaison de leurs performances commerciales.

Une analyse complémentaire des produits les plus vendus a également été effectuée à partir des ventes détaillées.

## Analyse 1 – Quels magasins réalisent le meilleur chiffre d'affaires ?

**Question métier :** Quels magasins réalisent le meilleur chiffre d'affaires ?

**Utilisateur concerné :** Direction commerciale.

**Priorité UC-01 :** Indispensable.

**Décision possible :** Identifier les magasins les plus performants et comparer leurs contributions au chiffre d'affaires global.

### 1. Données utilisées

Le jeu de données utilisé est `sales_performance_by_store`, situé dans la couche Gold.

Les principaux champs exploités sont :

- `store_sk` : identifiant du magasin 
- `total_revenue_inc_tax` : chiffre d'affaires TTC du magasin 
- `revenue_rank` : classement du magasin selon son chiffre d'affaires 
- `revenue_share_pct` : part du magasin dans le chiffre d'affaires global

### 2. Méthode de calcul

Les données sont agrégées à la granularité d'un magasin. Les magasins sont classés par chiffre d'affaires TTC décroissant.

La part de chaque magasin est calculée selon la formule :

Part du magasin (%) = (CA TTC du magasin / CA TTC global) × 100.

Aucun filtre métier supplémentaire n'a été appliqué : l'analyse porte sur l'ensemble des magasins présents dans le jeu Gold et sur la période couverte par les données.

### 3. Résultats obtenus

Le chiffre d'affaires TTC global est de **1 202 218 083,00 unités monétaires**, réparti entre 12 magasins.

| Classement | Magasin | Chiffre d'affaires TTC | Part du CA global |
|---:|---:|---:|---:|
| 1 | 7 | 103 384 198,80 | 8,60 % |
| 2 | 4 | 101 130 648,13 | 8,41 % |
| 3 | 9 | 101 109 360,86 | 8,41 % |
| 4 | 0 | 101 047 840,24 | 8,40 % |
| 5 | 8 | 100 916 146,68 | 8,40 % |
| 6 | 3 | 100 377 573,32 | 8,35 % |
| 7 | 1 | 100 230 588,43 | 8,34 % |
| 8 | 11 | 99 910 528,38 | 8,31 % |
| 9 | 6 | 99 040 970,11 | 8,24 % |
| 10 | 10 | 98 490 674,24 | 8,19 % |
| 11 | 5 | 98 329 868,79 | 8,18 % |
| 12 | 2 | 98 249 685,02 | 8,17 % |

### 4. Interprétation

Le magasin 7 réalise le meilleur chiffre d'affaires TTC, avec 103,38 millions d'unités monétaires, soit environ 8,60 % du chiffre d'affaires global.

Le magasin 2 arrive en dernière position, avec 98,25 millions. L'écart entre le premier et le dernier magasin est de 5 134 513,78 unités monétaires.

Les parts de chiffre d'affaires sont relativement proches, comprises entre 8,17 % et 8,60 %. Cela indique une répartition assez homogène du chiffre d'affaires entre les douze magasins.

Cette analyse permet à la direction commerciale d'identifier les magasins en tête du classement et de repérer ceux dont les résultats pourraient nécessiter une analyse complémentaire.

### 5. Limites éventuelles

- Les magasins sont identifiés uniquement par leur clé technique `store_sk`. Leurs noms ou localisations ne sont pas présentés.
- Le chiffre d'affaires ne permet pas, à lui seul, de mesurer la rentabilité d'un magasin.
- Les résultats sont cumulés sur la période disponible. Ils ne permettent pas d'identifier les évolutions ou les variations saisonnières.
- Les montants sont exprimés dans l'unité monétaire du jeu TPCx-BB ; la devise reste à confirmer dans la documentation source.

## Analyse 2 – Quel est le chiffre d'affaires de mon magasin ?

**Question métier :** Quel est le chiffre d'affaires de mon magasin ?

**Utilisateur concerné :** Responsable de magasin.

**Priorité UC-01 :** Indispensable.

**Décision possible :** Suivre les résultats commerciaux du magasin et adapter les objectifs de vente.

### 1. Données utilisées

Le jeu `sales_performance_by_store`, dans la couche Gold, est utilisé.

Les champs principaux sont :

- `store_sk` : identifiant du magasin 
- `total_revenue_inc_tax` : chiffre d'affaires TTC 
- `total_net_paid` : montant net payé 
- `total_quantity_sold` : quantités vendues 
- `number_of_tickets` : nombre de tickets

### 2. Méthode de calcul

Le chiffre d'affaires TTC est récupéré pour chaque magasin. Les autres indicateurs sont utilisés en complément pour fournir une vision plus complète de son activité commerciale.

La granularité du jeu Gold est d'une ligne par magasin. Il n'est donc pas nécessaire de recalculer les sommes à partir des ventes détaillées pour obtenir le chiffre d'affaires cumulé par magasin.

Aucun filtre métier supplémentaire n'a été appliqué. Le responsable peut consulter la ligne correspondant à son magasin à partir de son identifiant.

### 3. Résultats obtenus

Le tableau suivant présente les principaux indicateurs commerciaux par magasin.

| Magasin | CA TTC | Quantités vendues | Tickets |
|---:|---:|---:|---:|
| 7 | 103 384 198,80  | 2 915 053 | 7 645 |
| 4 | 101 130 648,13  | 2 832 572 | 7 462 |
| 9 | 101 109 360,86  | 2 830 684 | 7 435 |
| 0 | 101 047 840,24  | 2 830 581 | 7 456 |
| 8 | 100 916 146,68  | 2 821 869 | 7 414 |
| 3 | 100 377 573,32  | 2 800 824 | 7 396 |
| 1 | 100 230 588,43  | 2 817 524 | 7 422 |
| 11 | 99 910 528,38  | 2 790 631 | 7 449 |
| 6 | 99 040 970,11  | 2 780 253 | 7 284 |
| 10 | 98 490 674,24  | 2 785 773 | 7 409 |
| 5 | 98 329 868,79  | 2 789 703 | 7 369 |
| 2 | 98 249 685,02  | 2 760 007 | 7 359 |


### 4. Interprétation

Le tableau permet à chaque responsable de magasin de retrouver son chiffre d'affaires TTC et de le mettre en perspective avec les résultats des autres magasins.

Par exemple, le magasin 7 présente le chiffre d'affaires le plus élevé, tandis que le magasin 2 présente le chiffre d'affaires le plus faible.

Les quantités vendues et le nombre de tickets complètent l'indicateur de chiffre d'affaires et permettent de mieux caractériser l'activité commerciale.

Cette analyse répond au besoin de suivi individuel du responsable de magasin. Elle peut servir de base à un tableau de bord de pilotage commercial.

### 5. Limites éventuelles

- Les résultats sont cumulés sur toute la période disponible et ne sont pas ventilés par mois ou par jour.
- L'identification des magasins repose sur leur clé technique.
- Les données ne permettent pas, à elles seules, de comparer les objectifs commerciaux aux résultats réalisés.
- Le nombre de tickets correspond à la définition validée lors de l'étape précédente : somme des décomptes distincts par magasin et par date.

## Analyse complémentaire – Quels produits sont les plus vendus dans chaque magasin ?

**Question métier :** Quels produits sont les plus vendus dans mon magasin ?

**Utilisateur concerné :** Responsable de magasin.

**Priorité UC-01 :** Utile.

**Décision possible :** Adapter les commandes et la mise en rayon aux produits les plus demandés.

### 1. Données utilisées

Le jeu de données `store_sales`, situé dans la couche Silver, a été utilisé.

Les champs exploités sont :

- `ss_store_sk` : identifiant du magasin 
- `ss_item_sk` : identifiant du produit 
- `ss_quantity` : quantité vendue 
- `ss_net_paid_inc_tax` : montant net payé TTC

Les contrôles effectués montrent qu'aucune valeur NULL n'est présente dans ces quatre colonnes sur le jeu étudié.

### 2. Méthode de calcul

Les ventes sont regroupées par couple magasin-produit.

Pour chaque couple, les indicateurs suivants sont calculés :

- somme des quantités vendues 
- somme du montant net payé TTC 
- nombre de lignes de vente

Les produits sont ensuite classés par quantité vendue décroissante à l'intérieur de chaque magasin. Un classement global est également réalisé sur l'ensemble des magasins.

### 3. Résultats obtenus

Le classement global des dix produits les plus vendus en quantité est le suivant :

| Rang | Produit (`ss_item_sk`) | Quantités vendues | Montant net payé TTC |
|---:|---:|---:|---:|
| 1 | 10000 | 454 954 | 16 108 841,77 |
| 2 | 10003 | 439 086 | 15 614 283,97 |
| 3 | 10001 | 420 138 | 15 240 549,34 |
| 4 | 10002 | 377 027 | 13 397 798,56 |
| 5 | 5618 | 95 677 | 3 355 977,13 |
| 6 | 17502 | 94 625 | 3 482 713,49 |
| 7 | 673 | 92 967 | 3 187 900,02 |
| 8 | 11552 | 92 446 | 3 250 624,08 |
| 9 | 16513 | 91 710 | 3 297 977,63 |
| 10 | 689 | 91 464 | 3 247 954,55 |

Le classement par magasin montre également que les produits 10000, 10003, 10001 et 10002 figurent systématiquement parmi les quatre premières positions des douze magasins.

Le produit 10000 arrive en première position dans la majorité des magasins. Le produit 10003 arrive en première position dans certains magasins, notamment les magasins 1, 8, 10 et 11.

### 4. Interprétation

Les quatre premières références présentent des volumes de vente nettement supérieurs aux autres produits du classement.

Le produit 10000 est le plus vendu à l'échelle globale, avec 454 954 unités. Il constitue donc une référence importante dans l'activité commerciale du périmètre étudié.

La présence récurrente des mêmes références parmi les produits les plus vendus dans les différents magasins suggère une structure de demande relativement similaire entre les magasins.

Ces résultats peuvent aider les responsables à identifier les produits à suivre en priorité dans les commandes et la mise en rayon.

### 5. Limites éventuelles

- Les produits sont identifiés par leur clé technique `ss_item_sk` ; leurs noms et catégories commerciales ne sont pas disponibles dans cette analyse.
- Le classement repose sur les quantités vendues et non sur la marge ou la rentabilité des produits.
- Le montant utilisé est `ss_net_paid_inc_tax` ; il ne doit pas être confondu avec une mesure de marge.
- Les résultats sont cumulés sur la période disponible et ne permettent pas d'identifier les produits dont les ventes diminuent récemment.
- Les quantités vendues ne suffisent pas à mesurer la vitesse d'écoulement des stocks ni à identifier les risques de rupture.

## 6. Conclusion 

Les analyses réalisées répondent à plusieurs questions métier identifiées dans le TP UC-01.

La comparaison des chiffres d'affaires permet à la direction commerciale de classer les magasins selon leurs performances. Le détail par magasin permet aux responsables de suivre leur activité commerciale. Enfin, l'analyse des produits les plus vendus apporte un premier éclairage pour adapter les commandes et la mise en rayon.

Les résultats montrent notamment une répartition relativement homogène du chiffre d'affaires entre les magasins et une forte concentration des quantités vendues sur quatre références de produits.

Les analyses restent limitées par l'absence de libellés commerciaux, de comparaison avec des objectifs et de données temporelles exploitées sous forme de périodes comparables. Elles constituent néanmoins une première base d'aide à la décision à partir des données Silver et Gold préparées lors du TP3.