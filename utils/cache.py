"""
This module contains functions to save and retrieve data from a cache file.
The cache file is a JSON file stored in the cache directory defined in config/constants.py.
The cache file contains a dictionary with the region as the key and the data as the value.
This allows the application to store data for multiple regions in a single cache file whilst only fetching data for the selected region.
"""
import config.constants as constants
from utils.logger import logger
import json
import os
from datetime import datetime, timedelta

CACHE_DIR = constants.cache_dir
CACHE_VALIDITY_DAYS = constants.cache_expiry_days

# This function looks for a valid cache file for the selected region in the cache directory
# If found it returns the data from the cache file
def get_from_cache(cache_key):
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")
    
    if os.path.exists(cache_file):
        file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
        if datetime.now() - file_mtime < timedelta(days=CACHE_VALIDITY_DAYS):
            try:
                with open(cache_file, 'r') as file:
                    data = json.load(file)
                    region = os.environ.get('RDS_REGION', 'default_region')
                    return data.get(region, None)
            except Exception as e:
                logger.error(f"Could not read from cache: {e}")
                # print(f"Could not read from cache: {e}")
                os.remove(cache_file)  # Optionally delete corrupted/invalid cache file
    return None

# This function saves the data to a cache file in the cache directory for the selected region
def save_to_cache(cache_key, data):
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")
    
    current_data = {}
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as file:
            current_data = json.load(file)

    region = os.environ.get('RDS_REGION', 'default_region')
    current_data[region] = data

    try:
        with open(cache_file, 'w') as file:
            json.dump(current_data, file)
    except Exception as e:
        logger.error(f"Could not save to cache: {e}")
        # print(f"Could not save to cache: {e}")

# This function clears the cache for the selected region
def clear_existing_cache():
    if os.path.exists(CACHE_DIR):
        cache_files = os.listdir(CACHE_DIR)
        print
        for filename in cache_files:
            if filename.endswith(".json"):
                cache_file = os.path.join(CACHE_DIR, f"{filename}")
                if os.path.exists(cache_file):
                    try:
                        with open(cache_file, 'r') as file:
                            data = json.load(file)
                            region = os.environ.get('RDS_REGION', 'default_region')
                        if region in data:
                            logger.info(f"Clearing existing cache in {CACHE_DIR} for region {region}")
                            # print(f"INFO: Clearing existing cache in {CACHE_DIR} for region {region}")
                            del data[region]
                        with open(cache_file, 'w') as file:
                            json.dump(data, file)
                    except Exception as e:
                        logger.error(f"Could not clear cache: {e}")
                        # print(f"Could not clear cache: {e}")
    else:
        logger.info(f"No existing cache found in {CACHE_DIR}")
        # print(f"INFO: No existing cache found in {CACHE_DIR}")

