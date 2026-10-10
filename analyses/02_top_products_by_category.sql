-- Business question: Which products lead each of the top 5 categories?
-- Techniques: joins, DENSE_RANK window function, QUALIFY to filter on a window result.

with category_revenue as (
    select
        p.category_name,
        sum(i.price) as revenue
    from marts.fct_order_items i
    join marts.dim_products p on i.product_id = p.product_id
    where i.is_valid_order
    group by 1
    order by revenue desc
    limit 5
),

product_revenue as (
    select
        p.category_name,
        i.product_id,
        sum(i.price) as revenue,
        count(*)     as units
    from marts.fct_order_items i
    join marts.dim_products p on i.product_id = p.product_id
    where i.is_valid_order
      and p.category_name in (select category_name from category_revenue)
    group by 1, 2
)

select
    category_name,
    product_id,
    units,
    round(revenue, 0) as revenue,
    dense_rank() over (partition by category_name order by revenue desc) as rank_in_category
from product_revenue
qualify rank_in_category <= 3
order by category_name, rank_in_category;
