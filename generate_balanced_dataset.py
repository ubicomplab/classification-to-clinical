import os
import random
import numpy as np
import pandas as pd
import argparse


def save_samples(file_list, src_folder, dest_folder):

    for file in file_list:
        df = pd.read_csv(os.path.join(src_folder, file))
        duration_index = df[(df["depression"] == True) | (df["depression"] == False)].index
        duration_df = df.loc[(duration_index[-2] - 27) : duration_index[-2]]
        duration_df.to_csv(os.path.join(dest_folder, file), index=False)

def split_sample_years(samples):
    year2 = list()
    year3 = list()
    year4 = list()
    # split the data by years
    for i in range(len(samples)):
        pid_no = int(samples[i].split(".")[0].split("#")[0].split("_")[1])
        if pid_no < 600:
            year2.append(samples[i])
        elif pid_no < 900:
            year3.append(samples[i])
        else:
            year4.append(samples[i])
    
    return year2, year3, year4


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="settings")
    parser.add_argument("-d", "--data_path", type=str, default="./tmp_data", help="generated_dataset_path")
    parser.add_argument("-s", "--save_path", type=str, default="./tmp_data", help="save_path")
    opt = parser.parse_args()
    data_path = opt.data_path
    save_path = opt.save_path    
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    pid_file_list = os.listdir(data_path)
    pid_file_list = sorted(pid_file_list)
    positive_label = list()
    negative_label = list()

    for pid_file in pid_file_list:
        df = pd.read_csv(os.path.join(data_path, pid_file))
        duration_index = df[(df["depression"] == True) | (df["depression"] == False)].index
        if np.isnan(df.loc[(duration_index[-2]), "phq4"]):
            continue
        if df.loc[(duration_index[-2]), "phq4"] > 0 and df.loc[(duration_index[-2]), "phq4"] < 6:
            continue
        depression_label = df.loc[(duration_index[-2]), "depression"]

        if depression_label == True:
            positive_label.append(pid_file)
        else:
            negative_label.append(pid_file)

    # split the data by years
    pos2, pos3, pos4 = split_sample_years(positive_label)
    neg2, neg3, neg4 = split_sample_years(negative_label)
    # sample balanced data
    random_choices = random.sample(pos2, k=15)
    save_samples(random_choices, data_path, save_path)
    random_choices = random.sample(pos3, k=15)
    save_samples(random_choices, data_path, save_path)
    random_choices = random.sample(pos4, k=15)
    save_samples(random_choices, data_path, save_path)
    random_choices = random.sample(neg2, k=15)
    save_samples(random_choices, data_path, save_path)
    random_choices = random.sample(neg3, k=15)
    save_samples(random_choices, data_path, save_path)
    random_choices = random.sample(neg4, k=15)
    save_samples(random_choices, data_path, save_path)
