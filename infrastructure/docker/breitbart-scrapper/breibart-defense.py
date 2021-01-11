#!/usr/bin/python3

"""
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import re
import requests
from bs4 import BeautifulSoup, UnicodeDammit
import html2text
import pandas
from tqdm import tqdm


def clean_text(text):
  return re.sub(' $', '', re.sub('^ ', '', re.sub(' +', ' ', text.replace('\n', ' '))))



if __name__ == "__main__":

    """
        This script scrapes the Breibart website for  articles. 
        
        If a URL passes the criteria defined by filter_url(), then it is visited and its content extracted using 
        Beautiful soup.  B. Soup cleans up the inner element text by converting it to UTF8 from the mess it is.
        
        The data extracted is saved to  a  dictionary
        
        article_content = {
        'url': [],
        'title': [],
        'author': [],
        'date': [],
        'tags': [],
        'text': [],
        }

    """
response = requests.get('https://www.breitbart.com/tag/defense/#')
page_soup = BeautifulSoup(response.text, 'html.parser')
link_list_soup = page_soup.find('section', 'aList').find_all('article')
base_url = 'https://www.breitbart.com'
urls = []


for link_article_soup in link_list_soup:
  url = link_article_soup.find('a').attrs['href']
  urls.append(base_url + url)

article_content = {
        'url': [],
        'title': [],
        'author': [],
        'date': [],
        'tags': [],
        'text': [],
    }

for url in tqdm(urls):
  response = requests.get(url)
  page_soup = BeautifulSoup(response.text, 'html.parser')
  content_soup = page_soup.find('article', 'the-article')
  header_soup = content_soup.find('header')
  title = clean_text(header_soup.find('h1').text)
  author = clean_text(header_soup.find('address').text)
  date = header_soup.find('time').attrs['datetime'][:10]
  tags = 'defense'
  content_soup = content_soup.find('div', 'entry-content')
  p_list =  content_soup.find_all('p')

  def paragraph_is_not_caption_text(p):
        if p.attrs == {'class': ['wp-caption-text']}:
            return False
        else:
            return p
  text_soup = [ p.text for p in p_list if paragraph_is_not_caption_text(p)]

  article_content['url'].append(url)
  article_content['title'].append(title)
  article_content['author'].append(author)
  article_content['date'].append(date)
  article_content['tags'].append(tags)
  article_content['text'].append(text_soup)


try:
  pandas.DataFrame.from_dict(article_content).to_csv('output.csv', index=False)
except Exception as e:
  print(e)





