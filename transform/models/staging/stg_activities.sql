{{
    config(
        materialized="incremental",
        incremental_strategy='append'
    )
}}

select
    activity_id::string as activity_id,
    activity_name::string as activity_name,
    last_update::timestamp_ntz as last_update,
    _ab_cdc_deleted_at::timestamp_ntz as deleted_at,
    _airbyte_extracted_at::timestamp_ntz as extracted_at

from 
    {{ source('raw', 'activities') }} 

{% if is_incremental() %}
    where extracted_at > (select max(extracted_at) from {{ this }} )
{% endif %}
