import requests
import configparser
import os
from configparser import ConfigParser
import datetime

class Rail:
    def __init__(self):
        config = ConfigParser()
        config._interpolation = configparser.ExtendedInterpolation()
        config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
        self.url_arrivals = config.get('Rail', 'url_arrivals')
        self.dashing_url = config.get('Dashing', 'url')
        self.dashing_token = config.get('Dashing', 'auth_token')
    
    def arrivals(self, station=None):
        """Retrieve list of real-time train arrivals from MARTA API
        Each arrival in returned list is a dict like:
        {
            'DESTINATION':  'North Springs'          # The destination area, not the station name
            'DIRECTION':    'N'                      # Direction as either N, E, W, S
            'EVENT_TIME':   '12/31/2017 4:09:10 PM'  # The time as MM/DD/YYYY H:MM:SS (AM/PM)
            'LINE':         'BLUE'                   # BLUE, GREEN, GOLD, RED
            'NEXT_ARR':     '04:12:10 PM'            # Time of the next arrival as HH:MM:SS AM/PM
            'STATION':      'NORTH SPRINGS STATION'  # The actual station name
            'TRAIN_ID':     '104026'
            'WAITING_SECONDS': '-45'
            'WAITING_TIME': 'Boarding'               # Arriving, Arrived, Boarding,... 1 min, 2 min, 3 min...
        }
        """
        raw_arrivals = requests.get(self.url_arrivals)
        all_arrivals = raw_arrivals.json()
        
        if station is not None:
            return [arrival for arrival in all_arrivals if station in arrival['STATION']]
        else:
            return all_arrivals
        
    def dashing_push(self):
        arr = self.arrivals('BUCKHEAD')
        dashing_friendly = [
            {
                'label': event['DESTINATION'],
                'value': event['WAITING_TIME']
            } for event in arr
        ]
        
        d_data = {
            'auth_token': self.dashing_token,
            'title': 'Buckhead station',
            'items': dashing_friendly
        }
        requests.post(url=self.dashing_url, json=d_data)