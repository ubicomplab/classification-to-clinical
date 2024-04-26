#!/bin/bash
# The folder path of the pickel files after preparation of Globem
GLOBEM_RAW_DATA_PATH=/YOUR_PATH_TO_GLOBEM/data/datarepo_max_feature_types
# The folder path to save sliced csv data
SAVED_CSV_DATA_PATH=./csv_data
# The folder path to save preprocessed testset data
SAVED_TESTSET_PATH=./testset
# The file path of template prompt json 
TEMPLATE_PROMPT_PATH=./prompts/template_prompt.json
# The file path of generated prompt json
GENERATED_PROMPT_PATH=./prompts/generated_prompts.json
# The output prompt version
PROMPT_VERSION=b

# First preprocess the data from Globem
python generate_sliced_data.py --save_path $SAVED_CSV_DATA_PATH --pickle_path $GLOBEM_RAW_DATA_PATH
# Second sampling the balanced dataset from the preprocessed data
python generate_balanced_dataset.py --data_path $SAVED_CSV_DATA_PATH --save_path $SAVED_TESTSET_PATH
# Third generate final prompts from the templates and the preprocessed data
python generate_prompt.py --data_path $SAVED_TESTSET_PATH --prompt_path $TEMPLATE_PROMPT_PATH --save_path $GENERATED_PROMPT_PATH --version $PROMPT_VERSION
