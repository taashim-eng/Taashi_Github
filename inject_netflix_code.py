import os

# DEFINITION: Target Directory
base_dir = "/workspaces/Taashi_Github/Implementation Code/15_Streaming_Big_Data/03_Netflix_Keystone"

# Helper to write files
def write_file(filename, content):
    os.makedirs(base_dir, exist_ok=True)
    path = os.path.join(base_dir, filename)
    with open(path, "w") as f:
        f.write(content.strip())
    print(f"✅ Created/Updated: {filename}")

# ========================================================
# 1. CREATE PRODUCER (Simulates Client Devices)
# ========================================================
producer_code = """
import time
import json
import random
from utils_logger import setup_logger

logger = setup_logger("keystone_edge_producer")

# Mock Catalog
SHOWS = ["Stranger Things", "The Crown", "Squid Game", "Black Mirror"]
USERS = [f"user_{i}" for i in range(1001, 1010)]

def generate_event():
    user = random.choice(USERS)
    show = random.choice(SHOWS)
    
    # Event Probability Distribution
    # 5% Start, 5% Stop, 80% Heartbeat (Playing), 10% Error/Buffer
    rand = random.random()
    
    if rand < 0.05:
        event_type = "session_start"
    elif rand < 0.10:
        event_type = "session_end"
    elif rand < 0.20:
        event_type = "buffering_start"
    else:
        event_type = "playback_heartbeat"

    return {
        "event_type": event_type,
        "user_id": user,
        "title": show,
        "device": random.choice(["SmartTV", "Mobile", "Web"]),
        "timestamp_ms": int(time.time() * 1000),
        "bitrate_kbps": random.choice([4000, 5800, 12000]) if event_type == "playback_heartbeat" else 0
    }

def start_streaming():
    logger.info("Starting Netflix Keystone Simulation...")
    logger.info("Emitting telemetry from client devices...")
    
    while True:
        # Simulate high volume by generating batch events
        events = [generate_event() for _ in range(random.randint(1, 5))]
        
        for event in events:
            logger.info(f"📡 Ingest: {json.dumps(event)}")
            time.sleep(0.2) # Fast stream

if __name__ == "__main__":
    start_streaming()
"""

# ========================================================
# 2. CREATE CONSUMER (Keystone Aggregator / Analytics)
# ========================================================
consumer_code = """
import time
import json
from utils_logger import setup_logger

logger = setup_logger("keystone_aggregator")

# In-Memory Session Store (The "State" of the Stream)
active_sessions = {}

def process_event(event):
    uid = event["user_id"]
    e_type = event["event_type"]
    title = event["title"]
    
    # 1. Handle New Sessions
    if e_type == "session_start":
        active_sessions[uid] = {
            "title": title, 
            "start_time": event["timestamp_ms"],
            "buffer_count": 0
        }
        logger.info(f"▶️  START: {uid} began watching '{title}'")

    # 2. Handle Buffering (QoE Detection)
    elif e_type == "buffering_start":
        if uid in active_sessions:
            active_sessions[uid]["buffer_count"] += 1
            count = active_sessions[uid]["buffer_count"]
            logger.warning(f"⚠️  BUFFERING: {uid} experiencing lag on '{title}' (Count: {count})")
            
            # Simple Logic: If buffer > 3 times, flag as Critical Issue
            if count >= 3:
                logger.error(f"🚨 CRITICAL QoE ALERT: {uid} has poor connection. Downgrade bitrate requested.")

    # 3. Handle Heartbeats (View Duration)
    elif e_type == "playback_heartbeat":
        pass # In a real system, we accumulate "seconds watched" here

    # 4. Handle Stop (Session Finalization)
    elif e_type == "session_end":
        if uid in active_sessions:
            session = active_sessions.pop(uid)
            duration_sec = (event["timestamp_ms"] - session["start_time"]) / 1000
            logger.info(f"⏹️  STOP: {uid} finished '{session['title']}'. Total Duration: {duration_sec:.1f}s")

def start_consumer():
    logger.info("Keystone Processing Engine Started...")
    logger.info("Aggregating viewing sessions in real-time...")
    
    # Simulation Loop
    # In reality, this loop consumes from Kafka
    logger.info("... Listening for telemetry events ...")
    
    # Mock sequence to demonstrate logic
    mock_sequence = [
        {"event_type": "session_start", "user_id": "u1", "title": "Stranger Things", "timestamp_ms": 1000},
        {"event_type": "playback_heartbeat", "user_id": "u1", "title": "Stranger Things", "timestamp_ms": 2000},
        {"event_type": "buffering_start", "user_id": "u1", "title": "Stranger Things", "timestamp_ms": 3000},
        {"event_type": "buffering_start", "user_id": "u1", "title": "Stranger Things", "timestamp_ms": 4000},
        {"event_type": "buffering_start", "user_id": "u1", "title": "Stranger Things", "timestamp_ms": 5000}, # Should trigger ALERT
        {"event_type": "session_end", "user_id": "u1", "title": "Stranger Things", "timestamp_ms": 8000}
    ]
    
    for evt in mock_sequence:
        time.sleep(1.0)
        process_event(evt)

if __name__ == "__main__":
    start_consumer()
"""

# ========================================================
# 3. UTILS & REQUIREMENTS
# ========================================================
logger_code = """
import logging
import sys

def setup_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        # Using a shorter format for high-volume logs
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
"""

write_file("producer.py", producer_code)
write_file("consumer.py", consumer_code)
write_file("utils_logger.py", logger_code)
write_file("requirements.txt", "pandas\nnumpy\npython-dotenv")
write_file(".env", "KAFKA_BOOTSTRAP=localhost:9092\nENV=DEV")

print("\\n✅ Netflix Keystone simulation code injected successfully.")