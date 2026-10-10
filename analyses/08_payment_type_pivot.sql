-- Author: Gorla Poojitha
-- Business question: How do customers pay, and is it changing each year?
-- Technique: CASE-based pivot (turning rows into columns).

select
    year(order_date)                                                        as order_year,
    count(*)                                                                as orders,
    round(100.0 * avg(case when main_payment_type = 'credit_card' then 1 else 0 end), 1) as credit_card_pct,
    round(100.0 * avg(case when main_payment_type = 'boleto'      then 1 else 0 end), 1) as boleto_pct,
    round(100.0 * avg(case when main_payment_type = 'voucher'     then 1 else 0 end), 1) as voucher_pct,
    round(100.0 * avg(case when main_payment_type = 'debit_card'  then 1 else 0 end), 1) as debit_card_pct,
    round(avg(max_installments), 1)                                         as avg_installments
from marts.fct_orders
where is_valid_order
group by 1
order by 1;
