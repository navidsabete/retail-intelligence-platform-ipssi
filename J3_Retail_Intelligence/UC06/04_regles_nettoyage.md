# Étape 4 : Définition et application des règles de nettoyage

## 1. Objectif

À la suite de l'inventaire technique (étape 2) et de l'exploration PySpark (étape 3), cette étape définit les règles de nettoyage applicables aux deux sources retenues pour le projet Retail Intelligence Platform :

- `store_sales.dat` : ventes réalisées en magasin ;
- `inventory.dat` : quantités en stock par produit, entrepôt et date.

L'objectif est de préparer des données fiables pour la couche Silver, tout en conservant la traçabilité des anomalies et en évitant les corrections qui ne seraient pas justifiées par le métier.

**Principe retenu :** une anomalie détectée n'entraîne pas automatiquement la suppression ou la modification d'une valeur. Les enregistrements sont conservés, signalés ou mis à l'écart selon la gravité et la signification de l'anomalie.

## 2. Sources et constats issus de l'étape 3

| Indicateur | `store_sales.dat` | `inventory.dat` |
|---|---:|---:|
| Nombre de lignes de référence | 667 579 | 23 255 100 |
| Nombre de colonnes | 23 | 4 |
| Valeurs nulles constatées | 1 139 | 5 999 |
| Groupes en doublon sur la clé candidate testée | 4 038 | 0 |
| Lignes appartenant aux groupes en doublon | 8 174 | 0 |
| Quantités négatives | 0 | 0 |

Pour `store_sales.dat`, les valeurs nulles concernent `ss_cdemo_sk` (238), `ss_hdemo_sk` (295), `ss_addr_sk` (448) et `ss_promo_sk` (158).

Pour `inventory.dat`, les 5 999 valeurs nulles concernent `inv_quantity_on_hand`.

La clé candidate testée pour les ventes est composée de `ss_sold_date_sk`, `ss_store_sk`, `ss_ticket_number` et `ss_item_sk`. Elle n'est pas unique sur les données observées. La clé candidate du stock (`inv_date_sk`, `inv_item_sk`, `inv_warehouse_sk`) ne présente aucun groupe en doublon lors du contrôle réalisé.

L'exploration des ventes a également identifié des prix de vente unitaires nuls, des montants nets payés nuls et des bénéfices négatifs. Ces situations sont signalées, mais ne sont pas considérées automatiquement comme des erreurs.

## 3. Règles de nettoyage retenues

### 3.1. Tableau des règles

| Anomalie | Règle | Action appliquée | Justification |
|---|---|---|---|
| Valeur manquante dans une colonne descriptive facultative des ventes (`ss_cdemo_sk`, `ss_hdemo_sk`, `ss_addr_sk`, `ss_promo_sk`) | Autoriser le null et le signaler | Conserver la ligne et la valeur null ; ne pas remplacer par 0 | L'absence d'une information démographique, d'adresse ou de promotion peut être légitime. Le remplacement par 0 créerait une information artificielle. |
| Valeur manquante dans une colonne obligatoire des ventes (date, produit, magasin, ticket ou quantité) | Une ligne sans information indispensable à son interprétation n'est pas intégrée directement à Silver | Mettre la ligne en quarantaine et documenter le motif | Ces champs sont nécessaires pour identifier et analyser une vente. Aucun cas de ce type n'a été constaté dans les contrôles initiaux. |
| Valeur manquante dans `inventory.inv_quantity_on_hand` | Une quantité inconnue ne doit pas être assimilée à zéro | Mettre la ligne en quarantaine pour traitement complémentaire | Une quantité nulle signifie « aucun stock », alors qu'une valeur manquante signifie « stock inconnu ». Les deux situations sont différentes. |
| Type incorrect ou valeur non convertible | Convertir selon le schéma TPCx-BB ; repérer les échecs de conversion | Mettre en quarantaine les lignes comportant une conversion impossible sur un champ typé | Éviter les calculs sur des chaînes ou des valeurs mal interprétées. Les conversions sont réalisées explicitement. |
| Doublon potentiel dans les ventes | Contrôler la clé candidate complète ; ne pas supposer qu'elle est unique | Conserver les lignes dans Silver avec un indicateur de doublon ; produire un jeu de lignes à examiner | Les 4 038 groupes observés ne prouvent pas que les lignes sont des copies exactes. Une suppression automatique pourrait faire perdre des ventes valides. |
| Doublon dans les stocks | La combinaison date + produit + entrepôt doit être unique | Signaler et mettre en quarantaine les lignes appartenant à un groupe dupliqué si un tel cas apparaît | La granularité attendue est une observation de stock par produit, entrepôt et date. Aucun doublon n'a été observé à l'étape 3. |
| Identifiant obligatoire manquant | Les clés de date, produit, magasin, ticket et entrepôt doivent être présentes selon la source | Mettre en quarantaine les lignes dont une clé obligatoire est absente | Sans ces clés, les jointures et agrégations métier ne sont pas fiables. |
| Identifiant non référencé | Vérifier les clés avec les dimensions de référence lorsqu'elles seront disponibles | Signaler les clés non retrouvées ; ne pas inventer de correspondance | La validation d'existence nécessite les dimensions (`item`, `store`, `date`, `warehouse`, etc.). Elle ne peut pas être conclue avec les deux seuls fichiers. |
| Date incohérente | Les champs `*_date_sk` sont des clés de dimension, pas des dates calendaires | Conserver les clés et prévoir une jointure avec `date_dim.dat` ; ne pas les convertir directement en date | Une clé de dimension ne doit pas être interprétée comme un format de date. |
| Prix de vente ou montant net égal à zéro | Signaler les valeurs nulles en montant pour analyse métier | Conserver et ajouter des indicateurs de qualité | Une gratuité, une promotion ou une opération particulière peut produire un montant nul. |
| Bénéfice net négatif | Conserver les valeurs négatives et les signaler | Ne pas supprimer ni remplacer la valeur ; conserver un indicateur `flag_profit_negative` | Une vente à perte ou une règle de remise peut expliquer un bénéfice négatif. |
| Quantité négative | Signaler toute quantité négative pour investigation | Ne pas supprimer automatiquement ; mettre en quarantaine pour validation métier si le cas apparaît | Une valeur négative peut représenter un retour ou une correction. Aucun cas n'a été détecté à l'étape 3. |
| Format des fichiers | Utiliser le séparateur `|`, sans en-tête, et un schéma explicite | Harmoniser les types et produire les sorties Silver au format Parquet | Le format Parquet facilite les lectures analytiques et conserve les types. |

