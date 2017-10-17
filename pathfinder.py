from collections import defaultdict
import charge_calculations as cc
import parse_network as pn
import sys

class Graph:
  def __init__(self):
    self.nodes = set()
    self.edges = defaultdict(list)
    self.distances = {}

  def add_node(self, value):
    self.nodes.add(value)

  def add_edge(self, from_node, to_node, distance):
    self.edges[from_node].append(to_node)
    self.edges[to_node].append(from_node)
    self.distances[(from_node, to_node)] = distance
    self.distances[(to_node, from_node)] = distance

def dijsktra(graph, initial, dest):
  visited = {initial: 0}
  path = {}

  nodes = set(graph.nodes)

# loop through all of the nodes and see if they're 
# visited, find the min_node and go there
  while nodes: 
    min_node = None
    for node in nodes:
      if node in visited:
        if min_node is None:
          min_node = node
        # find the closest node, and reassign as the
        # min node
        elif visited[node] < visited[min_node]:
          min_node = node

    if min_node is dest:
      break

# once there is a min node, remove it from the list of rows to visit
# explore all the edges and choose the one with the lowest weight
# add the new weights to each edge of the node that is
# currently being considerend
    nodes.remove(min_node)
    current_weight = visited[min_node]
    for edge in graph.edges[min_node]:
      weight = current_weight + graph.distances[(min_node, edge)]
      if edge not in visited or weight < visited[edge]:
        visited[edge] = weight
        path[edge] = min_node

  return visited, path

def construct_graph():
    network = pn.ChargerNetwork('network.cpp')
    network.parse_file()
    scn = network.supercharger_network
    charger_graph = Graph()
    for src in scn.keys():
        src = scn[src]
        charger_graph.add_node(src['city'])
        for dest in scn.keys():
            dest = scn[dest]
            if (src['city'], dest['city']) in charger_graph.distances:
                pass
            else:
                distance = pn.calculate_distance((src['lat'], src['long']),
                                                 (dest['lat'], dest['long']))
                if (distance < 320) & (distance > 0):
                    charger_graph.add_edge(src['city'], dest['city'],
                                           distance)
    return charger_graph, scn

def parse_output(path, source, dest):
    path_instructions = [dest]
    backtrace_node = dest
    while backtrace_node != source:
        path_instructions.append(path[backtrace_node])
        backtrace_node = path[backtrace_node]
    return path_instructions[::-1]


def main(source, dest):
    charger_graph, supercharger_table = construct_graph()
    visited, tesla_path = dijsktra(charger_graph, source, dest)
    instructions = parse_output(tesla_path, source, dest)
    planner = cc.ChargerPlan(supercharger_table, instructions)
    plan = planner.calculate_time_at_supercharger()
    print(plan)

if __name__ == "__main__":
    main()
