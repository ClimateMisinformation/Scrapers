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


search_key_word = 'climate'
search_key = 's'
url = r'https://thebfd.co.nz/'

link_list_data_file_path = 'url-data.csv'

delay_time_min = 0.
delay_time_max = 0.1

quick_save_period = 10



def read_page_entries(page_soup, time_stamp, page_index, page_lists, do_print = True):
  entries = page_soup.find_all('div', 'td_module_16')
  if(do_print):
    print(f'Page {page_index} has {len(entries)} entries')
  for entry_index, entry in enumerate(entries):
    title_html = entry.find('h3', 'entry-title')
    link_html = title_html.find('a')
    page_lists['time_stamp'].append(time_stamp)
    page_lists['page'].append(page_index)
    page_lists['index_in_page'].append(entry_index)
    page_lists['title'].append(link_html.attrs['title'])
    page_lists['link'].append(link_html.attrs['href'])

def quick_save(page_lists, data_file_path):
  print(f'saving...')
  data = pandas.DataFrame(page_lists)
  data.to_csv(data_file_path, index = False)


page_lists = {
  'time_stamp' : [],
  'page' : [],
  'index_in_page' : [],
  'title' : [],
  'link' : [],
}




request_code = urllib.parse.urlencode({ search_key : search_key_word })
search_url = url + '?' + request_code

scrap_time = time.time()
res = requests.get(search_url)

result_page = res.text
soup = BeautifulSoup(result_page, 'html.parser')


nb_result_pages = int(soup.find('div', 'page-nav').find('a', 'last').attrs['title'])
print(f'Found {nb_result_pages} pages')


read_page_entries(soup, scrap_time, 1, page_lists)


for page_index in range(2, nb_result_pages + 1):
  url = r'https://thebfd.co.nz/page/' + f'{page_index}/?' + request_code
  time_stamp = time.time()
  res = requests.get(url)
  if(not res.ok):
    raise Exception(f'*** request failed: {res} - page = {page} - url = {url} ***')
  read_page_entries(BeautifulSoup(res.text, 'html.parser'), time_stamp, page_index, page_lists)
  if((page_index % quick_save_period) == 0):
    quick_save(page_lists, link_list_data_file_path)
  delay_time = np.random.uniform(delay_time_min, delay_time_max)
  time.sleep(delay_time)

quick_save(page_lists, link_list_data_file_path)

"""
# repair page numbers

nb_items = len(page_lists['title'])

current_time_stamp = page_lists['time_stamp'][0]
current_page = 1

for item_index in range(1, nb_items):
  next_time_stamp = page_lists['time_stamp'][item_index]
  if(next_time_stamp > current_time_stamp):
    current_page += 1
    current_time_stamp = next_time_stamp
  page_lists['page'] = current_page

quick_save(page_lists, link_list_data_file_path)
"""




"""
ENTRIES:
div, td_module_16
> h3, entry-title
  >> a (link)

NEXT ENTRIES:
div, page-nav
> span, current: current page
> a, page: link, title=page
format:
https://thebfd.co.nz/page/{page_number}/?s=climate
> a, last: link, title=page (=total number of pages)

PAGE:

paywall: https://thebfd.co.nz/2020/10/17/the-truth-about-climate-change-part-ii/
span: "Subscriber only content"

open: https://thebfd.co.nz/2020/10/17/the-truth-about-climate-change-part-ii/
categories
title
subtitle
type of author (such as "Guest Post")
date-time
nb viewers (=0 ?)
nb comments ('leave a comment = 0)
author
author role
article (first letter is fancy)
>> content has bold, ita, links, videos, images
curated list of links to related articles
(other stuff and comments)


"""


data_dir = 'the-bfd'
data_html_path = os.path.join(data_dir, 'html')
data_text_path = os.path.join(data_dir, 'text')

save_every = 50
page_content_data_file_path = 'pages.csv'

def check_if_page_is_paywalled(page_soup):
  all_h1 = page_soup.find_all('h1')
  for h1 in all_h1:
    span = h1.find('span')
    if(span is None):
      continue
    if(span.text == 'Subscriber only content'):
      return True
  return False

def make_page_path(page_index):
  return f'{page_index:04d}'

def save_html(data_html_path, page_path, page_html):
  html_file_path = os.path.join(data_html_path, page_path)
  f = open(html_file_path, 'w')
  f.write(page_html)
  f.close()

