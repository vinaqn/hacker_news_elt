# USGS Earthquake ELT

This project implements a cloud-deployed ETL pipeline that ingests earthquake data from the USGS Earthquake API. The pipeline extracts and incrementally loads seismic event data, applies data quality checks, and transforms it using dimensional modeling to support analytical use cases. Processed data is served to an analytics layer for downstream dashboards and exploration of earthquake frequency, magnitude, and geographic trends. The architecture is designed to scale horizontally (e.g., via cloud data warehouse compute scaling), is fully automated with CI/CD, and is scheduled to run in the cloud, demonstrating production-ready data engineering best practices.

## Data Source

**USGS Earthquake API**

The USGS Earthquake API provides near-real-time and historical global earthquake data in GeoJSON format. It exposes key seismic attributes including event time, magnitude, depth, latitude/longitude, location description, and update timestamps. Data is refreshed every few minutes and supports time-window and magnitude-based queries, making it well-suited for incremental ingestion, analytical pipelines, and large-scale monitoring.

**API Documentation:**  
https://earthquake.usgs.gov/fdsnws/event/1/

**GeoNames Geographical Database**

The GeoNames dataset provides a comprehensive global gazetteer containing geographic reference data such as place names, coordinates (latitude/longitude), country and administrative divisions, feature classifications, population, and elevation. For this project, the `allCountries.txt` geocode file was downloaded from GeoNames and stored in Amazon S3, where it is used to enrich earthquake events with standardized geographic attributes such as country and region.

**Data Download:**  
https://download.geonames.org/export/dump/

## ERD

## Data Architecture

## ELT

### Airbyte
Airbyte is used as the primary ingestion tool for this project. A custom Airbyte connector was built to extract earthquake data from the USGS Earthquake API. The connector configuration is defined in a declarative `earthquake_custom_connector.yml` file located in the `airbyte/` directory. Configuration details and setup instructions are documented in the README within the `airbyte` folder.

In addition, Airbyte’s standard Amazon S3 connector is used to ingest reference data from a private S3 bucket hosting the GeoNames `allCountries.txt` dataset. This enables consistent and repeatable ingestion of external geospatial reference data into the pipeline.


### dbt
dbt is used to transform data within Snowflake, staging raw ingested data in a **staging** schema and modeling it into **dimensional (fact and dimension) tables** within a **mart** schema. Data quality tests, including not-null, uniqueness, and relationship checks, are applied to ensure reliability and analytical correctness.
