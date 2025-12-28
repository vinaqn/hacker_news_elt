# Airbyte Ingestion

For local development, Airbyte was installed and managed using `abctl`, Airbyte’s official command-line tool for running the open-source platform. This setup runs Airbyte as a set of Docker containers and exposes the Airbyte UI at `http://localhost:8000`.

This folder contains Airbyte configuration for the project’s ingestion layer:

- A **custom Airbyte connector** (`earthquake_custom_connector.yml`) to ingest data from the **USGS Earthquake API**
