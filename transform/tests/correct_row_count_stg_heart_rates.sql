-- Asserts that the row count of stg_heart_rates is equal that of the raw table but without the invalid records (no further missing or added rows)

with raw_hr_table as (
    select count(*) as raw_row_count
    from {{ source('raw', 'heart_rate_stream') }} 
),

filtered_raw_hr_table as (
    select count(*) as filtered_raw_row_count
    from {{ source('raw', 'heart_rate_stream') }} 
    where timestamp<='1712343600'
),

stg_hr_table as (
    select count(*) as stg_row_count
    from {{ ref('stg_heart_rates') }}
)

select 
    raw_hr_table.raw_row_count - filtered_raw_hr_table.filtered_raw_row_count AS expected_stg_row_count,
    stg_hr_table.stg_row_count AS actual_stg_row_count

from raw_hr_table, filtered_raw_hr_table, stg_hr_table

where 
    expected_stg_row_count <> actual_stg_row_count

