# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

import os
import sys
from pathlib import Path
# Check if we're in a local development environment by looking for an environment variable.
# This variable can be set in the devcontainer configuration, and allows us to conditionally set up the Spark session with the right credentials when running the notebook outside of Fabric.
is_local_env =os.getenv("LocalDevelopment")
is_local_env = bool(is_local_env)

# if i'm developing locally, set up the spark session with the right credentials
if is_local_env:
    print("Running in local development environment")
    # Ensure project root is importable when this notebook runs as a script.
    project_root = Path.cwd()
    src_dir = project_root / "src"
    if src_dir.exists() and str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))

    from spark_setup import get_spark_session
    spark = get_spark_session()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

path = 'abfss://localspark@onelake.dfs.fabric.microsoft.com/lh_localspark.Lakehouse/Tables/dbo/test_table2'

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from datetime import datetime
df = spark.createDataFrame([(datetime.now(),)],schema=['time'])
df.write.mode("overwrite").save(path)
print("this code was added from my local VS code editor and")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
