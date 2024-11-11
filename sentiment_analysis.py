# code updated on 17/01/2024 

# from tabulate import tabulate
import os
# import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from langdetect import detect
from googletrans import Translator
from spellchecker import SpellChecker
from multiprocessing import Pool #deprecated
import datetime
import time
import sys
import os
import csv
# import concurrent.futures

# define lexicons
healthcare_lexicon_positive = {
    # Positive values
    'Hygienic facilities': 0.8,
    'Sterilized equipment': 0.8,
    'Sanitized surfaces': 0.7,
    'Regular cleaning': 0.7,
    'Pleasant environment': 0.8,
    'Pest-free': 0.8,
    'Short wait times': 0.9,
    'Efficient scheduling': 0.8,
    'Timely updates': 0.8,
    'Comfortable waiting areas': 0.8,
    'Entertainment options': 0.7,
    'Compassionate staff': 0.9,
    'Attentive nurses': 0.9,
    'Respectful doctors': 0.8,
    'Effective communication': 0.8,
    'Clear explanations': 0.8,
    'Personalized care': 0.9,
    'Follow-up appointments': 0.8,
    'Emotional support': 0.9,
    'Efficient recordkeeping': 0.8,
    'Organized systems': 0.8,
    'Electronic records': 0.8,
    'Secure storage': 0.8,
    'Prompt retrieval': 0.8,
    'Adequate stock': 0.8,
    'Timely refills': 0.8,
    'Clear instructions': 0.8,
    'Effective medications': 0.8,
    'Affordable options': 0.8,
    'Side-effect management': 0.8,
    'Assisted toileting': 0.7,
    'Clean linens': 0.8,
    'Comfortable facilities': 0.8,
    'Respectful care': 0.8,
    'Privacy': 0.8,
    'Clear explanations': 0.8,
    'Educational materials': 0.8,
    'Access to information': 0.8,
    'Support groups': 0.7,
    'Workshops': 0.7,
    'Individual counseling': 0.8,
    
    # Positive sentiments
    'Delighted': 0.9,
    'Thrilled': 0.9,
    'Impressed': 0.8,
    'Exceptional': 0.8,
    'Outstanding': 0.8,
    'Grateful': 0.9,
    'Appreciative': 0.9,
    'Relieved': 0.9,
    'Confident': 0.8,
    'Secure': 0.8,
    'Empowered': 0.8,
    'Competent': 0.8,
    'Efficient': 0.8,
    'Knowledgeable': 0.8,
    'Helpful': 0.8,
    'Proactive': 0.8,
    'Dedicated': 0.8,
    'Caring': 0.9,
    'Understanding': 0.9,
    'Empathetic': 0.9,
    'Trustworthy': 0.8,
    'Reliable': 0.8,
    'Respectful': 0.9,
    'Dignified': 0.9,
    'Comfortable': 0.8,
    'Safe': 0.8,
    'Alleviated': 0.8,
    'Healed': 0.9,
    'Cured': 0.9,
    'Recovered': 0.9,
    'Thriving': 0.8,
    'Timely': 0.8,
    'Convenient': 0.8,
    'Easy': 0.8,
    'Assistance': 0.8,
    'Aid': 0.8,
    'Accepted': 0.8,
    'Availability': 0.8,
    'Multilingual': 0.8,
    'Pleased': 0.8,
    'Satisfied': 0.8,
    'Improved': 0.8,
    'Beneficial': 0.8,
    'Hopeful': 0.8,
    'Optimistic': 0.8,
    'Adequate': 0.8,
    'Competent': 0.8,
    'Friendly': 0.8,
    'Courteous': 0.8,
    'Polite': 0.8,
    'Supportive': 0.8,
    'Informative': 0.8,
    'Engaged': 0.8,
    'Timely': 0.8,
    'Responsive': 0.8,
    'Accessible': 0.8,
    'Convenient': 0.8,
    'Affordable': 0.8,
    'Cost-effective': 0.8,
    'Valuable': 0.8,
    'Worthwhile': 0.8,
}

