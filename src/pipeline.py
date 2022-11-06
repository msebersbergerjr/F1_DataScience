import requests
import json
import os
from pathlib import Path

# -------------------- RAndomFunctions --------------------
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

# -------------------- Initialization --------------------
def init():
    '''Checks if all required directories are created; creates them if not'''

    current_drivers = get_current_drivers()
    filepath = Path('data/drivers')
    
    if not path_exist(filepath):
        os.mkdir(filepath)

    for driver in current_drivers:
        # Check if driver has a unique directory
        filepath = Path(f'data/drivers/{driver}')
        if not path_exist(filepath):
            os.mkdir(filepath)
        # Check if they have info.json
        get_driver_info(driver)

# -------------------- Main --------------------
if __name__ == '__main__':
    init()