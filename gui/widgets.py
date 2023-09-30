
"""
This module contains functions to create and populate the GUI widgets
"""
def populate_dropdowns(main_window, engines, db_classes):
    # Assuming engine_dropdown and db_class_dropdown are the variable names for your dropdown widgets
    main_window.engine_dropdown['values'] = engines
    main_window.db_class_dropdown['values'] = db_classes

# Add a function to allow disabling checkboxes when the selection of multiple checkboxes is invalid
def toggle_checkboxes(checked_var, checked_checkbox, *checkboxes):
    if checked_var.get():  # If the checkbox was checked
        for checkbox in checkboxes:
            checkbox.configure(state="disabled")
    else:  # If the checkbox was unchecked
        for checkbox in checkboxes:
            checkbox.configure(state="normal")

# Add a function to help break down the long list of db instance types into a dictionary of classes and types
def categorize_instance_classes(data_list):
    categorized_data = {}
    for instance in data_list:
        parts = instance.split('.')
        class_name = f"{parts[0]}.{parts[1]}"
        type_name = '.'.join(parts[2:])
        if class_name not in categorized_data:
            categorized_data[class_name] = []
        categorized_data[class_name].append(type_name)
    return categorized_data

# Add a function to update the DB instance type combobox when the DB instance class is selected
def on_class_selected(event, categorized_data, db_instance_class_entry, db_instance_type_entry):
    selected_class = db_instance_class_entry.get()
    if selected_class in categorized_data:
        db_instance_type_entry['values'] = categorized_data[selected_class]
    else:
        db_instance_type_entry['values'] = []
    db_instance_type_entry.set('')  # Reset the combobox value


# Define a function to initialize the main GUI window
def initialize_gui(fetch_and_display_func):
    global fetch_button
    import config.constants as constants
    import utils.cache as cache
    import utils.aws_api as aws_api
    import utils.data_processing as data_processing
    import tkinter as tk
    from tkinter import ttk, filedialog
    import os

    RDS_REGION = os.environ.get("RDS_REGION")
    # Initialize the main GUI window
    main_window = tk.Tk()
    main_window.title(constants.main_window_title)

    img = tk.PhotoImage(file = constants.main_window_image)
    img1 = img.subsample(2, 2)
 
    # setting image with the help of label
    tk.Label(main_window, image = img1).grid(row = 0, column = 4,
       columnspan = 2, rowspan = 2, padx = 5, pady = 5)

    # Create and place the RDS region selection widgets
    rds_region_label = tk.Label(main_window, text=f"{constants.rds_region_window_title}: {RDS_REGION}")
    rds_region_label.grid(column=1, row=0, columnspan=3, padx=1, pady=1)
    rds_region_label.grid_columnconfigure(1, weight=1)
    rds_region_label.grid_rowconfigure(1, weight=1)

    # Create and place the user input widgets
    engine_label = tk.Label(main_window, text="Select Database Engine (required)")
    engine_label.grid(column=0, row=1, columnspan=3, padx=1, pady=1)
    engine_label.grid_columnconfigure(1, weight=1)
    engine_label.grid_rowconfigure(1, weight=1)

    # Call the function to generate the list of supported engines
    engine_options = aws_api.get_supported_engines()
    engine_entry = ttk.Combobox(main_window, values=engine_options)
    engine_entry.grid(column=1, row=1, columnspan=3, padx=1, pady=1)
    engine_entry.grid_columnconfigure(1, weight=1)
    engine_entry.grid_rowconfigure(1, weight=1)

    db_instance_class_label = tk.Label(main_window, text="Select DB Instance Class (required)")
    db_instance_class_label.grid(column=0, row=2, columnspan=3, padx=1, pady=1)
    db_instance_class_label.grid_columnconfigure(1, weight=1)
    db_instance_class_label.grid_rowconfigure(1, weight=1)

    db_instance_type_label = tk.Label(main_window, text="Select DB Instance Type (required)")
    db_instance_type_label.grid(column=0, row=3, columnspan=3, padx=1, pady=1)
    db_instance_type_label.grid_columnconfigure(1, weight=1)
    db_instance_type_label.grid_rowconfigure(1, weight=1)

