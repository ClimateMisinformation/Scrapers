from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import pandas as pd
import time
import re

"""
Scraping for site: https://notrickszone.com/
Total number of pages with links : 418
Total number of posts in all pages: 4323
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

print ("Found urls:", len(urls))

start = time.time()
post_urls = []
for url in urls:
    # get the extra pages from each month and year
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    pagination = soup.find('div', {'class' : 'navigation-links'})
    # check if next page exists or not
    try:
        pages = pagination.findAll('a')
        for a in pages:
            if a['href'] not in urls:
                urls.append(a['href'])
    except AttributeError:
        continue    

print ("New urls after counting pagination:", len(urls))
print ("Time taken: {:.2f} sec".format(time.time()-start))

for url in tqdm(urls):
    # get the required page from each month and year
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    entry_title = soup.findAll('h2', {'class': 'entry-title'})
    for title in entry_title:
        post_urls.append(title.a.get('href'))

print ("Found posts:", len(post_urls))

post_url, post_authors, post_title, post_desc, post_cat = [], [], [], [], []
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
    # get author of the post
    author = soup.find('a', {'class': 'url fn n'})
    # check if author exists or not
    try:
        post_authors.append(author.text)
    except AttributeError:
        post_authors.append("")

# save all scraping to csv
df = pd.DataFrame(zip(post_url, post_authors, post_title, post_desc, post_cat), columns=["url", "author", "title", "text", "tags"])
# add date
df['date'] = df['url'].apply(lambda x : "/".join(x.split("/")[3:6]))
df.to_csv("no_tricks.csv", index=False)
