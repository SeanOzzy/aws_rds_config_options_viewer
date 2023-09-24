
"""
This file contains the constants used in the application.
You may modify the values in this file to suit your needs.
"""

# This is used for the requirements precheck function to verify AWS API access and to fail early if there are any missing requirements
AWS_TEST_REGION = "us-east-1"
required_packages_list = ["boto3", "jmespath"]

# Exclusion list for engines that are not core RDS engines, you can modify this list to suit your needs
# Ref: https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_DescribeDBEngineVersions.html
excluded_engines = ["custom-oracle-ee", "oracle-ee-cdb", "oracle-se2-cdb", "custom-sqlserver-ee", "custom-sqlserver-se", 
                    "custom-sqlserver-ex", "custom-sqlserver-web", "docdb", "neptune"]

# Cache expiry time in days
cache_expiry_days = 7

# Cache default directory
cache_dir = "cache/"

# Log file name and directory the log directory should be cross platform compatible
log_dir = "logs/"
log_filename = 'rds-support-options-viewer.log'


# Cache file names
supported_engines_cache_name = "supported_engines"
supported_db_classes_cache_name = "supported_db_classes"

# API results Save button default file name and type
api_results_save_file_name = "results"
api_results_save_file_type = ".csv"

# Define some values for the GUI
main_window_title = "AWS RDS Supported Options Viewer"
main_window_image = "gui/small_logo.png"
rds_region_window_title = "Select AWS Region"


