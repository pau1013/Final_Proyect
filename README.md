1)Conseguir procesos y sort (CPU, Memory)
	Para conseguir los procesos y la informacion contenida se instala 
libreria psutil con el comando en terminal

	"sudo pip install psutil"

	Esta libreria permite obtener objetos llamados "procesos" a los cuales
le puedes pedir su informacion.
Ejem:
	import psutil
	lista=[]
	for procs in psutil.process_iter()
		lista.append(procs)
		print procs.name()
		print procs.pid
		print procs.memory_percent()
		print procs.cpu_percent()

	Para poder hacer sort a esta lista se puede llamar las funciones de
psutil incluso dentro de la lista. Ejem lista[1].memory_percent()
lo cual nos deja comparar las diversas posiciones y utilizar un metodo de sort
como burbuja,merge,quicksort para acomodar.

2) Kill Process
	Para matar un proceso se puede utilizar el modulo os llamandolo como:
		
		os.kill(pid,sig)

	Es necesario mandar una senal predeterminada para que este lo ejecute, matando asi el proceso(pid) que desees eliminar. 
En el caso de este programa se utilizo como senal = 9. 

3) Create Process
	Para crear un proceso se utilizo el modulo de subprocess, en este caso se utiliza subproces.Popen.
Se pretende leer el README de este proyecto, es decir, a traves de este programa obtendremos el "path" en donde
se encuentra el archivo y por medio de subprocess lo mandaremos llamar. 

Ejemplo: 

	import subprocess
	import os

	p = 'README.md'
	o= os.path.abspath(p) #Aqui se obtiene la direccion donde esta guardado el archivo
	a = subprocess.Popen(o)	
	
4) Save everything
	Para salvar los resultados actuales se puede crear un archivo de 
texto y agregar los resultados de los procesos cada cierto tiempo. Con las 
funciones de python normales es posible crear el archivo.
 Codigo de ejemplo:

	import psutil
	import time
	 lista=[]
	count=0
	while 1
		archivo=open('Task manager stats '+str(count),'w')
	        for procs in psutil.process_iter():
			archivo.write(archi.write
			("USER: {0} PID: {1} CPU: {2} MEM: {3} NAME:
			 {4}\n".format (str(procs.username())
			,str(procs.pid),str(procs.cpu_percent()),
			str(procs.memory_percent()),str(procs.name())))
		count=count+1
		time.sleep(300)
5)Map Disk 
	Para obtener los porcentajes se puede utilizar la libreria os o por medio de la psutil la cual tiene un modulo para obtener el path de cada proceso y sacar cuando espacio tiene en memoria,
un par de ejemplos de codigo para esta funcion podrian ser:
		import os
from collections import namedtuple


DiskUsage = namedtuple('DiskUsage', 'total  used  free')

def disk_usage(path):
    size = os.statvfs(path)
    free = (size.f_bavail * size.f_frsize) / 1024
    total = (size.f_blocks * size.f_frsize) / 1024
    used = (total - free)
    return DiskUsage(total, used, free)


print disk_usage('./')

O dentro de la lista enlazada de procs: 
    def disk_usage(self):
        d_usage = list(psutil.disk_usage('/'))

        total = self(d_usage[0])
        used = self(d_usage[1])
        free = self(d_usage[2])
        percent = self(d_usage[3])

        return total, used, free, percent

                    
6) Research Charts Libs	
	La libreria para generación de gráficos que vamos a usar es la de "matplotlib". Hay dos formas de instalarla en ubuntu: la primera es con el comando: python get-pip.py, con este comando también se instalan las setuptools necesarias si es que no están instaladas. 
	La segunda y más segura es con dos comandos: 
	sudo apt-get build-dep python-matplotlib (Este instala todas las dependenencias necesarias)
	sudo apt-get install python-matplotlib
	
	Código de ejemplo: 
		import matplotlib.pyplot as plt
		
		x = [1,2,3]
		y = [5,7,4]
		
		plt.plot(y,x)
		plt.xlabel('Numero')
		plt.ylabel('Variable importante´)
		plt.title('Procesos')
		
		plt.show()
	
