from dagster import Definitions, load_assets_from_package_module
from orchestrate.assets.airbyte.airbyte import airbyte_assets_streaming
from orchestrate.assets.dbt.dbt import dbt_warehouse, dbt_warehouse_resource

defs = Definitions(
    assets=[dbt_warehouse],
    resources={
        "dbt_warehouse_resource": dbt_warehouse_resource
    }
)