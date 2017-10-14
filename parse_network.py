"""
Module for importing .cpp files and converting them into distances
"""
import pandas as pd
import CppHeaderParser
import time

class ChargerNetwork(object):
    """
    Class to parse a supercharger network text file into a nice lookup csv to use
    when we implement dijkstra's algorithm.
        Args:
            filename (str): string of the filename 
    """
    def __init__(self, filename):
        self.fn = filename
        self.supercharger_info = None
        self.distance_table = None

    def parse_file(self):
        charger_network = []
        with open(self.fn, mode='r') as f:
            for line in f:
                line = f.readline()
                if '{' in line:
                    line = line.rstrip(",\n")
                    line = line.replace('{', '').replace("'",'').replace('"','')\
                                                .replace('}','').split(',')
                    line = [x.strip() for x in line]
                    position_counter = 0
                    charger_info={'location': None, 'lat': None, 'long': None,
                            'charge_rate_kmph': None}
                    for info in line:
                        position_counter += 1
                        if position_counter == 1:
                            charger_info['location'] = info
                        elif position_counter == 2:
                            charger_info['lat'] = float(info)
                        elif position_counter == 3:
                            charger_info['long'] = float(info)
                        elif position_counter == 4:
                            charger_info['charge_rate_kmph'] = float(info)
                            position_counter = 0
                            charger_network.append(charger_info.copy())
        self.supercharger_network = pd.DataFrame(charger_network)


