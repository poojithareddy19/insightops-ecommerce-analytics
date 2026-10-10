-- Capstone: Does the FIRST order experience predict whether a customer comes back?
-- For each customer we look only at their first valid order.
--
-- Two choices that differ from a naive version:
-- 1. "Came back" = is_returning_customer (orders on 2+ different days). A checkout split
--    into two orders at the same second is not a return visit.
-- 2. Only first orders from Jan 2017 to May 2018, so everyone had at least 3 months to
--    return before the data ends (68% of returns happen within 90 days, query 15).

with ranked_orders as (
    select
        *,
        row_number() over (partition by customer_unique_id order by purchased_at, order_id) as order_number
    from marts.fct_orders
    where is_valid_order
),

first_orders as (
    select * from ranked_orders
    where order_number = 1
      and order_date between date '2017-01-01' and date '2018-05-31'
),

customers as (
    select customer_unique_id, is_returning_customer
    from marts.dim_customers
)

select
    case
        when f.review_score is null then 'no review'
        when f.review_score <= 2   then '1-2 stars'
        when f.review_score = 3    then '3 stars'
        else '4-5 stars'
    end                                                          as first_order_review,
    case when f.is_late then 'late' else 'on time / not delivered' end as first_order_delivery,
    count(*)                                                     as customers,
    round(100.0 * avg(case when c.is_returning_customer then 1 else 0 end), 2) as returning_pct
from first_orders f
join customers c using (customer_unique_id)
group by 1, 2
order by 1, 2;

-- Same population, one factor at a time: delivery on its own.
with first_orders as (
    select *
    from marts.fct_orders
    where is_valid_order
    qualify row_number() over (partition by customer_unique_id order by purchased_at, order_id) = 1
)
select
    case when f.is_late then 'late' else 'on time / not delivered' end as first_order_delivery,
    count(*)                                                           as customers,
    round(100.0 * avg(case when c.is_returning_customer then 1 else 0 end), 2) as returning_pct
from first_orders f
join marts.dim_customers c using (customer_unique_id)
where f.order_date between date '2017-01-01' and date '2018-05-31'
group by 1
order by 1;

-- Returning rate by the category of the first order (categories with 1,000+ customers).
with first_orders as (
    select *
    from marts.fct_orders
    where is_valid_order
    qualify row_number() over (partition by customer_unique_id order by purchased_at, order_id) = 1
),
first_category as (
    -- an order can hold several products; use the category of its most expensive item
    select i.order_id, arg_max(p.category_name, i.price) as category_name
    from marts.fct_order_items i
    join marts.dim_products p using (product_id)
    group by 1
)
select
    fc.category_name,
    count(*)                                                                    as customers,
    round(100.0 * avg(case when c.is_returning_customer then 1 else 0 end), 2)  as returning_pct
from first_orders f
join first_category fc using (order_id)
join marts.dim_customers c using (customer_unique_id)
where f.order_date between date '2017-01-01' and date '2018-05-31'
group by 1
having count(*) >= 1000
order by returning_pct desc;

-- Returning rate by customer state (states with 1,000+ customers).
with first_orders as (
    select *
    from marts.fct_orders
    where is_valid_order
    qualify row_number() over (partition by customer_unique_id order by purchased_at, order_id) = 1
)
select
    f.customer_state,
    count(*)                                                                    as customers,
    round(100.0 * avg(case when c.is_returning_customer then 1 else 0 end), 2)  as returning_pct
from first_orders f
join marts.dim_customers c using (customer_unique_id)
where f.order_date between date '2017-01-01' and date '2018-05-31'
group by 1
having count(*) >= 1000
order by returning_pct desc;

-- Returning rate by payment type and installments of the first order.
with first_orders as (
    select *
    from marts.fct_orders
    where is_valid_order
    qualify row_number() over (partition by customer_unique_id order by purchased_at, order_id) = 1
)
select
    f.main_payment_type,
    case when f.max_installments <= 1 then 'single payment' else 'installments' end as installments,
    count(*)                                                                    as customers,
    round(100.0 * avg(case when c.is_returning_customer then 1 else 0 end), 2)  as returning_pct
from first_orders f
join marts.dim_customers c using (customer_unique_id)
where f.order_date between date '2017-01-01' and date '2018-05-31'
  and f.main_payment_type is not null
group by 1, 2
having count(*) >= 500
order by returning_pct desc;
