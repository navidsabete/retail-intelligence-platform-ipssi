# Étape 9 : Mise en œuvre des contrôles qualité

### 1. Objectif

Cette étape a pour objectif de vérifier que les jeux de données produits par le pipeline sont cohérents et adaptés aux usages analytiques.

Les contrôles qualité permettent de détecter les valeurs manquantes, les doublons, les erreurs de typage, les incohérences métier et les problèmes éventuels de relations entre les jeux de données.

Les vérifications sont réparties sur les différentes étapes du pipeline, depuis la préparation des données Silver jusqu'à la production du jeu analytique Gold.

Pour cette étape, le contrôle complémentaire automatisé porte principalement sur le jeu Gold `sales_performance_by_store`, qui présente les performances commerciales des magasins.

### 2. Périmètre du contrôle

Le jeu de données contrôlé est situé dans :

`data/gold/sales_performance_by_store/`

Il contient 12 lignes, correspondant aux 12 magasins, et 14 colonnes.

La clé candidate retenue est `store_sk`. Elle doit être non nulle et identifier un seul enregistrement.

Les contrôles sont réalisés à l'aide de PySpark et portent sur les dimensions suivantes :

- complétude
- unicité 
- validité des types 
- cohérence des valeurs 
- volumes 
- clés candidates 
- intégrité référentielle 
- réconciliation avec le jeu Silver transformé.

Le rapport généré est enregistré dans :

`reports/quality/quality_report_gold.csv`

### 3. Tableau de synthèse des contrôles

| Contrôle | Règle | Résultat | Statut |
|---|---|---|---|
| Complétude | Champ requis non nul | Aucune valeur nulle dans les 11 colonnes contrôlées | PASS |
| Unicité | Clé candidate unique | 0 doublon sur `store_sk` | PASS |
| Validité | Type attendu | 11 colonnes conformes aux types attendus | PASS |
| Cohérence | Valeur dans un domaine valide | Classement, indicateurs et parts de CA cohérents | PASS |
| Volume | Nombre de lignes | 12 lignes, conformément au nombre de magasins attendu | PASS |
| Intégrité | Relation vérifiée | Contrôle non réalisable : `store_sk` absent de la source Silver `store_sales` | WARN |

Le statut PASS signifie que la règle contrôlée est respectée. Le statut WARN indique que le contrôle n'a pas pu être réalisé avec les données disponibles. Il ne signifie pas nécessairement que les données sont incorrectes.

### 4. Résultats détaillés de l'exécution

Le script PySpark a été exécuté sur le jeu Gold et a produit le bilan suivant :

| Statut | Nombre de contrôles |
|---|---:|
| PASS | 44 |
| FAIL | 0 |
| WARN | 1 |
| INFO | 0 |
| **Total** | **45** |

Aucun contrôle n'a échoué. Un seul contrôle a généré un avertissement, concernant l'intégrité référentielle avec les ventes Silver.

#### A. Complétude

Les 11 colonnes indispensables du jeu Gold ont été vérifiées :

- `store_sk`
- `revenue_rank`
- `is_best_revenue_store`
- `total_revenue_inc_tax`
- `global_revenue_inc_tax`
- `revenue_share_pct`
- `total_net_paid`
- `total_net_profit`
- `total_quantity_sold`
- `number_of_sales_lines`
- `number_of_tickets`

Résultat : aucune valeur nulle n'a été détectée dans ces colonnes.

Le contrôle de complétude est donc conforme pour le périmètre Gold étudié.

#### B. Unicité et clé candidate

La colonne `store_sk` est retenue comme clé candidate du jeu Gold.

Les résultats montrent :

- 12 lignes dans le jeu ;
- 12 identifiants de magasin distincts ;
- 0 doublon ;
- aucune valeur nulle dans `store_sk`.

La clé candidate est donc conforme : chaque magasin est représenté par un seul enregistrement.

#### C. Validité des types

Les types des colonnes indispensables ont été comparés aux types attendus dans Spark.

| Colonne | Type observé | Statut |
|---|---|---|
| `store_sk` | bigint | PASS |
| `revenue_rank` | int | PASS |
| `is_best_revenue_store` | boolean | PASS |
| `total_revenue_inc_tax` | decimal(17,2) | PASS |
| `global_revenue_inc_tax` | decimal(27,2) | PASS |
| `revenue_share_pct` | double | PASS |
| `total_net_paid` | decimal(17,2) | PASS |
| `total_net_profit` | decimal(17,2) | PASS |
| `total_quantity_sold` | bigint | PASS |
| `number_of_sales_lines` | bigint | PASS |
| `number_of_tickets` | bigint | PASS |

Les types observés correspondent aux types attendus. Les montants financiers sont conservés en Decimal, ce qui permet d'éviter de les traiter comme de simples nombres flottants.

#### D. Cohérence des valeurs

Plusieurs règles ont été appliquées aux indicateurs du jeu Gold.

**Classement des magasins :**

- tous les rangs sont compris entre 1 et 12 
- les 12 rangs sont distincts 
- un seul magasin est identifié comme meilleur magasin en chiffre d'affaires 
- cet indicateur correspond bien au rang 1

**Chiffre d'affaires :**

- aucune valeur de chiffre d'affaires TTC négative n'a été détectée 
- le chiffre d'affaires global est identique sur toutes les lignes 
- ce total correspond à la somme des chiffres d'affaires des magasins

Le chiffre d'affaires global observé est de **1 202 218 083,00**.

**Parts de chiffre d'affaires :**

- toutes les parts sont comprises entre 0 et 100 % 
- leur somme est de 99,99999999999999 % 
- aucune incohérence n'a été détectée entre la part calculée et le rapport entre le chiffre d'affaires du magasin et le chiffre d'affaires global

