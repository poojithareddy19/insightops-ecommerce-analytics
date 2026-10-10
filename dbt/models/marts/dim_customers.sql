-- Author: Gorla Poojitha
-- Grain: ONE ROW PER REAL CUSTOMER (customer_unique_id).

with customer_orders as (
    select
        c.customer_unique_id,
        c.customer_city,
        c.customer_state,
        o.purchased_at
    from {{ ref('stg_customers') }} c
    join {{ ref('stg_orders') }} o on c.customer_id = o.customer_id
),

latest_location as (
    -- a customer can move, so keep the location from their most recent order
    select * exclude (row_num)
    from (
        select
            *,
            row_number() over (partition by customer_unique_id order by purchased_at desc) as row_num
        from customer_orders
    )
    where row_num = 1
),

order_stats as (
    select
        customer_unique_id,
        min(purchased_at)                                        as first_order_at,
        max(purchased_at)                                        as last_order_at,
        count(*) filter (where is_valid_order)                   as valid_orders,
        count(distinct order_date) filter (where is_valid_order) as valid_order_days,
        coalesce(sum(order_value) filter (where is_valid_order), 0) as lifetime_revenue
    from {{ ref('fct_orders') }}
    group by customer_unique_id
)

select
    l.customer_unique_id,
    l.customer_city,
    l.customer_state,
    s.first_order_at,
    s.last_order_at,
    date_trunc('month', s.first_order_at) as cohort_month,
    s.valid_orders,
    s.lifetime_revenue,
    s.valid_orders >= 2                   as is_repeat_customer,
    -- 250 customers have 2 orders at the same second (one checkout split in two),
    -- so "came back on another day" is the stricter, more honest retention flag
    s.valid_order_days >= 2               as is_returning_customer
from latest_location l
join order_stats s on l.customer_unique_id = s.customer_unique_id
