# Étape 5 – Produire des visualisations

Trois supports de visualisation ont été produits afin de faciliter l'analyse des performances commerciales du jeu de données Retail Intelligence : deux diagrammes en barres et un tableau de synthèse.

## 5.1. Chiffre d'affaires TTC par magasin

**Type de visualisation :** diagramme en barres verticales.

**Objectif :** comparer le chiffre d'affaires TTC réalisé par les différents magasins et identifier ceux qui présentent les valeurs les plus élevées et les plus faibles.

**Source de données :** `silver-transformed/sales_by_store_date`.

**Transformation réalisée :** somme de `total_revenue_inc_tax`, regroupée par `store_sk`.

**Axes :**
- Axe horizontal : identifiant du magasin (`store_sk`).
- Axe vertical : chiffre d'affaires TTC, dans l'unité monétaire du jeu de données.

**Interprétation :**

Le magasin 7 présente le chiffre d'affaires TTC le plus élevé, avec 103 384 198,80. À l'inverse, le magasin 2 présente le chiffre d'affaires le plus faible, avec 98 249 685,02.

Les valeurs des 12 magasins restent relativement proches. Le diagramme permet de visualiser rapidement leur classement et les écarts de chiffre d'affaires.

## 5.2. Top 10 des produits les plus vendus

**Type de visualisation :** diagramme en barres horizontales.

**Objectif :** identifier les dix produits présentant les plus grandes quantités vendues sur l'ensemble des magasins.

**Source de données :** `silver/store_sales`.

**Transformation réalisée :** somme de `ss_quantity`, regroupée par `ss_item_sk`, puis sélection des dix produits ayant les quantités vendues les plus élevées.

**Axes :**
- Axe horizontal : quantités vendues, en unités.
- Axe vertical : identifiant du produit (`ss_item_sk`).

**Interprétation :**

Le produit 10000 arrive en première position avec 454 954 unités vendues. Il est suivi du produit 10003 avec 439 086 unités, puis du produit 10001 avec 420 138 unités.

Les quatre premiers produits se distinguent nettement des six autres produits du classement. Cette visualisation permet donc de repérer les références associées aux plus grands volumes de vente.

## 5.3. Tableau de synthèse du chiffre d'affaires par magasin

**Type de visualisation :** tableau de synthèse.

**Objectif :** compléter le diagramme du chiffre d'affaires par magasin avec les valeurs précises et le classement des magasins.

**Source de données :** `silver-transformed/sales_by_store_date`.

**Indicateurs présentés :**
- Rang du magasin selon son chiffre d'affaires.
- Identifiant du magasin.
- Chiffre d'affaires TTC.
- Part du magasin dans le chiffre d'affaires global.

Le tableau permet de retrouver les valeurs exactes et de comparer les contributions de chaque magasin au chiffre d'affaires global. Il complète ainsi la lecture visuelle du diagramme en barres.

## Conclusion

Les visualisations produites sont complémentaires. Le premier graphique compare les performances commerciales des magasins, le deuxième met en évidence les produits les plus vendus en volume et le tableau fournit une synthèse chiffrée du chiffre d'affaires par magasin.

Elles constituent des supports de lecture et d'exploration des données avant la formulation des constats métier.

---

# Étape 6 – Formuler des constats métier

Les constats suivants sont issus des agrégations réalisées sur les données du jeu TPCx-BB synthétique. Ils doivent être interprétés comme des résultats d'analyse pédagogique et non comme des observations réelles d'une entreprise.

## Constat 1 – Les chiffres d'affaires des magasins sont relativement proches

**Résultat observé :**

Le magasin 7 réalise le chiffre d'affaires TTC le plus élevé, avec 103 384 198,80, soit environ 8,60 % du chiffre d'affaires global.

Le magasin 2 présente le chiffre d'affaires le plus faible, avec 98 249 685,02, soit environ 8,17 % du total.

