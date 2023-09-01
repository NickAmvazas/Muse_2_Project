"""
The script takes two sample dataframes (df1 with 5 columns and df2 with 3 columns), 
and then checks if they have the same number of rows (if signals have the same time). 
If they do, it concatenates the two dataframes along the columns axis using the pd.concat() function 
and sets the result to a new dataframe called new_df. 

This script used only to combine the EEG and Gyroscope .csv files to one .csv file.
So for each session takes EEG2_crop.csv and GYRO2_crop.csv and creates EEG2_GYRO2.csv.
"""
import os
import pandas as pd


# Get the path of the directory containing the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the other file relative to the current script
read_folder_path = os.path.join(current_dir, "../DATA/Raw_EEG_Data/Muse2/SESSIONS") # Set paths

for user in os.listdir(read_folder_path):
    for action in os.listdir(read_folder_path+"/"+user):
        for session in os.listdir(read_folder_path+"/"+user+"/"+action):
            files = os.listdir(read_folder_path+"/"+user+"/"+action+"/"+session)
            if (len(files) == 5):
                file_path_1 = read_folder_path+"/"+user+"/"+action+"/"+session+"/"+files[1]
                file_path_2 = read_folder_path+"/"+user+"/"+action+"/"+session+"/"+files[3]
                dataframe_1 = pd.read_csv(file_path_1, header = 0, usecols = ['timeST','TP9','AF7','AF8','TP10'])
                dataframe_2 = pd.read_csv(file_path_2, header = 0, usecols = ['X','Y','Z']) 
                if len(dataframe_1) == len(dataframe_2):
                # Concatenate the two dataframes along the columns axis
                    new_df = pd.concat([dataframe_1, dataframe_2], axis=1)
                    save_path = read_folder_path+"/"+user+"/"+action+"/"+session+"/EEG2_GYRO2.csv"
                    #print(save_path)
                    new_df.to_csv(save_path, index=False)
                else:
                    print("Error: the two dataframes have different number of rows.")


