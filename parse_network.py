"""
Module for importing .cpp files and converting them into distances
"""
import time
import math

class ChargerNetwork(object):
    """
    Class to parse a supercharger network text file into a nice lookup csv to use
    when we implement dijkstra's algorithm.
        Args:
            filename (str): string of the filename 
    """
    def __init__(self, filename):
        self.fn = filename
        self.supercharger_network = None
        self.distance_table = None

    def parse_file(self):
        charger_network = []
        with open(self.fn, mode='r') as f:
            for line in f:
                if '{' in line:
                    line = line.rstrip(",\n")
                    line = line.replace('{', '').replace("'",'').replace('"','')\
                                                .replace('}','').split(',')
                    line = [x.strip() for x in line]
                    position_counter = 0
                    charger_info={'city': None, 'lat': None, 'long': None,
                            'charge_rate_kmph': None}
                    for info in line:
                        position_counter += 1
                        if position_counter == 1:
                            charger_info['city'] = info
                        elif position_counter == 2:
                            charger_info['lat'] = float(info)
                        elif position_counter == 3:
                            charger_info['long'] = float(info)
                        elif position_counter == 4:
                            charger_info['charge_rate_kmph'] = float(info)
                            position_counter = 0
                            charger_network.append(charger_info.copy())
        self.supercharger_network = charger_network

def calculate_distance(start_latlong, end_latlong):
    """
    Function for finding the distance between two supercharger sites
    """
    earth_radius_m = 6356.752
    start_lat, start_long, end_lat, end_long = map(math.radians,[start_latlong[0],
                                                                start_latlong[1],
                                                                end_latlong[0],
                                                                end_latlong[1]])
    lat_delta_rad = (end_lat - start_lat)
    long_delta_rad = (end_long - start_long)
    chord = math.sin(lat_delta_rad/2)**2 + math.cos(start_lat) *\
            math.cos(end_lat) * math.sin(long_delta_rad/2)**2
    angular_dist = 2 * math.atan2(math.sqrt(chord), math.sqrt(1-chord))
    distance = earth_radius_m * angular_dist
    return distance
