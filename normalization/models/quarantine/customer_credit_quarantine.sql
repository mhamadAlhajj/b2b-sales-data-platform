select user_id as customer_id , creditLimit 
from {{source('raw' , 'user_details')}}
where customer_id is null