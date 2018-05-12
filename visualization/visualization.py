import gmplot
import pandas as pd
from ast import literal_eval
import itertools as it
from numpy import mean

trainSet = pd.read_csv('./sets/train_set.csv', converters={"Trajectory": literal_eval}, index_col='tripId')
count = 0
lines = set()
colours = [ 'cornflowerblue', 'red', 'orange', 'purple' , 'pink' ]

for jpid, traj in it.izip(trainSet['journeyPatternId'], trainSet['Trajectory']):

    if count == 5:
        break

    if jpid not in lines:
        lines.add(jpid)
        lons = list()
        lats = list()
        for el in traj:
            lons.append(el[1])
            lats.append(el[2])
        gmap = gmplot.GoogleMapPlotter(mean(lats), mean(lons), 13)
        name = "./plots/line" + str(count) + ".html"
        gmap.plot(lats, lons, colours[count], edge_width=5)
        gmap.draw(name)
        count += 1

