#!/usr/bin/env python3
import urllib.request, urllib.error, urllib.parse
import json,time,ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

global __cookies__
__cookies__ = ""

def gcookies():
	return __cookies__

def getcookies(handler):
	headers = (handler.info().__dict__['_headers'])
	for header in headers:
		if 'Set-Cookie' in header[0]:
				__cookies__ += header[1].split(" ")[0]+" "
				print("++COOKIE SET:",header[1].split(" ")[0]+" ")
	return gcookies()

def login(u,p,base):
        authdata = {
            "username": u,
            "password": p,
        }

        cookies = ""
        url = "https://"+base+"/login/login.aspx?prelogin=https%3a%2f%2f"+base+"%2f"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        req = urllib.request.Request(url,headers=headers)
        handler = urllib.request.urlopen(req, context=ctx)

        headers = (handler.info().__dict__['_headers'])
        for header in headers:
                if 'Set-Cookie' in header[0]:
                    cookies += header[1].split(" ")[0]+" "
                    print("++COOKIE SET:",header[1].split(" ")[0]+" ")

        url = "https://"+base+"/login/login.aspx?prelogin=https%3a%2f%2fwincoll.fireflycloud.net%2f&kr=Cloud:Cloud"
        headers = {
            "Host": base,
            "Connection": "keep-alive",
            "Content-Length": str(len(urllib.parse.urlencode(authdata))),
            "Cache-Control": "max-age=0",
            "Origin": "https://wincoll.fireflycloud.net",
            "Upgrade-Insecure-Requests": "1",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": 'Mozilla/5.0 ("Windows NT 10.0; Win64; x64") AppleWebKit/537.36 ("KHTML"," like Gecko") Chrome/71.0.3578.98 Safari/537.36',
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Referer": "https://wincoll.fireflycloud.net/login/login.aspx?prelogin=https%3a%2f%2fwincoll.fireflycloud.net%2f",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Cookie": cookies,
        }
        req = urllib.request.Request(url,urllib.parse.urlencode(authdata).encode("utf-8"),headers)


        try:
            handler = urllib.request.urlopen(req, context=ctx)
            headers = (handler.info().__dict__['_headers'])
            #print(headers)
            for header in headers:
                if 'Set-Cookie' in header[0]:
                    cookies += header[1].split(" ")[0]+" "
                    print("++COOKIE SET:",header[1].split(" ")[0]+" ")

            #print(cookies.replace(" ","\n"))
            #print("\nCookies setup complete!")
            __cookies__ = cookies
            return cookies
        except HTTPError as error:
            content = error.read().decode("utf-8")
            if "The details you entered were incorrect" in content:
                print("! User or password incorrent !")
            elif "Please complete the reCAPTCHA to log in" in content:
                print("! Cannot complete reCAPCHA, login in a normal web browser and then try again !")
                print("Follow this link to login in normally: https://wincoll.fireflycloud.net/Login/")
            else:
                print("An unexpected error has occured! Please try again")
            return ""


def get_tasks(cookies="",ownerType="OnlySetters",archiveStatus="All",completionStatus="AllIncludingArchived",readStatus="All",markingStatus="All",sorting={"column":"DueDate","order":"Ascending"},page=1,base=None):
        if base==None:
         return False
        data = {
            "ownerType":ownerType,
            "page":page,
            "pageSize":10,
            "archiveStatus":archiveStatus,
            "completionStatus":completionStatus,
            "readStatus":readStatus,
            "markingStatus":markingStatus,
            "sortingCriteria":[{
                "column":sorting["column"],
                "order":sorting["order"]
            }]
        }
        data = str(json.dumps(data))
        headers = {
            "Referer": "https://"+base+"/set-tasks",
            "Host": base,
            "Cookie": cookies,
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://"+base,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "DNT": "1",
            "Content-Type": "application/json",
            "Content-Length": str(len(data)),
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate, br",
            "Accpet-Language": "en-US,en;q=0.9,ru;q=0.8",
        }

        url = "https://"+base+"/api/v2/taskListing/view/self/tasks/filterBy"
        req = urllib.request.Request(url,data.encode("utf-8"),headers)

        handler = urllib.request.urlopen(req, context=ctx)
        getcookies(handler)
        json_tasks = json.loads(handler.read().decode("utf8"))
        return {"list":json_tasks["items"],"total count":json_tasks["totalCount"]}
