import numpy as np
import numpy.random as loi
from exo1 import loi_unif

def chi2(theorique,pratique,pas):
    return np.sum((theorique-pratique)**2/theorique)

if __name__ == '__main__':
    nb_barres = 20
    pas_reel = 0.02
    pas_discret = 1


    xp = loi_unif(10, 0, 1, nb_barres, pas_reel)
    xt = loi.uniform(0,1, size=10)
    print(chi2(xt,xp,pas_reel))
