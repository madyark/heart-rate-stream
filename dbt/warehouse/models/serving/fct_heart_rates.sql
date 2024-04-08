select
    user_id,
    to_date(to_timestamp_ntz(timestamp::string)) as date,
    to_char(to_time(to_timestamp_ntz(timestamp::string)), 'HH24:MI:SS') AS time,
    heart_rate,
    lag(heart_rate) over (partition by user_id, activity_id, date order by timestamp) as previous_heart_rate,
    max(heart_rate) over (partition by user_id, activity_id, date) AS max_heart_rate,
    min(heart_rate) over (partition by user_id, activity_id, date) AS min_heart_rate,
    round(avg(heart_rate) over (partition by user_id, activity_id, date),2) AS avg_heart_rate,
    activity_id,
    latitude,
    longitude

from 
    {{ ref('stg_heart_rates') }} 

where 
    activity_id LIKE '2____' -- filter out stream data that used test activity_id values

order by 
    date, 
    time, 
    user_id, 
    activity_id, 
    latitude, 
    longitude