#!/usr/bin/env python3

# fireflyd, Copyright Charlie Camilleri 2018

from fireflyd_lib import *
import up_cache

print("[ fireflyd copyright Charlie Camilleri 2019 ]")

print("[ logging in ]")
cookies = login(u(),p())
print("[ logged in ]")

tasks = get_tasks(cookies=cookies)
print("[ downloaded tasks ]")
