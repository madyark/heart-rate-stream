{{
  config(
    cluster_by=['event_date'],
    meta={
        "dagster":{
            "freshness_policy": {
                "maximum_lag_minutes": 1,
                "cron_schedule": "30 2 * * *"
            }
        }
    }
  )
}}


-- use users dimension to map user_id from heart rate data to correct user_key
with users as ( 
    select 
        user_key,
        user_id,
        start_date as user_start_date,
        end_date as user_end_date
    
    from 
        {{ ref('dim_users') }} 
), 

-- user activities dimension to map activity_id from heart rate data to correct activity_key
activities as (
    select 
        activity_key, 
        activity_id,
        start_date as activity_start_date,
        end_date as activity_end_date
    
    from 
        {{ ref('dim_activities') }} 
)

select
    u.user_key,
    a.activity_key,
    to_date(to_timestamp_ntz(hr.timestamp)) as event_date,
    to_char(to_time(to_timestamp_ntz(hr.timestamp)), 'HH24:MI:SS')::time AS event_time,
    to_timestamp_ntz(hr.timestamp) as event_datetime,
    hr.heart_rate,
    lag(hr.heart_rate) over (partition by u.user_key, hr.activity_id, hr.latitude, hr.longitude, event_date order by timestamp) as previous_heart_rate,
    max(hr.heart_rate) over (partition by u.user_key, hr.activity_id, hr.latitude, hr.longitude, event_date) AS max_heart_rate,
    min(heart_rate) over (partition by u.user_key, hr.activity_id, hr.latitude, hr.longitude, event_date) AS min_heart_rate,
    round(avg(heart_rate) over (partition by u.user_key, hr.activity_id, hr.latitude, hr.longitude, event_date),2) AS avg_heart_rate,
    hr.latitude,
    hr.longitude

from 
    {{ ref('stg_heart_rates') }} hr

inner join users u
    on u.user_id=hr.user_id
        and event_datetime between u.user_start_date and coalesce(u.user_end_date, current_timestamp)

inner join activities a
    on a.activity_id=hr.activity_id
        and event_datetime between a.activity_start_date and coalesce(a.activity_end_date, current_timestamp)
