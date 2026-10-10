-- Grain: ONE ROW PER PRODUCT, with the English category name.

with products as (
    select * from {{ ref('stg_products') }}
),

translation as (
    select * from {{ ref('stg_category_translation') }}
)

select
    p.product_id,
    p.product_category_name                         as category_name_pt,
    coalesce(
        t.product_category_name_english,  -- English name when we have one
        p.product_category_name,          -- otherwise keep the Portuguese name
        'unknown'                         -- product has no category at all
    )                                               as category_name,
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm,
    p.product_photos_qty
from products p
left join translation t on p.product_category_name = t.product_category_name
