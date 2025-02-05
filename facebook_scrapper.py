from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv('email')
PASSWORD = os.getenv('fbpassword')
url = "https://www.facebook.com/NatWest?locale=en_GB"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    print(f"Visiting page: {url}")
    page.goto(url)
    # page.
    time.sleep(5)  

    soup = BeautifulSoup(page.content(), 'html.parser')
    with open('facebook.txt', 'w') as f:
        f.write(soup.get_text(separator='/n', strip=True))

    # posts = soup.find_all("div", class_="content")
    # count = 0
    # for post in posts:
    #     count += 1
    #     post_content = post.find("div", class_="content")
    #     print(f"Post count: {count}")
    #     print(post)
    #     if count > 20:
    #         break
    browser.close()
    print('Broswer closed!!')
