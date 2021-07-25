# calvintwo3.py

import time
from selenium import webdriver
import smtplib
import ssl
import email
from email import encoders
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.message import MIMEMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import math

options = webdriver.ChromeOptions()
options.add_argument("--incognito")
# options.add_argument("--headless")
browser = webdriver.Chrome(
    "C:\\Users\\calvi\\Desktop\\calvintwo\\auto-insta-bot\\chromedriver.exe", options=options)
browser.set_window_size(1920, 1080)
browser.maximize_window()
browser.get("https://www.instagram.com")
time.sleep(5)


def login2():
    inputs = browser.find_elements_by_tag_name("input")
    inputs[0].send_keys("calv.zheng")
    inputs[1].send_keys("Iliketrains0")
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


def getFollowing():
    browser.get("https://www.instagram.com/calv.zheng/")
    numFollowing = int(browser.find_element_by_xpath(
        "/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span").text)
    time.sleep(3)

    browser.find_element_by_xpath(
        "/html/body/div[1]/section/main/div/header/section/ul/li[3]/a").click()
    time.sleep(5)

    fBody = browser.find_element_by_xpath("//div[@class='isgrP']")
    for i in range(math.floor(numFollowing/2)):
        browser.execute_script(
            'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
        time.sleep(0.25)
    fList = browser.find_elements_by_xpath("//div[@class='isgrP']//li")
    followingList = []
    for i in fList:
        followingList.append(i.text[:-10])
    print("getFollowing done")
    return followingList


def getFollowers():
    browser.get("https://www.instagram.com/calv.zheng/")
    numFollowers = int(browser.find_element_by_xpath(
        "/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span").text)
    time.sleep(3)

    browser.find_element_by_xpath(
        "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a").click()
    time.sleep(5)

    fBody = browser.find_element_by_xpath("//div[@class='isgrP']")
    for i in range(math.floor(numFollowers/2)):
        browser.execute_script(
            'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
        time.sleep(0.25)
    fList = browser.find_elements_by_xpath("//div[@class='isgrP']//li")
    followerList = []
    for i in fList:
        followerList.append(i.text[:-7])
    print("getFollowers done")
    return followerList


def getDiffs(followerList, followingList):
    diffList = []
    for a in followingList:
        if a not in followerList:
            diffList.append(a)
    print(diffList)


def send_mail(counter, usernameList):
    message = str(counter) + '\n' + '\n'.join(usernameList)
    subject = "calvintwo update"
    body = f"{message}"

    message = MIMEMultipart()
    message["From"] = "calvinzheng168@gmail.com"
    message["To"] = "calvinzllama@gmail.com"
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    text = message.as_string()

    # Log in to server using secure context and send email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login("calvinzheng168@gmail.com", "passwordPassword!")
        server.sendmail("calvinzllama@gmail.com",
                        "calvinzllama@gmail.com", text)


login2()
getDiffs(getFollowers(),getFollowing())

browser.quit()
