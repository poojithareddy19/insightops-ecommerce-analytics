# Metric Catalog

All metrics are calculated from the dbt marts. Currency is BRL unless stated.

## Revenue
- **Definition:** Sum of item price + freight for valid orders.
- **Formula:** SUM(fct_orders.order_value) WHERE is_valid_order
- **Valid order:** order_status NOT IN ('canceled', 'unavailable')
- **Why not payment_value?** Payments include installment interest, which is not
  sales revenue. (See data audit, payment mismatch warning.)
- **Date:** attributed to the purchase date (order_date), not the delivery date.

## Orders
- **Definition:** Count of distinct valid orders.
- **Formula:** COUNT(DISTINCT order_id) WHERE is_valid_order

## Average Order Value (AOV)
- **Definition:** Revenue / Orders.
- **Note:** Order values are right-skewed; also report the median order value.

## Customer
- **Definition:** A distinct customer_unique_id. NEVER count customer_id
  (it is created per order).

## Active customer (month)
- **Definition:** A customer with at least 1 valid order in that calendar month.

## Repeat customer
- **Definition:** A customer with 2 or more valid orders in the whole dataset.

## Retention (month N)
- **Definition:** Of customers whose first valid order was in month M (their cohort),
  the % who placed a valid order in month M + N.

## Delivery time
- **Definition:** Days from purchase to delivery to the customer.
- **Population:** delivered orders with a delivery date only.
- **Reported as:** median (mean is pulled up by a few very long deliveries).

## Late delivery rate
- **Definition:** Delivered orders where the delivery date is after the estimated
  delivery date, divided by all delivered orders.

## Review score
- **Definition:** Average of review_score (1 to 5), latest review per order.

## Trend window
- **Definition:** Monthly trend charts and month-over-month numbers use January 2017
  to August 2018 only. The months before and after are incomplete (see data audit, issue 8).
