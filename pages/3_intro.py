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

# -------------------- FUNCTIONS --------------------
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

# -------------------- CONFIG --------------------
# Sets the configuration of the page. Currently using a wide layout to use entire screen realistate
st.set_page_config(page_title="F1 Datascience",page_icon=":zap:", layout="wide")


col1, col2 = st.columns([1,3])
with col1:
    st.image("https://1000logos.net/wp-content/uploads/2021/06/F1-logo.png",width=300)

with col2:
    st.markdown("")
    original_title = '<p style="font-family:Courier New, monospace;font-weight:700; color:white; font-size: 90px;">Rubber Casino</p>'
    st.markdown(original_title, unsafe_allow_html=True)


tab1, tab2, tab3, tab4, tab5 = st.tabs(['Introduction','Formula One','Exploratory Analysis','Performance Score','Outcome'])

with tab1:

    st.subheader("Our name")
    st.text("We joked that we would build this prediction to bet on the outcome of the Grand Prix.")
    st.text("Rubber for the wheels, Casino for the gambling.")

    st.markdown("---")
    st.markdown("")

    st.subheader("Goal")
    st.text("Build a system to predict the 2022 Grand Prix winners by using performance history of F1 Drivers.")
    st.markdown("---")



with tab2:
    st.header("Championships")
    st.text("There are two types of championships in Formula One.")
    st.text("The way that championships are scored is a point system.")
    points_data = [{'Position':'Points','1st':25,'2nd':18,'3rd':15,'4th':12,'5th':10,'6th':8,'7th':6,'8th':4,'9th':2,'10th':1,'FL':1}]
    st.write(pd.DataFrame(points_data).set_index('Position'))
    st.text("A driver must finish within the top ten to receive a point for setting the fastest lap of the race.")

    st.text("")
    st.text("")
    st.text("")



    st.subheader("Constructor Championship")
    st.text("A Constructor is a team within Formula One.")
    construct_data = [{
        'Team':'Country',
        'Alfa Romeo':'Switzerland',
        'AlphaTauri':'Italy',
        'Alpine':'France',
        'Aston Martin':'United Kingdom',
        'Ferrari':'Italy',
        'Haas':'United States',
        'McLaren':'United Kingdom',
        'Mercedes':'Germany',
        'Red Bull':'Austria',
        'Williams':'United Kingdom'
    }]
    st.write(pd.DataFrame(construct_data).set_index("Team"))
    st.text("Constructors are comprised of two driver roles called Primary Driver and Support Driver.")
    st.text("Funding is provided to teams based on the points earned by their driver. 1 point is worth roughly 1 million dollars.")


    st.text("")
    st.text("")
    st.text("")

    st.subheader("Driver Championship")
    st.text("Points are earned by drivers that place in the Top 10.")


with tab3:
# -------------------- Data Sets --------------------
    st.title("Data Sets")
    st.header("Scheduled Data")
    st.write("Description")
    st.subheader("Important Variables: season; round; circuitId")
    code = '''
    {
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
    },
    '''
    st.code(code, language=json)

    st.header("Race Data")
    st.write("Description")
    st.subheader("Important Variables: round; driverId; time")

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

    st.subheader("Experience")
    st.write("Related to the number of years a driver has been driving for. Not all drivers have been driving since the year 2012 which results in large amounts of missing data")
    st.write("This leads to a skew in the number of accrued points")

    temp = pd.DataFrame()
    temp['Driver'] = ['Latifi','Hamilton']

    for year in range(2012,2022):
        if year < 2020:
            temp[year] = ['False','True']
        else:
            temp[year] = ['True','True']

    st.dataframe(temp,use_container_width=True)

    st.subheader("DNF")
    st.write("Related to drivers not finishing a circuit. Various reason: Themselves, Their car, Other drivers etc..")
    st.write("Since there is not information that tells us the reason behind a DNF, we treated each DNF equally")
    st.write("Additionally, a driver would not receive any points from a DNF since they did not place in the top 10")

    filepath = Path('data/races/2012/1.json')
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
    st.dataframe(original_df.head(),use_container_width=True)

    st.title("Outliers")
    st.write("We expect there to be a handle full of outliers from our data from the nature of the sport")
    st.write("Expected outliers in lap data results: Pit Stop, Safety Cars, Crashes, Weather, etc...")
    st.write("We left them in since it doesn't hinder out outcome, and also its apart of the sport.")

    

