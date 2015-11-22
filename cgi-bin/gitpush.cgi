#!/usr/bin/python2.7
import cgitb
cgitb.enable()

import cgi
import os

if os.path.exists("./blog") == True :
    print("true")
    
else:
    print("False")
    import git
    os.makedirs("./blog")
    git.Git().clone("git@github.com:0mu-Project/blog.git")


