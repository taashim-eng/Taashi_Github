import os

# DEFINITION: Target Directory
base_dir = "/workspaces/Taashi_Github/Implementation Code/15_Streaming_Big_Data/02_Uber_CDC_Mesh"

# Helper to write files
def write_file(filename, content):
    # Ensure folder exists
    os.makedirs(base_dir, exist_ok=True)
    
    path = os.path.join(base_dir, filename)
    with open(path, "w") as f:
        f.write(content.strip())
    print(f"✅ Created/Updated: {filename}")

# ========================================================
# 1. CREATE PRODUCER (Simulates Postgres WAL / Debezium)
# ========================================================
producer_code = """
import time
import json
import random
from utils_logger import setup_logger

logger = setup_logger("cdc_producer")

# Mock Database Table: Drivers
# We simulate a "Write-Ahead Log" (WAL) stream
DRIVER_IDS = [101, 102, 103, 104, 105]

def generate_wal_event():
    driver_id = random.choice(DRIVER_IDS)
    
    # 60% chance of a Trip Update (Ride completed)
    # 30% chance of a Rating Change
    # 10% chance of a New Driver Signup (Insert)
    rand_val = random.random()
    
    if rand_val < 0.6:
        # UPDATE operation: Trip Completed
        return {
            "op": "u", # 'u' for Update
            "table": "trips_ledger",
            "ts_ms": int(time.time() * 1000),
            "before": None, 
            "after": {
                "driver_id": driver_id,
                "trips_today": random.randint(1, 20),
                "earnings": round(random.uniform(20.0, 500.0), 2)
            }
        }
    elif rand_val < 0.9:
        # UPDATE operation: Rating Change
        return {
            "op": "u",
            "table": "driver_profiles",
            "ts_ms": int(time.time() * 1000),
            "after": {
                "driver_id": driver_id,
                "rating": round(random.uniform(4.2, 5.0), 2)
            }
        }
    else:
        # CREATE operation: New Driver
        new_id = random.randint(200, 999)
        return {
            "op": "c", # 'c' for Create
            "table": "driver_profiles",
            "ts_ms": int(time.time() * 1000),
            "after": {
                "driver_id": new_id,
                "name": "New Driver",
                "status": "onboarding"
            }
        }

def start_cdc_stream():
    logger.info("Starting Postgres CDC Simulator (Debezium Style)...")
    logger.info("Streaming database changes to 'cdc-events' topic...")
    
    while True:
        event = generate_wal_event()
        # Log it like a database change event
        logger.info(f"CDC Event: {json.dumps(event)}")
        time.sleep(1)

if __name__ == "__main__":
    start_cdc_stream()
"""

# ========================================================
# 2. CREATE CONSUMER (The Data Mesh / Microservice)
# ========================================================
consumer_code = """
import time
import json
from utils_logger import setup_logger

logger = setup_logger("incentive_service")

# Local State Store (The "Mesh" Node)
# This service maintains its OWN copy of driver stats for calculating bonuses
driver_stats_cache = {}

def process_change_event(event):
    op_type = event.get("op")
    table = event.get("table")
    data = event.get("after")
    
    if not data: 
        return

    driver_id = data.get("driver_id")
    
    # Initialize cache if new driver
    if driver_id not in driver_stats_cache:
        driver_stats_cache[driver_id] = {"trips": 0, "rating": 5.0, "bonus_eligible": False}

    # LOGIC: Update local state based on DB change
    if table == "trips_ledger" and op_type == "u":
        driver_stats_cache[driver_id]["trips"] = data["trips_today"]
        logger.info(f"🔄 Syncing Trip Data: Driver {driver_id} has {data['trips_today']} trips.")
        
    elif table == "driver_profiles":
        if "rating" in data:
            driver_stats_cache[driver_id]["rating"] = data["rating"]
            logger.info(f"⭐ Rating Update: Driver {driver_id} is now {data['rating']}")

    # LOGIC: Check Business Rule (Real-time Incentive)
    # If trips > 15 AND rating > 4.8, unlock bonus
    stats = driver_stats_cache[driver_id]
    if stats["trips"] >= 15 and stats["rating"] >= 4.8:
        if not stats["bonus_eligible"]:
            logger.info(f"💰 BONUS UNLOCKED: Driver {driver_id} hit the daily target!")
            stats["bonus_eligible"] = True
            
def start_mesh_consumer():
    logger.info("Incentive Service (Mesh Node) Started...")
    logger.info("Listening for CDC events from Main Database...")
    
    # Simulation: We will generate events locally to verify the logic
    # In prod, this reads from Kafka
    logger.info("... Waiting for DB changes...")
    
    # Mock loop to show it working if run directly
    mock_events = [
        {"op": "c", "table": "driver_profiles", "after": {"driver_id": 99, "rating": 5.0}},
        {"op": "u", "table": "trips_ledger", "after": {"driver_id": 99, "trips_today": 10}},
        {"op": "u", "table": "trips_ledger", "after": {"driver_id": 99, "trips_today": 16}}, # Should trigger bonus
    ]
    
    for event in mock_events:
        time.sleep(1.5)
        process_change_event(event)

if __name__ == "__main__":
    start_mesh_consumer()
"""

# ========================================================
# 3. CREATE UTILS (Logger) & CONFIG
# ========================================================
logger_code = """
import logging
import sys

def setup_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
"""

requirements_code = """
pandas
numpy
python-dotenv
"""

write_file("producer.py", producer_code)
write_file("consumer.py", consumer_code)
write_file("utils_logger.py", logger_code)
write_file("requirements.txt", requirements_code)
write_file(".env", "DB_HOST=localhost\nKAFKA_BROKER=localhost:9092")

print("\\n✅ Uber CDC Mesh Logic successfully injected.")