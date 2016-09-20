import subprocess
import os


p = 'Primer_avance.md'
o= os.path.abspath(p)
print(o)
a= subprocess.call(o)
#print(a)
