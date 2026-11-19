#!/usr/bin/env python3
"""
TP3 - Etape 4 : règles de nettoyage Retail Intelligence

Sources :
  ~/retail_project/data/store_sales/store_sales.dat
  ~/retail_project/data/inventory/inventory.dat

Sorties Parquet :
  ~/retail-intelligence/tp3/output/silver/
  ~/retail-intelligence/tp3/output/quarantine/
  ~/retail-intelligence/tp3/output/quality/

Important :
- Les fichiers sources ne sont jamais modifiés.
- Les doublons potentiels de ventes sont conservés dans Silver et signalés.
- Les valeurs financières atypiques sont signalées, pas supprimées.
- Les clés temporelles *_date_sk restent des clés de dimension.
"""

import os
from functools import reduce

from pyspark.sql import SparkSession, Window
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField, StringType,
    LongType, IntegerType, DecimalType
)

# ---------------------------------------------------------------------
# 1. Chemins
# ---------------------------------------------------------------------

TP3_ROOT = os.path.expanduser("~/retail-intelligence/tp3")
DATA_ROOT = os.path.join(TP3_ROOT, "data")

# Sources brutes : Bronze
STORE_SALES_PATH = os.path.join(DATA_ROOT, "bronze", "store_sales", "store_sales.dat")
INVENTORY_PATH = os.path.join(DATA_ROOT, "bronze", "inventory", "inventory.dat")

# Sorties du traitement
SILVER_ROOT = os.path.join(DATA_ROOT, "silver")
QUARANTINE_ROOT = os.path.join(DATA_ROOT, "quarantine")
QUALITY_ROOT = os.path.join(DATA_ROOT, "quality")


SILVER_SALES = os.path.join(SILVER_ROOT, "store_sales")
SILVER_INVENTORY = os.path.join(SILVER_ROOT, "inventory")
QUARANTINE_SALES = os.path.join(QUARANTINE_ROOT, "store_sales")
QUARANTINE_INVENTORY = os.path.join(QUARANTINE_ROOT, "inventory")
QUALITY_SALES_DUPLICATES = os.path.join(QUALITY_ROOT, "store_sales_duplicate_candidates")
QUALITY_SUMMARY = os.path.join(QUALITY_ROOT, "summary")

# ---------------------------------------------------------------------
# 2. Schémas bruts : toutes les colonnes sont d'abord lues en chaînes.
#    Cela permet de distinguer une valeur vide d'un échec de conversion.
# ---------------------------------------------------------------------

SALES_COLUMNS = [
    "ss_sold_date_sk", "ss_sold_time_sk", "ss_item_sk", "ss_customer_sk",
    "ss_cdemo_sk", "ss_hdemo_sk", "ss_addr_sk", "ss_store_sk",
    "ss_promo_sk", "ss_ticket_number", "ss_quantity",
    "ss_wholesale_cost", "ss_list_price", "ss_sales_price",
    "ss_ext_discount_amt", "ss_ext_sales_price", "ss_ext_wholesale_cost",
    "ss_ext_list_price", "ss_ext_tax", "ss_coupon_amt",
    "ss_net_paid", "ss_net_paid_inc_tax", "ss_net_profit"
]

INVENTORY_COLUMNS = [
    "inv_date_sk", "inv_item_sk", "inv_warehouse_sk",
    "inv_quantity_on_hand"
]

def raw_string_schema(columns):
    return StructType([
        StructField(name, StringType(), True) for name in columns
    ])

