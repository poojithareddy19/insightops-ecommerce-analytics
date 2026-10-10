-- Business question: Do late deliveries get worse review scores?
-- Techniques: CASE buckets, aggregation, comparing groups.

select
    case
        when delivery_days - date_diff('day', purchased_at, estimated_delivery_at) <= -7 then '1. 7+ days early'
        when not is_late                                                                then '2. on time'
        when delivery_days - date_diff('day', purchased_at, estimated_delivery_at) <= 7  then '3. late 1-7 days'
        else '4. late 7+ days'
    end                                             as delivery_bucket,
    count(*)                                        as orders,
    round(avg(review_score), 2)                     as avg_review,
    round(100.0 * avg(case when review_score <= 2 then 1 else 0 end), 1) as pct_1_or_2_stars
from marts.fct_orders
where is_delivered
  and review_score is not null
group by 1
order by 1;
