from fastdtw import fastdtw
from harversine import harvesine

def dtwdistance(u, v):
    distance, __path = fastdtw(u, v, dist=harvesine)
    return distance