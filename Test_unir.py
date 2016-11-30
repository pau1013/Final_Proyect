import sys
import os
import fnmatch
import matplotlib.pyplot as plt
from PyQt4 import QtGui
from PyQt4 import QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import random
import psutil
import threading
#from threading import Thread
import time
import datetime
from subprocess import signal
import plotly.plotly as py
import plotly.graph_objs as go
from PIL import Image, ImageTk

py.sign_in('pau_1013', '6jnl8o6nbd')



mapa = []
raiz = '/home'
data = {}

class VentanaPrincipal(QtGui.QWidget):
    def __init__(self):
        super(VentanaPrincipal, self).__init__()
        self.initUI()
        self.setup_Map_Disk_Thread()
        self.setup_Limpiar_Thread()
        self.setup_Folders_Thread()

        self.setup_Save_Thread=Background_Save_Thread()
        self.setup_Save_Thread.start()

        #self.setup_Update_Thread = Background_Update_Thread()
        #self.setup_Update_Thread.start()
        #########################################################
        self.setup_Update_CPU_data = Background_Update_CPU_Graph()
        self.setup_Update_CPU_data.start()
        self.connect(self.setup_Update_CPU_data, QtCore.SIGNAL('CPU_Data'), self.graficaProceso)  # cambiar nombre de senal ####
        ###############################################
        self.setup_Update_MEM_data = Background_Update_MEM_Graph()
        self.setup_Update_MEM_data.start()
        self.connect(self.setup_Update_MEM_data, QtCore.SIGNAL('MEM_Data'), self.graficaMemoria)

        #self.setup_Save_Thread=Background_Save_Thread()
        #self.setup_Save_Thread.start()
        self.setup_Update_Thread=Background_Update_Thread()
        self.setup_Update_Thread.start()

        self.connect(self.setup_Update_Thread, QtCore.SIGNAL('Lista'),self.proc_table)


    def initUI(self):
        self.setGeometry(600, 400, 750, 500)
        self.setWindowTitle('Task Manager')
        self.setFixedSize(900, 550)

        self.grid = QtGui.QGridLayout()
        self.setLayout(self.grid)
        #self.proc_table()

        #aqui estaba tabla proc


        #------------------------------Botones!------------------------------------------
        self.btnEliminar = QtGui.QPushButton('Kill', self)
        btnGrafCPU = QtGui.QPushButton('Ordenar CPU', self)            #############cambie de proc a cpu
        btnGrafMem= QtGui.QPushButton('Ordenar Memoria', self)
        btnOrden = QtGui.QPushButton('Ordenar PID', self)
        self.btnMapDisk = QtGui.QPushButton('Map Disk', self)
        self.btnBrrCache=QtGui.QPushButton('Borrar Cache',self)
        self.btnMapFolders=QtGui.QPushButton('Map Folders',self)

#<<<<<<< HEAD
        # self.btnEliminar.setFixedSize(75,75)  #Tamano de botones
        # btnGrafMem.setFixedSize(75,30)
        # btnGrafCPU.setFixedSize(75,30)
        # self.btnMapDisk.setFixedSize(155,30)
        # self.btnBrrCache.setFixedSize(75,30)
        #
        # self.btnEliminar.move(460,13)
        # btnGrafMem.move(540,280)
        # btnGrafCPU.move(460,280)
        # self.btnMapDisk.move(460,245)
#=======
        self.btnEliminar.setFixedSize(155,75)  #Tamano de botones
        btnOrden.setFixedSize(115, 75)
        btnGrafMem.setFixedSize(155,37.5)
        btnGrafCPU.setFixedSize(155,37.5)
        self.btnMapDisk.setFixedSize(155,75)
        self.btnBrrCache.setFixedSize(115, 30)
        self.btnMapFolders.setFixedSize(115, 30)

        self.btnEliminar.move(115,315)
        btnOrden.move(0,315)
        btnGrafMem.move(425,315)
        btnGrafCPU.move(425,352.5)
        self.btnMapDisk.move(270,315)
        self.btnBrrCache.move(0,400)
        self.btnMapFolders.move(115,400)

        btnGrafMem.clicked.connect(self.ordenar_mem)
        btnGrafCPU.clicked.connect(self.ordenar_cpu)
        btnOrden.clicked.connect(self.ordenar_pid)
        self.btnEliminar.clicked.connect(self.Eliminar)




        


        # ------------------------------Botones!------------------------------------------


        #Graficas
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.grid.addWidget(self.canvas)
        #self.toolbar = NavigationToolbar(self.canvas,self)        ################esto que zoom and shit
