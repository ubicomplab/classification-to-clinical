### This is the code base for the IMWUT submission of the paper:
> From Classification to Clinical Insights: Towards Analyzing and Reasoning About Mobile and Behavioral Health Data With Large Language Models

### Enviroment Setup and Raw Data Preparation
We use Globem as our dataset for the experiments in the paper. 
To setup the enviroment and prepare raw data, you can follow the instructions in the `<Globem Github Repo>` : <https://github.com/UW-EXP/GLOBEM>

### Reproduce the Prompts in the experiments
To reproduce our prompt, you need to set some configuration in the `run.sh` script first. 
```
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
```
For the parameter of PROMPT_VERSION, you can check the following table:

| Prompt Version in the paper  | Parameter |
| ------------- | ------------- |
| CoT  | a  |
| CoT + Exp.  | b  |
| CoT + Exp. + DSM  | c  |

After setting the configuration, try the following command to generate the prompts.
```
bash run.sh
```