La légère différence par rapport à 100 % est liée à la représentation des nombres flottants. Elle reste dans la tolérance de 0,1 point définie par le contrôle.

#### E. Volumes

Le nombre de lignes attendu est de 12, correspondant aux 12 magasins présents dans le jeu de données.

Le résultat observé est également de 12 lignes.

Le contrôle de volume est donc conforme.

#### F. Réconciliation avec le jeu Silver transformé

Le jeu Gold a été comparé à sa source de construction :

`data/silver-transformed/sales_by_store/`

Les contrôles ont confirmé :

- 12 magasins dans la source et 12 dans le Gold
- aucun magasin manquant dans le Gold 
- aucun magasin supplémentaire dans le Gold 
- aucune différence entre les six mesures comparées, magasin par magasin.

Les sommes des mesures ont également été comparées.

| Mesure | Source Silver transformée | Gold | Résultat |
|---|---:|---:|---|
| `total_revenue_inc_tax` | 1 202 218 083,00 | 1 202 218 083,00 | PASS |
| `total_net_paid` | 1 150 529 586,37 | 1 150 529 586,37 | PASS |
| `total_net_profit` | -552 553 374,82 | -552 553 374,82 | PASS |
| `total_quantity_sold` | 33 755 474 | 33 755 474 | PASS |
| `number_of_sales_lines` | 667 579 | 667 579 | PASS |
| `number_of_tickets` | 89 100 | 89 100 | PASS |

Cette réconciliation confirme que les mesures commerciales ont été conservées lors de la construction du jeu Gold.

#### G. Intégrité référentielle

Un contrôle complémentaire devait comparer les identifiants `store_sk` du jeu Gold avec ceux présents dans les ventes Silver.

Cependant, le script a retourné le résultat suivant :

`Colonne store_sk absente`

Le contrôle a donc été classé WARN.

Cela signifie que la relation n'a pas pu être vérifiée avec le jeu `data/silver/store_sales/`, car cette source ne contient pas la colonne technique `store_sk` attendue.

Il ne s'agit pas d'une preuve d'une relation incorrecte, mais d'une limite du contrôle liée au schéma disponible.

La comparaison entre Silver transformé et Gold a néanmoins été réalisée avec succès sur `store_sk` : les 12 identifiants sont identiques dans les deux jeux.

Pour compléter l'intégrité référentielle, il faudrait identifier la source ou la dimension de référence contenant la correspondance entre les identifiants de magasin et les clés `store_sk`.

### 5. Anomalies et limites identifiées

Les résultats du contrôle Gold ne révèlent aucune anomalie bloquante : 44 contrôles sont conformes et aucun n'est en échec.

Un avertissement demeure sur l'intégrité référentielle avec les ventes Silver.

Il faut également distinguer ces résultats des anomalies détectées lors des étapes précédentes du pipeline.

| Anomalie identifiée précédemment | Constat | Traitement |
|---|---|---|
| Valeurs nulles dans `inventory` | 5 999 lignes mises en quarantaine, principalement pour une quantité en stock nulle | Données mises à l'écart |
| Doublons candidats dans `store_sales` | 8 174 lignes réparties en 4 038 groupes | Conservés, en attente d'une règle métier |
| Prix unitaires nuls | 3 324 occurrences | Pas de correction automatique |
| Montants nets payés nuls | 3 954 occurrences | Pas de correction automatique |
| Profits et marges négatifs | Valeurs négatives observées | Interprétation métier nécessaire |
| Ventes sans correspondance dans le stock agrégé | 484 701 lignes lors de la jointure | Pas de suppression automatique |

Ces anomalies ne remettent pas directement en cause la conformité technique du jeu Gold. Elles doivent toutefois rester documentées, car elles peuvent influencer certaines analyses métier.

### 6. Corrections et perspectives d'amélioration

Aucune correction automatique n'a été nécessaire sur le jeu Gold à la suite de cette exécution.

Plusieurs améliorations restent possibles :

- identifier une source de référence permettant de vérifier l'intégrité référentielle de `store_sk` 
- définir une règle métier de déduplication des ventes 
- préciser les règles de gestion des prix et montants nuls 
- documenter les cas pouvant expliquer des profits négatifs 
- compléter les contrôles sur les jeux Silver et Silver transformés 
- mettre en place un suivi régulier des volumes de données mises en quarantaine

La validation de ces règles nécessitera, selon les cas, des informations métier complémentaires ou une expérimentation sur les données.

### 7. Conclusion

L'étape 9 a permis de formaliser et d'automatiser les contrôles qualité sur le jeu Gold `sales_performance_by_store`.

L'exécution du script PySpark a produit 45 résultats de contrôle :

- 44 contrôles conformes 
- aucun contrôle en échec 
- un avertissement concernant une relation référentielle qui n'a pas pu être vérifiée

Les contrôles de complétude, d'unicité, de validité des types, de cohérence des indicateurs, de volume et de réconciliation avec la source Silver transformée sont conformes.

Le seul avertissement concerne l'absence de la colonne `store_sk` dans le jeu de ventes Silver utilisé pour le contrôle référentiel. Une source de référence adaptée devra être identifiée pour lever cette limite.

Les anomalies détectées précédemment dans les données sources restent documentées et ne font pas l'objet de corrections automatiques sans validation métier.

Le livrable de cette étape est le rapport de qualité généré dans :

`reports/quality/quality_report_gold.csv`

Ce rapport permet de conserver une trace des règles appliquées, des résultats obtenus et des points nécessitant une investigation complémentaire.