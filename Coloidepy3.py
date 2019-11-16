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
import matplotlib
import numpy as np
import random
from datetime import datetime
from time import time
import sys


"Variables importantes a lo largo del programa:"
L = 100.0 # Longitud de la caja
r = L/40.0# Radio de las particulas 
d = r*2 # Diametro de las particulas
A = L*L # Area del recipiente
xmin = r # Valor minimo de la coordenada x
xmax = L -r # Valor maximo de la coordenada x
ymin = xmin # Valor minimo de la coordenada y
ymax = xmax # Valor maximo de la coordenada y)):,
a0 = np.pi/3.0# Angulo minimo de la red hexagonal
e = 1 #Profundidad del potencial
omax = d*2 # distancia en el cual el potencial es cero
inicio = datetime.now()
random.seed(1999)
Emax = float(1)
x = [] # Lista de las coordenadas de la red, ordenadas con los indices de las particulas
y = []
red_t = [] # Esta sera una copia de la red que nos servira para trabajar con ella, sin modificar la original
Ecolormax = float(1)
Efin = float(1)

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


def circulo(x,y):
    "define el circulo en las coordenadas y con su radio apropiado"
    circ = plt.Circle((x,y),r)
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
        c = circulo(self.x,self.y)
        return c
        
    def __repr__(self):
        "Esto hace que al llamar la variable nos devuelva el nombre del objeto"
        return('Particula{0.n!r}({0.x!r},{0.y!r})'.format(self))
    

def Quitar (p,red):
    "Esta funcion quita las particulas aleatoreamente, deja una red de p porciento de la original"
    Ni = (100-p)/100
    global Emax
    global x
    global y
    global red_t
    redhexn = red[:] #Copia de la lizta hexagonal que se va a limpiar
    
    for i in range(int(Ni*N)):
        num = int(random.random()*len(redhexn))
        redhexn.pop(num)
        
    "Es necesario re indexsarlas en la nueva lista"
    "tambien llenamos las listas x y "
    for i in range(len(redhexn)):
        redhexn[i] = Particula(redhexn[i].x,redhexn[i].y,i)
        x.append(redhex[i].x)
        y.append(redhex[i].y)
    
    Emax = Energia_red(redhexn)
    red_t = redhexn[:]
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
    Eneta = Efinal/2
    return(Eneta)    
    
def Energia_Particula(P,red):
    " Esta función toma una sola particula y calcula su energia al entrar ultima al sistema"
    E = float()
    for i in range(len(red)):
        if i == P.n:
            continue
        else:
            Ei =Energia_LJ(P,red[i])
            E = E + Ei
    return(E)
    
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
    if round(xn,2) > round(xmax,2) and round(xn,2) < round(xmax +(0.66*d),2):
        xn = xmin
        yn = yi + d*np.sin(a0)
    elif round(xn,2) > round(xmax + r,2):
        xn = xmin + r
        yn = yi + d*np.sin(a0)
    else:
        xn = xn
        yn = yn
    phn = Particula(xn,yn,n)
    redhex.append(phn)        
    
def Mover_Espc (num):
    "Esta funcion mueve una particula definida de la red un solo paso"
    global red_t
    global x
    global y
    Pn = Mover(red_t[num])

    ocupada = int
    i = int(0)
    s2 = float
    xo = Pn.x
    yo = Pn.y
    s2 = L
    
    for i in range(len(red_t)):
        if i == num:
            continue
        else:
            s2 = (xo - x[i])**2 + (yo - y[i])**2
        
        if s2 < d**2:
            ocupada = 1
            break
        else:
            ocupada = 0
    if ocupada == 1:
        Pfin = red_t[num]
    else:
        Pfin = Pn
        Pfin.E = Energia_Particula(Pn,red_t)
    return(Pfin)
    

