{{
    config(
        materialized="incremental"
    )
}}

select
    activity_id,
    activity_name,
    last_update,
    _ab_cdc_deleted_at as deleted_at,
    _airbyte_extracted_at as extracted_at

from {{ source('operational_data', 'activities') }} 

{% if is_incremental() %}
    where extracted_at > (select max(extracted_at) from {{ this }} )
{% endif %}
