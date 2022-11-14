# F1_DataScience

*Data Source*: http://ergast.com/mrd/

Run:
> streamlit run main.py

## **Goals**
---
Goal 1: Based on current 2022 drivers, find the probability a driver gets in the top 10 on a track based on their history

Goal 2: Predict winner of F1 2022 drivers championship basedon on 10 years of previouse race history

## **Packages**
---
-   [Pandas](https://pandas.pydata.org/)
-   [Requests](https://docs.python-requests.org/en/latest/)

## **Data**
---
### Driver Data
`data/current_drivers.json`

*Current Drivers Data*: http://ergast.com/api/f1/2022/drivers.json?limit=1000

This request returns all the drivers who have raced this year and basic information about them
```
{
    "driverId"
    "permanentNumber"
    "code"
    "url"
    "givenName"
    "familyName"
    "dateOfBirth"
    "nationality"
}
```

### Race Data
`data/races/{year}/{round}.json`

*Season Round Data* http://ergast.com/api/f1/{year}/{round}/laps.json?limit=100000

This request returns a given years given round lap data
```
{
    "season"
    "round"
    "url"
    "raceName"
    "Circuit": {
        "circuitId"
        "url"
        "circuitName"
        "Location": {
            "lat"
            "long"
            "locality"
            "country"
        }
    },
    "date"
    "time"
    "Laps"
}
```

### Scheduled Data
`data/schedlued/{year}.json`

*Scheduled Races Data* http://ergast.com/api/f1/{year}.json?limit=1000

This request returns all the races within a given year
```
{
    "season"
    "round"
    "url"
    "raceName"
    "Circuit": {
        "circuitId"
        "url"
        "circuitName"
        "Location": {
            "lat"
            "long"
            "locality"
            "country"
        }
    },
    "date"
    "time"
}
```

## **Authors**:
---
-   Marc Ebersberger Jr
-   Logan Gillum