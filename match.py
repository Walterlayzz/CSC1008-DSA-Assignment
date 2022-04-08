import json
import math
from Driver import Driver

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

def matchDriver(passengerName):
    fpPassenger  = open("data/passengers.json")
    passengerList = json.load(fpPassenger)

    fpDriver  = open("data/drivers.json")
    driverList = json.load(fpDriver)

    dList = []
    dListSorted = []

    # Obtain nodeID of passenger
    for i in range(len(passengerList)):
        if (passengerList[i]["name"] == passengerName):
            node = passengerList[i]["passengerFromNode"]
    
    # Create a list of Driver objects
    for i in range(len(driverList)):
        dList.append(Driver(driverList[i]["name"], driverList[i]["nodeId"], driverList[i]["longitude"], driverList[i]["latitude"]))
        
    # Update driver distance to passenger attribute
    for i in dList:
        i.distToPass = estDist(node, i.node)

    # Bubble Sort to sort driver based on distance
    for i in range(len(dList)):
        for j in range(0, len(dList) - i - 1):
            if (dList[j].distToPass > dList[j+1].distToPass):
                temp = dList[j]
                dList[j] = dList[j+1]
                dList[j+1]=temp

    # Return a list of sorted driver
    for i in dList:
        dListSorted.append(i.name)

    return dListSorted
