import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import random as rd


with open ("nom_villes.txt", "r") as f: # ouverture du fichier en mode lecture
    l = f.readlines ()             # lecture de toutes les lignes, placées dans une liste

# contiendra la liste des lignes nettoyées
l_net = [ s.strip ("\n\r") for s in l ]

nb_villes = 35313
taille = 28
sensi_fin = 800

liste_caractère = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','\'','-']

T1 = np.zeros((1,46))
P1 = np.zeros((1,taille))
P2 = np.zeros((taille,taille))
D2 = np.zeros((taille,taille))
M1 = np.zeros((taille,taille,taille))

#fonction


def lettre_a_indice(lettre):
    i = 0
    while i < taille and liste_caractère[i] != lettre:
        i += 1

    if i == taille:
        i = 14
    return i

def normalisation(ligne,t):
    S = 0
    for i in range(t):
        S += ligne[i]
    for j in range(t):
        if S == 0:
            ligne[j] = 0
        else:
            ligne[j] = 100*ligne[j]/S

def randomiseur():
    return rd.randint(0,100000)/1000

def choisir_prochain(ligne,rand):
    S = 0
    i = 0
    while S < rand:
        S += ligne[i]
        i += 1
    return i - 1

def fin(n,indice1,indice2):
    if n == 46 :
        return True
    #print(T1[0][n]*D2[indice1][indice2])
    return T1[0][n]*D2[indice1][indice2] > rd.randint(0,sensi_fin)



def creer_nom():
    indice1 = choisir_prochain(P1[0],randomiseur())
    nom = liste_caractère[indice1]

    indice2 = choisir_prochain(P2[indice1],randomiseur())
    nom += liste_caractère[indice2]

    i = 2
    while fin(i,indice1,indice2) == False:
        indice3 = choisir_prochain(M1[indice1][indice2],randomiseur())
        nom += liste_caractère[indice3]
        indice1,indice2 = indice2,indice3
        i += 1
    return nom


def montrer_matrice(A):
    plt.figure()
    plt.imshow(A)
    plt.colorbar()
    plt.grid(False)
    plt.show()


#main

for s in l_net:
    compte = 0
    n = len(s)
    T1[0][n] += 1

    i = lettre_a_indice(s[0])
    j = lettre_a_indice(s[1])
    P1[0][i] += 1
    P2[i][j] += 1

    for a in range(2,n):
        k = lettre_a_indice(s[a])
        if s[a] == '-':
            compte += 1
        M1[i][j][k] += 1
        i,j = j,k
    D2[i][j] += 1

normalisation(T1[0],46)
for i in range(1,46):
    T1[0][i] = T1[0][i]+T1[0][i-1]


normalisation(P1[0],taille)

for ligne in P2:
    normalisation(ligne,taille)

D2 = (100/nb_villes)*D2

for b in range(taille):
    for ligne in M1[b]:
        normalisation(ligne,taille)


