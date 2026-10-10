# Insights, Part 1: What the Olist Data Says

*Gorla Poojitha*

**Bottom line:** Olist is almost entirely a first-purchase business. Only about 2 in
100 customers ever come back, so growing repeat purchases is the largest untapped
opportunity. Late delivery is the clearest thing standing in the way.

Scope: 98,207 valid orders, R$15.74M revenue (about US$4.69M at daily rates),
94,990 customers with at least one valid order, Sep 2016 to Aug 2018.

## Findings

1. **Almost nobody comes back.** 97.2% of customers never place a later order
   (query 03). Counting only customers who returned on a different day, the repeat
   rate is 2.2% (2,065 of 94,990). The naive "2+ orders" count says 3.0%, but 250 of
   those are one checkout split into two orders at the same second.
   *So what:* the business pays to acquire nearly every order from scratch.

2. **When customers do come back, they come back fast.** Of second orders, 30% are
   placed the same day, the median gap is 28 days, and 68% happen within 90 days
   (query 15). *So what:* a "come back" offer belongs in the first month, not
   after six.

3. **Revenue is concentrated, but in big baskets, not loyal customers.** The top 10%
   of customers generate 38.3% of revenue and the top 20% generate 53.6% (query 09).
   Since almost everyone buys once, these are people who placed one large order.
   *So what:* "protect your best customers" means protecting high-value first orders.

4. **Late deliveries wreck reviews.** Orders delivered 7+ days late average 1.70 stars
   and 79% get 1 or 2 stars. On-time orders average 4.17 and orders arriving 7+ days
   early average 4.31 (query 06). *So what:* delivery reliability is a lever for
   reputation; Phase 4 tests whether the gap is real.

5. **The worst sellers by late rate are not where most lateness lives.** The 20 worst
   sellers (20+ delivered orders) have late rates of 20% to 33% against 6.8% overall
   (query 10), but together they cause only 200 of 6,534 late orders (3%). The 10% of
   sellers with the most late orders cause 74% of them.
   *So what:* seller SLAs should target late-order volume, not late-order rate.

6. **The North and Northeast wait about three times as long.** Median delivery is 7 days in SP but
   26 in AM and 22 in AL; AL has a 21.4% late rate and MA 17.4%, against 4.5% in SP
   (query 13). *So what:* the delivery promise already allows for distance, and it is still
   missed 3 to 5 times as often in these states.

7. **Growth was real, then flattened.** January to August 2018 revenue was R$8.59M,
   up 140% on the same months of 2017 (R$3.57M), but monthly revenue has been flat at
   about R$1.0M to R$1.16M since January 2018 (query 01). *So what:* acquisition-led
   growth has stalled, which makes retention more urgent.

8. **The typical order is smaller than the average suggests.** AOV is R$160.23 but the
   median order is R$105.28. Big orders get paid in more installments: median R$72 on
   a single payment vs R$238 on 10+ installments (query 16). About 75% of orders are
   paid mainly by credit card, steady across years (query 08).

9. **Category growth is broad.** health_beauty (9.3% of item revenue), watches_gifts
   (8.9%) and bed_bath_table (7.7%) lead (query 02). Among sizeable categories, baby
   (+264%), watches_gifts (+243%) and health_beauty (+211%) grew fastest from Jan-Aug
   2017 to Jan-Aug 2018 (query 14).

10. **Standard RFM doesn't fit this data.** With 97% single-order customers, the
    frequency score separates almost nobody; the "Loyal" segment is 1.3% of customers
    and 2.5% of revenue (query 05). Recency and monetary value do the real work.

## Caveats
- 2016 and Sep/Oct 2018 are incomplete and excluded from trends.
- These are correlations; they do not prove cause (see Phase 4).
- Customers from mid-2018 had little time to come back before the data ends, so the
  repeat rate is a slight underestimate for recent cohorts.
