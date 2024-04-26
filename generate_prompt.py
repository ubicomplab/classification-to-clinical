import os
import argparse
import json
import pandas as pd


def markdown_refine(markdown_table):
    """
    Refine markdown format
    """
    # Split the markdown code into lines
    lines = markdown_table.split('\n')
    # Remove the second line (index 1)
    lines.pop(1)
    for i, line in enumerate(lines):
        if line.startswith('|'):
            line = line[1:]
        if '|' in line:
            lines[i] = '|'.join(segment.strip() for segment in line.split('|'))
    # Join the lines back together to get the modified markdown
    modified_markdown = '\n'.join(lines)
    return modified_markdown

def generate_prompt(df, prompt, to_markdown, version):
    """
    Generate prompt samples
    """
    prompt_start = prompt["prompt_start"]
    prompt_task_describe = prompt["prompt_task_describe"]
    prompt_outline = prompt["prompt_outline"]
    prompt_outline_explanation = prompt["prompt_outline_explanation"]
    prompt_outline_complete = prompt["prompt_outline_complete"]
    data_col = prompt["data_col"]
    instructions = prompt["instructions"]
    variable_concept = prompt["variable_concept"]
    dsm = prompt["dsm"]

    duration_index = df[(df["depression"] == True) | (df["depression"] == False)].index
    depression_label = df.loc[(duration_index[0]), "depression"]
    df = df.drop(["phq4", "depression", "anxiety_sub", "depress_sub"], axis=1)

    if to_markdown:
        df = df.to_markdown(index=False)
        df = markdown_refine(df)

    if version == "a":
        prompt_sample = f"{prompt_start} \n{prompt_task_describe} \n{prompt_outline} \n{data_col} \n{df} \n{instructions}"
    elif version == "b":
        prompt_sample = f"{prompt_start} \n{prompt_task_describe} \n{prompt_outline_explanation} \n{data_col} \n{df} \n{variable_concept} \n{instructions}"
    elif version == "c":
        prompt_sample = f"{prompt_start} \n{prompt_task_describe} \n{prompt_outline_complete} \n{data_col} \n{df} \n{variable_concept} \n{dsm} \n{instructions}"
    else:
        print("Wrong Prompt Version! Please check!")
    return prompt_sample, depression_label

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="settings")
    parser.add_argument("-d", "--data_path", type=str, default="./tmp_data", help="generated_dataset_path")
    parser.add_argument("-p", "--prompt_path", type=str, default="./tmp_data", help="prompt_content_path")
    parser.add_argument("-s", "--save_path", type=str, default="./tmp_data", help="save_path")
    parser.add_argument("-m", "--to_markdown", type=bool, default=True, help="use markdown format")
    parser.add_argument("-c", "--version", type=str, default="a", help="choose the prompt version")
    opt = parser.parse_args()
    data_path = opt.data_path
    prompt_path = opt.prompt_path
    save_path = opt.save_path
    to_markdown = opt.to_markdown
    version = opt.version

    with open(prompt_path, 'r', encoding='utf-8') as file:
        prompt = json.load(file)
    
    prompt_samples = dict()
    data_list = os.listdir(data_path)
    for data_file in data_list:
        df = pd.read_csv(os.path.join(data_path, data_file))
        pid = data_file.split("#")[0]
        prompt_sample, label = generate_prompt(df, prompt, to_markdown, version)
        prompt_samples[pid] = dict()
        prompt_samples[pid]["prompt"] = prompt_sample
        prompt_samples[pid]["label"] = label
    
    with open(save_path, 'w', encoding='utf-8') as file:
        json.dump(prompt_samples, file, indent=4)
    
    print(f"Prompts are successfully generated at {save_path}")