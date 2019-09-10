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

from fireflyd_lib import *
from up_cache import u,p # file contains username/password for easier development. WILL CHANGE LATER

print("[ fireflyd copyright Charlie Camilleri 2019 ]")

def refresh():
	print("[ logging in ]")
	cookies = login(u(),p())
	print("[ logged in ]")

	tasks = []

	print("[ downloading tasks ]")
	pages=1
	while True:
		_tasks = get_tasks(cookies=cookies,page=pages)
		print("[ downloaded page",pages,", of length",len(_tasks['list'])," ]")
		if ( len(_tasks['list']) == 0 ):
			break
		tasks.append(_tasks)
		pages=pages+1

	pages=pages-1
	todo = []
	done = []

	for i in range(pages):
		for task in tasks[i]['list']:
			print("[ processing task",task['id']," : ",task['title']," : ",task['dueDate'],"]")
			if task['isDone']:
				done.append(task)
			else:
				todo.append(task)

	_todo = json.dumps(todo)
	_done = json.dumps(done)

refresh() # Initial refresh

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
	refresh()
	return "done"

app.run()


