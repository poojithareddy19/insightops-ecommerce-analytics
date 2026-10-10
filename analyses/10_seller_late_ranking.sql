-- Business question: Which sellers cause the most late deliveries?
-- Techniques: multi-table joins, HAVING (filter after grouping), RANK.

with seller_orders as (
    select distinct
        i.seller_id,
        o.order_id,
        o.is_late,
        o.review_score
    from marts.fct_order_items i
    join marts.fct_orders o on i.order_id = o.order_id
    where o.is_delivered
)

select
    s.seller_id,
    d.seller_state,
    count(*)                                          as delivered_orders,
    round(100.0 * avg(case when s.is_late then 1 else 0 end), 1) as late_pct,
    round(avg(s.review_score), 2)                     as avg_review,
    rank() over (order by avg(case when s.is_late then 1 else 0 end) desc) as late_rank
from seller_orders s
join marts.dim_sellers d on s.seller_id = d.seller_id
group by 1, 2
having count(*) >= 20   -- ignore tiny sellers, their rates are noisy (use 20 on real data)
order by late_pct desc
limit 20;
