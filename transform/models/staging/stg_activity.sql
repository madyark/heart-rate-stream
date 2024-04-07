select 
    activity_id,
    activity_name, 
    last_update

from {{ source('operational_data', 'activities') }}