# syntax=docker/dockerfile:1
FROM mcr.microsoft.com/devcontainers/python:3.13-bookworm

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
  && apt-get -y install --no-install-recommends \
     openjdk-17-jdk-headless \
     ca-certificates \
     curl \
     procps \
  && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/*

# Compute JAVA_HOME dynamically (arm64 + amd64)
SHELL ["/bin/bash", "-lc"]
RUN set -euo pipefail; \
  JAVA_BIN="$(readlink -f "$(command -v java)")"; \
  JAVA_HOME_DIR="$(dirname "$(dirname "$JAVA_BIN")")"; \
  echo "Detected JAVA_HOME=${JAVA_HOME_DIR}"; \
  echo "export JAVA_HOME=${JAVA_HOME_DIR}" > /etc/profile.d/java.sh; \
  echo 'export PATH="$JAVA_HOME/bin:$PATH"' >> /etc/profile.d/java.sh; \
  echo "JAVA_HOME=${JAVA_HOME_DIR}" >> /etc/environment

# Install Python deps
RUN python -m pip install --upgrade pip \
  && pip install --no-cache-dir pyspark==4.1.1 ipykernel

# Preinstall Azure jars
RUN set -euo pipefail; \
  SPARK_JARS_DIR="$(python -c 'import pyspark, os; print(os.path.join(os.path.dirname(pyspark.__file__), "jars"))')"; \
  echo "Spark jars dir: ${SPARK_JARS_DIR}"; \
  curl -fL -o "${SPARK_JARS_DIR}/hadoop-azure-3.4.2.jar" \
    "https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-azure/3.4.2/hadoop-azure-3.4.2.jar"; \
  curl -fL -o "${SPARK_JARS_DIR}/azure-storage-blob-12.33.2.jar" \
    "https://repo1.maven.org/maven2/com/azure/azure-storage-blob/12.33.2/azure-storage-blob-12.33.2.jar"

# Sanity check
RUN source /etc/profile.d/java.sh && \
  java -version && \
  python -c 'from pyspark.sql import SparkSession; SparkSession.builder.master("local[1]").getOrCreate(); print("ok")'
