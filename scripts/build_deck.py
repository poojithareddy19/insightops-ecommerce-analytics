"""
Build the 5-slide capstone deck as docs/capstone-deck.pdf.
Numbers come from the warehouse; the impact ranges match docs/capstone-memo.md.
"""
from pathlib import Path

import duckdb
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import PercentFormatter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "warehouse" / "insightops.duckdb"
OUTPUT_FILE = PROJECT_ROOT / "docs" / "capstone-deck.pdf"

SURFACE = "#fcfcfb"
MAIN = "#2a78d6"
HIGHLIGHT = "#eb6834"
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
GRID = "#e4e3df"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
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
    "axes.axisbelow": True,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    # "R$55k to R$110k" has two dollar signs, which matplotlib would read as math markup
    "text.parse_math": False,
})

# Same population as the capstone query: first valid order Jan 2017 - May 2018
FIRST_ORDERS = """
    with f as (
        select * from marts.fct_orders
        where is_valid_order
        qualify row_number() over (partition by customer_unique_id order by purchased_at, order_id) = 1
    )
    select f.*, d.is_returning_customer
    from f join marts.dim_customers d using (customer_unique_id)
    where f.order_date between date '2017-01-01' and date '2018-05-31'
"""


def slide(number, title, subtitle=""):
    fig = plt.figure(figsize=(13.33, 7.5))
    fig.text(0.06, 0.88, title, fontsize=24, fontweight="bold", wrap=True)
    if subtitle:
        fig.text(0.06, 0.83, subtitle, fontsize=13, color=INK_SECONDARY)
    fig.text(0.94, 0.04, f"{number} / 5", fontsize=10, color=INK_SECONDARY, ha="right")
    fig.text(0.06, 0.04, "InsightOps | Olist marketplace, Sep 2016 to Aug 2018", fontsize=10, color=INK_SECONDARY)
    return fig


def bullet_block(fig, x, y, lines, size=14, gap=0.065):
    for i, line in enumerate(lines):
        fig.text(x, y - i * gap, line, fontsize=size, va="top")


