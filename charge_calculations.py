"""
Module to calculate the amount of time spent at a sueprcharger
"""

import parse_network as pn

class ChargerPlan(object):
    def __init__(self, table_of_chargers, optimized_path):
        self.nstops = len(optimized_path)
        self.car_range = 320
        self.charge_rates_kmph = [0] * self.nstops
        self.remaining_range = [self.car_range] + ([-1] * (self.nstops - 1))
        self.charging_time = [0] * self.nstops
        self.charger_table = table_of_chargers
        self.distances = [0] * self.nstops
        self.path = optimized_path

    def calculate_path_distance(self, subpath):
        """
        Calculates the great circle distance along a given subpath
        Args:
            charger_table (defaultdict): a subpath of of the shortest path to
                the destination. The subpath is a list of cities.
        Returns:
            dist_to_go (float): km measurement of far to go until the end of 
                the subpath or when a supercharger is reached
        """
        counter = 1
        dist_to_go = 0
        for city in subpath[1:]:
            temp_src = self.charger_table[subpath[counter - 1]]
            temp_dest = self.charger_table[subpath[counter]]
            dist_to_go += pn.calculate_distance((temp_src['lat'], temp_src['long']),
                                                (temp_dest['lat'], temp_dest['long']))
            counter += 1
            # if the charger in the destination city is used, return
            if self.remaining_range[self.path.index(temp_dest)] == 320:
                return dist_to_go
        return dist_to_go

    def calculate_km_charge_remaining(self):
        for idx, range_at_stop_km in enumerate(self.remaining_range):
            if range_at_stop_km == self.car_range:
                pass
            else:
                self.remaining_range[idx] = self.remaining_range[idx - 1] -\
                                                self.distances[idx - 1]

    def calculate_time_at_supercharger(self):
        """
        Calculates the time at each supercharger by charging at the fastest 
        supercharger, then recalculating the remaining range at each stop until
        the remaining range at all stops is > 0
        Args:
            charger_table (defaultdict): table of 'city' and 'charge_rate_kmph'
        """
        # populate the distance list and charge_rate list
        for idx, city in enumerate(self.path):
            self.charge_rates_kmph[idx] = (self.charger_table[city]['charge_rate_kmph'])
            temp_src = self.charger_table[self.path[idx]]
            if idx + 1 < self.nstops:
                temp_dest = self.charger_table[self.path[idx + 1]]
                self.distances[idx] = pn.calculate_distance((temp_src['lat'],
                                                                temp_src['long']),
                                                               (temp_dest['lat'],
                                                                temp_dest['long']))
        self.charge_rates_kmph[0] = 0
        self.charge_rates_kmph[-1] = 0
        while any(charge < 0 for charge in self.remaining_range):
            import ipdb; ipdb.set_trace() # BREAKPOINT
            charge_index = self.charge_rates_kmph.index(max(self.charge_rates_kmph))
            dist_to_compensate = self.calculate_path_distance(
                                                              self.path[charge_index:])
            if dist_to_compensate > self.car_range:
                dist_to_compensate = self.car_range
            self.remaining_range[charge_index] = self.car_range
            self.calculate_km_charge_remaining()
            self.charging_time[charge_index] = dist_to_compensate / self.charge_rates_kmph[charge_index]
            self.charge_rates_kmph[charge_index] = 0
        output_string = self.build_output_string()
        return self.build_output_string()

    def build_output_string(self):
        output_string = '{}, '.format(self.path[0])
        for idx, city in enumerate(self.path[1:-1]):
            middle_part = '{}, {}, '.format(city, self.charging_time[1:-1][idx])
            output_string = output_string + middle_part
        return output_string + '{}'.format(self.path[-1])

