-- Export the cohort retention table in "long" format for the Looker Studio heatmap.
-- Run from the project root AFTER scripts/export_marts.py (which creates data/exports/).
-- Only complete cohorts (Jan 2017 to Aug 2018) are included.

COPY (
    with valid_orders as (
        select customer_unique_id, date_trunc('month', purchased_at) as order_month
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
    )
    select
        cast(a.cohort_month as date) as cohort_month,
        a.months_since_first,
        a.active_customers,
        s.active_customers           as cohort_size,
        round(100.0 * a.active_customers / s.active_customers, 2) as retention_pct
    from activity a
    join activity s
      on a.cohort_month = s.cohort_month and s.months_since_first = 0
    where a.months_since_first between 1 and 12
      and a.cohort_month between date '2017-01-01' and date '2018-08-01'
    order by 1, 2
) TO 'data/exports/cohort_retention.csv' (HEADER, DELIMITER ',');
