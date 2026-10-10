-- Business question: How can we group customers by Recency, Frequency and Monetary value?
-- Technique: NTILE(5) splits customers into 5 equal-sized buckets (scores 1 to 5).

with snapshot as (
    -- "today" for this dataset = the day after the last order
    select max(purchased_at) + interval 1 day as as_of from marts.fct_orders
),

customer_stats as (
    select
        customer_unique_id,
        date_diff('day', max(purchased_at), (select as_of from snapshot)) as recency_days,
        count(*)                                                          as frequency,
        sum(order_value)                                                  as monetary
    from marts.fct_orders
    where is_valid_order
    group by 1
),

scored as (
    select
        *,
        ntile(5) over (order by recency_days desc) as r_score,  -- recent buyers get 5
        ntile(5) over (order by frequency)         as f_score,
        ntile(5) over (order by monetary)          as m_score
    from customer_stats
),

segmented as (
    select
        *,
        case
            when r_score >= 4 and frequency >= 2 then 'Loyal'
            when r_score >= 4 and m_score >= 4   then 'Recent big spender'
            when r_score >= 4                    then 'New / recent'
            when r_score <= 2 and m_score >= 4   then 'At risk, high value'
            when r_score <= 2                    then 'Lost'
            else 'Needs attention'
        end as segment
    from scored
)

select
    segment,
    count(*)                                  as customers,
    round(100.0 * count(*) / sum(count(*)) over (), 1) as pct_customers,
    round(avg(recency_days), 0)               as avg_recency_days,
    round(avg(frequency), 2)                  as avg_orders,
    round(sum(monetary), 0)                   as revenue,
    round(100.0 * sum(monetary) / sum(sum(monetary)) over (), 1) as pct_revenue
from segmented
group by segment
order by revenue desc;
