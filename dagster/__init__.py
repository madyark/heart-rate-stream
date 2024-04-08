from dagster import Definitions, load_assets_from_package_module
from dagster.assets.airbyte.airbyte import airbyte_assets_streaming
from dagster.assets.dbt.dbt import dbt_warehouse, dbt_warehouse_resource

defs = Definitions(
    assets=[airbyte_assets_streaming, dbt_warehouse],
    resources={
        "dbt_warehouse_resource": dbt_warehouse_resource
    }
)