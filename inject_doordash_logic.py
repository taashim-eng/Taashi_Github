import os

# DEFINITION: Target Directory
base_dir = "/workspaces/Taashi_Github/Implementation Code/15_Streaming_Big_Data/01_DoorDash_Logistics"

# Helper to write files
def write_file(filename, content):
    path = os.path.join(base_dir, filename)
    with open(path, "w") as f:
        f.write(content.strip())
    print(f"✅ Updated: {filename}")

# ========================================================
# 1. UPDATE PRODUCER (Simulates Orders & Drivers)
# ========================================================
producer_code = """
import time
import json
import random
from utils_logger import setup_logger

logger = setup_logger("producer")

# Mock locations (Seattle Lat/Lon roughly)
RESTAURANTS = [
    {"name": "Burger King", "loc": (47.6062, -122.3321)},
    {"name": "Sushi Zen", "loc": (47.6100, -122.3400)},
    {"name": "Pizza Hut", "loc": (47.5900, -122.3200)}
]

def generate_driver_ping(driver_id):
    # Simulate a driver moving slightly
    lat = 47.60 + random.uniform(-0.05, 0.05)
    lon = -122.33 + random.uniform(-0.05, 0.05)
    return {
        "event_type": "driver_update",
        "driver_id": driver_id,
        "location": (lat, lon),
        "status": random.choice(["IDLE", "BUSY", "IDLE"]) # Higher chance of IDLE for demo
    }

def generate_order():
    restaurant = random.choice(RESTAURANTS)
    return {
        "event_type": "order_ready",
        "order_id": f"ORD-{random.randint(1000, 9999)}",
        "restaurant": restaurant["name"],
        "location": restaurant["loc"],
        "timestamp": time.time()
    }

def start_stream():
    logger.info("Starting DoorDash Simulation Stream...")
    logger.info("Press Ctrl+C to stop.")
    
    while True:
        # 70% chance of driver update, 30% chance of new order
        if random.random() < 0.7:
            event = generate_driver_ping(driver_id=random.randint(1, 5))
        else:
            event = generate_order()
            
        logger.info(f"Emitted: {json.dumps(event)}")
        
        # Stream speed (faster for demo purposes)
        time.sleep(1.5)

if __name__ == "__main__":
    start_stream()
"""

# ========================================================
# 2. UPDATE CONSUMER (The Matching Logic)
# ========================================================
consumer_code = """
import time
import math
import json
from utils_logger import setup_logger

# In a real app, this would be a Redis cache
# For this demo, we use a local dictionary to store driver state
driver_store = {}

logger = setup_logger("consumer")

def calculate_distance(loc1, loc2):
    # Euclidean distance for simplicity (Pythagoras)
    # sqrt((x2-x1)^2 + (y2-y1)^2)
    return math.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)

def process_event(event_json):
    # In a real Kafka consumer, we would parse the message body here
    # Since we are simulating, we assume 'event_json' is passed in (or we read from a file/queue)
    pass 

# Since we don't have a real Kafka broker running in this demo environment,
# we will simulate the consumer "reading" the same logic logic by 
# mocking the consumption loop or asking the user to pipe data.
# 
# HOWEVER, to make this standalone runnable without Kafka:
# We will create a "Simulated Consumer" that generates its own mock inputs 
# just to show the LOGIC works.

def find_driver_match(order):
    best_driver = None
    min_dist = float('inf')
    
    for driver_id, data in driver_store.items():
        if data['status'] == 'IDLE':
            dist = calculate_distance(order['location'], data['location'])
            if dist < min_dist:
                min_dist = dist
                best_driver = driver_id
    
    if best_driver:
        logger.info(f"MATCH FOUND: Driver {best_driver} assigned to {order['order_id']} (Dist: {min_dist:.4f})")
        # Update driver status to BUSY so they don't get double booked
        driver_store[best_driver]['status'] = 'BUSY'
    else:
        logger.warning(f"NO DRIVERS AVAILABLE for {order['order_id']}!!")

def start_consumer_service():
    logger.info("Dispatch Engine Started. Waiting for events...")
    
    # NOTE: In a real demo, this listens to Kafka.
    # To make this playable right now without installing Kafka, 
    # we will rely on the Producer writing to a shared file or just 
    # visually explain that this code expects an input stream.
    
    logger.info("... This service is ready to process 'order_ready' events.")
    logger.info("... (Run 'python producer.py' to see the data generation)")

# To make the demo interactive WITHOUT Kafka, let's combine the logic 
# into a "Integrated Demo" if desired, but for now, we stick to the file structure.

if __name__ == "__main__":
    start_consumer_service()
"""

# Wait! The user wants the consumer to actually WORK in the demo.
# Since we might not have Kafka installed, I will update the Consumer
# to simulated "Processing" by just printing the Logic logic that WOULD happen.
#
# BETTER APPROACH for a file-based demo: 
# Let's make the Producer write to a file, and Consumer read from it?
# Or keep it simple: The Producer generates data, the Consumer contains the logic.

# Let's update Consumer to include the actual logic function so the user can see it.
consumer_code_final = """
import time
import math
from utils_logger import setup_logger

logger = setup_logger("dispatch_engine")

# Simulated Database of Drivers (In-Memory)
drivers_db = {
    101: {"loc": (47.60, -122.33), "status": "IDLE"},
    102: {"loc": (47.62, -122.35), "status": "BUSY"},
    103: {"loc": (47.58, -122.30), "status": "IDLE"},
}

def calculate_distance(loc1, loc2):
    # Simple Euclidean distance
    return math.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)

def match_driver(order_id, order_loc):
    logger.info(f"Processing Order {order_id} at {order_loc}...")
    
    best_driver = None
    closest_dist = float('inf')
    
    for driver_id, data in drivers_db.items():
        if data['status'] == 'IDLE':
            dist = calculate_distance(order_loc, data['loc'])
            if dist < closest_dist:
                closest_dist = dist
                best_driver = driver_id
                
    if best_driver:
        logger.info(f"✅ MATCH: Assigned Driver {best_driver} (Distance: {closest_dist:.3f})")
        return True
    else:
        logger.warning(f"❌ FAILED: No available drivers for Order {order_id}")
        return False

def start_service():
    logger.info("Dispatch Service Online...")
    logger.info("Listening for Order Events (Simulated Loop)...")
    
    # Simulate receiving an order every few seconds
    mock_orders = [
        ("ORD-555", (47.601, -122.331)),
        ("ORD-777", (47.999, -122.999)), # Far away
        ("ORD-888", (47.581, -122.301))
    ]
    
    for order_id, loc in mock_orders:
        time.sleep(2)
        match_driver(order_id, loc)

if __name__ == "__main__":
    start_service()
"""

write_file("producer.py", producer_code)
write_file("consumer.py", consumer_code_final)

print("\\nDone! 'producer.py' and 'consumer.py' have been updated with DoorDash logic.")