healthcare_lexicon_negative = {
    # Negative values
    'Dirty facilities': -0.8,
    'Unhygienic equipment': -0.8,
    'Unsanitary surfaces': -0.7,
    'Infrequent cleaning': -0.7,
    'Unpleasant odors': -0.8,
    'Pest problems': -0.8,
    'Housekeeping': -0.7,
    'Disinfection': -0.7,
    'Sanitation protocols': -0.7,
    'Inspections': -0.7,
    'Long wait times': -0.9,
    'Delays': -0.8,
    'Lack of communication': -0.8,
    'Uncomfortable waiting areas': -0.8,
    'Limited amenities': -0.7,
    'Uncaring staff': -0.9,
    'Inattentive nurses': -0.9,
    'Dismissive doctors': -0.8,
    'Poor communication': -0.8,
    'Confusing explanations': -0.8,
    'Impersonal care': -0.9,
    'Lack of follow-up': -0.8,
    'Emotional neglect': -0.9,
    'Lost files': -0.8,
    'Inaccurate information': -0.8,
    'Incomplete records': -0.8,
    'Disorganized systems': -0.8,
    'Paper-based records': -0.8,
    'Delayed retrieval': -0.8,
    'Stock shortages': -0.8,
    'Delays in refills': -0.8,
    'Unclear instructions': -0.8,
    'Ineffective medications': -0.8,
    'High cost': -0.8,
    'Adverse side effects': -0.8,
    'Unassisted toileting': -0.7,
    'Dirty linens': -0.8,
    'Uncomfortable facilities': -0.8,
    'Disrespectful care': -0.8,
    'Lack of privacy': -0.8,
    'Confusing explanations': -0.8,
    'Lack of information': -0.8,
    'Limited resources': -0.8,
    'Inaccessible support groups': -0.8,
    'Unavailable counseling': -0.8,

    # Negative sentiments
    'Unsatisfied': -0.8,
    'Disappointed': -0.8,
    'Discontented': -0.8,
    'Concerned': -0.8,
    'Worried': -0.8,
    'Anxious': -0.8,
    'Frustrated': -0.9,
    'Inconvenienced': -0.8,
    'Impatient': -0.8,
    'Delayed': -0.8,
    'Uncomfortable': -0.8,
    'Inadequate': -0.8,
    'Incompetent': -0.8,
    'Unfriendly': -0.8,
    'Dismissive': -0.8,
    'Unhelpful': -0.8,
    'Uninformed': -0.8,
    'Unresponsive': -0.8,
    'Inaccessible': -0.8,
    'Inconvenient': -0.8,
    'Unaffordable': -0.8,
    'Overpriced': -0.8,
    'Unfair': -0.8,
    'Deceptive': -0.8,
    'Misleading': -0.8,
    'Questionable': -0.8,
    'Harmful': -0.8,
    'Worsening': -0.8,
    'Deteriorating': -0.8,
    'Declining': -0.8,
    'Failing': -0.8,
    'Long': -0.8,
    'Wait': -0.8,
    'Limited': -0.8,
    'Distant': -0.8,
    'Distance': -0.8,
    'Complex': -0.8,
    'Lack': -0.8,
    'Burden': -0.8,
    'Restricted': -0.8,
    'Cancellations': -0.8,
    'Barriers': -0.8,

    # More negative sentiments
    'Frustrated': -0.9,
    'Angry': -0.9,
    'Outraged': -0.9,
    'Horrified': -0.9,
    'Appalled': -0.9,
    'Disappointed': -0.9,
    'Dismayed': -0.9,
    'Neglected': -0.9,
    'Abandoned': -0.9,
    'Ignored': -0.9,
    'Violated': -0.9,
    'Traumatized': -0.9,
    'Unsafe': -0.9,
    'Threatened': -0.9,
    'Helpless': -0.9,
    'Incompetent': -0.9,
    'Incapable': -0.9,
    'Negligent': -0.9,
    'Careless': -0.9,
    'Disrespectful': -0.9,
    'Abusive': -0.9,
    'Discrimination': -0.9,
    'Discriminatory': -0.9,
    'Humiliating': -0.9,
    'Humiliation': -0.9,
    'Dehumanized': -0.9,
    'Dehumanize': -0.9,
    'Exploited': -0.9,
    'Exploit': -0.9,
    'Scam': -0.9,
    'Scammed': -0.9,
    'Overcharged': -0.9,
    'Bankrupted': -0.9,
    'Financially ruined': -0.9,
    'Suffering': -0.9,
    'Worsening': -0.9,
    'Deteriorating': -0.9,
    'Declining': -0.9,
    'Failing': -0.9,
    'Fatal': -0.9,
    'Lethal': -0.9,
    'Bugs': -0.9,
    'Cockroach': -0.9,
    'Cockroaches': -0.9,
    'Flies': -0.9,
    'Dirty': -0.9,
    'Unclean': -0.9,
    'Attitude': -0.9,
    'Swear': -0.9,
    'Bully': -0.9,
    'Bullied': -0.9,
    'Confront': -0.9,
    'Disrespect': -0.9,
    'Disrespectful': -0.9,
}

