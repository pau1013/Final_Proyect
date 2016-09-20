import os
from collections import namedtuple


DiskUsage = namedtuple('DiskUsage', 'total  used  free')

def disk_usage(path):
    size = os.statvfs(path)
    free = (size.f_bavail * size.f_frsize) / 1024
    total = (size.f_blocks * size.f_frsize) / 1024
    used = (total - free)
    return DiskUsage(total, used, free)


print disk_usage('./')
