import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
# from plotting_functions import plot_sensor_data_batch_shaded 
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

    fig.add_trace(go.Scatter(x=[x0,x0,x1,x1], y=[y0,y1,y1,y0], fill="tonext", name='batch {}'.format(batch_num), mode='markers', marker={'size':1}))
    return fig
for i in range(0,60):
    sensor_fig = plot_sensor_data_batch_shaded(sensor_df, 'CE', i,sensor_fig)


sensor_fig.update_layout(
    updatemenus=[
        dict(
            buttons=list([

                dict(
                    args=[{'visible':True}],
                    label="Batch On",
                    method="restyle"
                ),
                dict(
                   
                    args = [{'visible': 'legendonly'}, {'visible':[0]}],
                    label="Batch Off",
                    method="restyle"
                ),
                dict(
                    args=[{'visible':[0]}],
                    label="CE On",
                    method="restyle"
                ),
            ]),
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.1,
            yanchor="top"
        ),
    ]
)