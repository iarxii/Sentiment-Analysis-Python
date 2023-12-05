# code updated on 30/11/2023 # import nltk

# from tabulate import tabulate
import os
from nltk.sentiment import SentimentIntensityAnalyzer
from langdetect import detect
from googletrans import Translator
from spellchecker import SpellChecker
from multiprocessing import Pool #deprecated
import csv
import datetime
import time
import sys
import concurrent.futures

# Function to read data from CSV file
def read_csv(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as csv_file:
        # csv_reader = csv.reader(csv_file)
        # Assuming the first row contains headers
        # headers = next(csv_reader)
        # Read the rest of the data
        # data = list(csv_reader)

        # copilot suggestion
        csv_reader = csv.DictReader(csv_file)
        headers = csv_reader.fieldnames
        data = [row for row in csv_reader]
    return headers, data

# Function to perform sentiment analysis
def analyze_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    sentiment_score = sid.polarity_scores(text)
    return sentiment_score['compound']

# Function to detect language and translate if necessary
def detect_and_translate(text):
    try:
        # If the text is empty or is "no comment" / "no comments", return it without translation
        if text == '' or text.lower() == 'no comment' or text.lower() == 'no comments':
            return text
        
        # convert text to normal case
        text = text.lower().capitalize()

        # Detect the language of the text
        source_language = detect(text)

        # If the detected language is not English, translate the text to English
        if source_language != 'en':
            print(f"Detected language: {source_language}") # debug
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
    
    # Correct misspelled words
    corrected_text = []
    for word in text.split():
        if word in misspelled:
            corrected_text.append(spell.correction(word))
        else:
            corrected_text.append(word)
    
    # copilot suggestion:
    corrected_text = [word for word in corrected_text if word is not None]
    return ' '.join(corrected_text), list(misspelled)

# Analyze sentiment, translate, and check spelling for each text in the CSV file
# for row in data:
# function that will be run in multiple processes.
def process_row(row):
    try:
        print(row) # debug
        # print the interation number
        print(f">>> Row iteration: {data.index(row)+1}") # debug

        # If text_column_index is 4, and you're using it to index into the row dictionary, 
        # that's likely the cause of the error. When you read a CSV file into a dictionary 
        # using csv.DictReader, the keys in the dictionary are the column names, not the 
        # column indices. So you should use the column name to access the value:
        # text = row[text_column_index] # deprecated
        text = row[text_column_name]

        # Check spelling and correct misspelled words
        corrected_text, misspelled_words = check_spelling(text)

        # Detect language and translate if necessary
        translated_text = detect_and_translate(corrected_text)

        # Analyze sentiment
        sentiment_score = analyze_sentiment(translated_text)

        row['sentiment_score'] = sentiment_score
        row['translated_text'] = translated_text
        row['misspelled_words'] = ','.join(misspelled_words)

        # Check if any of the fields are blank
        # if not sentiment_score or not translated_text or not misspelled_words:
        #     return None

        return row
    except Exception as e:
        print(f"Error processing row {row}: {e}")
        return None

# Function to write data to CSV file with timestamp
def write_to_csv_with_timestamp(data, headers, output_prefix):
    # Check if any of the processed rows are None
    # if any(row is None for row in data):
    #     return None
    
    # Generate a timestamp for the file name
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    # Construct the output path and file name
    output_csv_file_path = f'./output/{output_prefix}_output_{timestamp}.csv'
    
    # Specify 'utf-8-sig' encoding to handle BOM
    with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
        # csv_writer = csv.writer(csv_file)
        csv_writer = csv.DictWriter(csv_file, fieldnames=headers)

        # Write headers
        # csv_writer.writerow(headers)
        csv_writer.writeheader()

        # Write data
        # csv_writer.writerows(data)
        for row in data:
            csv_writer.writerow(row)

    return output_csv_file_path

# Check if command-line arguments are provided
if len(sys.argv) != 4:
    print("Usage: python your_script.py <csv_file_path> <text_column_name> <output_prefix>")
    sys.exit(1)

# The first item, sys.argv[0], is the name of the script itself. The subsequent items are the arguments you passed.
# Retrieve command-line arguments [1]
csv_file_path = sys.argv[1]
# csv_file_path = "test_data_OP_V3.csv" # debug

# Retrieve command-line arguments [2]
text_column_name = sys.argv[2]
# text_column_name = "patient_comments" # debug

# Retrieve output file prefix command-line arguments [3]
output_prefix = sys.argv[3]
# output_prefix = "whatkindof" # debug

# Record the start time
start_time = time.time()

# Read data from CSV file with specified encoding
headers, data = read_csv(csv_file_path, encoding='utf-8')

# Find the index of the column with the specified name
try:
    text_column_index = headers.index(text_column_name)
except ValueError:
    print(f"Column '{text_column_name}' not found in the CSV file.")
    sys.exit(1)

# Add new columns for sentiment analysis results, translated text, and misspelled words
headers.extend(['sentiment_score', 'translated_text', 'misspelled_words'])

num_processes = os.cpu_count()
print(f">>> CPU - Number of processes/cores: {num_processes}") #debug

if __name__ == "__main__":
    #***deprecated # multiprocessing - This is necessary on Windows to avoid recursive launching of subprocesses 
    with Pool(processes=num_processes) as p:
        data = p.map(process_row, data)
    
    # concurrent.futures.ProcessPoolExecutor #does the same thing as multiprocessing.Pool but it crashes on the main thread
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     data = list(executor.map(process_row, data))

# Record the end time
end_time = time.time()

# Write the table data to the CSV file with timestamp
output_csv_file_path = write_to_csv_with_timestamp(data, headers, output_prefix)

# Check if the output file path is None
if output_csv_file_path is None:
    print(f"Error writing to CSV file.")
else:
    print(f"Table output has been saved to '{output_csv_file_path}'.")

# Calculate and print the duration of the script execution
duration = end_time - start_time
# calcule the duration in minutes
print(f"Processing time (sec): {duration:.2f} seconds.")
# calcule the duration in minutes
duration /= 60
duration_min = duration
print(f"Processing time (min): {duration:.2f} minutes.")
# calcule the duration in hours
duration /= 60
duration_hrs = duration
print(f"Processing time (hrs): {duration:.2f} hours.")

# user input for indicate end of script execution
input(f"Press Enter to exit...")

# save to a log file with the script execution details, if log file is not found, it will be created
with open('./log/log.txt', 'a') as log_file:
    log_file.write(f"Script execution details:\n")
    # datetime object containing current date and time
    now = datetime.datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    log_file.write(f"Date and time: {dt_string}\n")
    log_file.write(f"CSV file path: {csv_file_path}\n")
    log_file.write(f"Text column name: {text_column_name}\n")
    log_file.write(f"Output prefix: {output_prefix}\n")
    log_file.write(f"Number of processes/cores: {num_processes}\n")
    log_file.write(f"Number of rows processed: {len(data)}\n")
    log_file.write(f"Processing time (sec): {duration:.2f} seconds.\n")
    log_file.write(f"Processing time (min): {duration_min:.2f} minutes.\n")
    log_file.write(f"Processing time (hrs): {duration_hrs:.2f} hours.\n")
    log_file.write(f"Table output has been saved to '{output_csv_file_path}'.\n")
    log_file.write(f"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
