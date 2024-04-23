from dagster import EnvVar, AutoMaterializePolicy
from dagster_airbyte import AirbyteResource, load_assets_from_airbyte_instance

airbyte_resource = AirbyteResource(
    host=EnvVar("AIRBYTE_HOST"),
    port=EnvVar("AIRBYTE_PORT"),
    username=EnvVar("AIRBYTE_USERNAME"),
    password=EnvVar("AIRBYTE_PASSWORD"),
)

airbyte_assets_streaming = load_assets_from_airbyte_instance(
    airbyte_resource,
    key_prefix="raw",
    connection_to_auto_materialize_policy_fn=lambda _: AutoMaterializePolicy.eager(),
)