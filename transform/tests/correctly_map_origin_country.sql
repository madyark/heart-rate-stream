select u.origin_country_code,
       u.origin_country_name,
       c.name as correct_country_name
from {{ source('stream_data', 'users') }} u
inner join {{ ref('country_codes' )}} c on u.origin_country_code = c.alpha2
where u.origin_country_name <> c.name