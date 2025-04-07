import pandas as pd
import re
import matplotlib.pyplot as plt

file_path = r"fos.xlsx"  # Excel file path

def process_fos_data(sheet_name, start_row, header_row_start, header_row_end):
    # Read the Excel sheet
    df_raw = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    
    # Set headers based on the provided range
    headers = df_raw.iloc[header_row_start:header_row_end]
    
    # Ensure all header values are treated as strings
    combined_headers = headers.T.fillna('').agg(lambda x: ' '.join(x.astype(str)), axis=1).str.strip()
    
    # Print the combined headers to check if all data are incorporated or not
    print(f"Combined Headers for {sheet_name}:")
    print(combined_headers)
    
    # Read data starting from the specified start_row
    df_data = df_raw.iloc[start_row:].copy()
    df_data.columns = combined_headers
    
    # Converting all data to numeric
    for col in df_data.columns:
        df_data[col] = pd.to_numeric(df_data[col], errors='coerce')
    
    # Initialize a dictionary to store reductions for each parameter, which is our cut slope
    fos_data = {}

    # Check column names and process each one that matches the required pattern
    for target_column in df_data.columns:
        # Updated regular expression to handle both whole numbers and decimal values
        match = re.match(r'(\d+m) 1:(\d+(\.\d+)?)', target_column)
        
        if match:
            cut_depth = match.group(1)  # Cut depth
            param = match.group(2)      # Cut slope
            
            # Calculate the absolute % reduction for all 123 days
            initial = df_data[target_column].iloc[0]
            
            if pd.notna(initial) and initial != 0:
                # Calculate percentage reduction
                percent_reduction = ((df_data[target_column] - initial) / initial) * 100
                abs_percent_reduction = percent_reduction.abs()
                
                # Limit to first 11 entries as later contain null values
                abs_percent_reduction_11 = abs_percent_reduction.iloc[:11]
                
                # Calculate the average reduction 
                avg_abs_reduction_11 = abs_percent_reduction_11.mean()
                
                # Store the average reduction in the fos_data dictionary
                if param not in fos_data:
                    fos_data[param] = []
                fos_data[param].append(avg_abs_reduction_11)

    return fos_data

def plot_fos_data(fos_data, cut_depths, title):
    # Creating DataFrames for each parameter and plot
    plt.figure(figsize=(10, 6))

    # Loop through each parameter (i.e., ground slopes) and plot
    for param, reductions in fos_data.items():
        # Creating a DataFrame for each parameter
        df = pd.DataFrame(reductions, columns=[f"Avg Abs Reduction for 1:{param}"])
        
        # Assigning cut depths to the DataFrame
        df['Cut Depth'] = cut_depths[:len(reductions)] 
        
        # Plotting the data
        plt.plot(df['Cut Depth'], df[f"Avg Abs Reduction for 1:{param}"], label=f"1:{param}")

    # Plot
    plt.xlabel('Cut Depth')
    plt.ylabel('Average Absolute % Reduction')
    plt.title(title)  # Using the passed title for the plot
    plt.legend(title='Parameter')

    # Showing plot
    plt.tight_layout()
    plt.show()

# Defining cut depth manually
cut_depths = ['2m', '3m', '4m', '6m', '8m']

# Load Excel to get sheet names
excel_file = pd.ExcelFile(file_path)
sheet_names = excel_file.sheet_names

# Loop through all sheets in the Excel file
for sheet_name in sheet_names:
    print(f"Processing data for sheet: {sheet_name}")
    
    # Define row settings for different percentages
    start_row_20pc = 3
    header_row_start_20pc = 0
    header_row_end_20pc = 3
    
    start_row_30pc = 20
    header_row_start_30pc = 16
    header_row_end_30pc = 19
    
    start_row_40pc = 36
    header_row_start_40pc = 32
    header_row_end_40pc = 35
    
    # Process data for each percentage of ground slopes (20%, 30%, 40%) dynamically for each sheet
    print(f"Processing 20% slope data for sheet: {sheet_name}")
    fos_data_20pc = process_fos_data(sheet_name=sheet_name, start_row=start_row_20pc, header_row_start=header_row_start_20pc, header_row_end=header_row_end_20pc)
    print(f"Processing 30% slope data for sheet: {sheet_name}")
    fos_data_30pc = process_fos_data(sheet_name=sheet_name, start_row=start_row_30pc, header_row_start=header_row_start_30pc, header_row_end=header_row_end_30pc)
    print(f"Processing 40% slope data for sheet: {sheet_name}")
    fos_data_40pc = process_fos_data(sheet_name=sheet_name, start_row=start_row_40pc, header_row_start=header_row_start_40pc, header_row_end=header_row_end_40pc)
    
    # Debugging: Check the contents of fos_data for all slopes
    print(f"FOS Data for 20% slope in {sheet_name}:")
    print(fos_data_20pc)
    
    print(f"FOS Data for 30% slope in {sheet_name}:")
    print(fos_data_30pc)
    
    print(f"FOS Data for 40% slope in {sheet_name}:")
    print(fos_data_40pc)

    # Plot the FOS data for 20%, 30%, and 40% slopes if available
    if fos_data_20pc:
        plot_fos_data(fos_data_20pc, cut_depths, title=f"{sheet_name}: Average FOS Reduction vs. Cut Depth (20%)")
    else:
        print(f"No data to plot for 20% slope in {sheet_name}.")

    if fos_data_30pc:
        plot_fos_data(fos_data_30pc, cut_depths, title=f"{sheet_name}: Average FOS Reduction vs. Cut Depth (30%)")
    else:
        print(f"No data to plot for 30% slope in {sheet_name}.")

    if fos_data_40pc:
        plot_fos_data(fos_data_40pc, cut_depths, title=f"{sheet_name}: Average FOS Reduction vs. Cut Depth (40%)")
    else:
        print(f"No data to plot for 40% slope in {sheet_name}.")
