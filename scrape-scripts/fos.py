from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import pandas as pd

"""
Scraping for site: https://blog.friendsofscience.org/
Total number of pages with links: 73
Total number of posts in all pages: 485
"""

site = "https://blog.friendsofscience.org/"
# get the required page
page = requests.get(site)
soup = BeautifulSoup(page.text, 'lxml')
section = soup.find('select', {'id': "archives-dropdown-3"})

urls = []
for l in section.find_all('option'):
    if l.text == "Select Month":
        continue
    # get all month and year linked urls
    urls.append(l['value'])

print ("Found urls:", len(urls))

post_urls = []
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
    p_class = soup.find("p", {"class" : 'post-categories'})
    cls = []
    for c in p_class.find_all('a'):
        cls.append(c.text)
    post_cat.append(cls)
    # get the title of post
    entry_title = soup.find('h1', {'class': 'entry-title'})
    post_title.append(entry_title.text.strip())
    # get description of post
    desc = soup.find('div', {'class': 'entry-content'})
    post_desc.append(desc.text)
    # get authors of the post
    authors = soup.find('cite', {'class': 'fn'})
    try:
        post_authors.append(authors.text)
    except AttributeError:
        post_authors.append("")

print (len(post_url), len(post_authors),  len(post_title), len(post_desc), len(post_cat))

# save all scraping to csv
df = pd.DataFrame(zip(post_url, post_authors, post_title, post_desc, post_cat), columns=["url", "author", "title", "text", "tags"])
# add date
df['date'] = df['url'].apply(lambda x : "/".join(x.split("/")[3:6]))
df.to_csv("fos.csv", index=False)