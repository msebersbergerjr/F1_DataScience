import streamlit as st
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import plotly.express as px

# -------------------- CONFIG --------------------
# Sets the configuration of the page. Currently using a wide layout to use entire screen realistate
st.set_page_config(page_title="F1 Datascience",page_icon=":zap:", layout="wide")

# -------------------- FUNCTIONS --------------------
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
    '''Returns list of current circuits as of year 2022'''

    filepath = Path('data/scheduled/2022.json')
    jsondata = dict()
    # Checks if data is already stored
    with open(filepath, 'r', encoding='utf-8') as infile: jsondata = json.load(infile)
    current_circuits = list()
    for circuit in jsondata:
        current_circuits.append([circuit['Circuit']['circuitId'],circuit['raceName']])
    return current_circuits

def find_circuit(name,circuit_list):
    '''Gets the circuitID from a circuit name'''
    for circuit in circuit_list:
        if circuit[1] == name:
            return circuit[0]

def get_round(year,circuitId):
    '''Returns the round within a given year the circuitId was found under'''

    filepath = Path(f'data/scheduled/{year}.json')
    jsondata = dict()
    with open(filepath, 'r', encoding='utf-8') as infile: jsondata = json.load(infile)
    for circuit in jsondata:
        if circuit['Circuit']['circuitId'] == circuitId:
            return circuit['round']
    return None

def time_to_nanoseconds(raw_time):
    '''Takes a string lap time and converts it to a nanosecond equivalent'''

    try:
        dirty = datetime.strptime(raw_time, '%M:%S.%f').time()
        #clean = timedelta(minutes=dirty.minute, seconds=dirty.second, microseconds=dirty.microsecond)
        nanoseconds = (dirty.minute*6e10)+(dirty.second*1e9)+(dirty.microsecond*1e3)
        #nanoseconds = (dirty.microsecond*1000)
        return nanoseconds/1e9
    # Catch NaaN
    except:
        return raw_time

def percent_difference(driver_time,average_time):
    '''find percent different between driver time and average time'''

    diff = abs((driver_time - average_time)/((driver_time + average_time)/2))*100
    if driver_time > average_time:
        return -abs(diff)
    return diff

def get_score(year,round,current_drivers):
    '''
    Get the Consistancy score of the current drivers on a given year and track
    Each drivers lap is compared to the average laptime, then a score is given based upon
    the difference on a driver lap and the average. Combining this score acorss all laps
    to give us a total

    As of drivers who DNF - we count the total as nan
    @returns:
    -   Ordered list of drivers and their respective score
    '''
    filepath = Path(f'data/races/{year}/{round}.json')
    with open(filepath, 'r', encoding='utf-8') as infile: jsondata = json.load(infile)

    # Gets list of all drivers at the start of the race, sorts them alphabetically
    drivers = []
    for driver in jsondata['Laps'][0]['Timings']:
        drivers.append(driver['driverId'])

    drivers.sort()

    # Create original dataframe which just holds a column of the drivers
    original_df = pd.DataFrame()
    original_df['Drivers'] = drivers

    # Goes through a race.json and adds the times for all laps per driver
    for lap in jsondata['Laps']:
        lap_data = []
        
        for _ in range(0, len(drivers)):
            try:
                driver = next(item for item in lap['Timings'] if item['driverId']==drivers[_])
                # Create a tuple of driver and lap time
                lap_data.append([driver['driverId'],driver['time']])
            except:
                lap_data.append([drivers[_],None])

        # Sort it so it matches the rows
        lap_data.sort(key = lambda x: x[0])
        # Add new column of lap time
        time_list = list(list(zip(*lap_data))[1])
        original_df[f"Lap {lap['number']}"] = time_list

    working_df = original_df.copy()
    # Convert each string laptime to nanosecond equivolent
    for col in working_df.columns[1:]: working_df[col] = working_df[col].apply(lambda x : time_to_nanoseconds(x))

    score_list = []
    for driver in current_drivers:
        score_avg = 0
        driver_row = working_df.loc[working_df['Drivers'] == driver]
        if not driver_row.empty:
            for lap in driver_row.columns[1:]:
                score_avg += percent_difference(driver_row[lap].values[0],working_df[lap].mean())
        else:
            score_avg = float('nan')
        score_list.append(score_avg)
    return score_list
        
current_drivers = get_current_drivers()
current_drivers.sort()
current_circuits = get_current_circuits()
circuit_names = []
for circuit in current_circuits:
    circuit_names.append(circuit[1])

# -------------------- MAINPAGE --------------------
st.title("F1 Datascience")

# Get the circuit user wants to see
track = st.selectbox('Select a Circuit', circuit_names)
track_id = find_circuit(track, current_circuits)

#init dataframe with just current drivers

df = pd.DataFrame()
df['Drivers'] = current_drivers

# Get All the seasons data for selected circuit
for year in range(2012,2022):
    round = get_round(year,track_id)
    if round != None:
        for driver in current_drivers:
            score_list = get_score(year,round,current_drivers)
    else: continue
    df[f'Season {year}'] = score_list

# Get the total score for a driver across all seasons
df_list = []
for driver in df['Drivers']:
    driver_row = df.loc[df['Drivers'] == driver]
    score = driver_row.drop('Drivers',axis=1).sum(axis=1, skipna=True).values[0]
    df_list.append(score)
df['Total'] = df_list

# Bar Graph to show driver consisancy score
df.sort_values('Total', ascending=False ,inplace=True)
fig = px.bar(df, x=df['Drivers'], y=df['Total'], title=f'{track} Consistancy Score', color=df['Drivers'])

# Display Chart
st.plotly_chart(fig)
del df
