import subprocess
import threading
from queue import Queue
from queue import Empty
import time

def pingtest(ip):
    s = subprocess.Popen(["ping", "-c", "5", ip],stdout=subprocess.PIPE).communicate()[0]
    out = open("./out.txt", 'a')
    if b'TTL' in s:
        print(ip, "active",file=out)
    elif b'ttl' in s:
            print(ip, "active", file=out)

    else:
        print(ip, "inactive",file=out)
    out.close()

def loadqueue(q):
    try:
        while True:
            ip=q.get_nowait()
            pingtest(ip)
    except Empty:
        pass


def main():
    q = Queue()
    with open("./ip.txt",'r') as f:
        x=" ".join([content.strip() for content in f])
        y=x.split()
        for t in y:
            q.put(t)

        threads=[]

        for i in range(1024):
            thr = threading.Thread(target=loadqueue, args=(q,))
            thr.start()
            threads.append(thr)

        for thr in threads:
            thr.join()


if __name__ == '__main__':
        print("This tool is developed to check active&inactive servers in internal network to support daily business/audit.\n"
              "Please put IP addrs into ip.txt under the folder and check out.txt for output result when the prompt closed!\n"
              "Author: PwC US MSH Hybrid Cloud, Simon Fan\n"
              "Contact: simon.m.fan@pwc.com")
        out= open("./out.txt", 'w')
        out.truncate()
        print('IP Status',file=out)
        out.close()
        time_start = time.time()
        main()
        out = open("./out.txt", 'r')
        str=out.read()
        print(str)
        out.close()
        time_end = time.time()
        time_c = time_end - time_start
        print('time cost', time_c, 's')