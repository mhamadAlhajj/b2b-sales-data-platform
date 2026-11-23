select customer_id , contactName, Email , isPrimary
from {{source('raw','customer_contacts')}}
where customer_id is null