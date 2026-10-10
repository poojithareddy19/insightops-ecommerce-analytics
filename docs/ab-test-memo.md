# A/B Test Memo: Free Shipping

*Gorla Poojitha*

> Note: this experiment is SIMULATED on real Olist customer IDs to demonstrate
> methodology. Order values and freight costs are real Olist figures.
> Full analysis: notebooks/04_statistics_ab_test.ipynb

## Decision
**Recommendation: don't ship blanket free shipping.** It lifted conversion by
+0.86 pp (95% CI [+0.57, +1.14]), but on the test population it costs R$63.5k in
shipping against R$4.4k of extra commission. Customers clearly respond to it, so the
next test should be free shipping above a basket threshold.

## Results
| Group | Customers | Converted | Conversion |
|---|---|---|---|
| Control | 47,841 | 2,349 | 4.91% |
| Treatment | 48,255 | 2,783 | 5.77% |

- Lift: +0.86 pp (relative +17%), p < 0.0001
- Sanity checks passed: SRM p = 0.18, A/A p = 0.40

## Business tradeoff
| | Amount |
|---|---|
| Extra orders from the lift | 414 |
| Extra revenue (at the median order value, R$105.28) | R$43,551 |
| Extra commission (10% assumed take rate) | R$4,355 |
| Free shipping cost (2,783 treatment orders x R$22.82 average freight) | R$63,509 |
| **Net** | **about -R$59,000** |

Even counting the full extra revenue rather than commission, the shipping bill is
larger. Breaking even at a 10% commission would need about 6,000 extra orders, a lift
of 12.5 pp: conversion going from 5% to 17.5%. Not realistic.

## Test design
- Hypothesis: free shipping increases conversion.
- Primary metric: conversion (customer places an order during the test), chosen in advance.
- Unit of randomization: customer (MD5 hash of customer_unique_id with an
  experiment-specific salt), not order, so each person sees one consistent experience.
- Sizing: baseline 5%, MDE 10% relative (5.0% to 5.5%), alpha 0.05, power 80%
  -> 31,218 customers per group, about 8 weeks at 8,000 eligible customers a week.

## Pitfalls considered
- **Peeking:** sample size fixed upfront. In 500 simulated A/A tests checked daily for
  20 days, stopping at the first p < 0.05 gave a 24% false positive rate instead of 5%.
- **Multiple comparisons:** one primary metric chosen in advance; secondary metrics
  are exploratory only.
- **Novelty effect:** customers may react to anything new; in a real test, check
  whether the lift fades over the weeks.
- **Repeat behavior:** with a 2% return rate, the test can't tell us whether free
  shipping builds loyalty. That would need a longer follow-up window.
