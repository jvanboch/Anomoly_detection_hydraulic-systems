import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash
from dash import  dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import numpy as np
con = sqlite3.connect("hydraulic_sensor_data.db")
sensor_df = pd.read_sql_query("SELECT * FROM sensor_batch_data", con)
sensor_fig=None
def plot_sensor_data_batch_shaded(sensor_df, sensor_name, batch_num,fig):
    if fig==None:
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=sensor_df[sensor_name],name='CE'))
    x0=sensor_df[sensor_df['batch_num']==batch_num].index.min()
    x1=sensor_df[sensor_df['batch_num']==batch_num].index.max()
    y0=sensor_df[sensor_name].min()
    y1=sensor_df[sensor_name].max()

    # fig.add_trace(go.Scatter(x=[x0,x0,x1,x1], y=[y0,y1,y1,y0], fill="toself", name='batch {}'.format(batch_num), mode='markers', marker={'size':1}))
    fig.add_trace(go.Scatter(x=[x1,x1], y=[y1,y1], name='batch {}'.format(batch_num), mode='lines',line=dict(color="black")))
    fig.add_trace(go.Scatter(x=[x0,x0], y=[y0,y1], name='batch {}'.format(batch_num), mode='lines',line=dict(color="black")))
    return fig
for i in range(0,60):
    sensor_fig = plot_sensor_data_batch_shaded(sensor_df, 'CE', i,sensor_fig)

def NormalizeData(sensor_series):
    return (sensor_series - np.mean(sensor_series)) / (np.max(sensor_series) - np.min(sensor_series))

sensensor_fig_html = sensor_fig.to_html()
with open('html_sensor_data.html','w+') as f:
    f.write(sensensor_fig_html)
app = dash.Dash()

app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = 'Sensor Data by Batch', style = {'textAlign':'center',\
                                            'marginTop':40,'marginBottom':40}),
    dcc.Dropdown( ['CE', 'CP', 'EPS1', 'FS1', 'PS1', 'PS2', 'PS3', 'PS4', 'PS5', 'PS6','SE', 'TS1', 'TS2', 'TS3', 'TS4', 'VS1'], ['CE'], id='sensor_drop_down', multi=True),
    dcc.Dropdown(['Normalized', 'Actual'], 'Actual', id='normalize_button'),
    html.Div(id='dd-output-container'),
        
        dcc.Graph(id = 'line_plot', figure = sensor_fig)    
    ]
                     )
@app.callback(
    Output('line_plot', 'figure'),
    Input('sensor_drop_down', 'value'),
    Input('normalize_button', 'value')
    # State("sensor_drop_down", "value")
)
def update_output(sensor_drop_down, normalize_button):
    print(sensor_drop_down, normalize_button)
    value = sensor_drop_down
    value_norm = normalize_button
    # print(value, search)_)
    # if not search_value:
    #     raise PreventUpdate
    sensor_fig = go.Figure()
    # if sensors==None:
    #     sensors=['CE']
    for sensor in value:
        if value_norm=='Normalized':
            sensor_series = NormalizeData(sensor_df[sensor])
        else: 
            sensor_series = sensor_df[sensor]
        sensor_fig.add_trace(go.Scatter(y=sensor_series,name=sensor))

    # for i in range(0,60):
    #     sensor_fig = plot_sensor_data_batch_shaded(sensor_df, sensor, i,sensor_fig)

    print(value)
   
    return sensor_fig

if __name__ == '__main__':
     app.run_server(debug=True, use_reloader=False)

