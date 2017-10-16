"""
Test module for finding the fastest path
"""
import parse_network as pn
import pathfinder as pf
import unittest

class TestFastPath(unittest.TestCase):
    def setUp(self):
        self.network = pn.ChargerNetwork('network.cpp')

    def test_graph_constructor(self):
        charger_graph = pf.construct_graph()
        dist = charger_graph.distances[('Albany_NY', 'West_Lebanon_NH')]
        self.assertTrue(round(dist) == 158)

if __name__ == "__main__":
    unittest.main()
