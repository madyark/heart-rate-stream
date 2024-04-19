{{
    config(
        materialized="incremental",
        incremental_strategy='append'
    )
}}

select 
    user_id::string as user_id,
    timestamp::string as timestamp,
    heart_rate::int as heart_rate,
    meta:activity_id::string as activity_id,
    meta:location:latitude::string as latitude,
    meta:location:longitude::string as longitude,
    _airbyte_extracted_at::timestamp_ntz as extracted_at

from 
    {{ source('raw', 'heart_rate_stream') }} 

where 
    -- Remove heart rate records that were used for testing (with different/invalid user and activity IDs)
    timestamp > 1712343600 

{% if is_incremental() %}
    and extracted_at > (select max(extracted_at) from {{ this }} )
{% endif %}
