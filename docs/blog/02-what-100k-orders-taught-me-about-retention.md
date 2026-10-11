# What 100k orders taught me about retention

*Gorla Poojitha*

I spent a few weeks analyzing about 100,000 orders from Olist, a Brazilian e-commerce
marketplace. The number that stuck with me is this one:

**2.2%.**

That's the share of customers who ever came back and ordered again on a different day.
2,065 out of 94,990. Everyone else bought once and disappeared.

This post is about how I got to that number, what seems to predict whether someone comes
back, and what I'd actually recommend, including the recommendation the data talked me
out of.

## Getting the number right

The first version of the number was wrong twice.

The dataset has a `customer_id` column that isn't a customer: Olist creates a new one for
every order. Count with it and the repeat rate is close to zero by construction. The real
person is `customer_unique_id`.

Even then, the naive count ("customers with two or more orders") gave 3.0%. When I
cross-checked it with a second query, 250 of those "repeat customers" had both orders at
the exact same second. That's one checkout split into two orders, not someone returning.
Counting only customers who ordered again on a different day gives 2.2%.

The gap between 3.0% and 2.2% sounds small. But it's a quarter of the repeat customers,
and every estimate built on top of it inherits the error.

## The cohort view

A cohort table groups customers by the month of their first order and tracks what share
come back in each later month.

![Executive overview with the cohort heatmap](../../dashboards/executive_overview.png)

The heatmap is almost empty. No monthly cohort of 100 or more customers ever had more than
0.71% of them order again in any single later month. For the 2017 cohorts, about 0.48%
came back in the first month, and it hovers between 0.2% and 0.3% after that.

When people do come back, they come back fast. Of all second orders, 30% happen the same
day, the median gap is 28 days, 51% happen within 30 days and 68% within 90.

That changes how you'd design anything to bring people back. A "we miss you" email after
six months is too late for most of the customers who were ever going to return.

## What predicts coming back

To compare fairly, I only looked at customers whose first order was between January 2017
and May 2018, so everyone had at least three months to return before the data ends.
Otherwise recent customers drag the rate down simply because they haven't had time.

**Delivery.** Customers whose first order arrived late came back at 1.74%. Customers whose
first order wasn't late came back at 2.57%. That's a third lower, with a 95% confidence
interval of 0.47 to 1.19 percentage points on the gap.

Combine lateness with the review the customer left and the spread widens: late and rated
1 to 2 stars returns at 1.48%; on time and rated 4 to 5 stars returns at 2.67%.

Late deliveries hurt reviews even more directly. Orders delivered 7 or more days late
average 1.70 stars, and 79% of them get 1 or 2 stars. On-time orders average 4.17. The
gap holds inside every one of the ten largest states, so it isn't just remote regions
dragging the numbers down.

**Category.** What someone buys first matters. Customers whose first order was in
fashion bags and accessories came back at 4.3%; bed, bath and table at 3.4%; pet shop at
3.3%; furniture and decor at 3.2%. Customers who started with electronics came back at
1.7%.

**Concentration, but not loyalty.** The top 10% of customers bring in 38% of revenue. On
most retail data that would mean loyal regulars. Here it means people who placed one big
order. A standard RFM segmentation barely works on this data: the "Loyal" segment is 1.3%
of customers.

## The recommendation the maths talked me out of

My first instinct was obvious: fix late deliveries, and customers will come back.

Then I did the arithmetic. About 5,250 new customers a year get a late first delivery.
Closing the gap (0.83 points) turns roughly 25 to 44 of them into returning customers.
A returning customer brings about R$167 in later orders. That's **R$4,000 to R$7,000 a
year** in repeat sales.

That's tiny. Not because delivery doesn't matter, but because repeat buying is so rare
that even a big relative improvement on a small group is a small absolute number. Fixing
late deliveries is still worth doing, mostly because of those 1 to 2 star reviews, which
every future shopper sees. But it isn't a retention strategy.

The bigger lever is everyone else. About 65,700 new customers arrive each year. A
win-back offer in the first 30 days, when returns actually happen, that lifts the return
rate from 2.5% to somewhere between 3.0% and 3.5%, would add **R$55,000 to R$110,000 a
year**. Those targets aren't invented: customers who start in high-return categories, or
who paid with a voucher, already come back at 3.1% to 4.3%.

## Test it before you believe it

I'd want an A/B test before rolling any of this out, and not only for the usual reasons.

Earlier in the project I simulated a free-shipping experiment. It "worked": conversion
went up by 0.86 percentage points, clearly significant. Then I counted the cost. Free
shipping on every treatment order cost about R$63,500, against about R$4,400 of extra
commission. Statistically a win, financially a loss of about R$59,000.

A win-back voucher has the same risk. So the test should count the voucher cost against
commission, not against sales. Detecting a one-point lift from a 2.5% base needs about
4,500 customers per group, which is under two months of new customers.

## Caveats

- **This is observational data.** Late first orders also differ by state, seller and
  category, so not all of that 0.83 point gap is necessarily caused by lateness.
- **The data covers about two years,** so "R$167 per returning customer" undercounts
  lifetime value. The estimates lean conservative.
- **The figures are sales, not profit.** Olist keeps a commission, which is a fraction of
  those amounts.

The short version: on this marketplace, almost nobody comes back, the window to bring
them back is the first month, and the most obvious fix is real but small. The full
analysis, memo and deck are in the repo:
[github.com/poojithareddy19/insightops-ecommerce-analytics](https://github.com/poojithareddy19/insightops-ecommerce-analytics).
