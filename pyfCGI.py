#!/usr/bin/python2.7
# -*- coding: utf-8 -*-  
import subprocess
import web
import os 
import hashlib
import git 
import datetime

web.config.debug = False
urls = (
        "/login/panel", "ClassLoginPanel",
        "/login" , "ClassLogin",
        "/save", "ClassSave" ,
        "/", "ClassLoad",
        "/jsonlist/(.+)" , "ClassJson",
        "/getmd/(.+)" , "ClassMD",
        "/getmdposted/(.+)", "ClassMDP",
        "/submit" , "ClassSubmit",
        "/raise" , "ClassRaise"
)
app = web.application(urls, globals())
session = web.session.Session(app,web.session.DiskStore('../nsessions'))
from web.contrib.template import render_jinja
render = render_jinja(
        'templates',
        encoding='utf-8',
        )
class ClassRaise:
    def GET(self):
        if session.loggin == True:
            print(session.loggin)
            return render.redit()

class ClassLogin:
    def POST(self):
        form = web.input()
        user = form.get('buser')
        passd = form.get('bpass')
        pathuser = "../pskey/" + user
        hashsha =  hashlib.sha256(passd.replace('\n','').encode())
        if os.path.exists(pathuser) == True :
            with open( pathuser ,'r' ) as f:
                fline = f.readline()
                if fline.replace('\n' , '')  == hashsha.hexdigest():
                    session.loggin = True      

class ClassLoginPanel:
    def GET(self):
        if session.get("loggin") is not None:
            print("data1")
            print(session.get('loggin'))
            return render.redit()
        else:
            print("d2")
            print(session.get('loggin'))
            return render.login()

class ClassSubmit:
    def POST(self):
        web.header('Content-Type', 'text')
        form = web.input()
        argment = form.get('content')
        fil = form.get('title')
        import datetime
        now = datetime.datetime.now()
        filen = now.strftime("%Y-%m-%d")+"-"+fil 
        if not fil.strip():
            return "打檔名拉,e04"
        else:
            user = form.get('username')
            passd = form.get('password')
            pathuser = "../pskey/" + user
            hashsha =  hashlib.sha256(passd.replace('\n','').encode())
            if os.path.exists(pathuser) == True :
                with open( pathuser ,'r' ) as f:
                    fline = f.readline()
                    if fline.replace('\n' , '')  == hashsha.hexdigest() :
                        f = open('_posted/'+ filen  +'.markdown', 'w') 
                        f.write(argment.encode('UTF-8'))
                        f.close()
                        ans = "file open"
                        import shutil
                        shutil.copyfile('_posted/' + filen +'.markdown','blog/_posts/' + filen +'.markdown')
                        repo = git.Repo("./blog")
                        index = repo.index
                        index.add(["_posts"])
                        message = 'add new posts' + filen
                        index.commit(message)
                        subprocess.call(['bash ./script/autoAuth.sh ' + user + ' ' + passd + ' ./blog'], shell=True)
                        return "文章已經存在本地的_posted,文章即將發布.." 
                    else:
                        return "密碼錯誤是要登入三小"
            else:
                return "帳號錯誤是要登入三小"
        


class ClassMD:
    def POST(self,name):
        f = open('./_posts/'+ name)
        
        return f.read()

class ClassMDP:
    def POST(self,name):
        f = open('./blog/_posts/'+ name)
        
        return f.read()
class ClassSave:
    def POST(self):
        form = web.input()
        argment = form.get('content')
        fil = form.get('title')
        import datetime
        now = datetime.datetime.now()
        filen = now.strftime("%Y-%m-%d")+"-"+fil

        if not fil.strip():
            return "打標題啦,e04!"
        else:
            f = open('_posts/'+ filen  +'.markdown', 'w') 
            f.write(argment.encode('UTF-8'))
            f.close()
            ans = "file open"
            return "文章已經存在本地的_posts,重新整理即可在佇列中看到"

class ClassLoad:
    def GET(self):
        return render.gitload()
    def POST(self):
        blogpath = "./blog"
        if os.path.exists(blogpath) == True:
            g = git.cmd.Git(blogpath)
            g.pull()
        else:
            git.Git().clone("https://github.com/0mu-Project/blog.git")
        

class ClassJson:
    def GET(self,name):
        if name == "posts" :
            postpath = "./_posts"
        else:
            postpath = "./blog/_posts"

        if os.path.exists(postpath) == True:
            directory = os.path.expanduser(postpath)
            data = []
            i = 0
            for f in os.listdir(directory):
                if os.path.isfile(os.path.join(directory, f)):
                    i = i + 1
                    data.insert(i,f)
                    import json
                    web.header('Content-Type', 'application/json')
                    return json.dumps(data,separators=( ',' , ':'))
                else:
                    data1 = "False"
                    
        else:
            os.makedirs(postpath)

if __name__ == "__main__":  
    app.run()  
