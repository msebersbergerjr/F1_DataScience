import statistics
import streamlit as st
from PIL import Image
import pandas as pd
import os
import numpy as np
import json
from pathlib import Path
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

def get_race(year,round):
    filepath = Path(f'data/races/{year}/{round}.csv')
    df = pd.read_csv(filepath)
    return df

# Takes a string lap time and converts it to a nanosecond equivalent
def time_to_nanoseconds(raw_time):
    try:
        dirty = datetime.strptime(raw_time, '%M:%S.%f').time()
        #clean = timedelta(minutes=dirty.minute, seconds=dirty.second, microseconds=dirty.microsecond)
        nanoseconds = (dirty.minute*6e10)+(dirty.second*1e9)+(dirty.microsecond*1e3)
        #nanoseconds = (dirty.microsecond*1000)
        return nanoseconds/1e9
    # Catch NaaN
    except:
        pass
    try:
        dirty = datetime.strptime(raw_time, '%I:%M:%S.%f').time()
        return None
    except:
        return raw_time

# find percent different between driver time and median time
def percent_difference(driver_time,median_time):
    diff = abs((driver_time - median_time)/((driver_time + median_time)/2))*100
    if driver_time > median_time:
        return -abs(diff)
    return diff

def get_current_drivers():
    '''Returns list of current years drivers'''
    filepath = Path('data/current_drivers.json')
    jsondata = dict()
    # Checks if data is already stored
    with open(filepath, 'r', encoding='utf-8') as infile: jsondata = json.load(infile)

    current_drivers = list()
    for driver in jsondata:
        current_drivers.append(driver['driverId'])
    return current_drivers

def get_current_circuits():
    '''Returns list of current circuits'''
    filepath = Path('data/scheduled/2022.json')
    jsondata = dict()
    # Checks if data is already stored
    with open(filepath, 'r', encoding='utf-8') as infile: jsondata = json.load(infile)
    current_circuits = list()
    for circuit in jsondata:
        current_circuits.append(circuit['Circuit']['circuitId'])
    return current_circuits

# -------------------- CONFIG --------------------
# Sets the configuration of the page. Currently using a wide layout to use entire screen realistate
st.set_page_config(page_title="F1 Datascience",page_icon=":zap:", layout="wide")

current_drivers = get_current_drivers()
current_circuits = get_current_circuits()

st.title("Exploratory Analysis")

st.title("Source")

st.write("Ergast Developer API [Source](http://ergast.com/mrd/)")

st.write("Formula1.com [Source](https://www.formula1.com/)")

st.title("Data Sets")
st.header("Scheduled Data")
st.write("Purpose of the scheduled data is to inform us of what circuits were driven in a season and also what round they are associated to")
st.write("Since we are predicting the 2022 circuits, we only care about those circuits history and we use the round as a key for lookup")
st.subheader("Important Variables")
st.write("season, round")

code = '''{
        "season": "2012",
        "round": "1",
        "url": "http://en.wikipedia.org/wiki/2012_Australian_Grand_Prix",
        "raceName": "Australian Grand Prix",
        "Circuit": {
            "circuitId": "albert_park",
            "url": "http://en.wikipedia.org/wiki/Melbourne_Grand_Prix_Circuit",
            "circuitName": "Albert Park Grand Prix Circuit",
            "Location": {
                "lat": "-37.8497",
                "long": "144.968",
                "locality": "Melbourne",
                "country": "Australia"
            }
        },
        "date": "2012-03-18",
        "time": "06:00:00Z"
    },'''
st.code(code, language=json)

st.header("Constructor Data")
st.write("This data is broken down into two separate data sets")
st.write("This 1st data set just shows the end results of a season for a constructor")
st.write("This is important to us because this gives us a loose idea of how well a team is in a season to be used as a weight later one.")
st.subheader("Important Variables")
st.write("constructorId, points")
code = '''{
        "position": "1",
        "positionText": "1",
        "points": "460",
        "wins": "7",
        "Constructor": {
            "constructorId": "red_bull",
            "url": "http://en.wikipedia.org/wiki/Red_Bull_Racing",
            "name": "Red Bull",
            "nationality": "Austrian"
        }
    },'''
st.code(code, language=json)

st.write("This 2nd data informs us of what constructor a driver was driving for in a season")
st.write("This is only important to us because the previous data set does not inform of drivers, so we use this to map a driver to a team")
st.subheader("Important Variables")

code = '''{
        "position": "1",
        "positionText": "1",
        "points": "281",
        "wins": "5",
        "Driver": {
            "driverId": "vettel",
            "permanentNumber": "5",
            "code": "VET",
            "url": "http://en.wikipedia.org/wiki/Sebastian_Vettel",
            "givenName": "Sebastian",
            "familyName": "Vettel",
            "dateOfBirth": "1987-07-03",
            "nationality": "German"
        },
        "Constructors": [
            {
                "constructorId": "red_bull",
                "url": "http://en.wikipedia.org/wiki/Red_Bull_Racing",
                "name": "Red Bull",
                "nationality": "Austrian"
            }
        ]
    },'''
