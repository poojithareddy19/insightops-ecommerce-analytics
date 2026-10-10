-- Author: Gorla Poojitha
-- Raw geolocation has many rows per zip code prefix.
-- We collapse it to ONE row per zip prefix (average coordinates, most common city/state).

with source as (
    select * from {{ source('olist', 'geolocation') }}
)

select
    lpad(geolocation_zip_code_prefix, 5, '0') as zip_code_prefix,
    avg(cast(geolocation_lat as double))      as latitude,
    avg(cast(geolocation_lng as double))      as longitude,
    mode(lower(trim(geolocation_city)))       as city,
    mode(upper(trim(geolocation_state)))      as state
from source
group by 1
