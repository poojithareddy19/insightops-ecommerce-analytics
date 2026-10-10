-- One row per ORDER (deduplicated).
-- Raw data issue: some orders have more than one review.
-- Rule (documented in docs/data-audit.md): keep the most recently answered review.

with source as (
    select * from {{ source('olist', 'order_reviews') }}
),

renamed as (
    select
        review_id,
        order_id,
        cast(review_score as integer)              as review_score,
        review_comment_title,
        review_comment_message,
        cast(review_creation_date    as timestamp) as review_created_at,
        cast(review_answer_timestamp as timestamp) as review_answered_at
    from source
),

ranked as (
    select
        *,
        row_number() over (
            partition by order_id
            order by review_answered_at desc, review_id
        ) as row_num
    from renamed
)

select * exclude (row_num)
from ranked
where row_num = 1
