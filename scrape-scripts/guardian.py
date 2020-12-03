from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import pandas as pd
import time
import re
import pickle

"""
Scraping for site: https://www.theguardian.com/environment/climate-change/
Total number of pages with links: 6030
Total number of posts in all pages: 26022
"""

site = "https://www.theguardian.com/environment/climate-change/"
# get the required page
page = requests.get(site)
soup = BeautifulSoup(page.text, 'lxml')
section = soup.find_all('header', {'class': 'fc-container__header js-container__header'})

urls = []
for header in section:
    curr_url = header.find('a')
    # get all month and year linked urls
    urls.append(curr_url.get('href'))

print ("Found urls:", len(urls))

start = time.time()
post_urls = []
for url in urls:
    # get the extra pages from each month and year
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    pagination = soup.find('div', {'class' : 'pagination u-cf'})
    # check if next page exists or not
    try:
        pages = pagination.findAll('a')
        for a in pages:
            u = a['href']
            if u not in urls and not u.endswith('altdate'):
                urls.append(u)
    except AttributeError:
        continue

print ("New urls after counting pagination:", len(urls))
print ("Time taken: {:.2f} sec".format(time.time()-start))

for url in tqdm(urls):
    # get the required page from each month and year
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    entry_title = soup.findAll('h3', {'class': 'fc-item__title'})
    for title in entry_title:
        u = title.a.get('href')
        if u not in post_urls:
            post_urls.append(u)

print ("Found posts:", len(post_urls))
# save for later use as backup
with open('posts.pkl', 'wb') as f:
    pickle.dump(post_urls, f)

post_url, post_authors, post_title, post_desc, post_cat = [], [], [], [], []
for url in tqdm(post_urls):
    # get url of the post
    post_url.append(url)
    # get the required post
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    # get category of post if any
    post_cat.append(url.split("/")[3])
    # get the title of post
    entry_title = soup.find('title')
    try:
        post_title.append(entry_title.text.split("|")[0])
    except AttributeError:
        post_title.append("")
    desc = soup.find_all('div', {'class': re.compile('article-body*')})
    cls = []
    for d in desc:
        if d is not None:
            para = d.find_all('p')
            for line in para:
                try:
                    cls.append(line.text)
                except AttributeError:
                    cls.append("")
    post_desc.append(' '.join(cls))
    # get author of the post
    author = soup.find('a', {'rel': 'author'})
    # check if author exists or not
    try:
        post_authors.append(author.text)
    except AttributeError:
        post_authors.append("")

# save all scraping to csv
df = pd.DataFrame(zip(post_url, post_authors, post_title, post_desc, post_cat), 
                    columns=["url", "author", "title", "text", "tags"])
# add date I am assuming all links share same pattern "https://www.theguardian.com/cat/2020/dec/03/title"
## this is not true for all cases --> we need to find a workaround for this
df['date'] = df['url'].apply(lambda x : "/".join(x.split("/")[4:7]))
df['source'] = ["Guardian"] * len(df)
df.to_csv("guardian.csv", index=False)