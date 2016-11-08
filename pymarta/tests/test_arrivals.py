from unittest import TestCase
from pymarta.pymarta import Rail


class TestArrivals(TestCase):
    def setUp(self):
        self.r = Rail()
    
    def test_all(self):
        self.r = Rail()
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
