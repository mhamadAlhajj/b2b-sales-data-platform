with cte_cities as (
select 
    distinct
    Trim("CityName") as city_name , 
    Trim("RegionName") as region_name
from {{source('raw','cities')}}
where Trim("CityName") is not null and  Trim("RegionName") is not null
)
select   
    {{ dbt_utils.generate_surrogate_key(["city_name", "region_name"]) }} as city_id,
    city_name ,
    region_name
from cte_cities