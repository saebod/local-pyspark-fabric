import os
from pyspark.sql import SparkSession


def _configure_azure(spark: SparkSession) -> None:
    """Configure Azure Data Lake storage credentials for the given Spark session.

    The values are read from environment variables so that your application code
    doesn't need to set them explicitly on every run.  You can populate the
    variables once (for example in the devcontainer configuration) and every
    script that obtains the session will automatically get the right settings.
    """
    host = os.getenv("SPARK_AZURE_HOST", "onelake.dfs.fabric.microsoft.com")
    tenant_id = os.getenv("AZ_TENANT_ID","<your-tenant-id>")
    client_id = os.getenv("AZ_CLIENT_ID","<your-client-id>")
    client_secret = os.getenv("AZ_CLIENT_SECRET","<your-client-secret>")

    if not (tenant_id and client_id and client_secret):
        # no credentials; it's helpful to warn rather than silently continue
        # because a user will later get the confusing "account.key null" error
        # if they try to access abfss paths.
        import logging

        logging.warning(
            "azure storage credentials not found (AZ_TENANT_ID/AZ_CLIENT_ID/" \
            "AZ_CLIENT_SECRET); calls to abfss:// will fail unless you set them"
        )
        return

    spark.conf.set(f"fs.azure.account.auth.type.{host}", "OAuth")
    spark.conf.set(
        f"fs.azure.account.oauth.provider.type.{host}",
        "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
    )
    spark.conf.set(f"fs.azure.account.oauth2.client.id.{host}", client_id)
    spark.conf.set(f"fs.azure.account.oauth2.client.secret.{host}", client_secret)
    spark.conf.set(
        f"fs.azure.account.oauth2.client.endpoint.{host}",
        f"https://login.microsoftonline.com/{tenant_id}/oauth2/token",
    )


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

    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel(os.getenv("SPARK_LOG_LEVEL", "INFO"))
    _configure_azure(spark)
    return spark
