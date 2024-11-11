# Sentiment Analysis using Python

This is a sentiment analysis python script that uses Natural Language Toolkit (nltk), Langauge Detection (langdetect) and Google Translate (googletrans) to process textual feedback data.

# Prerequitites

1. You will have to have python 3.11 installed on your computer. **Download**: https://www.python.org/downloads/
2. Make sure that the path value has been set for python: **Guide**: https://realpython.com/installing-python/
3. You will have to install the required libraries used in this script.
   > On the command line, type this command to download and install libraries (ps: multiprocessing library is preinstalled with Python):
   > `pip install nltk langdetect googletrans spellchecker`

Lets check if our environment is setup properly: https://realpython.com/installing-python/#how-to-check-your-python-version-on-windows

# How to use it?

Very simple:

1. Fork this repository so that you can save it to your profile
2. Download clone the repo on your computer
3. Open VS Code and open/navigate to the cloned repo on your computer
4. On the terminal, provide this command and hit enter (vals in <> indicate areguments, do not include the symbols <>):
   > **`python sentiment_analysis.py <csv_file_path> <text_column_name> <output_prefix> <limit_rows:-y/-n>`**
   > a. **csv_file_path**: relative file path to csv containing data to be processed.
   > b. **text_column_name**: the name of the column/header containing the textual data to be processed.
   > c. **output_prefix**: this is the prefix/title that will be appended to the start of the name of the output file.
   > d. **limit_rows**: this is the switch to limit the rows to be processed to 100 and is used for debugging the script. Use -y for yes and -n for no.
5. The script will process the data and provide outputs on the terminal.
6. Processing speed is dependedent on internet connection, cpu cores & computer specs, and # and intensity of processes running on your computer.
