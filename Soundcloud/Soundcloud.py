import time
import requests
import os
import csv
import json
from bs4 import BeautifulSoup
import smtplib, ssl

# Import selenium reqs
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import re
import traceback
import sys
import datetime
class Soundcloud:
    '''
    Initialize necessary variables
    This one works for the non-public profiles
    Requires login
    '''
    def __init__(self, ):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        self.driver = Chrome(options=chrome_options)

        # self.driver = webdriver.Chrome()
        # self.driver.maximize_window()

    # Goto public profile
    def gotoPodcast(self, url):
        driver = self.driver
        driver.get(url)
        print("Entering Podcast ...")
        time.sleep(2)

    # Send email
    def sendemail(self,msg):
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = ""  # Enter your address
        receiver_email = ''       
        password = input("Type your password and press enter: ")
        message = "Subject: SoundCloud Stats\n\nThis message is sent from Yong.\n"
        for i in msg:
            message+=i
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
    def getcracking(self,urls):
        msgarray = []
        for url in urls:
            self.gotoPodcast(url)
            msgarray.append(self.getDetails())
            time.sleep(1)
        self.sendemail(msgarray)

    def getDetails(self):
        driver = self.driver
        # Scroll to bottom to load the page fully
        # self.scrollToBottom()
        self.scrollToN(1)
        # print("Episodes found...")
        articles = driver.find_elements_by_xpath(".//div[@class='userStreamItem']")
        # print(len(articles))
        data=[]
        details = ""
        count=1
        for article in articles:
            description =article.find_element_by_xpath(".//div[@class='sound streamContext']").get_attribute('aria-label')
            reaction = int(article.find_element_by_xpath(".//span[@class='sc-ministats sc-ministats-small sc-ministats-plays']/span[@aria-hidden='true']").text)
            details+= "View Count: "+ str(reaction).zfill(2) +" [" + description + "]\n"
            data.append([count,description,reaction])
            count+=1
        currentDT = datetime.datetime.now()
        details+=("Total Count: " +str(sum([i[2] for i in data])) +" [On " + str(currentDT) + "]\n")
        # print(details)
        return details

    def scrollToN(self, n_scrolls):
        # Time to pause for the page to load
        SCROLL_PAUSE_TIME = 5

        driver = self.driver
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight;")

        for i in range(n_scrolls):
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight;")
            if new_height == last_height:
                break
            last_height = new_height

    def scrollToBottom(self):
        # Time to pause for the page to load
        SCROLL_PAUSE_TIME = 2

        driver = self.driver
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight;")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight;")
            if new_height == last_height:
                break
            last_height = new_height

    def quitBrowser(self):
        driver = self.driver
        driver.quit()

soundcloud = Soundcloud()
soundcloud.getcracking(['https://soundcloud.com/xl-podcast','https://soundcloud.com/schoolofthefuture'])


