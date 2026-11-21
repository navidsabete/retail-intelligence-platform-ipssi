# Étape 2 – Vérification et calcul des KPI

## 2.1. Objectif

Cette étape consiste à reprendre le dictionnaire des KPI défini lors du TP UC-01 et à vérifier la possibilité de calculer les indicateurs à partir des données disponibles dans les zones Silver et Gold.

Les indicateurs sont sélectionnés en fonction :
- de la disponibilité des champs nécessaires 
- de leur définition métier 
- de la granularité des jeux de données 
- de la cohérence des règles de calcul 
- des contrôles de validation réalisés.

3 KPI ont été retenus : le chiffre d'affaires TTC, les quantités vendues et le nombre de transactions.

## 2.2. Environnement et sources utilisées

Les calculs ont été réalisés avec PySpark 4.3.0 dans l'environnement virtuel dédié au TP4.

Les jeux utilisés sont :

| Jeu | Zone | Nombre de lignes | Utilisation |
|---|---|---:|---|
| sales_by_store_date | Silver transformé | 21 430 | Calcul des indicateurs par magasin et date |
| sales_performance_by_store | Gold | 12 | Vérification et comparaison des indicateurs par magasin |
| store_sales | Silver détaillé | 667 579 | Validation du nombre de transactions |

Les jeux Silver transformé et Gold sont stockés au format Parquet avec compression Snappy.

## 2.3. Dictionnaire des KPI retenus

### KPI 1 – Chiffre d'affaires TTC

**Définition métier :**

Montant total généré par les ventes, taxes incluses, sur le périmètre étudié.

**Formule :**

CA TTC = Σ total_revenue_inc_tax

**Champ utilisé :**
- `total_revenue_inc_tax`

**Sources :**
- `sales_by_store_date` : Silver transformé.
- `sales_performance_by_store` : Gold.

**Filtres appliqués :**

Aucun filtre supplémentaire. Le calcul porte sur l'ensemble des magasins et des dates présents dans le jeu sélectionné.

**Granularité :**
- Silver : magasin/date.
- Gold : magasin.

**Unité :** unité monétaire de la source, à confirmer.

**Résultat obtenu :** 1 202 218 083,00.

**Limites d'interprétation :**

Le chiffre d'affaires TTC ne représente pas le bénéfice de l'entreprise. Le traitement des remises, des retours et des annulations dépend des règles de transformation appliquées au TP3.

Les données Silver et Gold ne doivent pas être additionnées simultanément, car elles représentent des niveaux de transformation différents d'un même périmètre commercial.

Dans Gold, `global_revenue_inc_tax` est une valeur globale répétée sur les lignes des magasins. Elle ne doit pas être additionnée pour recalculer le chiffre d'affaires global.

### KPI 2 – Quantités vendues

**Définition métier :**

Volume total des quantités de produits vendues sur le périmètre étudié.

**Formule :**

Quantités vendues = Σ total_quantity_sold

**Champ utilisé :**
- `total_quantity_sold`

**Sources :**
- `sales_by_store_date` : Silver transformé.
- `sales_performance_by_store` : Gold.

**Filtres appliqués :**

Aucun filtre supplémentaire. Le calcul porte sur l'ensemble des magasins et des dates présents dans le jeu sélectionné.

**Granularité :**
- Silver : magasin/date.
- Gold : magasin.

**Unité :** nombre d'unités de produits selon la convention de la source.

**Résultat obtenu :** 33 755 474.

**Limites d'interprétation :**

Une quantité élevée ne signifie pas nécessairement un chiffre d'affaires élevé. Les quantités vendues ne sont pas directement comparables entre des produits de natures différentes.

Le traitement des retours et des quantités négatives doit être interprété selon les règles de nettoyage appliquées au TP3.

Il convient également de distinguer les quantités vendues du nombre de lignes de vente et du nombre de transactions.

### KPI 3 – Nombre de transactions

**Définition métier :**

Nombre de tickets de vente distincts réalisés sur le périmètre étudié.

**Formule de référence :**

Nombre de transactions = Σ par magasin et par date [COUNT(DISTINCT ss_ticket_number)]

