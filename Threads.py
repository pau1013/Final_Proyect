import threading
import time

exit = 0

class Thread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.ThreadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print "Starting " + self.name
        print_time(self.name, self.counter, 5)
        print "Exiting " + self.name

def print_time(threadName, delay, counter):
    while counter:
        if exit:
            threadName.exit()
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1

thread1 = Thread(1, "Thread 1", 1)
thread2 = Thread(2, "Thread 2", 2)
thread3 = Thread(3, "Thread 3", 3)
thread4 = Thread(4, "Thread 4", 4)
thread5 = Thread(5, "Thread 5", 5)

thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()

print "Exiting Main Thread"
