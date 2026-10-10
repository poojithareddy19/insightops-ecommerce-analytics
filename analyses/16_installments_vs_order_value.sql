-- Business question: Do bigger orders get paid in more installments?
-- Techniques: CASE buckets, median vs mean, share of orders.
-- Only credit card orders: boleto, voucher and debit are paid in one go.

select
    case
        when max_installments <= 1  then '01'
        when max_installments <= 3  then '02-03'
        when max_installments <= 6  then '04-06'
        when max_installments <= 9  then '07-09'
        else '10+'
    end                                                            as installments,
    count(*)                                                       as orders,
    round(100.0 * count(*) / sum(count(*)) over (), 1)             as pct_of_orders,
    round(median(order_value), 2)                                  as median_order_value,
    round(avg(order_value), 2)                                     as avg_order_value
from marts.fct_orders
where is_valid_order
  and main_payment_type = 'credit_card'
group by 1
order by 1;