Le comptage distinct est réalisé dans chaque groupe magasin/date afin d'éviter de compter plusieurs fois un même ticket comportant plusieurs lignes de produits.

**Champs utilisés :**
- `ss_store_sk` : identifiant du magasin.
- `ss_sold_date_sk` : identifiant de la date de vente.
- `ss_ticket_number` : numéro du ticket.

**Sources :**
- `store_sales` : Silver détaillé, utilisé pour la validation.
- `sales_by_store_date` : Silver transformé, contenant `number_of_tickets`.
- `sales_performance_by_store` : Gold, contenant `number_of_tickets`.

**Filtres appliqués :**

Aucun filtre métier supplémentaire. Les valeurs nulles de `ss_ticket_number` sont contrôlées avant le calcul.

**Granularité :**
- Calcul intermédiaire : magasin/date.
- Résultat global : ensemble des magasins et des dates disponibles.

**Unité :** nombre de tickets / transactions.

**Résultat obtenu :** 89 100.

**Limites d'interprétation :**

Un ticket peut contenir plusieurs lignes de vente et plusieurs produits. Le nombre de tickets ne doit donc pas être confondu avec le nombre de lignes de vente, le nombre d'articles ou le nombre de clients.

Le comptage distinct est réalisé par magasin et date, car un numéro de ticket peut éventuellement être réutilisé dans un autre contexte.

L'indicateur représente les tickets observés dans les données disponibles et ne permet pas, à lui seul, de déterminer le nombre de commandes ou de clients distincts.

## 2.4. Résultats des calculs

Les trois KPI ont été calculés à partir des jeux Silver et Gold.

| KPI | Silver | Gold | Écart |
|---|---:|---:|---:|
| Chiffre d'affaires TTC | 1 202 218 083,00 | 1 202 218 083,00 | 0,00 |
| Quantités vendues | 33 755 474 | 33 755 474 | 0 |
| Nombre de transactions | 89 100 | 89 100 | 0 |

Les résultats obtenus sont identiques entre les deux couches.

## 2.5. Validation du nombre de transactions

Le jeu détaillé `store_sales` contient 667 579 lignes.

Un contrôle préalable a permis de constater :
- aucune valeur nulle dans `ss_ticket_number` 
- 89 100 numéros de tickets distincts sur l'ensemble du fichier

Une vérification complémentaire a ensuite été réalisée en regroupant les ventes par magasin et date, puis en calculant le nombre de tickets distincts dans chaque groupe.

Les résultats ont été comparés avec le champ `number_of_tickets` du jeu Silver transformé.

| Contrôle | Résultat |
|---|---:|
| Nombre de groupes magasin/date comparés | 21 430 |
| Groupes absents de Silver | 0 |
| Groupes absents de la source | 0 |
| Groupes présentant un écart | 0 |

Cette comparaison confirme la cohérence de l'agrégation des tickets entre la source détaillée et le jeu Silver transformé.

Le résultat a également été retrouvé dans le jeu Gold.

## 2.6. Synthèse de validation

| KPI | Disponibilité des champs | Validation | Décision |
|---|---|---|---|
| Chiffre d'affaires TTC | Confirmée | Réconciliation Silver/Gold sans écart | Retenu |
| Quantités vendues | Confirmée | Réconciliation Silver/Gold sans écart | Retenu |
| Nombre de transactions | Confirmée | Comparaison source/Silver/Gold sans écart | Retenu |

Les 3 indicateurs sont retenus pour les analyses métier du TP4.

Le nombre de transactions, initialement considéré comme un indicateur à qualifier, a pu être validé grâce à un contrôle complémentaire sur les données détaillées de ventes.

## 2.7. Conclusion

La vérification du dictionnaire des KPI a permis de retenir 3 indicateurs calculables et cohérents avec les données réellement disponibles.

La réconciliation entre Silver et Gold ne présente aucun écart sur les 3 indicateurs.

Le contrôle complémentaire réalisé sur `store_sales` confirme également que les 89 100 tickets agrégés correspondent au décompte distinct des tickets par magasin et par date.

Ces résultats constituent un socle fiable pour poursuivre les analyses commerciales du TP4, sous réserve des limites d'interprétation documentées pour chaque indicateur.