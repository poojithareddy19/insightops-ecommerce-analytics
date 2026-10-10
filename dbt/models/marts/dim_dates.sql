-- Author: Gorla Poojitha
-- Grain: ONE ROW PER CALENDAR DAY. A calendar table makes date filtering easy.

with days as (
    select cast(unnest(generate_series(date '2016-01-01', date '2018-12-31', interval 1 day)) as date) as date_day
)

select
    date_day,
    year(date_day)                          as year,
    quarter(date_day)                       as quarter,
    month(date_day)                         as month,
    monthname(date_day)                     as month_name,
    cast(date_trunc('month', date_day) as date) as month_start,
    dayofweek(date_day)                     as day_of_week,   -- 0 = Sunday
    dayname(date_day)                       as day_name,
    dayofweek(date_day) in (0, 6)           as is_weekend
from days
