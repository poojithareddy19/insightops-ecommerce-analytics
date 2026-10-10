-- Business question: For customers who come back, how long until their second order?
-- This tells us when a "come back" offer should go out.
-- Techniques: LAG within each customer, QUALIFY, percentiles.

with ordered as (
    select
        customer_unique_id,
        purchased_at,
        row_number() over (partition by customer_unique_id order by purchased_at) as order_number,
        lag(purchased_at) over (partition by customer_unique_id order by purchased_at) as previous_purchase_at
    from marts.fct_orders
    where is_valid_order
),

second_orders as (
    select
        customer_unique_id,
        date_diff('day', previous_purchase_at, purchased_at) as days_to_second_order
    from ordered
    where order_number = 2
)

select
    count(*)                                                       as repeat_customers,
    count(*) filter (where days_to_second_order = 0)               as same_day_second_order,
    quantile_cont(days_to_second_order, 0.25)                      as p25_days,
    median(days_to_second_order)                                   as median_days,
    quantile_cont(days_to_second_order, 0.75)                      as p75_days,
    round(100.0 * avg(case when days_to_second_order <= 30 then 1 else 0 end), 1)  as within_30_days_pct,
    round(100.0 * avg(case when days_to_second_order <= 90 then 1 else 0 end), 1)  as within_90_days_pct
from second_orders;
