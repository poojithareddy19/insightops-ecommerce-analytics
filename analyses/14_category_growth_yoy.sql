-- Author: Gorla Poojitha
-- Business question: Which categories grew fastest from 2017 to 2018?
-- Only January to August is compared, because the data stops in August 2018.
-- Techniques: conditional aggregation, growth rate, minimum-size filter.

with category_year as (
    select
        p.category_name,
        sum(i.price) filter (where year(i.order_date) = 2017) as revenue_2017,
        sum(i.price) filter (where year(i.order_date) = 2018) as revenue_2018
    from marts.fct_order_items i
    join marts.dim_products p on i.product_id = p.product_id
    where i.is_valid_order
      and month(i.order_date) between 1 and 8
    group by 1
)

select
    category_name,
    round(revenue_2017, 0)                                          as revenue_jan_aug_2017,
    round(revenue_2018, 0)                                          as revenue_jan_aug_2018,
    round(100.0 * (revenue_2018 - revenue_2017) / revenue_2017, 1)  as growth_pct
from category_year
where revenue_2017 >= 50000   -- small categories swing wildly, so skip them
order by growth_pct desc;
