# SELENIUM
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import time
from datetime import datetime
import smtplib, ssl # EMAIL

class Instagram:
    # NEEDS IMPROVEMENT
    # Without login, there is a limit before instagram prompt you to login
    # Also the details that you can get is limited if you only over on page
    # Future improvement can include simulating click on and navigate to next image
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

    # GO TO INSTAGRAM PAGE
    def gotoPage(self, url):
        driver = self.driver
        driver.get(url)
        time.sleep(2)

    # SCRAPING
    def getDetails(self):
        print("Start Scraping...")  
        driver = self.driver
        # SCROLL TO BOTTOM
        self.scrollToN(2)
        
        # FIND ALL IMAGE ITEMS ON PAGE
        articles = driver.find_elements_by_xpath(".//div[@class='v1Nh3 kIKUG  _bz0w']")
        
        # INIT VARIABLES
        details = ""
        count = 1
        for article in articles:
            # GET LINK
            linkToImage =article.find_element_by_tag_name("a").get_attribute('href')

            # SIMULATE HOVER TO SEE LIKE AND COMMENT
            action = ActionChains(driver)
            action.move_to_element(article).perform()

            #GET LIKE AND COMMENT NUMBER
            reaction = (article.find_element_by_xpath(".//div[@class='qn-0x']").text)
            like,comment = reaction.split()
            # CONSTRUCT READABLE MESSAGE
            details+= "Link to post: "+ linkToImage + " Like: "+like+" Comment: "+comment + "]\n"

            # ONLY LATEST 15
            if count == 15:
                break
            # # ADD COUNT
            count+=1
            
        # CURRENT TIME
        currentDT = datetime.now()
        # # SUMMARY
        details+=(" [On " + str(currentDT) + "]\n")
        print("Scraping completed...")
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
        message = "Subject: Instagram Stats\n\nThis message is sent from Yong.\n"
        for i in msg:
            message+=i

        # EMAIL CONFIG
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        print('Email sent!')

    def scrollToN(self, n_scrolls):
        # TIME TO PAUSE FOR PAGE LOADING
        SCROLL_PAUSE_TIME = 1

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
            self.gotoPage(url)
            # GET INFO
            msgarray.append(self.getDetails())
            time.sleep(1)

        # CLEAR BROWSER
        self.quitBrowser()
        # SEND EMAIL
        self.sendemail(msgarray)

        print("DONE")
# EXECUTE 
instagram = Instagram()
instagram.runTool(['https://www.instagram.com/pikkal_creative'])