# Call the function to generate the list of supported DB instance classes
    db_instance_class_options = aws_api.get_supported_db_classes(engine_options)
    # Call the function to categorize the DB instance classes into a dictionary
    categorized_instance_classes_data = categorize_instance_classes(db_instance_class_options)
    # Create a combobox to display the DB instance classes
    db_instance_class_list = list(categorized_instance_classes_data.keys())
    # Insert the class list into the combobox
    db_instance_class_entry = ttk.Combobox(main_window, values=db_instance_class_list)
    db_instance_class_entry.grid(column=1, row=2, columnspan=3, padx=1, pady=1)
    db_instance_class_entry.grid_columnconfigure(1, weight=1)
    db_instance_class_entry.grid_rowconfigure(1, weight=1)

    # Create a combobox to display the DB instance types
    db_instance_type_entry = ttk.Combobox(main_window)
    db_instance_type_entry.grid(column=1, row=3, columnspan=3, padx=1, pady=1)
    db_instance_type_entry.grid_columnconfigure(1, weight=1)
    db_instance_type_entry.grid_rowconfigure(1, weight=1)

    # When the user selects the db class from the combobox, update the db instance type combobox
    # With this we can give the user a shorter list of instance types based on the instance class they select
    # Eg: If the user selects db.t3, then we can show only the t3 instance types in the instance type combobox
    db_instance_class_entry.bind("<<ComboboxSelected>>", 
                                 lambda event, data=categorized_instance_classes_data, class_entry=db_instance_class_entry, type_entry=db_instance_type_entry: on_class_selected(event, data, class_entry, type_entry))


    db_engine_version_label = tk.Label(main_window, text="Enter DB Engine Version (optional)")
    db_engine_version_label.grid(column=0, row=4, columnspan=3, padx=1, pady=1)
    db_engine_version_label.grid_columnconfigure(1, weight=1)
    db_engine_version_label.grid_rowconfigure(1, weight=1)
    db_engine_version_entry = ttk.Entry(main_window)
    db_engine_version_entry.grid(column=1, row=4, columnspan=3, padx=1, pady=1)
    db_engine_version_entry.grid_columnconfigure(1, weight=1)
    db_engine_version_entry.grid_rowconfigure(1, weight=1)
    # ... (repeat the above lines for other input fields)

# Define IntVar variables for the checkboxes and set initial values
    multi_az_var = tk.IntVar(value=0)
    supports_clusters_var = tk.IntVar(value=0)
    supports_performance_insights_var = tk.IntVar(value=0)
    supports_enhanced_monitoring_var = tk.IntVar(value=0)
    storage_encyption_var = tk.IntVar(value=0)
    iam_authentication_var = tk.IntVar(value=0)
    kerberos_authentication_var = tk.IntVar(value=0)
    global_database_var = tk.IntVar(value=0)
    gp2_storage_var = tk.IntVar(value=0)
    gp3_storage_var = tk.IntVar(value=0)
    io1_storage_var = tk.IntVar(value=0)
    magnetic_storage_var = tk.IntVar(value=0)
    # ... (repeat the above lines for additional checkboxes)

