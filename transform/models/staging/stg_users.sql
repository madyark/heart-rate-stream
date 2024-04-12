{{
    config(
        materialized="incremental",
        incremental_strategy='append'
    )
}}

select
    user_id,
    first_name,
    last_name,
    date_of_birth,
    sex,
    height,
    weight,
    blood_type, 
    race, 
    origin_country_code,
    origin_country_name,
    address,
    address_country_code,
    address_country_name,
    last_update,
    _ab_cdc_deleted_at as deleted_at,
    _airbyte_extracted_at as extracted_at

from 
    {{ source('stream_data', 'users') }} 

{% if is_incremental() %}
    where extracted_at > (select max(extracted_at) from {{ this }} )
{% endif %}
