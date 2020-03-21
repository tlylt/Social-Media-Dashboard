import time # SLEEP
import smtplib, ssl # EMAIL
import datetime # CURRENT TIME

# SELENIUM STUFF
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

class Soundcloud:
    '''
    Initialize necessary variables
    Requires login
    '''
    def __init__(self):
        # WITHOUT DISPLAY
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        self.driver = Chrome(options=chrome_options) # INITIALIZE DRIVER

        # WITH DISPLAY
        # self.driver = Chrome()
        # self.driver.maximize_window()

    # GO TO PODCAST
    def gotoPodcast(self, url):
        driver = self.driver
        driver.get(url)
        # print("Entering Podcast ...")
        time.sleep(2)

    # SCRAPING
    def getDetails(self):
            driver = self.driver
            # SCROLL TO BOTTOM
            self.scrollToBottom()
            
            # FIND ALL SOUNCLOUD ITEMS ON PAGE
            articles = driver.find_elements_by_xpath(".//div[@class='userStreamItem']")
            
            # INIT VARIABLES
            data=[]
            details = ""
            count = 1
            for article in articles:
                # GET DESCRIPTION
                description =article.find_element_by_xpath(".//div[@class='sound streamContext']").get_attribute('aria-label')
                #GET REACTION IN INTEGER
                reaction = int(article.find_element_by_xpath(".//span[@class='sc-ministats sc-ministats-small sc-ministats-plays']/span[@aria-hidden='true']").text)
                # CONSTRUCT READABLE MESSAGE
                details+= "View Count: "+ str(reaction).zfill(2) +" [" + description + "]\n"
                # KEEP IN ARRAY
                data.append([count,description,reaction])
                # ADD COUNT
                count+=1
            # CURRENT TIME
            currentDT = datetime.datetime.now()
            # SUMMARY
            details+=("Total Count: " +str(sum([i[2] for i in data])) +" [On " + str(currentDT) + "]\n")

            return details

    # SEND EMAIL REPORT
    def sendemail(self, msg):
        # EMAIL CONFIG
        port = 465  # FOR SSL
        smtp_server = "smtp.gmail.com"

        # FOR DEFAULT SETTING
        # sender_email = "" 
        # receiver_email = ""  
        # password = ""

        # FOR CLI INPUT
        sender_email = input("Type your Email and press enter: ")
        receiver_email = input("Type recevier Email and press enter: ")
        password = input("Type your password and press enter: ")
        
        # CONSTRUCT EMAIL CONTENT
        message = "Subject: SoundCloud Stats\n\nThis message is sent from Yong.\n"
        for i in msg:
            message+=i
        
        # EMAIL CONFIG
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

    def scrollToN(self, n_scrolls):
        # TIME TO PAUSE FOR PAGE LOADING
        SCROLL_PAUSE_TIME = 3

        # GET SCROLL HEIGHT
        driver = self.driver
        last_height = driver.execute_script("return document.body.scrollHeight;")

        for _ in range(n_scrolls):
            # SCROLL TO BOTTOM 
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # WAIT FOR LOADING
            time.sleep(SCROLL_PAUSE_TIME)
            # CALCULATE NEW SCROLL HEIGHT AND COMPARE WITH LAST SCROLL HEIGHT
            new_height = driver.execute_script("return document.body.scrollHeight;")
            if new_height == last_height:
                break
            last_height = new_height

    def scrollToBottom(self):
        # TIME TO PAUSE FOR PAGE LOADING
        SCROLL_PAUSE_TIME = 3

        # GET SCROLL HEIGHT
        driver = self.driver
        last_height = driver.execute_script("return document.body.scrollHeight;")

        while True:
            # SCROLL TO BOTTOM 
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # WAIT FOR LOADING
            time.sleep(SCROLL_PAUSE_TIME)

            # CALCULATE NEW SCROLL HEIGHT AND COMPARE WITH LAST SCROLL HEIGHT
            new_height = driver.execute_script("return document.body.scrollHeight;")
            if new_height == last_height:
                break
            else:
                last_height = new_height

    def quitBrowser(self):
        driver = self.driver
        driver.quit()

    # COMBINE ALL FUNCTIONS
    def runTool(self,urls):
        # KEEP INFO IN ARRAY
        msgarray = []

        # VISIT ALL URL
        for url in urls:
            # INIT
            self.gotoPodcast(url)
            # GET INFO
            msgarray.append(self.getDetails())
            time.sleep(1)

        # CLEAR BROWSER
        self.quitBrowser()
        # SEND EMAIL
        self.sendemail(msgarray)

        print("DONE")

# EXECUTE 
soundcloud = Soundcloud()
soundcloud.runTool(['https://soundcloud.com/xl-podcast','https://soundcloud.com/schoolofthefuture'])


