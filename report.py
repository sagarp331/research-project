import pandas as pd
import matplotlib.pyplot as plt
file_path = r"report.xlsx"
xls = pd.ExcelFile(file_path)
sheet_names = xls.sheet_names
# Define  matrix suction depth columns (AA and BB)
target_columns = ['0 m_AA', '3 m_AA', '6 m_AA', '0 m_BB', '3 m_BB', '6 m_BB']
colors = ['r', 'g', 'b', 'm', 'c', 'y', 'orange', 'purple', 'brown', 'pink']
# Loop through each depth column
for target_col in target_columns:
    fig, ax1 = plt.subplots(figsize=(14, 8))

    for i, sheet in enumerate(sheet_names):
        df = pd.read_excel(file_path, sheet_name=sheet)

        # Skip if required columns are missing
        if not {'Days', 'Rainfall(mm/d)', target_col}.issubset(df.columns):
            print(f"Skipping sheet '{sheet}' for column '{target_col}' (missing data)")
            continue

        # Replace negative rainfall values with 0 
        for idx in range(len(df['Rainfall(mm/d)'])):
            if df['Rainfall(mm/d)'][idx] < 0:
                df['Rainfall(mm/d)'][idx] = 0

        x = df['Days']
        y = df[target_col]

        # Plot Matric Suction values on left Y-axis
        color = colors[i % len(colors)]# Avoiding Color Cluttering
        ax1.plot(x, y, label=f"{sheet}", color=color)

    ax1.set_xlabel("Days")
    ax1.set_ylabel("Matric Suction")
    ax1.set_title(f"{target_col} For All Soil Types")
    ax1.grid(True)

    # Plot Rainfall as bar chart on right Y-axis from the first sheet only
    df_rain = pd.read_excel(file_path, sheet_name=sheet_names[0])
    
    # Replace negative rainfall values with 0 as negative rainfall might occur beacuse of instrumental error
    for idx in range(len(df_rain['Rainfall(mm/d)'])):
        if df_rain['Rainfall(mm/d)'][idx] < 0:
            df_rain['Rainfall(mm/d)'][idx] = 0

    ax2 = ax1.twinx()
    ax2.bar(df_rain['Days'], df_rain['Rainfall(mm/d)'], color='#87CEEB', alpha=0.5, label='Rainfall')
    ax2.set_ylabel("Rainfall (mm/day)", color='black')
    ax2.tick_params(axis='y', labelcolor='black')

    ax1.legend(loc='upper left')
    plt.tight_layout()
    plt.show()
