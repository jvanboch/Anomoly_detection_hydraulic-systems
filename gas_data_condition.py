import pandas as pd
from io import StringIO 
import plotly.express as px
import plotly.graph_objects as go
import os 
import sqlite3
con = sqlite3.connect("hydraulic_sensor_data.db")
cur = con.cursor()

sensor_folder_directory =r'C:\Users\jvanb\.vscode\Nebula\anomoly detection\Anomoly_detection_hydraulic-systems\data'
# for sensors_file in os.listdir(sensor_folder_directory):
sensor_types = ['CE', 'CP', 'EPS1', 'FS1', 'PS1', 'PS2', 'PS3', 'PS4', 'PS5', 'PS6','SE', 'TS1', 'TS2', 'TS3', 'TS4', 'VS1']
def sensor_text_data_to_df(path_to_sensor_data):
    with open(path_to_sensor_data,'r+') as f:
        sensor_data_str = f.read()
        f.close()
    sensor_data = pd.read_csv(StringIO(sensor_data_str),
                    sep="\t",skiprows=0, header = None)
    return sensor_data
def lengthen_sensor_df(sensor_df, combined_sensor_df,sensor_name):
    long_sensor_df = sensor_df[sensor_name].melt()
    long_sensor_df = long_sensor_df.rename(columns={'variable':'batch_num', 'value':sensor_name})
    if len(combined_sensor_df)==0:
        return long_sensor_df
    combined_sensor_df_new = pd.concat([combined_sensor_df, long_sensor_df[sensor_name]], join="inner", axis=1)
    return combined_sensor_df_new
def evaluate_resample_plot(sensor, sensors_datas,batch_num):
    fig=go.Figure()
    sensors_datas_resampled = sensors_datas[sensor].T[batch_num].copy()
    sensors_datas_resampled.index = pd.to_datetime(sensors_datas_resampled.index, unit='s', errors='coerce')
    fig.add_trace(go.Scatter(x=sensors_datas_resampled.index, y=sensors_datas_resampled,name='100HZ original'))
    for freq in [10,100]:
        sensors_datas_resampled_freq = sensors_datas_resampled.resample('{}s'.format(freq)).mean()
        fig.add_trace(go.Scatter(x=sensors_datas_resampled_freq.index, y=sensors_datas_resampled_freq, name='resample frequency to: {}s'.format(100/freq)))
    fig.update_xaxes(visible=False)
    return fig
sensors_datas={}
new_df = ''
for sensor_type in sensor_types:
    sensor_df = sensor_text_data_to_df(sensor_folder_directory +'\\'+sensor_type+'.txt')
    sensors_datas[sensor_type] = sensor_df
    new_df = lengthen_sensor_df(sensors_datas,new_df, sensor_type)

new_df.to_sql(name='sensor_batch_data',con=con,if_exists='replace')


PS1_resample_eval_fig = evaluate_resample_plot('PS1', sensors_datas,1491)
PS2_resample_eval_fig = evaluate_resample_plot('PS2', sensors_datas,1491)
PS3_resample_eval_fig = evaluate_resample_plot('PS3', sensors_datas,1491)
PS4_resample_eval_fig = evaluate_resample_plot('PS4', sensors_datas,1491)
PS5_resample_eval_fig = evaluate_resample_plot('PS4', sensors_datas,1491)
PS6_resample_eval_fig = evaluate_resample_plot('PS4', sensors_datas,1491)
EPS1_resample_eval_fig = evaluate_resample_plot('EPS1', sensors_datas,1491)

#TO DO save output plots as HTML files for future review purposes. 

#evaluate the shape of each data 
# CE (2205, 60)
# CP (2205, 60)
# EPS1 (2205, 6000)
# FS1 (2205, 600)
# PS1 (2205, 6000)
# PS2 (2205, 6000)
# PS3 (2205, 6000)
# PS4 (2205, 6000)
# PS5 (2205, 6000)
# PS6 (2205, 6000)
# SE (2205, 60)
# TS1 (2205, 60)
# TS2 (2205, 60)
# TS3 (2205, 60)
# TS4 (2205, 60)
# VS1 (2205, 60)
#each sensor has 2205 batches worth of data, Pressure has a higher sampling frequency of 100HZ,Volume_flow has a frequency of 10HZ, and ther rest is 1 HZ frequency
#need to evalute potential of downsampling. 

