with users as (

    select * from {{ source('operational_data', 'users') }}

),

final as (

    select
        users.user_id,
        users.first_name,
        users.last_name,
        users.date_of_birth,
        users.sex,
        users.height,
        users.weight,
        users.blood_type, 
        users.race, 
        users.origin_country_code,
        users.origin_country_name,
        users.address,
        users.address_country_code,
        users.address_country_name,
        users.last_update

    from users
    
)

select * from final