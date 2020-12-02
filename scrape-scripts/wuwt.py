from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import pandas as pd
import time
import re

"""
Scraping for site: https://wattsupwiththat.com/
Total number of pages with links: 170
Total number of posts in all pages: 1700
"""

site = "https://wattsupwiththat.com/"
# get the required page
page = requests.get(site)
soup = BeautifulSoup(page.text, 'lxml')
section = soup.find('select', {'id': "archives-dropdown-2"})

urls = []
for l in section.find_all('option'):
    # get all month and year linked urls
    urls.append(l['value'])

#remove urls with empty value
urls.remove("")
print ("Found urls:", len(urls))

post_urls = []
for url in tqdm(urls):
    # get the required page from each month and year
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    entry_title = soup.findAll('h1', {'class': 'entry-title'})
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
    entry_class = soup.find("article", {"id" : re.compile('post-*')})
    cls = []
    for c in entry_class['class']:
        if 'category' in c:
            cls.append(c.replace("category-", ""))
        if 'tag' in c:
            cls.append(c.replace("tag-", ""))
    post_cat.append(cls)
    # get the title of post
    entry_title = soup.find('h1', {'class': 'entry-title'})
    post_title.append(entry_title.text.strip())
    # get description of post
    desc = soup.find('div', {'class': 'entry-content'})
    post_desc.append(desc.text)
    # get author of post
    author = soup.find('a', {'class': 'author'})
    post_authors.append(author.text)

# save all scraping to csv
df = pd.DataFrame(zip(post_url, post_authors, post_title, post_desc, post_cat), columns=["url", "author", "title", "text", "tags"])
# add date
df['date'] = df['url'].apply(lambda x : "/".join(x.split("/")[3:6]))
df.to_csv("wuwt.csv", index=False)