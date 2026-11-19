from pyspark.sql import SparkSession

# Creation d’une session Spark en mode local
spark = (
    SparkSession.builder.appName("Test-Retail-Intelligence").master("local[*]").getOrCreate()
    )

# Afficher la version de Spark
print("Version Spark :", spark.version)

 # Creer un petit jeu de donnees de test
donnees = [
    (" Magasin A", 1200.0),
    (" Magasin B", 850.0),
    (" Magasin C", 1600.0)
]

colonnes = ["magasin", "chiffre_affaires"]

df = spark.createDataFrame(donnees, colonnes)

# Afficher les donnees
df.show()

# Arreter proprement la session
spark.stop()