"""Example script that reads a table from Fabric lakehouse.

Credentials and most configuration are pulled from environment variables so
that a long initialization block isn't required in every file.  See
``spark_setup.py`` for the helper used below.
"""

from spark_setup import get_spark_session


spark = get_spark_session()


# Replace  this with your lakehouse lakehouse_path
lakehouse_path = f"abfss://localspark@onelake.dfs.fabric.microsoft.com/lh_localspark.Lakehouse/Tables/dbo/"
# Write a simple dataframe to the lakehouse 
spark.sql("select Now() as dt").write.format("delta").save(lakehouse_path + "test_table3", mode="overwrite")
print(f"Written test data to {lakehouse_path}test_table3")

# Read the data back and show it
df = spark.read.load(lakehouse_path + "test_table3")
print("Read back the data:")
print(df.show())
