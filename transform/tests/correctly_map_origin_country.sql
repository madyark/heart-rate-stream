-- Assert the the origin_country_code field in each user record maps to the correct origin_country_name

select u.origin_country_code,
       u.origin_country_name,
       c.name as correct_country_name
from {{ source('stream_data', 'users') }} u
inner join {{ ref('country_codes' )}} c on u.origin_country_code = c.alpha2
where u.origin_country_name <> c.name