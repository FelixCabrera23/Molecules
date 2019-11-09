#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 23:39:50 2019

@author: Felix Cabrera
USAC - ECFM
Proyecto de Materia Condensada: 
Particulas en un resipiente
Optimizado para python 2
"""

import numpy as np
import random
from datetime import date
from datetime import datetime
from time import time


"Variables importantes a lo largo del programa:"
L = 100.0 # Longitud de la caja
r = L/200.0 # Radio de las particulas 
d = r*2 # Diametro de las particulas
A = L*L # Area del recipiente
xmin = r # Valor minimo de la coordenada x
xmax = L -r # Valor maximo de la coordenada x
ymin = xmin # Valor minimo de la coordenada y
ymax = xmax # Valor maximo de la coordenada y)):,
a0 = np.pi/3.0# Angulo minimo de la red hexagonal
e = 3 #Profundidad del potencial
omax = d*2 # distancia en el cual el potencial es cero
Emax = float(1) # Esta es la energia maxima de la configuracion de la red hexagonal llena
today = date.today()
now = datetime.now()
random.seed(1999)

"Calculo de N"
nc =int(L/d)
nf = int((L)/(d*np.sin(a0)))
N = nc*nf -int(nf/2)

class Particula(object):
    """Esta clase define la particula con sus coordenadas en el plano x y
    Sera necesario llamar al objeto por medio de una variable que tendra 
    las caracteristicas que la definen que son sus coordenadas."""
    
    def __init__(self, x=0, y=0, n=0 , E=0):
        "Esto define las coordenadas x y tambien el numero de particulas que es"
        self.x = x
        self.y = y
        self.n = n
        self.E = E
        
    def __repr__(self):
        "Esto hace que al llamar la variable nos devuelva el nombre del objeto"
        return('Particula{0.n!r}({0.x!r},{0.y!r})'.format(self))   
    
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
        yn = yi + d*np.sin(a0)
    elif xn > xmax+0.01:
        xn = xmin + r
        yn = yi + d*np.sin(a0)
    else:
        xn = xn
        yn = yn
    phn = Particula(xn,yn,n)
    redhex.append(phn)     



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
    return (P)

def Mover_Particula (redor):
    "Esta funcion mueve una particula aleatorea de la red un solo paso"
    redt = redor[:]
    num = int(random.random()*len(redt))
    Pn = Mover(redt[num])
    xs = []
    ys = []
    ocupada = int
    i = int(0)
    s2 = float
    xo = Pn.x
    yo = Pn.y
    s2 = L
    
    for i in range(len(redt)):
        x = redt[i].x
        y = redt[i].y
        xs.append(x)
        ys.append(y)
    
    for i in range(len(redt)):
        if i == num:
            continue
        else:
            s2 = (xo - xs[i])**2 + (yo - ys[i])**2
        
        if s2 < d**2:
            ocupada = 1
            break
        else:
            ocupada = 0
    if ocupada == 1:
        redt[num] = redor[num]
    else:
        redt[num] = Pn
    return(redt)

"Potencial de Lenard Jones"
def Energia_LJ (P_o,P_ext):
    "Esto define la energia entre un par de particulas"
    xo = P_o.x
    yo = P_o.y
    xi = P_ext.x
    yi = P_ext.y
    r2 = (xo - xi)**2 + (yo - yi)**2
    E1 = 4*e*((omax**12/r2**6) - (omax**6/r2**3))
    return(E1)
    
def Energia_red(red):
    "Esto toma una red y calcula la energia total"
    "Tambien le asigna su energia propia a cada particula"
    Et = float
    Efinal = 0.0
    for i in range(len(red)):
        Po = red[i]
        Et = 0.0
        for j in range(len(red)):
            if j == i:
                continue
            else:
                En = Energia_LJ(Po,red[j])
                Et = Et + En
        red[i] = Particula(Po.x,Po.y,i,Et)
    for i in range(len(red)):
        Efinal = Efinal + red[i].E
    Eneta = Efinal/2.0
    return(Eneta)
    
def Quitar (p,red):
	"Esta funcion quita las particulas aleatoreamente, deja una red de p porciento de la original"
	Ni = float
	Ni = (100.0-p)/100.0
	redhexn = red[:]
	for i in range(int(Ni*N)):
		num = int(random.random()*len(redhexn))
		redhexn.pop(num)
	for j in range(len(redhexn)):
		redhexn[j] = Particula(redhexn[j].x,redhexn[j].y,j)
	Energia_red(redhexn)
	return(redhexn)
   
    

"ahora procedemos a optimisar la energia"
def Optim (red,pasos):
    "Esta funcion toma una red, mueve sus particulas y analiza el cambio en la energia."
    redop = red[:]
    Eo = Energia_red(redop)
    i = 0    
    Energias = [1,2,3]
    Cv_count = 0
    
    while i < pasos: 
        redmov = Mover_Particula(redop)
        Emov = Energia_red(redmov)
        Ni = len(red)
        
        if Emov < Eo:
            Eo = Emov
            redop = redmov
            Energias.append(Emov)
            if i % Ni == 0:
                standev = np.std(Energias[-Ni:-1])
                prom = np.average(Energias[-Ni:-1])
                Cv = standev / prom   # Coeficiente de variacion
                if Cv < 0.001:
                    Cv_count+=1
                if Cv_count == 6:
                    print '\n El proceso encontro convergencia despues de '+str(i)+' pasos'
                    break
            i += 1
            if i % (pasos*0.2) == 0 :
                Guardar_archivo(redop,'backup'+str(i))      
        else:
            continue
    return(redop)
    
    
def Guardar_archivo (red,nombre):
    "Esta función guarda la red a un archivo que se generara"
    Ec = Energia_red(red)
    file = open('# %s%.0f.txt' % (nombre,Ec),'w')
    file.write('%f\n' % (Ec))
    for i in range(len(red)):
        x = red[i].x
        y = red[i].y
        file.write('%f %f\n' % (x,y))
    file.close()
    
    return('Su archivo ha sido guardado con exito')

def Montecarlo(h,porcentaje,nombre):
    "Esta función hace uso de todas las erramientas antes desarrolladas"
    print 'Bienvenido '+str(today)+' \n Calculando la energia maxima...'

    tm = time()
    redor = Quitar(porcentaje,redhex)
    Guardar_archivo(redor,nombre + '1st')
    print 'Se esta procesando el '+str(porcentaje)+'% de particulas ('+str(len(redor))+'). \n Numero de pasos maximos:'+str(h)
    redopt = Optim(redor,h)
    fin = datetime.now()
    Guardar_archivo(redopt,nombre +'2nd')
    Dt2 = time() - tm
    print 'Calculado en un tiempo de '+str(Dt2)+'s. \n'
    print fin
    return()

Montecarlo(10000,2,'helga')




    
            
        






    

    

    
    
    
    

    





    
    









