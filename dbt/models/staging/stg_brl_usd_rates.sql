-- Author: Gorla Poojitha
-- Daily BRL to USD rates collected by ingestion/fetch_rates.py (business days only).

with source as (
    select * from {{ source('olist', 'brl_usd_rates') }}
)

select
    cast(rate_date  as date)   as rate_date,
    cast(brl_to_usd as double) as brl_to_usd
from source
