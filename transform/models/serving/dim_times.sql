-- Times reference data (to be loaded once and persisted)

with h as (
  select 
    lpad(seq2(), 2, '0') as hour
  
  from 
    table(generator(rowcount => 24))
),

m as (
  select 
    lpad(seq2(), 2, '0') as minute
  
  from 
    table(generator(rowcount => 60))
),

s as (
  select 
    lpad(seq2(), 2, '0') as second
  
  from 
    table(generator(rowcount => 60))
)

select 
    h.hour || ':' || m.minute || ':' || s.second as hh_mm_ss,
    h.hour, 
    m.minute, 
    s.second,
    case 
        when h.hour::int < 6 then 'Night'
        when h.hour::int < 12 then 'Morning'
        when h.hour::int < 18 then 'Afternoon'
        else 'Evening'
    end as time_of_day

from h

cross join m

cross join s

order by hour, minute, second