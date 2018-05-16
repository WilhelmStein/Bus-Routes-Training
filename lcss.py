import numpy as np
from harversine import harvesine

def lcss(u, v, match_error_margin):

    def bt(t, u, v, match_error_margin, i , j): # Backtrack through matrix t in order to find the lcss
        if i == 0 or j == 0:
            return []
        if harvesine(u[i - 1], v[j - 1]) <= match_error_margin:
            return bt(t, u, v, match_error_margin, i - 1, j - 1) + [v[j - 1]]
        elif t[i][j - 1] > t[i - 1][j]:
            return bt(t, u, v, match_error_margin, i, j - 1)
        else:
            return bt(t, u, v, match_error_margin, i - 1, j)

    t = np.zeros( (len(u) + 1,len(v) + 1) ) # LCSS computation table

    for i in xrange(1,len(u) + 1):
        for j in xrange(1,len(v) + 1):
            if harvesine(u[i - 1], v[j - 1]) <= match_error_margin:
                t[i][j] = t[i - 1][j - 1] + 1
            else:
                t[i][j] = max( [ t[i][j - 1], t[i - 1][j] ] )
    return bt(t, u, v, match_error_margin, len(u), len(v))
