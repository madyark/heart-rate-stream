{{
    config(
        materialized="incremental"
    )
}}

select 
    user_id,
    timestamp::string as timestamp,
    heart_rate,
    meta:activity_id::string as activity_id,
    meta:location:latitude::string as latitude,
    meta:location:longitude::string as longitude,
    _airbyte_extracted_at as extracted_at

from 
    {{ source('stream_data', 'heart_rate_stream') }} 


{% if is_incremental() %}
    where extracted_at > (select max(extracted_at) from {{ this }} )
{% endif %}
