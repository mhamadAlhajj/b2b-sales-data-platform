with orders_cte as {
    select 
        o.OrderId  as order_id, 
        cu.customer_id,
        ci.city_id,
        ci_2.city_id as ship_to_city_id,
        ci_3.city_id as bill_to_city_id,
        o.OrderDate as order_date,
        o.OrderChannel as order_channel , 
        o.Status as status , 
        o.Priority as priority,
        o.GiftMessage as gift_message        
    from {{source('raw','Orders_2025')}}
    UNION 
    select 
        o.OrderId  as order_id, 
        cu.customer_id,
        ci.city_id,
        ci_2.city_id as ship_to_city_id,
        ci_3.city_id as bill_to_city_id,
        o.OrderDate as order_date,
        o.OrderChannel as order_channel , 
        o.Status as status , 
        o.Priority as priority,
        o.GiftMessage as gift_message        
    from {{source('raw','Orders_2026')}}
}
select * from orders_cte
where order_id is not null