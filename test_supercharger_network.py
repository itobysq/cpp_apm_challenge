"""
Test module for my solution
"""
import parse_network as pn
import unittest

class TestFileParser(unittest.TestCase):
    def setUp(self):
        self.network = pn.ChargerNetwork('network.cpp')

    def test_parse_file(self):
        self.network.parse_file()
        scn = self.network.supercharger_network
        charger =scn.loc['Albany_NY']
        self.assertTrue(round(charger['long']) == -74)

    def test_distance_calculator(self):
        self.network.parse_file()
        scn = self.network.supercharger_network
        dist = pn.calculate_distance((scn.loc['Albany_NY']['lat'],
                          scn.loc['Albany_NY']['long']),
                          (scn.loc['West_Lebanon_NH']['lat'],
                           scn.loc['West_Lebanon_NH']['long']))
        self.assertTrue(round(dist) == 158)

    def test_distance_table(self):
        self.network.parse_file()
        distance_table = self.network.build_distance_table()
        dist = distance_table.loc['Albany_NY', 'West_Lebanon_NH']
        self.assertTrue(round(dist) == 158)

    def test_build_charger_network_info(self):
        self.network.build_charger_network_tables()
        self.assertTrue((self.network.supercharger_network is not None) &
                         (self.network.distance_table is not None))

if __name__ == "__main__":
    unittest.main()
