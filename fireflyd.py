#!/usr/bin/env python3

# fireflyd, Copyright Charlie Camilleri 2018

''' TOYTIME example
{
"id":1989,
"title":"Problems as detailed on the sheet given out up to books",
"setter":{"guid":"DB:Cloud:DB:SIMSemp:227","name":"Mr T Ayres","deleted":false},
"addressees":[{"guid":"DB:Cloud:DB:SIMS:15406","name":"Class 1P8","isGroup":true}],
"setDate":"2018-09-04",
"dueDate":"2018-09-05",
"student":{"guid":"DB:Cloud:DB:SIMSstu:18145","name":"Gleb Koval","deleted":false},
"mark":{"isMarked":false,"grade":null,"mark":null,"markMax":null,"hasFeedback":false},
"isPersonalTask":false,
"isExcused":false,
"isDone":true,
"isResubmissionRequired":false,
"lastMarkedAsDoneBy":{"guid":"DB:Cloud:DB:SIMSstu:18145","name":"Gleb Koval","deleted":false},
"archived":false,
"isUnread":false,
"fileSubmissionRequired":false,
"hasFileSubmission":false,
"descriptionContainsQuestions":false}
'''
####SIGNATURE CHECK CODE####

'''#correct hash
import base64
__hash = b'z4PhNX7vuL3xVChQ1m2AB9Yg5AULVxXcg/SpIdNs6c5H0NE8XYXysP+DGNKHfuwvY7kxvUdBeoGlODJ6+SfaPg=='
__hash = base64.b64encode(__hash).decode()

def check():
	import sys,hashlib,base64
	file = sys.argv[0]

	with open(file,'r') as f:
		dat = f.read().split(str("#START"+"#"))[1].split(str("#END"+"#"))[0]

	m = hashlib.sha512()
	hash = m.digest()
	print("[sigcheck] SHA512:",base64.b64encode(hash).decode())
	if hash != __hash:
		print("[sigcheck] ERROR! hash not valid")
		exit(0xFF)

check() # check signature

''' ############################

#START#

from fireflyd_lib import *
from up_cache import u,p # file contains username/password for easier development. WILL CHANGE LATER

base_url = "wincoll.fireflycloud.net" # base firefly url -- not including http/https

print("[ fireflyd copyright Charlie Camilleri 2019 ]")

global _done
global _todo
global __tasks
global _cookies

_done="<none>"
_todo="<none>"

__tasks = []

def refresh():
	print("[ logging in ]")
	cookies = login(u(),p(),base_url)
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

	return _todo,_done

def get_task(tid):
	for task in __tasks:
		if str(task['id']) == str(tid):
			return str(task)
	return "{ 'error':'not found' }"

_todo, _done = refresh() # Initial refresh

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

app.run()

#END SIGNED CODE#
#END#
