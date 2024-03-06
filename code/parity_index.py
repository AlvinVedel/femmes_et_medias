import pandas as pd
import spacy
import csv
import gender_guesser.detector as gender

# Load the CSV file
#data_df = pd.read_csv("/home/data/ter_meduse_log/mdw_2024/data/concat/concat_all.csv", sep="\t")
# Function to detect delimiter
def detect_delimiter(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        sample = file.read(1024)  # Read the first 1024 bytes of the file
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample)
        return dialect.delimiter

# Detect the delimiter of the file
detected_delimiter = detect_delimiter("/home/data/ter_meduse_log/mdw_2024/data/concat/concat_all.csv")

data_df = pd.read_csv("/home/data/ter_meduse_log/mdw_2024/data/concat/concat_all.csv", sep=detected_delimiter, engine='python', on_bad_lines='skip')
print("reading ok")

# Ensure 'description' column is of string type
data_df['description'] = data_df['description'].astype(str)

# Load Spacy French language model with only necessary components
nlp_fr = spacy.load("fr_core_news_sm", disable=["tagger", "parser"])

# Initialize a gender detector
detector = gender.Detector()

# Pronouns and their associated genders
pronoun_gender_map = {'elle': 'female', 'elles': 'female', 'il': 'male', 'ils': 'male'}

# Combined function to extract, identify entities and assign gender
def extract_entities_and_assign_gender(texts):
    results = []
    for doc in nlp_fr.pipe(texts, batch_size=50):
        items = []
        for ent in doc.ents:
            if ent.label_ == 'PER':
                gender = detector.get_gender(ent.text.split()[0])
                items.append((ent.text, ent.label_, gender))
        for token in doc:
            if token.text.lower() in pronoun_gender_map:
                items.append((token.text, 'PRON', pronoun_gender_map[token.text.lower()]))
        results.append(items)
    return results

# Apply function to extract entities and assign gender
data_df['entities_and_pronouns_in_descriptions'] = extract_entities_and_assign_gender(data_df['description'].tolist())
print("extract entities pronouns ok")

# Predict gender for 'presenter' and calculate GPI
def predict_gender_from_name(name):
    # Check if 'name' is a string
    if isinstance(name, str):
        # Split the name and predict gender using the first part
        return detector.get_gender(name.split()[0])
    else:
        # Return a default value or handle the case where 'name' is not a string
        return 'unknown'  # Or any other default value you prefer

def calculate_adjusted_gpi(entities_list):
    gender_counts = {'male': 0, 'female': 0}
    for _, _, gender in entities_list:
        if gender in gender_counts:
            gender_counts[gender] += 1
    total = gender_counts['male'] + gender_counts['female']
    return (gender_counts['female'] - gender_counts['male']) / total if total > 0 else 0

data_df['presenter_gender'] = data_df['presenter'].apply(predict_gender_from_name)
print("presentator gender ok")
data_df['gpi'] = data_df['entities_and_pronouns_in_descriptions'].apply(calculate_adjusted_gpi)
print("gpi ok")
# Save the updated DataFrame
data_df.to_csv("/home/data/ter_meduse_log/mdw_2024/data/datasets/concat_all_with_gpi.csv")
