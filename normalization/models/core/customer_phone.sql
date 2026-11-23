select user_id as customer_id , phone 
from {{source('raw' , 'user_details')}}
where customer_id is not null