#EXTRACTS ONLY NAMES FROM THE .TXT FILE OF THE FORMAT "<Number>. <Name> - <Description>"

import csv
import re

# Define the input and output file paths
input_file = input("Enter the name of the file (must be placed in same folder as this script): ")
output_csv_file = 'output.csv'

# Regular expression pattern to extract names
pattern = r'\d+\.\s+([^-\n]+)'

# Create a list to store the extracted names
names = []

# Open and read the input file
with open(input_file, 'r') as file:
    for line in file:
        match = re.search(pattern, line)
        if match:
            name = match.group(1).strip()
            names.append([name])

# Write the extracted names to a CSV file
with open(output_csv_file, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(names)

print(f"Names extracted from '{input_file}' and saved in '{output_csv_file}'.")
