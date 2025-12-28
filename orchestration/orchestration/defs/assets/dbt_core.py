import os
from pathlib import Path

from dagster_dbt import DbtCliResource, dbt_assets, DagsterDbtTranslator
from dagster import AssetExecutionContext
import dagster as dg




class CustomDagsterDbtTranslator(DagsterDbtTranslator):
    def get_automation_condition(self, dbt_resource_props): 
        return dg.AutomationCondition.eager() 


def resolve_dbt_project_dir() -> Path:
    """
    Works for both:
    - local dev (repo checkout)
    - ECS container (/app layout)
    """
    container_path = Path("/app/transform/dbt/earthquake")
    if container_path.exists():
        return container_path

    # local: walk up until we find the repo root containing /transform
    here = Path(__file__).resolve()
    for parent in [here, *here.parents]:
        candidate = parent / "transform" / "dbt" / "earthquake"
        if candidate.exists():
            return candidate

    raise FileNotFoundError("Could not locate dbt project directory 'transform/dbt/earthquake'.")


dbt_project_dir = resolve_dbt_project_dir()
dbt_warehouse_resource = DbtCliResource(project_dir=str(dbt_project_dir))


# load manifest to produce asset defintion
dbt_manifest_path = dbt_project_dir / "target" / "manifest.json"
if not dbt_manifest_path.exists():
    # Optional: either build the manifest during Docker build, OR allow Dagster to run without dbt assets
    # For now, fail loudly so you know to generate it.
    raise FileNotFoundError(f"dbt manifest not found at {dbt_manifest_path}. "
                            f"Run `dbt parse` or `dbt build` to generate it (or generate it in your Dockerfile).")

@dbt_assets(
    manifest=str(dbt_manifest_path),
    dagster_dbt_translator=CustomDagsterDbtTranslator(),
)
def dbt_warehouse(context: AssetExecutionContext, dbt_warehouse_resource: DbtCliResource):
     # Ensure deps are installed
    yield from dbt_warehouse_resource.cli(["deps"]).stream()

    # Then run dbt
    yield from dbt_warehouse_resource.cli(["build"], context=context).stream()