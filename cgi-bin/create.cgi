#!/usr/bin/python3

import cgitb
cgitb.enable()

import cgi

form = cgi.FieldStorage()
argment = form.getvalue('content')
filen = form.getfirst('title')
f = open('_posts/'+ filen  +'.markdown', 'w', encoding = 'UTF-8') 
f.write(argment)
f.close()

print 


