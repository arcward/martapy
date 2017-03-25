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
from martapy import rail
from martapy.rail import RailClient
from configparser import ConfigParser


class TestArrivals(TestCase):
    def setUp(self):
        test_config = ConfigParser()
        test_config.read('config.ini')
        api_key = test_config.get('rail', 'api_key')
        self.api_client = RailClient(api_key=api_key)
        self.r = self.api_client.arrivals()

    def test_stations(self):
        for a in self.arrivals:
            self.assertIn(a.station, rail.stations)

    def test_all(self):
        # Ensure all results have the keys we're expecting
        arrival_list = self.r.arrivals
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
                self.assertIsNotNone(getattr(arrival, field.lower()),
                                     "All responses should have these fields")

        for arrival in arrival_list:
            self.assertIn(arrival.station, rail.stations)

    def test_chain(self):
        red_north = self.r.red_line.northbound
        self.assertGreaterEqual(len(red_north), 1)
        for rn in red_north:
            self.assertEqual("RED", rn.line)
            self.assertEqual("N", rn.direction)

    def test_line(self):
        # Ensure all lines return results
        arrivals = self.r.blue_line
        for a in arrivals:
            self.assertEqual('BLUE', a.line)

        arrivals = self.r.red_line
        for a in arrivals:
            self.assertEqual('RED', a.line)

        arrivals = self.r.green_line
        for a in arrivals:
            self.assertEqual('GREEN', a.line)

        arrivals = self.r.gold_line
        for a in arrivals:
            self.assertEqual('GOLD', a.line)

    def test_directions(self):
        n = self.r.northbound
        e = self.r.eastbound
        w = self.r.westbound
        s = self.r.southbound

        for a in n:
            self.assertEqual(a.direction, 'N')
        for a in e:
            self.assertEqual(a.direction, 'E')
        for a in w:
            self.assertEqual(a.direction, 'W')
        for a in s:
            self.assertEqual(a.direction, 'S')

    def test_lines(self):
        red = self.r.red_line
        green = self.r.green_line
        gold = self.r.gold_line
        blue = self.r.blue_line

        for a in red:
            self.assertEqual(a.line, 'RED')
        for a in green:
            self.assertEqual(a.line, 'GREEN')
        for a in gold:
            self.assertEqual(a.line, 'GOLD')
        for a in blue:
            self.assertEqual(a.line, 'BLUE')

    def test_waiting_time(self):
        boarding = self.r.boarding
        arrived = self.r.arrived
        arriving = self.r.arriving

        for a in boarding:
            self.assertEqual(a.waiting_time, 'Boarding')
        for a in arrived:
            self.assertEqual(a.waiting_time, 'Arrived')
        for a in arriving:
            self.assertEqual(a.waiting_time, 'Arriving')

    def test_station(self):
        # Match a partial station name
        example_station = 'Peachtree'
        station_list = self.r.by_station(example_station)
        self.assertGreaterEqual(len(station_list), 1,
                                "Try testing a station that has some results")

        # Ensure all stations in the station list returns results
        for s in rail.stations:
            arrivals = self.r.arrivals(station=s)
            self.assertGreaterEqual(len(arrivals), 1, "{}".format(s))
            for a in arrivals:
                self.assertEqual(s, a.station)

        # API returns uppercase stations
        for s in station_list:
            self.assertTrue(example_station.upper() in s.station)
