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
        charger =scn.loc[scn['location'] == 'Albany_NY']
        self.assertTrue(round(charger['long'].iloc[0]) == -74)

if __name__ == "__main__":
    unittest.main()
