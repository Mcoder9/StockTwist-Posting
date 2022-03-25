from faker import Faker
from time import sleep
import json
import requests
import random
import pyperclip
import subprocess,os,sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
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
    s = Service(executable_path=main_directory + "/chromedriver.exe")
    driver = webdriver.Chrome(service=s,options=options)
    wait = WebDriverWait(driver, 60)
    return driver

driver = browserSetup(main_directory)

driver.get('https://stocktwits.com/')
input()