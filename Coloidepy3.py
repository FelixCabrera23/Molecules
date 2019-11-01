#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 23:39:50 2019

@author: Félix Cabrera
USAC - ECFM
Proyecto de Materia Condensada: 
Particulas en un resipiente
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import random
import sys
from datetime import datetime
from time import time


"Variables importantes a lo largo del programa:"
L = 200 # Longitud de la caja
r = L/20# Radio de las particulas 
d = r*2 # Diametro de las particulas
A = L*L # Area del recipiente
xmin = r # Valor minimo de la coordenada x
xmax = L -r # Valor maximo de la coordenada x
ymin = xmin # Valor minimo de la coordenada y
ymax = xmax # Valor maximo de la coordenada y)):,
a0 = np.pi/3# Angulo minimo de la red hexagonal
e = 100 #Profundidad del potencial
omax = d*2.5 # distancia en el cual el potencial es cero
Emax = float(1) # Esta es la energia maxima de la configuracion de la red hexagonal llena
inicio = datetime.now()

"Calculo de N"
nc =int(L/d)
nf = int((L)/(d*np.sin(a0)))
N = nc*nf -int(nf/2)

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '#' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.flush()
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

def color(E):
    Eni = abs(E/(Emax*1.5))
    c1 = 'blue'
    c2 = 'red'
    c1 = np.array(mpl.colors.to_rgb(c1))
    c2 = np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-Eni)*c1 + Eni*c2)

def circulo(x,y,c):
    "define el circulo en las coordenadas y con su radio apropiado"
    cn = color(c)
    circ = plt.Circle((x,y),r,color = cn)
    return circ

def Grafica(red):
    "Esta parte plotea"
    ax = plt.gca()
    for i in range(len(red)):
        ax.add_patch(red[i].grafica())
    plt.axis([0,L,0,L])
    plt.show()

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

    def grafica(self):
        "Esto le da a cada particula su grafica"
        # Para llamarla usar Particula.grafica()
        c = circulo(self.x,self.y, self.E)
        return c
        
    def __repr__(self):
        "Esto hace que al llamar la variable nos devuelva el nombre del objeto"
        return('Particula{0.n!r}({0.x!r},{0.y!r})'.format(self))
    

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
    
    Energia_red(redhexn)
    
    return(redhexn)


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
    return(P)

def Mover_red (red,pasos):
    "Esta parte mueve toda la red una cantidad de pasos respetando las particulas entre ellas"
    redn = red[:] # Copia la red de entrada
    xs = []
    ys = []
    ocupada = int
    k = int
    s2 = float
    
    for i in range(len(red)):
        x = redn[i].x
        y = redn[i].y
        xs.append(x)
        ys.append(y)
    for i in range(pasos):
        for j in range(len(red)):
            Pn = Mover(redn[j])
            xo = Pn.x
            yo = Pn.y
            k = 0
            s2 = L
            for k in range(len(red)):
                if k == j:
                    continue
                else:
                    s2 = (xo - xs[k])**2 + (yo - ys[k])**2
                    
                if s2 < d**2:
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
        
#        Grafica(redn)
    return(redn)

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
        Et = 0
        for j in range(len(red)):
            if j == i:
                continue
            else:
                En = Energia_LJ(Po,red[j])
                Et = Et + En
        red[i] = Particula(Po.x,Po.y,i,Et)
        
    for i in range(len(red)):
        Efinal = Efinal + red[i].E
    Eneta = Efinal/len(red)


    return(Eneta)    
    
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

  


"ahora procedemos a optimisar la energia"
def Optim (red,pasos,mov):
    "Esta funcion toma una red, mueve sus particulas y analiza el cambio en la energia."
    redop = red[:]
    Eo = Energia_red(redop)
    i = 0    
    while i < pasos: 
        redmov = Mover_red(redop,mov)
        Emov = Energia_red(redmov)
        
        if Emov < Eo:
            if abs(Emov - Eo) < 0.0001:
                print('El proceso encontro convergencia despues de '+str(i)+' pasos')
                print('\n')
                break
            Eo = Emov
            redop = redmov
            i += 1
#            Grafica(redop)
#            print(Eo)
            if i % == 0 :
                Guardar_archivo(redop,'backup'+str(i))
           
        else:
            continue
        progress(i,pasos, status = 'Optimizando:')
    print('\n')
    return(redop)
     
    
def Guardar_archivo (red,nombre):
    "Esta función guarda la red a un archivo que se generara"
    Ec = Energia_red(red)
    file = open('%s%.0f.txt' % (nombre,Ec),'w')
    for i in range(len(red)):
        n = redhex[i].n
        x = redhex[i].x
        y = redhex[i].y
        E = redhex[i].E
        file.write('%i, %f, %f, %f \n' % (n,x,y,E))
    file.close()
    
    "Esta parte guarda la imagen de la red a un archivo.jpeg"
    plt.clf()
    ax = plt.gca()
    for j in range(len(red)):
        ax.add_patch(red[j].grafica())
    plt.axis([0,L,0,L])
    plt.savefig('%s%.0f.jpeg' %(nombre,Ec))
    
    return('Su archivo ha sido guardado con exito')

def Montecarlo(h,porcentaje,nombre):
    """Esta funcion utiliza las funciones desarrolladas anteriormente y calcula la posicion optima de
    una red de N particulas con radio r y el porcentaje de estas definido por el usuario
    """
    tm = time()
    print('Se esta procesando el '+str(porcentaje)+'% de particulas')
    print('\n')
    redor = Quitar(porcentaje,redhex)
    Guardar_archivo(redor,nombre + '1st')
    redopt = Optim(redor,h,1)
    fin = datetime.now()
    Guardar_archivo(redopt,nombre +'2nd')
    Dt2 = time() -tm
    print('Calculado para '+str(len(redor))+' particulas en un tiempo de '+str(Dt2)+'s. \n')
    print(fin)
    return()
    
def Recuperar (archivo):
    "Esta función sirve para recuperar un archivo de texto e interpretarlo como una red"
    "Se debe utilizar el nombre en str"
    with open(archivo) as arch_rec:
        content =arch_rec.read()
    
    return(content)
    
print('Bienvenido: \nCalculando Energia maxima...')
print(inicio)
to = time()
Emax = Energia_red(redhex) # Este calculo es necesario para realizar las optimizacione
Guardar_archivo(redhex,'redoriginal')
print('\n calculado para '+str(len(redhex))+' particulas de radio ='+str(r))
Dt1 = time() -to
print('en un tiempo de '+str(Dt1)+'s.\n')
#Grafica(redhex)
print('Calculando la configuacion optima')

Montecarlo(30,20,'prueba_py3')









    
            
        






    

    

    
    
    
    

    





    
    