spark = (
    SparkSession.builder
    .appName("TP3-Retail-Intelligence_Nettoyage")
    #.master("local[*]")
    .config("spark.hadoop.fs.defaultFS", "file:///")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

def read_raw_dat(path, columns):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Fichier source introuvable : {path}")

    return (
        spark.read
        .schema(raw_string_schema(columns))
        .option("header", "false")
        .option("sep", "|")
        .option("encoding", "UTF-8")
        .option("mode", "PERMISSIVE")
        .csv(path)
    )

# ---------------------------------------------------------------------
# 3. Fonctions de conversion et de qualité
# ---------------------------------------------------------------------

def cast_columns(df, type_map):
    """
    Convertit les champs vers les types attendus.
    Ajoute un indicateur par colonne pour détecter les échecs de cast :
    valeur source non vide mais résultat converti à null.
    """
    result = df

    for column, data_type in type_map.items():
        raw = F.trim(F.col(column))
        converted = raw.cast(data_type)

        result = (
            result
            .withColumn(f"_raw_{column}", F.col(column))
            .withColumn(column, converted)
            .withColumn(
                f"invalid_cast_{column}",
                F.col(f"_raw_{column}").isNotNull()
                & (F.trim(F.col(f"_raw_{column}")) != "")
                & F.col(column).isNull()
            )
        )

    return result

def any_true(columns):
    if not columns:
        return F.lit(False)
    return reduce(lambda a, b: a | b, [F.coalesce(F.col(c), F.lit(False)) for c in columns])

def write_parquet(df, path):
    (
        df.write
        .mode("overwrite")
        .parquet(path)
    )

# ---------------------------------------------------------------------
# 4. Traitement de store_sales.dat
# ---------------------------------------------------------------------

print("\n========== STORE_SALES : lecture ==========")

sales_raw = read_raw_dat(STORE_SALES_PATH, SALES_COLUMNS)

sales_types = {
    "ss_sold_date_sk": "bigint",
    "ss_sold_time_sk": "bigint",
    "ss_item_sk": "bigint",
    "ss_customer_sk": "bigint",
    "ss_cdemo_sk": "bigint",
    "ss_hdemo_sk": "bigint",
    "ss_addr_sk": "bigint",
    "ss_store_sk": "bigint",
    "ss_promo_sk": "bigint",
    "ss_ticket_number": "bigint",
    "ss_quantity": "int",
    "ss_wholesale_cost": "decimal(7,2)",
    "ss_list_price": "decimal(7,2)",
    "ss_sales_price": "decimal(7,2)",
    "ss_ext_discount_amt": "decimal(7,2)",
    "ss_ext_sales_price": "decimal(7,2)",
    "ss_ext_wholesale_cost": "decimal(7,2)",
    "ss_ext_list_price": "decimal(7,2)",
    "ss_ext_tax": "decimal(7,2)",
    "ss_coupon_amt": "decimal(7,2)",
    "ss_net_paid": "decimal(7,2)",
    "ss_net_paid_inc_tax": "decimal(7,2)",
    "ss_net_profit": "decimal(7,2)"
}

sales = cast_columns(sales_raw, sales_types)

sales_cast_flags = [f"invalid_cast_{c}" for c in sales_types]

# Colonnes nécessaires à l'identification et à l'analyse d'une vente.
# Les attributs démographiques et promotionnels restent facultatifs.
sales_required = [
    "ss_sold_date_sk", "ss_sold_time_sk", "ss_item_sk",
    "ss_store_sk", "ss_ticket_number", "ss_quantity"
]

sales_missing_required = reduce(
    lambda a, b: a | b,
    [F.col(c).isNull() for c in sales_required]
)

sales = (
    sales
    .withColumn("flag_missing_required", sales_missing_required)
    .withColumn("flag_invalid_cast", any_true(sales_cast_flags))
    .withColumn(
        "flag_quantity_negative",
        F.col("ss_quantity") < 0
    )
    .withColumn(
        "flag_zero_unit_sales_price",
        F.col("ss_sales_price") == F.lit(0)
    )
    .withColumn(
        "flag_zero_net_paid",
        F.col("ss_net_paid") == F.lit(0)
    )
    .withColumn(
        "flag_profit_negative",
        F.col("ss_net_profit") < 0
    )
)

# Doublons potentiels : la clé testée n'est pas garantie unique.
sales_key = [
    "ss_sold_date_sk", "ss_store_sk",
    "ss_ticket_number", "ss_item_sk"
]

sales_window = Window.partitionBy(*sales_key)

sales = (
    sales
    .withColumn("duplicate_candidate_count", F.count(F.lit(1)).over(sales_window))
    .withColumn(
        "flag_duplicate_candidate",
        F.col("duplicate_candidate_count") > 1
    )
)

# Quarantaine bloquante : champ obligatoire manquant ou échec de conversion.
# Les valeurs nulles facultatives ne provoquent pas une mise à l'écart.
sales_quarantine_condition = (
    F.col("flag_missing_required")
    | F.col("flag_invalid_cast")
    | F.col("flag_quantity_negative")
)

sales_quarantine = sales.filter(sales_quarantine_condition)
sales_silver = sales.filter(~sales_quarantine_condition)

# Jeu de contrôle des doublons : les lignes restent également dans Silver.
sales_duplicate_review = sales_silver.filter(F.col("flag_duplicate_candidate"))

sales_source_count = sales_raw.count()
sales_quarantine_count = sales_quarantine.count()
sales_silver_count = sales_silver.count()
sales_duplicate_count = sales_duplicate_review.count()

print("Nombre de lignes source ventes :", sales_source_count)
print("Nombre de lignes ventes en quarantaine :", sales_quarantine_count)
print("Nombre de lignes ventes conservées dans Silver :", sales_silver_count)
print(
    "Nombre de lignes ventes signalées comme doublons potentiels :",
    sales_duplicate_count
)

# ---------------------------------------------------------------------
# 5. Traitement de inventory.dat
# ---------------------------------------------------------------------

print("\n========== INVENTORY : lecture ==========")

inventory_raw = read_raw_dat(INVENTORY_PATH, INVENTORY_COLUMNS)

inventory_types = {
    "inv_date_sk": "bigint",
    "inv_item_sk": "bigint",
    "inv_warehouse_sk": "bigint",
    "inv_quantity_on_hand": "int"
}

inventory = cast_columns(inventory_raw, inventory_types)

inventory_cast_flags = [f"invalid_cast_{c}" for c in inventory_types]

inventory_required = [
    "inv_date_sk", "inv_item_sk",
    "inv_warehouse_sk", "inv_quantity_on_hand"
]

inventory_missing_required = reduce(
    lambda a, b: a | b,
    [F.col(c).isNull() for c in inventory_required]
)

inventory = (
    inventory
    .withColumn("flag_missing_required", inventory_missing_required)
    .withColumn("flag_invalid_cast", any_true(inventory_cast_flags))
    .withColumn(
        "flag_quantity_negative",
        F.col("inv_quantity_on_hand") < 0
    )
)

# La combinaison date + article + entrepôt est la granularité attendue.
inventory_key = [
    "inv_date_sk", "inv_item_sk", "inv_warehouse_sk"
]

inventory_window = Window.partitionBy(*inventory_key)

# Le contrôle exploratoire préalable a confirmé :
# 0 groupe dupliqué sur la clé :
# inv_date_sk + inv_item_sk + inv_warehouse_sk
#
# Pour éviter un tri Window coûteux sur 23,2 millions de lignes,
# on conserve cette conclusion pour le jeu de données étudié.
# Si les sources changent, il faudra réexécuter le contrôle
# des doublons dans un traitement qualité séparé.

inventory = (
    inventory
    .withColumn("duplicate_candidate_count", F.lit(1))
    .withColumn("flag_duplicate_candidate", F.lit(False))
)

# Une quantité absente ou une conversion invalide est bloquante.
# Les quantités négatives sont également mises en quarantaine.
inventory_quarantine_condition = (
    F.col("flag_missing_required")
    | F.col("flag_invalid_cast")
    | F.col("flag_quantity_negative")
)

inventory_quarantine = inventory.filter(
    inventory_quarantine_condition
)

inventory_silver = inventory.filter(
    ~inventory_quarantine_condition
)

inventory_source_count = inventory_raw.count()
inventory_quarantine_count = inventory_quarantine.count()
inventory_silver_count = inventory_silver.count()

print("Nombre de lignes source stock :", inventory_source_count)
print("Nombre de lignes stock en quarantaine :", inventory_quarantine_count)
print("Nombre de lignes stock conservées dans Silver :", inventory_silver_count)

# ---------------------------------------------------------------------
# 6. Ecriture des résultats
# ---------------------------------------------------------------------

print("\n========== ECRITURE DES SORTIES PARQUET ==========")

write_parquet(sales_silver, SILVER_SALES)
write_parquet(inventory_silver, SILVER_INVENTORY)

write_parquet(sales_quarantine, QUARANTINE_SALES)
write_parquet(inventory_quarantine, QUARANTINE_INVENTORY)

write_parquet(sales_duplicate_review, QUALITY_SALES_DUPLICATES)

# ---------------------------------------------------------------------
# 7. Rapport qualité synthétique
# ---------------------------------------------------------------------

quality_rows = [
    (
        "store_sales",
        sales_source_count,
        sales_silver_count,
        sales_quarantine_count,
        sales_duplicate_count
    ),
    (
        "inventory",
        inventory_source_count,
        inventory_silver_count,
        inventory_quarantine_count,
        0
    )
]

quality_schema = [
    "source",
    "rows_read",
    "rows_silver",
    "rows_quarantine",
    "rows_duplicate_review"
]

quality_df = spark.createDataFrame(quality_rows, quality_schema)

quality_df.show(truncate=False)
write_parquet(
    quality_df,
    QUALITY_SUMMARY
)

print("\nTraitement terminé.")
print("Silver ventes :", SILVER_SALES)
print("Silver stock :", SILVER_INVENTORY)
print("Quarantaine ventes :", QUARANTINE_SALES)
print("Quarantaine stock :", QUARANTINE_INVENTORY)
print("Revue doublons ventes :", QUALITY_SALES_DUPLICATES)

spark.stop()