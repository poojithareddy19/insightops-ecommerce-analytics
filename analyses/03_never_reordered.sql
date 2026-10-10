-- Business question: What share of customers never placed a second order?
-- Technique: anti-join with NOT EXISTS (find rows that have NO match).

with first_orders as (
    select customer_unique_id, min(purchased_at) as first_purchase_at
    from marts.fct_orders
    where is_valid_order
    group by 1
)

select
    count(*)                                                    as customers,
    count(*) filter (where not exists (
        select 1
        from marts.fct_orders later
        where later.customer_unique_id = f.customer_unique_id
          and later.is_valid_order
          and later.purchased_at > f.first_purchase_at
    ))                                                          as never_reordered,
    round(100.0 * never_reordered / customers, 1)               as never_reordered_pct
from first_orders f;

-- Stricter version: did they come back on a DIFFERENT DAY?
-- 250 customers have two orders at the exact same second (one checkout split into two orders),
-- and more have a second order the same day. Neither is a return visit.
select
    count(*)                                                          as customers,
    count(*) filter (where is_returning_customer)                     as came_back_another_day,
    round(100.0 * count(*) filter (where is_returning_customer) / count(*), 2) as returning_pct
from marts.dim_customers
where valid_orders > 0;
