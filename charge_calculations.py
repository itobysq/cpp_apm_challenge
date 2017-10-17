"""
Module to calculate the amount of time spent at a sueprcharger
"""

import parse_network as pn

class ChargerPlan(object):
    def __init__(self, table_of_chargers, optimized_path):
        self.nstops = len(optimized_path)
        self.car_range = 320
        self.charge_rates_kmph = [0] * self.nstops
        self.remaining_range = [self.car_range] + ([-1] * (self.nstops - 2))\
                                + [self.car_range]
        self.charging_time = [0] * self.nstops
        self.charger_table = table_of_chargers
        self.distances = [0] * self.nstops
        self.path = optimized_path

    def drive_ok(self, drive_stops):
        for idx, stop in enumerate(drive_stops):
            if idx == self.nstops - 2:
                if stop['km_on_arrival'] > stop['km_to_next_stop']:
                    return True
                else:
                    stop['charge_time'] = (stop['km_to_next_stop'] - stop['km_on_arrival'])\
                                            /stop['charge_rate_kmph']
                    return True
            else:
                next_stop = drive_stops[idx + 1]
                if stop['charge_here']:
                    if (stop['charge_rate_kmph'] < next_stop['charge_rate_kmph']) &\
                        next_stop['charge_here']:
                        stop['charge_time'] = (stop['km_to_next_stop'] - stop['km_on_arrival'])\
                                                /stop['charge_rate_kmph']
                        stop['km_on_departure'] = stop['km_to_next_stop']

                    #if this stop charges faster than the next, charge to the max
                    elif stop['charge_rate_kmph'] > next_stop['charge_rate_kmph']:
                        stop['charge_time'] = (self.car_range - stop['km_on_arrival'])\
                                                /stop['charge_rate_kmph']
                        stop['km_on_departure'] = self.car_range
                    elif stop['charge_time'] < 0:
                        stop['charge_time'] = 0
                        stop['km_on_departure'] = stop['km_on_arrial']
                else:
                    stop['km_on_departure'] = stop['km_on_arrival']

                if stop['km_to_next_stop'] > stop['km_on_departure']:
                    return False
                else:
                    next_stop['km_on_arrival'] = stop['km_on_departure'] - stop['km_to_next_stop']
        return True

    def calculate_time_at_supercharger(self):
        """
        Calculates the time at each supercharger by charging at the fastest 
        supercharger, then recalculating the remaining range at each stop until
        the remaining range at all stops is > 0
        Args:
            charger_table (defaultdict): table of 'city' and 'charge_rate_kmph'
        """
        # populate the distance list and charge_rate list
        drive_snapshots = []
        for idx, city in enumerate(self.path[:-1]):
            status_at_stop = {'city': city,
                              'km_on_departure': -1,
                              'km_on_arrival': -1,
                              'km_to_next_stop': 0,
                              'charge_rate_kmph': 0,
                              'charge_time': 0,
                              'charge_here': False,
                              'index': idx}
            status_at_stop['charge_rate_kmph'] = self.charger_table[city]\
                                                    ['charge_rate_kmph']
            if (idx == 0) | (idx == (self.nstops - 1)):
                status_at_stop['km_on_arrival'] = self.car_range
                status_at_stop['charge_rate_kmph'] = 0
            temp_src = self.charger_table[self.path[idx]]
            if idx + 1 < self.nstops:
                temp_dest = self.charger_table[self.path[idx + 1]]
            status_at_stop['km_to_next_stop'] = pn.calculate_distance((temp_src['lat'],
                                                                temp_src['long']),
                                                               (temp_dest['lat'],
                                                                temp_dest['long']))
            self.charge_rates_kmph[idx] = (self.charger_table[city]['charge_rate_kmph'])
            drive_snapshots.append(status_at_stop.copy())
        top_chargers = sorted(drive_snapshots,
                              key=lambda k:k['charge_rate_kmph'])
        while not self.drive_ok(drive_snapshots):
            charger_to_add = top_chargers.pop()
            drive_snapshots[charger_to_add['index']]['charge_here'] = True

        output_string = self.build_output_string(drive_snapshots)
        return output_string

    def build_output_string(self, drive_info):
        output_string = '{}, '.format(drive_info[0]['city'])
        for idx, pitstop in enumerate(drive_info[1:]):
            print(output_string)
            middle_part = '{}, {}, '.format(pitstop['city'],
                                            pitstop['charge_time'])
            output_string = output_string + middle_part
        return output_string + '{}'.format(self.path[-1])

