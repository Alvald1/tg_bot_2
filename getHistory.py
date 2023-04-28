import subprocess
import time
cmd = ['exe\setHistory.exe', 'exe\setIncome.exe', 'exe\getHistory.exe', 'exe\getPos.exe', 'exe\getBalance.exe', 'exe\stayAlive.exe']
# p = subprocess.run(cmd[3])


def getHis():
    p = subprocess.run(cmd[0])
    if p.returncode == 0:
        p = subprocess.run(cmd[1])
        if p.returncode == 0:
            p = subprocess.run(cmd[2])


def getBal():
    p = subprocess.run(cmd[4])
