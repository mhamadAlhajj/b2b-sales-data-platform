select  customer_id , SupportLanguage 
from {{source('raw' , 'customer_preferences')}}
where customer_id is null