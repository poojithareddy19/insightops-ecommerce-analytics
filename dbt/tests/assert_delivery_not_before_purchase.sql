-- A singular test: dbt FAILS this test if the query returns any rows.
-- An order cannot be delivered before it was purchased.
{{ config(severity = 'warn') }}

select order_id, purchased_at, delivered_to_customer_at
from {{ ref('fct_orders') }}
where delivered_to_customer_at < purchased_at
