import threading
import time

def threadings(num):
    number = str(num)
    print ("thread " + number)
    time.sleep(1)

if __name__ == "__main__":
    threads = []
    for i in range(0,5):
        thread = threading.Thread(target=threadings(i))
        threads.append(thread)

    for j in threads:
        j.start()
    print "im dead inside"

    for j in threads:
        j.join()

    print "Im so done"

num = 5
threadings(num)
