#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 23:39:50 2019

@author: Félix Cabrera
USAC - ECFM
Proyecto de Materia Condensada: 
Particulas en un recipiente

Este programa consta de varias partes que funciónan por separado y puede ser
modificado facilmente para lograr analizar distintas configuraciónes de particulas
asi como utilizando los potenciales de Lenard Jones como el potencial de London.

El programa funcióna a partir de una lista de objetos llamados Particulas. Estas tienen propiedades, 
tienen un indice, que indica su posición dentro de una lista, este es unico para cada particula
guardan su posición en el plano xy tambien guardan su "energia", esta es la energia para añadir esta
particula al sistema en ultimo lugar. 

Este programa presenta los datos de forma grafica y tambien los almacena en documentos de texto plano.
El programa empieza llenando una lista con las particulas necesarias para llenar el espacio
determinado por las constantes que aparecen en la primera seccion de codigo. Modificando
estas variables puede cambiar el tamaño del recipiente, y de las particulas, por lo tanto 
tambien modificara el numero de particulas maximas en el recipiente.

NOTA: debido a limitaciones de software el programa no puede lidear con tamaños muy pequeños
para las dimensiones tanto de la caja como de las particulas, por lo tanto se utilizan a escala. 
En la presente configuración la escala es 1 = 1 x 10 ^-6 metros.

La red con el llenado maximo se denomina redhex