"ahora procedemos a optimisar la energia"
def Optim (red,pasos):
    "Esta funcion toma una red, mueve sus particulas y analiza el cambio en la energia."
    random.seed(1991)
    global red_t
    global Emax
    global x
    global y
    global Ac
    global Efin
    x = []
    y = []
    if red != red_t:
        Emax = Energia_red(red)
        red_t = red[:]
    for j in range(len(red_t)):
        x.append(red_t[j].x)
        y.append(red_t[j].y)
    Eo = float()
    if Emax == 1 :
        Eo = Energia_red(red_t)
    else:
        Eo = Emax
    Ac = 0    
    Energias = [1,2,3]
    Cv_count = 0
    i = 0
    saltos = 0
    while i < pasos: 
        "Vamos a mover una particula aleaotrea"
        num = int(random.random()*len(red_t))
        Pmov = Mover_Espc(num)
        
        if Pmov == red_t[num]:
            saltos += 1
            continue
        
        Epo = (red_t[num].E)/2.0
        Epm = (Pmov.E)/2.0
        Emov = Eo - Epo + Epm
        Ni = len(red)
        
        if Emov < Eo:
            Eo = Emov
            red_t[num] = Pmov
            x[num] = Pmov.x
            y[num] = Pmov.y
            Energias.append(Emov)
            if i % Ni == 0:
                standev = np.std(Energias[-Ni:-1])
                prom = np.average(Energias[-Ni:-1])
                Cv = standev / prom   # Coeficiente de variacion
                if abs(Cv) < 0.000001:
                    Cv_count+=1
                if Cv_count == int(Ni/4):
                    print('\n El proceso encontro convergencia despues de ' +str(i) +' pasos')
                    break
            Ac += 1
            i += 1
#            if i % (pasos*0.2) == 0 :
#                Guardar_archivo(red_t,'backup'+str(i))      
        else:
            i += 1
            continue
        progress(i,pasos, status = 'Optimizando:')
    Emax = Eo
    Efin = Eo
    return(red_t)
     
    
def Guardar_archivo (red_s,nombre):
    "Esta función guarda la red a un archivo que se generara"
    Ec = Energia_red(red_s)
    file = open('%s%.0f.txt' % (nombre,Ec),'w')
    for i in range(len(red_s)):
        x = red_s[i].x
        y = red_s[i].y
        file.write('%f %f\n' % (x,y))
    file.close()
    
    "Esta parte guarda la imagen de la red a un archivo.jpeg"
    plt.clf()
    ax = plt.gca()
    for j in range(len(red_s)):
        ax.add_patch(red_s[j].grafica())
    plt.axis([0,L,0,L])
    plt.savefig('%s%.0f.jpeg' %(nombre,Ec),dpi = 200)
    
    return('Su archivo ha sido guardado con exito')

def Montecarlo(h,porcentaje,nombre):
    """Esta funcion utiliza las funciones desarrolladas anteriormente y calcula la posicion optima de
    una red de N particulas con radio r y el porcentaje de estas definido por el usuario
    """
    print(inicio)
    print('Bienvenido: \nCalculando Energia...')
    to = time()
    redor = Quitar(porcentaje,redhex)
    tf = time() - to
    print('Energia inicial: '+str(Emax))
    print('Calculado en un tiempo de: '+str(tf))
    print('Se esta procesando el '+str(porcentaje)+'% de particulas ('+str(len(redor))+') \n')
    Guardar_archivo(redor,nombre + '1st')
    tm = time()
    redopt = Optim(redor,h)
    fin = datetime.now()
    Guardar_archivo(redopt,nombre +'2nd')
    Dt2 = time() -tm
    print('Energia final: '+str(Efin))
    print('Calculado para '+str(len(redor))+' particulas en un tiempo de '+str(Dt2)+'s. \n')
    print('Se han aceptado '+str(Ac)+' pasos, de un total de '+str(h))
    print(fin)
    return()
    
def Recuperar (archivo):
    "Esta función sirve para recuperar un archivo de texto e interpretarlo como una red"
    "Se debe utilizar el nombre en str"
    global Emax
    global red_t
    red_recv = []
    with open(archivo) as arch_rec:
        for line in arch_rec:
            part = line.split(' ')
            x = float(part[0])
            y = float(part[1])
            red_recv.append(Particula(x,y))
        for i in range(len(red_recv)):
            red_recv[i] = Particula(red_recv[i].x,red_recv[i].y,i)
        Emax = Energia_red(red_recv)
    red_t = red_recv[:]
    return(red_recv)


