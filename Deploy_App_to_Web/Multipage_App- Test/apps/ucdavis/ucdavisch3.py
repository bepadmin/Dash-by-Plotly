import dash
from flask import Flask
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta
import pilib
import pandas as pd
import pytz
import plotly.express as px
import pandas as pd
import pathlib
from pytz import timezone
from app import app

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../webids").resolve()
print(DATA_PATH)


# webids_filename = "webid.csv"
webids = pd.read_csv(DATA_PATH.joinpath("webid.csv"),header = 0)



# from pilibrary import pi_client

# project = os.path.basename(__file__)
# LiftID = ""












# ### WEB API FILE ###
# webids_filename = "webid.csv"
# webids = pd.read_csv(webids_filename,header = 0)

#Webids
LiftID = webids['Lift'].iloc[0]
percentLoadID = webids['%Load'].iloc[0]
kWperTonID = webids['kW/Ton'].iloc[0]
ChillerStatusID = webids['ChillerStatus'].iloc[0]

#Establishes Timezones since database server accepts EST timestamp, client tz will be portrayed to the client.
clienttz = webids['Timezone'].iloc[0]  
dbservertz = 'US/Eastern'

Title = webids['Equipment'].iloc[0]



def chiller_status():
    currenttime = datetime.now(timezone(dbservertz))
    clienttime = datetime.now(timezone(clienttz))
    r = (pilib.getResponse(
        'https://40.117.156.48/piwebapi/streams/' + ChillerStatusID + '/recordedattime?time=' + currenttime.strftime('%Y-%m-%d %H:%M:%S')))
    if r.json()['Value'] == "On":
        return True
    elif r.json()['Value'] == "Off":
        return False

### CHECK IF VALUES ARE GREATER THAN 0 ###
def check_responses(lift,load,kW):
    if lift > 0 and load > 0 and kW > 0:
        return True
    else:
        return False
    
### CHECK IF VALUES ARE GREATER THAN 0 ###
def generate_sample():
    currenttime = datetime.now(timezone(dbservertz))
    clienttime = datetime.now(timezone(clienttz))
    date_format = "%Y-%m-%d %H:%M:%S"
    r = (pilib.getResponse(
        'https://40.117.156.48/piwebapi/streams/' + LiftID + '/recordedattime?time=' + currenttime.strftime('%Y-%m-%d %H:%M:%S')))   
    lift = 3#r.json()['Value']
##    time = (datetime.strptime(str(r.json()['Timestamp']), "%Y-%m-%dT%H:%M:%SZ")+ timedelta(hours=timeshift)).strftime("%Y-%m-%d %H:%M:%S")
    time = clienttime.strftime('%Y-%m-%d %H:%M:%S')
    r2 = (pilib.getResponse(
        'https://40.117.156.48/piwebapi/streams/' + percentLoadID + '/recordedattime?time=' + currenttime.strftime('%Y-%m-%d %H:%M:%S')))  
    load = 3#r2.json()['Value']
    r3 = (pilib.getResponse(
        'https://40.117.156.48/piwebapi/streams/' + kWperTonID + '/recordedattime?time=' + currenttime.strftime('%Y-%m-%d %H:%M:%S')))  
    kW = .5#r3.json()['Value']
    return lift, load, kW, time
### Load past data

import os

if os.path.exists('output.csv'):
    past_data = pd.read_csv(DATA_PATH.joinpath('output.csv'))
else:
    past_data = pd.read_csv(DATA_PATH.joinpath('past_data.csv')) # whatever the name of the csv file holding the initial historical data


##past_data = pd.read_csv('past_data.csv')
past_data = past_data.dropna()
past_data = past_data[past_data['kW/Ton']>0].reset_index(drop=True)

X = deque(list(past_data['Load(%)'].values), maxlen=8000)
Y = deque(list(past_data['Lift'].values), maxlen=8000)
Z = deque(list(past_data['kW/Ton'].values), maxlen=8000)
timestamps = deque(list(past_data['time'].values), maxlen=8000)
hovertextdisplay = []

for x_ini, y_ini, z_ini, time_ini in zip(X,Y,Z,timestamps):
    hovertextdisplay.append(f"{time_ini} <br> % Load: {x_ini} <br> Lift (°F): {y_ini}, kW/ton: {z_ini}")

hovertextdisplay = deque(hovertextdisplay, maxlen=8000)

# app = Flask(__name__)

# dash_app = dash.Dash(__name__, server=app)

layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=False),
        dcc.Interval(
            id='graph-update',
            interval=3*1000, #sec * 1000
            n_intervals = 0
        ),
    ]
)

@app.callback(Output('live-graph', 'figure'),
        [Input('graph-update', 'n_intervals')])
