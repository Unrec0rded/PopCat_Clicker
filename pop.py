from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
import time

path_to_chromedriver = 'chromedriver'
service = Service(path_to_chromedriver)
options = webdriver.ChromeOptions()
path_to_chrome_binary = '/var/lib/flatpak/exports/bin/com.google.Chrome'
options.binary_location = path_to_chrome_binary

options.add_argument("--remote-debugging-port=6969")
options.add_argument("--disable-dev-shm-using") 
options.add_argument("--disable-extensions") 
options.add_argument("--disable-gpu") 
# options.add_argument("start-maximized") 
options.add_argument("disable-infobars")
driver = webdriver.Chrome(service=service, options=options)

driver.get('https://popcat.click')
driver.implicitly_wait(10)

POP = 0 #CLICK COUNTER

CLICK = 10 #MAX is 800 every 30 second | more than 800 detected as BOT
CLICK_SPEED = 0.005 #Smaller is faster
SLEEP = 30 #SLEEP after CLICK reach 800 to prevent BOT detection | Min sleep is 30s
GOAL = 20 #GOAL POP to achieve before STOP/break the program

def pop():
    global POP

    body = driver.find_element(By.TAG_NAME, 'body')
    for e in range(int(CLICK/2)):
        time.sleep(CLICK_SPEED)
        body.send_keys(Keys.CONTROL, 'g')
        POP+=2
        print(POP)
        if POP >= GOAL:
            save_cookie()
            break


# Set cookie 'country' and cookie expire, to prevent detected as BOT
# def set_cookie():
#     driver.execute_script('document.cookie = "country=SG; expires=Sat, 10 JUN 2023 12:00:00 UTC; path=/"')

# Save cookie to JSON
def save_cookie():
    cookies = driver.get_cookies()
    with open('cookie.json', 'w') as f:
        json.dump(cookies, f)

# Load cookie from JSON
def load_cookie():
    try:
        with open('cookie.json', 'r') as f:
            cookies = json.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)
    except FileNotFoundError:
        # set_cookie() #Undisable it if you want to use expired cookie
        save_cookie()

load_cookie()
time.sleep(5)
driver.get('https://popcat.click')
driver.implicitly_wait(10)
# Loop click every 30 second
while True:
    pop()
    # if POP >= GOAL:
    #     save_cookie()
    #     break
    time.sleep(SLEEP)


driver.close()
driver.quit()
