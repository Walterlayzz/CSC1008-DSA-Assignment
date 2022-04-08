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


def Route(WeightedGraph, startNode, endNode):
    routeNodes = {}
    costNodes = {}
    routeNodes[startNode] = None
    costNodes[startNode] = 0
    prioQ = PriorityQueue.PriorityQueue()
    prioQ.enqueue(startNode, 0)

    while not prioQ.isEmpty():
        currNode = prioQ.dequeue()
        if currNode["nodeId"] == endNode:
            return routeNodes

        for i in WeightedGraph.neighbour(currNode["nodeId"]):
            cost = costNodes[currNode["nodeId"]] + WeightedGraph.length(currNode["nodeId"], i)
            if i not in costNodes or cost < costNodes[i]:
                costNodes[i] = cost
                dist = cost + estDist(i, endNode)
                prioQ.enqueue(i, dist)
                routeNodes[i] = currNode["nodeId"]


def makePath(parent, goal):
    if goal not in parent:
        return None
    v = goal
    path = []
    while v is not None: # root has null parent
        path.append(v)
        v = parent[v]
    return path[::-1]


def estDist(nodeFrom, nodeTo):
    fpNode = open("data/nodes.json")
    nodeDict = json.load(fpNode)

    fromNodeLon = 0
    fromNodeLat = 0
    toNodeLon = 0
    toNodeLat = 0
    meter = 6371 * 1000

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

    return meter * c


def convertPathToCoord(startNode, endNode):
    wg = Graph()
    routePath = Route(wg, startNode, endNode)

    nodePath = makePath(routePath, endNode)
    pathCoord = []

    fpNode = open("data/nodes.json")
    nodeDict = json.load(fpNode)

    for i in range(len(nodePath)):
        for j in range(len(nodeDict)):
            if nodePath[i] == nodeDict[j]["nodeId"]:
                longitude = nodeDict[j]["longitude"]
                latitude = nodeDict[j]["latitude"]
                coord = (latitude, longitude)
                pathCoord.append(coord)

    return pathCoord

# print(convertPathToCoord(1249576750 , 1787007911))

# "name": "Maury", "passengerFromNode": 1249576750, "passengerToNode": 1787007911,
# {
#     "name": "Daniel",
#     "nodeId": 5129163188,
#     "longitude": 103.8017649,
#     "latitude": 1.2866672
#     },