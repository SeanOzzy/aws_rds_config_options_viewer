import boto3
from config.constants import excluded_engines, supported_engines_cache_name, supported_db_classes_cache_name
import datetime
import utils.cache as cache
from utils.logger import logger
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
import os

# Define a function to fetch the list of supported RDS engines, filter out non-core engines (defined in constants.py) and return a list
def get_supported_engines(region=None):
    RDS_REGION = os.environ.get("RDS_REGION")
    client = boto3.client('rds', region_name=os.environ.get("RDS_REGION"))
    cache_key = supported_engines_cache_name

    cached_data = cache.get_from_cache(cache_key)
    if cached_data:
        # Write information to logger
        logger.info(f"Found valid cached data for {len(cached_data)} DB engines in region {RDS_REGION}")
        # print(f"INFO: Found valid cached data for {len(cached_data)} DB engines in region {RDS_REGION}")
        return cached_data
    # print(f"DEBUG: client in get_supported_engines function: {region_name}")
    paginated_response = client.get_paginator('describe_db_engine_versions')
    # Use logger to log some basic information
    logger.warning(f"Cached data expired or not found, populating cache for all supported RDS engines in {RDS_REGION}")
    logger.info(f"HINT: This may take a few minutes depending on the number of supported engines in the region...")
    # print(f"WARN: Cached data expired or not found, populating cache for all supported RDS engines in {RDS_REGION}")
    # print(f"HINT: This may take a few minutes depending on the number of supported engines in the region...")

    # Fetch the list of supported RDS engines and filter out non-core engines (defined in constants.py)
    engine_options = []
    for page in paginated_response.paginate():
        for option in page['DBEngineVersions']:
            if option['Engine'] not in excluded_engines:
                engine_options.append(option['Engine'])
    engine_options = sorted(set(engine_options))
    # Save the list of engines to cache
    cache.save_to_cache(cache_key, engine_options)
    return engine_options

# Define a function to fetch the list of supported DB instance classes for a given engine and return a sorted list
def fetch_db_instance_classes_for_engine(engine_option):
    client = boto3.client('rds', region_name=os.environ.get("RDS_REGION"))
    db_instance_class_options = set()
    try:
        # print("DEBUG: client in fetch_db_instance_classes_for_engine function: {region_name}")
        paginated_response = client.get_paginator('describe_orderable_db_instance_options')
        for page in paginated_response.paginate(Engine=engine_option):
            for option in page['OrderableDBInstanceOptions']:
                db_instance_class_options.add(option['DBInstanceClass'])
    except Exception as exc:
        # Write information to logger
        logger.error(f"ERROR: Could not fetch data for engine {engine_option} - {str(exc)}")
        logger.info(f"INFO: Trying again for engine {engine_option}...")
        # print(f"ERROR: Could not fetch data for engine {engine_option} - {str(exc)}")
        # print(f"INFO: Trying again for engine {engine_option}...")
    return db_instance_class_options

# Call the function to fetch the list of supported DB instance classes for a given engine in parallel and return a sorted list
def get_supported_db_classes(engine_options):
    RDS_REGION = os.environ.get("RDS_REGION")
    cache_key = supported_db_classes_cache_name
    # Read the list of supported DB instance classes from cache
    cached_data = cache.get_from_cache(cache_key)
    if cached_data:
        # Write information to logger
        logger.info(f"Found valid cached data for {len(cached_data)} DB instance types in region {RDS_REGION}")
        # print(f"INFO: Found valid cached data for {len(cached_data)} DB instance types in region {RDS_REGION}")
        return cached_data
    
    get_supported_db_classes_start_time = datetime.datetime.now()
    # Write information to logger
    logger.warning(f"Cached data expired or not found, populating DB instance classes for {engine_options} in region {RDS_REGION}")
    logger.info(f"HINT: This may take a few minutes depending on the number of supported instances in the region...")
    print(f"WARN: Cached data expired or not found, populating DB instance classes for {engine_options} in region {RDS_REGION}")
    print(f"HINT: Please be patient. This may take a few minutes depending on the number of supported instances in the region, consult log file for further information...")
    db_instance_class_options = set()
    
    with ThreadPoolExecutor() as executor:
        future_to_engine = {executor.submit(fetch_db_instance_classes_for_engine, engine): engine for engine in engine_options}
        for future in futures.as_completed(future_to_engine):
            engine = future_to_engine[future]
            try:
                db_instance_class_options.update(future.result())
            except Exception as exc:
                # Write information to logger
                logger.error(f"Could not fetch data for engine {engine} - {str(exc)}")
                # print(f"ERROR: Could not fetch data for engine {engine} - {str(exc)}")

    db_instance_class_options = sorted(db_instance_class_options)
    contruct_db_instance_class_end_time = datetime.datetime.now()
    total_construct_db_instance_class_time = contruct_db_instance_class_end_time - get_supported_db_classes_start_time
    # Write information to logger
    logger.info(f"INFO: DB Instance Class Search completed in: {total_construct_db_instance_class_time} (format HH:MM:SS.MS))")
    # print(f"INFO: DB Instance Class Search completed in: {total_construct_db_instance_class_time} (format HH:MM:SS.MS))")
    cache.save_to_cache(cache_key, db_instance_class_options)
    # Write information to logger
    logger.info(f"Found {len(db_instance_class_options)} supported DB instance classes in region {RDS_REGION} for {engine_options} \n")
    # print(f"INFO: Found {len(db_instance_class_options)} supported DB instance classes in region {RDS_REGION} for {engine_options} \n")
    # Save the list of DB instance classes to cache for performance reasons, 
    # looking up the list of DB instance classes for each engine takes between 2-4 minutes
    # cache.save_to_cache(cache_key, db_instance_class_options)
    return db_instance_class_options