# -------------------- Performance Score --------------------
with tab4:
    st.header("Performance Score")
    st.subheader("Description- what is a performance score")

    st.subheader("Season: 2012 Round: 1")

    # ---------- RAW DATA ----------
    st.subheader("Raw Data - Time Series")
    df =  get_race(2012, 1)
    st.dataframe(df)
    
    # ---------- CONVERTED DATA ----------
    st.subheader("Converted Data - Time Series represented as seconds (float)")
    working_df = df.copy()
    for col in working_df.columns[1:]: working_df[col] = working_df[col].apply(lambda x : time_to_nanoseconds(x))
    st.dataframe(working_df)

    # ---------- Lap time Vertically ----------
    st.subheader("Lap times Vertically")
    fig = go.Figure()
    for col in working_df.columns[1:]:
        fig.add_trace(go.Box(y=working_df[col].values.tolist(), name=col, boxmean=True))
    fig.update_yaxes(type="log", showgrid=False)
    fig.update_layout(height=1000)

    st.plotly_chart(fig,use_container_width=True, height=1000)

    # ---------- Lap time Horizontally ----------
    st.subheader("Lap times Horizontally")
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

    # ---------- Breakdown ----------

    st.subheader("How we give a performance score")
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

    # ---------- Mean vs Median ----------
    st.subheader("Mean vs Median")
    st.write("We had to determine the best fit for a true comparison line when calculating a score")
    st.write("What we learned is that the mean line allows for me leeway when giving score, while the median was more strict")
    median = working_df[1:].median(axis=0, skipna=True).tolist()
    average = working_df[1:].mean(axis=0, skipna=True).tolist()
    fig = go.Figure()
    fig.add_trace(go.Box(x=median, name='Median',boxpoints='all',boxmean=True))
    fig.add_trace(go.Box(x=average, name='Average',boxpoints='all',boxmean=True))
    fig.update_xaxes(showgrid=False)
    fig.update_layout(height=1000)
    st.plotly_chart(fig,use_container_width=True, height=1000)

    # ---------- Total picture ----------
    st.subheader("Performance Score for Current Drivers and Current Circuits")
    pp_df = pd.read_csv(Path('data/pp.csv'))
    st.dataframe(pp_df,use_container_width=True)

    # ---------- Normalize using ZScore ----------
    st.subheader("Normalize using ZScore")
    ppnorm_df = pd.read_csv(Path('data/pp_norm.csv'))
    st.dataframe(ppnorm_df,use_container_width=True)

    # ---------- Points outcome ----------
    st.subheader("Predicted Points per circuit")
    champ_df = pd.read_csv(Path('data/driver_champ.csv'))
    st.dataframe(champ_df,use_container_width=True)

with tab5:
    st.title("Outcome")
    champ_df['Total'] = champ_df.sum(axis=1)
    champ_df = champ_df.sort_values('Total',ascending=False)

    col1, col2, col3 = st.columns(3)
    with col1:
        image = Image.open(Path(f'data/images/{champ_df.iloc[1]["Driver"]}.jpg'))
        st.image(image)
        st.subheader(f'2nd place  Driver: {champ_df.iloc[1]["Driver"]}  Points: {champ_df.iloc[1]["Total"]}')

    with col2:
        image = Image.open(Path(f'data/images/{champ_df.iloc[0]["Driver"]}.jpg'))
        st.image(image)
        st.subheader(f'1st place  Driver: {champ_df.iloc[1]["Driver"]}  Points: {champ_df.iloc[1]["Total"]}')

    with col3:
        image = Image.open(Path(f'data/images/{champ_df.iloc[2]["Driver"]}.jpg'))
        st.image(image)
        st.subheader(f'3rd place  Driver: {champ_df.iloc[1]["Driver"]}  Points: {champ_df.iloc[1]["Total"]}')

st.write("")