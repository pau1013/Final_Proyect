import os
import fnmatch
import plotly.plotly as py
import plotly.graph_objs as go
from PIL import Image, ImageTk

import Tkinter
#from Tkinter import *


py.sign_in('pau1013','tnfc99jciz')


mapa = []
raiz = '/home'



#Map_Disk()

class App:
    def __init__(self,master):
        frame = Tkinter.Frame(master)
        frame.pack()
        self.button=Tkinter.Button(frame,text="REFRESH", fg='blue',
                                   command=self.Map_Disk)
        self.button.pack(side=Tkinter.TOP)
        img=ImageTk.PhotoImage(Image.open('Map_Disk.png'))
        self.panel=Tkinter.Label(frame,image=img)
        self.image=img
        self.panel.pack(side=Tkinter.BOTTOM,fill='both',expand='yes')

    def Map_Disk(self):
        lista = []
        cont = 0
        print('Archivos: ')
        mapa = ["*.doc", "*.txt", "*.xml", "*.exc", "*.pdf", "*.dochtml", "*.dic", "*.idx", "*.rtf", "*.wri", "*.wtx",
                "*.log", "*.zip", "*.rar", "*.zoo", "*.tgz", "*.tar", "*.uu", "*.xxe", "*.r0", "*.tbz2", "*.avi",
                "*.iso", "*.arj"]
        for n in mapa:
            cont = cont + self.get_mapa(n)
        lista.append(cont)
        cont = 0

        print("Imagenes: ")
        mapa = ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp", "*.dib", "*.tif", "*.bw", "*.cdr", "*.cgm", "*.gih",
                "*.ico", "*.iff", "*.cpt", "*.mac", "*.pic", "*.pict", "*.pntg", "*.psd", "*.pix"]
        for n in mapa:
            cont = cont + self.get_mapa(n)
        lista.append(cont)
        cont = 0

        print("Videos: ")
        mapa = ["*.avi", "*.mov", "*.wmv", "*.mng", "*.qt", "*.dvd", "*.movie", "*.mpeg", "*.mpa", "*.mpv2", "*.divx",
                "*.div", "*.mp2v", "*.bik"]
        for n in mapa:
            cont = cont + self.get_mapa(n)
        lista.append(cont)
        cont = 0

        print("Musica: ")
        mapa = ["*.mp3", "*.au", "*.wav", "*.mid", "*.aiff", "*.it"]
        for n in mapa:
            cont = cont + self.get_mapa(n)
        lista.append(cont)
        cont = 0

        print(lista)

        Labels = ['Archivos', 'Imagenes', 'Videos', 'Musica']
        fig = {
            'data': [{'labels': Labels,
                      'values': lista,
                      'type': 'pie'}]
        }
        py.image.save_as(fig, 'Map_Disk.png')
        img=ImageTk.PhotoImage(Image.open('Map_Disk.png'))
        self.panel.configure(image=img)
        self.image=img

    def get_mapa(self,m):
        cont = 0
        for root, dirnames, filenames in os.walk(raiz):
            for filename in fnmatch.filter(filenames, m):
                cont = cont + os.stat(os.path.join(root, filename)).st_size
        return cont

root=Tkinter.Tk()
app=App(root)
root.mainloop()