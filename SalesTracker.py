from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import BeautifulSoup as bs
from matplotlib.pyplot import title
from win10toast_persist import ToastNotifier
import requests


URL = 'https://www.reddit.com/r/buildapcsales/new/?f=flair_name%3A%22GPU%22'
ARTICLE_CLASS_NAME = 'yn9v_hQEhjlRNZI0xspbA'
TITLE_CLASS_NAME = '_eYtD2XCVieq6emjKBH3m'
LINK_CLASS_NAME = '_13svhQIUZqD9PVzFcLwOKT'

toaster = ToastNotifier()
scheduler = BlockingScheduler()
links = []

def check_reddit():
    page = requests.get(URL)
    reddit_soup = bs(page.content, "html.parser")
    reddit_posts = reddit_soup.find_all("article", class_="yn9v_hQEhjlRNZI0xspbA")
    for post in reddit_posts:
        post_title = post.find("h3", class_= TITLE_CLASS_NAME).text.strip()
        linked_url = post.find("a", class_= LINK_CLASS_NAME)["href"]
    
        if("EVGA" in post_title or "ASUS" in post_title and "3080" in post_title):
            if(linked_url not in links):
                toaster.show_toast(title = "GPU", msg = linked_url, duration=None)
                print(linked_url)
                links.append(linked_url)

    print('I Ran')
 
 
check_reddit()
scheduler.add_job(check_reddit, 'interval', minutes = 30)
scheduler.start()
