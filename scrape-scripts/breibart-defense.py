
import datetime
import os
import re
import requests
import urllib.parse
import time

from bs4 import BeautifulSoup
import html2text
import numpy as np
import pandas
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException as slnm_NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException as slnm_StaleElementReferenceException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm


def clean_text(text):
  return re.sub(' $', '', re.sub('^ ', '', re.sub(' +', ' ', text.replace('\n', ' '))))


html_to_text_converter = html2text.HTML2Text()
html_to_text_converter.body_width = 0
html_to_text_converter.ignore_links = True


response = requests.get('https://www.breitbart.com/tag/defense/#')
page_soup = BeautifulSoup(response.text, 'html.parser')

link_list_soup = page_soup.find('section', 'aList').find_all('article')

base_url = 'https://www.breitbart.com'
urls = []

for link_article_soup in link_list_soup:
  url = link_article_soup.find('a').attrs['href']
  urls.append(base_url + url)

articles = {
  'url' : [],
  'title' : [],
  'author' : [],
  'date' : [],
  'tags' : [],
  'text' : [],
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
  p_list = [ html_to_text_converter.handle(str(p_soup)) for p_soup in content_soup.find_all('p') ]
  text = '\n'.join(p_list)
  articles['url'].append(url)
  articles['title'].append(title)
  articles['author'].append(author)
  articles['date'].append(date)
  articles['tags'].append(tags)
  articles['text'].append(text)


pandas.DataFrame(articles).to_csv('data/breibart-defense.csv', index = False)






