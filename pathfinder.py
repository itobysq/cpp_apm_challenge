from collections import defaultdict
import parse_network as pn


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
    for src in scn:
        charger_graph.add_node(src['city'])
        for dest in scn:
            if (src['city'], dest['city']) in charger_graph.distances:
                pass
            else:
                charger_graph.add_edge(src['city'],
                                       dest['city'],
                                       pn.calculate_distance((src['lat'],
                                                              src['long']),
                                                             (dest['lat'],
                                                              dest['long']))
                                       )
    return charger_graph

