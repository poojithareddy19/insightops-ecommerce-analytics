-- Author: Gorla Poojitha
-- One row per payment. An order can be paid in several parts (e.g. voucher + card).

with source as (
    select * from {{ source('olist', 'order_payments') }}
)

select
    order_id || '-' || payment_sequential     as payment_key,
    order_id,
    cast(payment_sequential   as integer)     as payment_sequence,
    payment_type,
    cast(payment_installments as integer)     as payment_installments,
    cast(payment_value as decimal(10, 2))     as payment_value
from source
