import csv
import sys
import datetime
from tabulate import tabulate
# import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# nltk.download('vader_lexicon')

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

# CSV file path (deprecated)
# csv_file_path = './GDoHPSA_DPOS_Survey_IP_Data.csv'

# Read data from CSV file with specified encoding
headers, data = read_csv(csv_file_path, encoding='utf-8')

# Add a new column for sentiment analysis results
headers.append('Sentiment Score')

# Analyze sentiment for each text in the CSV file
for row in data:
    text = row[4]  # Assuming the text is in the third column (index 2)
    sentiment_score = analyze_sentiment(text)
    row.append(sentiment_score)

# Write the table data to the CSV file with timestamp
output_csv_file_path = write_to_csv_with_timestamp(data, headers)

# Optional: Print a message indicating the output file path
print(f"Table output has been saved to '{output_csv_file_path}'.")

# Add this line at the end
input("Press Enter to exit...")
