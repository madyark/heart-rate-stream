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
    origin_country_code,
    origin_country_name,
    address,
    address_country_code,
    address_country_name,
    last_update

from {{ source('operational_data', 'users') }}