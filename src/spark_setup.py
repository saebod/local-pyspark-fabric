import os
from pyspark.sql import SparkSession
import pyspark


def _resolve_spark_settings() -> dict:
    """Build Spark settings compatible with the local basic example."""
    tenant_id = os.getenv("AZ_TENANT_ID", "<your-tenant-id>")
    client_id = os.getenv("AZ_CLIENT_ID", "<your-client-id>")
    client_secret = os.getenv("AZ_CLIENT_SECRET", "<your-client-secret>")
    host = os.getenv("SPARK_AZURE_HOST", "onelake.dfs.fabric.microsoft.com")
    spark_hadoop = "spark.hadoop.fs.azure.account"

    spark_version = pyspark.__version__.split(".")
    spark_major = int(spark_version[0])
    spark_minor = int(spark_version[1]) if len(spark_version) > 1 else 0

    if (spark_major, spark_minor) >= (4, 1) and "SPARK_DELTA_PACKAGE" not in os.environ:
        raise RuntimeError(
            "Delta Lake jars published today are not compatible with PySpark "
            f"{pyspark.__version__} in this script. "
            "Use PySpark 4.0.x (or 3.x), or set SPARK_DELTA_PACKAGE to a custom compatible build."
        )

    delta_package = os.getenv(
        "SPARK_DELTA_PACKAGE",
        "io.delta:delta-spark_2.13:4.0.1" if spark_major >= 4 else "io.delta:delta-spark_2.12:3.2.0",
    )

    package_list = [
        "org.apache.hadoop:hadoop-azure:3.4.2",
        delta_package,
    ]
    extra_packages = os.getenv("SPARK_EXTRA_PACKAGES")
    if extra_packages:
        package_list.extend([pkg.strip() for pkg in extra_packages.split(",") if pkg.strip()])

    return {
        "spark.jars.packages": ",".join(package_list),
        "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
        "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        # Prevent truncated query plans in logs / explain()
        "spark.sql.debug.maxToStringFields": "200",
        f"{spark_hadoop}.auth.type.{host}": "OAuth",
        f"{spark_hadoop}.oauth.provider.type.{host}": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
        f"{spark_hadoop}.oauth2.client.id.{host}": client_id,
        f"{spark_hadoop}.oauth2.client.secret.{host}": client_secret,
        f"{spark_hadoop}.oauth2.client.endpoint.{host}": f"https://login.microsoftonline.com/{tenant_id}/oauth2/token",
        
    }


def get_spark_session() -> SparkSession:
    """Return a singleton SparkSession with sensible defaults.

    If a session already exists, ``getOrCreate`` will return it and any
    previous configuration is preserved – this means you can call
    :func:`get_spark_session` at the top of every script and not worry about
    re‑running the long configuration block.
    """
    builder = SparkSession.builder.appName(os.getenv("SPARK_APP", "fabric-dev"))
    # allow user to override the master URL (cluster or local) via an env var
    master_url = os.getenv("SPARK_MASTER", "local[*]")
    builder = builder.master(master_url)

    # you can also control memory/partitions via environment variables
    driver_mem = os.getenv("SPARK_DRIVER_MEMORY")
    exec_mem = os.getenv("SPARK_EXECUTOR_MEMORY")
    shuffle = os.getenv("SPARK_SQL_SHUFFLE_PARTITIONS")
    if driver_mem:
        builder = builder.config("spark.driver.memory", driver_mem)
    if exec_mem:
        builder = builder.config("spark.executor.memory", exec_mem)
    if shuffle:
        builder = builder.config("spark.sql.shuffle.partitions", shuffle)

    for key, value in _resolve_spark_settings().items():
        builder = builder.config(key, value)

    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel(os.getenv("SPARK_LOG_LEVEL", "INFO"))
    return spark
