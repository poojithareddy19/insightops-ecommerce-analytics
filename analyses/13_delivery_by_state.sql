-- Author: Gorla Poojitha
-- Business question: Which states have the slowest deliveries and the most late orders?
-- Techniques: median, conditional average, comparing each state to the national figure.

with state_delivery as (
    select
        customer_state,
        count(*)                                              as delivered_orders,
        median(delivery_days)                                 as median_delivery_days,
        avg(case when is_late then 1 else 0 end)              as late_rate
    from marts.fct_orders
    where is_delivered
    group by 1
),

national as (
    select
        median(delivery_days)                    as median_delivery_days,
        avg(case when is_late then 1 else 0 end) as late_rate
    from marts.fct_orders
    where is_delivered
)

select
    s.customer_state,
    s.delivered_orders,
    s.median_delivery_days,
    round(100.0 * s.late_rate, 1)                              as late_pct,
    s.median_delivery_days - n.median_delivery_days            as days_vs_national_median,
    round(100.0 * (s.late_rate - n.late_rate), 1)              as late_pp_vs_national
from state_delivery s
cross join national n
order by s.median_delivery_days desc, s.late_rate desc;
