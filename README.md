SIMULACIÓN DE UN COLOIDE UTILIZANDO EL METODO DE MONTECARLO

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
