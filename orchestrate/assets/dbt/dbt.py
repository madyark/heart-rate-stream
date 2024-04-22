import os
from pathlib import Path
from dagster_dbt import DbtCliResource
from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets

# Configure dbt CLI resource
dbt_project_dir = Path(__file__).joinpath("..", "..", "..", "..", "transform").resolve()
dbt_warehouse_resource = DbtCliResource(project_dir=os.fspath(dbt_project_dir))

# Configure manifest.json file path
dbt_manifest_path = dbt_project_dir.joinpath("target", "manifest.json")

# Load dbt assets from manifest.json file
@dbt_assets(manifest=dbt_manifest_path)
def dbt_warehouse(context: AssetExecutionContext, dbt_warehouse_resource: DbtCliResource):
    yield from dbt_warehouse_resource.cli(["build", "--target", "prod"], context=context).stream()