healthcare_lexicon_neutral = {
    # Neutral values
    'Referral': 0.0,
    'Process': 0.0,
    'Eligibility': 0.0,
    'Requirements': 0.0,
    'Appointment': 0.0,
    'Confirmation': 0.0,
    'Waitlist': 0.0,
    'Triage': 0.0,
    'Intake': 0.0,
    'Check-in process': 0.0,
    'Estimated wait time': 0.0,
    'Appointment reminders': 0.0,
    'Seating arrangements': 0.0,
    'Bedside manner': 0.0,
    'Patient-centered care': 0.0,
    'Treatment options': 0.0,
    'Informed consent': 0.0,
    'Shared decision-making': 0.0,
    'Discharge planning': 0.0,
    'Documentation': 0.0,
    'Filing': 0.0,
    'Archiving': 0.0,
    'Data entry': 0.0,
    'Backups': 0.0,
    'Audits': 0.0,
    'Prescriptions': 0.0,
    'Dispensaries': 0.0,
    'Dosage': 0.0,
    'Administration': 0.0,
    'Monitoring': 0.0,
    'Adherence': 0.0,
    'Hygiene assistance': 0.0,
    'Continence care': 0.0,
    'Bathing': 0.0,
    'Toileting facilities': 0.0,
    'Privacy curtains': 0.0,
    'Health literacy': 0.0,
    'Informed consent': 0.0,
    'Decision-making support': 0.0,
    'Patient portals': 0.0,
    'Educational resources': 0.0,

    # Expanded neutral values
    'Clinic': 0.0,
    'Hospital': 0.0,
    'Emergency room': 0.0,
    'Urgent care': 0.0,
    'Surgery center': 0.0,
    'Diagnostic center': 0.0,
    'Laboratory': 0.0,
    'Pharmacy': 0.0,
    'Rehabilitation center': 0.0,
    'Nursing home': 0.0,
    'Hospice': 0.0,
    'Home care': 0.0,
    'Telehealth': 0.0,
    'Virtual care': 0.0,

    'Doctor': 0.0,
    'Physician': 0.0,
    'Surgeon': 0.0,
    'Specialist': 0.0,
    'Nurse': 0.0,
    'Physician assistant': 0.0,
    'Nurse practitioner': 0.0,
    'Therapist': 0.0,
    'Technician': 0.0,
    'Aide': 0.0,
    'Intern': 0.0,
    'Resident': 0.0,
    'Fellow': 0.0,
    'Administrator': 0.0,
    'Receptionist': 0.0,
    'Billing staff': 0.0,

    'Medication': 0.0,
    'Prescription': 0.0,
    'Diagnosis': 0.0,
    'Test': 0.0,
    'Examination': 0.0,
    'Surgery': 0.0,
    'Therapy': 0.0,
    'Intervention': 0.0,
    'Consultation': 0.0,
    'Referral': 0.0,
    'Monitoring': 0.0,
    'Follow-up': 0.0,
    'Education': 0.0,
    'Counseling': 0.0,
    'Support group': 0.0,

    'Copay': 0.0,
    'Deductible': 0.0,
    'Premium': 0.0,
    'Coinsurance': 0.0,
    'Out-of-pocket': 0.0,
    'Claim': 0.0,
    'Denial': 0.0,
    'Appeal': 0.0,
    'Refund': 0.0,
    'Reimbursement': 0.0,
    'Network': 0.0,
    'Coverage': 0.0,
    'Eligibility': 0.0,
    'Authorization': 0.0,
    'Pre-approval': 0.0,
    'Balance': 0.0,
    'Statement': 0.0,
}

