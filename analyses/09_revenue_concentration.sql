-- Business question: What % of revenue comes from the top 10% of customers?
-- Techniques: NTILE(10) deciles, share of total with SUM() OVER ().

with customer_revenue as (
    select customer_unique_id, sum(order_value) as revenue
    from marts.fct_orders
    where is_valid_order
    group by 1
),

deciles as (
    select *, ntile(10) over (order by revenue desc) as decile  -- decile 1 = top 10%
    from customer_revenue
)

select
    decile,
    count(*)                                                     as customers,
    round(sum(revenue), 0)                                       as revenue,
    round(100.0 * sum(revenue) / sum(sum(revenue)) over (), 1)   as pct_of_revenue,
    round(100.0 * sum(sum(revenue)) over (order by decile)
          / sum(sum(revenue)) over (), 1)                        as cumulative_pct
from deciles
group by decile
order by decile;
