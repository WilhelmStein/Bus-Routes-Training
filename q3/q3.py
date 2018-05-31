import numpy as np
import gmplot
import pandas as pd
from ast import literal_eval
import itertools as it
import time
from sklearn.preprocessing import LabelEncoder
from knearestbrute import KNearestBrute


trainSet = pd.read_csv('../sets/train_set.csv', converters={"Trajectory": literal_eval})
testSet = pd.read_csv('../sets/test_set_a2.csv', converters={"Trajectory": literal_eval})

start = time.time()

le = LabelEncoder()
y = le.fit_transform(trainSet['journeyPatternId'])

y = list(y)

X = list()

clf = KNearestBrute(set(y), k_neighbours=5)

for traj in trainSet["Trajectory"]:
    xi = list()
    for el in traj:
        xi.append( [el[1], el[2]] )
    X.append(xi)

X_test = list()

for traj in testSet['Trajectory']:
    xi = list()
    for el in traj:
        xi.append( [el[1], el[2]] )
    X_test.append(xi)



clf.fit(X, y)    
predictions = clf.predict(X_test)
predictions = le.inverse_transform(predictions)
print predictions

f = open("../sets/testSet_JourneyPatternIDs.csv", "w+")
f.write("Test_Trip_ID\tPredicted_JourneyPatternID\n")

for i in xrange(0, len(predictions)):
    f.write(str(i + 1) + "\t" + str(predictions[i]) + "\n")
f.close


end = time.time()
duration = end - start
print str(duration)
