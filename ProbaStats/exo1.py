#!/usr/bin/python3
import numpy as np
import numpy.random as loi
import scipy.stats as loiT
import matplotlib.pyplot as plt


# TP PROBAS et STATISTIQUES en PYTHON 2
# EXERCICE 1 : comparaison de lois uniformes : theorique & pratique


# Loi uniforme
def loi_unif(nb_val, param1, param2, barres, pas):

    # Loi pratique (valeurs aleatoires)
    xp = loi.uniform(param1, param2, size=nb_val)

    # Normalisation
    mini = param1
    maxi = param2

    # Loi theorique
    vec = np.arange(mini, maxi, pas)
    xt = loiT.uniform.pdf(vec, loc = param1, scale = param2-param1)

    # Affichage
    plt.figure()
    plt.hist(xp, barres, density = True, label='resultat pratique')
    plt.plot(vec, xt, 'r', label='resultat theorique') # A MODIFIER dans le cas discret par 'or'
    plt.title('Loi Uniforme')
    plt.xlabel('Intervalles')
    plt.ylabel('Probabilites')
    plt.legend()
    plt.show()

    return (xp, xt)

# Loi exponentielle
def loi_expo(nb_val, lamda, barres, pas):

    # Loi pratique
    xp = loi.exponential(1/lamda, size = nb_val)

    # Exponentiation
    mini = min(xp)
    maxi = max(xp)

    # Loi theorique
    vec = np.arange(mini, maxi, pas)
    xt = loiT.expon.pdf(vec, loc = 0, scale = 1/lamda)

    # Affichage
    plt.figure()
    plt.hist(xp, barres, density=True, label='resultat pratique')
    plt.plot(vec, xt, 'r', label='resultat theorique') # A MODIFIER dans le cas discret par 'or'
    plt.title('Loi Exponentielle')
    plt.xlabel('Intervalles')
    plt.ylabel('Probabilites')
    plt.legend()
    plt.show()

    return (xp, xt)

# Loi géométrique
def loi_geom(nb_val, p, barres, pas):

    # Loi pratique
    xp = loi.geometric(p, size = nb_val)

    # Geometrisation
    mini = min(xp)
    maxi = max(xp)

    # Loi theorique
    vec = np.arange(mini, maxi, pas)
    xt = loiT.geom.pmf(vec, p, loc = 0)

    # Affichage
    plt.figure()
    plt.hist(xp, barres, density=True, label='resultat pratique')
    plt.plot(vec, xt, 'r', label='resultat theorique') # A MODIFIER dans le cas discret par 'or'
    plt.title('Loi Geometrique')
    plt.xlabel('Intervalles')
    plt.ylabel('Probabilites')
    plt.legend()
    plt.show()

    return (xp, xt)

# Loi de Poisson
def loi_Poisson(nb_val, lamda, barres, pas):

    # Loi pratique
    xp = loi.poisson(lamda, size = nb_val)

    # Normalisation
    mini = min(xp)
    maxi = max(xp)

    # Loi theorique
    vec = np.arange(mini, maxi, pas)
    xt = loiT.poisson.pmf(vec, lamda, 0)

    # Affichage
    plt.figure()
    plt.hist(xp, barres, density=True, label='resultat pratique')
    plt.plot(vec, xt, 'r', label='resultat theorique') # A MODIFIER dans le cas discret par 'or'
    plt.title('Loi de Poisson')
    plt.xlabel('Intervalles')
    plt.ylabel('Probabilites')
    plt.legend()
    plt.show()

    return (xp, xt)

# Loi Normale
def loi_normale(nb_val, param1, param2, barres, pas):

    # Loi pratique
    xp = loi.normal(param1, param2, size = nb_val)

    # Normalisation
    mini = min(xp)
    maxi = max(xp)

    # Loi theorique
    vec = np.arange(mini, maxi, pas)
    xt = loiT.norm.pdf(vec, loc = param1, scale = param2)

    # Affichage
    plt.figure()
    plt.hist(xp, barres, density=True, label='resultat pratique')
    plt.plot(vec, xt, 'r', label='resultat theorique') # A MODIFIER dans le cas discret par 'or'
    plt.title('Loi Normale')
    plt.xlabel('Intervalles')
    plt.ylabel('Probabilites')
    plt.legend()
    plt.show()

    return (xp, xt)


