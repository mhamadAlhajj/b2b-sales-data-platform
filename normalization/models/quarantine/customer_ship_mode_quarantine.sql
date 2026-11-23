select  customer_id , PreferredShipMode 
from {{source('raw' , 'customer_preferences')}}
where customer_id is null