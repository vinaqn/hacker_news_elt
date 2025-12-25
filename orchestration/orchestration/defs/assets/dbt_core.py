import os
from pathlib import Path

from dagster_dbt import DbtCliResource, dbt_assets, DagsterDbtTranslator
from dagster import AssetExecutionContext
import dagster as dg

# configure dbt project resource; construct relative path
repo_root = Path(__file__).resolve().parents[4]
dbt_project_dir = repo_root / "transform" / "dbt" / "earthquake"

dbt_warehouse_resource = DbtCliResource(project_dir=os.fspath(dbt_project_dir))



# generate manifest
dbt_manifest_path = (
    dbt_warehouse_resource.cli(
        ["--quiet", "parse"],
        target_path=Path("target"),
    )
    .wait()
    .target_path.joinpath("manifest.json")
)

class CustomDagsterDbtTranslator(DagsterDbtTranslator):
    def get_automation_condition(self, dbt_resource_props): 
        return dg.AutomationCondition.eager()

# load manifest to produce asset defintion
@dbt_assets(manifest=dbt_manifest_path, 
            dagster_dbt_translator=CustomDagsterDbtTranslator()
            )
def dbt_warehouse(context: AssetExecutionContext, dbt_warehouse_resource: DbtCliResource):
    yield from dbt_warehouse_resource.cli(["run"], context=context).stream()