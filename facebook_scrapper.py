from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import os
from pathlib import Path

url = "https://www.facebook.com/NatWest?locale=en_GB"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    print(f"Visiting page: {url}")
    page.goto(url)
    time.sleep(5)  

    soup = BeautifulSoup(page.content(), 'html.parser')
    
    posts = soup.find_all("div", class_="content")
    count = 0
    for post in posts:
        count += 1
        post_content = post.find("div", class_="content")
        print(f"Post count: {count}")
        print(post)
        if count > 20:
            break
    browser.close()
    print('Broswer closed!!')
