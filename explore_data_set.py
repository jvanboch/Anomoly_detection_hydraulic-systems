import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash
from dash import  dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import numpy as np
from plotly.subplots import make_subplots
dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")
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
    fig.add_trace(go.Scatter(x=[x1,x1], y=[y1,y1], name='batch {}'.format(batch_num), mode='lines',line=dict(color="red")))
    fig.add_trace(go.Scatter(x=[x0,x0], y=[y0,y1], name='batch {}'.format(batch_num), mode='lines',line=dict(color="red")))

    return fig
for i in range(0,60):
    sensor_fig = plot_sensor_data_batch_shaded(sensor_df, 'CE', i,sensor_fig)
sensor_fig.update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    )
batch_fig = go.Figure()
batch_fig.update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    )
def NormalizeData(sensor_series):
    return (sensor_series - np.mean(sensor_series)) / (np.max(sensor_series) - np.min(sensor_series))

sensensor_fig_html = sensor_fig.to_html()
with open('html_sensor_data.html','w+') as f:
    f.write(sensensor_fig_html)
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.CYBORG, dbc_css])




# html.Div(id = 'parent', 
#          children = [
#     html.H1(id = 'H1', children = 'Sensor Data by Batch', style = {'textAlign':'center',\
#                                             'marginTop':40,'marginBottom':40}),
#     html.Div(dcc.Dropdown( ['CE', 'CP', 'EPS1', 'FS1', 'PS1', 'PS2', 'PS3', 'PS4', 'PS5', 'PS6','SE', 'TS1', 'TS2', 'TS3', 'TS4', 'VS1'], ['CE'], id='sensor_drop_down', multi=True),style={"width": "25%", "color":"dark", "margin": "0 auto","justify-content": 'center',"align":"center",'background':'black'}),
#     html.Div(dcc.Dropdown(['Normalized', 'Actual', 'Multi-y axis'], 'Actual', id='chart_option_dropdown'), style={"width": "25%", "color":"dark", "background":"black", "justify-content":"center", 'align': 'center',"margin": "0 auto"}),
#     html.Div(dcc.Dropdown(list(set(sensor_df.batch_num)),1, id='batch_drop_down'),style={"width": "25%", "color":"dark", "background":"black", "justify-content":"center", 'align': 'center',"margin": "0 auto"}),
#     html.Div(id='dd-output-container'),
        
#         dcc.Graph(id = 'line_plot', figure = sensor_fig),    
#         dcc.Graph(id='batch_plot', figure=batch_fig)
#     ]
#                      )
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem"
    # "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem"
}
sidebar = html.Div(
    [
        html.H2("Sliders", className="display-4"),
        html.Hr(),
        html.P(
            "Select your options", className="lead"
        ),
        dbc.Nav(
            [
                html.Div(dcc.Dropdown( ['CE', 'CP', 'EPS1', 'FS1', 'PS1', 'PS2', 'PS3', 'PS4', 'PS5', 'PS6','SE', 'TS1', 'TS2', 'TS3', 'TS4', 'VS1'], ['CE'], id='sensor_drop_down', multi=True)),
                html.Div(dcc.Dropdown(['Normalized', 'Actual', 'Multi-y axis'], 'Actual', id='chart_option_dropdown')),
                html.Div(dcc.Dropdown(list(set(sensor_df.batch_num)),1, id='batch_drop_down')),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

# sidebar=[    html.Div(dcc.Dropdown( ['CE', 'CP', 'EPS1', 'FS1', 'PS1', 'PS2', 'PS3', 'PS4', 'PS5', 'PS6','SE', 'TS1', 'TS2', 'TS3', 'TS4', 'VS1'], ['CE'], id='sensor_drop_down', multi=True),style={"width": "25%", "color":"dark", "margin": "0 auto","justify-content": 'center',"align":"center",'background':'black'}),
#     html.Div(dcc.Dropdown(['Normalized', 'Actual', 'Multi-y axis'], 'Actual', id='chart_option_dropdown'), style={"width": "25%", "color":"dark", "background":"black", "justify-content":"center", 'align': 'center',"margin": "0 auto"}),
#     html.Div(dcc.Dropdown(list(set(sensor_df.batch_num)),1, id='batch_drop_down'),style={"width": "25%", "color":"dark", "background":"black", "justify-content":"center", 'align': 'center',"margin": "0 auto"})]

app.layout = dbc.Container(
     [dbc.Col(sidebar),
      dbc.Col(dcc.Graph(id = 'line_plot', figure = sensor_fig), className="lead", style=CONTENT_STYLE),
      dbc.Col(dcc.Graph(id = 'batch_plot', figure = sensor_fig), className="lead",style=CONTENT_STYLE),
      ],
    fluid=True,
    className="dbc")
@app.callback(
    Output('line_plot', 'figure'),
    Input('sensor_drop_down', 'value'),
    Input('chart_option_dropdown', 'value')


)



def update_output(sensor_drop_down, chart_option_dropdown):
    sensor_fig = go.Figure()
    sub_plots_data=[]
    for i,sensor in enumerate(sensor_drop_down):
        print(i,sensor)
        if chart_option_dropdown=='Normalized':
            sensor_series = NormalizeData(sensor_df[sensor])
            print(sensor_series[0:5])
        else: 
            sensor_series = sensor_df[sensor]
        # if chart_option_dropdown=='Multi-y axis':
        #     sensor_fig.add_trace(go.Scatter(y=sensor_series,name=sensor,yaxis='y{}'.format(i+1)))

        # else:
        sensor_range = sensor_df['batch_num'] + sensor_df.index
        sensor_fig.add_trace(go.Scatter(y=sensor_series ,name=sensor))

    # for i in range(0,60):
    #     sensor_fig = plot_sensor_data_batch_shaded(sensor_df, sensor, i,sensor_fig)
        sensor_fig.update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    )
   
    return sensor_fig

@app.callback(
    Output('batch_plot', 'figure'),
    Input('batch_drop_down','value'),
    Input('sensor_drop_down','value'),
    Input('chart_option_dropdown', 'value')
)
def update_batch_plot(batch_drop_down,sensor_drop_down,chart_option_dropdown):
    sensor_df_batch_filtered = sensor_df[sensor_df['batch_num']==batch_drop_down]
    batch_fig = go.Figure()
    for i,sensor in enumerate(sensor_drop_down):
        if chart_option_dropdown=='Normalized':
            sensor_series = NormalizeData(sensor_df_batch_filtered[sensor])
        else: 
            sensor_series = sensor_df_batch_filtered[sensor]
        # if chart_option_dropdown=='Multi-y axis':
        #     sensor_fig.add_trace(go.Scatter(y=sensor_series,name=sensor,yaxis='y{}'.format(i+1)))

        # else:

        batch_fig = batch_fig.add_trace(go.Scatter(y=sensor_series, name=sensor))
    
    # for i in range(0,60):
    #     sensor_fig = plot_sensor_data_batch_shaded(sensor_df, sensor, i,sensor_fig)
        batch_fig.update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    )
    return batch_fig

if __name__ == '__main__':
     app.run_server(debug=True, use_reloader=False)

