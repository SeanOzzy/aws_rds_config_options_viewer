"""
This module contains functions to process the API response and display the results in the treeview.
"""
global api_results
api_results = None
import boto3
from config.constants import api_results_save_file_name, api_results_save_file_type
import csv
from utils.logger import logger
from tkinter import filedialog
import jmespath
import os


# Define a function to construct the JMESPath query
# This function controls which checkboxes are selected and constructs the JMESPath query accordingly
def construct_jmespath_query(checkbox_states, engine, db_instance_class, db_engine_version_entry, **kwargs):
    # print(f"DEBUG: engine_version in construct_jmespath_query function: {engine_version}")
    engine_version = db_engine_version_entry
    # print(f"DEBUG: engine_version in construct_jmespath_query function after db_engine_version_entry.get(): {engine_version}")
    query_parts = []
    if engine_version:
        query_parts.append("EngineVersion == '{}'".format(engine_version))
    if checkbox_states['multi_az']:
        query_parts.append('MultiAZCapable == `true`')
    if checkbox_states['supports_clusters']:
        query_parts.append('SupportsClusters == `true`')
    if checkbox_states['supports_performance_insights']:
        query_parts.append('SupportsPerformanceInsights == `true`')
    if checkbox_states['supports_enhanced_monitoring']:
        query_parts.append('SupportsEnhancedMonitoring == `true`')
    if checkbox_states['storage_encyption']:
        query_parts.append('SupportsStorageEncryption == `true`')
    if checkbox_states['iam_authentication']:
        query_parts.append('SupportsIAMDatabaseAuthentication == `true`')
    if checkbox_states['kerberos_authentication']:
        query_parts.append('SupportsKerberosAuthentication == `true`')
    if checkbox_states['global_database']:
        query_parts.append('SupportsGlobalDatabases == `true`')
    if checkbox_states['gp2_storage']:
        query_parts.append('StorageType == `gp2`')
    if checkbox_states['gp3_storage']:
        query_parts.append('StorageType == `gp3`')
    if checkbox_states['io1_storage']:
        query_parts.append('StorageType == `io1`')
    if checkbox_states['magnetic_storage']:
        query_parts.append('StorageType == `standard`')
    
    # print(f"DEBUG: query_parts after construction: {query_parts}")

    query = 'OrderableDBInstanceOptions[?{}]'.format(' && '.join(query_parts)) if query_parts else 'OrderableDBInstanceOptions[]'
    
    # Use the logger to write some information to the log file
    logger.info(f"Executing API call with the following options:")
    logger.info(f"Region: {os.environ.get('RDS_REGION')}")
    logger.info(f"Engine: {engine}")
    if engine_version:
        logger.info(f"EngineVersion: {engine_version}")
    logger.info(f"DBInstanceClass: {db_instance_class}")
    logger.info(f"MultiAZCapable: {kwargs['multi_az_var'].get()}")
    logger.info(f"SupportsClusters: {kwargs['supports_clusters_var'].get()}")
    logger.info(f"SupportsPerformanceInsights: {kwargs['supports_performance_insights_var'].get()}")
    logger.info(f"SupportsEnhancedMonitoring: {kwargs['supports_enhanced_monitoring_var'].get()}")
    logger.info(f"SupportsStorageEncryption: {kwargs['storage_encyption_var'].get()}")
    logger.info(f"SupportsIAMDatabaseAuthentication: {kwargs['iam_authentication_var'].get()}")
    logger.info(f"SupportsKerberosAuthentication: {kwargs['kerberos_authentication_var'].get()}")
    logger.info(f"SupportsGlobalDatabases: {kwargs['global_database_var'].get()}")
    logger.info(f"GP2 Storage: {kwargs['gp2_storage_var'].get()}")
    logger.info(f"GP3 Storage: {kwargs['gp3_storage_var'].get()}")
    logger.info(f"IO1 Storage: {kwargs['io1_storage_var'].get()}")
    logger.info(f"Magnetic Storage: {kwargs['magnetic_storage_var'].get()}")
    logger.debug(f"JMESPath query: {query} \n")

    # Print some console information, this isn't necessary but it's useful for debugging

    # print(f"INFO: Executing API call with the following options:")
    # print(f"INFO: Region: {os.environ.get('RDS_REGION')}")
    # print(f"INFO: Engine: {engine}")
    # if engine_version:
    #     print(f"INFO: EngineVersion: {engine_version}")
    # print(f"INFO: DBInstanceClass: {db_instance_class}")
    # print(f"INFO: MultiAZCapable: {kwargs['multi_az_var'].get()}")
    # print(f"INFO: SupportsClusters: {kwargs['supports_clusters_var'].get()}")
    # print(f"INFO: SupportsPerformanceInsights: {kwargs['supports_performance_insights_var'].get()}")
    # print(f"INFO: SupportsEnhancedMonitoring: {kwargs['supports_enhanced_monitoring_var'].get()}")
    # print(f"INFO: SupportsStorageEncryption: {kwargs['storage_encyption_var'].get()}")
    # print(f"INFO: SupportsIAMDatabaseAuthentication: {kwargs['iam_authentication_var'].get()}")
    # print(f"INFO: SupportsKerberosAuthentication: {kwargs['kerberos_authentication_var'].get()}")
    # print(f"INFO: SupportsGlobalDatabases: {kwargs['global_database_var'].get()}")
    # print(f"DEBUG: JMESPath query: {query} \n")
    return query

