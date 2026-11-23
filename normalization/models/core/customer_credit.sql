select user_id as customer_id , creditLimit as credit_limit
from {{source('raw' , 'user_details')}}