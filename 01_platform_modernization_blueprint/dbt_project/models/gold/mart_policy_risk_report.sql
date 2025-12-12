-- models/gold/mart_policy_risk_report.sql
-- Goal: Pre-compute complex aggregations for PowerBI/Superset to query fast.

with claims as (
    select * from {{ ref('dim_claims_cleaned') }}
),
policies as (
    select * from {{ ref('raw_policies') }} 
)

select 
    p.policy_type,
    count(distinct p.policy_id) as total_policies,
    count(distinct c.claim_id) as total_claims,
    
    -- RISK METRIC: Claims per Policy Ratio
    -- specific logic: handle division by zero
    cast(count(distinct c.claim_id) as float) / nullif(count(distinct p.policy_id),0) as claim_frequency,
    
    sum(c.claim_amount) as total_loss_amount,
    avg(c.claim_amount) as average_claim_cost

from policies p
left join claims c on p.policy_id = c.policy_id
group by 1
order by total_loss_amount desc