import requests

from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import subprocess,os
main_directory = os.getcwd()
def browserSetup(main_directory):
    subprocess.Popen(
        ["start","chrome","--remote-debugging-port=8989","--user-data-dir=" + main_directory + "/chrome_profile",],shell=True
                        )
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--disable-infobars")
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("debuggerAddress", "localhost:8989")
    driver = webdriver.Chrome(executable_path='chromedriver.exe',options=options)
    return driver


chrome_options = Options()
driver = browserSetup(main_directory)

with open('usernames.txt') as file:
    usernames = file.readlines()

for x in usernames:
    url = f'https://stocktwits.com/{x}'
    driver.get(url)
    time.sleep(2)
    try: post = driver.find_element(By.XPATH, '//a[contains(text(),"xtrades.io")]')
    except: post = None
    if post:
        print(f'{x.strip()} is valid username')
        with open('validUsers.txt','a') as file:
            file.write(url)
