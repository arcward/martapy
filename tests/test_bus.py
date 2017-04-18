from unittest import TestCase
from martapy import bus


class TestBuses(TestCase):
    def setUp(self):
        self.client = bus.BusClient()

    def test_all(self):
        buses = self.client.buses()
        for b in buses:
            for k in bus.Bus._attr_map.values():
                self.assertIsNotNone(getattr(b, k))

    def test_filter(self):
        buses = self.client.buses().filter(direction='Westbound')
        for b in buses:
            self.assertEqual('Westbound', b.direction)

    def test_route(self):
        buses = self.client.buses(route=111)
        for b in buses:
            self.assertEqual('111', b.route)