# Define a function to process the API response
def process_api_response(response, query):
    filtered_options = jmespath.search(query, response)
    api_results = []
    for option in filtered_options:
        row_data = [
            option.get("Engine", ""),
            option.get("EngineVersion", ""),
            option.get("DBInstanceClass", ""),
            option.get("StorageType", ""),
            option.get("MaxIopsPerDbInstance", ""), 
            option.get("MaxStorageSize", ""),
            option.get("MaxStorageThroughputPerDbInstance", ""),
        ]
        api_results.append(row_data)
    return api_results
  
# Define a function to fetch and display the results when the execute button is clicked
# def fetch_and_display(engine_entry, db_instance_class_entry, result_tree, db_engine_version_entry, **kwargs):
def fetch_and_display(engine_entry, db_instance_class, result_tree, db_engine_version_entry, **kwargs):
    global api_results
    client = boto3.client('rds', region_name=os.environ.get("RDS_REGION"))
    # Get the user inputs
    engine = engine_entry.get()
    # db_instance_class = db_instance_class_entry.get()
    db_instance_class = db_instance_class
    # This is a hack to support db.serverless as this class does not support the db.class.type format eg. db.t3.micro
    if db_instance_class == "db.serverless.":
        db_instance_class = "db.serverless"
    else:
        db_instance_class = db_instance_class
    if db_engine_version_entry:
        db_engine_version_entry = db_engine_version_entry.get()
    
    # Call the boto3 API to get the supported orderables for the engine and instance class
    try:
        # print(f"DEBUG: boto3 client in fetch_and_display function: {region_name}")
        response = client.describe_orderable_db_instance_options(
            Engine=engine,
            DBInstanceClass=db_instance_class
        )
    except Exception as e:
        # Write to logger
        logger.error(f"Could not execute API call: {e}")
        # print(f"ERROR: Could not execute API call: {e}")
        return
    
    # Clear previous results in the treeview
    for row in result_tree.get_children():
        result_tree.delete(row)
    
    # Get the checkbox states and construct the JMESPath query
    checkbox_states = {
        'multi_az': kwargs['multi_az_var'].get(),
        'supports_clusters': kwargs['supports_clusters_var'].get(),
        'supports_performance_insights': kwargs['supports_performance_insights_var'].get(),
        'supports_enhanced_monitoring': kwargs['supports_enhanced_monitoring_var'].get(),
        'storage_encyption': kwargs['storage_encyption_var'].get(),
        'iam_authentication': kwargs['iam_authentication_var'].get(),
        'kerberos_authentication': kwargs['kerberos_authentication_var'].get(),
        'global_database': kwargs['global_database_var'].get(),
        'gp2_storage': kwargs['gp2_storage_var'].get(),
        'gp3_storage': kwargs['gp3_storage_var'].get(),
        'io1_storage': kwargs['io1_storage_var'].get(),
        'magnetic_storage': kwargs['magnetic_storage_var'].get(),
    }
    query = construct_jmespath_query(checkbox_states, engine, db_instance_class, db_engine_version_entry, **kwargs)
    
    # Process the API response and add rows to the treeview
    api_results = process_api_response(response, query)
    for row_data in api_results:
        result_tree.insert("", "end", values=row_data)

# Define a function to save the results to a CSV file, the file name and file type are defined in config/constants.py
def save_to_csv():
    global api_results
    try:
        file_path = filedialog.asksaveasfilename(initialfile=f"{api_results_save_file_name}", defaultextension=f"{api_results_save_file_type}", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Engine", "EngineVersion", "DBInstanceClass", "StorageType", "MaxIopsPerDbInstance", "MaxStorageSize", "MaxStorageThroughputPerDbInstance"])
                writer.writerows(api_results)
    except Exception as e:
        # Write to logger
        logger.error(f"Could not save to CSV: {e}")
        # print(f"ERROR: Could not save to CSV: {e}")
        return