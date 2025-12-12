"""
Insurance Data Generation Script for GEICO Modernization Demo
Generates synthetic customer, policy, and claims data with intentional data quality issues
to demonstrate the need for data cleaning pipelines.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import random

# --- Configuration ---
BASE_PATH = "01_platform_modernization_blueprint/data"
NUM_CUSTOMERS = 100
NUM_POLICIES = 150
NUM_CLAIMS = 300


def generate_data():
    """
    Generate synthetic insurance data with intentional quality issues.
    
    Creates three datasets:
    - Customers: Basic customer information with some NULL values
    - Policies: Insurance policies linked to customers
    - Claims: Claims data with duplicates and inconsistent formatting
    
    Data quality issues injected:
    - NULL values in customer state field
    - Inconsistent casing in claim status ('OPEN' vs 'investigation')
    - Duplicate claims to simulate at-least-once delivery semantics
    """
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # --- 1. Generate Customers (with some messy data) ---
    customer_ids = [f"CUST_{i:04d}" for i in range(1, NUM_CUSTOMERS + 1)]
    states = ['CA', 'TX', 'NY', 'FL', 'WA', None]  # Intentional NULL
    
    customers = pd.DataFrame({
        'customer_id': customer_ids,
        'first_name': [f"Person_{i}" for i in range(NUM_CUSTOMERS)],
        'last_name': [f"Lname_{i}" for i in range(NUM_CUSTOMERS)],
        'state': np.random.choice(states, NUM_CUSTOMERS),
        'email': [f"user_{i}@example.com" for i in range(NUM_CUSTOMERS)],
        'created_at': [
            datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365)) 
            for _ in range(NUM_CUSTOMERS)
        ]
    })
    
    # --- 2. Generate Policies (Many-to-One relationship with Customers) ---
    policy_types = ['AUTO', 'HOME', 'RENTERS']
    
    policies = pd.DataFrame({
        'policy_id': [f"POL_{i:05d}" for i in range(1, NUM_POLICIES + 1)],
        'customer_id': np.random.choice(customer_ids, NUM_POLICIES),
        'policy_type': np.random.choice(policy_types, NUM_POLICIES),
        'start_date': [
            datetime(2023, 1, 1) + timedelta(days=random.randint(0, 300)) 
            for _ in range(NUM_POLICIES)
        ],
        'premium_amount': np.random.randint(500, 3000, NUM_POLICIES)
    })
    
    # --- 3. Generate Claims (The "Fact" Table - intentionally messy!) ---
    # Inconsistent casing in status field to demonstrate data quality issues
    claim_statuses = ['OPEN', 'CLOSED', 'PENDING', 'investigation']
    
    claims = pd.DataFrame({
        'claim_id': [f"CLM_{i:05d}" for i in range(1, NUM_CLAIMS + 1)],
        'policy_id': np.random.choice(policies['policy_id'], NUM_CLAIMS),
        'claim_amount': np.random.uniform(100.0, 50000.0, NUM_CLAIMS).round(2),
        'incident_date': [
            datetime(2023, 6, 1) + timedelta(days=random.randint(0, 150)) 
            for _ in range(NUM_CLAIMS)
        ],
        'status': np.random.choice(claim_statuses, NUM_CLAIMS)
    })
    
    # INJECT NOISE: Create duplicates to simulate "At-Least-Once" delivery
    # This mimics real-world streaming systems like Kafka where messages can be delivered multiple times
    duplicate_claims = claims.sample(20)
    claims = pd.concat([claims, duplicate_claims]).sample(frac=1).reset_index(drop=True)
    
    # --- Save Files ---
    os.makedirs(BASE_PATH, exist_ok=True)
    
    customers.to_csv(f"{BASE_PATH}/raw_customers.csv", index=False)
    policies.to_csv(f"{BASE_PATH}/raw_policies.csv", index=False)
    claims.to_csv(f"{BASE_PATH}/raw_claims.csv", index=False)
    
    print(f"✅ Data generation complete!")
    print(f"   - Customers: {len(customers)} records")
    print(f"   - Policies: {len(policies)} records")
    print(f"   - Claims: {len(claims)} records (includes {len(duplicate_claims)} duplicates)")
    print(f"   - Output directory: {BASE_PATH}")


if __name__ == "__main__":
    generate_data()