# DEBUT DU PROGRAMME PRINCIPAL

# Constante
nb_barres = 20
pas_reel = 0.02
pas_discret = 1


# EXERCICE 1 : Lois de probabilites
# (a) Tests de la loi Uniforme : loi discrete ou reelle au choix...
# 50 valeurs suivant une loi uniforme (min=0 & max=20)
loi_unif(50, 0, 20, nb_barres, pas_reel)
# 10000 valeurs suivant une loi uniforme (min=0 & max=20)
loi_unif(10000, 0, 20, nb_barres, pas_reel)
# 10000 valeurs suivant une loi uniforme (min=-5 & max=5)
loi_unif(10000, -5, 5, nb_barres, pas_reel)

# (b) Tests de la loi Exponentielle : loi reelle
# 50 valeurs suivant une loi exponentielle : λ = 0.02
loi_expo(50, 0.02, nb_barres, pas_reel)
# 10000 valeurs suivant une loi exponentielle : λ = 0.02
loi_expo(10000, 0.02, nb_barres, pas_reel)
# 10000 valeurs suivant une loi exponentielle : λ = 0.8
loi_expo(10000, 0.8, nb_barres, pas_reel)

# (c) Tests de la loi Geometrique : loi discrete
# 50 valeurs suivant une loi geometrique : p = 0.07
loi_geom(50, 0.07, nb_barres, pas_discret)
# 10000 valeurs suivant une loi geometrique : p = 0.07
loi_geom(10000, 0.07, nb_barres, pas_discret)
# 10000 valeurs suivant une loi geometrique : p = 0.2
loi_geom(10000, 0.2, nb_barres, pas_discret)

# (d) Tests de la loi de Poisson :
# 50 valeurs suivant une loi de Poisson : λ = 5
loi_Poisson(50, 5, nb_barres, pas_discret)
# 10000 valeurs suivant une loi de Poisson : λ = 5
loi_Poisson(10000, 5, nb_barres, pas_discret)
# 10000 valeurs suivant une loi de Poisson : λ = 0.5
loi_Poisson(10000, 0.5, nb_barres, pas_discret)
# 10000 valeurs suivant une loi de Poisson : λ = 50
loi_Poisson(10000, 50, nb_barres, pas_discret)

# (e) Tests de la loi Normale d'éspérance et d'écart-type : loi reelle
# 50 valeurs suivant une loi normale d'espérance 0 et d'écart-type 1
loi_normale(50,0,1,nb_barres,pas_reel)
# 10000 valeurs suivant une loi normale d'espérance 0 et d'écart-type 1
loi_normale(10000,0,1,nb_barres,pas_reel)
# 50 valeurs suivant une loi normale d'espérance 5 et d'écart-type 0.5
loi_normale(10000,5,0.5,nb_barres,pas_reel)
# 50 valeurs suivant une loi normale d'espérance 50 et d'écart-type 500
loi_normale(10000,50,500,nb_barres,pas_reel)

# EXERCICE 2 : Esperance et Variance
# Question 1 : Loi uniforme
print("X1")
(xp1, xt1) = loi_unif(1000, 10, 20, nb_barres, pas_reel)
print("X2")
(xp2, xt2) = loi_unif(10000, 10, 20, nb_barres, pas_reel)
print("X3")
(xp3, xt3) = loi_unif(100000, 10, 20, nb_barres, pas_reel)

# Question 2 : Esperance et variance pratiques des 3 échantillons
print("X1 : Esperance et Variance pratiques")
print(np.mean(xp1))
print(np.var(xp1))
print("X2 : Esperance et Variance pratiques")
print(np.mean(xp2))
print(np.var(xp2))
print("X3 : Esperance et Variance pratiques")
print(np.mean(xp3))
print(np.var(xp3))
print("\n")

