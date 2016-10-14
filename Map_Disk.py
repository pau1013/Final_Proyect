import os
import fnmatch
import plotly.plotly as py
import plotly.graph_objs as go
from PIL import Image, ImageTk
import psutil

import Tkinter
#from Tkinter import *
py.sign_in('pau1_1013', '6jnl8o6nbd')




mapa = []
raiz = '/'



#Map_Disk()

class App:
    def __init__(self,master):
        frame = Tkinter.Frame(master)
        frame.pack()
        self.button=Tkinter.Button(frame,text="REFRESH", fg='blue',
                                   command=self.Map_Disk)
        self.button.pack(side=Tkinter.TOP)
        if os.path.isfile("Map_Disk.png") is False:
            img=None
        else:
            img=ImageTk.PhotoImage(Image.open('Map_Disk.png'))
        self.panel=Tkinter.Label(frame,image=img)
        self.image=img
        self.panel.pack(side=Tkinter.BOTTOM,fill='both',expand='yes')



    def Map_Disk(self):
        lista = []
        cont = 0
        #print("Apps: ")
        cont =self.get_app()
        lista.append(cont)
        cont =0

        #print('Archivos: ')
        mapa = ["*.doc", "*.txt", "*.xml","*.exc", "*.pdf", "*.dochtml", "*.dic", "*.idx", "*.rtf", "*.wri", "*.wtx",
                "*.log", "*.zip", "*.rar", "*.zoo", "*.tgz", "*.tar", "*.uu", "*.xxe", "*.r0", "*.tbz2", "*.avi",
                "*.iso", "*.arj", "*.lha", ".*r00", "*.r01",'*.sh',"*.os",'*.o','*.py']
        cont = self.get_mapa(mapa)
        lista.append(cont)
        cont = 0

        #print("Imagenes: ")
        mapa = ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp", "*.dib", "*.tif", "*.bw", "*.cdr", "*.cgm", "*.gih",
                "*.ico", "*.iff", "*.cpt", "*.mac", "*.pic", "*.pict", "*.pntg", "*.psd", "*.pix", "*.img"]
        cont = self.get_mapa(mapa)
        lista.append(cont)
        cont = 0

        #print("Videos: ")
        mapa = ["*.avi", "*.mov", "*.wmv", "*.mng", "*.qt", "*.dvd", "*.movie", "*.mpeg", "*.mpa", "*.mpv2", "*.divx",
                "*.div", "*.mp2v", "*.bik"]
        cont = self.get_mapa(mapa)
        lista.append(cont)
        cont = 0

        #print("Musica: ")
        mapa = ["*.mp3", "*.au", "*.wav", "*.mid", "*.aiff", "*.it"]
        cont = self.get_mapa(mapa)
        lista.append(cont)
        cont = 0

        for i in range(len(lista)):
            cont=cont+lista[i]
        d_usage = list(psutil.disk_usage('/'))

        total =(d_usage[0])

        free = (d_usage[2])

        print total

        other=total-free-cont
        lista.append(other)
        lista.append(free)
        
        print("Apps: " + str(lista[0]))
        print("Archivos: " + str(lista[1]))
        print("Imagenes: " + str(lista[2]))
        print("Videos: " + str(lista[3]))
        print("Musica: " + str(lista[4]))
        
        print(lista)

        Labels = ['Apps('+str(lista[0]/1073741824)+')GB','Archivos('+str(lista[1]/1073741824)+')GB',
                  'Imagenes'+str(lista[2]/1073741824)+')GB', 'Videos'+str(lista[3]/1073741824)+')GB', 'Musica'+str(lista[4]/1073741824)+')GB',
                  'Other'+str(lista[5]/1073741824)+')GB','Free'+str(lista[6]/1073741824)+')GB']
        fig = {
            'data': [{'labels': Labels,
                      'values': lista,
                      'type': 'pie'}],
            'layout': {'title': 'Disk Mapping'}
        }
        py.image.save_as(fig, 'Map_Disk.png')
        img=ImageTk.PhotoImage(Image.open('Map_Disk.png'))
        self.panel.configure(image=img)
        self.image=img

    def get_mapa(self,m):
        cont = 0
        for root, dirnames, filenames in os.walk(raiz):
           for extension in m:
               for filename in fnmatch.filter(filenames, extension):
                   try:
                        cont = cont + os.stat(os.path.join(root,filename)).st_size
                   except:
                       pass
        return cont

    def get_app(self):
        cont = 0
        for root, dirnames, filenames in os.walk(raiz):
            for filename in filenames:
                if os.access(os.path.join(root,filename),os.X_OK) is True:
                    cont = cont + os.stat(os.path.join(root, filename)).st_size
        return cont

root=Tkinter.Tk()
app=App(root)
root.mainloop()
