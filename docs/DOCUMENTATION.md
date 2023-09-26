## Overview

### Main Script launching point

**Description**: The main script, ```rdsConfigViewer.py```, begins by importing necessary modules and setting up some initial configurations. Here's a brief overview:

**Imports**: The script uses the boto3 library (AWS SDK for Python) to interact with AWS services. It also imports tkinter for GUI-related tasks, along with other utility and configuration modules from the project.
**Initial GUI Configuration**: Initializes the region selection window using tkinter.
**Requirement Precheck Function**: This function performs various checks to fail early if there is a missing dependency.
    - **AWS API Access**: It checks if the application can successfully make a call to the AWS RDS API to ensure valid credentials and access.
    - **Python Package Requirements**: Checks if all required Python packages are installed.

### Utility modules
The utils directory contains the following utility modules:

#### aws_api.py
**Description**: The ```aws_api.py``` utility module focuses on fetching and processing data from AWS using the boto3 library. Here's a breakdown of how it works:

**Imports**: The script imports necessary libraries and modules such as boto3, caching utilities, logging, and configurations.
**Key Functions**:
    - **get_supported_engines Function**: Fetches a list of supported RDS engines. Utilizes a cache to store previously fetched data for faster subsequent accesses. If valid cache data is found, it returns the cached data. If the cache is expired or not found, it fetches data from AWS using paginated responses and populates the cache. There is a filter to remove non-core engines as defined in the ```constants.py``` configuration.
    - **fetch_db_instance_classes_for_engine Function**: Fetches a list of supported DB instance classes for the selected region and DB engines that were found via the ```get_supported_engines()```. This function also utilizes a cache to store previously fetched data for faster subsequent accesses.


#### cache.py
The ```cache.py``` utility module manages caching for the application. Here's a breakdown:

**Description**: The module uses a JSON file to store cached data. Cached data is stored in a dictionary with the AWS region as the key, allowing for data from multiple regions to be stored in a single file. Data is fetched from the cache only for the selected region.
**Key Functions**:
    - **get_from_cache**: This function attempts to retrieve data from the cache based on a provided cache key. It checks if the cache file exists and if the data is still valid based on a cache validity duration (in days). If the cache is valid, it reads the data and returns it. If there's an issue reading the cache or if the cache is invalid, the function can optionally delete the corrupted or expired cache file.
    - **save_to_cache**: Saves data to the cache file. If the cache directory doesn't exist, it creates it. Appends new data to the existing cache file, if it exists. The AWS region is used as the key for the cached data. The caching strategy is region-based, which means data for different AWS regions can be cached separately. This is useful since AWS offerings and configurations may differ across regions.

#### data_processing.py
The ```data_processing.py``` module deals with processing API responses and presenting results. Here's a brief overview:

**Description**: The module is focused on constructing JMESPath queries based on user preferences and extracting desired details from AWS API responses.
**Key Functions**:
    - **construct_jmespath_query**: Constructs a JMESPath query based on various checkboxes' states. The function allows users to filter RDS instances based on features like MultiAZ capability, support for clusters, performance insights, enhanced monitoring, storage encryption, IAM authentication, and more. It dynamically constructs the query string based on selected checkboxes. This utility provides a fine-grained filtering mechanism for users to narrow down their RDS instance choices based on multiple criteria. The use of JMESPath is efficient for extracting specific details from complex JSON responses.

