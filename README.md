# F1_DataScience

*Data Source*: http://ergast.com/mrd/

Run:
> streamlit run main.py

## **Goals**
---
Goal 1: Based on current 2022 drivers, find the probability a driver gets in the top 10 on a track based on their history

Goal 2: Predict winner of F1 2022 drivers championship based on on 10 years of previous race history

## **Packages**
---
-   [Pandas](https://pandas.pydata.org/)
-   [Requests](https://docs.python-requests.org/en/latest/)
-   [ipykernel]()
-   [plotly]()
-   [streamlit]()

## `Consistency Score`

### `Description`
We want to give a score to a driver to reflect how consistent a driver's laps are compared to the rest of the drivers.

On a per lap basis, we calculate the median of all the lap times and compare this to our drivers lap time, percentage wise. Doing this through all the laps will give us a score at the end that reflects how consistent the driver was compared to the rest.

Those who did poorly rate lower, while those who did well rate higher.

### `Anomalies or Outliers`

Because the consistency score is based upon the difference of a single lap compared to the average, we wanted to be sure that the average is a solid base to compare too. 

When comparing the averages for all laps to the median for all laps, what we noticed was that the median was far more grouped then the average and this makes sense. There are a lot of situations in F1 that can go wrong for a driver. They could crash, spin, damage their car, have bad tires, or even take a pit stop all of which would have a significant impact on the average. So by using the median instead, a couple bad laps from drivers is not going to have as much of a impact as it would on the average

This is very much reflective on figure 2. It looks like around lap 71, everyone shared similar "bad" times and this is probably due to a safety car, but it also shows around laps 29-31 that they probably made a pit stop and this had less of a effect on the median line then it did on the average line

`Fig 1) This Graph shows a comparison of all the laps for the 2012 round 6 race using the average vs the median `

![Average vs Median](/images/avgvsmed.png)

`Fig 2) This graph shows the same comparison, but compares it to two drivers: Hamilton and Alonso the higher the points the slower the lap time was, lower the points the faster the lap time was`

![Average vs Median Ham Alo](/images/hamvalo.png)

`Fig 3) The outcome of this produces a list of drivers and their respective scores for 2021 round 6. Those who DNF got a score of nan`

![cs](/images/score.png)


### `Unexpected Patterns or Relationships in the data`

Not that this was unexpected, but the way that the total score a driver gets at the end mostly reflects their end position. While this was to be expected for drivers who simple out performed, we were hoping to see somewhere in the middle a mixed bag of score and position.

## **Data**
---
### `Driver Data`
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

### `Race Data`
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

### `Scheduled Data`
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