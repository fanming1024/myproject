## -*- coding: utf-8 -*-
import subprocess
import threading
from queue import Queue
from queue import Empty
import time
mutex=threading.Lock()


def pingtest(ip):


    s = subprocess.Popen(["ping", "-n", "5", ip],stdout=subprocess.PIPE).communicate()[0]

    mutex.acquire()
    if b'TTL' in s:

        out=ip+' Active'
        result.append(out)

    else:

        out=ip+' Inactive'
        result.append(out)

    mutex.release()



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

        for i in range(2048):
            thr = threading.Thread(target=loadqueue, args=(q,))
            thr.start()
            threads.append(thr)

        for thr in threads:
            thr.join()


if __name__ == '__main__':


        print("This tool is developed to check active&inactive servers in internal network to support daily business/audit.\n"
              "Please put IP addrs into ip.txt under the folder and check out.txt for output result!\n"
              "Author: PwC US MSH Hybrid Cloud, Simon Fan\n"
              "Contact: simon.m.fan@pwc.com\n"
              "Please make sure ip.txt file is exsiting and contains IP addr info if the result shows blank! ")
        print('''
                        .---- .
                       .       、
                    _·'__       ·
                . --($) ($$)---/#\\
              .`@             /###\\
              :         ,     #####
               `-..__.-'  _.- \###/
                   `;_:       `"
                     .'""""""`.
                    /,  hi,    \\\\
                   //  你好！    \\\\
                  `-._________.-'
                     __`.|.`__
                   (_____|_____)
        ''')

        print("Initializing", end="")

        for g in range(5):
            print(".", end='', flush=True)
            time.sleep(0.5)
        print("\n")

        result = []
        num = 0
        file = open("./out.txt", 'w',newline='')
        file.truncate()


        time_start = time.time()
        print('IP            Status')
        main()


        print('IP            Status', file=file)
        result.sort()
        for x in result:
            print(x)
            print(x,file=file)
            num=num+1

        time_end = time.time()
        time_c = time_end - time_start

        print('Time Cost=%s s'%(time_c))
        print('The total IP number is',num)

        file.close()
        print('./out.txt is created for the result.')

        input("Press any keys to exit.")




