
from pathlib import Path
import csv

from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import (
    LongType,
    IntegerType,
    BooleanType,
    DoubleType,
    DecimalType,
)

# ============================================================
# 1. CONFIGURATION
# ============================================================

GOLD_PATH = Path("data/gold/sales_performance_by_store")
SALES_BY_STORE_PATH = Path(
    "data/silver-transformed/sales_by_store"
)
SILVER_STORE_SALES_PATH = Path("data/silver/store_sales")

REPORT_DIR = Path("reports/quality")
REPORT_PATH = REPORT_DIR / "quality_report_gold.csv"

EXPECTED_GOLD_ROWS = 12
TOLERANCE = 0.01

METRIC_COLUMNS = [
    "total_revenue_inc_tax",
    "total_net_paid",
    "total_net_profit",
    "total_quantity_sold",
    "number_of_sales_lines",
    "number_of_tickets",
]

REQUIRED_COLUMNS = [
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
]

EXPECTED_TYPES = {
    "store_sk": LongType,
    "revenue_rank": IntegerType,
    "is_best_revenue_store": BooleanType,
    "total_revenue_inc_tax": DecimalType,
    "global_revenue_inc_tax": DecimalType,
    "revenue_share_pct": DoubleType,
    "total_net_paid": DecimalType,
    "total_net_profit": DecimalType,
    "total_quantity_sold": LongType,
    "number_of_sales_lines": LongType,
    "number_of_tickets": LongType,
}

# ============================================================
# 2. INITIALISATION
# ============================================================

spark = (
    SparkSession.builder
    .appName("TP3-Retail-Intelligence-Etape9")
    .config("spark.hadoop.fs.defaultFS", "file:///")
    .getOrCreate()
)

results = []


def add_result(category, rule, observed, status, details=""):
    results.append({
        "controle": category,
        "regle": rule,
        "resultat": str(observed),
        "statut": status,
        "details": details,
    })


def check(condition, category, rule, observed, details=""):
    add_result(
        category,
        rule,
        observed,
        "PASS" if condition else "FAIL",
        details,
    )


