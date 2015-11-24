#!/usr/bin/python2.7
# -*- coding: utf-8 -*-  
import subprocess
import web
import os 
import hashlib
import git 

urls = (
        "/cgi-bin/login", "ClassLogin",
        "/cgi-bin/save", "ClassSave" ,
        "/cgi-bin/blogget", "ClassLoad",
        "/cgi-bin/jsonlist/(.+)" , "ClassJson",
        "/cgi-bin/getmd/(.+)" , "ClassMD",
        "/cgi-bin/getmdposted/(.+)", "ClassMDP",
        "/cgi-bin/submit" , "ClassSubmit"
)
app = web.application(urls, globals())
session = web.session.Session(app,web.session.DiskStore('../sessions'),initializer={'login':0,' username' : ''})
web.config.debug = False

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
                if fline.replace('\n' , '')  == hashsha.hexdigest() :
                    web.setcookie('login','login_cookie',60)
                    session._initializer['login'] = 1
                    session._initializer['username'] = user 
                    print("posted")
                    print(session._initializer['login'])
                    print(session._initializer['username'])
    
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
    def POST(self):
        web.header('Content-Type', 'text')
        blogpath = "./blog"
        if os.path.exists(blogpath) == True:
            g = git.cmd.Git(blogpath)
            g.pull()
        else:
            git.Git().clone("https://github.com/0mu-Project/blog.git")

        print(session._initializer['login'])
        if session._initializer['login'] == 1:
            print("test")
            return "login"
        else:
            return "nlogin"



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
