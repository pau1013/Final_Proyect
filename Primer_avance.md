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

	
3) Save everything
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
                    
	