def save_text(data_text_path, page_path, content):
  text_file_path = os.path.join(data_text_path, page_path)
  f = open(text_file_path, 'w')
  f.write(content)
  f.close()


def process_link(page_index, page_url, page_data):
  res = requests.get(page_url)
  if(not res.ok):
    raise Exception(f'*** Failed request for {url} : {res} ***')
    
  page_soup = BeautifulSoup(res.text, 'html.parser')
  
  header_soup = page_soup.find('header', 'td-post-title')
  
  categories = []
  categories_soup = header_soup.find('ul', 'td-category')
  if(categories_soup is not None):
    category_entries = categories_soup.find_all('li', 'entry-category')
    nb_categories = len(category_entries)
    for category_entry in category_entries:
      categories.append(category_entry.find('a').text)
  
  title = header_soup.find('h1', 'entry-title').text
  
  try:
    subtitle = header_soup.find('p', 'td-post-sub-title').text
  except(AttributeError):
    subtitle = ''
  
  meta_info_soup = header_soup.find('div', 'td-module-meta-info')
  
  author = meta_info_soup.find('div', 'td-post-author-name').find('a').text
  
  date_time = meta_info_soup.find('span', 'td-post-date').find('time').attrs['datetime']
  
  nb_views = int(meta_info_soup.find('div', 'td-post-views').find('span').text)
  
  # a page has 2 comments but appear as 0???
  
  nb_comments_text = meta_info_soup.find('div', 'td-post-comments').find('a').text
  if(nb_comments_text == 'Leave a Comment'):
    nb_comments = 0
  else:
    nb_comments = int(nb_comments_text.split()[0])
  
  is_paywalled = check_if_page_is_paywalled(page_soup)
  
  if(is_paywalled):
    page_type = 'subscription only'
    page_html_path = None
    page_text_path = None
    introduction = None
  else:
    page_type = 'open'
    page_path = make_page_path(page_index)
    page_html_path = page_path + '.html'
    save_html(data_html_path, page_html_path, res.text)
    article_content = page_soup.find('div', 'td-post-content')
    article_text = '\n'.join([ html_to_text_converter.handle(str(p)) for p in article_content.find_all('p') ])
    page_text_path = page_path + '.txt'
    save_text(data_text_path, page_text_path, article_text)
    introduction = ''
    introduction_soup = article_content.find('p', 'wp-block-advanced-gutenberg-blocks-intro__content')
    if(introduction_soup is not None):
      introduction = html2text.html2text(str(introduction_soup))
  
  page_data['id'].append(page_index)
  page_data['url'].append(page_url)
  page_data['categories'].append(categories)
  page_data['title'].append(title)
  page_data['subtitle'].append(subtitle)
  page_data['author'].append(author)
  page_data['date_time'].append(date_time)
  page_data['nb_views'].append(nb_views)
  page_data['nb_comments'].append(nb_comments)
  page_data['type'].append(page_type)
  page_data['introduction'].append(introduction)
  page_data['html_path'].append(page_html_path)
  page_data['text_path'].append(page_text_path)






html_to_text_converter = html2text.HTML2Text()
html_to_text_converter.body_width = 0

page_list = pandas.read_csv(link_list_data_file_path)
nb_links = len(page_list)



page_data = {
 'id' : [],
 'url' : [],
 'categories' : [],
 'title' : [],
 'subtitle' : [],
 'author' : [], # author or contribution
 'date_time' : [],
 'nb_views' : [],
 'nb_comments' : [],
 'type' : [], # open or subscription-only,
 # below apply only to 'open'
 'introduction' : [], # note: introduction is part of the text saved in text_path file
 'html_path' : [], # path to html content of the bare page
 'text_path' : [], # path to file containing the body of the article in pure text form (all the 'p' from div'td-post-content')
}


print(f'Scrapping through {nb_links} links...')

for page_index in range(nb_links):
  page_url = page_list.loc[page_index]['link']
  process_link(page_index, page_url, page_data)
  if(((page_index + 1) % save_every) == 0):
    print('saving...')
    page_data_df = pandas.DataFrame(page_data)
    page_data_df.to_csv(page_content_data_file_path, index = False)
  #if(page_index >= 10):
  #  break


page_data_df = pandas.DataFrame(page_data)
page_data_df.to_csv(page_content_data_file_path, index = False)





























