# Associate the IntVar variables with the checkboxes and set commands to print variable values on click
    multi_az_checkbox = tk.Checkbutton(main_window, text="RDS Multi-AZ", variable=multi_az_var, onvalue=1, offvalue=0, 
                                       command=lambda: toggle_checkboxes(multi_az_var, multi_az_checkbox, multi_az_cluster_checkbox))
    multi_az_checkbox.grid(column=0, row=6, columnspan=3, padx=10, pady=10)
    multi_az_checkbox.grid_columnconfigure(1, weight=1)
    multi_az_checkbox.grid_rowconfigure(1, weight=1)

    multi_az_cluster_checkbox = tk.Checkbutton(main_window, text="RDS Multi-AZ Clusters", variable=supports_clusters_var, 
                                               command=lambda: toggle_checkboxes(supports_clusters_var, multi_az_cluster_checkbox, multi_az_checkbox))
    multi_az_cluster_checkbox.grid(column=1, row=6, columnspan=3, padx=10, pady=10)
    multi_az_cluster_checkbox.grid_columnconfigure(1, weight=1)
    multi_az_cluster_checkbox.grid_rowconfigure(1, weight=1)

    storage_encyption_checkbox = tk.Checkbutton(main_window, text="SupportsStorageEncryption", variable=storage_encyption_var, command=None)
    storage_encyption_checkbox.grid(column=0, row=8, columnspan=3, padx=10, pady=10)
    storage_encyption_checkbox.grid_columnconfigure(1, weight=1)
    storage_encyption_checkbox.grid_rowconfigure(1, weight=1)
    
    iam_authentication_checkbox = tk.Checkbutton(main_window, text="SupportsIAMDatabaseAuthentication", variable=iam_authentication_var, command=None)
    iam_authentication_checkbox.grid(column=1, row=9, columnspan=3, padx=10, pady=10)
    iam_authentication_checkbox.grid_columnconfigure(1, weight=1)
    iam_authentication_checkbox.grid_rowconfigure(1, weight=1)

    kerberos_authentication_checkbox = tk.Checkbutton(main_window, text="SupportsKerberosAuthentication", variable=kerberos_authentication_var, command=None)
    kerberos_authentication_checkbox.grid(column=0, row=9, columnspan=3, padx=10, pady=10)
    kerberos_authentication_checkbox.grid_columnconfigure(1, weight=1)
    kerberos_authentication_checkbox.grid_rowconfigure(1, weight=1)

    global_database_checkbox = tk.Checkbutton(main_window, text="SupportsGlobalDatabases", variable=global_database_var, command=None)
    global_database_checkbox.grid(column=1, row=8, columnspan=3, padx=10, pady=10)
    global_database_checkbox.grid_columnconfigure(1, weight=1)
    global_database_checkbox.grid_rowconfigure(1, weight=1)

    pi_checkbox = tk.Checkbutton(main_window, text="SupportsPerformanceInsights", variable=supports_performance_insights_var, command=None)
    pi_checkbox.grid(column=0, row=7, columnspan=3, padx=10, pady=10)
    pi_checkbox.grid_columnconfigure(1, weight=1)
    pi_checkbox.grid_rowconfigure(1, weight=1)

    em_checkbox = tk.Checkbutton(main_window, text="SupportsEnhancedMonitoring", variable=supports_enhanced_monitoring_var, command=None)
    em_checkbox.grid(column=1, row=7, columnspan=3, padx=10, pady=10)
    em_checkbox.grid_columnconfigure(1, weight=1)
    em_checkbox.grid_rowconfigure(1, weight=1)
    # ... (repeat the above lines for additional checkboxes)

    # If gp2_checkbox selected then unselect all other storage type checkboxes
    # The lambda function is used to pass the checkbox variable and checkbox widget to the toggle_checkboxes() function
    # The format is command=lambda: function_name(variable_name, widget_name)
    # Where variable_name is the IntVar variable associated with the checkbox and widget_name is the selected checkbox widget
    # Any susequent arguments are the other checkboxes that need to be disabled when the selected checkbox is enabled
    gp2_checkbox = tk.Checkbutton(main_window, text="General Purpose Storage (gp2)", variable=gp2_storage_var, 
                                  command=lambda: toggle_checkboxes(gp2_storage_var, gp2_checkbox, gp3_checkbox, io1_checkbox, magnetic_checkbox))
    gp2_checkbox.grid(column=0, row=10, columnspan=3, padx=10, pady=10)
    gp2_checkbox.grid_columnconfigure(1, weight=1)
    gp2_checkbox.grid_rowconfigure(1, weight=1)

    gp3_checkbox = tk.Checkbutton(main_window, text="General Purpose Storage (gp3)", variable=gp3_storage_var, 
                                  command=lambda: toggle_checkboxes(gp3_storage_var, gp3_checkbox, gp2_checkbox, io1_checkbox, magnetic_checkbox))
    gp3_checkbox.grid(column=1, row=10, columnspan=3, padx=10, pady=10)
    gp3_checkbox.grid_columnconfigure(1, weight=1)
    gp3_checkbox.grid_rowconfigure(1, weight=1)

    io1_checkbox = tk.Checkbutton(main_window, text="Provisioned IOPS Storage (io1)", variable=io1_storage_var, 
                                  command=lambda: toggle_checkboxes(io1_storage_var, io1_checkbox, gp2_checkbox, gp3_checkbox, magnetic_checkbox))
    io1_checkbox.grid(column=0, row=11, columnspan=3, padx=10, pady=10)
    io1_checkbox.grid_columnconfigure(1, weight=1)
    io1_checkbox.grid_rowconfigure(1, weight=1)

    magnetic_checkbox = tk.Checkbutton(main_window, text="Magnetic Storage (deprecated)", variable=magnetic_storage_var, 
                                       command=lambda: toggle_checkboxes(magnetic_storage_var, magnetic_checkbox, gp2_checkbox, gp3_checkbox, io1_checkbox))
    magnetic_checkbox.grid(column=1, row=11, columnspan=3, padx=10, pady=10)
    magnetic_checkbox.grid_columnconfigure(1, weight=1)
    magnetic_checkbox.grid_rowconfigure(1, weight=1)


