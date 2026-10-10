"""
Build the two dashboard pages from the dbt marts and save them as PNGs:

    dashboards/executive_overview.png   headline KPIs, revenue trend, states, categories, retention
    dashboards/operations.png           delivery speed, lateness and reviews

Same metric definitions as docs/metric-catalog.md: valid orders only, trends limited
to Jan 2017 - Aug 2018, delivery metrics on delivered orders only.
"""
from pathlib import Path

import duckdb
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import FuncFormatter, MultipleLocator, PercentFormatter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "warehouse" / "insightops.duckdb"
OUT_DIR = PROJECT_ROOT / "dashboards"

# Chart palette: one main color, one highlight, ink for text, a recessive grid
SURFACE = "#fcfcfb"
MAIN = "#2a78d6"
HIGHLIGHT = "#eb6834"
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
GRID = "#e4e3df"
BLUES = LinearSegmentedColormap.from_list(
    "blues", ["#f0efec", "#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])

TREND_START, TREND_END = "2017-01-01", "2018-08-01"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "text.color": INK,
    "axes.labelcolor": INK_SECONDARY,
    "axes.edgecolor": GRID,
    "axes.facecolor": SURFACE,
    "figure.facecolor": SURFACE,
    "xtick.color": INK_SECONDARY,
    "ytick.color": INK_SECONDARY,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": GRID,
    "grid.linewidth": 0.8,
    "axes.axisbelow": True,
})

brl = FuncFormatter(lambda v, _: f"R${v / 1e6:.1f}M" if v >= 1e6 else f"R${v / 1e3:,.0f}K")


def query(con, sql):
    return con.sql(sql).df()


def stat_tile(ax, label, value, note=""):
    ax.axis("off")
    ax.text(0.0, 0.78, label, fontsize=11, color=INK_SECONDARY, transform=ax.transAxes)
    ax.text(0.0, 0.30, value, fontsize=24, fontweight="bold", color=INK, transform=ax.transAxes)
    if note:
        ax.text(0.0, 0.02, note, fontsize=9, color=INK_SECONDARY, transform=ax.transAxes)


def title(ax, question, subtitle=""):
    ax.set_title(question, loc="left", fontsize=12.5, fontweight="bold", color=INK, pad=22)
    if subtitle:
        ax.text(0, 1.02, subtitle, transform=ax.transAxes, fontsize=9, color=INK_SECONDARY, va="bottom")


def hbar(ax, labels, values, fmt, highlight_first=True):
    """Horizontal bars, largest at the top, values at the tips."""
    y = np.arange(len(labels))[::-1]
    colors = [HIGHLIGHT if (highlight_first and i == 0) else MAIN for i in range(len(labels))]
    ax.barh(y, values, height=0.62, color=colors)
    ax.set_yticks(y, labels)
    ax.grid(axis="y", visible=False)
    ax.tick_params(axis="y", length=0)
    top = max(values)
    for yi, v in zip(y, values):
        ax.text(v + top * 0.01, yi, fmt(v), va="center", fontsize=9, color=INK_SECONDARY)
    ax.set_xlim(0, top * 1.18)


