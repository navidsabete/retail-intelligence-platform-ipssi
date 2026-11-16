
#!/usr/bin/env bash

# ============================================================
# TP IPSSI - RETAIL INTELLIGENCE
# Etape C : inventaire et profilage des fichiers de donnees
#
# Utilisation :
#   ./etape_c.sh "/chemin/vers/le/dossier"
#
# Rapports produits :
#   rapport_inventaire.csv
#   rapport_colonnes.csv
#   rapport_anomalies.csv
# ============================================================

set -Eeuo pipefail

# ---------- Vérification des paramètres ----------

if [[ $# -ne 1 ]]; then
    echo "ERREUR : tu dois fournir le chemin du dossier à analyser."
    echo "Exemple : ./etape_c.sh ./donnees"
    exit 1
fi

DOSSIER="$1"

if [[ ! -d "$DOSSIER" ]]; then
    echo "ERREUR : le dossier '$DOSSIER' n'existe pas."
    exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
    echo "ERREUR : Python 3 est nécessaire pour exécuter ce script."
    exit 1
fi

DOSSIER_ABSOLU="$(cd "$DOSSIER" && pwd)"
DOSSIER_RAPPORT="$PWD/rapport_analyse"

mkdir -p "$DOSSIER_RAPPORT"

echo
echo "============================================================"
echo "       TP IPSSI - ANALYSE DES DONNEES RETAIL"
echo "============================================================"
echo "Dossier analysé : $DOSSIER_ABSOLU"
echo "Dossier rapports : $DOSSIER_RAPPORT"
echo

echo "[1/3] Recherche des fichiers de données..."

export DOSSIER_ABSOLU
export DOSSIER_RAPPORT

python3 - <<'PYTHON'
import os
import csv
import sys
import re
from pathlib import Path
from collections import Counter

root = Path(os.environ["DOSSIER_ABSOLU"])
out = Path(os.environ["DOSSIER_RAPPORT"])

extensions = {".csv", ".dat", ".txt", ".tsv"}
files = sorted(
    p for p in root.rglob("*")
    if p.is_file() and p.suffix.lower() in extensions
)

print(f"       {len(files)} fichier(s) détecté(s).")

if not files:
    print("       Aucun fichier CSV, DAT, TXT ou TSV trouvé.")
    sys.exit(0)

inventory_path = out / "rapport_inventaire.csv"
columns_path = out / "rapport_colonnes.csv"
anomalies_path = out / "rapport_anomalies.csv"

inventory_rows = []
column_rows = []
anomaly_rows = []

def detect_delimiter(path):
    """Détecte le séparateur à partir d'un échantillon du fichier."""
    candidates = ["|", ";", ",", "\t"]
    try:
        with path.open("r", encoding="utf-8-sig", errors="replace") as f:
            sample = f.read(12000)

        lines = [line for line in sample.splitlines()[:20] if line.strip()]
        if not lines:
            return "|"

        scores = {}
        for sep in candidates:
            counts = [line.count(sep) for line in lines]
            scores[sep] = sum(counts) / len(counts)

        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else "|"
    except Exception:
        return "|"

def detect_type(values):
    """Estimation simple du type d'une colonne."""
    values = [v.strip() for v in values if v.strip() != ""]

    if not values:
        return "VIDE"

    def is_integer(v):
        return re.fullmatch(r"[+-]?\d+", v) is not None

    def is_decimal(v):
        try:
            float(v.replace(",", "."))
            return True
        except ValueError:
            return False

    if all(is_integer(v) for v in values):
        return "ENTIER"

    if all(is_decimal(v) for v in values):
        return "NUMERIQUE"

    if all(
        re.fullmatch(r"\d{4}-\d{2}-\d{2}", v)
        or re.fullmatch(r"\d{2}/\d{2}/\d{4}", v)
        for v in values
    ):
        return "DATE_PROBABLE"

    return "TEXTE"

def has_header(path, extension):
    """
    Convention pédagogique :
    CSV/TSV : première ligne considérée comme en-tête.
    DAT/TXT : pas d'en-tête par défaut.
    """
    return extension in {".csv", ".tsv"}

for index, path in enumerate(files, start=1):
    relative = str(path.relative_to(root))
    extension = path.suffix.lower()

    print(f"\n[2/3] Analyse {index}/{len(files)} : {relative}")

    try:
        size = path.stat().st_size
        delimiter = "\t" if extension == ".tsv" else detect_delimiter(path)
        header_present = has_header(path, extension)

        with path.open(
            "r",
            encoding="utf-8-sig",
            errors="replace",
            newline=""
        ) as f:

            reader = csv.reader(f, delimiter=delimiter)

            first_row = next(reader, None)

            if first_row is None:
                inventory_rows.append([
                    relative, extension, size, 0, 0,
                    delimiter, "OUI", "FICHIER VIDE"
                ])
                anomaly_rows.append([
                    relative, "FICHIER VIDE",
                    "Le fichier ne contient aucune ligne."
                ])
                continue

            if header_present:
                headers = [
                    value.strip() if value.strip()
                    else f"colonne_{i+1}"
                    for i, value in enumerate(first_row)
                ]
                first_data_row = next(reader, None)
            else:
                headers = [
                    f"colonne_{i+1}"
                    for i in range(len(first_row))
                ]
                first_data_row = first_row

            expected_columns = len(headers)
            row_count = 0
            inconsistent_rows = 0
            empty_counts = [0] * expected_columns
            samples = [[] for _ in range(expected_columns)]
            distinct = [set() for _ in range(expected_columns)]
            distinct_limited = [False] * expected_columns

            def process_row(row):
                nonlocal_placeholder = None
                nonlocal_values = row

                nonlocal_state["rows"] += 1

                if len(nonlocal_values) != expected_columns:
                    nonlocal_state["inconsistent"] += 1

                for col in range(expected_columns):
                    value = (
                        nonlocal_values[col].strip()
                        if col < len(nonlocal_values)
                        else ""
                    )

                    if value == "":
                        empty_counts[col] += 1
                    else:
                        if len(samples[col]) < 5000:
                            samples[col].append(value)

                        if len(distinct[col]) < 100000:
                            distinct[col].add(value)
                        else:
                            distinct_limited[col] = True

            nonlocal_state = {"rows": 0, "inconsistent": 0}

            if first_data_row is not None:
                process_row(first_data_row)

            for row in reader:
                if not row:
                    continue
                process_row(row)

            row_count = nonlocal_state["rows"]
            inconsistent_rows = nonlocal_state["inconsistent"]

            inventory_rows.append([
                relative,
                extension,
                size,
                row_count,
                expected_columns,
                "TABULATION" if delimiter == "\t" else delimiter,
                "OUI" if header_present else "NON",
                "OK" if inconsistent_rows == 0 else "A VERIFIER"
            ])

            if inconsistent_rows > 0:
                anomaly_rows.append([
                    relative,
                    "NOMBRE DE COLONNES VARIABLE",
                    f"{inconsistent_rows} ligne(s) ont un nombre de colonnes différent de {expected_columns}."
                ])

            for col in range(expected_columns):
                values = samples[col]
                type_guess = detect_type(values)

                column_rows.append([
                    relative,
                    headers[col],
                    col + 1,
                    type_guess,
                    row_count,
                    empty_counts[col],
                    round(
                        empty_counts[col] / row_count * 100, 2
                    ) if row_count else 0,
                    len(distinct[col]),
                    "OUI" if distinct_limited[col] else "NON"
                ])

                if empty_counts[col] > 0:
                    anomaly_rows.append([
                        relative,
                        "VALEURS VIDES",
                        f"{headers[col]} : {empty_counts[col]} valeur(s) vide(s)."
                    ])

            print(f"       Lignes de données : {row_count}")
            print(f"       Nombre de colonnes : {expected_columns}")
            print(f"       Séparateur détecté : {repr(delimiter)}")
            print(f"       En-tête supposé : {'oui' if header_present else 'non'}")

    except Exception as error:
        print(f"       ERREUR pendant l'analyse : {error}")
        anomaly_rows.append([
            relative,
            "ERREUR DE LECTURE",
            str(error)
        ])

# ---------- Écriture des rapports ----------

def write_csv(filename, headers, rows):
    with (out / filename).open(
        "w", encoding="utf-8-sig", newline=""
    ) as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(headers)
        writer.writerows(rows)

write_csv(
    "rapport_inventaire.csv",
    [
        "fichier", "extension", "taille_octets",
        "nombre_lignes", "nombre_colonnes",
        "separateur", "entete_suppose", "statut"
    ],
    inventory_rows
)

write_csv(
    "rapport_colonnes.csv",
    [
        "fichier", "colonne", "position",
        "type_estime", "nombre_lignes",
        "valeurs_vides", "pourcentage_vide",
        "valeurs_distinctes_observees",
        "comptage_distinct_limite"
    ],
    column_rows
)

write_csv(
    "rapport_anomalies.csv",
    ["fichier", "anomalie", "description"],
    anomaly_rows
)

print("\n[3/3] Génération des rapports terminée.")

print("\n============================================================")
print("                  BILAN DE L'ANALYSE")
print("============================================================")
print(f"Fichiers examinés : {len(inventory_rows)}")
print(f"Colonnes décrites : {len(column_rows)}")
print(f"Anomalies relevées : {len(anomaly_rows)}")
print("\nRapports disponibles dans :")
print(out)
print(" - rapport_inventaire.csv")
print(" - rapport_colonnes.csv")
print(" - rapport_anomalies.csv")
print("============================================================")
PYTHON

echo
echo "Analyse terminée."