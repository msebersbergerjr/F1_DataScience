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
    original_title = '<p style="font-family:Courier New, monospace;font-weight: 500; color:white; font-size: 90px;">Rubber Casino</p>'
    st.markdown(original_title, unsafe_allow_html=True)

font_css = """
<style>
button[data-baseweb="tab"] {
  font-family:Courier New, monospace;
  font-size: 20px;
  word-spacing: -5px;
  padding: 20px;
  
}
</style>
"""

st.write(font_css, unsafe_allow_html=True)

tabs = st.tabs(['Introduction','Formula One','Exploratory Analysis','Performance Score','Outcome'])

with tabs[0]:

    goal_title = '<p style="font-family:Courier New, monospace;font-weight:500; color:white; font-size: 45px;">Goal</p>'
    st.markdown(goal_title, unsafe_allow_html=True)

    goal_text = '<p style="font-family:Courier New, monospace;font-weight:500; color:white; font-size: 20px;">We wanted to build a statistical model that can predict the 2022 Grand Prix winners by using historical performance data for Formula One Drivers.</p>'
    st.markdown(goal_text, unsafe_allow_html=True)

    st.markdown("---")

    approach_title = '<p style="font-family:Courier New, monospace;font-weight:500; color:white; font-size: 45px;">Approach</p>'
    st.markdown(approach_title, unsafe_allow_html=True)

    approach_text = '<p style="font-family:Courier New, monospace;font-weight:500; color:white; font-size: 20px;">After collecting the F1 data from the Ergast API, we conducted our EDA and found that we could use the Time variable (per lap) to create derived variables.</p>'
    approach_text_2 = '<p style="font-family:Courier New, monospace;font-weight:500; color:white; font-size: 20px;"> These derived variables served as the basis for our analysis and predictions.</p>'
    st.markdown(approach_text, unsafe_allow_html=True)
    st.markdown(approach_text_2,unsafe_allow_html=True)

    st.markdown("---")

    limits_title = '<p style="font-family:Courier New, monospace;font-weight:500; color:white; font-size: 45px;">Limitations</p>'
    st.markdown(limits_title,unsafe_allow_html=True)

    limits_text = '<p style="font-family:Courier New, monospace;font-weight:500; color:white; font-size: 20px;"> Due to the nature of Formula One, there are too many variables to factor in when attempting to produce an accurate model. </p>'
    limits_text_2 = '<p style="font-family:Courier New, monospace;font-weight:500; color:white; font-size: 20px;"> Examples of these limitations are Weather, Strategies, Car Models, Track Alterations, Regulations, and Quality of Team Engineers. </p>'
    st.markdown(limits_text,unsafe_allow_html=True)
    st.markdown(limits_text_2,unsafe_allow_html=True)

    pic_cols = st.columns(3)

    with pic_cols[1]:
        st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/FIA_F1_Austria_2019_Nr._77_Bottas_1.jpg/800px-FIA_F1_Austria_2019_Nr._77_Bottas_1.jpg',width=800,caption=2019)
    with pic_cols[0]:
        st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Alonso_%28Renault%29_qualifying_at_USGP_2005.jpg/800px-Alonso_%28Renault%29_qualifying_at_USGP_2005.jpg',width=1030,caption=2005)
    with pic_cols[2]:
        st.image('https://www.formula1.com/content/dam/fom-website/manual/Misc/2021manual/AbuDhabiTrack/Updated%20Abu%20Dhabi%20Circuit%2016x9%20WEB%20Slide%201.jpg.transform/9col/image.jpg',width=800,caption='Track Alterations')