# Question 3 : Esperance et variance theorique des 3 échantillons
print("X1 : Esperance et Variance theorique")
print(np.mean(xt1))
print(np.var(xt1))
print("X2 : Esperance et Variance theorique")
print(np.mean(xt2))
print(np.var(xt2))
print("X3 : Esperance et Variance theorique")
print(np.mean(xt3))
print(np.var(xt3))
print("\n")

# Question 4 : Loi normale de parametres μ = 0 et σ = 1
print("X4")
(xp4, xt4) = loi_normale(1000, 0, 1, nb_barres, pas_reel)
print("X5")
(xp5, xt5) = loi_normale(10000, 0, 1, nb_barres, pas_reel)
print("X6")
(xp6, xt6) = loi_normale(100000, 0, 1, nb_barres, pas_reel)

print("X4 : Esperance et Variance pratiques")
print(np.mean(xp4))
print(np.var(xp4))
print("X5 : Esperance et Variance pratiques")
print(np.mean(xp5))
print(np.var(xp5))
print("X6 : Esperance et Variance pratiques")
print(np.mean(xp6))
print(np.var(xp6))
print("\n")

print("X4 : Esperance et Variance theorique")
print(np.mean(xt4))
print(np.var(xt4))
print("X5 : Esperance et Variance theorique")
print(np.mean(xt5))
print(np.var(xt5))
print("X6 : Esperance et Variance theorique")
print(np.mean(xt6))
print(np.var(xt6))
print("\n")

# Loi exponentielle avec lambda = 0.5
print("X7")
(xp7, xt7) = loi_expo(1000, 0.5, nb_barres, pas_reel)
print("X8")
(xp8, xt8) = loi_expo(10000, 0.5, nb_barres, pas_reel)
print("X9")
(xp9, xt9) = loi_expo(100000, 0.5, nb_barres, pas_reel)

print("X7 : Esperance et Variance pratiques")
print(np.mean(xp7))
print(np.var(xp7))
print("X8 : Esperance et Variance pratiques")
print(np.mean(xp8))
print(np.var(xp8))
print("X9 : Esperance et Variance pratiques")
print(np.mean(xp9))
print(np.var(xp9))
print("\n")

print("X7 : Esperance et Variance theorique")
print(np.mean(xt7))
print(np.var(xt9))
print("X8 : Esperance et Variance theorique")
print(np.mean(xt8))
print(np.var(xt9))
print("X9 : Esperance et Variance theorique")
print(np.mean(xt9))
print(np.var(xt9))
print("\n")

# EXERCICE 3 : Matrice de covariance
# Question 1 : Loi normale de taille 1000 et de parametres (0,1)
(Xp, Xt) = loi_normale(1000, 0, 1, nb_barres, pas_reel)
# Question 2 : Loi uniforme de taille 1000 dans l’intervalle [10,20]
(Yp, Yt) = loi_unif(1000, 10, 20, nb_barres, pas_reel)
# Question 3 : Loi uniforme de taille 1000 dans l’intervalle [0,1]
(Zp, Zt) = loi_unif(1000, 0, 1, nb_barres, pas_reel)
# Question 4 : Covariances
print("\nMatrice de covariance de X et Y", np.cov(Xp, Yp))
print("\nMatrice de covariance de X et Z", np.cov(Xp, Zp))
print("\nMatrice de covariance de Y et Z", np.cov(Yp, Zp))

# les valeurs de covariances sont faibles car les lois sont differentes et indépendantes

# EXERCICE 4 : Coefficient de correlation
print("\nCoefficient de correlation de X et X+Y", np.corrcoef(Xp, Xp+Yp))
print("\nCoefficient de correlation de X et X*Y", np.corrcoef(Xp, Xp*Yp))
print("\nCoefficient de correlation de 2*X+Y et 3*X+Y", np.corrcoef(2*Xp+Yp, 3*Xp+Yp))

# Les deux derniers coefficients sont les memes
