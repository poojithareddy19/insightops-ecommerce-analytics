-- Author: Gorla Poojitha
-- Business question: Which categories are expensive to ship, relative to what they sell for?
-- Techniques: ratio of sums (not average of ratios), HAVING, RANK.

select
    p.category_name,
    count(*)                                                     as items_sold,
    round(sum(i.price), 0)                                       as product_revenue,
    round(sum(i.freight_value), 0)                               as freight_revenue,
    round(100.0 * sum(i.freight_value) / sum(i.item_total), 1)   as freight_share_pct,
    rank() over (order by sum(i.freight_value) / sum(i.item_total) desc) as freight_rank
from marts.fct_order_items i
join marts.dim_products p on i.product_id = p.product_id
where i.is_valid_order
group by 1
having count(*) >= 500   -- ignore categories too small to plan around
order by freight_share_pct desc
limit 15;
