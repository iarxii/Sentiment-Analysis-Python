import csv
import os
import sys
import time
import datetime

def print_tdke():
    tdke_art = """
          _____                    _____                    _____                    _____          
         /\    \                  /\    \                  /\    \                  /\    \         
        /::\    \                /::\    \                /::\____\                /::\    \        
        \:::\    \              /::::\    \              /:::/    /               /::::\    \       
         \:::\    \            /::::::\    \            /:::/    /               /::::::\    \      
          \:::\    \          /:::/\:::\    \          /:::/    /               /:::/\:::\    \     
           \:::\    \        /:::/  \:::\    \        /:::/____/               /:::/__\:::\    \    
           /::::\    \      /:::/    \:::\    \      /::::\    \              /::::\   \:::\    \   
          /::::::\    \    /:::/    / \:::\    \    /::::::\____\________    /::::::\   \:::\    \  
         /:::/\:::\    \  /:::/    /   \:::\ ___\  /:::/\:::::::::::\    \  /:::/\:::\   \:::\    \ 
        /:::/  \:::\____\/:::/____/     \:::|    |/:::/  |:::::::::::\____\/:::/__\:::\   \:::\____|
       /:::/    \::/    /\:::\    \     /:::|____|\::/   |::|~~~|~~~~~     \:::\   \:::\   \::/    /
      /:::/    / \/____/  \:::\    \   /:::/    /  \/____|::|   |           \:::\   \:::\   \/____/ 
     /:::/    /            \:::\    \ /:::/    /         |::|   |            \:::\   \:::\    \     
    /:::/    /              \:::\    /:::/    /          |::|   |             \:::\   \:::\____\    
    \::/    /                \:::\  /:::/    /           |::|   |              \:::\   \::/    /    
     \/____/                  \:::\/:::/    /            |::|   |               \:::\   \/____/     
                               \::::::/    /             |::|   |                \:::\    \         
                                \::::/    /              \::|   |                 \:::\____\        
                                 \::/____/                \:|   |                  \::/    /        
                                  ~~                       \|___|                   \/____/         
                                   Textual Data Keyword Extractor                                   
    """
    print(tdke_art)

def extract_records(input_csv_file, output_csv_file, keywords, limit_rows, text_column_name):
    extracted_records = []

    with open(input_csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if limit_rows == '-y':
            for i, row in enumerate(reader):
                if i >= 100:  # Limit rows to 100
                    break
                text = row[text_column_name]  # Column containing the processed textual data
                if any(keyword.lower() in text.lower() for keyword in keywords):
                    extracted_records.append(row)
        else:
            for row in reader:
                text = row[text_column_name]  # Column containing the processed textual data
                if any(keyword.lower() in text.lower() for keyword in keywords):
                    extracted_records.append(row)

    if extracted_records:
        headers = extracted_records[0].keys()
        output_dir = './output/tdke/'
        os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist
        with open(os.path.join(output_dir, output_csv_file), 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(extracted_records)
        print(f"Extracted records containing keywords {keywords} saved to {output_csv_file}")
    else:
        print("No records containing the specified keywords found.")

    # Record the end time
    end_time = time.time()

    # Calculate and print the duration of the script execution
    duration = end_time - start_time
    # Calculate the duration in minutes
    duration_min = duration / 60
    # Calculate the duration in hours
    duration_hrs = duration_min / 60

    # Save to a log file with the script execution details
    log_file_path = './log/log.txt'
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"Script execution details:\n")
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        log_file.write(f"*** TDKE Script Log item ***\n")
        log_file.write(f"Date and time: {dt_string}\n")
        log_file.write(f"CSV file path: {input_csv_file}\n")
        log_file.write(f"Text column name: {text_column_name}\n")
        log_file.write(f"Output prefix: {output_csv_file}\n")
        log_file.write(f"Number of rows processed: {i + 1 if limit_rows == '-y' else 'all'}\n")
        log_file.write(f"Processing time (sec): {duration:.2f} seconds.\n")
        log_file.write(f"Processing time (min): {duration_min:.2f} minutes.\n")
        log_file.write(f"Processing time (hrs): {duration_hrs:.2f} hours.\n")
        log_file.write(f"Table output has been saved to '{os.path.join(output_dir, output_csv_file)}'.\n")
        log_file.write(f"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")

if __name__ == "__main__":
    print_tdke()

    if len(sys.argv) != 5:
        print("Usage: python your_script.py <csv_file_path> <text_column_name> <output_prefix> <limit_rows:-y/-n>")
        sys.exit(1)

    start_time = time.time()

    csv_file_path = sys.argv[1]
    text_column_name = sys.argv[2]
    output_prefix = sys.argv[3]
    now = datetime.datetime.now()
    output_prefix += now.strftime("_%Y%m%d%H%M%S")
    limit_rows = sys.argv[4]

    input_csv_file = csv_file_path
    output_csv_file = f'{output_prefix}_extracted_records.csv'
    keywords = ['fall', 'falls', 'pressure', 'sore', 'sores', 'pressure injuries', 'pressure sores', 'abscond', 'absconded', 'abscondment', 'abscondments']

    extract_records(input_csv_file, output_csv_file, keywords, limit_rows, text_column_name)