def executive_overview(con):
    kpi = query(con, """
        select sum(order_value) as revenue, count(*) as orders,
               sum(order_value) / count(*) as aov, median(order_value) as median_order,
               count(distinct customer_unique_id) as customers
        from marts.fct_orders where is_valid_order
    """).iloc[0]
    returning = query(con, """
        select avg(case when is_returning_customer then 1 else 0 end) as rate
        from marts.dim_customers where valid_orders > 0
    """).iloc[0]["rate"]
    monthly = query(con, f"""
        select date_trunc('month', order_date) as month, sum(order_value) as revenue
        from marts.fct_orders
        where is_valid_order and date_trunc('month', order_date) between '{TREND_START}' and '{TREND_END}'
        group by 1 order by 1
    """)
    states = query(con, """
        select customer_state, sum(order_value) as revenue
        from marts.fct_orders where is_valid_order
        group by 1 order by 2 desc limit 10
    """)
    categories = query(con, """
        select p.category_name, sum(i.item_total) as revenue
        from marts.fct_order_items i join marts.dim_products p using (product_id)
        where i.is_valid_order group by 1 order by 2 desc limit 10
    """)
    cohort = query(con, f"""
        with v as (
            select customer_unique_id, date_trunc('month', purchased_at) as m
            from marts.fct_orders where is_valid_order
        ),
        c as (select customer_unique_id, min(m) as cohort from v group by 1),
        a as (
            select c.cohort, date_diff('month', c.cohort, v.m) as k, count(distinct v.customer_unique_id) as n
            from v join c using (customer_unique_id) group by 1, 2
        )
        select a.cohort, a.k, 100.0 * a.n / s.n as pct
        from a join a s on a.cohort = s.cohort and s.k = 0
        where a.k between 1 and 6 and a.cohort between '{TREND_START}' and '2018-02-01'
    """)

    fig = plt.figure(figsize=(18, 12.5))
    gs = GridSpec(3, 5, figure=fig, height_ratios=[0.42, 1, 1], hspace=0.55, wspace=0.55,
                  left=0.1, right=0.97, top=0.88, bottom=0.06)
    fig.text(0.07, 0.955, "InsightOps: Executive Overview", fontsize=20, fontweight="bold")
    fig.text(0.07, 0.928, "Olist marketplace, valid orders (canceled and unavailable excluded). "
             "Trends: Jan 2017 to Aug 2018, the complete months.", fontsize=10.5, color=INK_SECONDARY)

    stat_tile(fig.add_subplot(gs[0, 0]), "Revenue", f"R${kpi.revenue / 1e6:.2f}M", "items + freight, BRL")
    stat_tile(fig.add_subplot(gs[0, 1]), "Orders", f"{kpi.orders / 1e3:.1f}K")
    stat_tile(fig.add_subplot(gs[0, 2]), "Average order value", f"R${kpi.aov:,.0f}",
              f"median order R${kpi.median_order:,.0f}")
    stat_tile(fig.add_subplot(gs[0, 3]), "Customers", f"{kpi.customers / 1e3:.1f}K", "distinct people")
    stat_tile(fig.add_subplot(gs[0, 4]), "Returning customers", f"{returning:.1%}",
              "ordered again on another day")

    ax = fig.add_subplot(gs[1, :3])
    ax.plot(monthly["month"], monthly["revenue"], color=MAIN, lw=2, solid_capstyle="round")
    ax.fill_between(monthly["month"], monthly["revenue"], color=MAIN, alpha=0.10)
    last = monthly.iloc[-1]
    peak = monthly.loc[monthly["revenue"].idxmax()]
    ax.scatter([last.month, peak.month], [last.revenue, peak.revenue], s=50, color=MAIN,
               edgecolor=SURFACE, linewidth=2, zorder=3)
    ax.annotate(f"Nov 2017 peak\nR${peak.revenue / 1e6:.2f}M", (peak.month, peak.revenue),
                xytext=(-12, 0), textcoords="offset points", ha="right", va="center", fontsize=9, color=INK_SECONDARY)
    ax.annotate(f"R${last.revenue / 1e6:.2f}M", (last.month, last.revenue),
                xytext=(8, -4), textcoords="offset points", fontsize=9, color=INK_SECONDARY)
    ax.yaxis.set_major_formatter(brl)
    ax.set_ylim(0, None)
    title(ax, "Is revenue growing?", "Monthly revenue: strong growth in 2017, flat since January 2018")

    ax = fig.add_subplot(gs[1, 3:])
    hbar(ax, states["customer_state"], states["revenue"], lambda v: f"R${v / 1e6:.1f}M")
    ax.xaxis.set_major_formatter(brl)
    sp_share = states.iloc[0].revenue / kpi.revenue
    title(ax, "Where are our customers?", f"Top 10 states by revenue; SP alone is {sp_share:.0%}")

    ax = fig.add_subplot(gs[2, :3])
    hbar(ax, categories["category_name"], categories["revenue"], lambda v: f"R${v / 1e6:.2f}M")
    ax.xaxis.set_major_formatter(brl)
    title(ax, "Which categories drive revenue?", "Top 10 categories, item price + freight")

    ax = fig.add_subplot(gs[2, 3:])
    grid = cohort.pivot(index="cohort", columns="k", values="pct").sort_index()
    im = ax.imshow(grid.values, cmap=BLUES, aspect="auto", vmin=0, vmax=0.8)
    ax.set_xticks(range(grid.shape[1]), [f"+{k}" for k in grid.columns])
    ax.set_yticks(range(grid.shape[0]), [d.strftime("%b %Y") for d in grid.index])
    ax.grid(False)
    ax.tick_params(length=0)
    for (r, c), v in np.ndenumerate(grid.values):
        if not np.isnan(v):
            ax.text(c, r, f"{v:.2f}", ha="center", va="center", fontsize=7.5,
                    color="white" if v > 0.45 else INK)
    ax.set_xlabel("months after first order")
    cbar = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
    cbar.ax.yaxis.set_major_formatter(PercentFormatter(decimals=1))
    cbar.outline.set_visible(False)
    title(ax, "Do customers come back?", "% of each monthly cohort ordering again; never above 0.8%")

    out = OUT_DIR / "executive_overview.png"
    fig.savefig(out, dpi=110)
    plt.close(fig)
    print("Saved", out)


