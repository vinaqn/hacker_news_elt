from dagster_airbyte import AirbyteWorkspace, build_airbyte_assets_definitions, DagsterAirbyteTranslator

import dagster as dg

class CustomDagsterAirbyteTranslator(DagsterAirbyteTranslator):
    def get_asset_spec(self, props):
        default_spec = super().get_asset_spec(props)

        # props is an object (AirbyteConnectionTableProps), not a dict
        stream_name = (
            getattr(props, "name", None)
            or getattr(getattr(props, "stream", None), "name", None)
            or getattr(getattr(props, "airbyte_stream", None), "name", None)
        )
        if not stream_name:
            stream_name = default_spec.key.path[-1]

        return default_spec.replace_attributes(
            key=dg.AssetKey(["airbyte", "earthquake", stream_name]),
            group_name="airbyte_earthquake",
            automation_condition=dg.AutomationCondition.on_cron(cron_schedule="* * * * *"),
        )



# Connect to OSS Airbyte instance
airbyte_workspace = AirbyteWorkspace(
    rest_api_base_url="http://localhost:8000/api/public/v1",
    configuration_api_base_url="http://localhost:8000/api/v1",
    workspace_id=dg.EnvVar("AIRBYTE_WORKSPACE_ID"),
    # If using basic auth, include username and password:
    client_id=dg.EnvVar("AIRBYTE_CLIENT_ID"),
    client_secret=dg.EnvVar("AIRBYTE_CLIENT_SECRET"),
)

# Load all assets from Airbyte workspace
airbyte_assets = build_airbyte_assets_definitions(workspace=airbyte_workspace, 
                                                    dagster_airbyte_translator=CustomDagsterAirbyteTranslator()
                                                    )


amazon_s3_job = dg.define_asset_job(
    name="amazon_s3_job",
    selection=dg.AssetSelection.keys(
        dg.AssetKey(["airbyte", "earthquake", "allCountries"]),
        dg.AssetKey(["airbyte", "earthquake", "countries_regional_codes"])
    )
)                

earthquake_api_job = dg.define_asset_job(
    name="earthquake_api",
    selection=dg.AssetSelection.keys(
        dg.AssetKey(["airbyte", "earthquake", "Earthquake"])
    )
)          


defs = dg.Definitions(
    assets=airbyte_assets,
    resources={"airbyte": airbyte_workspace},
)