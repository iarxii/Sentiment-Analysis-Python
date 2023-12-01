# code updated on 16/11/2023 # import nltk

import csv
import sys
import datetime
from tabulate import tabulate
from nltk.sentiment import SentimentIntensityAnalyzer
from langdetect import detect
from googletrans import Translator
from spellchecker import SpellChecker
import time

# Function to read data from CSV file
def read_csv(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as csv_file:
        csv_reader = csv.reader(csv_file)
        # Assuming the first row contains headers
        headers = next(csv_reader)
        # Read the rest of the data
        data = list(csv_reader)
    return headers, data

# Function to perform sentiment analysis
def analyze_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    sentiment_score = sid.polarity_scores(text)
    return sentiment_score['compound']

# Function to detect language and translate if necessary
def detect_and_translate(text):
    try:
        # Detect the language of the text
        source_language = detect(text)

        # If the detected language is not English, translate the text to English
        if source_language != 'en':
            translator = Translator()
            translation = translator.translate(text, src=source_language, dest='en')
            translated_text = translation.text
            return translated_text
        else:
            return text
    except Exception as e:
        print(f"Error during language detection or translation: {e}")
        return text

# Function to check spelling errors
def check_spelling(text):
    spell = SpellChecker()
    # Find misspelled words
    misspelled = spell.unknown(text.split())
    return list(misspelled)

# Function to write data to CSV file with timestamp
def write_to_csv_with_timestamp(data, headers):
    # Generate a timestamp for the file name
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    # Construct the file name
    output_csv_file_path = f'output_{timestamp}.csv'
    
    # Specify 'utf-8-sig' encoding to handle BOM
    with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write headers
        csv_writer.writerow(headers)
        # Write data
        csv_writer.writerows(data)

    return output_csv_file_path

# Check if a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python your_script.py <csv_file_path>")
    sys.exit(1)

# Retrieve the CSV file path from the command-line argument
csv_file_path = "./" + sys.argv[1]

# Record the start time
start_time = time.time()

# Read data from CSV file with specified encoding
headers, data = read_csv(csv_file_path, encoding='utf-8')

# Add new columns for sentiment analysis results, translated text, and misspelled words
headers.append('Sentiment Score')
headers.append('Translated Text')
headers.append('Misspelled Words')

# Analyze sentiment, translate, and check spelling for each text in the CSV file
for row in data:
    text = row[4]  # Assuming the text is in the third column (index 2)
    
    # Detect language and translate if necessary
    translated_text = detect_and_translate(text)

    # Analyze sentiment
    sentiment_score = analyze_sentiment(translated_text)

    # Check spelling
    misspelled_words = check_spelling(translated_text)

    row.append(sentiment_score)
    row.append(translated_text)
    row.append(','.join(misspelled_words))

# Record the end time
end_time = time.time()

# Write the table data to the CSV file with timestamp
output_csv_file_path = write_to_csv_with_timestamp(data, headers)

# Calculate and print the duration
duration = end_time - start_time
print(f"Processing time: {duration:.2f} seconds.")

# Print a message indicating the output file path
print(f"Table output has been saved to '{output_csv_file_path}'.")

# user input for indicate end of script execution
input("Press Enter to exit...")

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
