import pandas as pd
import matplotlib.pyplot as plt

# Excel file path
file_path = r"swcc-hcf.xlsx"

# Load all sheet names
xls = pd.ExcelFile(file_path)
sheet_names = xls.sheet_names

# Initialize plot

plt.figure(figsize=(12, 6))


for sheet in sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet, header=1)
    df = df.apply(pd.to_numeric, errors='coerce')
    if 'Negative Water Pressure (kPa)' in df.columns and 'Volumetric Water Content' in df.columns:
        plt.plot(df['Negative Water Pressure (kPa)'], df['Volumetric Water Content'],
                 marker='.', label=sheet)  


# Configure plot
plt.title('Volumetric Water Content vs Negative Water Pressure (All Soils)')
plt.xlabel('Negative Water Pressure (kPa)')
plt.ylabel('Volumetric Water Content')
plt.xscale('log')  
plt.grid(True, which='both')
plt.legend()
plt.tight_layout()
plt.show()
#End of figure 1

# Initalize plot 

plt.figure(figsize=(12, 6))
for sheet in sheet_names:
   
    df = pd.read_excel(file_path, sheet_name=sheet, header=1)


    df = df.apply(pd.to_numeric, errors='coerce')


    if 'Matric Suction (kPa)' in df.columns and 'Water X-Conductivity (m/hr)' in df.columns:
        plt.plot(df['Matric Suction (kPa)'], df['Water X-Conductivity (m/hr)'],
                 marker='.', label=sheet)  

# Configure plot
plt.title('Water X-Conductivity vs Matric Suction (All Soils)')
plt.xlabel(' Matric Suction (kPa)')
plt.ylabel('Water X-Conductivity (m/hr)')
plt.xscale('log')
plt.grid(True, which='both')
plt.legend()
plt.tight_layout()
plt.show()