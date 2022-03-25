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


def signupInfo():
    driver.get("https://temp-mail.org/en/")
    driver.find_element(By.CSS_SELECTOR, 'button.click-to-delete').click()
    copybutton = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "form>div:last-of-type>button.click-to-copy.copyIconGreenBtn")))
    copybutton.click()
    # driver.find_element(By.CSS_SELECTOR, "form>div:last-of-type>button.click-to-copy.copyIconGreenBtn").click()
    email = pyperclip.paste()
    name = Faker().name()
    username = Faker().name().replace(' ', str(random.randint(1,500))).replace('.','_')
    password = Faker().name().replace(' ', str(random.randint(1,500))).replace('.','_')[:10]
    return {'Name':name, "Email":email, "Username":username, "Password":password}

def signup(data):
    driver.switch_to.window(driver.window_handles[1])
    driver.get("https://stocktwits.com/")
    driver.find_element(By.XPATH, '(//nav//button)[2]').click(), sleep(2) # signup-button
    driver.find_element(By.XPATH, '//input[@name="name"]').send_keys(data['Name']), sleep(2)
    driver.find_element(By.XPATH, '//input[@name="email"]').send_keys(data['Email']), sleep(2)
    driver.find_element(By.XPATH, '//input[@name="login"]').send_keys(data["Username"]), sleep(2)
    driver.find_element(By.XPATH, '//input[@name="password"]').send_keys(data['Password']), sleep(2)
    while True:
        status = driver.find_element(By.CSS_SELECTOR, 'div.antigate_solver').get_attribute('class')
        if 'solved' in status.lower():
            break
        if 'error' in status.lower():
            signup(data)
        else:
            sleep(1)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click(), sleep(2) # submit
    try:driver.find_element(By.XPATH, '//button[@type="submit"]').click() # Build watchlist
    except: pass

def emailVerification():
    driver.switch_to.window(driver.window_handles[0])
    while True:
        try:
            driver.find_element(By.XPATH, '//span[@class="inboxSubject subject-title"]/a[contains(@href,"temp-mail.org")]').get_attribute('href')
            break
        except: sleep(1)
    mailSourceLink = driver.find_element(By.XPATH, '//span[@class="inboxSubject subject-title"]/a[contains(@href,"temp-mail.org")]').get_attribute('href')
    driver.get(mailSourceLink)
    verificationLink = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="inbox-data-content-intro"]//a[contains(@href,"verify?token=")]'))).get_attribute('href')
    # verificationLink = driver.find_element(By.XPATH, '//div[@class="inbox-data-content-intro"]//a[contains(@href,"verify?token=")]').get_attribute('href')
    driver.get(verificationLink)

def saveLoginToText(data):
    with open('Accounts.json') as f:
        savedData = json.load(f)
    with open('Accounts.json','w') as f:
        savedData[str(len(savedData)+1)] = data
        updatedData = savedData
        json.dump(updatedData,f,indent=4)

def Saaf_Saman():
    driver.get('chrome://settings/clearBrowserData')
    clear_button = "document.querySelector('settings-ui').shadowRoot.querySelector('settings-main').shadowRoot.querySelector('settings-basic-page').shadowRoot.querySelector('settings-section>settings-privacy-page').shadowRoot.querySelector('settings-clear-browsing-data-dialog').shadowRoot.querySelector('cr-dialog>div>cr-button#clearBrowsingDataConfirm').click();"
    sleep(1)
    driver.execute_script(clear_button)

def close_free_tabs():
    tabs = driver.window_handles
    current_tab = driver.current_window_handle
    for tab in tabs:
        driver.switch_to.window(tab)
        if tab == current_tab:
            continue
        else:
            driver.close()
    driver.switch_to.window(current_tab)


if __name__ == '__main__':
    main_directory = os.getcwd()
    driver = browserSetup(main_directory)
    for _ in range(500):
        try:
            data = signupInfo()
            driver.execute_script("window.open('');")
            signup(data)
            emailVerification()
            saveLoginToText(data)
            Saaf_Saman()
            close_free_tabs()
        except:
            Saaf_Saman()
            close_free_tabs()

            