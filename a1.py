import numpy as np
from fastdtw import fastdtw
import math
import gmplot
import pandas as pd
from ast import literal_eval
import itertools as it
import time

def harvesine(u, v):
    # u and v are tuples
    # 0 is longitude 1 is latitude
    R = 6371
    lat1 = math.radians(u[1])
    lat2 = math.radians(v[1])
    Dlat = math.radians(v[1] - u[1])
    Dlon = math.radians(v[0] - u[0])

    a = math.sin(Dlat / 2) * math.sin(Dlat / 2) + math.cos(lat1) * math.cos(lat2) * math.sin(Dlon / 2) * math.sin(Dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    d = R * c
    return d

trainSet = pd.read_csv('./sets/train_set.csv', converters={"Trajectory": literal_eval})
testSet = pd.read_csv('./sets/test_set_a1.csv', converters={"Trajectory": literal_eval})

queries = list()
trains = list()

for traj in testSet["Trajectory"]:
    xi = list()
    for el in traj:
        xi.append( (el[1], el[2]) )
    queries.append(xi)
    
for traj in trainSet["Trajectory"]:
    yi = list()
    for el in traj:
        yi.append( (el[1], el[2]) )
    trains.append(yi)

start = time.time


toSort = list()
TestTrips = list()
# i iindex in train set
for query in queries:
    i = 0
    toSort = []
    for traj in trains:
        distance, path = fastdtw(query, traj, dist=harvesine)
        toSort.append((distance, i))
        i += 1
    Sorted = sorted(toSort, key = lambda x: x[0])
    Sorted = Sorted[:5]
    toAppend = list()
    for trip in Sorted:
        jpid = trainSet["journeyPatternId"][trip[1]]
        route = trainSet["Trajectory"][trip[1]]
        distance = trip[0]
        toAppend.append( (jpid, distance, route) )
    TestTrips.append(toAppend)

i = 1
for k in TestTrips:
    print "Trip "
    j = 1
    for m in k:
        print "\t" + "Neighbour " + str(j)
        print "\t\t" + str(m[0])
        print "\t\t" + str(m[1])
        j += 1
    i += 1
    print "\n"

end = time.time

