with cte_distinct_campaign as (
    select
        distinct
        trim("CampaignName") as campaign_name,
        trim("Channel")      as channel,
        cast("StartDate" as date) as start_date,
        cast("EndDate" as date) as end_date,
        cast("Budget" as int) as budget 
    from {{ source('raw','campaign_log') }}
    where "CampaignName" is not null and "StartDate" is not null
)
select 
    {{ dbt_utils.generate_surrogate_key(["campaign_name", "start_date"]) }} as campaign_id,
    *
from cte_distinct_campaign

