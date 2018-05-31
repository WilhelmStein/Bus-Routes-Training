import itertools as it
from math import sqrt
import time
from fastdtw import fastdtw
from harversine import harvesine

class KNearestBrute:
    def __init__(self, labels, k_neighbours=5):
        self.k_neighbours = k_neighbours
        self.data = list()
        self.label_set = labels
            

    def fit(self, X, y):
        for con, lab in it.izip(X, y):
            self.data.append( (con, lab) )


    def predict(self, X_test):
        predictions = list()
        for u in X_test:
            dists = list()

            for traj, lab in self.data:
                distance = self.__distance(u, traj)
                dists.append( (distance, lab) )

            # Sort the list so we can get the k closest neighbours
            dists = sorted(dists, key=lambda dist: dist[0])

            nearest = dists[:self.k_neighbours]

            # Find Majority
            predictions.append(self.__findMajority(nearest))
        return predictions


    def __findMajority(self, dists):
        labels = dict()
        # Make a dict of occurences of each label in dists
        for l in self.label_set:
            labels[l] = 0
        for __dist, lab in dists:
            labels[lab] += 1

        # Find max label
        maxval = 0
        maxkey = -1
        for key, value in labels.iteritems():
            if value > maxval:
                maxval = value
                maxkey = key
        return maxkey

    # Harvesine distance of 2 trajectories
    def __distance(self, U, V):
        distance, __path = fastdtw(U, V, dist=harvesine)
        return distance
