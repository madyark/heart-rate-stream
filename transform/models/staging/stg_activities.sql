 -- Create a type 2 SCD for the activities table by adding effective date columns for updated and deleted rows 

with updated_rows as (
    select 
        activity_id,
        activity_name,
        last_update as start_date,
        lead(last_update) over (partition by activity_id order by last_update) as end_date
    from {{ source('operational_data', 'activities') }} 
), 

deleted_rows as (
    select 
        activity_id, 
        _ab_cdc_deleted_at
    from {{ source('operational_data', 'activities') }} 
    where _ab_cdc_deleted_at is not null
)

select
    ur.activity_id,
    ur.activity_name,
    ur.start_date,
    case 
        when dr._ab_cdc_deleted_at is not null then dr._ab_cdc_deleted_at -- use deleted_at value as end_date if the row is deleted
        else ur.end_date -- else use the end_date from updated_rows
    end as end_date
from updated_rows ur
left join deleted_rows dr on ur.activity_id = dr.activity_id
where ur.start_date is not null -- filters out the empty deleted_row field 
