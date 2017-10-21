"""Wrapper for MARTA Bus Realtime RESTful API"""
import json as json_
import requests
from datetime import datetime


class BusClient:
    """API client"""
    url = ("http://developer.itsmarta.com/BRDRestService"
           "/RestBusRealTimeService/GetAllBus")
    route_url = ("http://developer.itsmarta.com/BRDRestService"
                 "/RestBusRealTimeService/GetBusByRoute/{}")

    def __init__(self):
        pass

    def buses(self, route=None):
        """Get all active buses
        
        :param route: When supplied, only returns active buses for *route*
        :return: ``Buses(list)``
        """
        if route:
            return self._route(route)
        return self._all()

    @staticmethod
    def _all():
        """Returns all active buses"""
        return Buses(requests.get(BusClient.url).json())

    @staticmethod
    def _route(route):
        """Returns active buses for *route*"""
        return Buses(requests.get(BusClient.route_url.format(str(route)))
                     .json())


class Buses(list):
    """List of active buses"""
    def __init__(self, buses):
        self._buses = None
        self.buses = buses
        super().__init__(self.buses)

    @property
    def buses(self):
        return self._buses

    @buses.setter
    def buses(self, buses):
        self._buses = [Bus.from_json(b) for b in buses]

    def filter(self, adherence=None, block_id=None, block_abbr=None,
               direction=None, latitude=None, longitude=None,
               msg_time=None, route=None, stop_id=None, timepoint=None,
               trip_id=None, vehicle=None):
        """Returns a list of buses matching supplied criteria"""
        filter_kws = {
            'adherence': adherence,
            'block_id': block_id,
            'block_abbr': block_abbr,
            'direction': direction,
            'latitude': latitude,
            'longitude': longitude,
            'msg_time': msg_time,
            'route': route,
            'stop_id': stop_id,
            'timepoint': timepoint,
            'trip_id': trip_id,
            'vehicle': vehicle
        }
        for k, v in filter_kws.items():
            if not v:
                continue
            self = self._filter(k, v)
        return self

    def _filter(self, attribute_name, value):
        v = getattr(self[0], attribute_name)
        print(v)
        return [bus for bus in self if getattr(bus, attribute_name) == value]


class Bus:
    _attr_map = {
        'ADHERENCE': 'adherence',
        'BLOCKID': 'block_id',
        'BLOCK_ABBR': 'block_abbr',
        'DIRECTION': 'direction',
        'LATITUDE': 'latitude',
        'LONGITUDE': 'longitude',
        'MSGTIME': 'msg_time',
        'ROUTE': 'route',
        'STOPID': 'stop_id',
        'TIMEPOINT': 'timepoint',
        'TRIPID': 'trip_id',
        'VEHICLE': 'vehicle'
    }

    def __init__(self, adherence, block_id, block_abbr, direction,  latitude,
                 longitude, msg_time, route, stop_id, timepoint, trip_id,
                 vehicle, json):
        self.adherence = adherence
        self.block_id = block_id
        self.block_abbr = block_abbr
        self.direction = direction
        self.latitude = latitude
        self.longitude = longitude
        self._msg_time = None
        self.msg_time = msg_time
        self.route = route
        self.stop_id = stop_id
        self.timepoint = timepoint
        self.trip_id = trip_id
        self.vehicle = vehicle
        #: Original JSON response
        self.json = json

    @property
    def msg_time(self):
        return self._msg_time

    @msg_time.setter
    def msg_time(self, msg_time):
        if not msg_time:
            self._msg_time = None
        self._msg_time = datetime.strptime(msg_time, "%m/%d/%Y %I:%M:%S %p")

    @staticmethod
    def from_json(json_obj):
        kwargs = {Bus._attr_map[k]: v for (k, v) in json_obj.items()}
        return Bus(json=json_.dumps(json_obj), **kwargs)

    def __str__(self):
        return self.json

    def __repr__(self):
        return str(self)

