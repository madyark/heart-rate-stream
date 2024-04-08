from dagster import EnvVar
from dagster_airbyte import AirbyteResource, load_assets_from_airbyte_instance

airbyte_resource = AirbyteResource(
    host=EnvVar("AIRBYTE_HOST"),
    port=EnvVar("AIRBYTE_PORT"),
    username=EnvVar("AIRBYTE_USERNAME"),
    password=EnvVar("AIRBYTE_PASSWORD"),
)

airbyte_assets = load_assets_from_airbyte_instance(
    airbyte_resource
)