L'écart entre ces deux magasins est de 5 134 513,78, ce qui représente environ 5,23 % du chiffre d'affaires du magasin 2.

**Interprétation possible :**

Les chiffres d'affaires des magasins sont relativement homogènes à l'échelle du jeu de données. Aucun magasin ne semble représenter à lui seul une part dominante du chiffre d'affaires global.

Le magasin 7 se distingue néanmoins par sa première position dans le classement.

**Limite de l'analyse :**

Cette comparaison porte uniquement sur le chiffre d'affaires cumulé. Elle ne tient pas compte des différences éventuelles de taille des magasins, de fréquentation, de coûts d'exploitation ou de contexte commercial.

Les résultats ne permettent donc pas d'expliquer les écarts observés ni d'affirmer qu'un magasin est plus rentable qu'un autre.

**Recommandation éventuelle :**

Approfondir la comparaison en étudiant le chiffre d'affaires par période, le nombre de tickets, les quantités vendues et, si les données sont disponibles, les coûts et les caractéristiques des magasins.

## Constat 2 – Quatre produits concentrent les plus grands volumes de vente

**Résultat observé :**

Le classement des dix produits les plus vendus fait apparaître quatre références nettement en tête :

- Produit 10000 : 454 954 unités.
- Produit 10003 : 439 086 unités.
- Produit 10001 : 420 138 unités.
- Produit 10002 : 377 027 unités.

Le cinquième produit du classement, identifié par la clé 5618, totalise 95 677 unités.

**Interprétation possible :**

Les quatre premières références présentent des volumes de vente particulièrement élevés par rapport aux autres produits du Top 10. Elles pourraient donc représenter des références importantes à suivre dans une analyse commerciale ou dans une réflexion sur la gestion des stocks.

**Limite de l'analyse :**

Le classement repose sur les quantités vendues cumulées sur l'ensemble des magasins. Il ne permet pas de mesurer la vitesse de vente, l'évolution de la demande ou le risque de rupture de stock.

De plus, les identifiants utilisés sont des clés techniques. Les noms commerciaux des produits ne sont pas disponibles dans cette visualisation.

**Recommandation éventuelle :**

Rapprocher ces résultats du référentiel produit afin d'obtenir les noms des références. Étudier ensuite les ventes par période et par magasin, puis les comparer aux niveaux de stock disponibles pour identifier les besoins éventuels de réapprovisionnement.

## Constat 3 – Le classement global ne suffit pas à expliquer les performances locales des produits

**Résultat observé :**

Le graphique des produits présente un classement global calculé sur l'ensemble des magasins. Les résultats détaillés par magasin obtenus précédemment montrent que les produits 10000, 10003, 10001 et 10002 figurent systématiquement parmi les quatre premières positions de chaque magasin.

Le produit 10000 ou le produit 10003 occupe la première position dans chacun des douze magasins.

**Interprétation possible :**

Les quatre références semblent présenter une importance commerciale récurrente dans les différents magasins du jeu de données. Leur présence dans les premières positions ne paraît donc pas limitée à un seul magasin.

**Limite de l'analyse :**

Le classement repose sur les quantités cumulées. Il ne permet pas de comparer les évolutions dans le temps, les différences de comportement des clients ou les spécificités locales de chaque magasin.

Il ne démontre pas non plus que ces produits ont les mêmes performances relatives sur toutes les périodes.

**Recommandation éventuelle :**

Construire une analyse des quantités vendues par produit, par magasin et par période afin d'identifier les éventuelles différences locales et les évolutions de la demande.

## Précaution générale d'interprétation

Les données utilisées proviennent du jeu TPCx-BB, qui est synthétique. Les constats formulés servent à illustrer une démarche d'analyse décisionnelle et ne doivent pas être présentés comme des conclusions sur une entreprise réelle.

Par ailleurs, les résultats observés décrivent des associations et des différences entre indicateurs. Ils ne permettent pas d'établir une relation de causalité.