import gmplot
import pandas as pd
from ast import literal_eval
import itertools as it
from numpy import mean

trainSet = pd.read_csv('../sets/test_set_a1.csv', converters={"Trajectory": literal_eval})
count = 0
colours = [ 'cornflowerblue', 'red', 'orange', 'purple' , 'pink' ]

for traj in trainSet['Trajectory']:
    if count == 5:
        break
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
        

