#!/usr/bin/python3
import numpy as np
import numpy.random as loi
import matplotlib.pyplot as plt

def Ligne_Regression(start, stop, taille):
    X = loi.uniform(0, 9, size = taille)
    Y = loi.uniform(0, 9, size = taille)
    mX = np.mean(X)
    mY = np.mean(Y)
    varX = np.var(X)
    covXY = np.cov(X,Y)
    x = np.arange(np.floor(min(X)), np.ceil(max(X)+1))
    y = ((covXY[0][1])/varX)*(x-mX)+mY
    
    plt.plot(X, Y, 'xk', label = 'X par Y')
    plt.plot(y, 'r')
    plt.show()
    


if __name__ == "__main__":
    # EXERCICE 5 : Ligne de regression
    Ligne_Regression(0, 9, 10)
    Ligne_Regression(0, 9, 100)
    Ligne_Regression(0, 9, 1000)
