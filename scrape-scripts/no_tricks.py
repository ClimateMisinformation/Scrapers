from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import pandas as pd
import time
import re

"""
Scraping for site: https://notrickszone.com/
Total number of pages with links : 417
Total number of posts in all pages: 4321
"""

site = "https://notrickszone.com/"
# get the required page
page = requests.get(site)
soup = BeautifulSoup(page.text, 'lxml')
section = soup.find('ul', {'class': "xoxo archives"})

urls = []
for l in section.findAll('li'):
    # get all month and year linked urls
    urls.append(l.a.get('href'))

print ("Found URLS:", len(urls))

start = time.time()
post_urls = []
for url in urls:
    # get the extra pages from each month and year
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    pagination = soup.find('div', {'class' : 'navigation-links'})
    pages = pagination.findAll('a')
    for a in pages:
        if a['href'] not in urls:
            urls.append(a['href'])

print ("New URLS after counting pagination:", len(urls))
print ("Time taken: {:.2f} sec".format(time.time()-start))

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
    entry_class = soup.find("div", {"id" : re.compile('post-*')})
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

print (len(post_url), len(post_title), len(post_desc), len(post_cat))

# save all scraping to csv
df = pd.DataFrame(zip(post_url, post_title, post_desc, post_cat), columns=["URL", "Title", "Description", "Category"])
df.to_csv("no_tricks.csv", index=False)