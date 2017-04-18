"""
API client library for the MARTA Rail Realtime RESTful API

More info: http://www.itsmarta.com/app-developer-resources.aspx

"""

import json
import requests
from datetime import datetime
from warnings import warn
from collections import OrderedDict, defaultdict


station_list = [
    'AIRPORT STATION',
    'ARTS CENTER STATION',
    'ASHBY STATION',
    'AVONDALE STATION',
    'BANKHEAD STATION',
    'BROOKHAVEN STATION',
    'BUCKHEAD STATION',
    'CHAMBLEE STATION',
    'CIVIC CENTER STATION',
    'COLLEGE PARK STATION',
    'DECATUR STATION',
    'DORAVILLE STATION',
    'DUNWOODY STATION',
    'EAST LAKE STATION',
    'EAST POINT STATION',
    'EDGEWOOD CANDLER PARK STATION',
    'FIVE POINTS STATION',
    'GARNETT STATION',
    'GEORGIA STATE STATION',
    'HAMILTON E HOLMES STATION',
    'INDIAN CREEK STATION',
    'INMAN PARK STATION',
    'KENSINGTON STATION',
    'KING MEMORIAL STATION',
    'LAKEWOOD STATION',
    'LENOX STATION',
    'LINDBERGH STATION',
    'MEDICAL CENTER STATION',
    'MIDTOWN STATION',
    'NORTH AVE STATION',
    'NORTH SPRINGS STATION',
    'OAKLAND CITY STATION',
    'OMNI DOME STATION',
    'PEACHTREE CENTER STATION',
    'SANDY SPRINGS STATION',
    'VINE CITY STATION',
    'WEST END STATION',
    'WEST LAKE STATION'
 ]


class RailClient:
    """Client for the MARTA rail API to retrieve pending arrivals.
    
    The API returns an 'arrival' in a dict like:
    
    .. code-block:: json
    
        {
            "DESTINATION":  "North Springs",
            "DIRECTION":    "N",
            "EVENT_TIME":   "12/31/2017 4:09:10 PM",
            "LINE":         "BLUE",
            "NEXT_ARR":     "04:12:10 PM",
            "STATION":      "NORTH SPRINGS STATION",
            "TRAIN_ID":     "104026",
            "WAITING_SECONDS": "-45",
            "WAITING_TIME": "Boarding"
        }
            
    """
    base_url = "http://developer.itsmarta.com/RealtimeTrain" \
               "/RestServiceNextTrain/GetRealtimeArrivals?apikey={api_key}"

    def __init__(self, api_key):
        """Initialize client

        :param api_key: MARTA API key
        :type api_key: str
        """
        self.api_key = api_key
        self._trains = None

    def arrivals(self):
        """Retrieves and returns current arrivals as ``Arrivals(list)``
            
        :return: A list of current train arrivals (events)
        :rtype: ``martapy.rail.Arrivals(list)``
        """
        arrivals = requests.get(self.url).json()
        # Copy each dict to a new one with lowercase keys to pass to Arrival()
        return Arrivals(arrivals)

    @property
    def url(self):
        """``RailClient.base_url`` formatted with API key"""
        return self.base_url.format(api_key=self.api_key)


