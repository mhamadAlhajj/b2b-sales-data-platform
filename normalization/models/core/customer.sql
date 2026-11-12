with cte_customer as (
    select 
        cast("CustomerID" as int) as customer_id,
        Trim("CustomerName") as customer_name,
        Trim("Segment") as segment,
        "AddressID" as address_id,
        Trim("AccountManager") as account_manager,
        Trim("PaymentTerms") as payment_terms
    from {{source('raw' , 'cust_master')}}
)
select * from cte_customer