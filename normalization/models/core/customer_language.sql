select  customer_id , SupportLanguage as support_language
from {{source('raw' , 'customer_preferences')}}
where customer_id is not null