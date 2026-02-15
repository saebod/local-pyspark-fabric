# Agents Guide

This file defines how coding agents should work in this repository.

## Mission
Help developers build and validate Microsoft Fabric data code locally with PySpark, then keep behavior aligned when pushed to Fabric.

## Repository context
- Local Spark bootstrap lives in `src/spark_setup.py`.
- Example local runs:
  - `src/basic_example.py`
  - `src/main.py`
- Fabric notebook source example:
  - `fabric-workspace/write_fabric.Notebook/notebook-content.py`

## Environment assumptions
- Python + PySpark + Java are available.
- OneLake access is done with Service Principal OAuth credentials:
  - `AZ_TENANT_ID`
  - `AZ_CLIENT_ID`
  - `AZ_CLIENT_SECRET`
- Optional host override:
  - `SPARK_AZURE_HOST` (default `onelake.dfs.fabric.microsoft.com`)
- Local notebook behavior may rely on:
  - `LocalDevelopment`

## Agent workflow
1. Prefer reusing `get_spark_session()` from `src/spark_setup.py` instead of duplicating Spark configuration.
2. Keep local and Fabric behavior compatible; use environment gating for local-only setup.
3. Prefer path-based lakehouse I/O (`abfss://...`) for portability.
4. Keep notebook metadata blocks intact when editing `notebook-content.py`.
5. Make minimal, targeted changes and explain tradeoffs clearly.

## Editing rules
- Do not hardcode secrets in committed files.
- Do not remove existing metadata blocks from Fabric notebook source files.
- Keep imports robust for both script execution and notebook execution context.
- Favor small, testable refactors over broad rewrites.

## Validation checklist
- Confirm code still imports without relative-import errors in local mode.
- Confirm Spark session creation uses shared setup helper.
- Confirm OneLake path read/write code paths remain unchanged unless requested.
- If tests are added, keep them fast and local-first.

## Non-goals
- Replacing PySpark with an alternative engine for this repo.
- Redesigning Fabric deployment or CI/CD architecture unless explicitly requested.

