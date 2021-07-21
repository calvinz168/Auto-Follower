# calvintwo3.py

import time
from selenium import webdriver
import smtplib

options = webdriver.ChromeOptions()
options.add_argument("--incognito")
# options.add_argument("--headless")
browser = webdriver.Chrome(
    "C:\\Users\\calvi\\Desktop\\calvintwo\\auto-insta-bot\\chromedriver.exe", options=options)
browser.set_window_size(1920, 1080)
browser.maximize_window()
browser.get("https://www.instagram.com")
time.sleep(5)


def login():
    inputs = browser.find_elements_by_tag_name("input")
    inputs[0].send_keys("username")
    inputs[1].send_keys("password")
    loginBut = browser.find_element_by_xpath(
        "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button/div")
    loginBut.click()
    while browser.current_url != "https://www.instagram.com/accounts/onetap/?next=%2F":
        time.sleep(1)
    not_now_button = browser.find_element_by_xpath(
        "/html/body/div[1]/section/main/div/div/div/div/button")
    not_now_button.click()
    time.sleep(3)
    not_now_button2 = browser.find_element_by_xpath(
        "/html/body/div[4]/div/div/div/div[3]/button[2]")
    not_now_button2.click()


def seeAll():
    time.sleep(3)
    seeAllButton = browser.find_element_by_xpath(
        "/html/body/div[1]/section/main/section/div[3]/div[2]/div[1]/a/div")
    seeAllButton.click()
    time.sleep(0.5)


def follow(length):
    counter = 0
    usernameList = []
    try:
        for i in range(length):
            time.sleep(0.1)
            username = browser.find_element_by_xpath(
                f"/html/body/div[1]/section/main/div/div[2]/div/div/div[{i+1}]/div[2]/div[1]/div/span/a").get_attribute("title")
            followButton = browser.find_element_by_xpath(
                f"/html/body/div[1]/section/main/div/div[2]/div/div/div[{i+1}]/div[3]/button")
            followButton.click()
            print(f"{i+1}", end=" ")
            browser.execute_script("window.scrollBy(0,75)", "")
            time.sleep(0.1)
            browser.execute_script("window.scrollBy(0,-75)", "")
            counter += 1
            usernameList.append(username)
        send_sms(counter, usernameList)
    except:
        send_sms(counter, usernameList)


def send_sms(counter, usernameList):
    message = str(counter) + '\n' + '\n'.join(usernameList)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    sender = 'email'
    passwd = 'password!'
    server.login(sender, passwd)

    recipient = "phone#@txt.freedommobile.ca"
    print(sender, recipient, message)
    server.sendmail(sender, recipient, message)


login()
seeAll()
follow(50)

browser.quit()
