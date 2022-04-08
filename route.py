import json
import math
from queue import PriorityQueue


def Graph():
    fpEdge = open("data/edges.json")

    edgeDict = json.load(fpEdge)

    graphDict = {}

    for i in edgeDict:
        if i["nodeFrom"] not in graphDict:
            graphDict[i["nodeFrom"]] = list()
        graphDict[i["nodeFrom"]].append((i["nodeTo"], i["length"]))
    return graphDict


def dijkstra(G, startNode, endNode):
    visited = set()
    dist = {startNode: 0}
    parent = {startNode: None}
    priorityQueue = PriorityQueue()
    priorityQueue.put((0, startNode))

    while priorityQueue:
        while not priorityQueue.empty():
            _, vertex = priorityQueue.get()  # finds lowest cost vertex
            # loop until we get a fresh vertex
            if vertex not in visited: break
        else:  # if todo ran out
            break  # quit main loop
        visited.add(vertex)
        if vertex == endNode:
            break
        try:
            for neighbor, distance in G[vertex]:
                if neighbor in visited: continue  # skip these to save time
                oldDist = dist.get(neighbor, float('inf'))  # default to infinity
                newDist = dist[vertex] + distance
                if newDist < oldDist:
                    priorityQueue.put((newDist, neighbor))
                    dist[neighbor] = newDist
                    parent[neighbor] = vertex
        except:
            continue

    return parent



def makePath(parent, goal):
    if goal not in parent:
        return None
    v = goal
    path = []
    while v is not None: # root has null parent
        path.append(v)
        v = parent[v]
    return path[::-1]



def convertPathToCoord(startNode, endNode):
    graph = Graph()
    routePath = dijkstra(graph, startNode, endNode)
    print(routePath)
    #list of nodes to traverse
    nodePath = makePath(routePath, endNode)
    pathCoord = []

    fpNode = open("data/nodes.json")
    nodeDict = json.load(fpNode)

    #convert the list of nodes to list of coordinates
    for i in range(len(nodePath)):
        for j in range(len(nodeDict)):
            if nodePath[i] == nodeDict[j]["nodeId"]:
                longitude = nodeDict[j]["longitude"]
                latitude = nodeDict[j]["latitude"]
                coord = (latitude, longitude)
                pathCoord.append(coord)

    return pathCoord

print(convertPathToCoord(1249576750 , 1787007911))

# "name": "Maury", "passengerFromNode": 1249576750, "passengerToNode": 1787007911,
# {
#     "name": "Daniel",
#     "nodeId": 5129163188,
#     "longitude": 103.8017649,
#     "latitude": 1.2866672
#     },