def main() -> None:
    con = duckdb.connect(str(DB_PATH), read_only=True)
    returning = con.sql("""
        select count(*) filter (where is_returning_customer), count(*)
        from marts.dim_customers where valid_orders > 0
    """).fetchone()
    curve = con.sql("""
        with v as (
            select customer_unique_id, date_trunc('month', purchased_at) as m
            from marts.fct_orders where is_valid_order
        ),
        c as (select customer_unique_id, min(m) as cohort from v group by 1),
        a as (
            select c.cohort, date_diff('month', c.cohort, v.m) as k, count(distinct v.customer_unique_id) as n
            from v join c using (customer_unique_id) group by 1, 2
        ),
        pct as (
            select a.k, 100.0 * a.n / s.n as p
            from a join a s on a.cohort = s.cohort and s.k = 0
            where a.cohort between '2017-01-01' and '2017-08-01' and a.k between 1 and 12
        )
        select k, avg(p) as retention from pct group by 1 order by 1
    """).df()
    segments = con.sql(f"""
        select
            case when is_late then 'Late' else 'On time' end
              || ', ' ||
            case when review_score <= 2 then '1-2 stars' when review_score >= 4 then '4-5 stars' else '3 stars' end
              as segment,
            count(*) as customers,
            avg(case when is_returning_customer then 1 else 0 end) as rate
        from ({FIRST_ORDERS})
        where review_score is not null
        group by 1 having count(*) >= 1000
        order by rate
    """).df()
    late_vs = con.sql(f"""
        select avg(case when is_returning_customer then 1 else 0 end) filter (where is_late) as late,
               avg(case when is_returning_customer then 1 else 0 end) filter (where not coalesce(is_late, false)) as on_time
        from ({FIRST_ORDERS})
    """).fetchone()

    with PdfPages(OUTPUT_FILE) as pdf:
        # 1. The answer
        fig = slide(1, "Repeat purchases are the growth engine Olist doesn't have yet",
                    "Revenue has been flat since January 2018, and almost every order comes from a new customer.")
        fig.text(0.06, 0.52, f"{returning[0] / returning[1]:.1%}", fontsize=96, fontweight="bold", color=MAIN)
        fig.text(0.06, 0.44, f"of customers come back on a later day ({returning[0]:,} of {returning[1]:,})",
                 fontsize=16, color=INK_SECONDARY)
        bullet_block(fig, 0.06, 0.33, [
            "A late first delivery cuts the chance of returning by a third.",
            "A tested first-month win-back program could add R$55k to R$110k a year in sales.",
        ], size=15)
        pdf.savefig(fig); plt.close(fig)

        # 2. Retention curve
        fig = slide(2, "Only 2.2% of customers ever come back",
                    "Average share of a monthly cohort ordering again N months after their first order (2017 cohorts)")
        ax = fig.add_axes([0.08, 0.14, 0.86, 0.62])
        ax.plot(curve["k"], curve["retention"], color=MAIN, lw=2.5, marker="o", markersize=7,
                markeredgecolor=SURFACE, markeredgewidth=2)
        ax.set_xticks(curve["k"], [f"+{k}" for k in curve["k"]])
        ax.set_xlabel("months after first order", fontsize=12)
        ax.yaxis.set_major_formatter(PercentFormatter(decimals=1))
        ax.set_ylim(0, 1)
        ax.annotate(f"{curve['retention'].iloc[0]:.2f}% in month 1", (1, curve["retention"].iloc[0]),
                    xytext=(12, 8), textcoords="offset points", fontsize=12, color=INK_SECONDARY)
        pdf.savefig(fig); plt.close(fig)

        # 3. First-order experience
        fig = slide(3, "A late first delivery cuts the chance of returning by a third",
                    f"Return rate by first-order experience: late {late_vs[0]:.2%} vs on time {late_vs[1]:.2%} "
                    "(gap 0.83 pp, 95% CI 0.47 to 1.19)")
        ax = fig.add_axes([0.22, 0.14, 0.72, 0.62])
        colors = [HIGHLIGHT if s.startswith("Late") else MAIN for s in segments["segment"]]
        bars = ax.barh(segments["segment"], segments["rate"], height=0.55, color=colors)
        for bar, rate, n in zip(bars, segments["rate"], segments["customers"]):
            ax.text(bar.get_width() + 0.0005, bar.get_y() + bar.get_height() / 2,
                    f"{rate:.2%}  ({n:,} customers)", va="center", fontsize=12, color=INK_SECONDARY)
        ax.xaxis.set_major_formatter(PercentFormatter(1.0, decimals=1))
        ax.set_xlim(0, segments["rate"].max() * 1.5)
        ax.grid(axis="y", visible=False)
        ax.tick_params(axis="y", labelsize=13, length=0)
        fig.text(0.22, 0.08, "First orders Jan 2017 to May 2018, so every customer had 3+ months to return. "
                 "Segments with 1,000+ customers.", fontsize=10, color=INK_SECONDARY)
        pdf.savefig(fig); plt.close(fig)

        # 4. Recommendations
        fig = slide(4, "A first-month win-back is worth more than any delivery fix",
                    "Estimated extra sales per year (GMV, item price + freight)")
        rows = [
            ("1. Win-back offer within 30 days of the first delivery", "R$55k to R$110k",
             "65,673 new customers a year; return rate 2.5% to 3.0-3.5%"),
            ("2. Pilot it in high-return categories first", "proves #1 cheaply",
             "bed_bath_table, furniture_decor, sports, pet, fashion bags: 14,900 a year, return at 3.1-4.3%"),
            ("3. Realistic delivery promises in the North/Northeast", "R$4k to R$7k",
             "5,250 late first orders a year; main payoff is fewer 1-2 star reviews"),
        ]
        for i, (action, impact, basis) in enumerate(rows):
            y = 0.68 - i * 0.18
            fig.text(0.06, y, action, fontsize=16, fontweight="bold")
            fig.text(0.94, y, impact, fontsize=18, fontweight="bold", color=MAIN, ha="right")
            fig.text(0.075, y - 0.05, basis, fontsize=12, color=INK_SECONDARY)
        fig.text(0.06, 0.12, "Value of a returning customer: R$167 of later orders. "
                 "Assumptions and ranges in docs/capstone-memo.md.", fontsize=11, color=INK_SECONDARY)
        pdf.savefig(fig); plt.close(fig)

        # 5. Next steps
        fig = slide(5, "Next step: prove the win-back with an A/B test before scaling",
                    "The free-shipping test showed an offer can lift conversion and still lose money.")
        bullet_block(fig, 0.06, 0.72, [
            "Test design",
            "    Randomize new customers by hashed customer ID; primary metric: return within 90 days",
            "    +1 pp from a 2.5% base needs about 4,500 customers per group: under 2 months of new customers",
            "    Fix the sample size up front; no peeking (daily peeking gave a 24% false positive rate)",
            "    Count the voucher cost against commission, not against sales",
            "",
            "Risks",
            "    Late first orders also differ by state, seller and category; the gap may not all be lateness",
            "",
            "Data needed",
            "    Marketing spend by channel, website sessions, customer contact consent",
        ], size=14, gap=0.055)
        pdf.savefig(fig); plt.close(fig)

    print("Saved", OUTPUT_FILE)


if __name__ == "__main__":
    main()
