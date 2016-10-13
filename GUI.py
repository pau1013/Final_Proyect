import sys
import os
import fnmatch
import matplotlib.pyplot as plt
from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import random

mapa = []
raiz = '/home'

class VentanaPrincipal(QtGui.QWidget):
    def __init__(self):
        super(VentanaPrincipal, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 400, 750, 500)
        self.setWindowTitle('Task Manager')
        self.setFixedSize(750, 500)

        grid = QtGui.QGridLayout()
        self.setLayout(grid)

        # ------------------------------Tabla de Procesos------------------------------------------
        data = {'User': ['1', '2', '3', '3'],
                'PID': ['465121', '5541', '651121', '251512'],
                '%CPU': ['9', '8', '9', '5'],
                'Memory': ['4', '3', '4', '8'],
                'Nombre de Proceso': ['4', '3', '4', '8'],}  #Diccionario con los datos de la tabl

        self.table = QtGui.QTableWidget(self) #Se crea la tabla con el numero de filas y columnas
        self.table.setRowCount(6)
        self.table.setColumnCount(5)

        horHeaders = []  # Ingresa los datos a la tabla
        for n, key in enumerate(sorted(data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(data[key]):
                newitem = QtGui.QTableWidgetItem(item)
                self.table.setItem(m, n, newitem)

        # Se agregab los headers
        self.table.setHorizontalHeaderLabels(horHeaders)

        # Tamano de la tabla
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.setFixedSize(400, 300)

        grid.addWidget(self.table, 0, 0)

        self.table.cellClicked.connect(self.seleccionaProceso) #Para seleccionar proceso
        # ------------------------------Tabla de Procesos------------------------------------------


        #------------------------------Botones!------------------------------------------
        btnEliminar = QtGui.QPushButton('Terminar', self)
        btnGrafProc = QtGui.QPushButton('Proceso', self)
        btnGrafMem= QtGui.QPushButton('Memoria', self)
        btnMapDisk = QtGui.QPushButton('Map Disk', self)

        btnEliminar.setFixedSize(75,75)  #Tamano de botones
        btnGrafMem.setFixedSize(75,30)
        btnGrafProc.setFixedSize(75,30)
        btnMapDisk.setFixedSize(155,30)

        btnEliminar.move(460,13)
        btnGrafMem.move(540,280)
        btnGrafProc.move(460,280)
        btnMapDisk.move(460,245)

        btnGrafMem.clicked.connect(self.graficaMemoria)
        btnGrafProc.clicked.connect(self.graficaProceso)
        btnMapDisk.clicked.connect(Map_Disk)
        # ------------------------------Botones!------------------------------------------


        #Graficas
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        grid.addWidget(self.canvas)
        #self.toolbar = NavigationToolbar(self.canvas,self)



        self.show()

    def graficaMemoria(self):
        data = [random.random() for i in range(100)]
        ax = self.figure.add_subplot(111)
        ax.hold(False)
        ax.plot(data, 'b.-')
        self.canvas.draw()

    def graficaProceso(self):
        data = [random.random() for i in range(100)]
        ax = self.figure.add_subplot(111)
        ax.hold(False)
        ax.plot(data, 'r.-')
        self.canvas.draw()

    def seleccionaProceso(self, row, column):
        print("Row %d and Column %d was clicked" % (row, column))
        pidSelec = self.table.item(row,3).text()
        print("PID: "+ pidSelec)



def Map_Disk():
    lista = []
    cont = 0
    mapa = ["*.doc", "*.txt", "*.xml", "*.exc", "*.pdf", "*.dochtml", "*.dic", "*.idx", "*.rtf", "*.wri", "*.wtx",
            "*.log", "*.zip", "*.rar", "*.zoo", "*.tgz", "*.tar", "*.uu", "*.xxe", "*.r0", "*.tbz2", "*.avi",
            "*.iso", "*.arj"]
    for n in mapa:
        cont = cont + get_mapa(n)
    lista.append(cont)
    cont = 0
    print("Archivos: " + str(lista[0]))

def get_mapa(m):
    cont = 0
    for root, dirnames, filenames in os.walk(raiz):
        for filename in fnmatch.filter(filenames, m):
            cont = cont + os.stat(os.path.join(root, filename)).st_size
    return cont



def main():
    app = QtGui.QApplication(sys.argv)
    w = VentanaPrincipal()
    app.exec_()



if __name__ == '__main__':
    main()
