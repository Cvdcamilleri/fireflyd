#!/usr/bin/env python3
print('[ fireflyd_filesub copyright Charlie Camilleri 2019 ]')
print('[ fireflyd_filesub is licensed under GPLv3. ]')
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

cookies = ''
if __name__ == '__main__':
    from fireflyd_login import *
    print('FIREFLYD_FILESUB Self test')
    cooks_ = weblogin('wincoll.fireflycloud.net')
    print(cooks_)
    for cook in cooks_:
        cookies += str(cook['name'] + '=' + cook['value'] + '; ')

    print(cookies)
