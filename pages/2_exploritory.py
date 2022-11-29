import streamlit as st
from PIL import Image
import pandas as pd
import os
import numpy as np
import json
from pathlib import Path
from datetime import datetime
import plotly.express as px

# -------------------- CONFIG --------------------
# Sets the configuration of the page. Currently using a wide layout to use entire screen realistate
st.set_page_config(page_title="F1 Datascience",page_icon=":zap:", layout="wide")

st.title("Exploratory Analysis")


st.title("Source")

st.write("Ergast Developer API [Source](http://ergast.com/mrd/)")

st.write("Formula1.com [Source](https://www.formula1.com/)")

st.title("Data Sets")

st.header("Scheduled Data")

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