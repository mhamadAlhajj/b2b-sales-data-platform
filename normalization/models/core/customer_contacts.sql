select customer_id , contactName as customer_name, Email as email , isPrimary as is_primary
from {{source('raw','customer_contacts')}}
where customer_id is not null