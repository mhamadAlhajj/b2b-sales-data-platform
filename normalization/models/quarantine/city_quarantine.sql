select 
    distinct
    Trim("CityName") as city_name , 
    Trim("RegionName") as region_name
from {{source('raw','cities')}}
where Trim("CityName") is  null and  Trim("RegionName") is  null