st.code(code, language=json)

st.header("Race Data")
st.write("Purpose of this data set is")
st.subheader("Important Variables")

code = '''"season": "2012",
    "round": "1",
    "url": "http://en.wikipedia.org/wiki/2012_Australian_Grand_Prix",
    "raceName": "Australian Grand Prix",
    "Circuit": {
        "circuitId": "albert_park",
        "url": "http://en.wikipedia.org/wiki/Melbourne_Grand_Prix_Circuit",
        "circuitName": "Albert Park Grand Prix Circuit",
        "Location": {
            "lat": "-37.8497",
            "long": "144.968",
            "locality": "Melbourne",
            "country": "Australia"
        }
    },
    "date": "2012-03-18",
    "time": "06:00:00Z",
    "Laps": [
        {
            "number": "1",
            "Timings": [
                {
                    "driverId": "button",
                    "position": "1",
                    "time": "1:39.264"
                },
                {
                    "driverId": "hamilton",
                    "position": "2",
                    "time": "1:40.622"
                },
            ]
        },
        {
            "number": "2",
            "Timings": [
                {
                    "driverId": "button",
                    "position": "1",
                    "time": "1:33.414"
                },
                {
                    "driverId": "hamilton",
                    "position": "2",
                    "time": "1:34.297"
                },
            ]
        },'''
st.code(code, language=json)

st.title("Missing Data")

st.title("Outliers")

st.title("Derived Variables")
st.header("Performance Score")
st.subheader("Purpose")

st.write("Raw Data")
df =  get_race(2012, 1)
st.dataframe(df)

working_df = df.copy()
st.write("Converted Data")
for col in working_df.columns[1:]: working_df[col] = working_df[col].apply(lambda x : time_to_nanoseconds(x))
st.dataframe(working_df)

fig = go.Figure()
for col in working_df.columns[1:]:
    fig.add_trace(go.Box(y=working_df[col].values.tolist(), name=col, boxmean=True))
    fig.update_layout(title='All Lap times per lap')
fig.update_yaxes(type="log", showgrid=False)
fig.update_layout(height=1000)

st.plotly_chart(fig,use_container_width=True, height=1000)

median = working_df[1:].median(axis=0, skipna=True).tolist()
median_list = []
for _ in range(len(median)): median_list.append(statistics.median(median))
drivers = working_df['Drivers'].values.tolist()
fig = go.Figure()
for driver in drivers:
    temp = working_df.loc[working_df['Drivers'] == driver]
    lap_time = temp.iloc[0].values[1:].flatten().tolist()
    fig.add_trace(go.Box(y=lap_time, name=driver))
fig.add_trace(go.Box(x=drivers,y=median_list, name='Median',marker_color = 'red'))
fig.update_yaxes(type="log",showgrid=False)
fig.update_layout(height=1000)

st.plotly_chart(fig,use_container_width=True, height=1000)

st.subheader("Breakdown of Lap 5")

col1,col2,col3 = st.columns(3)

driver_row = working_df.loc[working_df['Drivers'] == 'hamilton']
driver_time = driver_row['Lap 5']
median = working_df['Lap 5'].median()
p_diff = percent_difference(driver_row['Lap 5'].values[0],working_df['Lap 5'].median())
with col1:
    st.subheader('Hamilton')
    st.metric(label='', value=driver_time)

with col2:
    st.subheader('Median Time')
    st.metric(label="", value=median)

with col3:
    st.subheader('Score')
    st.metric(label="", value=round(p_diff,5))

driver_row = working_df.loc[working_df['Drivers'] == 'pic']
driver_time = driver_row['Lap 5']
median = working_df['Lap 5'].median()
p_diff = percent_difference(driver_row['Lap 5'].values[0],working_df['Lap 5'].median())
with col1:
    st.subheader('Pic')
    st.metric(label='', value=driver_time)

with col2:
    st.subheader('Median Time')
    st.metric(label="", value=median)

with col3:
    st.subheader('Score')
    st.metric(label="", value=round(p_diff,5))

# -------------------- Performance Points All drivers across all circuits --------------------

pp_df = pd.read_csv(Path('data/pp.csv'))
st.dataframe(pp_df,use_container_width=True)

# -------------------- Zscore  --------------------

norm_df = pd.read_csv(Path('data/pp_norm.csv'))
st.dataframe(norm_df,use_container_width=True)

# -------------------- Driver Championship points --------------------
champ_df = pd.read_csv(Path('data/driver_champ.csv'))
st.dataframe(champ_df,use_container_width=True)