import requests
import json
import os
from pathlib import Path

# -------------------- RandomFunctions --------------------
def connection(url):
    '''
    Try and Establish a Connection to given website
    Return: data in json format
    '''

    try:
        response = requests.get(url)
        
        if not response.status_code // 100 == 2:
            return(f"Error: Unexpected response {response}")

        geodata = response.json()
        return(geodata)

    except requests.exceptions.RequestException as e:
        return(f"Error: {e}")

def path_exist(filepath):
    '''Checks if a filepath exist or not'''
    if os.path.exists(filepath):
        print('Data Status: Stored')
        return True
    print('Data Source: Gathered')
    return False

# -------------------- Driver Data --------------------
def get_current_drivers():
    '''Returns list of current years drivers'''
    
    filepath = Path('data/current_drivers.json')
    jsondata = dict()

    # Checks if data is already stored
    if path_exist(filepath):
        with open(filepath, 'r', encoding='utf-8') as infile: jsondata = json.load(infile)
    else:
        # Request data from API
        link = 'http://ergast.com/api/f1/2022/drivers.json?limit=1000'
        jsondata = connection(link)
        jsondata = jsondata['MRData']['DriverTable']['Drivers']
        # Store the data under data/current_drivers.json
        json_object = json.dumps(jsondata, indent=4)
        with open(filepath, 'w', encoding='utf-8') as outfile: outfile.write(json_object)

    current_drivers = list()
    for driver in jsondata:
        current_drivers.append(driver['driverId'])
    return current_drivers

def get_driver_info(driver):
    '''Returns basic information on driver'''

    filepath = Path(f'data/drivers/{driver}/info.json')
    jsondata = dict()

    # Checks if data is already stored
    if path_exist(filepath):
        with open(filepath, 'r', encoding='utf-8') as infile: jsondata = json.load(infile)
    else:
        # Create a drivers info.json based on data in current_drivers.json
        with open(Path('data/current_drivers.json'), 'r', encoding='utf-8') as infile: jsondata = json.load(infile)
        for drivers in jsondata:
            if drivers['driverId'] == driver:
                # Create info.json
                driverId = drivers['driverId']
                permanentNumber = drivers['permanentNumber']
                givenName = drivers['givenName']
                familyName = drivers['familyName']
                dateOfBirth = drivers['dateOfBirth']
                nationality = drivers['nationality']
                info = {'driverId':driverId,'permanentNumber':permanentNumber,
                        'givenName':givenName,'familyName':familyName,
                        'dateOfBirth':dateOfBirth,'nationality':nationality}
                json_object = json.dumps(info, indent=4)
                with open(filepath, 'w', encoding='utf-8') as outfile: outfile.write(json_object)
                with open(filepath, 'r', encoding='utf-8') as infile: jsondata = json.load(infile)
    return jsondata

# -------------------- Race Data --------------------

def get_scheduled_races(year):
    '''Get all the scheduled races of a given year'''

    filepath = Path(f'data/scheduled/')
    jsondata = dict()

    # Check if scheduled directory exist
    if not path_exist(filepath):
        os.mkdir(filepath)

    # Check if scheduled year.json exist
    filepath = Path(f'data/scheduled/{year}.json')
    if path_exist(filepath):
        with open(filepath, 'r', encoding='utf-8') as infile: jsondata = json.load(infile)

    else:
        # Requests scheudlued races in given year
        link = f'http://ergast.com/api/f1/{year}.json?limit=1000'
        jsondata = connection(link)
        jsondata = jsondata['MRData']['RaceTable']['Races']
        # Store the data under data/current_drivers.json
        json_object = json.dumps(jsondata, indent=4)
        with open(filepath, 'w', encoding='utf-8') as outfile: outfile.write(json_object)

    return jsondata

def get_season_rounds(year):
    '''return the number of rounds in the given season'''

    filepath = Path(f'data/scheduled/{year}.json')
    if not path_exist(filepath):
        print('Scheduled Year data doesnt exist')
        raise

    with open(filepath, 'r', encoding='utf-8') as infile: jsondata = json.load(infile)
    return len(jsondata)

def get_season_round_data(year,_round):
    '''Gets every lap within a race of a given year'''

    jsondata = dict()
    filepath = Path(f'data/races')
    if not path_exist(filepath):
        os.mkdir(filepath)

    filepath = Path(f'data/races/{year}/')
    if not path_exist(filepath):
        os.mkdir(filepath)

    # Check if a years round.json exist
    filepath = Path(f'data/races/{year}/{_round}.json')
    if path_exist(filepath):
        with open(filepath, 'r', encoding='utf-8') as infile: jsondata = json.load(infile)
    else:
        # Requests scheudlued races in given year
        link = f'http://ergast.com/api/f1/{year}/{_round}/laps.json?limit=100000'
        jsondata = connection(link)
        jsondata = jsondata['MRData']['RaceTable']['Races'][0]
        # Store the data under data/current_drivers.json
        json_object = json.dumps(jsondata, indent=4)
        with open(filepath, 'w', encoding='utf-8') as outfile: outfile.write(json_object)

    return jsondata

# -------------------- Initialization --------------------
def init():
    '''Checks if all required directories are created; creates them if not'''

    current_drivers = get_current_drivers()
    filepath = Path('data/drivers')
    
    if not path_exist(filepath):
        os.mkdir(filepath)

    # Checks current drivers
    for driver in current_drivers:
        # Check if driver has a unique directory
        filepath = Path(f'data/drivers/{driver}')
        if not path_exist(filepath):
            os.mkdir(filepath)
        # Check if they have info.json
        get_driver_info(driver)
    
    # Checks year data 2012-2022
    for year in range(2012,2023):
        get_scheduled_races(year)

    # Checks year round data
    for year in range(2012,2022):
        # get the amount of rounds in a year
        rounds = get_season_rounds(year)
        for _round in range(1,rounds+1):
            get_season_round_data(year,_round)

# -------------------- Main --------------------
if __name__ == '__main__':
    init()