#!/usr/bin/env python3
# fireflyd, Copyright Charlie Camilleri 2018

from fireflyd_lib import *
from getpass import *
#from up_cache import u,p # file contains username/password for easier development. WILL CHANGE LATER
#yeet i've just done it

def u():
	return input("Username: ")
def p():
	return getpass()

mcookie = ""
mcookieused = False

import sys
if len(sys.argv) > 1:
	if sys.argv[1] == "-m":
		print("[ starting in manual cookies mode ]")
		print("[ paste your cookie string here   ]")
		mcookie = input()
		mcookieused = True

extcookies=mcookieused

base_url = "wincoll.fireflycloud.net" # base firefly url -- not including http/https

print("[ fireflyd copyright Charlie Camilleri 2019 ]")

global _done
global _todo
global __tasks
global _cookies

_done="<none>"
_todo="<none>"

__tasks = []
_cookies="<none>"

def refresh():
	if not mcookieused:
		print("[ logging in ]")
		cookies = login(u(),p(),base_url)
	elif mcookieused:
		print("[ cookes pasted ]")
		cookies = mcookie
	print("[ logged in ]")
	_cookies = cookies
	tasks = []

	print("[ downloading tasks ]")
	pages=1
	while True:
		_tasks = get_tasks(cookies=cookies,page=pages,base=base_url)
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

	_todo = json.dumps(todo)
	_done = json.dumps(done)
	_cookies = cookies

	print(cookies)
	return _todo,_done,_cookies


def get_task(tid):
	for task in __tasks:
		if str(task['id']) == str(tid):
			return str(task)
	return "{ 'error':'not found' }"

_todo, _done, _cookies = refresh() # Initial refresh

print(gcookies())

print("[ starting webserver ]")

from flask import Flask
app = Flask(__name__)

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

@app.route("/tasks/<tid>")
def web_disp_task(tid):
	return get_task(int(tid))

@app.route("/tasks/<tid>/markdone")
def web_mark_done(tid):
	if extcookies:
		task_ = get_task(int(tid)).replace("\'","\"").replace("None","\"None\"").replace("False","\"False\"").replace("True","\"True\"").replace(" ","")
		task_ = json.loads(task_)
		return markasdone(cookies=_cookies,base=base_url,task=task_)
	else:
		return '{"error":"not supported with generated cookies. try again having used the -m argument"}'

@app.route("/tasks/<tid>/marktodo")
def web_mark_undone(tid):
	if extcookies:
		task_ = get_task(int(tid)).replace("\'","\"").replace("None","\"None\"").replace("False","\"False\"").replace("True","\"True\"").replace(" ","")
		task_ = json.loads(task_)
		return markasdone(cookies=_cookies,base=base_url,task=task_,done=False)
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

app.run()

#END SIGNED CODE#
#END#
