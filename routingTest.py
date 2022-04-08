import json
import math
from queue import PriorityQueue

class WeightedGraph():
    def __init__(self):
        self.edge = {}

    def neighbour(self, nodeId):
        return list(self.edge.get(nodeId).keys())

    def length(self, fromNodeId, toNodeId):
        return self.edge.get(fromNodeId).get(toNodeId)


def Graph():
    fpNode = open("data/nodes.json")
    fpEdge = open("data/edges.json")

    nodeDict = json.load(fpNode)
    edgeDict = json.load(fpEdge)

    # wg = WeightedGraph()
    graphDict = {}

    for i in edgeDict:
        if i["nodeFrom"] not in graphDict:
            graphDict[i["nodeFrom"]] = list()
        for j in graphDict[i["nodeFrom"]]:
            if i["nodeTo"] not in j:
                graphDict[i["nodeFrom"]].append((i["nodeTo"], i["length"]))

    return graphDict


def dijkstra(G, start, goal):
    visited = set()
    cost = {start: 0}
    parent = {start: None}
    todo = PriorityQueue()

    todo.put((0, start))
    while todo:
        while not todo.empty():
            _, vertex = todo.get()  # finds lowest cost vertex
            # loop until we get a fresh vertex
            if vertex not in visited: break
        else:  # if todo ran out
            break  # quit main loop
        visited.add(vertex)
        if vertex == goal:
            break
        try:
            for neighbor, distance in G[vertex]:
                if neighbor in visited: continue  # skip these to save time
                old_cost = cost.get(neighbor, float('inf'))  # default to infinity
                new_cost = cost[vertex] + distance
                if new_cost < old_cost:
                    todo.put((new_cost, neighbor))
                    cost[neighbor] = new_cost
                    parent[neighbor] = vertex
        except:
            continue

    return parent


def estDist(nodeFrom, nodeTo):
    fpNode = open("data/nodes.json")
    nodeDict = json.load(fpNode)
    fromNodeLon = 0
    fromNodeLat = 0
    toNodeLon = 0
    toNodeLat = 0
    for i in nodeDict:
        if i["nodeId"] == nodeFrom:
            fromNodeLon = i["longitude"]
            fromNodeLat = i["latitude"]

        if i["nodeId"] == nodeTo:
            toNodeLon = i["longitude"]
            toNodeLat = i["latitude"]

    # calculate the approximate distance using the coordinates
    lonDist = math.radians(toNodeLon - fromNodeLon)
    latDist = math.radians(toNodeLat - fromNodeLat)

    a = pow(math.sin(latDist / 2), 2) + math.cos(math.radians(fromNodeLat)) * math.cos(math.radians(toNodeLat)) * pow(
        math.sin(lonDist / 2), 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    dist = (6371 * 1000) * c
    return dist

def make_path(parent, goal):
    if goal not in parent:
        return None
    v = goal
    path = []
    while v is not None: # root has null parent
        path.append(v)
        v = parent[v]
    return path[::-1]

graph = Graph()
routePath = dijkstra(graph, 4734863627, 5239711167)
print(routePath)

nodePath = make_path(routePath, 5239711167)
pathCoord = []

fpNode = open("data/nodes.json")
nodeDict = json.load(fpNode)

for i in range(len(nodePath)):
    for j in range(len(nodeDict)):
        if nodePath[i] == nodeDict[j]["nodeId"]:
            longitude = nodeDict[i]["longitude"]
            latitude = nodeDict[i]["latitude"]
            coord = (latitude, longitude)
            pathCoord.append(coord)

print(pathCoord)