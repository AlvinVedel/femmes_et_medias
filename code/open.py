# Attempting to read the file with less strict parsing settings
# Ignoring bad lines and not assuming any particular structure of quotes

# First, let's try to detect the separator automatically using Python's CSV Sniffer tool
import csv
import pandas as pd

# Function to detect delimiter
def detect_delimiter(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        sample = file.read(1024)  # Read the first 1024 bytes of the file
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample)
        return dialect.delimiter

# Detect the delimiter of the file
detected_delimiter = detect_delimiter("concat_all.csv")

# Now, read the CSV with the detected delimiter and minimal assumptions
try:
    data_df_loose = pd.read_csv("concat_all.csv", sep=detected_delimiter, engine='python', on_bad_lines='skip')
    print(data_df_loose)
except Exception as e:
    print("Error reading with loose settings:", e)


