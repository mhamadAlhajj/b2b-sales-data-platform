select 
    "AddressID" as address_id , 
    "Street" as street , 
    "CityName" as city_name
from {{ source('raw', 'address') }}