with tabs[1]:

    champ_title = '<p style="font-family:Courier New, monospace;font-weight:500; color:white; font-size: 45px;">Championships</p>'
    st.markdown(champ_title, unsafe_allow_html=True)

    champ_text = '<p style="font-family:Courier New, monospace;font-weight:500; color:white; font-size: 20px;">There are two types of championships in Formula One, Constructor and Driver.</p>'
    st.markdown(champ_text,unsafe_allow_html=True)
    champ_text_2 = '<p style="font-family:Courier New, monospace;font-weight:500; color:white; font-size: 20px;">Championships are scored by the following point system: </p>'
    st.markdown(champ_text_2,unsafe_allow_html=True)


    points_data = [{'Position':'Points','1st':25,'2nd':18,'3rd':15,'4th':12,'5th':10,'6th':8,'7th':6,'8th':4,'9th':2,'10th':1,'FL':1}]
    # point_df = pd.DataFrame(points_data).set_index('Position')
    # point_cols = st.columns(11)

    # for x in range(len(point_df.columns)):
    #     with point_cols[x]:
    #         st.write(point_df.columns[x])
    #         st.text(point_df.loc['Points'][x])

    st.dataframe(pd.DataFrame(points_data).set_index('Position'),use_container_width=True)

    footnote_text = '<p style="font-family:Courier New, monospace;font-weight:500; color:white; font-size: 13px;text-indent: 25px">*A driver must finish within the top ten to receive a point for setting the fastest lap of the race.</p>'
    st.markdown(footnote_text,unsafe_allow_html=True)

    st.markdown("---")


    c_champ_title = '<p style="font-family:Courier New, monospace;font-weight:500; color:white; font-size: 35px;">Constructor Championships</p>'
    st.markdown(c_champ_title, unsafe_allow_html=True)

    c_champ_text = '<p style="font-family:Courier New, monospace;font-weight:500; color:white; font-size: 17px;">A Constructor is a team within Formula One.</p>'
    st.markdown(c_champ_text,unsafe_allow_html=True)

    st.write('')

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
    },{
        'Team':'Car',
        'Alfa Romeo':'https://www.formula1.com/content/dam/fom-website/teams/2022/alfa-romeo.png.transform/4col/image.png',
        'AlphaTauri':'https://www.formula1.com/content/dam/fom-website/teams/2022/alphatauri.png.transform/4col/image.png',
        'Alpine':'https://www.formula1.com/content/dam/fom-website/teams/2022/teamcar-alpine.png.transform/4col/image.png',
        'Aston Martin':'https://www.formula1.com/content/dam/fom-website/teams/2022/aston-martin.png.transform/4col/image.png',
        'Ferrari':'https://www.formula1.com/content/dam/fom-website/teams/2022/ferrari.png.transform/4col/image.png',
        'Haas':'https://www.formula1.com/content/dam/fom-website/teams/2022/haas-f1-team.png.transform/4col/image.png',
        'McLaren':'https://www.formula1.com/content/dam/fom-website/teams/2022/teamcar-mclaren.png.transform/4col/image.png',
        'Mercedes':'https://www.formula1.com/content/dam/fom-website/teams/2022/mercedes.png.transform/4col/image.png',
        'Red Bull':'https://www.formula1.com/content/dam/fom-website/teams/2022/red-bull-racing.png.transform/4col/image.png',
        'Williams':'https://www.formula1.com/content/dam/fom-website/teams/2022/williams.png.transform/4col/image.png'
        }]

    cs_df = pd.DataFrame(construct_data).set_index("Team")

    car_cols = st.columns(10)

    st.write('')

    for x in range(len(cs_df.columns)):
        with car_cols[x]:
            st.image(cs_df.loc['Car'][x],width=300)
            st.write(cs_df.columns[x])
            st.write(cs_df.loc['Country'][x])

    c_champ_text_2 = '<p style="font-family:Courier New, monospace;font-weight:500; color:white; font-size: 17px;">Constructors are teams with Two Drivers, Engineers, Crew. Drivers are assigned the role of Primary or Support based on early performance in a circuit.</p>'
    st.markdown(c_champ_text_2,unsafe_allow_html=True)

    c_champ_text_3 = '<p style="font-family:Courier New, monospace;font-weight:500; color:white; font-size: 17px;">Funding is provided to teams based on the points earned by their driver. 1 point is worth roughly 1 million dollars.</p>'
    st.markdown(c_champ_text_3,unsafe_allow_html=True)
    
    st.markdown("---")

    d_champ_title = '<p style="font-family:Courier New, monospace;font-weight:500; color:white; font-size: 35px;">Driver Championships</p>'
    st.markdown(d_champ_title, unsafe_allow_html=True)

    d_champ_text = '<p style="font-family:Courier New, monospace;font-weight:500; color:white; font-size: 17px;">Points are earned by drivers that place in the Top 10.</p>'
    st.markdown(d_champ_text,unsafe_allow_html=True)
    st.markdown('---')


