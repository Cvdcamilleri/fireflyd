print('[ fireflyd_login copyright Charlie Camilleri 2019 ]')
print('[ fireflyd_login is licensed under GPLv3. Do not distribute! ]')
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def doweblogin(addr):
    print('[ fireflyd_login ] Presenting login window..')
    browser = webdriver.Chrome()
    browser.get(addr)
    try:
        element_present = EC.presence_of_element_located((By.ID, 'school-header'))
        WebDriverWait(browser, 600).until(element_present)
        print('[ fireflyd_login ] Logged in.. waiting for cookies')
    except TimeoutException:
        print('[ fireflyd_login ] User/page took too long!')
        browser.quit()
        exit(1)

    cookies = browser.get_cookies()
    print('[ fireflyd_login ] Got cookies, closing login window..')
    browser.quit()
    return cookies


def genloginaddr(base):
    return 'https://' + str(base) + '/login/login.aspx?prelogin=https%3a%2f%2f' + str(base) + '%2f'


def weblogin(base):
    cooks_ = doweblogin(genloginaddr(base))
    cookies___ = ''
    for cook in cooks_:
        cookies___ += str(cook['name'] + '=' + cook['value'] + '; ')

    return cookies___


cookies = ''
if __name__ == '__main__':
    print('FIREFLYD_LOGIN Self test')
    cooks_ = weblogin('wincoll.fireflycloud.net')
    for cook in cooks_:
        cookies += str(cook['name'] + '=' + cook['value'] + '; ')

    print(cookies)
