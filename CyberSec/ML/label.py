import pandas as pd
import os
import pathlib

path = pathlib.Path().resolve()

# Define paths
input_csv = r"./estimate_1/subset_1.csv"
output_dir = r"./estimate_1"
os.makedirs(output_dir, exist_ok=True)

# Load the dataset
data = pd.read_csv(input_csv)

# Extract unique labels from the 'label' column
unique_labels = data['label'].unique()

# Create LABEL_MAPPING as a dictionary
LABEL_MAPPING = {label: idx for idx, label in enumerate(unique_labels)}

# Save the LABEL_MAPPING dictionary to a file in the desired format
label_mapping_file = os.path.join(output_dir, 'label_mapping.txt')
with open(label_mapping_file, 'w') as f:
    f.write("LABEL_MAPPING = {\n")
    f.write(",\n".join([f"    '{label}': {idx}" for label, idx in LABEL_MAPPING.items()]))
    f.write("\n}")

print(f"LABEL_MAPPING saved to: {label_mapping_file}")