#=======
        self.canvas2 = FigureCanvas(self.figure)
        self.grid.addWidget(self.canvas, 0, 1)
        self.grid.addWidget(self.canvas2, 1, 1)
        #self.toolbar = NavigationToolbar(self.canvas,self)


        self.show()

    def proc_table(self, Lista):

       #------------------------------Tabla de Procesos------------------------------------------

        data = {'User': Lista.lista_users,
                'PID': Lista.lista_pids,
                '%CPU': Lista.lista_cpu,
                'Memory': Lista.lista_mem,
                'Nombre de Proceso': Lista.lista_name,}  #Diccionario con los datos de la tabl

        self.table = QtGui.QTableWidget(self) #Se crea la tabla con el numero de filas y columnas
        self.table.setRowCount(Lista.length())
        self.table.setColumnCount(5)
        self.table.setSortingEnabled(True)

        horHeaders = []  # Ingresa los datos a la tabla

        for n, key in enumerate(sorted(data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(data[key]):
                newitem = QtGui.QTableWidgetItem(item)  ########how does this work tho? ask sam
                self.table.setItem(m, n, newitem)

        # Se agregab los headers
        self.table.setHorizontalHeaderLabels(horHeaders)

        # Tamano de la tabla
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.setFixedSize(575, 250)

        self.grid.addWidget(self.table, 0, 0)

        self.table.cellClicked.connect(self.seleccionaProceso) #Para seleccionar proceso
        #------------------------------Tabla de Procesos------------------------------------------

    def graficaMemoria(self, data):
        ax = self.figure.add_subplot(111)
        ax.hold(False)
        ax.plot(data, 'b.-')
        ax.set_ylim([0,6])
        self.canvas.draw()
        

    def graficaProceso(self, data):
        ax = self.figure.add_subplot(111)
        ax.hold(False)
        ax.plot(data, 'r.-')
        ax.set_ylim([0,10])
        self.canvas2.draw()

    def seleccionaProceso(self, row, column):
        print("Row %d and Column %d was clicked" % (row, column))
        self.pidSelec = self.table.item(row,3).text()
        self.pidSelec=int(self.pidSelec)
        print("PID: "+ str(self.pidSelec))


    # --------------------Boton presionado con thread-----------------------
    def enableButton(self):
        self.btnMapDisk.setEnable(True)
    def done(self):
        self.btnMapDisk.setEnable(False)

    def enableButton_limpiar(self):
        self.btnBrrCache.setEnable(True)
    def done_limpiar(self):
        self.btnBrrCache.setEnable(False)

    def enableButton_Folders(self):
        self.btnMapFolders.setEnable(True)
    def done_Folders(self):
        self.btnMapFolders.setEnable(False)

    # --------------------Boton presionado con thread-----------------------


    # ---------------------Background Save Thread ----------------------
    def setup_Save_Thread(self):
        #self.thread_Save=QtCore.QThread()
        self.thread_Save=Background_Save_Thread()

        #self.worker_Save=Background_Save_Worker()
        #self.worker_Save.moveToThread(self.thread_Save)

        self.thread_Save.start()

    # ---------------------Background Save Thread ----------------------
        # ---------------------Background Update Thread ----------------------

    def setup_Update_Thread(self):
        self.thread_Update = Background_Update_Thread()
        self.thread_Update.start()

        # ---------------------Background UpdateThread ----------------------

    # --------------------Map Disk Button----------------------

    def setup_Map_Disk_Thread(self):
        self.thread_MapDisk = QtCore.QThread()
        self.worker_MapDisk = Map_Disk_worker()

        self.worker_MapDisk.moveToThread(self.thread_MapDisk)

        self.btnMapDisk.clicked.connect(self.worker_MapDisk.Map_Disk)
        self.worker_MapDisk.wait_for_input.connect(self.enableButton)
        self.worker_MapDisk.done.connect(self.done)

        self.thread_MapDisk.start()

    # --------------------Map Disk Button----------------------

    #------------------------Limpiar Cache Button ------------------

    def setup_Limpiar_Thread(self):
        self.thread_Limpiar = QtCore.QThread()
        self.worker_Limpiar = Limpiar_worker()

        self.worker_Limpiar.moveToThread(self.thread_Limpiar)

        self.btnBrrCache.clicked.connect(self.worker_Limpiar.borrar_cache)
        self.worker_Limpiar.wait_for_input.connect(self.enableButton_limpiar)
        self.worker_Limpiar.done.connect(self.done_limpiar)

        self.thread_Limpiar.start()

    #------------------------Limpiar Cache Button ------------------

    #------------------------Map Folder Button ---------------------

    def setup_Folders_Thread(self):
        self.thread_Folders = QtCore.QThread()
        self.worker_Folders = Folders_worker()

        self.worker_Folders.moveToThread(self.thread_Folders)

        self.btnMapFolders.clicked.connect(self.worker_Folders.map_folders)
        self.worker_Folders.wait_for_input.connect(self.enableButton_Folders)
        self.worker_Folders.done.connect(self.done_Folders)

        self.thread_Folders.start()

    #------------------------Map Folder Button ---------------------

    def ordenar_mem(self):
        if Lista.MEM==True:
            Lista.Reverse=not (Lista.Reverse)
        Lista.PID=False
        Lista.MEM=True
        Lista.CPU=False

    def ordenar_cpu(self):
        if Lista.CPU==True:
            Lista.Reverse=not (Lista.Reverse)
        Lista.PID=False
        Lista.MEM=False
        Lista.CPU=True

    def ordenar_pid(self):
        if Lista.PID==True:
            Lista.Reverse=not (Lista.Reverse)
        Lista.PID=True
        Lista.MEM=False
        Lista.CPU=False

    def Eliminar(self):
        try:
            os.kill(self.pidSelec, signal.SIGKILL)
        except:
            pass
        self.pidSelec=None

    #----------------Map Folders -------------------------------
class Folders_worker(QtCore.QObject):
    wait_for_input=QtCore.pyqtSignal()
    done = QtCore.pyqtSignal()

    def map_folders(self):
        os.system('baobab /')

    #-------------------Borrar Cache y Ram --------------------------
class Limpiar_worker(QtCore.QObject):
    wait_for_input=QtCore.pyqtSignal()
    done = QtCore.pyqtSignal()

    def borrar_cache(self):
        os.system(" sudo sh -c 'echo 3 >/proc/sys/vm/drop_caches'")
        os.system(" sudo swapoff -a")
        os.system(" sudo swapon -a")


# --------------------Map Disk ----------------------
class Map_Disk_worker(QtCore.QObject):
    wait_for_input=QtCore.pyqtSignal()
    done=QtCore.pyqtSignal()

    def Map_Disk(self):
        lista = []
        cont = 0
        # print("Apps: ")
        cont = self.get_app()
        lista.append(cont)
        cont = 0

        # print('Archivos: ')
        mapa = ["*.doc", "*.txt", "*.xml", "*.exc", "*.pdf", "*.dochtml", "*.dic", "*.idx", "*.rtf", "*.wri", "*.wtx",
                "*.log", "*.zip", "*.rar", "*.zoo", "*.tgz", "*.tar", "*.uu", "*.xxe", "*.r0", "*.tbz2", "*.avi",
                "*.iso", "*.arj", "*.lha", ".*r00", "*.r01", '*.sh', "*.os", '*.o', '*.py']
        cont = self.get_mapa(mapa)
        lista.append(cont)
        cont = 0

        # print("Imagenes: ")
        mapa = ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp", "*.dib", "*.tif", "*.bw", "*.cdr", "*.cgm", "*.gih",
                "*.ico", "*.iff", "*.cpt", "*.mac", "*.pic", "*.pict", "*.pntg", "*.psd", "*.pix", "*.img"]
        cont = self.get_mapa(mapa)
        lista.append(cont)
        cont = 0

        # print("Videos: ")
        mapa = ["*.avi", "*.mov", "*.wmv", "*.mng", "*.qt", "*.dvd", "*.movie", "*.mpeg", "*.mpa", "*.mpv2", "*.divx",
                "*.div", "*.mp2v", "*.bik"]
        cont = self.get_mapa(mapa)
        lista.append(cont)
        cont = 0

        # print("Musica: ")
        mapa = ["*.mp3", "*.au", "*.wav", "*.mid", "*.aiff", "*.it"]
        cont = self.get_mapa(mapa)
        lista.append(cont)
        cont = 0

        for i in range(len(lista)):
            cont = cont + lista[i]
        d_usage = list(psutil.disk_usage('/'))

        total = (d_usage[0])

        free = (d_usage[2])

        print total

        other = total - free - cont
        lista.append(other)
        lista.append(free)

        print("Apps: " + str(lista[0]))
        print("Archivos: " + str(lista[1]))
        print("Imagenes: " + str(lista[2]))
        print("Videos: " + str(lista[3]))
        print("Musica: " + str(lista[4]))

        print(lista)

        Labels = ['Apps ' + str(lista[0] / 1073741824) + ' GB', 'Archivos ' + str(lista[1] / 1073741824) + ' GB',
                  'Imagenes ' + str(lista[2] / 1073741824) + ' GB', 'Videos' + str(lista[3] / 1073741824) + ' GB',
                  'Musica ' + str(lista[4] / 1073741824) + ' GB',
                  'Other ' + str(lista[5] / 1073741824) + ' GB', 'Free' + str(lista[6] / 1073741824) + ' GB']
        fig = {
            'data': [{'labels': Labels,
                      'values': lista,
                      'type': 'pie'}],
            'layout': {'title': 'Disk Mapping'}
        }
        py.image.save_as(fig, 'Map_Disk.png')
        img=Image.open("Map_Disk.png")
        img.show()


        #py.plot(fig)

    def get_mapa(self,m):
        cont = 0
        for root, dirnames, filenames in os.walk(raiz):
            for extension in m:
                for filename in fnmatch.filter(filenames, extension):
                    cont = cont + os.stat(os.path.join(root, filename)).st_size
        return cont

    def get_app(self):
        cont = 0
        for root, dirnames, filenames in os.walk(raiz):
            for filename in filenames:
                if os.access(os.path.join(root,filename),os.X_OK) is True:
                    cont = cont + os.stat(os.path.join(root, filename)).st_size
        return cont

    


# --------------------Map Disk ----------------------

# --------------------Map Disk ----------------------

# ---------------------Background Save Thread ----------------------

class Background_Save_Thread(QtCore.QThread):

    def __init__(self,parent=None):
        super(Background_Save_Thread,self).__init__(parent)

    def run (self):
        while True:
            time.sleep(3)
            #print 'saving'
            Lista.Salvar()
            #print 'done'
            time.sleep(3)


# ---------------------Background Save Thread ----------------------

# ---------------------Background Update Thread ----------------------

class Background_Update_Thread(QtCore.QThread):

    def __init__(self, parent=None):
        super(Background_Update_Thread, self).__init__(parent)

    def run(self):
        while True:

            Lista.Vaciar()
            for proc in psutil.process_iter():
                Lista.agregar(proc)
            Lista.Ordenar(Lista.PID,Lista.CPU,Lista.MEM)
            Lista.reverse()
            Lista.imprimir()
            self.emit(QtCore.SIGNAL('Lista'), Lista)
            time.sleep(7)



# --------------------- Background_Update_CPU_Graph ----------------------

class Background_Update_CPU_Graph(QtCore.QThread):

    def __init__(self, parent=None):
        super(Background_Update_CPU_Graph,self).__init__(parent)

    def run(self):
        while True:
            #time.sleep(1)
            data = []
            for i in range(0, 100):
                a = psutil.cpu_percent(interval=0.10, percpu= False)
                q = a / 10
                data.append(q)
            self.emit(QtCore.SIGNAL('CPU_Data'), data)


# --------------------- Background_Update_CPU_Graph ----------------------
class Background_Update_MEM_Graph(QtCore.QThread):

    def __init__(self, parent=None):
        super(Background_Update_MEM_Graph,self).__init__(parent)

    def run(self):
        while True:
            time.sleep(0.5)
            data = []
            for i in range(0, 100):
                q = psutil.virtual_memory()
                mem = q.percent / 10
                data.append(mem)
            self.emit(QtCore.SIGNAL('MEM_Data'), data)

###########################################################################################################

class procs: #proc es un objeto de la clase psutil del cual podemos obtener toda la informacion de un proceso
    def __init__(self,proc):
        #self.proc=proc
        self.username=proc.username()
        self.pid=proc.pid
        self.cpu=float(proc.cpu_percent())
        self.mem=float((proc.memory_info().vms)/(1024*1024))
        self.name=proc.name()

        self.next = None
        self.prev=None
        self.posicion=None



class Lista:
    def __init__(self):
        self.head=None
        self.lista_users=[]
        self.lista_cpu=[]
        self.lista_pids=[]
        self.lista_name=[]
        self.lista_mem=[]


        self.CPU=False
        self.MEM=False
        self.PID=False
        self.Reverse=False

    def Vaciar(self):
        self.head = None
        self.lista_users = []
        self.lista_cpu = []
        self.lista_pids = []
        self.lista_name = []
        self.lista_mem = []


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

            self.Quicksort_interno_CPU(izquierda)
            izquierda.append(Pivote)
            self.Quicksort_interno_CPU(derecha)

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

            self.Quicksort_interno_MEM(izquierda)
            izquierda.append(Pivote)
            self.Quicksort_interno_MEM(derecha)

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
        self.lista_users = []
        self.lista_pids = []
        self.lista_cpu= []
        self.lista_mem = []
        self.lista_name = []
        string=""
        if temp!= None:
            while temp is not None:
                string=string + "USER: {0} PID: {1} CPU: {2} MEM: {3} NAME: {4}\n".format(str(temp.username),str(temp.pid),str(temp.cpu),str(temp.mem),str(temp.name))
                self.lista_users.append(str(temp.username))
                self.lista_pids.append(str(temp.pid))
                self.lista_cpu.append(str(temp.cpu))
                self.lista_mem.append(str(temp.mem))
                self.lista_name.append(str(temp.name))
                temp=temp.next

            #print(string)


    def agregar(self,proceso): #agrega un proc a la lista
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
    def reverse(self):

        if self.Reverse==True:
            list_nodes=self.Lista_desordenada()
            list_nodes=list_nodes[::-1]

            self.head=list_nodes[0]

            self.head.prev = None

            nodo_temp = self.head
            i = 1
            while i < len(list_nodes):
                nodo_temp.next = list_nodes[i]
                i = i + 1
                if i == len(list_nodes) - 1:
                    list_nodes[i].next = None
                nodo_temp = nodo_temp.next

            count = 0
            nodo_temp = self.head
            while nodo_temp != None:
                nodo_temp.posicion = count
                nodo_temp = nodo_temp.next
                count = count + 1




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
        archi = open('Task_Manager_Stats_%s.txt' % cont, 'a')
        statsinfo = os.stat('Task_Manager_Stats_%s.txt' % cont)
        while (statsinfo.st_size / (1024*1024)) > 100:
            cont = cont + 1
            archi = open('Task_Manager_Stats_%s.txt' % cont, 'a')
            statsinfo = os.stat('Task_Manager_Stats_%s.txt' % cont)

        date=datetime.datetime.now()
        #print date.strftime("%Y-%m-%d %H:%M")
        archi.write(str(date.strftime("%Y-%m-%d %H:%M"))+"\n")
        proc_temp = self.head
        while proc_temp != None:
            archi.write("USER: {0} PID: {1} CPU: {2} MEM: {3} NAME: {4}\n".format
                        (str(proc_temp.username), str(proc_temp.pid), str(proc_temp.cpu), str(proc_temp.mem),
                         str(proc_temp.name)))
            proc_temp = proc_temp.next
        archi.write('\n')

        archi.close()





def Crear_Lista(): #Regresa una lista con todos los procesos actuales
    List=Lista()
    thread_procesos=[]
    for proc in psutil.process_iter():
        thread=threading.Thread(target=List.agregar,args=(proc,))
        thread.setDaemon(True)
        thread.start()
        thread_procesos.append(thread)

    for thread_proceso in thread_procesos:
        thread_proceso.join()

    return List


def main():
    app = QtGui.QApplication(sys.argv)
    w = VentanaPrincipal()
    app.exec_()



if __name__ == '__main__':
    Lista = Crear_Lista()
    #Lista=Lista()
    Lista.PID=True
    Lista.Ordenar(Lista.PID,Lista.CPU,Lista.MEM)
    Lista.imprimir()

    main()

