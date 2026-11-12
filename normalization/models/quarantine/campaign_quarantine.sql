    select
        distinct
        trim("CampaignName") as campaign_name,
        trim("Channel")      as channel,
        cast("StartDate" as date)    as start_date,
        cast("EndDate" as date)      as end_date,
        "Budget"       as budget 
    from {{ source('raw','campaign_log') }}
    where "CampaignName" is  null and "StartDate" is null
