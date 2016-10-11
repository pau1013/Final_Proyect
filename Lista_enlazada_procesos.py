import os
import psutil
from time import time
from threading import Thread
from collections import namedtuple

tiempo_inicial=time()
DiskUsage = namedtuple('DiskUsage', 'total  used  free')

class procs: #proc es un objeto de la clase psutil del cual podemos obtener toda la informacion de un proceso
    def __init__(self,proc):
        self.proc=proc
        self.username=proc.username()
        self.pid=proc.pid
        self.cpu=proc.cpu_percent()
        self.mem=proc.memory_percent()
        self.name=proc.name()
        #self.mem_disk=proc.memory_maps()
        self.path=proc.exe()

        self.next = None
        self.prev=None
        self.posicion=None




class Lista:
    def __init__(self):
        self.head=None


    def insertar(self,proc,Posicion): # agregaa un proc a la lista, eventualmente lo necesitaremos para actualizar
        temp=self.head
        cont=0
        nodo=procs(proc)


        if Posicion <= self.length() and Posicion != 0:
            if temp!=None:
                while cont!=Posicion-1:
                    temp=temp.next
                    cont=cont+1
            nodo.next=temp.next
            nodo.posicion=temp.next.posicion-1
            temp.next=nodo

        elif Posicion==0:
            nodo.next=self.head
            nodo.end=None
            self.head=nodo
        if Posicion <= self.length() and nodo.next != None:
            while nodo != None:
                nodo.posicion = nodo.posicion + 1
                nodo = nodo.next



    def Ordenar(self,PID,CPU,MEM): #Ordena la lista de menor a mayor de acuerdo a su pid,cpu,mem recibe boolean ejem(True,False,False)
        if PID==True:
            temp = self.Quicksort_interno_PID(self.Lista_desordenada())
        elif CPU==True:
            temp = self.Quicksort_interno_CPU(self.Lista_desordenada())
        elif MEM==True:
            temp = self.Quicksort_interno_MEM(self.Lista_desordenada())

        self.head=temp[0]
        self.head.prev=None

        nodo_temp=self.head
        i=1
        while i < len(temp):
            nodo_temp.next=temp[i]
            i=i+1
            if i == len(temp)-1:
                temp[i].next=None
            nodo_temp=nodo_temp.next

        count = 0
        nodo_temp=self.head
        while nodo_temp!=None:
            nodo_temp.posicion=count
            nodo_temp=nodo_temp.next
            count=count+1

    def Lista_desordenada(self): #Regresa una lista con todos los procs en su orden actual
        LISTA_DESORDENADA=[]
        temp=self.head
        while temp != None:
            LISTA_DESORDENADA.append(temp)
            temp=temp.next
        return LISTA_DESORDENADA

    def Quicksort_interno_PID(self,list): #Ordena una lista
        if len(list) > 1:
            izquierda = []
            derecha = []

            Pivote = len(list) // 2
            Pivote = list[Pivote]

            for piv in range(len(list)):
                if list.index(Pivote) != piv:
                    if (list[piv]).pid <= Pivote.pid:
                        izquierda.append(list[piv])
                    else:
                        derecha.append(list[piv])

            self.Quicksort_interno_PID(izquierda)
            izquierda.append(Pivote)
            self.Quicksort_interno_PID(derecha)

            i = 0
            j = 0
            k = 0
            while i < len(izquierda) and j < len(derecha):
                if izquierda[i].pid < derecha[j].pid:
                    list[k] = izquierda[i]
                    i = i + 1
                else:
                    list[k] = derecha[j]
                    j = j + 1
                k = k + 1


            while i < len(izquierda):
                list[k] = izquierda[i]
                i = i + 1
                k = k + 1

            while j < len(derecha):
                list[k] = derecha[j]
                j = j + 1
                k = k + 1
        return list

    def Quicksort_interno_CPU(self,list): #Ordena una lista
        if len(list) > 1:
            izquierda = []
            derecha = []

            Pivote = len(list) // 2
            Pivote = list[Pivote]

            for piv in range(len(list)):
                if list.index(Pivote) != piv:
                    if (list[piv]).cpu <= Pivote.cpu:
                        izquierda.append(list[piv])
                    else:
                        derecha.append(list[piv])

            self.Quicksort_interno_PID(izquierda)
            izquierda.append(Pivote)
            self.Quicksort_interno_PID(derecha)

            i = 0
            j = 0
            k = 0
            while i < len(izquierda) and j < len(derecha):
                if izquierda[i].cpu < derecha[j].cpu:
                    list[k] = izquierda[i]
                    i = i + 1
                else:
                    list[k] = derecha[j]
                    j = j + 1
                k = k + 1


            while i < len(izquierda):
                list[k] = izquierda[i]
                i = i + 1
                k = k + 1

            while j < len(derecha):
                list[k] = derecha[j]
                j = j + 1
                k = k + 1
        return list

    def Quicksort_interno_MEM(self,list): #Ordena una lista
        if len(list) > 1:
            izquierda = []
            derecha = []

            Pivote = len(list) // 2
            Pivote = list[Pivote]

            for piv in range(len(list)):
                if list.index(Pivote) != piv:
                    if (list[piv]).mem <= Pivote.mem:
                        izquierda.append(list[piv])
                    else:
                        derecha.append(list[piv])

            self.Quicksort_interno_PID(izquierda)
            izquierda.append(Pivote)
            self.Quicksort_interno_PID(derecha)

            i = 0
            j = 0
            k = 0
            while i < len(izquierda) and j < len(derecha):
                if izquierda[i].mem < derecha[j].mem:
                    list[k] = izquierda[i]
                    i = i + 1
                else:
                    list[k] = derecha[j]
                    j = j + 1
                k = k + 1


            while i < len(izquierda):
                list[k] = izquierda[i]
                i = i + 1
                k = k + 1

            while j < len(derecha):
                list[k] = derecha[j]
                j = j + 1
                k = k + 1
        return list



    def remueve(self,pid): #Remueve un proceso de la lista y luego lo cierra por su pid
        remov = self.busqueda_PID(pid)


        if remov != None:
            if self.head != remov and remov.next.next != None:
                remov.next=remov.next.next
            elif remov == self.head:
                self.head=remov.next
            elif remov.next.next == None:
                remov.next=None
            if remov.next != None:
                while remov!=None:
                    remov.posicion=remov.posicion-1
                    remov=remov.next
            os.kill(pid,9)


    def imprimir(self): #Imprime los cambios, (lo necesitamos cambiar para que funcione en el GUI)
        temp=self.head
        string=""
        if temp!= None:
            while temp is not None:
                string=string + "USER: {0} PID: {1} CPU: {2} MEM: {3} NAME: {4}\n".format(str(temp.username),str(temp.pid),str(temp.cpu),str(temp.mem),str(temp.name))
                temp=temp.next
            print(string)


    def agregar(self,proceso): #agrega un proc a la lista, solo se hace en la creacion
        proc = procs(proceso)
        if self.head == None:
            proc.posicion=0
            self.head = proc
        elif self.head.next==None:
            proc.posicion = 1
            self.head.next=proc
            self.head.next.prev=self.head
        else:
            count=2
            proc_temp=self.head
            while proc_temp.next != None:
                proc_temp=proc_temp.next
                count=count+1
            proc.posicion=count
            proc_temp.next=proc



    def length(self): #largo de la lista
        temp=self.head
        count=0
        if temp !=None:
            while temp!= None:
                count = count + 1
                temp=temp.next
        return count


    def busqueda_PID(self,valor): #Regresa el proc anterior al que se busco, la lista funciona solo con next, era necesario para remover
        temp=self.head
        if temp != None:
            if (temp.pid==valor):
                return temp
            while temp.next != None:
                if (temp.next.pid==valor): #temp.numero
                    return temp
                temp=temp.next
            if (temp.pid==valor):
                return temp
        return None

    def Salvar(self): #Salva los resultados de cada proceso
        cont = 1
        archiv = open('Task_Manager_Stats_%s.txt' % cont, 'a')
        statsinfo = os.stat('Task_Manager_Stats_%s.txt' % cont)
        while statsinfo.st_size/1024 > 500:
            cont = cont +1
            statsinfo = os.stat('Task_Manager_Stats_%s.txt' % cont)
        archi = open('Task_Manager_Stats_%s.txt' % cont, 'a')
        proc_temp=self.head
        while proc_temp!=None:
            archi.write("USER: {0} PID: {1} CPU: {2} MEM: {3} NAME: {4}\n".format
            (str(proc_temp.username),str(proc_temp.pid),str(proc_temp.cpu),str(proc_temp.mem),str(proc_temp.name)))
            proc_temp=proc_temp.next


    def disk_usage(self):
        d_usage = list(psutil.disk_usage('/'))

        total = self(d_usage[0])
        used = self(d_usage[1])
        free = self(d_usage[2])
        percent = self(d_usage[3])

        return total, used, free, percent

def Crear_Lista(): #Regresa una lista con todos los procesos actuales
    List=Lista()
    thread_procesos=[]
    for proc in psutil.process_iter():
        thread=Thread(target=List.agregar,args=(proc,))
        thread.setDaemon(True)
        thread.start()
        thread_procesos.append(thread)

    for thread_proceso in thread_procesos:
        thread_proceso.join()

    return List






Lista=Crear_Lista()



Lista.imprimir()

Lista.Ordenar(True,False,False)

#Lista.remueve(4819)
#Lista.imprimir()

tiempo_final=time()

print tiempo_final-tiempo_inicial
