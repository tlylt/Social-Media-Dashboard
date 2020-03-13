import time
import requests
import os
import csv
import json
from bs4 import BeautifulSoup

# Import selenium reqs
from selenium import webdriver
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

class Linkedin:
    '''
    Initialize necessary variables
    This one works for the non-public profiles
    Requires login
    '''
    def __init__(self, ):
        # options = webdriver.ChromeOptions()
        # Replace the dir with the profile of your google chrome
        # To do this, goto google-chrome, and type: chrome://version, and get the profile path
        # Also make sure to clear all caches before starting
        # options.add_argument('user-data-dir=/home/dipes/.config/google-chrome/Profile')
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.email = 'your email'
        self.password = 'yourpassword'

    def login(self):
        driver = self.driver
        url = 'https://www.linkedin.com/'
        try:
            driver.get(url)
            emailFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_name('session_key') )
            passwordFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_name('session_password')) 
            loginbutton = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_class_name('sign-in-form__submit-btn'))
        except Exception as e:
            print(e)
            print('Error in elements for login...')
        else:
            emailFieldElement.send_keys(self.email)
            time.sleep(2)
            passwordFieldElement.send_keys(self.password)
            time.sleep(2)
            loginbutton.click()
            print('Logging in...')
            time.sleep(3)

    # Goto public profile
    def gotoProfile(self, url):
        driver = self.driver
        driver.get(url)
        print("Entering profile ...")
        time.sleep(8)

    # Get posts
    def getPosts(self):
        driver = self.driver
        # Scroll to bottom to load the page fully
        # self.scrollToBottom()
        self.scrollToN(5)
        time.sleep(5)
        print("Posts found...")
        # print(posts_div)
        articles = driver.find_elements_by_xpath(".//div[@class='occludable-update ember-view']")
        print(len(articles))
        data=[]
        count=1
        for article in articles:
            description =article.find_element_by_xpath(".//div[@dir='ltr']").text
            reaction = int(article.find_element_by_xpath(".//span[@class='v-align-middle social-details-social-counts__reactions-count']").text)
            ago = article.find_element_by_xpath(".//div[@class='feed-shared-text-view white-space-pre-wrap break-words ember-view']").text
            #get just the ago
            ago = ago.split()[0]
            try:
                comment = article.find_element_by_xpath(".//button[@data-control-name='comments_count']").text
                #get integer
                comment = int(comment.split()[0])
            except Exception as e:
                print("no comments")
                comment = 0
            # print(description, reaction, comment,ago)
            total = reaction+comment
            data.append([count,description,reaction,comment,total,ago])
            count+=1
            time.sleep(0.5)
        with open('07_03_pikkal.csv', mode='w',encoding="utf-8") as linkedin_file:
            linkedin_writer = csv.writer(linkedin_file, delimiter=',',  quoting=csv.QUOTE_ALL)
            linkedin_writer.writerow(['post','content','reactions','comments','total','time'])
            for item in data:
                linkedin_writer.writerow(item)
        linkedin_file.close()
    
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

profile_urls = {
        'Pikkal & Co': 'https://www.linkedin.com/company/pikkal/',
        'Graham Brown':'https://www.linkedin.com/in/grahamdbrown/detail/recent-activity/shares/',
        'Prarthana':'https://www.linkedin.com/in/prarthanasibal/detail/recent-activity/shares/'
        }
    # Try it with test_urls
test_urls = list(profile_urls.values())
test_names =list(profile_urls.keys())
test_name = test_names[0]
test_url = test_urls[0]

linkedin = Linkedin()
linkedin.login()
linkedin.gotoProfile(test_url)
linkedin.getPosts()


