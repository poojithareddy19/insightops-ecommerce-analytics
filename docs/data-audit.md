# Data Audit: Olist E-commerce Dataset

Date: 2026-10-10
Tables audited: 9 Olist tables + BRL/USD rates (Frankfurter API)
Orders cover 2016-09-04 to 2018-10-17.

## Summary
The data is usable for analysis after handling 15 issues. The most important is
that customer_id identifies an order, not a person: there are 99,441 customer_ids
but only 96,096 real customers.

## Issues found

| # | Issue | Evidence (my numbers) | Impact | Decision |
|---|---|---|---|---|
| 1 | customer_id is per order, not per person | 99,441 customer_ids vs 96,096 customer_unique_ids | Retention and customer counts would be wrong | Use customer_unique_id for all customer metrics |
| 2 | Some orders have more than one review | 547 orders with 2+ reviews (up to 3) | Averages would double-count | Keep the latest review per order (stg_order_reviews) |
| 3 | review_id is not unique | 789 review_ids appear on 2+ orders | review_id cannot be a primary key | Use order_id as the key in the review model |
| 4 | Orders with no items | 775 orders: 603 unavailable, 164 canceled, 8 other | Revenue would be 0 for these | Keep; they get order_value 0 and are almost all excluded as invalid orders anyway |
| 5 | Order with no payment | 1 order | Payment analysis misses it | Keep; payment_value is null for it |
| 6 | Missing delivery dates | 2,965 orders. Expected for shipped/canceled/unavailable etc., but 8 "delivered" orders also have no date | Delivery time can't be computed | Delivery metrics only use delivered orders with a date (is_delivered) |
| 7 | Missing approval dates | 160 orders, 14 of them "delivered" | Minor; we don't use approval time in any metric | Keep, document |
| 8 | Thin months at start and end | Sep 2016: 4, Oct 2016: 324, Nov 2016: 0, Dec 2016: 1, Sep 2018: 16, Oct 2018: 4 | Trend charts would show fake drops | Trends use Jan 2017 to Aug 2018 only |
| 9 | Products with no category | 610 products (1.85%), which also have no name/description length or photo count | Category charts miss them | Label as 'unknown' |
| 10 | Categories with no English translation | 2: pc_gamer, portateis_cozinha_e_preparadores_de_alimentos | Mixed languages in charts | Fall back to the Portuguese name |
| 11 | Geolocation has many rows per zip | 1,000,163 rows for 19,015 zip prefixes | Joins would multiply rows | Average to one row per zip prefix |
| 12 | Zip prefixes missing from geolocation | 278 customers and 7 sellers have a zip prefix with no coordinates | Map points missing for a few | Keep; latitude/longitude null |
| 13 | Odd payments | 3 payments of type 'not_defined' (all 0 value); 9 zero-value payments in total (6 voucher) | Small; could confuse payment analysis | Keep, document, exclude from payment-type charts |
| 14 | Column name typos | product_name_lenght, product_description_lenght | Confusing | Rename in staging |
| 15 | Zip codes lose leading zeros if read as numbers | e.g. 01310 becomes 1310 | Broken joins | Load raw as text (all 5-character prefixes survived); pad to 5 digits in staging as a safeguard |

Text columns that are mostly empty and that's fine: review_comment_title (88.3% null)
and review_comment_message (58.7% null). Customers leave a score without a comment.

## Checks I ran
See analyses/00_data_quality_checks.sql and docs/profile_raw.md.
