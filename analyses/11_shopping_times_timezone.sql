-- Business question: When do customers shop? (local Brazil time vs UTC)
-- Techniques: timezone conversion, extracting day of week and hour.
-- Olist timestamps are in Sao Paulo local time with no timezone attached.

with orders as (
    select
        purchased_at                                          as local_time,
        timezone('UTC', timezone('America/Sao_Paulo', purchased_at)) as utc_time
    from marts.fct_orders
    where is_valid_order
)

select
    dayname(local_time)          as day_of_week,
    hour(local_time)             as local_hour,
    hour(utc_time)               as utc_hour,
    count(*)                     as orders
from orders
group by 1, 2, 3
order by orders desc
limit 15;