# Create a button to fetch and display data
    fetch_button = tk.Button(
        main_window, 
        text="Execute", 
        command=lambda: fetch_and_display_func(
            engine_entry, 
            # We need to join the DB instance class and type together to get the full name of the DB instance class.
            # db.serverless is a special case since this class does not have a type, so we hack this in the fetch_and_display() in data_processing.py
            db_instance_class_entry.get() + "." + db_instance_type_entry.get(), 
            result_tree,
            db_engine_version_entry,
            multi_az_var = multi_az_var,
            supports_clusters_var = supports_clusters_var,
            supports_performance_insights_var = supports_performance_insights_var,
            supports_enhanced_monitoring_var = supports_enhanced_monitoring_var,
            storage_encyption_var = storage_encyption_var,
            iam_authentication_var = iam_authentication_var,
            kerberos_authentication_var = kerberos_authentication_var,
            global_database_var= global_database_var,
            gp2_storage_var = gp2_storage_var,
            gp3_storage_var = gp3_storage_var,
            io1_storage_var = io1_storage_var,
            magnetic_storage_var = magnetic_storage_var,
            )  # add other needed elements
    )
    fetch_button.grid(column=0, row=12, columnspan=3, padx=1, pady=1)
    fetch_button.grid_columnconfigure(1, weight=1)
    fetch_button.grid_rowconfigure(1, weight=1)
    

    # Create a button to save the results to a CSV file
    save_csv_button = tk.Button(main_window, text="Save to CSV", command=data_processing.save_to_csv)
    save_csv_button.grid(column=1, row=12, columnspan=3, padx=1, pady=1)
    save_csv_button.grid_columnconfigure(1, weight=1)
    save_csv_button.grid_rowconfigure(1, weight=1)

    # Create a button to clear the cache, clearing the cache will force the application to fetch the latest data from the API which takes 2-4 mins
    clear_cache_button = tk.Button(main_window, text="Clear Cache", command=cache.clear_existing_cache)
    clear_cache_button.grid(column=1, row=13, columnspan=3, padx=1, pady=1)
    clear_cache_button.grid_columnconfigure(1, weight=1)
    clear_cache_button.grid_rowconfigure(1, weight=1)

    # Create a Treeview to display the results within the GUI
    result_tree = ttk.Treeview(main_window, columns=(
        "Engine", "EngineVersion", "DBInstanceClass", "StorageType", "MaxIopsPerDbInstance", "MaxStorageSize", "MaxStorageThroughputPerDbInstance"), show="headings")
    result_tree.heading("Engine", text="Engine")
    result_tree.heading("EngineVersion", text="EngineVersion")
    result_tree.heading("DBInstanceClass", text="DBInstanceClass")
    result_tree.heading("StorageType", text="StorageType")
    result_tree.heading("MaxIopsPerDbInstance", text="MaxIopsPerDbInstance")
    result_tree.heading("MaxStorageSize", text="MaxStorageSize")
    result_tree.heading("MaxStorageThroughputPerDbInstance", text="MaxStorageThroughputPerDbInstance")
    # If required add more headings here, remember to update header information in the save_to_csv() function if you add more columns
    result_tree.grid(column=0, row=15, columnspan=3, padx=1, pady=1)
    result_tree.grid_columnconfigure(1, weight=1)
    result_tree.grid_rowconfigure(1, weight=1)

    # Run the Tkinter event loop
    main_window.mainloop()