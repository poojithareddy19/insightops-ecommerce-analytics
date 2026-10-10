-- Author: Gorla Poojitha
-- Grain: ONE ROW PER SELLER, with approximate coordinates.

with sellers as (
    select * from {{ ref('stg_sellers') }}
),

geo as (
    select * from {{ ref('stg_geolocation') }}
)

select
    s.seller_id,
    s.seller_city,
    s.seller_state,
    s.seller_zip_code_prefix,
    g.latitude,
    g.longitude
from sellers s
left join geo g on s.seller_zip_code_prefix = g.zip_code_prefix