INSTRUCCIÓNES:
    GENERAR PORCENTAJES INICIALES:
    Para Generar una configuración de particulas aleatoreas, (un porcentaje de llenado) 
    debe crear una lista donde se puedan almacenar. Luego utilice la función Quitar(p,red), donde 
    p es el porcentaje de llenado y red es la red de donde desea partir.
    Ejemplo:
        red20 = Quitar(20,redhex)
        
        red20 = [Particula0(2.5,0.5), Particula1(3.5,0.5), Particula2(8.5,0.5), Particula3(16.5,0.5),...
      
        Esto le dara una red, almacenada en la lista red20 que tiene el 20 porciento de llenado. 
        Se utiliza la redhex como madre ya que esta red presenta un llenado de 100.
    
    El segundo paso para trabajar con una configuración inicial sera guardarla. Para eso haremos uso
    de la función Guardar_archivo(red,nombre). Esta función guardara una grafica de la red y
    tambien generará un archivo de texto plano con las posiciones de las particulas en el plano xy
    Ejemplo:
        Guardar(red20,'ejemplo')
        
        Esto generara un archivo de texto con las posiciones y una grafica donde se podran observar la 
        configuración del sistema en el espacio.
        
    RECUPERAR Y ABRIR ARCHIVOS DE CONFIGURACIONES:
    Para trabajar con configuraciones guardadas previamente o con configuraciones de otras fuentes 
    haremos uso de la función Recuperar(archivo). De nuevo, como en el caso de la función quitar,
    esta regresa una lista de las particulas en las posiciones que se encuentren detalladas en el archivo
    de texto. Para recuperar un archivo debe introducir el nombre exacto del archivo de origen, incluyendo
    su extencion, es necesario introducirlo dentro de comillas.
    Ejemplo:
        
        red_recuperarda = Recuperar('ejemplo.txt')
        red_recuperada = [Particula0(2.5,0.5), Particula1(3.5,0.5), Particula2(8.5,0.5),...
    
    
    REALIZAR SIMULACIÓNES DE TIPO MONTECARLO
    
    IMPORTANTE:
        PARA QUE EL CODIGO CALCULE EL POTENCIAL DE LONDON DEBE ASIGNARSE MANUALMENTE 
        EL VALOR 1 A LA VARIABLE "POTENCIAL", EL VALOR CERO SE UTILIZA PARA EL 
        POTENCIAL DE L-J. Para cambiar entre el potencial de London atractivo y repulsivo 
        basta con cambiar de signo a la constante A (linea 129).
    
    Montecarlo_1():
    Existen tres tipos fundamentales de simulaicónes montecarlo que puede realizar este programa,
    su uso dependera de las necesidades del usuario. La forma más simple para realizar un metodo de
    montecarlo sera por medio de la función Montecarlo_1(pasos,porcentaje,'nombre')
    Esta funcion empieza generando una configuracion inicial para el porcentaje que se ingrese "porcentaje"
    como entrada. A partir de esta configuración inical realizara la cantidad n de "pasos" indicada,
    debera ingresarse un nombre particular, entre comillas 'nombre' para que el programa 
    pueda guardar los archivos necesarios del proceso. Al finalizar se generaran graficas de la
    configuracion inicial y de la configuracion final y se guardarn en archivos de texto. otros
    datos importantes, como el tiempo y la cantidad de pasos aceptados se desplegaran 
    en pantalla.
    
    Montecarlo_2():
    El segundo tipo de simulacion montecarlo empieza apartir de un archivo de texto plano con una
    configuración inicial. Este puede ser simplemente una configuracion inicial o puede sera a partir
    de una configuracion final que ya este procesada.
    La funcion se debe escribir de la siguiente forma: Montecarlo_2(pasos,'nombre')
    Entonces el programa buscara en la carpeta donde se encuentre al archivo 'nombre', por lo que debe
    de incluir la extención. Sobre esta configuración inical realizara una opitmización de N pasos,
    segun determine el usuario.
    
    Montecarlo_3():
    El tercer tipo de simulación de montecarlo, es la más compleja, Esta funciona realizando corridas
    de un numero fijo de pasos cada una. Al finalizar Guarda graficas y archivos de texto donde se observa
    el analizis de los tiempos, la energia y la aceptación de pasos. Este es el metodo más recomendable
    pára utilizar. Dentro del codigo tambien se encuentra un criterio de convergencia, por lo que se puede
    proponer realizar un numero grande de corridas y si el sistema termaliza se detendra el proceso
    automaticamente. Ejemplo:
        Montecarlo_3(pasos, corridas, porcentaje)
        
    Al igual que el primer metodo este generara su propia configuración inicial, sobre el cual realizara
    las corridas, cada una de la cantidad de pasos indicados.
    

"""

import matplotlib.pyplot as plt
import numpy as np
import random
from datetime import datetime
from time import time
import sys

"Variable de desición de potencial, seleccióne 0 para L-J o 1 para London"

Potencial = int(1)

"Dimensiones de la caja y de las particulas"
L = 20 # Longitud de la caja
r = 0.5# Radio de las particulas 
d = r*2 # Diametro de las particulas

"Constantes de los potenciales"
e = 1 #Profundidad del potencial
omax = d*2 # distancia en el cual el potencial es cero
A = r*1.5 # Constante de London

"Variables importantes a lo largo del programa:"
xmin = r # Valor minimo de la coordenada x
xmax = L -r # Valor maximo de la coordenada x
ymin = xmin # Valor minimo de la coordenada y
ymax = xmax # Valor maximo de la coordenada y)):,
a0 = np.pi/3.0# Angulo minimo de la red hexagonal
inicio = datetime.now() #Fecha actual
random.seed(1999) # Semilla primordial del sistema, determina entre otras cosas el vaciado de la red hexagonal
Emax = float(1) # variable para almacenar el valor de la energia del sistema
x = [] # Lista ordenada de las coordenadas de la red, ordenadas con los indices de las particulas
y = [] # Lista ordenada de las coordenadas de la red.
red_t = [] # Esta sera una copia de la red que nos servira para trabajar con ella, sin modificar la original
Efin = float(1) #Variable para almacenar valores temporales de energia.

"Calculo de N, para calcular el numero maximo de particulas"
nc =int(L/d)
nf = int((L-r)/(d*np.sin(a0)))
N = nc*nf -int(nf/2)

def progress(count, total, status=''):
    " Barra de progreso, ayuda a determinar el porcentaje del proceso"
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
    ax.set(ylabel = 'L x10^-6 [m]',title = 'Coloide')
    plt.tight_layout()
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
    
"Potencial de London"
def Energia_London(P_o,P_ext):
    "Este es el potencial de London para un par de particulas"
    xo = P_o.x
    yo = P_o.y
    xi = P_ext.x
    yi = P_ext.y
    rl = np.sqrt((xo - xi)**2 + (yo - yi)**2)
    E2 = A/rl
    return(E2)
    
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
                if Potencial == 0:
                    En = Energia_LJ(Po,red[j])
                else:
                    En = Energia_London(Po,red[j])
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
            if Potencial == 0:
                Ei = Energia_LJ(P,red[i])
            else:
                Ei = Energia_London(P,red[i])
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
    i = 0

    while i < pasos: 
        "Vamos a mover una particula aleaotrea"
        num = int(random.random()*len(red_t))
        Pmov = Mover_Espc(num)
        
        if Pmov == red_t[num]:
            continue
        
        Epo = (red_t[num].E)/2.0
        Epm = (Pmov.E)/2.0
        Emov = Eo - Epo + Epm
        
        if Emov < Eo:
            Eo = Emov
            red_t[num] = Pmov
            x[num] = Pmov.x
            y[num] = Pmov.y
            Ac += 1
            i += 1
            continue

        else:
            i += 1
            Lamda = random.random()*(1/3)
            Ca = (Ac/i)
            if Lamda > Ca:
                Eo = Emov
                red_t[num] = Pmov
                x[num] = Pmov.x
                y[num] = Pmov.y
                continue
            else:
                continue

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
    ax.set(ylabel = 'L x10^-6 [m]',title = 'Coloide '+str(nombre))
    plt.tight_layout()
    plt.savefig('%s%.0f.jpeg' %(nombre,Ec),dpi = 200)
    
    return('Su archivo ha sido guardado con exito')

def Montecarlo_1(h,porcentaje,nombre):
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
    Recuperar(nombre)
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



def Montecarlo_3(h,corridas,porcentaje):
    """Esta función realiza una aproximación por el metodo de montecarlo
    En varias etapas. Al finalizar guardara automaticamente las graficas de la energia y los
    tiempos. Guardara los archivos con los datos utilizados para generar estas graficas en un 
    documento .txt llamado caracterización.
    """
    print('Bienvenido \n Se realizaran '+str(corridas)+ ' corridas, de '+str(h)+' pasos cada una. \n Sobre una configuración de '+str(porcentaje)+' porciento de particulas')
    tiempos = [0]
    Energias = []
    Pasos = [0]
    Pasos_ac = [0]
    t1 = time()
    print('Calculando energia inicial... ')
    redop = Quitar(porcentaje,redhex)
    Guardar_archivo(redop,str(porcentaje)+' porciento, configuración inicial')
    t2 = time() - t1
    print('Calculada en un tiempo de: '+str(t2)+'s')
    Energias.append(Emax)
    t3 = time()
    Cv_count = 0
    i = 0
    while i < corridas:

        redop = Optim(redop,h)
        t4 = time() - t3
        Energias.append(Efin)
        tiempos.append(t4)
        pas = h + i*h
        Pasos.append(pas)
        Pasos_ac.append(Ac)
        i +=1
        if i % int(corridas*0.1) == 0:
            Guardar_archivo(redop,str(porcentaje)+' porciento_'+str(i))
            print('\n')
        Ni = int(corridas/4)
        if i % Ni == 0:
            standev = np.std(Energias[-Ni:-1])
            prom = np.average(Energias[-Ni:-1])
            Cv = standev / prom   # Coeficiente de variacion
            if abs(Cv) < 0.001:
                Cv_count+=1
            if Cv_count == 3:
                print('\n El proceso encontro convergencia despues de ' +str(i) +' corridas')
                break
        else:
            continue
        progress(i,corridas, status = 'Optimizando:')
        
    "Grafica de tiempo vs Energia"
    plt.clf()
    fig, ax = plt.subplots()
    ax.plot(tiempos,Energias)
    ax.set(xlabel='tiempo [s]', ylabel = 'Energia x 10^-6 [J]',title = 'Tiempo vs Energias')
    ax.grid()
    plt.tight_layout()
    plt.savefig('%stvsE.jpeg' %(porcentaje),dpi = 200)
    
    "Grafica de tiempo vs pasos "
    plt.clf()
    fig, ax = plt.subplots()
    ax.plot(tiempos,Pasos)
    ax.set(xlabel = 'tiempo [s]' , ylabel = 'Pasos Montecarlo', title = 'Pasos Montecarlo vs tiempo')
    ax.grid()
    plt.tight_layout()
    plt.savefig('%stvsP.jpeg' %(porcentaje),dpi = 200)

    "Grafica de Pasos aceptados vs tiempo"
    plt.clf()
    fig, ax = plt.subplots()
    ax.plot(tiempos,Pasos_ac)
    ax.set(xlabel = 'tiempo [s]' , ylabel = 'Pasos Aceptados', title = 'Pasos aceptados vs tiempo')
    ax.grid()
    plt.tight_layout()
    plt.savefig('%stvsP_ac.jpeg' %(porcentaje),dpi = 200)
    
    "Grafica de Energia vs Pasos Montecarlo"
    plt.clf()
    fig, ax = plt.subplots()
    ax.plot(Pasos,Energias)
    ax.set(xlabel = 'Pasos Montecarlo', ylabel = 'Energia x 10^-6 [J]', title = 'Energia vs Pasos Montecarlo')
    ax.grid()
    plt.tight_layout()
    plt.savefig('%sEvsP.jpeg' %(porcentaje),dpi = 200)
    
    file2 = open('caracterizacion.txt','w')
    file2.write('tiempo Energia Pasos_aceptados Pasos_montecarlo\n')
    for i in range(len(tiempos)):
        t = tiempos[i]
        E = Energias[i]
        Pa = Pasos_ac[i]
        Pm = Pasos[i]
        file2.write('%f %f %i %i\n' % (t,E,Pa,Pm))
    file2.close()
    return()
    
"Ejemplos"
"Recomendación personal: usen la función Montecarlo_3"
"Este calcula 10 millones de pasos para 20 porciento, para el potencial L-J"
#Potencial = 0
#Montecarlo_3(50000,200,20)

"Este calcula 5 millones de pasos para 30 porciento, para el potencial de London"
#Potencial = 1
#Montecarlo_3(50000,100,30)

"Este genera una red llena al 50 porciento y lo guarda en un archivo de texto"
#red50 = Quitar(50,redhex)
#Guardar_archivo(red50,'red al 50 porciento')