class Arrivals(list):
    """A list of ``Arrival`` objects returned from the API"""
    def __init__(self, arrivals):
        """
        :param arrivals: List of ``Arrival`` objects
        :type arrivals: ``martapy.rail.Arrival``
        """
        self._arrivals = None
        self.arrivals = arrivals
        super().__init__(self._arrivals)

    @property
    def arrivals(self):
        """All ``Arrival`` objects"""
        return self._arrivals

    @arrivals.setter
    def arrivals(self, arrivals):
        # Transforms JSON objects to a list of ``Arrival`` objects
        arrival_list = []
        for arrival in arrivals:
            a = Arrival(**dict((k.lower(), v) for (k, v) in arrival.items()))
            a.json = arrival
            arrival_list.append(a)
        self._arrivals = arrival_list
        self._arrivals.sort(key=lambda ar: ar.next_arr)
        self.__new_station()

    # Line filters

    @property
    def blue_line(self):
        """Arrivals for the blue line"""
        return self._filter('line', 'BLUE')

    @property
    def gold_line(self):
        """Arrivals for the gold line"""
        return self._filter('line', 'GOLD')

    @property
    def green_line(self):
        """Arrivals for the green line"""
        return self._filter('line', 'GREEN')

    @property
    def red_line(self):
        """Arrivals for the red line"""
        return self._filter('line', 'RED')

    # Directional filters

    @property
    def northbound(self):
        """Northbound arrivals"""
        return self._filter('direction', 'N')

    @property
    def eastbound(self):
        """Eastbound arrivals"""
        return self._filter('direction', 'E')

    @property
    def westbound(self):
        """Westbound arrivals"""
        return self._filter('direction', 'W')

    @property
    def southbound(self):
        """Southbound arrivals"""
        return self._filter('direction', 'S')

    @property
    def boarding(self):
        """Arrivals that are currently boarding"""
        return self._filter('waiting_time', 'Boarding')

    @property
    def arriving(self):
        """Arrivals that are... arriving"""
        return self._filter('waiting_time', 'Arriving')

    @property
    def arrived(self):
        """Arrivals that have arrived"""
        return self._filter('waiting_time', 'Arrived')

    # Misc filters

    @property
    def trains(self):
        """Arrivals grouped by train ID
        
        :return: *OrderedDict*, train IDs as keys and each train's 
            associated arrivals as lists
        """
        trains = defaultdict(list)
        for a in self._arrivals:
            trains[a.train_id].append(a)
        # Sort by arrival time
        for train_events in trains.values():
            train_events.sort(key=lambda x: x.next_arr)
        return OrderedDict(sorted(trains.items()))

    @property
    def stations(self):
        """Arrivals grouped by station name
        
        :return: *OrderedDict* with station names as keys and associated 
            arrivals as values
        """
        station_arrivals = defaultdict(list)
        for a in self._arrivals:
            station_arrivals[a.station].append(a)

        return OrderedDict(sorted(station_arrivals.items()))

    def by_station(self, station_name):
        """Filter arrivals by station.

        :param station_name: Name of the station to filter.
            Ex: *LENOX*
        :type station_name: str
        :return: List of arrivals for this station
        """
        station_name = station_name.upper()
        found_station = None
        for s in station_list:
            if station_name in s:
                found_station = s
                break
        if not found_station:
            msg = "'{}' not found in station list.".format(station_name)
            warn(msg)
        return self._filter('station', found_station)

    def __new_station(self):
        """Iterate through arrivals, checking for any station names that aren't
        in the known list. Raises warnings for any that aren't found and
        adds them to the list.

        :raises Warning: If a station name is found that isn't in
            ``martapy.rail.station_list``
        :return:
        """
        station_names = list(self.stations.keys())
        for s in station_names:
            if s not in station_list:
                station_list.append(s)
                msg = ("Received station '{}' which wasn't found in the known "
                       "stations list. New station?").format(s)
                warn(msg)

    def _filter(self, attribute_name, value):
        """Filter Arrivals based on a key/value pair.

        :param attribute_name: Name of the attribute to filter. Such as
            *line* or *station*
        :type attribute_name: str
        :param value: Value to look for (such as *RED* for line)
        :type value: str
        :return: ``martapy.rail.Arrivals`` containing matching arrivals
        """
        filtered = [json.loads(a.json) for a in self.arrivals if
                    getattr(a, attribute_name) == value]
        return Arrivals(filtered)