# Merge the lexicons into a comprehensive lexicon
healthcare_lexicon = {**healthcare_lexicon_positive, **healthcare_lexicon_negative, **healthcare_lexicon_neutral}

def print_sa():
    sa_art = r"""
    |_______/\\\\\\\\\\\___________________________________________________________________________________________________________________________|
    |______/\\\/////////\\\________________________________________________________________________________________________________________________|
    |______\//\\\______\///___________________________________/\\\_______/\\\______________________________________________________/\\\____________|
    |________\////\\\_____________/\\\\\\\\___/\\/\\\\\\____/\\\\\\\\\\\_\///_____/\\\\\__/\\\\\_______/\\\\\\\\___/\\/\\\\\\____/\\\\\\\\\\\______|
    |____________\////\\\________/\\\/////\\\_\/\\\////\\\__\////\\\////___/\\\__/\\\///\\\\\///\\\___/\\\/////\\\_\/\\\////\\\__\////\\\////______|
    |________________\////\\\____/\\\\\\\\\\\__\/\\\__\//\\\____\/\\\______\/\\\_\/\\\_\//\\\__\/\\\__/\\\\\\\\\\\__\/\\\__\//\\\____\/\\\_________|
    |__________/\\\______\//\\\__\//\\///////___\/\\\___\/\\\____\/\\\_/\\__\/\\\_\/\\\__\/\\\__\/\\\_\//\\///////___\/\\\___\/\\\____\/\\\_/\\____|
    |__________\///\\\\\\\\\\\/____\//\\\\\\\\\\_\/\\\___\/\\\____\//\\\\\___\/\\\_\/\\\__\/\\\__\/\\\__\//\\\\\\\\\\_\/\\\___\/\\\____\//\\\\\____|
    |____________\///////////_______\//////////__\///____\///______\/////____\///__\///___\///___\///____\//////////__\///____\///______\/////_____|
    |______________________________________________________________________________________________________________________________________________|
    |_______/\\\\\\\\\__________________________________/\\\\\\____________________________________________________________________________________|
    |______/\\\\\\\\\\\\\_______________________________\////\\\___________________________________________________________________________________|
    |______/\\\/////////\\\_________________________________\/\\\_______/\\\__/\\\_______________/\\\______________________________________________|
    |______\/\\\_______\/\\\__/\\/\\\\\\____/\\\\\\\\\_______\/\\\______\//\\\/\\\___/\\\\\\\\\\_\///___/\\\\\\\\\\________________________________|
    |_______\/\\\\\\\\\\\\\\\_\/\\\////\\\__\////////\\\______\/\\\_______\//\\\\\___\/\\\//////___/\\\_\/\\\//////________________________________|
    |________\/\\\/////////\\\_\/\\\__\//\\\___/\\\\\\\\\\_____\/\\\________\//\\\____\/\\\\\\\\\\_\/\\\_\/\\\\\\\\\\______________________________|
    |_________\/\\\_______\/\\\_\/\\\___\/\\\__/\\\/////\\\_____\/\\\_____/\\_/\\\_____\////////\\\_\/\\\_\////////\\\_____________________________|
    |__________\/\\\_______\/\\\_\/\\\___\/\\\_\//\\\\\\\\/\\__/\\\\\\\\\_\//\\\\/_______/\\\\\\\\\\_\/\\\__/\\\\\\\\\\____________________________|
    |___________\///________\///__\///____\///___\////////\//__\/////////___\////________\//////////__\///__\//////////____________________________|
    """
    print(sa_art)

