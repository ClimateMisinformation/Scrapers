from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import pandas as pd

"""
Scraping for site:https://carbon-sense.com/
Total number of pages with links: 150
Total number of posts in all pages: 682
"""

site = "https://carbon-sense.com/"
# get the required page
page = requests.get(site)
soup = BeautifulSoup(page.text, 'lxml')
section = soup.find_all('link', {'rel': "archives"})
urls = []
for l in section:
    # get all month and year linked urls
    urls.append(l['href'])

print ("Found urls:", len(urls))

post_urls = []
for url in tqdm(urls):
    # get the required page from each month and year
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    entry_title = soup.findAll('div', {'class': 'storycontent'})
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
    p_class = soup.find("p", {"class" : 'postmetadata'})
    cls = []
    for c in p_class.find_all('a'):
        cls.append(c.text)
    post_cat.append(cls)
    # get the title of post
    story = soup.find('div', {'class': 'storycontent'})
    entry_title = story.find('a')
    post_title.append(entry_title.text.strip())
    # get the description of post
    desc = soup.find('div', {'class': 'storybody'})
    post_desc.append(desc.text)

# difficult to extract exact authors they are usually on 1st line of description
post_authors = [""]*len(post_url)

# save all scraping to csv
df = pd.DataFrame(zip(post_url, post_authors, post_title, post_desc, post_cat), columns=["url", "author", "title", "text", "tags"])
# add date
df['date'] = df['url'].apply(lambda x : "/".join(x.split("/")[3:6]))
df.to_csv("carbon_sense.csv", index=False)