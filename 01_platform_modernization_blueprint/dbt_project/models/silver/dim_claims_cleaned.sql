-- models/silver/dim_claims_cleaned.sql
-- Goal: Deduplication, Standardization, and Null Handling.

with bronze_claims as (
    select * from {{ ref('stg_claims') }}
),

-- DEDUPLICATION LOGIC
-- Use Window Function to rank duplicate claim_ids by ingestion time
deduped as (
    select 
        *,
        row_number() over (
            partition by claim_id 
            order by ingestion_time desc
        ) as rn
    from bronze_claims
)

select
    claim_id,
    policy_id,
    claim_amount,
    incident_date,
    -- STANDARDIZATION: Normalize status to Uppercase
    upper(trim(raw_status)) as status_normalized,
    ingestion_time
from deduped
where rn = 1 -- Filter out older duplicates