def operations(con):
    kpi = query(con, """
        select median(delivery_days) as median_days, avg(case when is_late then 1 else 0 end) as late_rate,
               avg(review_score) as avg_review
        from marts.fct_orders where is_delivered
    """).iloc[0]
    monthly = query(con, f"""
        select date_trunc('month', order_date) as month, median(delivery_days) as median_days,
               avg(case when is_late then 1 else 0 end) as late_rate
        from marts.fct_orders
        where is_delivered and date_trunc('month', order_date) between '{TREND_START}' and '{TREND_END}'
        group by 1 order by 1
    """)
    states = query(con, """
        select customer_state, median(delivery_days) as median_days, count(*) as orders
        from marts.fct_orders where is_delivered
        group by 1 order by 2 desc, 3 desc limit 12
    """)
    reviews = query(con, """
        select case when is_late then 'Late' else 'On time' end as delivery, avg(review_score) as avg_review
        from marts.fct_orders where is_delivered and review_score is not null
        group by 1 order by 2
    """)
    categories = query(con, """
        with o as (
            select distinct p.category_name, f.order_id, f.is_late, f.review_score
            from marts.fct_order_items i
            join marts.fct_orders f using (order_id)
            join marts.dim_products p using (product_id)
            where f.is_delivered
        )
        select category_name, count(*) as orders, avg(case when is_late then 1 else 0 end) as late_rate,
               avg(review_score) as avg_review
        from o group by 1 having count(*) >= 1000
        order by late_rate desc limit 10
    """)

    fig = plt.figure(figsize=(18, 12.5))
    gs = GridSpec(3, 6, figure=fig, height_ratios=[0.42, 1, 1], hspace=0.55, wspace=0.9,
                  left=0.07, right=0.97, top=0.88, bottom=0.06)
    fig.text(0.07, 0.955, "InsightOps: Operations", fontsize=20, fontweight="bold")
    fig.text(0.07, 0.928, "Delivered orders only. Late = delivered after the estimated date given at purchase.",
             fontsize=10.5, color=INK_SECONDARY)

    stat_tile(fig.add_subplot(gs[0, 0:2]), "Median delivery time", f"{kpi.median_days:.0f} days",
              "purchase to customer")
    stat_tile(fig.add_subplot(gs[0, 2:4]), "Late delivery rate", f"{kpi.late_rate:.1%}")
    stat_tile(fig.add_subplot(gs[0, 4:6]), "Average review", f"{kpi.avg_review:.2f} / 5",
              "latest review per order")

    # Two measures, two charts: never a second y-axis
    ax = fig.add_subplot(gs[1, 0:3])
    ax.plot(monthly["month"], monthly["median_days"], color=MAIN, lw=2)
    ax.set_ylim(0, None)
    ax.set_ylabel("days")
    title(ax, "Is delivery getting faster?", "Median days from purchase to delivery, by order month")

    ax = fig.add_subplot(gs[1, 3:6])
    ax.plot(monthly["month"], monthly["late_rate"], color=MAIN, lw=2)
    worst = monthly.loc[monthly["late_rate"].idxmax()]
    ax.scatter([worst.month], [worst.late_rate], s=50, color=HIGHLIGHT, edgecolor=SURFACE, linewidth=2, zorder=3)
    ax.annotate(f"{worst.month:%b %Y}: {worst.late_rate:.0%}", (worst.month, worst.late_rate),
                xytext=(8, 0), textcoords="offset points", fontsize=9, color=INK_SECONDARY)
    ax.yaxis.set_major_locator(MultipleLocator(0.05))
    ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    ax.set_ylim(0, None)
    title(ax, "Are we keeping our delivery promise?", "Share of delivered orders that arrived late")

    ax = fig.add_subplot(gs[2, 0:2])
    hbar(ax, states["customer_state"], states["median_days"], lambda v: f"{v:.0f} d")
    sp = query(con, "select median(delivery_days) from marts.fct_orders where is_delivered and customer_state = 'SP'").iloc[0, 0]
    title(ax, "Which states wait longest?", f"Median delivery days; SP is {sp:.0f}")

    ax = fig.add_subplot(gs[2, 2:4])
    ax.bar(reviews["delivery"], reviews["avg_review"], width=0.5,
           color=[HIGHLIGHT if d == "Late" else MAIN for d in reviews["delivery"]])
    for x, v in enumerate(reviews["avg_review"]):
        ax.text(x, v + 0.08, f"{v:.2f}", ha="center", fontsize=10, color=INK)
    ax.set_ylim(0, 5)
    ax.grid(axis="x", visible=False)
    title(ax, "Do late orders get worse reviews?", "Average review score (1 to 5)")

    ax = fig.add_subplot(gs[2, 4:6])
    ax.axis("off")
    title(ax, "Which categories are late most often?", "Categories with 1,000+ delivered orders")
    rows = [[r.category_name, f"{r.orders:,}", f"{r.late_rate:.1%}", f"{r.avg_review:.2f}"]
            for r in categories.itertuples()]
    table = ax.table(cellText=rows, colLabels=["category", "orders", "late", "review"],
                     loc="upper left", cellLoc="left", colWidths=[0.52, 0.17, 0.14, 0.17])
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.45)
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor(GRID)
        cell.set_linewidth(0.6)
        cell.set_facecolor(SURFACE)
        if r == 0:
            cell.set_text_props(color=INK_SECONDARY, fontweight="bold")

    out = OUT_DIR / "operations.png"
    fig.savefig(out, dpi=110)
    plt.close(fig)
    print("Saved", out)


def main() -> None:
    con = duckdb.connect(str(DB_PATH), read_only=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    executive_overview(con)
    operations(con)


if __name__ == "__main__":
    main()
