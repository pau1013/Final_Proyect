import os
import fnmatch

mapa = []
raiz = '/home'

def Map_Disk():
    lista = []
    cont=0
    print('Archivos: ')
    mapa = ["*.doc","*.txt", "*.xml", "*.exc", "*.pdf", "*.dochtml", "*.dic", "*.idx", "*.rtf", "*.wri", "*.wtx", "*.log", "*.zip", "*.rar", "*.zoo", "*.tgz", "*.tar", "*.uu", "*.xxe", "*.r0", "*.tbz2", "*.avi", "*.iso", "*.arj"]
    for n in mapa:
        cont =cont+get_mapa(n)
    lista.append(cont)
    cont=0

    print("Imagenes: ")
    mapa = ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp", "*.dib", "*.tif", "*.bw", "*.cdr", "*.cgm", "*.gih", "*.ico", "*.iff", "*.cpt", "*.mac", "*.pic", "*.pict", "*.pntg", "*.psd", "*.pix"]
    for n in mapa:
        cont =cont+get_mapa(n)
    lista.append(cont)
    cont=0

    print("Videos: ")
    mapa = ["*.avi", "*.mov", "*.wmv", "*.mng", "*.qt", "*.dvd", "*.movie", "*.mpeg", "*.mpa", "*.mpv2", "*.divx", "*.div", "*.mp2v", "*.bik"]
    for n in mapa:
        cont =cont+get_mapa(n)
    lista.append(cont)
    cont=0

    print("Musica: ")
    mapa = ["*.mp3", "*.au", "*.wav", "*.mid", "*.aiff", "*.it"]
    for n in mapa:
        cont =cont+get_mapa(n)
    lista.append(cont)
    cont=0

    print(lista)
def get_mapa(m):
    cont = 0
    for root, dirnames, filenames in os.walk(raiz):
        for filename in fnmatch.filter(filenames, m):
            cont=cont+os.stat(os.path.join(root, filename)).st_size
    return cont

Map_Disk()