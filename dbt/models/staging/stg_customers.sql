-- One row per customer_id.
-- WARNING: customer_id is created per ORDER in Olist.
-- The real person is customer_unique_id. Always use customer_unique_id for retention.

with source as (
    select * from {{ source('olist', 'customers') }}
)

select
    customer_id,
    customer_unique_id,
    lpad(customer_zip_code_prefix, 5, '0') as customer_zip_code_prefix,
    lower(trim(customer_city))            as customer_city,
    upper(trim(customer_state))           as customer_state
from source
