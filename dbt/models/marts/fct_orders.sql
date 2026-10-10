-- Grain: ONE ROW PER ORDER.
-- The main table for revenue, orders, AOV, delivery and review analysis.

with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select customer_id, customer_unique_id, customer_state
    from {{ ref('stg_customers') }}
),

items as (
    select
        order_id,
        count(*)                  as item_count,
        count(distinct seller_id) as seller_count,
        sum(price)                as items_value,
        sum(freight_value)        as freight_value
    from {{ ref('stg_order_items') }}
    group by order_id
),

payments as (
    select
        order_id,
        sum(payment_value)                      as payment_value,
        max(payment_installments)               as max_installments,
        arg_max(payment_type, payment_value)    as main_payment_type  -- type that paid the most
    from {{ ref('stg_order_payments') }}
    group by order_id
),

reviews as (
    select order_id, review_score
    from {{ ref('stg_order_reviews') }}
),

rates as (
    select * from {{ ref('stg_brl_usd_rates') }}
),

joined as (
    select
        o.order_id,
        c.customer_unique_id,
        o.customer_id,
        c.customer_state,
        'BR-' || c.customer_state                         as customer_state_iso,  -- for map charts
        o.order_status,
        o.purchased_at,
        cast(o.purchased_at as date)                       as order_date,
        o.approved_at,
        o.delivered_to_carrier_at,
        o.delivered_to_customer_at,
        o.estimated_delivery_at,
        coalesce(i.item_count, 0)                          as item_count,
        i.seller_count,
        coalesce(i.items_value, 0)                         as items_value,
        coalesce(i.freight_value, 0)                       as freight_value,
        coalesce(i.items_value, 0) + coalesce(i.freight_value, 0) as order_value,
        p.payment_value,
        p.main_payment_type,
        p.max_installments,
        r.review_score,
        o.order_status not in ('canceled', 'unavailable')  as is_valid_order,
        o.order_status = 'delivered'
            and o.delivered_to_customer_at is not null     as is_delivered,
        date_diff('day', o.purchased_at, o.delivered_to_customer_at) as delivery_days,
        case
            when o.delivered_to_customer_at is null then null
            when cast(o.delivered_to_customer_at as date) > cast(o.estimated_delivery_at as date) then true
            else false
        end                                                as is_late
    from orders o
    left join customers c on o.customer_id = c.customer_id
    left join items     i on o.order_id = i.order_id
    left join payments  p on o.order_id = p.order_id
    left join reviews   r on o.order_id = r.order_id
)

-- ASOF JOIN: rates only exist on business days, so for a weekend order
-- we take the most recent rate before that date.
select
    j.*,
    round(j.order_value * r.brl_to_usd, 2) as order_value_usd
from joined j
asof left join rates r
    on j.order_date >= r.rate_date
