
from pathlib import Path
from functools import reduce

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import NumericType


# ============================================================
# ETAPE 7 - PRODUCTION DU JEU GOLD
# Question métier :
# Quels magasins réalisent le meilleur chiffre d'affaires ?
# ============================================================


# ------------------------------------------------------------
# 1. Configuration des chemins
# ------------------------------------------------------------

PROJECT_ROOT = Path.home() / "retail-intelligence" / "tp3"

INPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "silver-transformed"
    / "sales_by_store"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "gold"
    / "sales_performance_by_store"
)

print("=" * 65)
print("ETAPE 7 - PRODUCTION DU JEU GOLD")
print("=" * 65)

print(f"Projet      : {PROJECT_ROOT}")
print(f"Source      : {INPUT_PATH}")
print(f"Destination : {OUTPUT_PATH}")


# ------------------------------------------------------------
# 2. Initialisation de Spark
# ------------------------------------------------------------

spark = (
    SparkSession.builder
    .appName("TP3-Retail-Intelligence-Etape7")
    .config("spark.hadoop.fs.defaultFS", "file:///")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


try:

    # --------------------------------------------------------
    # 3. Lecture du jeu source
    # --------------------------------------------------------

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Jeu source introuvable : {INPUT_PATH}"
        )

    df_source = spark.read.parquet(str(INPUT_PATH))

    source_count = df_source.count()

    print(f"\nNombre de lignes sources : {source_count}")

    if source_count == 0:
        raise ValueError("Le jeu source est vide.")


    # --------------------------------------------------------
    # 4. Vérification du schéma et de la granularité
    # --------------------------------------------------------

    required_columns = [
        "store_sk",
        "total_revenue_inc_tax",
        "total_net_paid",
        "total_net_profit",
        "total_quantity_sold",
        "number_of_sales_lines",
        "number_of_tickets",
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df_source.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Colonnes absentes : {missing_columns}"
        )

    # Vérification des clés nulles

    null_keys = (
        df_source
        .filter(F.col("store_sk").isNull())
        .count()
    )

    if null_keys > 0:
        raise ValueError(
            f"{null_keys} clés magasin nulles."
        )

    # Vérification de l'unicité

    duplicate_keys = (
        df_source
        .groupBy("store_sk")
        .count()
        .filter(F.col("count") > 1)
        .count()
    )

    if duplicate_keys > 0:
        raise ValueError(
            f"{duplicate_keys} magasins dupliqués."
        )

    print("Unicité des magasins : OK")


    # --------------------------------------------------------
    # 5. Vérification des indicateurs numériques
    # --------------------------------------------------------

    metric_columns = [
        "total_revenue_inc_tax",
        "total_net_paid",
        "total_net_profit",
        "total_quantity_sold",
        "number_of_sales_lines",
        "number_of_tickets",
    ]

    for col_name in metric_columns:

        data_type = (
            df_source.schema[col_name].dataType
        )

        if not isinstance(data_type, NumericType):
            raise TypeError(
                f"Type non numérique pour {col_name} : "
                f"{data_type}"
            )

        null_count = (
            df_source
            .filter(F.col(col_name).isNull())
            .count()
        )

        if null_count > 0:
            raise ValueError(
                f"{null_count} valeurs nulles dans {col_name}."
            )

    print("Types numériques et valeurs nulles : OK")


    # --------------------------------------------------------
    # 6. Calcul du chiffre d'affaires global
    # --------------------------------------------------------

    # Agrégation indépendante : évite une fenêtre globale
    # uniquement destinée au calcul du total.

    df_global = (
        df_source
        .agg(
            F.sum("total_revenue_inc_tax")
            .alias("global_revenue_inc_tax")
        )
    )

    # Conservation des mesures sources

    df_gold_base = df_source.select(
        "store_sk",
        *metric_columns
    )

    # --------------------------------------------------------
    # 7. Construction des indicateurs Gold
    # --------------------------------------------------------

    ranking_window = Window.orderBy(
        F.col("total_revenue_inc_tax").desc()
    )

    df_gold = (
        df_gold_base

        # Ajout du chiffre d'affaires global
        .crossJoin(df_global)

        # Part du CA global
        .withColumn(
            "revenue_share_pct",
            F.when(
                F.col("global_revenue_inc_tax") != 0,
                F.round(
                    F.col("total_revenue_inc_tax")
                    / F.col("global_revenue_inc_tax")
                    * 100,
                    2
                )
            ).otherwise(
                F.lit(None).cast("double")
            )
        )

        # Classement des magasins
        .withColumn(
            "revenue_rank",
            F.rank().over(ranking_window)
        )

        # Identification du meilleur magasin
        .withColumn(
            "is_best_revenue_store",
            F.col("revenue_rank") == 1
        )

        # Métadonnées
        .withColumn(
            "_gold_dataset",
            F.lit("sales_performance_by_store")
        )
        .withColumn(
            "_business_grain",
            F.lit("one row per store")
        )
        .withColumn(
            "_processing_stage",
            F.lit("gold")
        )

        .select(
            "store_sk",
            "revenue_rank",
            "is_best_revenue_store",
            "total_revenue_inc_tax",
            "global_revenue_inc_tax",
            "revenue_share_pct",
            "total_net_paid",
            "total_net_profit",
            "total_quantity_sold",
            "number_of_sales_lines",
            "number_of_tickets",
            "_gold_dataset",
            "_business_grain",
            "_processing_stage",
        )
    )


    # --------------------------------------------------------
    # 8. Contrôles du jeu Gold
    # --------------------------------------------------------

    gold_count = df_gold.count()

    print("\nContrôles Gold :")
    print(f"Lignes source : {source_count}")
    print(f"Lignes Gold   : {gold_count}")

    if gold_count != source_count:
        raise ValueError(
            "Le nombre de lignes Gold est incorrect."
        )

    if gold_count == 0:
        raise ValueError("Le jeu Gold est vide.")

    # Vérification de l'unicité après transformation

    duplicate_gold = (
        df_gold
        .groupBy("store_sk")
        .count()
        .filter(F.col("count") > 1)
        .count()
    )

    if duplicate_gold > 0:
        raise ValueError(
            "Des clés magasin sont dupliquées dans Gold."
        )

    # Vérification du classement

    invalid_ranks = (
        df_gold
        .filter(F.col("revenue_rank").isNull())
        .count()
    )

    if invalid_ranks > 0:
        raise ValueError("Classement invalide.")

    # Vérification du magasin classé premier

    best_count = (
        df_gold
        .filter(F.col("is_best_revenue_store"))
        .count()
    )

    expected_best_count = (
        df_gold
        .filter(F.col("revenue_rank") == 1)
        .count()
    )

    if best_count != expected_best_count:
        raise ValueError(
            "Incohérence entre classement et indicateur du meilleur magasin."
        )

    if best_count == 0:
        raise ValueError("Aucun meilleur magasin identifié.")

    # Vérification des parts de chiffre d'affaires

    share_total = (
        df_gold
        .agg(F.sum("revenue_share_pct").alias("total"))
        .first()["total"]
    )

    print(f"Somme des parts : {share_total} %")

    if share_total is None or abs(share_total - 100.0) > 0.1:
        raise ValueError(
            "La somme des parts de CA est incohérente."
        )


    # --------------------------------------------------------
    # 9. Réconciliation des mesures Silver / Gold
    # --------------------------------------------------------

    # Comparaison des sommes de chaque indicateur

    source_totals = (
        df_source
        .agg(
            *[
                F.sum(col).alias(col)
                for col in metric_columns
            ]
        )
        .first()
        .asDict()
    )

    gold_totals = (
        df_gold
        .agg(
            *[
                F.sum(col).alias(col)
                for col in metric_columns
            ]
        )
        .first()
        .asDict()
    )

    print("\nRéconciliation des mesures :")

    for col_name in metric_columns:

        source_value = source_totals[col_name]
        gold_value = gold_totals[col_name]

        print(
            f"{col_name} : "
            f"Source={source_value} | Gold={gold_value}"
        )

        if source_value != gold_value:
            raise ValueError(
                f"Écart détecté dans la mesure {col_name}."
            )

    print("Réconciliation globale : OK")

    # Vérification des valeurs par magasin

    df_comparison = (
        df_source.alias("s")
        .join(
            df_gold.select(
                "store_sk",
                *metric_columns
            ).alias("g"),
            F.col("s.store_sk") == F.col("g.store_sk"),
            how="full_outer"
        )
    )

    mismatch_condition = reduce(
        lambda a, b: a | b,
        [
            ~F.col(f"s.{col}").eqNullSafe(
                F.col(f"g.{col}")
            )
            for col in metric_columns
        ]
    )

    mismatches = (
        df_comparison
        .filter(
            F.col("s.store_sk").isNull()
            | F.col("g.store_sk").isNull()
            | mismatch_condition
        )
        .count()
    )

    if mismatches > 0:
        raise ValueError(
            f"{mismatches} écarts détectés entre source et Gold."
        )

    print("Correspondance des mesures par magasin : OK")


    # --------------------------------------------------------
    # 10. Affichage du classement
    # --------------------------------------------------------

    print("\nClassement des magasins par CA TTC :")

    df_gold.orderBy("revenue_rank").show(
        20,
        truncate=False
    )


    # --------------------------------------------------------
    # 11. Écriture du jeu Gold
    # --------------------------------------------------------

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    (
        df_gold
        .write
        .mode("overwrite")
        .option("compression", "snappy")
        .parquet(str(OUTPUT_PATH))
    )

    print(f"\nJeu Gold écrit : {OUTPUT_PATH}")


    # --------------------------------------------------------
    # 12. Relecture et validation après écriture
    # --------------------------------------------------------

    df_gold_check = spark.read.parquet(
        str(OUTPUT_PATH)
    )

    readback_count = df_gold_check.count()

    print("\nContrôle après écriture :")
    print(f"Avant écriture : {gold_count}")
    print(f"Après relecture : {readback_count}")

    if readback_count != gold_count:
        raise ValueError(
            "Nombre de lignes incorrect après relecture."
        )

    # Comparaison complète des lignes, indépendamment
    # de leur ordre physique dans les fichiers Parquet.

    differences_before = (
        df_gold.exceptAll(df_gold_check).count()
    )

    differences_after = (
        df_gold_check.exceptAll(df_gold).count()
    )

    if differences_before > 0 or differences_after > 0:
        raise ValueError(
            "Les données relues diffèrent des données écrites."
        )

    print("Comparaison complète avant/après : OK")

    # Vérification du schéma relu

    print("\nSchéma Gold :")
    df_gold_check.printSchema()

    print("\nAperçu Gold :")

    df_gold_check.orderBy(
        "revenue_rank"
    ).show(20, truncate=False)

    print("=" * 65)
    print("ETAPE 7 TERMINEE AVEC SUCCES")
    print("=" * 65)

finally:

    spark.stop()