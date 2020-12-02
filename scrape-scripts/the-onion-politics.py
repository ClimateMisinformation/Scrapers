
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


response = requests.get('https://politics.theonion.com/')
page_soup = BeautifulSoup(response.text, 'html.parser')


def check_if_url_to_skip(url):
  if(url in [ '/search', '/newsletter' ]):
    return True
  if(url[:2] == '//'):
    return True
  if(url[-4:] == '.com'):
    return True
  if(url[-5:] == '.com/'):
    return True
  if(url.find('/c/') >= 0):
    return True
  if(url.find('?') >= 0):
    return True
  return False

urls = []

for link_article_soup in tqdm(page_soup.find_all('a')):
  try:
    url = link_article_soup.attrs['href']
  except(KeyError):
    continue
  if(check_if_url_to_skip(url)):
    continue
  urls.append(url)

urls = list(set(urls))

print(f'Found {len(urls)} valid links')


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
  title = clean_text(page_soup.find('h1').text)
  author = ''
  date = page_soup.find('time').attrs['datetime'][:10] # theoretically should convert to GMT...
  tags = ''
  #
  p_list = [ html_to_text_converter.handle(str(p_soup)) for p_soup in page_soup.find_all('p') ]
  text = '\n'.join(p_list)
  if(len(text) == 0):
    continue
  articles['url'].append(url)
  articles['title'].append(title)
  articles['author'].append(author)
  articles['date'].append(date)
  articles['tags'].append(tags)
  articles['text'].append(text)


pandas.DataFrame(articles).to_csv('data/the-onion-politics.csv', index = False)






