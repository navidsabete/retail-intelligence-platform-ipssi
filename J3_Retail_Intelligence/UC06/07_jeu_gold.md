# Étape 7 – Production des données Gold

## 1. Objectif

L'objectif de cette étape est de produire un jeu de données Gold orienté analyse et décision, à partir des données préparées lors des étapes précédentes.

Le jeu Gold retenu est `sales_performance_by_store`. Il répond à la question métier identifiée lors du Jour 1 :

**Quels magasins réalisent le meilleur chiffre d'affaires ?**

Il contribue également à répondre à la question :

**Quel est le chiffre d'affaires de mon magasin ?**

Ce jeu permet de comparer les performances commerciales des magasins, de calculer leur contribution au chiffre d'affaires global et d'identifier le magasin réalisant le chiffre d'affaires TTC le plus élevé.

## 2. Sources utilisées

Le jeu Gold est construit à partir du jeu de données Silver transformé :

`data/silver-transformed/sales_by_store/`

Cette source, produite lors de l'étape 6, contient déjà les agrégations commerciales par magasin.

Le traitement Gold reprend les mesures existantes et les enrichit avec des indicateurs analytiques supplémentaires.

Cette approche évite de recalculer les agrégations à partir des ventes détaillées et garantit la continuité entre les couches Silver transformée et Gold.

## 3. Granularité

La granularité retenue est :

**Une ligne par magasin, identifié par la clé technique `store_sk`.**

Le jeu source contient 12 magasins.

Les contrôles réalisés confirment l'absence de clés magasin nulles et de doublons à cette granularité.

Le jeu Gold contient donc 12 lignes, correspondant aux 12 magasins présents dans la source.

## 4. Indicateurs produits

Le jeu Gold contient 14 colonnes réparties entre les dimensions, les mesures, les indicateurs calculés et les métadonnées.

Les principaux indicateurs ajoutés sont :

- `revenue_rank` : classement des magasins par chiffre d'affaires TTC décroissant.
- `is_best_revenue_store` : indicateur booléen identifiant le ou les magasins classés premiers.
- `global_revenue_inc_tax` : chiffre d'affaires TTC total de l'ensemble des magasins.
- `revenue_share_pct` : part du chiffre d'affaires TTC de chaque magasin dans le chiffre d'affaires global.

Les autres mesures sont reprises du jeu Silver transformé :

- `total_revenue_inc_tax` : chiffre d'affaires TTC.
- `total_net_paid` : montant net payé.
- `total_net_profit` : profit net agrégé.
- `total_quantity_sold` : quantité totale vendue.
- `number_of_sales_lines` : nombre de lignes de vente.
- `number_of_tickets` : nombre de tickets.

Trois colonnes supplémentaires assurent la traçabilité du jeu :

- `_gold_dataset` : nom du jeu Gold.
- `_business_grain` : granularité métier.
- `_processing_stage` : couche de traitement.

## 5. Règles de calcul

Le chiffre d'affaires global correspond à la somme des chiffres d'affaires TTC des différents magasins :

CA global = somme des CA TTC de tous les magasins.

La part de chiffre d'affaires de chaque magasin est calculée selon la formule :

Part (%) = (CA TTC du magasin / CA TTC global) × 100.

Le résultat est arrondi à deux décimales.

Le classement est réalisé par ordre décroissant du chiffre d'affaires TTC avec la fonction `rank()` de PySpark. En cas d'égalité, plusieurs magasins peuvent obtenir le même rang.

L'indicateur `is_best_revenue_store` vaut `true` lorsque le rang du magasin est égal à 1.

Les montants financiers conservent leurs types `decimal`, tandis que les indicateurs de comptage utilisent des types entiers.

## 6. Résultats obtenus

L'exécution du traitement a produit un jeu Gold de 12 lignes et 14 colonnes.

Le chiffre d'affaires TTC global des 12 magasins s'élève à 1 202 218 083,00.

Le classement obtenu identifie :

- Le magasin 7 comme premier, avec un chiffre d'affaires TTC de 103 384 198,80.
- Le magasin 4 en deuxième position, avec 101 130 648,13.
- Le magasin 9 en troisième position, avec 101 109 360,86.
- Le magasin 2 en dernière position, avec 98 249 685,02.

Le magasin 7 représente environ 8,60 % du chiffre d'affaires TTC global.

Ces résultats permettent de répondre à la question métier portant sur les magasins réalisant le meilleur chiffre d'affaires.

## 7. Contrôles qualité et validation

Plusieurs contrôles ont été intégrés au traitement afin de vérifier la cohérence du jeu Gold.

Les contrôles de structure ont confirmé :

- La présence de toutes les colonnes obligatoires.
- L'absence de clés magasin nulles.
- L'absence de doublons à la granularité choisie.
- La présence de types numériques adaptés aux mesures.
- L'absence de valeurs nulles dans les indicateurs numériques contrôlés.

Les contrôles de cohérence ont confirmé :

- La conservation des 12 lignes entre Silver transformé et Gold.
- La validité des classements.
- La cohérence de l'indicateur identifiant le meilleur magasin.
- Une somme des parts de chiffre d'affaires égale à environ 100 %.

Une réconciliation des mesures entre Silver transformé et Gold a également été réalisée.

Les sommes des six indicateurs contrôlés sont strictement identiques dans les deux couches : chiffre d'affaires TTC, montant net payé, profit net, quantités vendues, lignes de vente et tickets.

Une comparaison complémentaire par magasin n'a détecté aucun écart.

Enfin, le jeu Gold a été écrit au format Parquet avec compression Snappy, puis relu avec succès. Le nombre de lignes après relecture est identique au nombre de lignes avant écriture, et la comparaison complète des données n'a détecté aucune différence.

## 8. Limites d'interprétation

Le jeu Gold fournit une analyse descriptive des performances commerciales par magasin.

Le classement repose uniquement sur le chiffre d'affaires TTC. Il ne constitue donc pas un classement de rentabilité. Les identifiants de magasins sont des clés techniques et ne sont pas enrichis avec des informations descriptives supplémentaires.

Le jeu produit constitue néanmoins une base exploitable pour des tableaux de bord et des analyses comparatives des performances commerciales.

## 9. Emplacement du résultat

Le jeu Gold est disponible dans le répertoire :

`data/gold/sales_performance_by_store/`

Il est stocké au format Parquet avec compression Snappy et peut être relu directement par PySpark pour les traitements analytiques ultérieurs.