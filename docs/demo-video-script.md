# Demo video script

*Gorla Poojitha*

About 2.5 minutes at a relaxed speaking pace. Record with Loom or OBS Studio, screen plus
a small webcam bubble if you like. The **Say** text is meant to be spoken, not read word
for word; it's fine to paraphrase.

## Before you record

Open these, in this order, so you can switch with one click each:

1. `dashboards/executive_overview.png` (full screen)
2. `dbt/models/marts/fct_orders.sql` in VS Code
3. `dashboards/dbt_lineage.png`
4. `docs/capstone-deck.pdf`, on slide 3, then slide 4

Close notifications, and zoom VS Code in (Ctrl and +) so the SQL is readable on a phone.

---

## 1. Who I am and what this is (0:00 to 0:20)

**Screen:** the repo's README on GitHub, scrolled to the top.

**Say:**
> Hi, I'm Gorla Poojitha. This is InsightOps, an end-to-end analytics project on a real
> Brazilian e-commerce marketplace called Olist: about a hundred thousand orders. I took
> it from raw CSV files to a tested warehouse, SQL analysis, an A/B test, dashboards, and
> a recommendation for the business.

## 2. The executive dashboard and the headline (0:20 to 1:20)

**Screen:** `executive_overview.png`. Point at each area as you mention it.

**Say:**
> This is the executive overview. Across the top: 15.7 million reais in revenue, about
> 98 thousand orders, and an average order of 160 reais. The median order is only 105,
> because a few big orders pull the average up, so I show both.
>
> *(point at the revenue chart)* Revenue grew fast through 2017, then went flat from
> January 2018.
>
> *(point at the states and categories)* São Paulo alone is 37% of revenue, and health
> and beauty is the biggest category.
>
> *(point at the last tile, then the heatmap)* But this is the number that matters:
> 2.2%. Only 2.2% of customers ever come back and order again on another day. This
> heatmap shows it. Each row is the month a group of customers first bought, and no
> group ever has more than about 0.7% returning in any later month. When growth from
> new customers stalls, there's nothing underneath it.

## 3. One dbt model and the lineage (1:20 to 2:00)

**Screen:** `fct_orders.sql`, scrolling slowly. Then switch to `dbt_lineage.png`.

**Say:**
> All of this comes from a warehouse I built with dbt and DuckDB. This is fct_orders:
> one row per order, with revenue, delivery time, review score and a late flag already
> worked out, so most questions become a single-table query.
>
> *(switch to the lineage graph)* Ten raw sources flow into ten staging models and seven
> mart tables, with 49 data tests running on every build. Those checks caught real
> problems: customer_id turned out to identify an order, not a person, and 250
> "repeat customers" were really one checkout split in two.

## 4. The recommendation (2:00 to 2:35)

**Screen:** `capstone-deck.pdf`, slide 3. Switch to slide 4 at "the bigger lever".

**Say:**
> So what should Olist do? Customers whose first delivery is late come back a third less
> often. But repeat buying is so rare that fixing late deliveries is only worth about
> 4 to 7 thousand reais a year in repeat sales.
>
> *(switch to slide 4)* The bigger lever is a win-back offer in the first month, when
> almost all returns happen. That's worth an estimated 55 to 110 thousand reais a year,
> and I'd prove it with an A/B test before rolling it out.
>
> Everything, including the code, is linked below. Thanks for watching.

---

## After recording

- Trim the start and end; keep it under 3 minutes.
- Add the video link to the top of the README, next to the capstone memo link.
- In the video description, link the repo:
  https://github.com/poojithareddy19/insightops-ecommerce-analytics
