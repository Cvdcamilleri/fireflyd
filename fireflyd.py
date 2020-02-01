#!/usr/bin/env python3
# fireflyd, Copyright Charlie Camilleri 2018

import urllib.request, urllib.error, urllib.parse
from fireflyd_lib import *
from fireflyd_login import *
from getpass import *
import argparse,base64,hmac,hashlib,os
#from up_cache import u,p # file contains username/password for easier development. WILL CHANGE LATER
#yeet i've just done it

def u():
	return input("Username: ")
def p():
	return getpass()

mcookie = ""
mcookieused = False

basicauth=False
usehmac = False

ap = argparse.ArgumentParser()
ap.add_argument("-m", "--manual", required=False, help="Use custom cookes", action='store_true')
ap.add_argument("-hm", "--hmac", required=False, help="Use HMAC for the HTTP API", action='store_true')
args = vars(ap.parse_args())

if args['hmac']:
	usehmac = True

import sys
if args['manual']:
	print("[ starting in manual cookies mode ]")
	print("[ paste your cookie string here   ]")
	mcookie = input()
	mcookieused = True

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

extcookies=mcookieused

base_url = "wincoll.fireflycloud.net" # base firefly url -- not including http/https

print("[ fireflyd copyright Charlie Camilleri 2019 ]")

#_done
#_todo
global __tasks
#global _cookies

_done=[]
_todo=[]

__tasks = []
_cookies=[]
cookies =[]

if not mcookieused:
 print("[ logging in ]")
 _cookies = weblogin(base_url)
elif mcookieused:
 print("[ cookes pasted ]")
 _cookies = mcookie
else:
 _cookies="NOSET"

def refresh():
	global _todo
	global _done
	#if not mcookieused:
	#	print("[ logging in ]")
	#	cookies = weblogin(base_url)
	#elif mcookieused:
	#	print("[ cookes pasted ]")
	#	cookies = mcookie
	print("[ logged in ]")
	#cookies = _cookies
	#_cookies = cookies
	tasks = []
	print(_cookies)
	print("[ downloading tasks ]")
	pages=1
	while True:
		_tasks = get_tasks(cookies=_cookies,page=pages,base=base_url)
		print("[ downloaded page",pages,", of length",len(_tasks['list'])," ]\t\t",end="\r")
		if ( len(_tasks['list']) == 0 ):
			break
		tasks.append(_tasks)
		pages=pages+1
	print("")

	pages=pages-1
	todo = []
	done = []

	for i in range(pages):
		for task in tasks[i]['list']:
			print("[ processing task",task['id']," : ",task['dueDate'],"]\t\t",end="\r")
			__tasks.append(task)
			if task['isDone']:
				done.append(task)
			else:
				todo.append(task)
	print("")

	#_todo = json.dumps(todo)
	#_done = json.dumps(done)
	_todo = todo
	_done = done
	#_cookies = cookies

	print(_cookies)
	return _todo,_done

def get_task(tid):
	for task in __tasks:
		if str(task['id']) == str(tid):
			return task
	return "{ 'error':'not found' }"

def getindex(tid,ta):
	___c=0
	for task in ta:
		if str(task['id']) == str(tid):
			return c
		c+=1
	return 0xffffffff

_todo, _done = refresh() # Initial refresh

print(gcookies())

print("*****************************")
print("Done LEN=",len(_done))
print("Todo LEN=",len(_todo))
print("*****************************")

#print("[ development mode, no webserver ]")
#exit(0)

print("[ starting webserver ]")

from flask import Flask,request
app = Flask(__name__)

hmac_key = "t35t hm4c k3y"
def computehmac(data,mac=None):
	data = data.encode()
	key = hmac_key.encode()
	if usehmac:
		return hmac.new(key, data, hashlib.sha512).hexdigest()
	else:
		return mac

extcookies=True

@app.route("/")
def web_index():
	return "fireflyd copyright Charlie Camilleri 2019"

@app.route("/tasks/todo")
def web_todo():
	return str(_todo)

@app.route("/tasks/done")
def web_done():
	return str(_done)

@app.route("/refresh")
def web_refresh():
	_todo,_done = refresh()
	return "done"

@app.route("/<hmac>/tasks/<tid>")
def web_disp_task(hmac,tid):
	if hmac != computehmac(tid) and usehmac:
                print("BAD HMAC, EXPECTED ",computehmac(tid,mac=hmac))
                return '{"error":"invalid MAC"}'
	return get_task(int(tid))

@app.route("/<hmac>/tasks/<tid>/markdone")
def web_mark_done(hmac,tid):
	global _todo
	global _done
	if hmac != computehmac(tid) and usehmac:
		print("BAD HMAC, EXPECTED ",computehmac(tid,mac=hmac))
		return '{"error":"invalid MAC"}'
	if extcookies:
		task_ = get_task(int(tid))
		print(_todo[len(_todo)-1])
		print(task_)
		_todo.remove(task_)
		#task_ = json.loads(task_)
		fb=feedback(cookies=_cookies,base=base_url,task=task_)
		_done.append(task_)
		return fb
	else:
		return '{"error":"not supported with generated cookies. try again having used the -m argument"}'

@app.route("/<hmac>/tasks/<tid>/marktodo")
def web_mark_undone(hmac,tid):
	global _todo
	global _done
	if hmac != computehmac(tid) and usehmac:
                print("BAD HMAC, EXPECTED ",computehmac(tid,mac=hmac))
                return '{"error":"invalid MAC"}'
	if extcookies:
		task_ = get_task(int(tid))
		print(_done[len(_done)-1])
		print(task_)
		_done.remove(task_)
		#task_ = json.loads(task_)
		fb= feedback(cookies=_cookies,base=base_url,task=task_,done=False)
		_todo.append(task_)
		return fb
	else:
		return '{"error":"not supported with generated cookies. try again having used the -m argument"}'

@app.route("/<hmac>/tasks/<tid>/comment")
def web_comment(tid):
	if hmac != computehmac(request.args['b64']) and usehmac:
                print("BAD HMAC, EXPECTED ",computehmac(request.args['b64'],mac=hmac))
                return '{"error":"invalid MAC"}'
	if extcookies:
		b64txt = urllib.parse.unquote_plus(request.args['b64'])
		task_ = get_task(int(tid))
		#task_ = json.loads(task_)
		return feedback(cookies=_cookies,base=base_url,task=task_,iscomment=True,comment=base64.b64decode(b64txt).decode())
	else:
		return '{"error":"not supported with generated cookies. try again having used the -m argument"}'

@app.route("/cookies")
def web_cookie_dump():
	return _cookies.replace(";",";<br>\n")

@app.route("/sendfile")
def send_file():
	#tid = 23770
	#task_ = get_task(int(tid)).replace("\'","\"").replace("None","\"None\"").replace("False","\"False\"").replace("True","\"True\"").replace(" ","")
	#task_ = json.loads(task_)
	#return sendfile(cookies=_cookies,base=base_url,task=task_)
	return '{"error":"not supported. check https://github.com/cvdcamilleri/fireflyd for more info"}'

#@auth.verify_password
#def verify_password(username, password):
#    if username in users:
#        return check_password_hash(users.get(username), password)
#    return False

#from flask_httpauth import HTTPBasicAuth
#auth = HTTPBasicAuth()

#web_mark_undone("nohash","25776")
#web_mark_done("nohash","25776")
#web_mark_undone("nohash","25776")

if not basicauth:
	app.run(ssl_context=('ssl/cert.pem', 'ssl/key.pem'))
elif basicauth:
	print("! HTTP Basic not yet supported !")
	exit(0xFF)


#END SIGNED CODE#
#END#