# Function to read data from CSV file
def read_csv(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding, errors='replace') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        headers = csv_reader.fieldnames
        data = [row for row in csv_reader]
    return headers, data

# Function to perform sentiment analysis
def analyze_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    sentiment_score = sid.polarity_scores(text)['compound']
    # return sentiment_score['compound'] # deprecated
    # Custom sentiment analysis using lexicons
    words = text.lower().split()
    custom_sentiment_score = sum(healthcare_lexicon.get(word, 0) for word in words) / max(len(words), 1)

    # Combine the compound score and custom sentiment score (you can adjust weights if needed) - 0.7 (30%) 0.3 (30%)
    combined_score = 0.7 * sentiment_score + 0.3 * custom_sentiment_score
    return combined_score

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

        return row
    except Exception as e:
        print(f"Error processing row {row}: {e}")
        return {
            'sentiment_score': 'x_error',
            'translated_text': 'x_error',
            'misspelled_words': 'x_error'
        }
    
# Function to write data to CSV file with timestamp
def write_to_csv_with_timestamp(data, headers, output_prefix):
    # Check if any of the processed rows are None
    # data = [row for row in data if row is not None]
    # if not data:
    #     return None
    
    # Generate a timestamp for the file name
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    # Construct the output path and file name
    output_csv_file_path = f'./output/{output_prefix}_output_{timestamp}.csv'
    
    # Specify 'utf-8-sig' encoding to handle BOM
    with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=headers)

        # Write headers
        csv_writer.writeheader()

        # Write data
        for row in data:
            if row is not None:  # Check if row is not None
                csv_writer.writerow(row)

    return output_csv_file_path

# Check if command-line arguments are provided
if len(sys.argv) != 5:
    print("Usage: python your_script.py <csv_file_path> <text_column_name> <output_prefix> <limit_rows:-y/-n>")
    sys.exit(1)

# The first item, sys.argv[0], is the name of the script itself. The subsequent items are the arguments you passed.
# Retrieve command-line arguments [1]
csv_file_path = sys.argv[1]

# Retrieve command-line arguments [2]
text_column_name = sys.argv[2]

# Retrieve output file prefix command-line arguments [3]
output_prefix = sys.argv[3]

# argument to limit the rows to process
limit_rows = sys.argv[4] # use for debug

# Record the start time
start_time = time.time()

# Read data from CSV file with specified encoding
headers, data = read_csv(csv_file_path, encoding='utf-8')

# Limit processed rows to 100 if limit_rows value is '-y'
if limit_rows == '-y':
    data = data[:100]

# Find the index of the column with the specified name
try:
    text_column_index = headers.index(text_column_name)
except ValueError:
    print(f"Column '{text_column_name}' not found in the CSV file.")
    sys.exit(1)

# Add new columns for sentiment analysis results, translated text, and misspelled words
headers.extend(['sentiment_score', 'translated_text', 'misspelled_words'])

# Prompt the user for multiprocessing option
use_multiprocessing = input("Do you want to use multiprocessing? (y/n): ")

if use_multiprocessing.lower() == "y":
    num_processes = os.cpu_count()
    print(f">>> CPU - Number of processes/cores: {num_processes}") # debug

    if __name__ == "__main__":
        # print ASCII art
        print_sa()

        #***deprecated # multiprocessing - This is necessary on Windows to avoid recursive launching of subprocesses 
        with Pool(processes=num_processes) as p:
            data = p.map(process_row, data)

    # concurrent.futures.ProcessPoolExecutor #does the same thing as multiprocessing.Pool but it crashes on the main thread
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     data = list(executor.map(process_row, data))
else:
    num_processes = 1
    print(f">>> CPU - Number of processes/cores: {num_processes}") # debug

    if __name__ == "__main__":
        # print ASCII art
        print_sa()

        # Run the process sequentially without multiprocessing
        data = list(map(process_row, data))
        # print(f"data: {data}") # debug
        # sys.exit(1) # debug

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
