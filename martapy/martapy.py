"""
MIT License

Copyright (c) 2016 - Edward Wells

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import requests


class Rail:
    """Client for the MARTA rail API to retrieve pending arrivals."""
    def __init__(self, api_key):
        base_url = "http://developer.itsmarta.com/"
        arrivals_url = "RealtimeTrain/RestServiceNextTrain/GetRealtimeArrivals?apikey={}"
        self.url = ''.join([base_url, arrivals_url.format(api_key)])

    def arrivals(self, station=None):
        """Retrieve list of real-time train arrivals from MARTA API.
        If station isn't specified, all entries will be returned.
        Otherwise, specify part of the station name (ex: "Buckhead") and matching entries will be returned.
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
        all_arrivals = requests.get(self.url).json()
        if station is not None:
            return [arrival for arrival in all_arrivals if station.upper() in arrival['STATION']]
        else:
            return all_arrivals
