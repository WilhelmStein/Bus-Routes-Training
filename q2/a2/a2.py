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
from itertools import izip

trainSet = pd.read_csv('../../sets/train_set.csv', converters={"Trajectory": literal_eval})
testSet = pd.read_csv('../../sets/test_set_a2.csv', converters={"Trajectory": literal_eval})
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

fds = list()

for i in xrange(1, len(queries) + 1):
    name = "./a2Plots/Test Trip " + str(i) + "/Info.txt"
    f = open(name, "w+")
    fds.append(f)

toSort = list()
TestTrips = list()
# i is index in train set
for query, file in izip(queries, fds):
    start = time.time()

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
        route = trains[trip[1]]
        toAppend.append( (jpid, trip[0], route) )
    TestTrips.append(toAppend)

    end = time.time()
    duration = end - start
    file.write("Time : " + str(duration) + "\n")

i = 1
for query, test, file in izip(queries, TestTrips, fds):

    # Draw query map
    querylons = list()
    querylats = list()
    for lons, lats in query:
        querylons.append(lons)
        querylats.append(lats)

    gmap = gmplot.GoogleMapPlotter(np.mean(querylats), np.mean(querylons), 13)

    name = "./a2Plots/Test Trip " + str(i) + "/Query.html"
    gmap.plot(querylats, querylons, 'green', edge_width=5)
    gmap.draw(name)

    j = 1
    # for each neighbour draw neighbour map with green and common subsequence with red
    for neighbour in test:

        routelons = list()
        routelats = list()
        sbsqlons = list()
        sbsqlats = list()
        for lons, lats in neighbour[2]:
            routelons.append(lons)
            routelats.append(lats)
        for lons, lats in neighbour[1]:
            sbsqlons.append(lons)
            sbsqlats.append(lats)
        
        gmapn = gmplot.GoogleMapPlotter(np.mean(routelats), np.mean(routelons), 13)

        name = "./a2Plots/Test Trip " + str(i) + "/Neighbour " + str(j) + ".html"
        file.write("Neighbour " + str(j) + " :\tMatchingPoints : " + str(len(neighbour[1])) + "\t" + " JPID : " + neighbour[0] + "\n")

        gmapn.plot(routelats, routelons, 'green', edge_width=5)
        gmapn.plot(sbsqlats, sbsqlons, 'red', edge_width=5)
        gmapn.draw(name)
        j += 1
    i += 1
    file.close()



end = time.time
