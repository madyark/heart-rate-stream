-- Dates reference data (to be loaded once and persisted)

{{ dbt_date.get_date_dimension(start_date="1900-01-01", end_date="2099-12-31") }}