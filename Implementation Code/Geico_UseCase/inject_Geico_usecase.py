
"""
dbt Project Setup Script for GEICO Modernization Demo
Creates a complete dbt project structure with Bronze/Silver/Gold medallion architecture
"""

import os

# --- Configuration ---
BASE_DBT_PATH = "01_platform_modernization_blueprint/dbt_project"

# --- File Contents ---

# 1. dbt_project.yml
dbt_project_yml = """
name: 'geico_modernization_demo'
version: '1.0.0'
config-version: 2

profile: 'default'

model-paths: ["models"]
seed-paths: ["seeds"]
test-paths: ["tests"]
analysis-paths: ["analysis"]
macro-paths: ["macros"]

target-path: "target"
clean-targets: ["target", "dbt_packages"]

models:
  geico_modernization_demo:
    # Materialization Strategy:
    # Bronze is ephemeral (views) for speed.
    # Silver is tables (cleansed storage).
    # Gold is tables (optimized for BI).
    bronze:
      +materialized: view
    silver:
      +materialized: table
    gold:
      +materialized: table
"""

# 2. Bronze Model (stg_claims.sql)
stg_claims_sql = """
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
"""

# 3. Silver Model (dim_claims_cleaned.sql)
dim_claims_cleaned_sql = """
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
"""

# 4. Gold Model (mart_policy_risk_report.sql)
mart_policy_risk_report_sql = """
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
"""

# 5. README.md
readme_md = """
# 🛡️ Project Polaris: Insurance Data Platform Modernization

**Role Simulation:** Senior Data Engineer (Analytics)  
**Tech Stack:** Python, SQL, dbt Core, Spark (simulated), Medallion Architecture

---

## 🚩 1. Problem Statement
The legacy data system at GEICO suffers from **"The Dirty Lake"** problem:
1.  **Duplicate Data:** Real-time ingestion pipelines often re-send claim events, causing duplicate records in reports.
2.  **Inconsistent formatting:** `status` fields are mixed case ('Open', 'OPEN', 'open'), breaking BI filters.
3.  **Slow Reporting:** Analysts are querying raw log files, leading to hour-long wait times for basic risk reports.

## 🛠️ 2. The Solution Architecture
We implemented a **Medallion Architecture (Bronze/Silver/Gold)** using **dbt** to modularize transformations and ensure data quality.

```mermaid
graph TD
    subgraph "Raw Ingestion (Bronze)"
        A[CSV / Kafka Stream] --> B(stg_claims)
        A --> C(stg_policies)
    end
    
    subgraph "Conformed & Cleaned (Silver)"
        B --> D{Deduplication Logic}
        D --> E[dim_claims_cleaned]
        C --> F[dim_policies]
    end
    
    subgraph "Business Aggregates (Gold)"
        E --> G[mart_policy_risk_report]
        F --> G
    end

    G --> H((PowerBI / Superset))
```

## 🚀 3. Technical Highlights (How to Demo)

### A. Handling Duplicates (The "Idempotency" Fix)
In `models/silver/dim_claims_cleaned.sql`, we utilize Window Functions (ROW_NUMBER()) to handle the "At-Least-Once" delivery guarantee of distributed systems (like Kafka).

```sql
row_number() over (partition by claim_id order by ingestion_time desc)
```

This ensures that even if the pipeline runs twice, the downstream report only counts the claim once.

### B. Standardization
We moved cleaning logic upstream to the Silver layer.

- **Before:** investigation, PENDING, Pending
- **After:** INVESTIGATION, PENDING

**Impact:** Zero-downtime reporting. The dashboard no longer breaks when a new casing format is introduced.

## 🏃 4. How to Run This Project
1. **Generate Data:** Run the python data generation script.
2. **Setup Seeds:** Copy the generated CSVs from `data/` to `dbt_project/seeds/`.
3. **Load Seeds:** `dbt seed`
4. **Run Pipeline:** `dbt run`
5. **Test Quality:** `dbt test` (Checks for uniqueness and referential integrity)

This blueprint demonstrates the shift from Legacy ETL to Modern Analytics Engineering.
"""


# --- Execution Functions ---

def create_file(path, content):
    """
    Helper to write content to a file, creating directories if needed.
    
    Args:
        path (str): File path to create
        content (str): Content to write to the file
    """
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"✅ Created: {path}")


def main():
    """
    Main execution function that creates the dbt project structure.
    Creates all necessary files and directories for the GEICO modernization demo.
    """
    print("🚀 Injecting dbt code and documentation...")
    
    # Define file mappings
    files_to_create = {
        f"{BASE_DBT_PATH}/dbt_project.yml": dbt_project_yml,
        f"{BASE_DBT_PATH}/models/bronze/stg_claims.sql": stg_claims_sql,
        f"{BASE_DBT_PATH}/models/silver/dim_claims_cleaned.sql": dim_claims_cleaned_sql,
        f"{BASE_DBT_PATH}/models/gold/mart_policy_risk_report.sql": mart_policy_risk_report_sql,
        f"{BASE_DBT_PATH}/README.md": readme_md
    }
    
    # Write files
    for file_path, content in files_to_create.items():
        create_file(file_path, content)
    
    print("\n🎉 Injection complete. Your dbt project structure is ready.")


if __name__ == "__main__":
    main()