import numpy as np
import gmplot
import pandas as pd
from ast import literal_eval
import itertools as it
import time
from dtwdistance import dtwdistance
from sklearn.preprocessing import LabelEncoder
from knearestbrute import KNearestBrute
from sklearn.metrics import classification_report
from sklearn.model_selection import KFold
# Metrics
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score


def appendLists(list1, list2):
    retlist = list()
    for elem in list1:
        retlist.append(elem)
    for elem in list2:
        retlist.append(elem)
    return retlist


trainSet = pd.read_csv('./sets/train_set.csv', converters={"Trajectory": literal_eval})
trainSet = trainSet[:len(trainSet) / 10]

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


k = 10
size = len(X)

precs = 0
recs = 0
f1s = 0
accs = 0

for i in xrange(0, k):
    print "Iteration : " + str(i)
    X_test = X[ (size / k) * i : (size / k) * (i + 1)]
    X_train = appendLists(X[: (size / k) * i], X[(size / k) * (i + 1):])

    y_test = y[ (size / k) * i : (size / k) * (i + 1)]
    y_train = appendLists(y[: (size / k) * i], y[(size / k) * (i + 1):])

    clf.fit(X_train, y_train)    
    predictions = clf.predict(X_test)


    precs += precision_score(y_test, predictions, average='macro')
    recs += recall_score(y_test, predictions, average='macro')
    f1s += f1_score(y_test, predictions, average='macro')
    accs += accuracy_score(y_test, predictions)

avgprec = precs / k
avgrec = recs / k
avgf1 = f1s / k
avgacc = accs / k

print "Precision : " + str(avgprec)
print "Recall : " + str(avgrec)
print "F1 - Measure : " + str(avgf1)
print "Accuracy : " + str(avgacc)


end = time.time()
duration = end - start
print str(duration)


