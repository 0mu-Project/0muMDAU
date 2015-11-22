#!/usr/bin/python3

import cgitb
cgitb.enable()

import cgi
import os 
import hashlib
form = cgi.FieldStorage()
argment = form.getvalue('content')
filen = form.getvalue('title')
user = form.getvalue ('username')
passd = form.getvalue('password')
pathuser = "../pskey/" + user
hashsha =  hashlib.sha256(passd.replace('\n','').encode())

if os.path.exists(pathuser) == True :
    with open( pathuser ,'r' ) as f:
        fline = f.readline()
    if fline.replace('\n' , '')  == hashsha.hexdigest() :
        f = open('_posts/'+ filen  +'.markdown', 'w', encoding = 'UTF-8') 
        f.write(argment)
        f.close()
    else:
        print("去吃大便")
else:
    print("去吃屎吧你")

print 


