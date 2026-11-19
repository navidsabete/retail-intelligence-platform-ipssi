
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TP3 - Retail Intelligence Platform
Étapes 5 et 6 : transformations métier et production des jeux Silver.

Sources nettoyées :
    data/silver/store_sales
    data/silver/inventory

Résultats :
    data/silver-transformed/

Format de sortie :
    Parquet avec compression Snappy

Les données Raw/Bronze et Silver de l'étape 4 ne sont jamais modifiées.
"""

import os
from pathlib import Path

from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import NumericType


# ============================================================
# 1. CONFIGURATION DES CHEMINS
# ============================================================

ROOT = Path(
    os.environ.get(
        "TP3_ROOT",
        str(Path.home() / "retail-intelligence" / "tp3")
    )
).expanduser()

# Entrées nettoyées à l'étape 4
INPUT_ROOT = Path(
    os.environ.get(
        "TP3_STEP4_SILVER_ROOT",
        str(ROOT / "data" / "silver")
    )
).expanduser()

# Sorties transformées des étapes 5 et 6
OUTPUT_ROOT = Path(
    os.environ.get(
        "TP3_OUTPUT_SILVER",
        str(ROOT / "data" / "silver-transformed")
    )
).expanduser()

SALES_PATH = INPUT_ROOT / "store_sales"
INVENTORY_PATH = INPUT_ROOT / "inventory"

SALES_BRONZE_SOURCE = (
    ROOT / "data" / "bronze" / "store_sales" / "store_sales.dat"
)

INVENTORY_BRONZE_SOURCE = (
    ROOT / "data" / "bronze" / "inventory" / "inventory.dat"
)

APP_NAME = "TP3-Retail-Intelligence-Etapes5-6"


# ============================================================
# 2. FONCTIONS UTILITAIRES
# ============================================================

def require_columns(df, required, label):
    """Vérifie la présence des colonnes nécessaires."""

    missing = [column for column in required if column not in df.columns]

    if missing:
        raise ValueError(
            f"{label} : colonnes absentes : {missing}"
        )


def require_numeric_columns(df, columns, label):
    """Vérifie que les colonnes demandées sont numériques."""

    for column in columns:
        if not isinstance(df.schema[column].dataType, NumericType):
            raise TypeError(
                f"{label} : la colonne {column} doit être numérique."
            )


def add_provenance(df, dataset_name, source_path):
    """Ajoute les informations de provenance et de traitement."""

    return (
        df
        .withColumn("_source_dataset", F.lit(dataset_name))
        .withColumn("_source_original_file", F.lit(str(source_path)))
        .withColumn("_processing_stage", F.lit(APP_NAME))
    )


def write_and_verify(df, dataset_name, spark):
    """
    Écrit un DataFrame en Parquet puis relit le résultat.

    Vérifie :
    - le nombre de lignes ;
    - le nombre de colonnes ;
    - la lisibilité du fichier écrit.
    """

    output_path = OUTPUT_ROOT / dataset_name

    expected_count = df.count()

    (
        df.write
        .mode("overwrite")
        .format("parquet")
        .option("compression", "snappy")
        .save(str(output_path))
    )

    reread = spark.read.parquet(str(output_path))

    actual_count = reread.count()

    print(
        f"{dataset_name} : "
        f"attendu={expected_count} | "
        f"relu={actual_count} | "
        f"colonnes={len(reread.columns)} | "
        f"chemin={output_path}"
    )

    if actual_count != expected_count:
        raise RuntimeError(
            f"Écart de comptage après écriture pour {dataset_name}"
        )

    if reread.columns != df.columns:
        raise RuntimeError(
            f"Écart de schéma après écriture pour {dataset_name}"
        )

    return {
        "dataset": dataset_name,
        "rows": actual_count,
        "columns": len(reread.columns),
        "path": str(output_path)
    }


# ============================================================
# 3. INITIALISATION SPARK ET LECTURE
# ============================================================

def main():

    spark = (
        SparkSession.builder
        .appName(APP_NAME)
        .config("spark.hadoop.fs.defaultFS", "file:///")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    try:

        print("\n========== CONFIGURATION ==========")
        print(f"Racine du projet : {ROOT}")
        print(f"Entrée Silver : {INPUT_ROOT}")
        print(f"Sortie transformée : {OUTPUT_ROOT}")

        if not SALES_PATH.exists():
            raise FileNotFoundError(
                f"Source ventes introuvable : {SALES_PATH}"
            )

        if not INVENTORY_PATH.exists():
            raise FileNotFoundError(
                f"Source stock introuvable : {INVENTORY_PATH}"
            )

        print("\n========== LECTURE DES SOURCES SILVER ==========")

        sales = spark.read.parquet(str(SALES_PATH))
        inventory = spark.read.parquet(str(INVENTORY_PATH))

        # Vérification des colonnes ventes
        require_columns(
            sales,
            [
                "ss_sold_date_sk",
                "ss_sold_time_sk",
                "ss_item_sk",
                "ss_store_sk",
                "ss_ticket_number",
                "ss_quantity",
                "ss_net_paid",
                "ss_net_paid_inc_tax",
                "ss_net_profit"
            ],
            "store_sales"
        )

        # Vérification des colonnes stock
        require_columns(
            inventory,
            [
                "inv_date_sk",
                "inv_item_sk",
                "inv_warehouse_sk",
                "inv_quantity_on_hand"
            ],
            "inventory"
        )

        # Vérification des types numériques
        require_numeric_columns(
            sales,
            [
                "ss_quantity",
                "ss_net_paid",
                "ss_net_paid_inc_tax",
                "ss_net_profit"
            ],
            "store_sales"
        )

        require_numeric_columns(
            inventory,
            ["inv_quantity_on_hand"],
            "inventory"
        )

        sales_count = sales.count()
        inventory_count = inventory.count()

        print(f"Nombre de lignes ventes : {sales_count}")
        print(f"Nombre de lignes stock : {inventory_count}")


        # ====================================================
        # 4. JEUX DÉTAILLÉS AVEC PROVENANCE
        # ====================================================

        print("\n========== JEUX DÉTAILLÉS ==========")

        sales_detail = add_provenance(
            sales,
            "store_sales",
            SALES_BRONZE_SOURCE
        )

        inventory_detail = add_provenance(
            inventory,
            "inventory",
            INVENTORY_BRONZE_SOURCE
        )


        # ====================================================
        # 5. AGRÉGATION DU CHIFFRE D'AFFAIRES PAR MAGASIN
        # ====================================================

        print("\n========== VENTES PAR MAGASIN ==========")

        # Granularité : une ligne par magasin.
        #
        # ss_net_paid_inc_tax : montant net payé TTC.
        # ss_net_paid : montant net payé hors taxe.
        # ss_net_profit : bénéfice net.
        # ss_quantity : quantité vendue.

        sales_by_store = (
            sales
            .groupBy("ss_store_sk")
            .agg(
                F.sum("ss_net_paid_inc_tax").alias(
                    "total_revenue_inc_tax"
                ),
                F.sum("ss_net_paid").alias(
                    "total_net_paid"
                ),
                F.sum("ss_net_profit").alias(
                    "total_net_profit"
                ),
                F.sum("ss_quantity").alias(
                    "total_quantity_sold"
                ),
                F.count(F.lit(1)).alias(
                    "number_of_sales_lines"
                ),
                F.countDistinct("ss_ticket_number").alias(
                    "number_of_tickets"
                )
            )
            .withColumnRenamed(
                "ss_store_sk",
                "store_sk"
            )
            .withColumn(
                "_grain",
                F.lit("un magasin")
            )
        )

        sales_by_store = add_provenance(
            sales_by_store,
            "store_sales",
            SALES_BRONZE_SOURCE
        )

        sales_by_store.orderBy(
            F.desc("total_revenue_inc_tax")
        ).show(20, truncate=False)


        # ====================================================
        # 6. AGRÉGATION DES VENTES PAR MAGASIN ET DATE
        # ====================================================

        print("\n========== VENTES PAR MAGASIN ET DATE ==========")

        # Granularité : une ligne par magasin et date.
        #
        # La clé date_sk est conservée :
        # elle devra être reliée à date_dim pour obtenir
        # une date calendrier lisible.

        sales_by_store_date = (
            sales
            .groupBy(
                "ss_store_sk",
                "ss_sold_date_sk"
            )
            .agg(
                F.sum("ss_net_paid_inc_tax").alias(
                    "total_revenue_inc_tax"
                ),
                F.sum("ss_net_paid").alias(
                    "total_net_paid"
                ),
                F.sum("ss_net_profit").alias(
                    "total_net_profit"
                ),
                F.sum("ss_quantity").alias(
                    "total_quantity_sold"
                ),
                F.count(F.lit(1)).alias(
                    "number_of_sales_lines"
                ),
                F.countDistinct("ss_ticket_number").alias(
                    "number_of_tickets"
                )
            )
            .withColumnRenamed(
                "ss_store_sk",
                "store_sk"
            )
            .withColumnRenamed(
                "ss_sold_date_sk",
                "date_sk"
            )
            .withColumn(
                "_grain",
                F.lit("un magasin par date")
            )
        )

        sales_by_store_date = add_provenance(
            sales_by_store_date,
            "store_sales",
            SALES_BRONZE_SOURCE
        )


        # ====================================================
        # 7. AGRÉGATION DES VENTES PAR ARTICLE ET DATE
        # ====================================================

        print("\n========== VENTES PAR ARTICLE ET DATE ==========")

        # Granularité : une ligne par article et date.
        #
        # Cet indicateur permettra d'étudier :
        # - les produits les plus vendus ;
        # - les quantités vendues par date ;
        # - les évolutions des ventes après enrichissement
        #   avec la dimension calendrier.

        sales_by_item_date = (
            sales
            .groupBy(
                "ss_item_sk",
                "ss_sold_date_sk"
            )
            .agg(
                F.sum("ss_net_paid_inc_tax").alias(
                    "total_revenue_inc_tax"
                ),
                F.sum("ss_net_paid").alias(
                    "total_net_paid"
                ),
                F.sum("ss_net_profit").alias(
                    "total_net_profit"
                ),
                F.sum("ss_quantity").alias(
                    "total_quantity_sold"
                ),
                F.count(F.lit(1)).alias(
                    "number_of_sales_lines"
                ),
                F.countDistinct(
                    "ss_store_sk",
                    "ss_ticket_number"
                ).alias(
                    "number_of_tickets"
                )
            )
            .withColumnRenamed(
                "ss_item_sk",
                "item_sk"
            )
            .withColumnRenamed(
                "ss_sold_date_sk",
                "date_sk"
            )
            .withColumn(
                "_grain",
                F.lit("un article par date")
            )
        )

        sales_by_item_date = add_provenance(
            sales_by_item_date,
            "store_sales",
            SALES_BRONZE_SOURCE
        )

        sales_by_item_date.orderBy(
            F.desc("total_quantity_sold")
        ).show(20, truncate=False)


        # ====================================================
        # 8. AGRÉGATION DU STOCK PAR ARTICLE ET DATE
        # ====================================================

        print("\n========== STOCK PAR ARTICLE ET DATE ==========")

        # La source inventory peut contenir plusieurs
        # entrepôts pour un même article et une même date.
        #
        # On agrège donc le stock avant la jointure.
        #
        # Granularité : un article par date,
        # tous entrepôts confondus.

        inventory_by_item_date = (
            inventory
            .groupBy(
                "inv_item_sk",
                "inv_date_sk"
            )
            .agg(
                F.sum("inv_quantity_on_hand").alias(
                    "total_quantity_on_hand"
                ),
                F.countDistinct("inv_warehouse_sk").alias(
                    "number_of_warehouses"
                ),
                F.count(F.lit(1)).alias(
                    "number_of_inventory_records"
                )
            )
            .withColumnRenamed(
                "inv_item_sk",
                "item_sk"
            )
            .withColumnRenamed(
                "inv_date_sk",
                "date_sk"
            )
            .withColumn(
                "_grain",
                F.lit("un article par date, tous entrepôts")
            )
        )

        inventory_by_item_date = add_provenance(
            inventory_by_item_date,
            "inventory",
            INVENTORY_BRONZE_SOURCE
        )


        # ====================================================
        # 9. JOINTURE VENTES ET STOCK
        # ====================================================

        print("\n========== JOINTURE VENTES ET STOCK ==========")

        # Sources :
        # - ventes agrégées par article et date ;
        # - stock agrégé par article et date.
        #
        # Clés :
        # - item_sk ;
        # - date_sk.
        #
        # Nature :
        # - jointure gauche (left join).
        #
        # Cardinalité attendue :
        # - une ligne côté ventes ;
        # - zéro ou une ligne côté stock.
        #
        # La clé article/date doit être unique dans
        # chacun des deux jeux agrégés.

        sales_join = sales_by_item_date.select(
            "item_sk",
            "date_sk",
            "total_revenue_inc_tax",
            "total_net_paid",
            "total_net_profit",
            "total_quantity_sold",
            "number_of_sales_lines",
            "number_of_tickets"
        )

        stock_join = inventory_by_item_date.select(
            "item_sk",
            "date_sk",
            "total_quantity_on_hand",
            "number_of_warehouses",
            "number_of_inventory_records"
        )

        # Vérification de l'unicité des clés côté ventes.
        duplicate_sales_keys = (
            sales_join
            .groupBy("item_sk", "date_sk")
            .count()
            .filter(F.col("count") > 1)
            .count()
        )

        # Vérification de l'unicité des clés côté stock.
        duplicate_stock_keys = (
            stock_join
            .groupBy("item_sk", "date_sk")
            .count()
            .filter(F.col("count") > 1)
            .count()
        )

        if duplicate_sales_keys > 0:
            raise RuntimeError(
                "La clé article/date n'est pas unique côté ventes agrégées."
            )

        if duplicate_stock_keys > 0:
            raise RuntimeError(
                "La clé article/date n'est pas unique côté stock agrégé."
            )

        before_join = sales_join.count()

        sales_inventory = (
            sales_join
            .join(
                stock_join,
                on=["item_sk", "date_sk"],
                how="left"
            )
            .withColumn(
                "flag_inventory_not_matched",
                F.col("total_quantity_on_hand").isNull()
            )
            .withColumn(
                "_grain",
                F.lit("un article par date, ventes enrichies du stock")
            )
        )

        after_join = sales_inventory.count()

        unmatched_count = (
            sales_inventory
            .filter(F.col("flag_inventory_not_matched"))
            .count()
        )

        print(f"Lignes avant jointure : {before_join}")
        print(f"Lignes après jointure : {after_join}")
        print(f"Lignes sans stock rapproché : {unmatched_count}")

        print(f"Clés dupliquées côté ventes : {duplicate_sales_keys}")
        print(f"Clés dupliquées côté stock : {duplicate_stock_keys}")

        if before_join != after_join:
            raise RuntimeError(
                "La jointure a modifié le nombre de lignes ventes. "
                "Vérifier la cardinalité."
            )

        sales_inventory = add_provenance(
            sales_inventory,
            "store_sales+inventory",
            f"{SALES_BRONZE_SOURCE} + {INVENTORY_BRONZE_SOURCE}"
        )


        # ====================================================
        # 10. PRÉPARATION DES JEUX DE DONNÉES À ÉCRIRE
        # ====================================================

        datasets = {
            "store_sales": sales_detail,
            "inventory": inventory_detail,
            "sales_by_store": sales_by_store,
            "sales_by_store_date": sales_by_store_date,
            "sales_by_item_date": sales_by_item_date,
            "inventory_by_item_date": inventory_by_item_date,
            "sales_inventory_by_item_date": sales_inventory
        }


        # ====================================================
        # 11. ÉCRITURE PARQUET ET CONTRÔLES
        # ====================================================

        print("\n========== ÉCRITURE DES JEUX TRANSFORMÉS ==========")

        OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

        results = []

        for dataset_name, dataframe in datasets.items():

            result = write_and_verify(
                dataframe,
                dataset_name,
                spark
            )

            results.append(result)

        print("\n========== BILAN FINAL ==========")

        for result in results:
            print(
                f"{result['dataset']} | "
                f"lignes={result['rows']} | "
                f"colonnes={result['columns']} | "
                f"chemin={result['path']}"
            )

        print("\nÉtapes 5 et 6 terminées avec succès.")

    finally:
        spark.stop()


# ============================================================
# 12. POINT D'ENTRÉE
# ============================================================

if __name__ == "__main__":
    main()