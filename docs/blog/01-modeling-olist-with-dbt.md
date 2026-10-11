# Modeling a messy 9-table e-commerce dataset with dbt

*Gorla Poojitha*

The Olist dataset on Kaggle is a real Brazilian marketplace: about 100,000 orders from
2016 to 2018, spread across nine CSV files. Customers, orders, items, payments, reviews,
products, sellers, a category translation table and a million rows of geolocation.

It looks tidy. It isn't. This post is about turning those nine files into a warehouse I
could trust, using DuckDB and dbt, and about the problems that only showed up because I
went looking for them.

## The trap in the customers table

The first thing I checked was the simplest: how many customers are there?

`customer_id` has 99,441 distinct values. `customer_unique_id` has 96,096.

That gap is the whole story. Olist creates a new `customer_id` for every order, so it
identifies an order, not a person. If you count customers with `customer_id`, almost
everyone looks like a one-time buyer by construction, and every retention number you
produce is wrong before you've written a single interesting query.

It's an easy mistake because the column is literally named "customer id". So the rule
went into the metric catalog on day one: a customer is a `customer_unique_id`, never a
`customer_id`.

## Load raw, and don't touch it

Before any modeling, I loaded every file into a `raw` schema in DuckDB with two rules:

- **Every column is text.** Zip code prefixes like `01310` lose their leading zero if a
  loader decides they're numbers, and then joins silently fail. Types get fixed later,
  in dbt, where the conversion is visible and tested.
- **Every load replaces the table.** Running the loader twice gives the same row counts,
  not double. That property (idempotency) means I never have to wonder whether the
  warehouse is in a half-loaded state.

Then I profiled every column and ran targeted checks for duplicate keys, orphans and odd
values. The audit ended up with 15 issues. A few that shaped the models:

- 547 orders have more than one review, and 789 `review_id`s appear on more than one
  order. So `review_id` can't be a key.
- Geolocation has 1,000,163 rows for only 19,015 zip prefixes. Join to it naively and you
  multiply rows.
- 610 products have no category, and two categories have no English translation.
- 775 orders have no items at all, almost all canceled or unavailable.

Every one of these got a written decision: drop, fix, flag or keep.

## Raw, staging, marts

The dbt project has three layers.

**Staging** is one view per source table, and its job is boring on purpose: rename,
cast types, and fix the issues from the audit. `stg_order_reviews` keeps the latest
review per order with `ROW_NUMBER()`. `stg_geolocation` collapses to one row per zip
prefix. `stg_products` fixes the source's misspelled `product_name_lenght` columns.

**Marts** are tables built for analysis, in a star schema. `fct_orders` has one row per
order with revenue, delivery times, the review score and a late flag already computed.
`dim_customers` has one row per real person. There are also fact tables for items and
payments, and dimensions for products, sellers and dates.

Exchange rates were a nice small problem. I pulled daily BRL to USD rates from the
Frankfurter API, but rates only exist on business days. An `ASOF JOIN` attaches the most
recent earlier rate to each order, so a Saturday order gets Friday's rate.

The result: 17 models. A question like "revenue by month" went from a four-table join to
a single-table query.

![dbt lineage](../../dashboards/dbt_lineage.png)

## What the tests caught

The project has 49 data tests: `unique` and `not_null` on every key, `relationships` to
catch orphans, `accepted_values` on statuses and payment types, and two custom tests.

`dbt build` finishes with PASS=65, WARN=1, ERROR=0. The warning turned out to be the most
interesting thing in the project.

The test checks that what customers paid roughly matches item prices plus freight. 1,021
orders don't match. The guide I was following said to expect this, because installment
plans add interest. I almost wrote that down and moved on.

Instead I split the 1,021 orders:

- **772** were orders with no items at all. Payment was taken, nothing shipped. They're
  almost all canceled or unavailable.
- **232** paid more than items plus freight, and 229 of those were on installment plans,
  with a median overpayment around 10%. That's the interest.
- **17** paid less, for no reason I could find.

Interest was real, but it was the minority. The obvious explanation would have gone into
the audit unchecked. The warning stays, documented, and revenue is defined from items
plus freight, so neither group distorts it.

## The bug no test caught

The second surprise came later, during analysis. One query said 2,638 customers ordered
again. `dim_customers` said 2,888 customers had two or more orders. Same data, two answers.

The difference was 250 customers with two orders at the exact same second. That's not a
customer coming back; it's one checkout split into two orders, probably because the basket
had items from different sellers. Counting orders treats it as a repeat purchase.

I added an `is_returning_customer` flag (valid orders on two or more different days) and
made it the headline metric. The repeat rate went from 3.0% to 2.2%.

No dbt test caught this, because nothing was technically wrong. Both numbers were valid
answers to slightly different questions. What caught it was computing the same thing two
ways and refusing to move on until they agreed.

## What I'd do differently

- **Test the definitions, not just the keys.** A singular test that reconciles "customers
  with a later order" against "customers with 2+ orders" would have flagged the split
  checkouts at build time instead of during analysis.
- **Write the metric catalog before the marts.** I wrote it after, and the "customer" and
  "revenue" definitions ended up driving changes back into the models anyway.
- **Check where data comes from, byte by byte.** Much later, adding a header line to the raw
  files, I found that two Olist files use Windows line endings and one starts with an
  invisible byte order mark. Small things, but they break CSV parsers in confusing ways.

The code, the data audit and the metric catalog are all in the repo:
[github.com/poojithareddy19/insightops-ecommerce-analytics](https://github.com/poojithareddy19/insightops-ecommerce-analytics).
