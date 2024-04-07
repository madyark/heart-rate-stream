select 
    activity_id,
    activity_name, 
    last_update

from {{ source('mock_operational_data', 'users') }}