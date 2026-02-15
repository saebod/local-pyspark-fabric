from pyspark.sql import SparkSession
import os
import pyspark

############### Configure the Spark session - START ###############
# Servie principal credentials are read from environment variables, 
# or replace the <placeholders> with your actual values.
tenant_id = os.getenv("AZ_TENANT_ID","<your-tenant-id>")
client_id = os.getenv("AZ_CLIENT_ID","<your-client-id>")
client_secret = os.getenv("AZ_CLIENT_SECRET","<your-client-secret>")
host = os.getenv("SPARK_AZURE_HOST", "onelake.dfs.fabric.microsoft.com")
spark_hadoop='spark.hadoop.fs.azure.account'
spark_version = pyspark.__version__.split(".")
spark_major = int(spark_version[0])
spark_minor = int(spark_version[1]) if len(spark_version) > 1 else 0

# Pick a Delta package that matches the local Spark/Scala runtime.
delta_package = os.getenv(
    "SPARK_DELTA_PACKAGE",
    "io.delta:delta-spark_2.13:4.0.1" if spark_major >= 4 else "io.delta:delta-spark_2.12:3.2.0",
)

if (spark_major, spark_minor) >= (4, 1) and "SPARK_DELTA_PACKAGE" not in os.environ:
    raise RuntimeError(
        "Delta Lake jars published today are not compatible with PySpark "
        f"{pyspark.__version__} in this script. "
        "Use PySpark 4.0.x (or 3.x), or set SPARK_DELTA_PACKAGE to a custom compatible build."
    )
# Set up the Spark session with Azure Data Lake credentials and other configurations.
spark = (
    SparkSession.builder
    .appName("fabric-dev")
    .config(
        "spark.jars.packages",",".join([
            # Hadoop Azure support is required to read/write from OneLake
            "org.apache.hadoop:hadoop-azure:3.4.2", delta_package]),
    )
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    # The following configs set up the credentials for accessing OneLake via ABFS.
    .config(f"{spark_hadoop}.auth.type.{host}", "OAuth")
    .config(f"{spark_hadoop}.oauth.provider.type.{host}",
            "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
    .config(f"{spark_hadoop}.oauth2.client.id.{host}", client_id)
    .config(f"{spark_hadoop}.oauth2.client.secret.{host}", client_secret)
    .config(f"{spark_hadoop}.oauth2.client.endpoint.{host}",
            f"https://login.microsoftonline.com/{tenant_id}/oauth2/token")
    .getOrCreate()
)

############### Configure the Spark session - END ###############

# Replace  this with your lakehouse lakehouse_path
lakehouse_path = f"abfss://localspark@onelake.dfs.fabric.microsoft.com/test_2.Lakehouse/Tables/"

spark.sql("select Now() as dt").write.format("delta").save(lakehouse_path + "testing2", mode="overwrite")
print(f"Written test data to {lakehouse_path}test_table")
df = spark.read.load(lakehouse_path + "testing")
print("Read back the data:")


print(df.show())
