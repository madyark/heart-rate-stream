from dagster import Definitions, define_asset_job, ScheduleDefinition, AssetSelection
from orchestrate.assets.airbyte.airbyte import airbyte_assets_streaming
from orchestrate.assets.dbt.dbt import dbt_warehouse, dbt_warehouse_resource

run_everything_job = define_asset_job("run_everything", selection="*")

defs = Definitions(
    assets=[airbyte_assets_streaming, dbt_warehouse],
    resources={
        "dbt_warehouse_resource": dbt_warehouse_resource
    },
    schedules=[
        ScheduleDefinition(
            job=run_everything_job,
            cron_schedule="@daily",
        ),
    ],
)