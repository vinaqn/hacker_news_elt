from pathlib import Path

from dagster import Definitions, load_from_defs_folder
from orchestration.defs.assets.airbyte import airbyte_assets,airbyte_workspace,amazon_s3_job,earthquake_api_job
from orchestration.defs.assets.dbt_core import dbt_warehouse_resource,dbt_warehouse
from dagster_airbyte import AirbyteResource

defs=Definitions(
    assets=[*airbyte_assets,dbt_warehouse],
    jobs=[amazon_s3_job,earthquake_api_job],
    resources={
        "airbyte": airbyte_workspace,
        "dbt_warehouse_resource": dbt_warehouse_resource
    }
)