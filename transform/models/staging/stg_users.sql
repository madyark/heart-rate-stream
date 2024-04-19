{{
    config(
        materialized="incremental",
        incremental_strategy='append'
    )
}}

select
    user_id::string as user_id,
    first_name::string as first_name,
    last_name::string as last_name,
    date_of_birth::int as date_of_birth,
    sex::string as sex,
    height::int as height,
    weight::int as weight,
    blood_type::string as blood_type, 
    race::string as race, 
    origin_country_code::string as origin_country_code,
    origin_country_name::string as origin_country_name,
    address::string as address,
    address_country_code::string as address_country_code,
    address_country_name::string as address_country_name,
    last_update::timestamp_ntz as last_update,
    _ab_cdc_deleted_at::timestamp_ntz as deleted_at,
    _airbyte_extracted_at::timestamp_ntz as extracted_at

from 
    {{ source('raw', 'users') }} 

{% if is_incremental() %}
    where extracted_at > (select max(extracted_at) from {{ this }} )
{% endif %}
