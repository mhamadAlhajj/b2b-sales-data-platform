with invoice_cte as {
    select 
        invoiceID as invoice_id, 
        OrderId as order_id, 
        cast(Invoice_date as date) as invoice_date
}
select * from invoice_cte
where invoice_id is  null