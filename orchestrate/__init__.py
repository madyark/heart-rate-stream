from dagster import Definitions, ScheduleDefinition, AssetSelection
from orchestrate.assets.airbyte.airbyte import airbyte_assets_streaming
from orchestrate.assets.dbt.dbt import dbt_warehouse, dbt_warehouse_resource

defs = Definitions(
    assets=[airbyte_assets_streaming, dbt_warehouse],
    resources={
        "dbt_warehouse_resource": dbt_warehouse_resource
    },
)