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
            # browser.execute_script("window.scrollBy(0,75)", "")
            time.sleep(0.1)
            # browser.execute_script("window.scrollBy(0,-75)", "")
            counter += 1
            usernameList.append(username)
        send_mail(counter, usernameList)
    except:
        send_mail(counter, usernameList)


def send_mail(counter, usernameList):
    message = str(counter) + '\n' + '\n'.join(usernameList)
    subject = "calvintwo update"
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

browser.quit()
