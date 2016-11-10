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
        example_station = 'Peachtree'
        station_list = self.r.arrivals(example_station)
        self.assertTrue(len(station_list) > 0, "Try testing a station that has some results..")
        for s in station_list:
            self.assertTrue(example_station.upper() in s['STATION'])  # API uses uppercase stations
