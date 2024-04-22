# Installs dbt dependencies when deploying to Dagster Cloud Serverless 
# https://github.com/dagster-io/dagster/discussions/12180

dbt deps --project-dir ./transform/ --target prod