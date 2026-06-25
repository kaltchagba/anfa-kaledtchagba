"""
analyse_referentiel.py
Calcule quelques statistiques sur le référentiel d'Anfa
à partir des CSV (lignes, arrêts, bus, tarifs).
Le script utilise PySpark en mode LOCAL.
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as spark_sum, avg, desc

DATA_DIR = "/data/referentiel"


def main() -> None:
    spark = (
        SparkSession.builder
        .appName("Anfa - Analyse du référentiel")
        .master("local[*]")
        .config("spark.ui.showConsoleProgress", "false")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    lignes = spark.read.csv(f"{DATA_DIR}/lignes.csv",  header=True, inferSchema=True)
    arrets = spark.read.csv(f"{DATA_DIR}/arrets.csv",  header=True, inferSchema=True)
    bus    = spark.read.csv(f"{DATA_DIR}/bus.csv",     header=True, inferSchema=True)
    tarifs = spark.read.csv(f"{DATA_DIR}/tarifs.csv",  header=True, inferSchema=True)

    print("\n" + "=" * 60)
    print("  ANALYSE DU RÉFÉRENTIEL ANFA")
    print("=" * 60)

    nb_lignes         = lignes.count()
    nb_arrets_uniques = arrets.select("arret_id").distinct().count()
    nb_bus            = bus.count()
    nb_bus_actifs     = bus.filter(bus.statut == "actif").count()

    print(f"\n  Nombre de lignes de bus       : {nb_lignes}")
    print(f"  Nombre d'arrêts uniques        : {nb_arrets_uniques}")
    print(f"  Nombre total de bus            : {nb_bus}")
    print(f"  Dont actifs                    : {nb_bus_actifs}")

    capacite_totale = (
        bus.filter(bus.statut == "actif")
        .agg(spark_sum("capacite").alias("capacite_totale"))
        .collect()[0]["capacite_totale"]
    )
    print(f"  Capacité totale de la flotte   : ~{capacite_totale} places")

    print("\n  Top 3 des lignes les plus longues :")
    top3 = lignes.orderBy(desc("distance_km")).limit(3).collect()
    for i, row in enumerate(top3, start=1):
        print(f"    {i}. {row['nom']:40s} {row['distance_km']:5.2f} km")

    print("\n  Tarif moyen par type :")
    tarifs.groupBy("type").agg(avg("prix_fcfa").alias("prix_moyen")) \
        .orderBy("type") \
        .show(truncate=False)

    print("=" * 60)
    print("  Analyse terminée.\n")
    spark.stop()


if __name__ == "__main__":
    main()
