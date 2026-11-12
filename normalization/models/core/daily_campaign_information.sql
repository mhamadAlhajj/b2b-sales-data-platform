with cte_distinct_campaign as (
    select
        c.campaign_id ,
        trim(cl."CampaignName") as campaign_name,
        cast(cl."StartDate" as date)    as start_date,
        cast(cl."Date" as date) as daily_date,
        cast(cl."Impressions" as int) as impressions ,
        cast(cl."Clicks" as int) as clicks,
        cast(cl."Spend" as float) as spend 
    from {{ source('raw','campaign_log') }} cl
    inner join {{ref('campaign')}} c
    on c.campaign_name = trim(cl."CampaignName") and c.start_date = cast(cl."StartDate" as date)
    where "CampaignName" is not null and "StartDate" is not null
)
select
    campaign_id,
    daily_date,
    impressions, 
    clicks,
    spend
from cte_distinct_campaign