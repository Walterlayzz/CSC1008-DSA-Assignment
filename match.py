import json
import math

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

