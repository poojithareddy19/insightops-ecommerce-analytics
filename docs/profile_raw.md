# Raw data profile

*Gorla Poojitha*

## raw.brl_usd_rates (2,610 rows)

| column | nulls | null % | distinct values |
|---|---|---|---|
| rate_date | 0 | 0.00% | 2,610 |
| brl_to_usd | 0 | 0.00% | 2,227 |

## raw.category_translation (71 rows)

| column | nulls | null % | distinct values |
|---|---|---|---|
| product_category_name | 0 | 0.00% | 71 |
| product_category_name_english | 0 | 0.00% | 71 |

## raw.customers (99,441 rows)

| column | nulls | null % | distinct values |
|---|---|---|---|
| customer_id | 0 | 0.00% | 99,441 |
| customer_unique_id | 0 | 0.00% | 96,096 |
| customer_zip_code_prefix | 0 | 0.00% | 14,994 |
| customer_city | 0 | 0.00% | 4,119 |
| customer_state | 0 | 0.00% | 27 |

## raw.geolocation (1,000,163 rows)

| column | nulls | null % | distinct values |
|---|---|---|---|
| geolocation_zip_code_prefix | 0 | 0.00% | 19,015 |
| geolocation_lat | 0 | 0.00% | 717,372 |
| geolocation_lng | 0 | 0.00% | 717,615 |
| geolocation_city | 0 | 0.00% | 8,011 |
| geolocation_state | 0 | 0.00% | 27 |

## raw.order_items (112,650 rows)

| column | nulls | null % | distinct values |
|---|---|---|---|
| order_id | 0 | 0.00% | 98,666 |
| order_item_id | 0 | 0.00% | 21 |
| product_id | 0 | 0.00% | 32,951 |
| seller_id | 0 | 0.00% | 3,095 |
| shipping_limit_date | 0 | 0.00% | 93,318 |
| price | 0 | 0.00% | 5,968 |
| freight_value | 0 | 0.00% | 6,999 |

## raw.order_payments (103,886 rows)

| column | nulls | null % | distinct values |
|---|---|---|---|
| order_id | 0 | 0.00% | 99,440 |
| payment_sequential | 0 | 0.00% | 29 |
| payment_type | 0 | 0.00% | 5 |
| payment_installments | 0 | 0.00% | 24 |
| payment_value | 0 | 0.00% | 29,077 |

## raw.order_reviews (99,224 rows)

| column | nulls | null % | distinct values |
|---|---|---|---|
| review_id | 0 | 0.00% | 98,410 |
| order_id | 0 | 0.00% | 98,673 |
| review_score | 0 | 0.00% | 5 |
| review_comment_title | 87,656 | 88.34% | 4,527 |
| review_comment_message | 58,247 | 58.70% | 36,159 |
| review_creation_date | 0 | 0.00% | 636 |
| review_answer_timestamp | 0 | 0.00% | 98,248 |

## raw.orders (99,441 rows)

| column | nulls | null % | distinct values |
|---|---|---|---|
| order_id | 0 | 0.00% | 99,441 |
| customer_id | 0 | 0.00% | 99,441 |
| order_status | 0 | 0.00% | 8 |
| order_purchase_timestamp | 0 | 0.00% | 98,875 |
| order_approved_at | 160 | 0.16% | 90,733 |
| order_delivered_carrier_date | 1,783 | 1.79% | 81,018 |
| order_delivered_customer_date | 2,965 | 2.98% | 95,664 |
| order_estimated_delivery_date | 0 | 0.00% | 459 |

## raw.products (32,951 rows)

| column | nulls | null % | distinct values |
|---|---|---|---|
| product_id | 0 | 0.00% | 32,951 |
| product_category_name | 610 | 1.85% | 73 |
| product_name_lenght | 610 | 1.85% | 66 |
| product_description_lenght | 610 | 1.85% | 2,960 |
| product_photos_qty | 610 | 1.85% | 19 |
| product_weight_g | 2 | 0.01% | 2,204 |
| product_length_cm | 2 | 0.01% | 99 |
| product_height_cm | 2 | 0.01% | 102 |
| product_width_cm | 2 | 0.01% | 95 |

## raw.sellers (3,095 rows)

| column | nulls | null % | distinct values |
|---|---|---|---|
| seller_id | 0 | 0.00% | 3,095 |
| seller_zip_code_prefix | 0 | 0.00% | 2,246 |
| seller_city | 0 | 0.00% | 611 |
| seller_state | 0 | 0.00% | 23 |
