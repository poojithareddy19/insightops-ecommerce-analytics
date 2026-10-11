# LinkedIn posts

*Gorla Poojitha*

Four posts, one per big piece of the project. Post them about a week apart, in this order,
so each one has time to get comments. Attach the image listed under each post; posts with
an image get far more reach than text-only ones.

Replace `[blog link]` with the real URL after publishing each blog post.

---

## Post 1: the dashboard

**Attach:** `dashboards/executive_overview.png`

> 98 out of 100 customers never came back.
>
> I analyzed about 100,000 orders from Olist, a Brazilian e-commerce marketplace, and built an executive dashboard from scratch to see how the business was really doing.
>
> On the surface it looked healthy: R$15.7M in revenue, and January to August sales up 140% on the year before. But revenue had gone flat since January 2018, and the retention heatmap at the bottom right is almost empty. Only 2.2% of customers ever ordered again on a different day.
>
> What I built:
> • A DuckDB warehouse modeled with dbt (17 models, 49 data tests)
> • An executive and an operations dashboard, generated straight from the warehouse
> • A data audit of 15 issues found before trusting any number
>
> Code and dashboards: https://github.com/poojithareddy19/insightops-ecommerce-analytics
>
> If you've worked in e-commerce: is a repeat rate this low normal for a marketplace, or a warning sign?
>
> #DataAnalytics #dbt #SQL #Ecommerce

---

## Post 2: the A/B test memo

**Attach:** a screenshot of the "Business tradeoff" table in `docs/ab-test-memo.md`

> My A/B test was a statistically significant win. I still recommended not shipping it.
>
> I simulated a free-shipping experiment on real Olist customer IDs. Conversion went up by 0.86 percentage points, p < 0.0001. Clear result.
>
> Then I counted the cost. Free shipping on every treatment order cost about R$63,500. At an assumed 10% commission, the extra sales earned Olist about R$4,400. Net: roughly R$59,000 lost.
>
> What I did:
> • Sized the test before running it (31,218 customers per group)
> • Checked the setup with a sample ratio check and an A/A test
> • Simulated "peeking" daily: it pushed false positives from 5% to 24%
>
> The decision memo: https://github.com/poojithareddy19/insightops-ecommerce-analytics/blob/main/docs/ab-test-memo.md
>
> How do you decide when a significant result isn't worth shipping?
>
> #ABTesting #Statistics #ProductAnalytics #DataAnalytics

---

## Post 3: blog post on modeling with dbt

**Attach:** `dashboards/dbt_lineage.png`

> The column was called customer_id. It wasn't a customer.
>
> In the Olist dataset, there are 99,441 customer IDs but only 96,096 real people. A new customer_id is created for every order. Count with it, and every retention number you produce is wrong before you start.
>
> I wrote up how I modeled the 9 messy tables with dbt:
> • Why I loaded everything as text first
> • How a test warning led me to 772 paid orders that never shipped
> • The 250 "repeat customers" that were really one checkout split in two, which no test caught
>
> Read it here: [blog link]
>
> What's the sneakiest data issue you've found hiding behind a normal-looking column?
>
> #dbt #AnalyticsEngineering #SQL #DataQuality

---

## Post 4: blog post on retention

**Attach:** slide 3 of `docs/capstone-deck.pdf`, exported as an image

> Fixing late deliveries would be worth only R$4,000 to R$7,000 a year in repeat sales.
>
> That surprised me. Customers whose first order arrived late came back a third less often (1.74% vs 2.57%). So I expected fixing delivery to be the big retention win.
>
> It isn't, because repeat buying is so rare to begin with. What the data pointed to instead:
> • Half of all returns happen within 30 days, so that's the window to act in
> • A first-month win-back offer could be worth R$55,000 to R$110,000 a year
> • It should be A/B tested first, with the offer's cost counted against commission
>
> The full write-up: [blog link]
>
> Has a "fix the obvious problem" plan ever turned out to be smaller than you expected?
>
> #CustomerRetention #DataAnalytics #Ecommerce #Analytics