def update_graph_scatter(n):
    
    if os.path.exists('output.csv'):
        past_data = pd.read_csv(DATA_PATH.joinpath('output.csv'))
    else:
        past_data = pd.read_csv(DATA_PATH.joinpath('past_data.csv')) # whatever the name of the csv file holding the initial historical data


    ##past_data = pd.read_csv('past_data.csv')
    past_data = past_data.dropna()
    past_data = past_data[past_data['kW/Ton']>0].reset_index(drop=True)

    X = deque(list(past_data['Load(%)'].values), maxlen=8000)
    Y = deque(list(past_data['Lift'].values), maxlen=8000)
    Z = deque(list(past_data['kW/Ton'].values), maxlen=8000)
    timestamps = deque(list(past_data['time'].values), maxlen=8000)
    hovertextdisplay = []

    for x_ini, y_ini, z_ini, time_ini in zip(X,Y,Z,timestamps):
        hovertextdisplay.append(f"{time_ini} <br> % Load: {x_ini} <br> Lift (°F): {y_ini}, kW/ton: {z_ini}")
    hovertextdisplay = deque(hovertextdisplay, maxlen=8000)
    ## check stat
    lift, load, kW, time = generate_sample()
    status = check_responses(lift,load,kW)
    if status == True:
        X.append(load)
        Y.append(lift)
        Z.append(kW)
        timestamps.append(time)
        x_ann = X[-1]
        y_ann = Y[-1]
        z_ann = Z[-1]
        time=timestamps[-1]
        hovertextdisplay.append(f"{time} <br> % Load: {x_ann:.2f} <br> Lift (°F): {y_ann:.2f} <br> kW/ton: {z_ann:.2f}")
        row = pd.DataFrame({'Load(%)':X[-1], 'Lift':Y[-1], 'kW/Ton':Z[-1], 'time':timestamps[-1]}, index=[0])
        past_data = past_data.append(row,ignore_index = True)
        past_data.to_csv(DATA_PATH.joinpath('output.csv'),index = False)
        annotations = [dict(x=x_ann, y=y_ann, text=f"Latest: {time} <br> % Load: {x_ann:.2f} <br> Lift (°F): {y_ann:.2f} <br> kW/ton: {z_ann:.2f}", showarrow=True, arrowhead=2, arrowcolor='white', ax=0, ay=40)]
    else:
        x_ann = 0
        y_ann = 0
        z_ann = 0
        time = time
        annotations=[dict(x=x_ann, y=y_ann, text=f"Latest: {time} <br>  kW/ton: {z_ann:.2f}", showarrow=True, arrowhead=2, arrowcolor='white', ax=10, ay=-40)]

##    x_ann = X[-1]
##    y_ann = Y[-1]
##    z_ann = Z[-1]
##    time=timestamps[-1]
    data = go.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'markers',
            hovertext=list(hovertextdisplay),
            hoverinfo='text',
            marker=dict(color = list(Z), cmax=1, cmin=0.3, showscale=True, reversescale=True,
            colorscale=[
##            # Let first 10% (0.1) of the values have color rgb(0, 0, 0)
            [0, "rgb(255, 0, 0)"],
            [0.2, "rgb(255, 60, 0)"],

            [0.2, "rgb(255, 60, 0)"],
            [0.3, "rgb(255, 100, 0)"],

            [0.3, "rgb(255, 100, 0)"],
            [0.4, "rgb(220, 140, 0)"],

            [0.4, "rgb(220, 140, 0)"],
            [0.5, "rgb(220, 140, 0)"],

            [0.5, "rgb(200, 160, 0)"],
            [0.6, "rgb(100, 180, 0)"],

            [0.6, "rgb(100, 180, 0)"],
            [0.7, "rgb(100, 200, 0)"],

            [0.7, "rgb(50, 200, 0)"],
            [0.8, "rgb(50, 190, 0)"],

            [0.8, "rgb(50, 190, 0)"],
            [1.0, "rgb(0, 190, 0)"]], size=8, colorbar=dict(title='kW/Ton', thickness=20) )
            )

    return {'data': [data], 'layout': go.Layout(title=dict(text= Title, x=.01, y=.98, xanchor='left'),
                                                xaxis=dict(title='% Load', range=[0,120]),
                                                yaxis=dict(title='Lift (°F)', range=[0,80], scaleratio=1),
                                                annotations=annotations,
                                                paper_bgcolor='black',
                                                plot_bgcolor='black',
                                                width=650,
                                                height=300,
                                                margin=dict(l=35,r=35,b=35,t=35),
                                                font=dict(color='white', size=12)
                                                )}




##
# if __name__ == "__main__":
#     app.run(debug=False)
##if __name__ == '__main__':
##    app.run(host="0.0.0.0", ssl_context=('/etc/letsencrypt/live/bepchilleranalytics.eastus.cloudapp.azure.com/fullchain.pem','/etc/letsencrypt/live/bepchilleranalytics.eastus.cloudapp.azure.com/privkey.pem'))
##if(__name__=='__main__'):
##    app.run_server()

