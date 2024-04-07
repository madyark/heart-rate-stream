-- Create a Type 2 SCD for users by adding effective date columns for updated and deleted rows 

with updated_rows as (
    select
        user_id,
        first_name,
        last_name,
        {{ dob_transform('date_of_birth') }},
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
        {{ ref('stg_users') }} 
), 

deleted_rows as (
    select 
        user_id, 
        deleted_at
    
    from 
        {{ ref('stg_users') }} 
    
    where 
        deleted_at is not null
),

final as (
    select
        {{ dbt_utils.generate_surrogate_key(['ur.user_id', 'ur.start_date', 'ur.end_date']) }} as user_key,
        ur.user_id,
        ur.first_name,
        ur.last_name,
        ur.date_of_birth,
        ur.sex,
        ur.height,
        ur.weight,
        ur.blood_type, 
        ur.race, 
        ur.origin_country,
        ur.address,
        ur.address_country,
        ur.start_date,
        case 
            when dr.deleted_at is not null then dr.deleted_at -- use deleted_at value as end_date if the row is deleted
            else ur.end_date -- else use the end_date from updated_rows
        end as end_date
    
    from 
        updated_rows ur
    
    left join 
        deleted_rows dr on ur.user_id = dr.user_id
    
    where 
        ur.start_date is not null -- filters out the empty deleted_row field 
    
    order by 
        ur.date_of_birth -- clustering key as column likely to be used in filtering
)

select * from final