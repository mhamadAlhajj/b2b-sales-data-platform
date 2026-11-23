select  customer_id , PreferredShipMode as preferred_ship_mode
from {{source('raw' , 'customer_preferences')}}
where customer_id is not null