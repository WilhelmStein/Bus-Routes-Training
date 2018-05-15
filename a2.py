import numpy as np
from fastdtw import fastdtw
import math
import gmplot
import pandas as pd
from ast import literal_eval
import itertools as it
import time
from harversine import harvesine
from lcss import lcss

trainSet = pd.read_csv('./sets/train_set.csv', converters={"Trajectory": literal_eval})
testSet = pd.read_csv('./sets/test_set_a2.csv', converters={"Trajectory": literal_eval})
#trainSet = trainSet[:100]
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
        sbsq = lcss(query, traj, 0.2)  
        toSort.append((sbsq, i))
        i += 1
    Sorted = sorted(toSort, key = lambda x: len(x[0]))
    Sorted = Sorted[-5:]
    toAppend = list()
    for trip in Sorted:
        jpid = trainSet["journeyPatternId"][trip[1]]
        route = trainSet["Trajectory"][trip[1]]
        distance = len(trip[0])
        toAppend.append( (jpid, distance, route) )
    TestTrips.append(toAppend)

i = 1
for k in TestTrips:
    print "Trip " + str(i)
    j = 1
    for m in k:
        print "\t" + "Neighbour " + str(j)
        print "\t\tJP_ID: " + str(m[0])
        print "\t\tMatching Points: " + str(m[1])
        j += 1
    i += 1
    print "\n"

end = time.time
