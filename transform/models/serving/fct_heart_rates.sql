select
    user_id,
    timestamp,
    heart_rate,
    activity_id,
    latitude,
    longitude,
    extracted_at

from 
    {{ ref('stg_heart_rate') }} 