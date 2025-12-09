import os

# DEFINITION: Target Directory
base_dir = "/workspaces/Taashi_Github/Implementation Code/15_Streaming_Big_Data/05_X_Stream_Filtering"

# Helper to write files
def write_file(filename, content):
    os.makedirs(base_dir, exist_ok=True)
    path = os.path.join(base_dir, filename)
    with open(path, "w") as f:
        f.write(content.strip())
    print(f"✅ Created/Updated: {filename}")

# ========================================================
# 1. CREATE PRODUCER (The Firehose)
# ========================================================
producer_code = """
import time
import json
import random
from utils_logger import setup_logger

logger = setup_logger("firehose_producer")

# Mock Data Sources
TOPICS = ["Politics", "Sports", "K-Pop", "Crypto", "Tech", "Memes", "News"]
HASHTAGS = ["#Bitcoin", "#AI", "#TaylorSwift", "#SuperBowl", "#Python", "#Election2024", "#Cats"]
USERS = [f"@user_{i}" for i in range(1000, 9999)]

def generate_tweet():
    topic = random.choice(TOPICS)
    hashtag = random.choice(HASHTAGS)
    
    # Simulate a tweet structure
    return {
        "id": random.getrandbits(64),
        "user": random.choice(USERS),
        "text": f"Just saw this crazy update about {topic}! {hashtag}",
        "topic": topic,
        "is_verified": random.choice([True, False]),
        "timestamp_ms": int(time.time() * 1000)
    }

def start_firehose():
    logger.info("Starting X (Twitter) Firehose Simulation...")
    logger.info("Warning: High Volume Stream Initiated 🌊")
    
    while True:
        # Generate a burst of tweets to simulate high throughput
        burst_size = random.randint(1, 10)
        
        for _ in range(burst_size):
            tweet = generate_tweet()
            # We log minimal info here because the volume is too high to read
            logger.info(f"Generated Tweet: [{tweet['topic']}] {tweet['text'][:30]}...")
            
        # Very short sleep to simulate 50+ tweets per second
        time.sleep(0.1)

if __name__ == "__main__":
    start_firehose()
"""

# ========================================================
# 2. CREATE CONSUMER (The Filter Service)
# ========================================================
consumer_code = """
import time
import json
from utils_logger import setup_logger

logger = setup_logger("topic_filter_service")

# CONFIGURATION: What we actually care about
INTEREST_KEYWORDS = ["#AI", "#Python", "Tech"]
BLOCKED_USERS = ["@user_1234", "@bot_999"]

def filter_process(tweet):
    # 1. Spam/Block Filter
    if tweet['user'] in BLOCKED_USERS:
        return # Drop silently
    
    # 2. Content Filter (The "Where" Clause)
    # We only want Tech and AI tweets. Everything else is "Noise" to this service.
    
    is_interesting = any(k in tweet['text'] for k in INTEREST_KEYWORDS) or tweet['topic'] == "Tech"
    
    if is_interesting:
        # PROCESSED: This is the data we keep/store/analyze
        logger.info(f"✅ MATCH FOUND: {tweet['user']} says: '{tweet['text']}'")
        # In a real app, we would write this to a specific Kafka topic like 'tech-stream'
    else:
        # IGNORED: This represents data we pay to ingest but discard
        # We log at DEBUG level (or not at all) to save space
        # Here we print a faint message just to show it was checked
        pass 

def start_filter_engine():
    logger.info("Filter Engine Online. Listening for: " + str(INTEREST_KEYWORDS))
    
    # Simulation: We will generate mock data internally to demonstrate the filtering
    # because piping the actual producer output in a simple shell is hard to visualize.
    
    logger.info("... Connecting to Firehose ...")
    
    # Mock loop representing the incoming stream
    mock_data = [
        {"user": "@user_1", "topic": "K-Pop", "text": "I love BTS! #Music"},
        {"user": "@dev_guy", "topic": "Tech", "text": "Learning #Python is awesome for #AI"}, # MATCH
        {"user": "@sports_fan", "topic": "Sports", "text": "Did you see that goal? #Soccer"},
        {"user": "@crypto_bro", "topic": "Crypto", "text": "Bitcoin to the moon! #Bitcoin"},
        {"user": "@ai_researcher", "topic": "Tech", "text": "New LLM models are changing everything #AI"}, # MATCH
    ]
    
    while True:
        for tweet in mock_data:
            time.sleep(1.0) # Slow down for readability
            filter_process(tweet)

if __name__ == "__main__":
    start_filter_engine()
"""

# ========================================================
# 3. UTILS & CONFIG
# ========================================================
logger_code = """
import logging
import sys

def setup_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
"""

write_file("producer.py", producer_code)
write_file("consumer.py", consumer_code)
write_file("utils_logger.py", logger_code)
write_file("requirements.txt", "pandas\npython-dotenv")
write_file(".env", "FILTER_KEYWORDS=AI,Python,Tech")

print("\\n✅ X (Twitter) Filter Logic injected successfully.")