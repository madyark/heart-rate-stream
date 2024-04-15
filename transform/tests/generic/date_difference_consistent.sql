-- Assert the date in the column is the correct derived calculation from a base date column (potential for errors when dealing with leap year dates)

{% test date_difference_consistent(model, column_name, date_part, difference_value, base_date_column) %}

with validation as (

    select
        {{ column_name }} as target_date_column,
        {{ base_date_column }} as base_date_column

    from {{ model }}

),

validation_errors as (

    select
        target_date_column,
        dateadd({{ date_part }}, {{ difference_value }}, to_date(base_date_column)) as derived_date

    from validation
    
    where target_date_column <> derived_date

)

select *
from validation_errors

{% endtest %}