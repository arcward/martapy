from unittest import TestCase
from martapy.martapy import Rail
from configparser import ConfigParser


class TestArrivals(TestCase):
    def setUp(self):
        test_config = ConfigParser()
        test_config.read('config.ini')
        api_key = test_config.get('rail', 'api_key')
        self.r = Rail(api_key=api_key)
    
    def test_all(self):
        arrival_list = self.r.arrivals()
        print(arrival_list)
        
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
        
        for arrival in arrival_list:
            for field in expected_keys:
                self.assertIsNotNone(arrival[field], "All responses should have these fields")
        
    def test_station(self):
        example_station = 'BUCKHEAD'
        station_list = self.r.arrivals(example_station)
        for s in station_list:
            self.assertTrue(example_station in s['STATION'])
