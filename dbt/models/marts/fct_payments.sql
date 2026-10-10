-- Author: Gorla Poojitha
-- Grain: ONE ROW PER PAYMENT PART.

with payments as (
    select * from {{ ref('stg_order_payments') }}
),

orders as (
    select order_id, order_date, is_valid_order
    from {{ ref('fct_orders') }}
)

select
    p.payment_key,
    p.order_id,
    o.order_date,
    o.is_valid_order,
    p.payment_sequence,
    p.payment_type,
    p.payment_installments,
    p.payment_value
from payments p
left join orders o on p.order_id = o.order_id
