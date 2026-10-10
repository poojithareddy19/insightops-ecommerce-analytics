-- Phase 1 data quality checks on the RAW tables.
-- Run one block at a time and write every surprising number into docs/data-audit.md.

-- CHECK 1: Real customers vs customer_id. If these differ, customer_id is NOT a person.
select
    count(distinct customer_id)        as customer_ids,
    count(distinct customer_unique_id) as real_customers
from raw.customers;

-- CHECK 2: Duplicate keys. Any row returned = a key that appears more than once.
select 'orders.order_id' as key_checked, order_id as key_value, count(*) as copies
from raw.orders group by order_id having count(*) > 1
union all
select 'order_reviews.review_id', review_id, count(*)
from raw.order_reviews group by review_id having count(*) > 1
union all
select 'order_reviews.order_id', order_id, count(*)
from raw.order_reviews group by order_id having count(*) > 1
order by copies desc
limit 20;

-- CHECK 3: Orphans. Orders that have no items, and orders that have no payment.
select
    (select count(*) from raw.orders o
      where not exists (select 1 from raw.order_items i where i.order_id = o.order_id))    as orders_without_items,
    (select count(*) from raw.orders o
      where not exists (select 1 from raw.order_payments p where p.order_id = o.order_id)) as orders_without_payments;

-- CHECK 4: Order statuses and missing delivery dates per status.
select
    order_status,
    count(*)                                                   as orders,
    count(*) filter (where order_delivered_customer_date is null) as missing_delivery_date,
    count(*) filter (where order_approved_at is null)          as missing_approval_date
from raw.orders
group by 1
order by orders desc;

-- CHECK 5: Date range and orders per month (look for thin months at the start and end).
select
    date_trunc('month', cast(order_purchase_timestamp as timestamp)) as order_month,
    count(*) as orders
from raw.orders
group by 1
order by 1;

-- CHECK 6: Products with no category, and categories with no English translation.
select
    count(*) filter (where p.product_category_name is null)                         as products_without_category,
    count(distinct p.product_category_name) filter (
        where p.product_category_name is not null
          and t.product_category_name is null)                                      as categories_without_translation
from raw.products p
left join raw.category_translation t on p.product_category_name = t.product_category_name;

-- CHECK 7: Strange payments.
select payment_type, count(*) as payments,
       count(*) filter (where cast(payment_value as double) = 0) as zero_value_payments
from raw.order_payments
group by 1
order by 2 desc;

-- CHECK 8: Geolocation duplicates per zip code prefix.
select
    count(*)                                     as geo_rows,
    count(distinct geolocation_zip_code_prefix)  as distinct_zip_prefixes
from raw.geolocation;
