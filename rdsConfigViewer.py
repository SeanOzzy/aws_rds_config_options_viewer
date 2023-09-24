import boto3
import tkinter as tk
from tkinter import ttk
import utils.data_processing as data_processing
from gui import widgets
from config.constants import AWS_TEST_REGION, required_packages_list
from config import rds_endpoints
from utils.logger import logger
import os
import pkg_resources

# Start the region selection window, we need the region the user selects to initialize the main window
region_selection_root = tk.Tk()
region_var = tk.StringVar()

def requirement_precheck():
    """
    Performs various checks to ensure the environment is properly set up.
    """
    # Check AWS API access
    try:
        print(f"INFO: Running requirement precheck, please wait...")
        client = boto3.client('rds', region_name=AWS_TEST_REGION)
        # This is a lightweight API call to check if we have valid credentials
        client.describe_db_engine_versions(MaxRecords=20)
        logger.info("AWS API access verified.")
        # print("AWS API access verified.")
    except Exception as e:
        # Log error to log file and exit
        logger.critical(f"Failed to access AWS API. Ensure you have valid credentials. Error: {e}")
        raise EnvironmentError(f"Failed to access AWS API. Ensure you have valid credentials. Error: {e}")
    
    # Check Python package requirements
    required_packages = [pkg for pkg in required_packages_list]  # Add any other required packages here
    installed_packages = [pkg.key for pkg in pkg_resources.working_set]
    
    missing_packages = [pkg for pkg in required_packages if pkg not in installed_packages]
    
    if missing_packages:
        logger.critical(f"Missing required Python packages: {', '.join(missing_packages)}")
        raise ImportError(f"Missing required Python packages: {', '.join(missing_packages)}")
    logger.info("All requirements satisfied.")
    # print("All requirements satisfied.")

# This functions initializes the region selection window and waits for the user to select a region
def create_region_selection_window():
    """
    Create a popup window for region selection.
    """
    global region_selection_window
    region_selection_window = region_selection_root
    region_selection_window.title("Select AWS Region")
    region_selection_window.geometry("300x200")

    # Load available regions from the config file
    regions = list(rds_endpoints.RDS_ENDPOINTS.keys())

    # Create and pack the region selection combobox
    region_label = tk.Label(region_selection_window, text="Select a region:")
    region_label.pack(pady=10)

    region_combobox = ttk.Combobox(region_selection_window, textvariable=region_var, values=regions, state="readonly")
    region_combobox.pack(pady=10)
    region_combobox.set(regions[0])  # Default value

    ok_button = tk.Button(region_selection_window, text="OK", command=region_selection_ok)
    ok_button.pack(pady=10)

    # Pause the script execution until the region_selection_window is closed
    region_selection_root.wait_window(region_selection_window)

# This function is called when the user clicks the OK button in the region selection window
# It closes the region selection window and launches the main application window
# If cached data is found for the selected regions the main window is initialized immediately
# Else the the data is fetched and the main window is initialized, fetching the data can take 2-4 mins
def region_selection_ok():
    """
    Callback for the OK button in the region selection window.
    """
    SELECTED_REGION = region_var.get()
    # print(f"DEBUG: global_vars.SELECTED_REGION: {SELECTED_REGION}")
    # Set as a temporary environment variable
    os.environ["RDS_REGION"] = SELECTED_REGION
    RDS_REGION = os.environ.get("RDS_REGION")
    # print(f"DEBUG: osenv RDS_REGION: {RDS_REGION}")
    region_selection_window.destroy()
    initialize_main_window(RDS_REGION)

def initialize_main_window(RDS_REGION):
    """
    Initialize and display the main application window's widgets.
    """
    # print(f"DEBUG: initialize_main_window RDS_REGION: {RDS_REGION}")
    widgets.initialize_gui(data_processing.fetch_and_display)

def main():
    # Run the requirements precheck
    requirement_precheck()
    # Create region selection window
    create_region_selection_window()

if __name__ == "__main__":
    main()