### 3.2. Règles spécifiques à `store_sales.dat`

1. Convertir les 23 colonnes selon le schéma TPCx-BB.
2. Conserver les valeurs nulles des colonnes facultatives démographiques et promotionnelles.
3. Mettre à l'écart les lignes dont une clé ou une quantité obligatoire est absente ou non convertible.
4. Identifier les groupes dupliqués avec la clé candidate `ss_sold_date_sk + ss_store_sk + ss_ticket_number + ss_item_sk`.
5. Conserver les lignes des groupes dupliqués dans la sortie Silver, avec un indicateur de doublon, tant que leur signification n'est pas établie.
6. Signaler les prix unitaires nuls, les montants nets nuls et les bénéfices négatifs sans les supprimer.
7. Conserver les clés temporelles ; leur interprétation calendaire sera faite par jointure avec les dimensions.

### 3.3. Règles spécifiques à `inventory.dat`

1. Convertir les quatre colonnes selon le schéma TPCx-BB.
2. Exiger la présence des trois identifiants : date, produit et entrepôt.
3. Mettre en quarantaine les lignes dont `inv_quantity_on_hand` est null ou non convertible.
4. Contrôler l'unicité de la combinaison `inv_date_sk + inv_item_sk + inv_warehouse_sk`.
5. Signaler les quantités négatives pour investigation, sans les supprimer automatiquement.
6. Conserver la clé de date pour une future jointure avec `date_dim.dat`.

## 4. Mise en œuvre PySpark

Le traitement est fourni dans un script distinct du notebook d'exploration :

`etape4_nettoyage.py`

Le script réalise les opérations suivantes :

- lecture des fichiers DAT avec le séparateur `|` et sans en-tête ;
- lecture initiale des champs en chaînes pour contrôler les conversions ;
- conversion explicite vers les types attendus ;
- création d'indicateurs de qualité ;
- mise à l'écart des lignes dont les champs obligatoires sont absents ou non convertibles ;
- détection des groupes en doublon ;
- conservation des doublons potentiels des ventes avec un indicateur ;
- mise à l'écart des doublons de stock si de nouveaux cas sont détectés ;
- signalement des prix nuls, montants nuls, bénéfices négatifs et quantités négatives ;
- écriture des données préparées en Parquet.

Les données sont écrites dans des répertoires distincts :

- `output/silver/store_sales/`
- `output/silver/inventory/`
- `output/quarantine/store_sales/`
- `output/quarantine/inventory/`
- `output/quality/` pour les lignes de ventes à examiner en raison d'un doublon potentiel.

Les lignes de ventes présentant un doublon potentiel ne sont pas supprimées de Silver : elles sont également identifiées dans un jeu de contrôle afin de permettre une analyse ultérieure.

## 5. Limites et précautions

- Les clés candidates ne sont pas nécessairement des clés primaires garanties par la documentation. Leur unicité est évaluée sur les données observées.
- La validation des identifiants par rapport aux dimensions nécessite de charger les fichiers de référence correspondants. Elle n'est pas considérée comme réalisée dans ce traitement.
- Les clés temporelles ne sont pas converties directement en dates.
- Les valeurs nulles facultatives sont conservées.
- Les valeurs financières atypiques sont signalées, mais ne sont pas corrigées automatiquement.
- Les doublons de ventes sont conservés tant que leur origine n'est pas comprise.
- Les sorties Parquet sont des données préparées pour la couche Silver ; elles ne remplacent pas les fichiers sources Raw.

## 6. Résultats attendus et vérifications après exécution

Après exécution du script, vérifier :

1. Le nombre de lignes lues pour chaque source.
2. Le nombre de lignes envoyées en quarantaine.
3. Le nombre de groupes de doublons détectés.
4. Le nombre de lignes conservées dans les sorties Silver.
5. La présence des indicateurs de qualité dans les schémas Parquet.
6. La possibilité de relire les fichiers Parquet avec PySpark.

Les résultats exacts du traitement doivent être reportés dans le compte rendu après exécution. Ils ne sont pas présumés dans ce document.

## 7. Conclusion

Les règles de nettoyage ont été définies à partir des anomalies réellement observées pendant l'exploration.

La stratégie privilégie la conservation des données et la traçabilité : les valeurs manquantes facultatives et les valeurs financières atypiques sont conservées et signalées ; les enregistrements incomplets sur des champs indispensables ou non convertibles sont mis à l'écart ; les doublons de ventes sont identifiés sans suppression automatique.

Le script PySpark applique ces règles et prépare les deux sources au format Parquet pour la suite du projet, en particulier la constitution de la couche Silver puis des indicateurs Gold.
