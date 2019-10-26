#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 23:39:50 2019

@author: Félix Cabrera
USAC - ECFM
Proyecto de Materia Condensada: PITO PITO PITO PITO ME GUSTA EL PITO 
Particulas en un resipiente
"""

import matplotlib.pyplot as plt
import numpy as np
import random

"Variables importantes a lo largo del programa:"
L = 100 # Longitud de la caja
r = L/100 # Radio de las particulas 
d = r*2 # Diametro de las particulas
A = L*L # Area del recipiente
xmin = r # Valor minimo de la coordenada x
xmax = L -r # Valor maximo de la coordenada x
ymin = xmin # Valor minimo de la coordenada y
ymax = xmax # Valor maximo de la coordenada y
a0 = np.pi/3# Angulo minimo de la red hexagonal

"Calculo de N"
nc =int(L/d)
nf = int((L)/(d*np.sin(a0)))
N = nc*nf -int(nf/2)

def circulo(x,y):
    "define el circulo en las coordenadas y con su radio apropiado"
    circ = plt.Circle((x,y),r,fill=False)
    return circ

def Grafica(red):
    "Esta parte plotea"
    ax = plt.gca()
    for i in range(len(red)):
        ax.add_patch(red[i].grafica())
    plt.axis([0,L,0,L])
    plt.show()

def xy(r,phi): 
    "Esta funcion regresa las coordenadas de polares a cartesianas"
    return r*np.cos(phi), r*np.sin(phi)
    #Fuente: https://www.iteramos.com/pregunta/83886/trazar-un-circulo-con-pyplot

class Particula(object):
    """Esta clase define la particula con sus coordenadas en el plano x y
    Sera necesario llamar al objeto por medio de una variable que tendra 
    las caracteristicas que la definen que son sus coordenadas."""
    
    def __init__(self, x=0, y=0, n=0):
        "Esto define las coordenadas x y tambien el numero de particulas que es"
        self.x = x
        self.y = y
        self.n = n

    def grafica(self):
        "Esto le da a cada particula su grafica"
        # Para llamarla usar Particula.grafica()
        c = circulo(self.x,self.y)
        return c
        
    def __repr__(self):
        "Esto hace que al llamar la variable nos devuelva el nombre del objeto"
        return 'Particula{0.n!r}({0.x!r},{0.y!r})'.format(self)
    
    # Hace falta delimitar que los valores x y solo sean numericos pero que weba
    
# Ya comprobe que puedo guardar las particulas en una lista
# Ya comprobe que puedo sacar valores de x y de las listas
# Al llenar la lista entonces tenemos las particulas ya indexadas con el orden de la lista    
" Esto es la red hexagonal"
ph0 = Particula(xmin,ymin,0) # Primer particula de la red hexagonal
redhex = [ph0] # Lista de las particulas en la red hexagonal

for i in range(N-1):
    "Esta parte leera las coordenadas de la particula anterior"
    xi = redhex[i].x
    yi = redhex[i].y
    xn = xi + d
    yn = yi
    n = i +1
    if int(xn) == int(xmax+r):
        xn = xmin
        yn = yi + d*np.sin(np.pi/3)
    elif xn > xmax+0.01:
        xn = xmin + r
        yn = yi + d*np.sin(np.pi/3)
    else:
        xn = xn
        yn = yn
    phn = Particula(xn,yn,n)
    redhex.append(phn)
    

def Quitar (p,red):
    "Esta funcion quita las particulas aleatoreamente, deja una red de p porciento de la original"
    Ni = (100-p)/100
    redhexn = red[:] #Copia de la lizta hexagonal que se va a limpiar
    
    for i in range(int(Ni*N)):
        num = int(random.random()*len(redhexn))
        redhexn.pop(num)
        
    "Es necesario re indexsarlas en la nueva lista"
    for i in range(len(redhexn)):
        redhexn[i] = Particula(redhexn[i].x,redhexn[i].y,i)
        
    return redhexn


def Mover (P):
    "Esta parte mueve una particula aleatoreamente sin que se salga de los limites"
    ang = random.random()*2*np.pi
    rn = random.random()*r
    xn = P.x + rn*np.cos(ang)
    yn = P.y + rn*np.sin(ang)
    
    if xn <= xmax and xn >= xmin and yn <= ymax and yn >= ymin:
        P = Particula(xn,yn,P.n)
    else:
        P = P
    return P

def Mover_red (red,pasos):
    redn = red[:] # Copia la red de entrada
    xs = []
    ys = []
    ocupada = int
    k = int
    
    for i in range(len(red)):
        x = redn[i].x
        y = redn[i].y
        xs.append(x)
        ys.append(y)
    for i in range(pasos):
        for j in range(len(red)):
            Pn = Mover(redn[j])
            hmax = Pn.x + d
            hmin = Pn.x - d
            vmax = Pn.y + d
            vmin = Pn.y - d
            k = 0
            for k in range(len(red)):
                if k == j:
                    continue
                if xs[k] > hmin and xs[k] < hmax and ys[k] > vmin and ys[k] < vmax:
                    ocupada = 1
                    break
                else:
                    ocupada = 0
            if ocupada == 1 :
                continue
            else:
                redn[j] = Pn
                xs[j] = Pn.x
                ys[j] = Pn.y    
        
        Grafica(redn)
    return(redn)

            
        






    

    

    
    
    
    

    





    
    









