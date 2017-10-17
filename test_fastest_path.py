"""
Test module for finding the fastest path
"""
import parse_network as pn
import pathfinder as pf
import unittest

class TestFastPath(unittest.TestCase):
    def setUp(self):
        self.network = pn.ChargerNetwork('network.cpp')
        self.charger_graph = pf.construct_graph()

    def test_graph_constructor(self):
        dist = charger_graph.distances[('Albany_NY', 'West_Lebanon_NH')]
        self.assertTrue(round(dist) == 158)

    def test_big_path(self):
        pf.main('Albany_NY', 'Truckee_CA')

    def test_small_path(self):
        pf.main('Albany_NY', 'West_Lebanon_NH')

if __name__ == "__main__":
    unittest.main()
