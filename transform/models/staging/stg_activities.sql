select 
    activity_id,
    activity_name,
    last_update as start_date,
    lead(last_update) over (partition by user_id order by last_update) as end_date

from {{ source('operational_data', 'activities') }} 
