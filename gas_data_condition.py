import pandas as pd
from io import StringIO 
import plotly.express as px
import plotly.graph_objects as go
import os 
import sqlite3
con = sqlite3.connect("hydraulic_sensor_data.db")
cur = con.cursor()

sensor_folder_directory =r'C:\Users\jvanb\.vscode\Nebula\anomoly detection\gas data\data'
# for sensors_file in os.listdir(sensor_folder_directory):
sensor_types = ['CE', 'CP', 'EPS1', 'FS1', 'PS1', 'PS2', 'PS3', 'PS4', 'PS5', 'PS6','SE', 'TS1', 'TS2', 'TS3', 'TS4', 'VS1']
def sensor_text_data_to_df(path_to_sensor_data):
    with open(path_to_sensor_data,'r+') as f:
        sensor_data_str = f.read()
    sensor_data = pd.read_csv(StringIO(sensor_data_str),
                    sep="\t",skiprows=0, header = None)

    # sensor_data.loc[-1] = sensor_data.columns.to_list() 
    # sensor_data = sensor_data.sort_index().reset_index(drop=True)
    # sensor_data.columns=list(range(0,sensor_data.shape[1])) #correct header to batch number
    #need to transpose since the sensor file structure is each row is a batch, and column is a point in the data set. final output should be each batch is a column, with the row being a data point. 
    # sensor_data = sensor_data.T
    return sensor_data
for sensor_type in sensor_types:
    sensor_df = sensor_text_data_to_df(sensor_folder_directory +'\\'+sensor_type+'.txt')
    sensor_df.to_sql(name=sensor_type+'_sensor_values',con=con,if_exists='replace')
fig = go.Figure()
for i in range(50,75,5):
    fig.add_trace(go.Scatter( y=dft[i],name=i))