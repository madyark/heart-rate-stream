select
    user_id,
    first_name,
    last_name,
    date_of_birth,
    sex,
    height,
    weight,
    blood_type, 
    race, 
    origin_country_name as origin_country,
    address,
    address_country_name as address_country,
    last_update as start_date,
    lead(last_update) over (partition by user_id order by last_update) as end_date

from 
    {{ source('operational_data', 'users') }}

order by 
    user_id, start_date

