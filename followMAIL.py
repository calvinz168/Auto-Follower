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
    f = open("C:\\Users\\calvi\\Desktop\\calvintwo\\auto-insta-bot\\unfollowed.txt", "r")
    unfollowedList = (f.read().split("\n")[1:])
    print(unfollowedList)
    try:
        for i in range(length):
            time.sleep(0.1)
            username = browser.find_element_by_xpath(
                f"/html/body/div[1]/section/main/div/div[2]/div/div/div[{i+1}]/div[2]/div[1]/div/span/a").get_attribute("title")
            if username not in unfollowedList:
                followButton = browser.find_element_by_xpath(
                    f"/html/body/div[1]/section/main/div/div[2]/div/div/div[{i+1}]/div[3]/button")
                followButton.click()
                print(f"{i+1}", end=" ")
                time.sleep(0.1)
                counter += 1
                usernameList.append(username)
        send_mail(counter, usernameList, "FOLLOW")
    except:
        send_mail(counter, usernameList, "FOLLOW")


def unfollow(length):
    counter = 0
    unfollowList = getDiffs(getFollowers(), getFollowing())
    usernameList = []
    # unfollowList = []
    # print(unfollowList[0:100])
    try:
        for i in range(length):
            username = unfollowList[i].split("\n")[0]
            print(username)
            browser.get(f"https://www.instagram.com/{username}/")
            try:
                unfollowButton = browser.find_element_by_xpath(
                    "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button/div/span")
                unfollowButton.click()
                unfollowButton2 = browser.find_element_by_xpath(
                    "/html/body/div[5]/div/div/div/div[3]/button[1]")
                unfollowButton2.click()
                counter += 1
                writeFile(username)
                usernameList.append(username)
            except:
                pass
            time.sleep(1)
        send_mail(counter, usernameList, "UNFOLLOW")
    except:
        send_mail(counter, usernameList, "UNFOLLOW")


def getFollowing():
    browser.get("https://www.instagram.com/calv.zheng/")
    numFollowing = int(browser.find_element_by_xpath(
        "/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span").text.replace(",", ""))
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
        "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span").text.replace(",", ""))
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
    return diffList


def writeFile(usernameList):
    f = open("C:\\Users\\calvi\\Desktop\\calvintwo\\auto-insta-bot\\unfollowed.txt", "a")
    # usernameList = "\n" + "\n".join(usernameList)
    f.write(f"\n{usernameList}")
    f.close()


def send_mail(counter, usernameList, version):
    if version == "FOLLOW":
        message = str(counter) + '\n' + '\n'.join(usernameList)
        subject = "calvintwo follow update"
        body = f"{message}"
    elif version == "UNFOLLOW":
        message = str(counter) + '\n' + '\n'.join(usernameList)
        subject = "calvintwo unfollow update"
        body = f"{message}"

    message = MIMEMultipart()
    message["From"] = "email"
    message["To"] = "email"
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    text = message.as_string()

    # Log in to server using secure context and send email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login("email", "password")
        server.sendmail("email",
                        "email", text)


login()
seeAll()
follow(50)
unfollow(50)
browser.quit()
