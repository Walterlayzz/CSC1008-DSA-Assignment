import json
import math
import PriorityQueue


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

    wg = WeightedGraph()

    for i in nodeDict:
        edgesTo = {}
        for j in edgeDict:
            if i["nodeId"] == j["nodeFrom"]:
                edgesTo.update({j["nodeTo"]: j["length"]})
        wg.edge.update({i["nodeId"]: edgesTo})
    return wg


def Route(wg: WeightedGraph, startNode, endNode):
    prioQ = PriorityQueue.PriorityQueue()
    prioQ.enqueue(startNode, 0)

    route = {}
    costTable = {}

    route[startNode] = None
    costTable[startNode] = 0


    count = 0
    while not prioQ.isEmpty():
        currNode = prioQ.dequeue()
        if currNode["nodeId"] == endNode:
            return route

        for i in wg.neighbour(currNode["nodeId"]):
            cost = costTable[currNode["nodeId"]] + wg.length(currNode["nodeId"], i)
            if i not in costTable or cost < costTable[i]:
                costTable[i] = cost
                dist = cost + estDist(i, endNode)
                prioQ.enqueue(i, dist)
                route[i] = currNode["nodeId"]
    print("No Path")
    return False


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
routePath = Route(graph, 4734863627, 5239711167)
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