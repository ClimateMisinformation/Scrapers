from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import pandas as pd

"""
Scraping for site: http://clexit.net/
"""

site = "http://clexit.net/"
# get the required page
page = requests.get(site)
soup = BeautifulSoup(page.text, 'lxml')
section = soup.find('section', {'class': "widget widget_archive"})

urls = []
for l in section.findAll('li'):
    # get all month and year linked urls
    urls.append(l.a.get('href'))

print ("Found URLS:", len(urls))

post_urls = []
for url in tqdm(urls):
    # get the required page from each month and year
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    entry_title = soup.findAll('h2', {'class': 'entry-title'})
    for title in entry_title:
        post_urls.append(title.a.get('href'))

print ("Found posts:", len(post_urls))

post_url, post_title, post_desc, post_cat = [], [], [], []
for url in tqdm(post_urls):
    # get url of the post
    post_url.append(url)
    # get the required post
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    # get category of post if any
    entry_class = soup.find('article')
    cls = []
    for c in entry_class['class']:
        if 'category' in c:
            cls.append(c)
    post_cat.append(cls)
    # get the title of post
    entry_title = soup.find('h1', {'class': 'entry-title'})
    post_title.append(entry_title.text.strip())
    desc = soup.find('div', {'class': 'entry-content'})
    post_desc.append(desc.text)

# save all scraping to csv
df = pd.DataFrame(zip(post_url, post_title, post_desc, post_cat), columns=["URL", "Title", "Description", "Category"])
df.to_csv("clexit.csv", index=False)
