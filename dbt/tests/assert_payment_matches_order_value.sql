-- Payments should roughly equal items + freight.
-- Differences can come from installment interest, so this only WARNS.
-- The number of rows it returns goes into docs/data-audit.md.
{{ config(severity = 'warn') }}

select order_id, order_value, payment_value
from {{ ref('fct_orders') }}
where payment_value is not null
  and abs(order_value - payment_value) > 1.00
