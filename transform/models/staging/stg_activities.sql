with activities as (

    select * from {{ source('operational_data', 'activities') }} 

),

final as (

    select 
        activity_id,
        activity_name, 
        last_update

    from activities

)

select * from final