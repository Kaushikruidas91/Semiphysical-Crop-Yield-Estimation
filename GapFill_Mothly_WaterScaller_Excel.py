import pandas as pd
import numpy as np

# Input file
file_path = r"D:\CIPL_WORK\Semiphysical_Kharif_Paddy_25_UP\WithGap_WS_FAPAR_Data\WS_FPAR_Value_withGape_UP.xlsx"

# Output file
output_path = r"D:\CIPL_WORK\Semiphysical_Kharif_Paddy_25_UP\WithGap_WS_FAPAR_Data\WS_FPAR_Value_Gapfill_withMean_UP.xlsx"

# Load dataset
df = pd.read_excel(file_path)

# Define your WS combinations
groups = [
    ["WS_153","WS_161", "WS_169", "WS_177"],
    ["WS_185", "WS_193", "WS_201", "WS_209"],
    ["WS_217", "WS_225", "WS_233", "WS_241"],
    ["WS_249", "WS_257", "WS_265", "WS_273"],
    [ "WS_281", "WS_289", "WS_297","WS_305"],
    [ "WS_305", "WS_313", "WS_321","WS_329"]
]

# Process each combination
for group in groups:
    # Check columns exist in the Excel file
    existing_cols = [col for col in group if col in df.columns]

    if len(existing_cols) == 0:
        print(f"Skipping group {group}: No matching columns found.")
        continue

    # Calculate row-wise mean for the group (ignore NaN)
    row_mean = df[existing_cols].mean(axis=1)

    # Fill missing values with the row mean
    for col in existing_cols:
        df[col] = df[col].fillna(row_mean)

    print(f"Filled gaps for group: {existing_cols}")

# Save the gap-filled result
df.to_excel(output_path, index=False)

print("✅ Gap filling complete.")
print("➡️ Output saved as:", output_path)
