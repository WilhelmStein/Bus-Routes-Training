import numpy as np
from harversine import harvesine

def lcss(u, v, match_error_margin):

    def bt(t, u, v, match_error_margin, i , j): # Backtrack through matrix t in order to find the lcss
        if i == -1 or j == -1:
            return []
        if harvesine(u[i], v[j]) <= match_error_margin:
            return bt(t, u, v, match_error_margin, i - 1, j - 1) + [u[i]]
        elif t[i][j - 1] > t[i - 1][j]:
            return bt(t, u, v, match_error_margin, i, j - 1)
        else:
            return bt(t, u, v, match_error_margin, i - 1, j)

    t = np.zeros( (len(u),len(v)) ) # LCSS computation table

    for i in xrange(len(u)):
        for j in xrange(len(v)):
            if harvesine(u[i], v[j]) <= match_error_margin:
                t[i][j] = t[i - 1][j - 1] + 1
            else:
                t[i][j] = max( [ t[i][j - 1], t[i - 1][j] ] )
    
    return bt(t, u, v, match_error_margin, len(u) - 1, len(v) - 1)