import subprocess
import os


p = 'README.md'
o= os.path.abspath(p)
print(o)
a= subprocess.Popen(o, shell=True)
#print(a)
