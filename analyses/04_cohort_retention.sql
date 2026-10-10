-- Author: Gorla Poojitha
-- Business question: Of the customers who first bought in month X,
-- what % came back 1, 2, 3, 6 and 12 months later?
-- Techniques: cohort analysis, date_diff, conditional aggregation (pivot with CASE).

with valid_orders as (
    select
        customer_unique_id,
        date_trunc('month', purchased_at) as order_month
    from marts.fct_orders
    where is_valid_order
),

cohorts as (
    select customer_unique_id, min(order_month) as cohort_month
    from valid_orders
    group by 1
),

activity as (
    select
        c.cohort_month,
        date_diff('month', c.cohort_month, v.order_month) as months_since_first,
        count(distinct v.customer_unique_id)              as active_customers
    from valid_orders v
    join cohorts c using (customer_unique_id)
    group by 1, 2
),

pivoted as (
    select
        cohort_month,
        max(case when months_since_first = 0  then active_customers end) as cohort_size,
        max(case when months_since_first = 1  then active_customers end) as m1,
        max(case when months_since_first = 2  then active_customers end) as m2,
        max(case when months_since_first = 3  then active_customers end) as m3,
        max(case when months_since_first = 6  then active_customers end) as m6,
        max(case when months_since_first = 12 then active_customers end) as m12
    from activity
    group by 1
)

select
    cohort_month,
    cohort_size,
    round(100.0 * coalesce(m1, 0)  / cohort_size, 2) as m1_pct,
    round(100.0 * coalesce(m2, 0)  / cohort_size, 2) as m2_pct,
    round(100.0 * coalesce(m3, 0)  / cohort_size, 2) as m3_pct,
    round(100.0 * coalesce(m6, 0)  / cohort_size, 2) as m6_pct,
    round(100.0 * coalesce(m12, 0) / cohort_size, 2) as m12_pct
from pivoted
order by cohort_month;
