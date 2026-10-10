-- Author: Gorla Poojitha
-- Business question: How is revenue trending month over month?
-- Techniques: date_trunc, LAG window function, running total (SUM OVER).

with monthly as (
    select
        date_trunc('month', order_date) as order_month,
        count(*)                        as orders,
        sum(order_value)                as revenue
    from marts.fct_orders
    where is_valid_order
    group by 1
)

select
    order_month,
    orders,
    round(revenue, 0)                                          as revenue,
    round(revenue / orders, 2)                                 as aov,
    round(100.0 * (revenue - lag(revenue) over (order by order_month))
          / lag(revenue) over (order by order_month), 1)       as revenue_mom_pct,
    round(sum(revenue) over (order by order_month), 0)         as running_revenue
from monthly
order by order_month;
