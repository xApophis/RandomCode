import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import expon
# Représentation des lois statistiques
# Question 1 : loi normale théorique N(2, 1) sur [-1, 5]
def question1():
    x = np.arange(-1, 5, 0.001)
    mu = 2
    sigma = 1
    loiNormale = norm.pdf(x, mu, sigma)
    plt.plot(x, loiNormale)
    plt.show

# Question 2 :  la loi normale théorique N(5,3) et la loi exponentielle théorique de paramètre μ = 1 sur [0, 10]
def question2():
    x = np.arange(0, 10, 0.001)
    loiNormale = norm.pdf(x, 5, 2)
    plt.plot(x, loiNormale)
    loiExponentielle = expon.pdf(x)
    plt.plot(x, loiExponentielle)
    plt.show

# Question 3 : afficher l’histogramme d’une distribution aléatoire den = 1000 points d’une loi normale N(5,1)
def question3():
    x = np.random.normal(5, 1, 1000)
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.hist(x)
    x2 = np.arange(0, 10, 0.001)
    loiNormale = norm.pdf(x2, 5, 3)
    plt.subplot(2, 1, 2)
    plt.plot(x2, loiNormale)
    plt.show
#main
question1()
question2()
question3()
