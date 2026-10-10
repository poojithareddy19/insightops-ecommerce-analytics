-- Author: Gorla Poojitha
-- Business question: How many orders had more than one review, and which one do we keep?
-- Technique: ROW_NUMBER() to deduplicate (the most common live SQL interview question).

with ranked as (
    select
        order_id,
        review_id,
        review_score,
        review_answer_timestamp,
        row_number() over (
            partition by order_id
            order by review_answer_timestamp desc
        ) as row_num
    from raw.order_reviews
)

select
    count(distinct order_id)                       as orders_with_reviews,
    count(*) filter (where row_num > 1)            as duplicate_rows_removed,
    count(distinct order_id) filter (where row_num = 2) as orders_with_multiple_reviews
from ranked;