try:
    # ========================================================
    # 3. LECTURE DU GOLD
    # ========================================================

    if not GOLD_PATH.exists():
        raise FileNotFoundError(
            f"Répertoire Gold introuvable : {GOLD_PATH}"
        )

    df = spark.read.parquet(str(GOLD_PATH))

    row_count = df.count()
    columns = df.columns
    schema = {field.name: field.dataType
              for field in df.schema.fields}

    print("\n=== CONTROLE QUALITE GOLD ===")
    print("Répertoire :", GOLD_PATH)
    print("Nombre de lignes :", row_count)

    # ========================================================
    # 4. VOLUME ET STRUCTURE
    # ========================================================

    check(
        row_count == EXPECTED_GOLD_ROWS,
        "Volume",
        f"Le nombre de lignes doit être égal à "
        f"{EXPECTED_GOLD_ROWS}",
        row_count,
        "Une ligne est attendue par magasin.",
    )

    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in columns
    ]

    check(
        len(missing_columns) == 0,
        "Structure",
        "Toutes les colonnes indispensables doivent être présentes",
        missing_columns if missing_columns else "Aucune colonne manquante",
    )

    # Les contrôles suivants nécessitent les colonnes requises.
    if missing_columns:
        raise ValueError(
            "Colonnes indispensables absentes : "
            + ", ".join(missing_columns)
        )

    # ========================================================
    # 5. COMPLETUDE
    # ========================================================

    for col in REQUIRED_COLUMNS:
        null_count = df.filter(F.col(col).isNull()).count()

        check(
            null_count == 0,
            "Complétude",
            f"{col} ne doit pas contenir de valeur nulle",
            f"{null_count} valeur(s) nulle(s)",
        )

    # ========================================================
    # 6. VALIDITE DES TYPES
    # ========================================================

    for col, expected_type in EXPECTED_TYPES.items():
        actual_type = schema[col]
        valid_type = isinstance(actual_type, expected_type)

        check(
            valid_type,
            "Validité des types",
            f"{col} doit être de type {expected_type.__name__}",
            actual_type.simpleString(),
        )

    # ========================================================
    # 7. UNICITE ET CLE CANDIDATE
    # ========================================================

    distinct_stores = df.select("store_sk").distinct().count()
    duplicate_count = row_count - distinct_stores

    check(
        duplicate_count == 0,
        "Unicité",
        "store_sk doit identifier un seul enregistrement",
        f"{duplicate_count} doublon(s)",
        "Clé candidate du jeu Gold.",
    )

    check(
        df.filter(F.col("store_sk").isNull()).count() == 0,
        "Clé candidate",
        "store_sk ne doit pas être nul",
        "Contrôle effectué",
    )

    # ========================================================
    # 8. COHERENCE DES VALEURS
    # ========================================================

    invalid_rank = df.filter(
        (F.col("revenue_rank") < 1)
        | (F.col("revenue_rank") > row_count)
    ).count()

    check(
        invalid_rank == 0,
        "Cohérence",
        "Le rang doit être compris entre 1 et le nombre de magasins",
        f"{invalid_rank} rang(s) invalide(s)",
    )

    distinct_ranks = df.select("revenue_rank").distinct().count()

    check(
        distinct_ranks == row_count,
        "Cohérence",
        "Chaque magasin doit avoir un rang distinct",
        f"{distinct_ranks} rang(s) distinct(s) pour {row_count} lignes",
        "À adapter si des ex aequo doivent partager un rang.",
    )

    best_count = df.filter(
        F.col("is_best_revenue_store") == True
    ).count()

    check(
        best_count == 1,
        "Cohérence",
        "Un seul magasin doit être identifié comme meilleur CA",
        f"{best_count} magasin(s) identifié(s)",
    )

    incorrect_best_flag = df.filter(
        (
            (F.col("revenue_rank") == 1)
            & (F.col("is_best_revenue_store") != True)
        )
        | (
            (F.col("revenue_rank") != 1)
            & (F.col("is_best_revenue_store") != False)
        )
    ).count()

    check(
        incorrect_best_flag == 0,
        "Cohérence",
        "Le booléen du meilleur magasin doit correspondre au rang 1",
        f"{incorrect_best_flag} incohérence(s)",
    )

    invalid_revenue = df.filter(
        F.col("total_revenue_inc_tax") < 0
    ).count()

    check(
        invalid_revenue == 0,
        "Cohérence",
        "Le chiffre d'affaires TTC ne doit pas être négatif",
        f"{invalid_revenue} valeur(s) négative(s)",
        "Règle métier à confirmer si des écritures correctives "
        "ou retours peuvent produire des montants négatifs.",
    )

    invalid_share = df.filter(
        (F.col("revenue_share_pct") < 0)
        | (F.col("revenue_share_pct") > 100)
    ).count()

    check(
        invalid_share == 0,
        "Cohérence",
        "La part de chiffre d'affaires doit être comprise entre 0 et 100",
        f"{invalid_share} valeur(s) hors domaine",
    )

    # Vérification du total global répété sur chaque ligne
    totals = df.agg(
        F.sum("total_revenue_inc_tax").alias("sum_revenue"),
        F.min("global_revenue_inc_tax").alias("min_global"),
        F.max("global_revenue_inc_tax").alias("max_global"),
        F.sum("revenue_share_pct").alias("sum_share"),
    ).first()

    total_consistent = (
        totals["sum_revenue"] is not None
        and totals["min_global"] is not None
        and totals["max_global"] is not None
        and abs(
            float(totals["sum_revenue"])
            - float(totals["min_global"])
        ) <= TOLERANCE
        and abs(
            float(totals["min_global"])
            - float(totals["max_global"])
        ) <= TOLERANCE
    )

    check(
        total_consistent,
        "Cohérence",
        "Le total global doit être identique sur chaque ligne "
        "et égal à la somme des CA magasins",
        (
            f"Somme CA={totals['sum_revenue']} ; "
            f"total global min={totals['min_global']} ; "
            f"max={totals['max_global']}"
        ),
    )

    share_consistent = (
        totals["sum_share"] is not None
        and abs(float(totals["sum_share"]) - 100.0) <= 0.1
    )

    check(
        share_consistent,
        "Cohérence",
        "La somme des parts de chiffre d'affaires doit être proche de 100 %",
        f"{totals['sum_share']} %",
        "Tolérance de 0,1 point pour les arrondis et les flottants.",
    )

    # Vérification individuelle de la part de CA
    invalid_calculated_share = df.filter(
        F.abs(
            F.col("revenue_share_pct")
            - (
                F.col("total_revenue_inc_tax")
                / F.col("global_revenue_inc_tax")
                * F.lit(100.0)
            )
        ) > F.lit(0.1)
    ).count()

    check(
        invalid_calculated_share == 0,
        "Cohérence",
        "La part de CA doit correspondre au CA magasin / CA global",
        f"{invalid_calculated_share} ligne(s) incohérente(s)",
        "Tolérance de 0,1 point.",
    )

    # ========================================================
    # 9. RECONCILIATION AVEC LA SOURCE SILVER TRANSFORMEE
    # ========================================================

    if SALES_BY_STORE_PATH.exists():
        source = spark.read.parquet(str(SALES_BY_STORE_PATH))

        source_count = source.count()

        check(
            source_count == row_count,
            "Réconciliation",
            "Le nombre de magasins doit être identique entre source et Gold",
            f"Source={source_count} ; Gold={row_count}",
        )

        source_keys = source.select("store_sk").distinct()
        gold_keys = df.select("store_sk").distinct()

        missing_in_gold = (
            source_keys.join(gold_keys, "store_sk", "left_anti")
            .count()
        )

        missing_in_source = (
            gold_keys.join(source_keys, "store_sk", "left_anti")
            .count()
        )

        check(
            missing_in_gold == 0 and missing_in_source == 0,
            "Clés candidates",
            "Les magasins doivent être identiques entre Silver transformé et Gold",
            (
                f"Absents du Gold={missing_in_gold} ; "
                f"absents de la source={missing_in_source}"
            ),
        )

        comparable_metrics = [
            col for col in METRIC_COLUMNS
            if col in source.columns and col in df.columns
        ]

        if len(comparable_metrics) == len(METRIC_COLUMNS):
            source_totals = source.agg(
                *[
                    F.sum(col).alias(col)
                    for col in METRIC_COLUMNS
                ]
            ).first()

            gold_totals = df.agg(
                *[
                    F.sum(col).alias(col)
                    for col in METRIC_COLUMNS
                ]
            ).first()

            for col in METRIC_COLUMNS:
                source_value = source_totals[col]
                gold_value = gold_totals[col]

                same_value = (
                    source_value == gold_value
                    if source_value is not None
                    else gold_value is None
                )

                check(
                    same_value,
                    "Réconciliation",
                    f"La somme de {col} doit être conservée",
                    f"Source={source_value} ; Gold={gold_value}",
                )

            # Comparaison des valeurs par magasin
            source_selected = source.select(
                "store_sk", *METRIC_COLUMNS
            ).alias("s")

            gold_selected = df.select(
                "store_sk", *METRIC_COLUMNS
            ).alias("g")

            comparison = source_selected.join(
                gold_selected,
                F.col("s.store_sk") == F.col("g.store_sk"),
                "full_outer",
            )

            mismatch_condition = (
                F.col("s.store_sk").isNull()
                | F.col("g.store_sk").isNull()
            )

            for col in METRIC_COLUMNS:
                mismatch_condition = (
                    mismatch_condition
                    | ~F.col(f"s.{col}").eqNullSafe(
                        F.col(f"g.{col}")
                    )
                )

            mismatch_count = comparison.filter(
                mismatch_condition
            ).count()

            check(
                mismatch_count == 0,
                "Réconciliation",
                "Les six mesures doivent être identiques par magasin",
                f"{mismatch_count} ligne(s) différente(s)",
            )
        else:
            add_result(
                "Réconciliation",
                "Les six mesures doivent être disponibles dans les deux jeux",
                "Colonnes manquantes pour la comparaison",
                "WARN",
                "Réconciliation détaillée non effectuée.",
            )
    else:
        add_result(
            "Réconciliation",
            "Comparer Gold avec sales_by_store",
            "Source introuvable",
            "WARN",
            f"Chemin attendu : {SALES_BY_STORE_PATH}",
        )

    # ========================================================
    # 10. INTEGRITE REFERENTIELLE AVEC LES VENTES SILVER
    # ========================================================

    if SILVER_STORE_SALES_PATH.exists():
        silver_sales = spark.read.parquet(
            str(SILVER_STORE_SALES_PATH)
        )

        if "store_sk" in silver_sales.columns:
            silver_store_keys = (
                silver_sales
                .select("store_sk")
                .filter(F.col("store_sk").isNotNull())
                .distinct()
            )

            gold_store_keys = df.select("store_sk").distinct()

            unknown_stores = (
                gold_store_keys
                .join(
                    silver_store_keys,
                    "store_sk",
                    "left_anti"
                )
                .count()
            )

            check(
                unknown_stores == 0,
                "Intégrité référentielle",
                "Chaque magasin Gold doit exister dans les ventes Silver",
                f"{unknown_stores} magasin(s) sans correspondance",
            )
        else:
            add_result(
                "Intégrité référentielle",
                "Vérifier store_sk dans les ventes Silver",
                "Colonne store_sk absente",
                "WARN",
            )
    else:
        add_result(
            "Intégrité référentielle",
            "Comparer les magasins Gold avec les ventes Silver",
            "Source Silver introuvable",
            "WARN",
            f"Chemin attendu : {SILVER_STORE_SALES_PATH}",
        )

    # ========================================================
    # 11. GENERATION DU RAPPORT
    # ========================================================

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    with open(
        REPORT_PATH,
        "w",
        newline="",
        encoding="utf-8"
    ) as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=[
                "controle",
                "regle",
                "resultat",
                "statut",
                "details",
            ],
            delimiter=";",
        )

        writer.writeheader()
        writer.writerows(results)

    print("\n=== BILAN DES CONTROLES ===")

    for status in ["PASS", "FAIL", "WARN", "INFO"]:
        count = sum(
            1 for result in results
            if result["statut"] == status
        )
        print(f"{status} : {count}")

    print("\nRapport généré :", REPORT_PATH)

    if any(r["statut"] == "FAIL" for r in results):
        print("ATTENTION : au moins un contrôle a échoué.")
    else:
        print("Aucun contrôle en échec.")

finally:
    spark.stop()
