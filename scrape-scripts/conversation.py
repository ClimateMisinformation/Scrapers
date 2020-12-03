from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import pandas as pd
import time
import pickle

"""
Scraping for site: https://theconversation.com/uk/environment
Total number of pages with links: 111
Total number of posts in all pages:
"""

site = "https://theconversation.com/uk/environment/articles"

start = time.time()
urls = [site]
for url in urls:
    # get the extra pages from each month and year
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    pagination = soup.find('nav', {'class' : 'pagination'})
    # check if next page exists or not
    try:
        links = pagination.find_all('a')
        for a in links:
            u = a['href']
            if "https://theconversation.com"+u not in urls:
                urls.append("https://theconversation.com"+u)
    except AttributeError:
        continue

print ("New urls after counting pagination:", len(urls))
print ("Time taken: {:.2f} sec".format(time.time()-start))

post_urls = []
for url in tqdm(urls):
    # get the required page from each month and year
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    section = soup.find_all('div', {'class': 'article--header'})
    for header in section:
        heading = header.find('h2')
        u = heading.a.get('href')
        if "https://theconversation.com"+u not in post_urls:
            post_urls.append("https://theconversation.com"+u)

print ("Found posts:", len(post_urls))

# save for later use as backup
with open('posts_conversation.pkl', 'wb') as f:
    pickle.dump(post_urls, f)

post_url, post_authors, post_title, post_desc, post_cat, post_dates = [], [], [], [], [], []
for url in tqdm(post_urls):
    # get url of the post
    post_url.append(url)
    # get the required post
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    topic = soup.find_all('li', {'class': 'topic-list-item"'})
    cat = []
    for link in topic:
        cat.append(link.a.get('href'))
    # get category of post if any
    post_cat.append(cat)
    # get the title of post
    entry_title = soup.find('title')
    try:
        post_title.append(entry_title.text.strip())
    except AttributeError:
        post_title.append("")
    desc = soup.find_all('div', {'itemprop': 'articleBody'})
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
    author = soup.find('span', {'class': 'fn author-name'})
    # check if author exists or not
    try:
        post_authors.append(author.text.strip())
    except AttributeError:
        post_authors.append("")
    date = soup.find('time', {'itemprop': 'datePublished'})
    try:
        post_dates.append(date.text.strip())
    except AttributeError:
        post_dates.append("")    

# save all scraping to csv
df = pd.DataFrame(zip(post_url, post_authors, post_title, post_desc, post_cat, post_dates), 
                    columns=["url", "author", "title", "text", "tags", "date"])
df['source'] = ["the conversation"] * len(df)
df.to_csv("conversation.csv", index=False)