#{
#  "recipient":{
#    "type": "user",
#    "guid": "DB:Cloud:DB:SIMSstu:18526"
#  },
#  "event": {
#    "type": "mark-as-done",
#    "feedback": "",
#    "sent": "2019-09-12T07:30:39.670Z",
#    "author": "DB:Cloud:DB:SIMSstu:18526"
#  }
#}
def feedback(base="wincoll.fireflycloud.net",cookies="",task=None,done=True,iscomment=False,comment=""):
        if done and not iscomment:
           eventype="mark-as-done"
        elif not done and not iscomment:
           eventype="mark-as-undone"
        elif iscomment:
           eventype="comment"
        else:
           eventype="mark-as-done"

        if base==None:
           return '{"error":"incorrect \'base\' parameter"}'
        if task==None:
           return '{"error":"incorrect \'task\' parameter"}'
        if cookies==None:
           return '{"error":"incorrect \'cookies\' parameter"}'

        guid = task['student']['guid']
        author = task['setter']['guid']
        sendtime = str( time.strftime("%Y-%m-%dT%H:%M:%S.000Z")  )
        print("MARK STUDENT GUID="+guid+"  SETTER GUID="+author+"  TIMESTAMP="+sendtime)
        if eventype!="comment":
         data = {
                  "recipient": {
                    "type": "user",
                    "guid": guid
                  },
                  "event": {
                    "type": eventype,
                    "feedback": "",
                    "sent": str(sendtime),
                    "author": author,
                  }
                }
         data = str(json.dumps(data)).replace(" ","")
        else:
         data = {
                  "recipient": {
                    "type": "user",
                    "guid": guid
                  },
                  "event": {
                    "type": eventype,
                    "message":comment,
                    "feedback": "",
                    "sent": str(sendtime),
                    "author": author,
                  }
                }
         data = str(json.dumps(data))
        #data = str(json.dumps(data)).replace(" ","")
        data = "data="+urllib.parse.quote_plus(data)
        print("DATA: ",data)
        extracookies = "" #"FireflyNETLoggedIn=yes; Prelogin=https://wincoll.fireflycloud.net/;"
        headers = {
            "Host": base,
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0",
            "Accept": "*/*",
            "Accept-Language":"en-GB,en;q=0.5",
            "Accept-Encoding":"gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With":"XMLHttpRequest",
            "Content-Length": str(len(data)),
            "Connection":"keep-alive",
            "Referer":"https://"+base+"/set-tasks/"+str(task['id']),
            "Cookie":str(cookies+extracookies)
        }

        url = "https://"+base+"/_api/1.0/tasks/"+str(task['id'])+"/responses"
        req = urllib.request.Request(url,data.encode("ascii"),headers)

        try:
         handler = urllib.request.urlopen(req, context=ctx)
        except urllib.error.HTTPError as e:
          with open("error.htm", "wb") as f:
           f.write(e.fp.read())
          return "{\"error\":\"HTTPError "+str(e.code)+"\"}"
        #json_tasks = json.loads(handler.read().decode("utf8"))
        return handler.read().decode()

## NOT SUPPORTED. USE AT YOUR OWN RISK
## TODO make this work
def sendfile(base="wincoll.fireflycloud.net",cookies="",task=None):
        if base==None or cookies=="" or task==None:
           return '{"error":"incorrect parameter"}'
        guid = task['student']['guid']
        author = task['setter']['guid']
        sendtime = str( time.strftime("%Y-%m-%dT%H:%M:%S.000Z")  )
        print("STUDENT GUID="+guid+"  SETTER GUID="+author+"  TIMESTAMP="+sendtime)
        data = """-----------------------------9430462821759297635809569235
Content-Disposition: form-data; name="fileAction"

KEEPBOTH
-----------------------------9430462821759297635809569235
Content-Disposition: form-data; name="test file"; filename="testfile.txt"
Content-Type: application/octet-stream

<TEST DATA>

-----------------------------9430462821759297635809569235--
"""
        #data = str(json.dumps(data)).replace(" ","")
        #data = "data="+urllib.parse.quote_plus(data)
        #print("DATA: ",data)
        extracookies = "" #"FireflyNETLoggedIn=yes; Prelogin=https://wincoll.fireflycloud.net/;"
        headers = {
            "Host": base,
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0",
            "Accept": "*/*",
            "Accept-Language":"en-GB,en;q=0.5",
            "Accept-Encoding":"gzip, deflate, br",
            "Content-Type": "multipart/form-data; boundary=---------------------------9430462821759297635809569235",
            "Content-Length": str(len(data)),
            "Connection":"keep-alive",
            "Referer":"https://"+base+"/set-tasks/"+str(task['id']),
            "Cookie":str(cookies+extracookies)
        }
        folderid="90034"
        url = "https://"+base+"/folders/"+folderid+"/files"
        req = urllib.request.Request(url,data.encode("ascii"),headers)

        try:
         handler = urllib.request.urlopen(req, context=ctx)
        except urllib.error.HTTPError as e:
          with open("error.htm", "wb") as f:
           f.write(e.fp.read())
          return "{\"error\":\"HTTPError\"}"
        #json_tasks = json.loads(handler.read().decode("utf8"))
        return handler.read().decode()

if __name__ == "__main__":
	print("this is a library")

print("[ fireflyd_lib copyright Charlie Camilleri 2019 ]")
