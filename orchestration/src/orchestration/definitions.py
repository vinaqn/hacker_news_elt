from pathlib import Path

from dagster import Definitions, load_from_defs_folder
from src.orchestration.defs.assets.airbyte import airbyte_assets,airbyte_workspace,amazon_s3_job,earthquake_api_job
from dagster_airbyte import AirbyteResource

defs=Definitions(
    assets=[*airbyte_assets],
    jobs=[amazon_s3_job,earthquake_api_job],
    resources={
        "airbyte": airbyte_workspace
    }
)