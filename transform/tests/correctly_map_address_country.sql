-- Assert the the address_country_code field in each user record maps to the correct address_country_name

select u.address_country_code,
       u.address_country_name,
       c.name as correct_country_name
from {{ source('stream_data', 'users') }} u
inner join {{ ref('country_codes' )}} c on u.address_country_code = c.alpha2
where u.address_country_name <> c.name