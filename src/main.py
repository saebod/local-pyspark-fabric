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
table_name:str='notebook_test_table'
spark.sql("select Now() as dt").write.format("delta").mode("overwrite").save(lakehouse_path +table_name)
print(f"Written test data to {lakehouse_path}{table_name}")

# Read the data back and show it
df = spark.read.format("delta").load(lakehouse_path + table_name)
print("Read back the data:")
print(df.show())
