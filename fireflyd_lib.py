import urllib.request
import json

def login(u,p):
        authdata = {
            "username": u,
            "password": p,
        }

        cookies = ""
        url = "https://wincoll.fireflycloud.net/login/login.aspx?prelogin=https%3a%2f%2fwincoll.fireflycloud.net%2f"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        req = urllib.request.Request(url,headers=headers)
        handler = urllib.request.urlopen(req)

        headers = (handler.info().__dict__['_headers'])
        for header in headers:
                if 'Set-Cookie' in header[0]:
                    cookies += header[1].split(" ")[0]+" "

        url = "https://wincoll.fireflycloud.net/login/login.aspx?prelogin=https%3a%2f%2fwincoll.fireflycloud.net%2f&kr=Cloud:Cloud"
        headers = {
            "Host": "wincoll.fireflycloud.net",
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
            handler = urllib.request.urlopen(req)
            headers = (handler.info().__dict__['_headers'])
            #print(headers)
            for header in headers:
                if 'Set-Cookie' in header[0]:
                    cookies += header[1].split(" ")[0]+" "

            #print(cookies.replace(" ","\n"))
            #print("\nCookies setup complete!")
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


def get_tasks(cookies="",ownerType="OnlySetters",archiveStatus="All",completionStatus="AllIncludingArchived",readStatus="All",markingStatus="All",sorting={"column":"DueDate","order":"Ascending"},page=1):
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
            "Referer": "https://wincoll.fireflycloud.net/set-tasks",
            "Host": "wincoll.fireflycloud.net",
            "Cookie": cookies,
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://wincoll.fireflycloud.net",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "DNT": "1",
            "Content-Type": "application/json",
            "Content-Length": str(len(data)),
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate, br",
            "Accpet-Language": "en-US,en;q=0.9,ru;q=0.8",
        }

        url = "https://wincoll.fireflycloud.net/api/v2/taskListing/view/self/tasks/filterBy"
        req = urllib.request.Request(url,data.encode("utf-8"),headers)

        handler = urllib.request.urlopen(req)
        json_toytimes = json.loads(handler.read().decode("utf8"))
        return {"list":json_toytimes["items"],"total count":json_toytimes["totalCount"]}


print("[ fireflyd_lib copyright Charlie Camilleri 2019 ]")
