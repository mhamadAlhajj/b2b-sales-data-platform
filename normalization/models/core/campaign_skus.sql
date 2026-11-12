with cte_campaign as (
select 
    campaign_id,
    TRIM(UNNEST(STRING_TO_ARRAY("PromotedSKUs", ','))) AS promoted_skus
from {{source('raw','campaign_skus')}} cs 
inner join {{ref('campaign')}} c 
on c.campaign_name = trim(cs."CampaignName")
)

select * from cte_campaign
where promoted_skus <> '' and promoted_skus <> ' '