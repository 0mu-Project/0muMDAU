#!/usr/bin/python2.7
# -*- coding: utf-8 -*-  

import web
import os 
import hashlib
import git 

urls = (
        "/cgi-bin/save", "ClassSave" ,
        "/cgi-bin/blogget", "ClassLoad",
        "/cgi-bin/jsonlist" , "ClassJson"
) 


class ClassSave:
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

class ClassLoad:
    def POST(self):
        blogpath = "./blog"
        if os.path.exists(blogpath) == True:
            g = git.cmd.Git(blogpath)
            g.pull()
        else:
            git.Git().clone("https://github.com/0mu-Project/blog.git")

class ClassJson:
    def GET(self):
        postpath = "./_posts"
        if os.path.exists(postpath) == True:
            directory = os.path.expanduser(postpath)
            data = []
            i = 0
            for f in os.listdir(directory):
                if os.path.isfile(os.path.join(directory, f)):
                    i = i + 1
                    data.insert(i,f)
                else:
                    data1 = "False"
                import json 
        web.header('Content-Type', 'application/json')
        return json.dumps(data,separators=( ',' , ':'))

if __name__ == "__main__":  
    app = web.application(urls, globals())
    app.run()  
