# DPOS analysis command:

`python sentiment_analysis.py raw_data/dpos/exported_dd_MM_YYYY/GDOHPSA_DPOS_Survey_IP_Data_V3.csv patient_comments dpos_analysis_V3_IP -n`

`python sentiment_analysis.py raw_data/dpos/exported_dd_MM_YYYY/GDOHPSA_DPOS_Survey_OP_Data_V3.csv patient_comments dpos_analysis_V3_OP -n`

------------------------------------------------------------------------------------------------------------------------------------------------/

# Ideal analysis command (modify the arguments to point to the desired csv file, column name and output filename prefix):

`python sentiment_analysis.py ./raw_data/ideal/Ideal_Complaints_2023_24.csv 'Summary of Compliment' ideal_analysis_complaints -n`

# TDKE command

`python textual_data_keyword_extractor.py ./raw_data/tdke_input/<excel file name.csv> 'column name' output_file_prefix -n`
