from dagster import Definitions, load_assets_from_package_module
from analytics.assets.airbyte.airbyte import airbyte_assets_streaming
from analytics.assets.dbt.dbt import dbt_warehouse, dbt_warehouse_resource

defs = Definitions(
    assets=[airbyte_assets_streaming, dbt_warehouse],
    resources={
        "dbt_warehouse_resource": dbt_warehouse_resource
    }
)