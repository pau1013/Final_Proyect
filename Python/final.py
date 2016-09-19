import os

size = os.statvfs('/')
output = (size.f_bavail * size.f_frsize) / 1024

print("Available disk space", output, "k")
