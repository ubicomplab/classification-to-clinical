import os
import pandas as pd
import numpy as np
import argparse
from data_loader import data_loader_ml

def delete_folder(folder_path):
    try:
        # Use os.rmdir() to remove an empty folder
        os.rmdir(folder_path)
        # print(f"Folder '{folder_path}' has been deleted successfully.")
    except OSError as e:
        # If the folder is not empty, use os.remove() to delete its contents first
        if e.errno == 39:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    os.remove(os.path.join(root, file))
            os.rmdir(folder_path)
            # print(f"Folder '{folder_path}' and its contents have been deleted successfully.")
        else:
            print(f"Error: {e}")


title_mapping = {
    "date":"date",
    'f_loc:phone_locations_doryab_totaldistance:allday':"total_distance_traveled(meters)",
    'f_loc:phone_locations_doryab_timeathome:allday':"time_at_home(minutes)",
    'f_loc:phone_locations_doryab_locationentropy:allday':"location_entropy",
    'f_screen:phone_screen_rapids_sumdurationunlock:allday':"phone_screen_time(minutes)",
    'f_screen:phone_screen_rapids_avgdurationunlock:allday':"average_phone_use_unlock_duration(minutes)",
    'f_call:phone_calls_rapids_incoming_sumduration:allday':"phone_call_incoming_duration(minutes)",
    'f_call:phone_calls_rapids_outgoing_sumduration:allday':"phone_call_outgoing_duration(minutes)",
    'f_blue:phone_bluetooth_doryab_uniquedevicesothers:allday':"unique_bluetooth_devices_found_nearby",
    'f_steps:fitbit_steps_intraday_rapids_sumsteps:allday':"step_count",
    'f_steps:fitbit_steps_intraday_rapids_countepisodesedentarybout:allday':"number_of_sedentary_episodes",
    'f_steps:fitbit_steps_intraday_rapids_sumdurationsedentarybout:allday':"total_time_spent_sedentary(minutes)",
    'f_steps:fitbit_steps_intraday_rapids_countepisodeactivebout:allday':"number_of_activity_episodes",
    'f_steps:fitbit_steps_intraday_rapids_sumdurationactivebout:allday':"total_time_spent_active(minutes)",
    'f_slp:fitbit_sleep_intraday_rapids_sumdurationasleepunifiedmain:allday':"total_time_asleep(minutes)",
    'f_slp:fitbit_sleep_intraday_rapids_sumdurationawakeunifiedmain:allday':"total_time_spent_awake_while_in_bed(minutes)",
    # 'f_slp:fitbit_sleep_summary_rapids_firstbedtimemain:allday':"bedtime(minutes)",
    # 'f_slp:fitbit_sleep_summary_rapids_firstwaketimemain:allday':'wakebedtime(minutes)',
}

round_list = ['f_loc:phone_locations_doryab_totaldistance:allday', 'f_loc:phone_locations_doryab_timeathome:allday', 'f_screen:phone_screen_rapids_sumdurationunlock:allday', 
              'f_screen:phone_screen_rapids_avgdurationunlock:allday', 'f_call:phone_calls_rapids_incoming_sumduration:allday', 'f_call:phone_calls_rapids_outgoing_sumduration:allday',
              'f_steps:fitbit_steps_intraday_rapids_sumsteps:allday', 'f_steps:fitbit_steps_intraday_rapids_countepisodesedentarybout:allday', 'f_steps:fitbit_steps_intraday_rapids_sumdurationsedentarybout:allday',
              'f_steps:fitbit_steps_intraday_rapids_countepisodeactivebout:allday', 'f_steps:fitbit_steps_intraday_rapids_sumdurationactivebout:allday', 'f_slp:fitbit_sleep_intraday_rapids_sumdurationasleepunifiedmain:allday',
              'f_slp:fitbit_sleep_intraday_rapids_sumdurationawakeunifiedmain:allday']

pd.set_option('display.float_format', '{:.2f}'.format)
placeholder = -1000

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="settings")
    parser.add_argument("-d", "--save_path", type=str, default="./tmp_data", help="temp data folder")
    parser.add_argument("-p", "--pickle_path", type=str, default="./tmp_data", help="pickel folder")
    opt = parser.parse_args()
    save_path = opt.save_path
    pickles_path = opt.pickle_path
    tmp_path = "./tmp"
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    pids = set()
    for pickle_path in os.listdir(pickles_path):
        if "1" in pickle_path:
            continue
        dataset_dict = data_loader_ml.data_loader_raw_single(os.path.join(pickles_path, pickle_path))
        feature_list = list(title_mapping.keys())

        for index, row in dataset_dict.datapoints.iterrows():
            df = row["X_raw"]
            pid = row["pid"]
            date = row["date"]
            date = date.strftime('%Y-%m-%d %H:%M:%S')
            df = df[feature_list]
            df = df.round(2)
            df[round_list] = df[round_list].round(0)
            df = df.rename(columns=title_mapping)
            total_elements = df.size
            total_na = df.isna().sum().sum()
            if (total_na / total_elements) > 0.2:
                continue
            phq_list = [np.nan] * df.shape[0]
            phq_list[-1] = row["y_allraw"]["phq4"]
            anxiety_list = [np.nan] * df.shape[0]
            anxiety_list[-1] = row["y_allraw"]["anx_weekly_subscale"]
            depress_sub_list = [np.nan] * df.shape[0]
            depress_sub_list[-1] = row["y_allraw"]["dep_weekly_subscale"]
            depress_list = [np.nan] * df.shape[0]
            depress_list[-1] = row['y_raw']
            df['phq4'] = phq_list
            df['depression'] = depress_list
            df['anxiety_sub'] = anxiety_list
            df['depress_sub'] = depress_sub_list

            file_name = os.path.join(tmp_path, pid + "_" + date[:10] + ".csv")
            
            df.to_csv(file_name, index=False)
            pids.add(pid)
    
    tmp_file_list = sorted(os.listdir(tmp_path))
    for pid in pids:
        dfs = list()
        for i in range(len(tmp_file_list)):
            if pid in tmp_file_list[i]:
                tmp_df = pd.read_csv(os.path.join(tmp_path, tmp_file_list[i]))
                dfs.append(tmp_df)
        if len(dfs) < 2:
            continue
        df = pd.concat(dfs)
        df.to_csv(os.path.join(save_path, pid + ".csv"), index=False)
    
    delete_folder(tmp_path)
    