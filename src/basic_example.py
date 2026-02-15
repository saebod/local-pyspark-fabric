from pyspark.sql import SparkSession
import os

############### Configure the Spark session - START ###############
# Servie principal credentials are read from environment variables, 
# or replace the <placeholders> with your actual values.
tenant_id = os.getenv("AZ_TENANT_ID","<your-tenant-id>")
client_id = os.getenv("AZ_CLIENT_ID","<your-client-id>")
client_secret = os.getenv("AZ_CLIENT_SECRET","<your-client-secret>")
host = os.getenv("SPARK_AZURE_HOST", "onelake.dfs.fabric.microsoft.com")
spark_hadoop='spark.hadoop.fs.azure.account'

# Set up the Spark session with Azure Data Lake credentials and other configurations.
spark = (
    SparkSession.builder
    .appName("fabric-dev")
    .config(
        "spark.jars.packages",",".join([
            # Hadoop Azure support is required to read/write from OneLake
            "org.apache.hadoop:hadoop-azure:3.4.2"]),
    )
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
lakehouse_path = f"abfss://localspark@onelake.dfs.fabric.microsoft.com/lh_localspark.Lakehouse/Tables/dbo/"

spark.sql("select Now() as dt").write.save(lakehouse_path + "test_table", mode="overwrite")
print(f"Written test data to {lakehouse_path}test_table")
df = spark.read.load(lakehouse_path + "test_table")
print("Read back the data:")


print(df.show())
