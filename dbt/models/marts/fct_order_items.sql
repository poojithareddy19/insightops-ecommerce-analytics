-- Author: Gorla Poojitha
-- Grain: ONE ROW PER ITEM IN AN ORDER. Use for product, category and seller analysis.

with items as (
    select * from {{ ref('stg_order_items') }}
),

orders as (
    select order_id, customer_unique_id, order_date, order_status, is_valid_order
    from {{ ref('fct_orders') }}
)

select
    i.order_item_key,
    i.order_id,
    i.order_item_number,
    i.product_id,
    i.seller_id,
    o.customer_unique_id,
    o.order_date,
    o.order_status,
    o.is_valid_order,
    i.price,
    i.freight_value,
    i.price + i.freight_value as item_total
from items i
left join orders o on i.order_id = o.order_id
