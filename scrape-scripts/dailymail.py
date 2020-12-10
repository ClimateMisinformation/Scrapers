from bs4 import BeautifulSoup
import requests
import re
import time
from tqdm import tqdm
import pandas
import html2text
import datetime
import sys
"""
Scraping for site: https://www.dailymail.co.uk/textbased/channel-1/index.html
General news from the text  only Daily  Mail website
"""

site = "https://www.dailymail.co.uk/textbased/channel-1/index.html"
start = time.time()
response = requests.get(site)
soup = BeautifulSoup(response.text, 'html.parser')
body = soup.body
urls = []

def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')

def clean_text(text):
  return re.sub(' $', '', re.sub('^ ', '', re.sub(' +', ' ', text.replace('\n', ' '))))

html_to_text_converter = html2text.HTML2Text()
html_to_text_converter.body_width = 0
html_to_text_converter.ignore_links = True


links = soup.find_all(has_class_but_no_id, href=re.compile("text-"))

for a in links:
    u = a['href']
    urls.append("https://www.dailymail.co.uk" + u)

print(urls)


articles = {
  'url' : [],
  'title' : [],
  'author' : [],
  'date' : [],
  'tags' : [],
  'text' : [],
}

for url in tqdm(urls):
    try:
        response = requests.get(url)
        page_soup = BeautifulSoup(response.text, 'html.parser')
        content_soup = page_soup.find('div', 'article')
        title = clean_text(content_soup.find('h1').text)
        author = clean_text(content_soup.find('p', 'author-section byline-plain').text)
        datestring = page_soup.body.div.span.text
        dateobject = datetime.datetime.strptime(datestring, '%A, %B %d %Y')
        date = dateobject.date()
        tags = 'Neutral'
        text = clean_text(content_soup.text)
        articles['url'].append(url)
        articles['title'].append(title)
        articles['author'].append(author)
        articles['date'].append(date)
        articles['tags'].append(tags)
        articles['text'].append(text)
    except Exception:
        print("Unexpected error:", sys.exc_info()[0])
        raise



pandas.DataFrame(articles).to_csv('data/dailymail.csv', index = False)


print ("New urls after counting pagination:", len(urls))
print ("Time taken: {:.2f} sec".format(time.time()-start))

