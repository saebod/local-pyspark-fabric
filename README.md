# Local PySpark Development for Microsoft Fabric

Develop and test Fabric data workloads locally with PySpark, then push the same code to Fabric.

## Why this approach
- Faster iteration in VS Code than in the Fabric web editor.
- Lower Fabric compute usage for small development tasks.
- Better local tooling (linting, testing, Git workflows, AI assistants).

## What this repo demonstrates
- Local Spark session setup for OneLake access via Service Principal.
- Reusable Spark bootstrap in `src/spark_setup.py`.
- Simple example flow in `src/basic_example.py` and `src/main.py`.
- Fabric notebook compatibility using environment-based local detection in:
  `fabric-workspace/write_fabric.Notebook/notebook-content.py`

## Prerequisites
- Microsoft Fabric workspace access (Member or equivalent).
- A Service Principal with required access to the target workspace/lakehouse.
- VS Code.
- Optional but recommended: Docker + VS Code Dev Containers extension.

## Quick start
1. Clone the repository.
2. Open in VS Code.
3. If using dev containers, reopen in container.
4. Set environment variables:
   - `AZ_TENANT_ID`
   - `AZ_CLIENT_ID`
   - `AZ_CLIENT_SECRET`
   - `LocalDevelopment` = 1
5. Run an example:
   - Update `lakehouse_path` in `src/basic_example.py` or `src/main.py` to your own lakehouse ABFSS path first.
   - `python src/basic_example.py`
   - or `python src/main.py`
   


## Working with Fabric notebooks locally
Use an environment flag to switch behavior:
- If `LocalDevelopment` is set, import local Spark setup and run locally.
- Otherwise, run in Fabric runtime as normal.

This allows one notebook codebase to work both locally and in Fabric.

## Limitations
- Local Spark settings may differ from Fabric runtime.
- Attached-lakehouse SQL behavior may not match local usage as we cannot attach a lakehouse to our pyspark.
- Notebook metadata can break if edited carelessly in raw `notebook-content.py`.

## Ideas for next improvements
- Add lint/format checks for Fabric notebook metadata ordering.
- Add conversion tooling between Jupyter notebooks and Fabric `notebook-content.py`.

## References
- https://endjin.com/blog/2025/01/spark-devcontainers-local-spark
- https://stackoverflow.com/questions/78527732/writing-to-azure-blob-storage-from-local-spark-environment
- https://code.visualstudio.com/docs/devcontainers/containers
