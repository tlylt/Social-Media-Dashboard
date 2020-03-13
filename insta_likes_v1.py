import requests
import json
import re
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import csv
import html
import time
from datetime import datetime
def recent_posts(username,no_of_post = 50):
    """With the input of an account page and number of posts to scrape,
    return the posts urls"""
    url = "https://www.instagram.com/" + username + "/"
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    browser = Chrome(options=chrome_options)
    browser.get(url)
    post = 'https://www.instagram.com/p/'
    post_links = []
    while len(post_links) < no_of_post:
        links = [a.get_attribute('href') for a in browser.find_elements_by_tag_name('a')]
        for link in links:
            if post in link and link not in post_links:
                post_links.append(link)
        scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
        browser.execute_script(scroll_down)
        time.sleep(8)
    print('post url collection done...')
    return post_links

def get_stat(posts):
    data=[]
    time_pattern = re.compile(r"\"taken_at_timestamp\":(\d+),")
    for post in posts:
        response = requests.get(post)
        soup = BeautifulSoup(response.content,features="html.parser")
        detail = (soup.find(property="og:description")['content'])
        title = html.unescape(soup.find(property="og:title")['content']).encode("utf-8")
        title = title.decode('utf-8')
        like_index = detail.find('Likes')-1
        # comments_index = detail.find('Comments')-1
        # comments = detail[detail.find(',')+2:comments_index]
        # data.append([post,likes,comments])
        likes = detail[:like_index]
        t=re.search(time_pattern,str(soup))
        timestamp=int(t.group()[21:-1])
        dt = datetime.fromtimestamp(timestamp)
        readable_time=dt.strftime('%B %d')
        data.append([post,timestamp,readable_time,title,likes])
        time.sleep(3)
    print('data cleaning done...')
    return data

urls = recent_posts("pikkal_creative",50)
# urls = recent_posts("gem0816",10)
data=get_stat(urls)

with open('insta_01032020.csv', mode='w',encoding="utf-8") as insta_file:
    insta_writer = csv.writer(insta_file, delimiter=',',  quoting=csv.QUOTE_ALL)
    insta_writer.writerow(['link','timestamp','time','summary','likes'])
    for item in data:
        insta_writer.writerow(item)

insta_file.close()