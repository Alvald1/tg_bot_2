import time
import threading
import subprocess
flag = 1
arr = []
with open('config.txt', 'r', encoding="utf-8") as f:
    text = f.read()
    arr = [i.split() for i in text.split('\n')]
st_arr = arr


def doit():
    t = threading.currentThread()
    a = len(arr)
    flag = 1
    while flag:
        for i in st_arr:
            if not getattr(t, "do_run", True):
                flag = 0
                break
            print(i)
            getMove(i)
            p = subprocess.run('exe\stayAlive.exe')
            time.sleep(2)


def start():
    t = threading.Thread(target=doit)
    t.start()
    return t


def stop(t):
    t.do_run = False
    time.sleep(1)


def find(a):
    for i in arr:
        if a == i:
            return arr.index(i)


def getMove(a):
    global arr
    f = open('config.txt', 'r', encoding="utf-8")
    text = f.read()
    arr = [i.split() for i in text.split('\n')]
    f.close()
    t = find(a)

    tmp = arr[t]
    del arr[t]
    arr.insert(0, tmp)
    f = open('config.txt', 'w')
    s = ''
    for i in arr:
        s += (' '.join(i)+'\n')
    s = s[:-1]
    f.write(s)
    f.close()
    p = subprocess.run(['exe\getMove.exe', str(t)])
