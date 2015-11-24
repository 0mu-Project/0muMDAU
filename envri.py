#!/usr/bin/python2.7 
import setting
import subprocess
import sys
import git 
import socket

def rungitpull():
    g = git.cmd.Git("./")
    g.pull()

def importapp():
    subprocess.call(['python2 ./pyfCGI.py 9002'],shell=True)


def portcheck(port):
    s = socket.socket()
    s.settimeout(0.5)
    try:
         return s.connect_ex(('localhost', port)) != 0
    finally:
        s.close()

if __name__ == "__main__":
    while 1:
        if portcheck(9002) == True:
            rungitpull()
            importapp()

