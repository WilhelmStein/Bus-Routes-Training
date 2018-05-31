import math

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
