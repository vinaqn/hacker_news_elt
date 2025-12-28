from dagster_airbyte import (AirbyteCloudWorkspace,
                            build_airbyte_assets_definitions, 
                            DagsterAirbyteTranslator)

import dagster as dg

class CustomDagsterAirbyteTranslator(DagsterAirbyteTranslator):
    def get_asset_spec(self, props):
        default_spec = super().get_asset_spec(props)

        stream_name = (
            getattr(props, "name", None)
            or getattr(getattr(props, "stream", None), "name", None)
            or getattr(getattr(props, "airbyte_stream", None), "name", None)
            or default_spec.key.path[-1]
        )


        # Decide the dbt source name based on connection (preferred) or stream naming convention 
        connection_name = getattr(getattr(props, "connection", None), "name", None)

        # mapping the connection name in Airbyte to the source name in dbt
        stream_lower = stream_name.lower()

        if ("countries" in stream_lower):
            source_name = "amazon_s3"
        elif ("earthquake" in stream_lower):
            source_name = "earthquake_api"
        else:
            source_name = "airbyte"

        return default_spec.replace_attributes(
            key=dg.AssetKey([source_name, stream_name]),
            group_name=f"airbyte_{source_name}",
        )



# Connect to Airbyte Cloud workspace
airbyte_workspace = AirbyteCloudWorkspace(
    
    #local
    #rest_api_base_url="http://localhost:8000/api/public/v1",
    #configuration_api_base_url="http://localhost:8000/api/v1",
    
    workspace_id=dg.EnvVar("AIRBYTE_WORKSPACE_ID"),
    client_id=dg.EnvVar("AIRBYTE_CLIENT_ID"),
    client_secret=dg.EnvVar("AIRBYTE_CLIENT_SECRET"),
)

# Load all assets from Airbyte workspace
airbyte_assets = build_airbyte_assets_definitions(workspace=airbyte_workspace, 
                                                    dagster_airbyte_translator=CustomDagsterAirbyteTranslator()
                                                    )

# defining amazon s3 job
amazon_s3_job = dg.define_asset_job(
    name="amazon_s3_job",
    selection=dg.AssetSelection.keys(
        dg.AssetKey(["amazon_s3", "allCountries"]),
        dg.AssetKey(["amazon_s3", "countries_regional_codes"])
    )
)                

# defining earthquake api job
earthquake_api_job = dg.define_asset_job(
    name="earthquake_api",
    selection=dg.AssetSelection.keys(
        dg.AssetKey([ "earthquake_api", "Earthquake"])
    )
)          


defs = dg.Definitions(
    assets=airbyte_assets,
    resources={"airbyte": airbyte_workspace},
)