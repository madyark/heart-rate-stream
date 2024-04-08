from dagster import Definitions, load_assets_from_modules
from analytics.assets.airbyte.airbyte import airbyte_assets

defs = Definitions(
    assets=[airbyte_assets],
)
