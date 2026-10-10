# Growing Repeat Purchases at Olist

**To:** Head of Growth  |  **From:** InsightOps analytics  |  **Date:** 10 October 2026

## Bottom line
Only 2.2% of customers ever come back on a later day, and the first order matters:
customers whose first delivery was late return a third less often (1.74% vs 2.57%).
But repeat buying is so rare that fixing late first deliveries alone adds only about
R$4k to R$7k a year in repeat sales. The bigger lever is a first-month win-back program
for all new customers: an estimated **R$55k to R$110k a year** in extra sales, to be
proven with an A/B test before rollout.

## Context
Revenue grew 140% from Jan-Aug 2017 to Jan-Aug 2018 (R$3.57M to R$8.59M), but it has been
flat at about R$1.0M to R$1.16M a month since January 2018. Nearly every order comes from
a new customer, so when acquisition stalls, growth stalls. Retention is the untested
alternative.

## Findings
1. **Almost nobody comes back.** 2,065 of 94,990 customers (2.2%) placed orders on two or
   more different days. A naive "2+ orders" count says 3.0%, but 250 of those are one
   checkout split into two orders at the same second.
2. **A late first delivery cuts the return rate by a third.** Among 76,552 customers whose
   first order was between Jan 2017 and May 2018 (so all had at least 3 months to return):
   1.74% return after a late first delivery vs 2.57% otherwise. Difference 0.83 pp,
   95% CI [0.47, 1.19], p = 0.0001. The worst case, late and rated 1-2 stars, returns at
   1.48%; on time and rated 4-5 stars returns at 2.67%.
3. **Returns happen fast or not at all.** Of second orders, 51% come within 30 days and
   68% within 90 days (median 28 days).
4. **Some first categories bring people back more.** Customers whose first order was in
   fashion_bags_accessories (4.3%), bed_bath_table (3.4%), pet_shop (3.3%), furniture_decor
   (3.2%) or sports_leisure (3.1%) return more than those starting in electronics (1.7%) or
   cool_stuff (1.6%). Customers who paid mainly with a voucher return at 3.2%.
5. **Late deliveries hurt more than repeat sales.** 79% of orders delivered 7+ days late get
   1 or 2 stars (vs 11% of on-time orders), and the gap holds inside every large state.
   Those reviews are public and affect every future shopper, which this memo doesn't value.

## Recommendations
1. **Test a first-month win-back offer for every new customer.** Contact customers within
   30 days of their first delivery with a voucher for a complementary category.
   Expected impact: **R$55k to R$110k/year** in extra sales (appendix, B).
   It must be A/B tested: the free-shipping test showed that an offer can lift conversion
   and still lose money once its cost is counted.
2. **Run the pilot in the high-return categories first.** bed_bath_table, furniture_decor,
   sports_leisure, pet_shop and fashion_bags_accessories bring in about 14,900 new customers
   a year who already return at 3.1% to 4.3%. Detecting a +1 pp lift from 3.3% needs about
   5,700 customers per group, so a pilot fits in under a year of first orders from these
   categories alone; extending to all new customers gets there in a few months.
   Impact: included in recommendation 1; this is the cheaper way to prove it.
3. **Stop late first deliveries, starting in the North and Northeast.** Set realistic
   delivery promises where they are missed most (AL 21% late, MA 17%, vs 4.5% in SP) and
   in peak months (Feb-Mar 2018 reached 19% late). Expected impact on repeat sales:
   **R$4k to R$7k/year** (appendix, A). The main payoff is fewer 1-2 star reviews, which
   needs its own measurement.

## Risks and limitations
- Observational data: late first orders also differ by state, seller and category, so the
  0.83 pp gap may not be fully caused by lateness.
- Repeat value is measured inside a 2-year window; true lifetime value is likely higher,
  so the estimates lean conservative.
- Figures are sales (GMV, item price + freight), not Olist's commission, which is a fraction.
- The win-back lift (+0.5 to +1.0 pp) is an assumption until the A/B test runs.

## What data I'd want next
- Marketing spend by channel (to compare retention spend with acquisition cost)
- Website sessions (to measure conversion, not just orders)
- Customer contact consent (to know how many new customers a win-back could actually reach)

## Appendix: Method
Queries: analyses/12_capstone_repeat_drivers.sql, 03, 06, 13, 15. Significance test and
power calculations as in notebooks/04_statistics_ab_test.ipynb.

**Value of a returning customer:** R$167 of later orders per returning customer
(1.12 later orders at a mean of R$149). Measured on all returning customers in the data.

**A. Fix late first deliveries**
| Input | Value | Source |
|---|---|---|
| New customers a year with a late first delivery | 5,250 | first orders Jun 2017 to May 2018 |
| Their return rate | 1.74% | capstone population |
| Target return rate | 2.57% (on-time rate) | capstone population |
| Extra returning customers a year | 25 (CI low, 0.47 pp) to 44 (0.83 pp) | 5,250 x gap |
| Extra sales a year | R$4.1k to R$7.3k | x R$167 |

**B. First-month win-back**
| Input | Value | Source |
|---|---|---|
| New customers a year | 65,673 | first orders Jun 2017 to May 2018 |
| Current return rate | 2.5% | capstone population |
| Target return rate | 3.0% (conservative) to 3.5% (expected) | assumption: within the 3.1% to 4.3% already seen in high-return categories and voucher payers |
| Extra returning customers a year | 328 to 657 | 65,673 x 0.5 to 1.0 pp |
| Extra sales a year | R$55k to R$110k | x R$167 |
