-- Assert that the end date column in a type 2 SCD table is equal to the next start_date column (for rows with a non-null end date)

{% test correct_scd_start_end_dates(model, id_column, start_date_column, end_date_column) %}

with validation as (

    select 
        {{ id_column }} as id, 
        {{ start_date_column }} as start_date, 
        {{ end_date_column }} as end_date, 
        lead(start_date) over (partition by id order by start_date) as next_start_date 

    from {{ model }}

),

validation_errors as (

    select *

    from validation
    
    where end_date <> next_start_date

)

select *
from validation_errors

{% endtest %}