with tabs[2]:
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

    st.markdown("---")


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

    st.markdown("---")

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

    st.markdown("---")

    st.title("Outliers")
    st.write("We expect there to be a handle full of outliers from our data from the nature of the sport")
    st.write("Expected outliers in lap data results: Pit Stop, Safety Cars, Crashes, Weather, etc...")
    st.write("We left them in since it doesn't hinder out outcome, and also its apart of the sport.")

    st.markdown("---")

    

# -------------------- Performance Score --------------------
with tabs[3]:
    st.header("Performance Score")
    st.subheader("Description- what is a performance score")

    st.subheader("Season: 2012 Round: 1")

    # ---------- RAW DATA ----------
    st.subheader("Raw Data - Time Series")
    df =  get_race(2012, 1)
    st.dataframe(df)
    st.markdown("---")
    
    # ---------- CONVERTED DATA ----------
    st.subheader("Converted Data - Time Series represented as seconds (float)")
    working_df = df.copy()
    for col in working_df.columns[1:]: working_df[col] = working_df[col].apply(lambda x : time_to_nanoseconds(x))
    st.dataframe(working_df)
    st.markdown("---")

    # ---------- Lap time Vertically ----------
    st.subheader("Lap times Vertically")
    fig = go.Figure()
    for col in working_df.columns[1:]:
        fig.add_trace(go.Box(y=working_df[col].values.tolist(), name=col, boxmean=True))
    fig.update_yaxes(type="log", showgrid=False)
    fig.update_layout(height=1000)

    st.plotly_chart(fig,use_container_width=True, height=1000)
    st.markdown("---")

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
    st.markdown("---")

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

    st.markdown("---")


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
    st.markdown("---")

    # ---------- Total picture ----------
    st.subheader("Performance Score for Current Drivers and Current Circuits")
    pp_df = pd.read_csv(Path('data/pp.csv'))
    st.dataframe(pp_df,use_container_width=True)
    st.markdown("---")

    # ---------- Normalize using ZScore ----------
    st.subheader("Normalize using ZScore")
    ppnorm_df = pd.read_csv(Path('data/pp_norm.csv'))
    st.dataframe(ppnorm_df,use_container_width=True)
    st.markdown("---")

    # ---------- Points outcome ----------
    st.subheader("Predicted Points per circuit")
    champ_df = pd.read_csv(Path('data/driver_champ.csv'))
    st.dataframe(champ_df,use_container_width=True)
    st.markdown("---")

with tabs[4]:
    st.title("Outcome")
    champ_df['Total'] = champ_df.sum(axis=1)
    champ_df = champ_df.sort_values('Total',ascending=False)

    col1, col2, col3 = st.columns(3)
    with col1:
        image = Image.open(Path(f'data/images/{champ_df.iloc[1]["Driver"]}.jpg'))
        st.image(image)
        st.subheader(f'2nd: {champ_df.iloc[1]["Driver"].capitalize()}\n Points: {champ_df.iloc[1]["Total"]}')

    with col2:
        image = Image.open(Path(f'data/images/{champ_df.iloc[0]["Driver"]}.jpg'))
        st.image(image)
        st.subheader(f'1st:  {champ_df.iloc[0]["Driver"].capitalize()}\n  Points:  {champ_df.iloc[0]["Total"]}')

    with col3:
        image = Image.open(Path(f'data/images/{champ_df.iloc[2]["Driver"]}.jpg'))
        st.image(image)
        st.subheader(f'3rd: {champ_df.iloc[2]["Driver"].capitalize()}\n  Points: {champ_df.iloc[2]["Total"]}')

st.write("")