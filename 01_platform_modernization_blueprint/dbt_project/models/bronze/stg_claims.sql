-- models/bronze/stg_claims.sql
-- Goal: Lightest transformation possible. Just type casting and renaming.
-- Note: We assume 'raw_claims' is loaded via 'dbt seed' or exists in the warehouse.

with raw_source as (
    select * from {{ ref('raw_claims') }} 
)

select
    claim_id,
    policy_id,
    -- Cast amounts to correct numeric types for financial math
    cast(claim_amount as decimal(18,2)) as claim_amount,
    cast(incident_date as date) as incident_date,
    -- Keep status raw for now, clean it in Silver
    status as raw_status,
    -- Add ingestion metadata (crucial for auditing)
    current_timestamp as ingestion_time
from raw_source