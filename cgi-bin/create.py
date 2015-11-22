#!/usr/bin/python2.7
# -*- coding: utf-8 -*-  

import web
import os 
import hashlib

urls = ("/.*", "InputRun") 

app = web.application(urls, globals())  

class InputRun:
    def POST(self):
        form = web.input()
        argment = form.get('content')
        filen = form.get('title')
        user = form.get('username')
        passd = form.get('password')
        pathuser = "../pskey/" + user
        hashsha =  hashlib.sha256(passd.replace('\n','').encode())
        if os.path.exists(pathuser) == True :
            with open( pathuser ,'r' ) as f:
                fline = f.readline()
                if fline.replace('\n' , '')  == hashsha.hexdigest() :
                    f = open('_posts/'+ filen  +'.markdown', 'w') 
                    f.write(argment.encode('UTF-8'))
                    f.close()
                    ans = "file open"
                else:
                    ans ="eat shit"
        else:
            ans = "eat shit"
            return pathuser 

if __name__ == "__main__":  
        app.run()  
