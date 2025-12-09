import os

def create_project_structure(project_name):
    """
    Creates a folder structure and template files for a streaming big data project.
    """
    
    # Define the project root
    base_dir = os.path.join(os.getcwd(), project_name)
    
    # Helper function to write files safely
    def write_file(path, content):
        # Ensure the directory for the file exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(content.strip())
        print(f"Created: {path}")

    # Create the base project directory
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        print(f"Created directory: {base_dir}")

    # ---------------------------------------------------------
    # 1. Create Producer Code (producer.py)
    # ---------------------------------------------------------
    write_file(f"{base_dir}/producer.py", """
import time
import json
import random
from utils_logger import setup_logger

logger = setup_logger("producer")

def generate_data():
    logger.info("Starting Data Producer...")
    while True:
        data = {
            "id": random.randint(1, 1000),
            "value": round(random.random() * 100, 2),
            "timestamp": time.time()
        }
        # Log the data generation instead of just printing
        logger.info(f"Generated event: {json.dumps(data)}")
        time.sleep(1)

if __name__ == "__main__":
    generate_data()
""")

    # ---------------------------------------------------------
    # 2. Create Consumer Code (consumer.py)
    # ---------------------------------------------------------
    write_file(f"{base_dir}/consumer.py", """
import time
from utils_logger import setup_logger

logger = setup_logger("consumer")

def consume_data():
    logger.info("Starting Consumer Service...")
    while True:
        # Placeholder for consumption logic
        logger.info("Waiting for incoming stream data...")
        time.sleep(2)

if __name__ == "__main__":
    consume_data()
""")

    # ---------------------------------------------------------
    # 3. Create Logger Utility (utils_logger.py)
    # ---------------------------------------------------------
    write_file(f"{base_dir}/utils_logger.py", """
import logging
import sys

def setup_logger(name):
    \"\"\"
    Sets up a logger that writes to the console with a specific format.
    \"\"\"
    logger = logging.getLogger(name)
    
    # Only add handler if not already added to avoid duplicate logs
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
        
    return logger
""")

    # ---------------------------------------------------------
    # 4. Create Environment Config (.env)
    # ---------------------------------------------------------
    write_file(f"{base_dir}/.env", """
# Configuration Secrets
# DO NOT COMMIT THIS FILE TO GITHUB

KAFKA_BOOTSTRAP_SERVERS=localhost:9092
DB_HOST=localhost
DB_USER=admin
DB_PASSWORD=secret_password
API_KEY=12345-abcde
""")

    # ---------------------------------------------------------
    # 5. Create Git Ignore (.gitignore)
    # ---------------------------------------------------------
    write_file(f"{base_dir}/.gitignore", """
# Ignore Python build files
__pycache__/
*.py[cod]

# Ignore Environment Variables (Security Risk)
.env
.env.local

# Ignore OS files
.DS_Store
""")

    # ---------------------------------------------------------
    # 6. Create Requirements (requirements.txt)
    # ---------------------------------------------------------
    write_file(f"{base_dir}/requirements.txt", """
pandas
numpy
python-dotenv
""")

    # ---------------------------------------------------------
    # 7. Create README.md
    # ---------------------------------------------------------
    write_file(f"{base_dir}/README.md", """
# Big Data Streaming Project

## Overview
This project contains a basic setup for a streaming pipeline with logging and configuration management.

## Structure
- `producer.py`: Generates mock data streams using a shared logger.
- `consumer.py`: Consumes and processes the data using a shared logger.
- `utils_logger.py`: Centralized logging configuration.
- `.env`: (Not verified) Stores secret variables like API keys.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Create your `.env` file (if not present) based on the template.

## Execution
Run the producer:
```bash
python producer.py

""")

print(f"\nSuccessfully generated project 'Streaming_Bigdata_code' with logging and env config!")