def Montecarlo_2(h,nombre):
    """Esta funcion utiliza las funciones desarrolladas anteriormente y calcula la posicion optima de
    una red de N particulas con radio r y el porcentaje de estas definido por el usuario
    """
    print(inicio)
    print('Bienvenido: \nCalculando Energia...')
    to = time()
    Recuperar('datos.txt')
    redor = red_t[:]
    tf = time() - to
    print('Energia inicial: '+str(Emax))
    print('Calculado en un tiempo de: '+str(tf))
    print('Se esta procesando el archivo con un numero de particulas: ('+str(len(redor))+')')
    Guardar_archivo(redor,nombre + '1st')
    tm = time()
    redopt = Optim(redor,h)
    fin = datetime.now()
    Guardar_archivo(redopt,nombre +'2nd')
    Dt2 = time() -tm
    print('Energia final: '+str(Efin))
    print('Calculado para '+str(len(redor))+' particulas en un tiempo de '+str(Dt2)+'s. \n')
    print('Se han aceptado '+str(Ac)+' pasos, de un total de '+str(h))
    print(fin)
    return()



def Caracterizacion(h,corridas,porcentaje):
    "Esta funcion caracteriza el sistema en una nueva pc"
    print('Bienvenido \n se caracterizara el sistema para '+str(corridas)+ 'de '+str(h)+' pasos cada una.')
    tiempos = [0]
    Energias = []
    Pasos = [0]
    Pasos_ac = [0]
    t1 = time()
    print('calculando energia inicial... ')
    redop = Quitar(porcentaje,redhex)
    t2 = time() - t1
    print('Calculada en un tiempo de: '+str(t2)+'s')
    Energias.append(Emax)
    t3 = time()
    for i in range(corridas):
        redop = Optim(redop,h)
        t4 = time() - t3
        Energias.append(Efin)
        tiempos.append(t4)
        pas = h + i*h
        Pasos.append(pas)
        Pasos_ac.append(Ac)
        Guardar_archivo(redop,'red'+str(porcentaje)+'p'+str(i))
        
    "Grafica de tiempo vs Energia"
    plt.clf()
    fig, ax = plt.subplots()
    ax.plot(tiempos,Energias)
    ax.set(xlabel='tiempo [s]', ylabel = 'Energias',title = 'Tiempo vs Energias')
    ax.grid()
    plt.savefig('%stvsE.jpeg' %(porcentaje),dpi = 200)
    
    "Grafica de tiempo vs pasos "
    plt.clf()
    fig, ax = plt.subplots()
    ax.plot(tiempos,Pasos)
    ax.set(xlabel = 'tiempo [s]' , ylabel = 'Pasos Montecarlo', title = 'Pasos Montecarlo vs tiempo')
    ax.grid()
    plt.savefig('%stvsP.jpeg' %(porcentaje),dpi = 200)
x
    "Grafica de Pasos aceptados vs tiempo"
    plt.clf()
    fig, ax = plt.subplots()
    ax.plot(tiempos,Pasos_ac)
    ax.set(xlabel = 'tiempo [s]' , ylabel = 'Pasos Aceptados', title = 'Pasos aceptados vs tiempo')
    ax.grid()
    plt.savefig('%stvsP_ac.jpeg' %(porcentaje),dpi = 200)
    
    "Grafica de Energia vs Pasos Montecarlo"
    plt.clf()
    fig, ax = plt.subplots()
    ax.plot(Pasos,Energias)
    ax.set(xlabel = 'Pasos Montecarlo', ylabel = 'Energia', title = 'Energia vs Pasos Montecarlo')
    ax.grid()
    plt.savefig('%sEvsP.jpeg' %(porcentaje),dpi = 200)
    
            
        






    

    

    
    
    
    

    





    
    