class Arrival:
    def __init__(self, station, line, destination, direction, next_arr,
                 waiting_time, waiting_seconds, event_time, train_id):
        """Arrival event

        :param station: Station name (uppercase)
        :param line: Line (BLUE, GREEN, RED, GOLD)
        :param destination: Train destination (generally similar to a
            station name, ex: 'AIRPORT STATION' becomes 'Airport')
        :param direction: Cardinal direction (N, S, E, W)
        :param next_arr: Time of the next arrival, as HH:MM:SS AM/PM
        :param waiting_time: Arriving, Arrived, Boarding, 1 min, 2 min, ...
        :param waiting_seconds: Example: '-45'
        :param event_time: Timestamp as MM/DD/YYYY H:MM:SS AM/PM
        :param train_id: Train ID
        """
        self._direction = None
        self._event_time = None
        self._json = None
        self._next_arr = None

        self.direction = direction
        self.event_time = event_time
        self.train_id = train_id
        self.next_arr = next_arr

        #: Destination (station name sans '*STATION*')
        self.destination = destination

        #: *RED*, *GREEN*, *BLUE*, or *GOLD* line
        self.line = line

        #: Station name (current list: ``martapy.rail.station_list``)
        self.station = station.upper()

        #: Positive or negative integer (ex '*-45*' seconds)
        self.waiting_seconds = waiting_seconds

        #: *Arriving*, *Arrived*, *Boarding*, *1 min*, *2 min*...
        self.waiting_time = waiting_time

    @property
    def direction(self):
        """Direction of travel as one of: *N, E, W, S*"""
        return self._direction

    @direction.setter
    def direction(self, direction):
        """Set the direction of travel.
        
        :param direction: N, E, W or S
        :type direction: str
        :return: 
        """
        choices = ['N', 'E', 'W', 'S']
        direction = direction.upper()
        if direction not in choices:
            raise ValueError("Direction must be one of: {}"
                             .format(','.join(choices)))
        else:
            self._direction = direction

    @property
    def event_time(self):
        """Event timestamp. (Note: This isn't a timestamp of the API call"""
        return self._event_time

    @event_time.setter
    def event_time(self, event_time):
        """Set the event time as *MM/DD/YYYY HH:MM:SS AM/PM*"""
        self._event_time = datetime.strptime(event_time,
                                             "%m/%d/%Y %I:%M:%S %p")

    @property
    def next_arr(self):
        """Time of the train's next arrival as *HH:MM:SS AM/PM*"""
        return self._next_arr

    @property
    def next_arrival(self):
        """Time of the train's next arrival. (Same as next_arr() property)"""
        return self.next_arr

    @next_arr.setter
    def next_arr(self, next_arr):
        """Sets NEXT_ARR (next arrival time)
        
        :param next_arr: Timestamp as HH:MM:SS AM/PM
        :type next_arr: str
        :return: 
        """
        self._next_arr = datetime.strptime(next_arr, "%I:%M:%S %p").time()

    def __str__(self):
        """JSON string of original API response (or one imitating it)"""
        return self.json

    @property
    def json(self):
        """JSON string of the original API response, or one imitating it."""
        if self._json is not None:
            return self._json
        # If it hasn't been set yet, create our own dict, updating keys with
        # properties and popping keys that don't belong
        d = dict((k.upper(), v) for (k, v) in self.__dict__.items())
        replacement_keys = ['_DIRECTION', '_EVENT_TIME', '_NEXT_ARR']
        for key in replacement_keys:
            d[key.lstrip('_')] = d.pop(key)
        if '_JSON' in d:
            d.pop('_JSON')
        d['EVENT_TIME'] = d['EVENT_TIME'].strftime("%m/%d/%Y %I:%M:%S %p")
        d['NEXT_ARR'] = d['NEXT_ARR'].strftime("%I:%M:%S %p")
        return json.dumps(d)

    @json.setter
    def json(self, json_obj):
        """Set JSON dictionary attribute.

        :param json_obj: Arrival JSON
        :type json_obj: ``str`` or ``dict``
        :return:
        """
        j_dict = None
        if isinstance(json_obj, str):
            j_dict = json.loads(json_obj)
        elif isinstance(json_obj, dict):
            j_dict = json_obj
        self.__has_keys(j_dict)
        self._json = json.dumps(j_dict)

    @staticmethod
    def __has_keys(arrival):
        """Verifies the provided arrival dictionary has the necessary keys.

        Expected keys:
         * DESTINATION
         * DIRECTION
         * EVENT_TIME
         * LINE
         * NEXT_ARR
         * STATION
         * TRAIN_ID
         * WAITING_SECONDS
         * WAITING_TIME

        :param arrival: Arrival JSON from MARTA API
        :type arrival: dict
        :return: True if all keys are found
        :raises KeyError: If the provided dict has an unexpected key or
            is missing an expected key.
        """
        expected_keys = [
            'DESTINATION',
            'DIRECTION',
            'EVENT_TIME',
            'LINE',
            'NEXT_ARR',
            'STATION',
            'TRAIN_ID',
            'WAITING_SECONDS',
            'WAITING_TIME'
        ]
        arrival_keys = list(arrival.keys())
        unique_keys = set(expected_keys) ^ set(arrival_keys)
        if unique_keys:
            raise KeyError("Found unexpected keys.\n\tExpected: {}\n\t"
                           "Not in list: {}".format(','.join(expected_keys),
                                                    ','.join(unique_keys)))
        return True

