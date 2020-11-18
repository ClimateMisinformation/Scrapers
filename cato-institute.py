
"""
TODO:


copy in data dir
targzip
post


DONE:

clean date_time string

rename types:
type -> type_string
processed_type -> item_type

merge the data
save file

only 1 section (check content is correct): checked
"""

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
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

# params

search_key_word = 'climate change'
search_key = 'search'
url = r'https://www.cato.org/search'

link_list_data_file_path = 'url-data-cato-institute.csv'

data_dir = 'cato-institute'
html_dir = os.path.join(data_dir, 'html')
text_dir = os.path.join(data_dir, 'text')
articles_data_file = 'pages.csv'

quick_save_period = 10

do_print = True


testing = False
test_end = 20

# lib

def clean_text(text):
  return re.sub(' $', '', re.sub('^ ', '', re.sub(' +', ' ', text.replace('\n', ' '))))

def read_page_entries(driver, time_stamp, page_index, page_lists, do_print = True):
  entries_container = driver.find_element_by_class_name('algolia-search-results').find_element_by_class_name('ais-Hits-list')
  entries = entries_container.find_elements_by_class_name('ais-Hits-item')
  if(do_print):
    print(f'Page {page_index} has {len(entries)} entries')
  for entry_index, entry in enumerate(entries):
    meta_soup = entry.find_element_by_class_name('article-embed__meta')
    date_soup = meta_soup.find_elements_by_class_name('meta')[0]
    date = date_soup.text
    entry_type = meta_soup.find_element_by_class_name('article-embed__topic').text
    entry_body_soup = entry.find_element_by_class_name('article-embed__inner')
    entry_title_and_link_soup = entry_body_soup.find_element_by_tag_name('h3').find_element_by_tag_name('a')
    link = entry_title_and_link_soup.get_attribute('href')
    title = entry_title_and_link_soup.text
    page_lists['time_stamp'].append(time_stamp)
    page_lists['page'].append(page_index)
    page_lists['index_in_page'].append(entry_index)
    page_lists['date'].append(date)
    page_lists['type'].append(entry_type)
    page_lists['title'].append(title)
    page_lists['link'].append(link)

def quick_save(page_lists, data_file_path):
  print(f'saving...')
  data = pandas.DataFrame(page_lists)
  data.to_csv(data_file_path, index = False)


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




# main


firefox_bin_path = '/usr/bin/firefox'
geckodriver_path = '/usr/bin/geckodriver'

firefox_binary = FirefoxBinary(firefox_bin_path)

capabilities = DesiredCapabilities.FIREFOX.copy()

capabilities['marionette'] = True


driver = webdriver.Firefox(firefox_binary = firefox_binary,
                           capabilities = capabilities,
                           executable_path = geckodriver_path)


request_code = urllib.parse.urlencode({ search_key : search_key_word })
search_url = url + '?' + request_code

scrap_time = time.time()

driver.get(search_url)

search_input = driver.find_element_by_class_name('form-control--search')

search_input.send_keys('climate change')
search_input.send_keys(Keys.RETURN)

time.sleep(4)

nb_result_pages_element = driver.find_element_by_class_name('ais-Stats-text')
nb_result_pages_text = nb_result_pages_element.text
assert(nb_result_pages_text[-13:] == 'results found')
nb_result_pages = int(nb_result_pages_text.split()[0].replace(',', ''))
print(f'Found {nb_result_pages} pages')



pager_items = driver.find_element_by_class_name('pager__items')
nb_pages = int(pager_items.find_element_by_class_name('pager__item--last').find_element_by_tag_name('a').get_attribute('data-value')) + 1
print(f'Going through {nb_pages} pages...')


page_lists = {
  'time_stamp' : [],
  'page' : [],
  'index_in_page' : [],
  'date' : [], # human format
  'type' : [], # eg 'Blog' or 'Publication'
  'title' : [],
  'link' : [],
}

read_page_entries(driver, scrap_time, 1, page_lists)



for page_index in range(2, nb_pages + 1):
  pager_items = driver.find_element_by_class_name('pager__items')
  next_page_link = pager_items.find_element_by_class_name('pager__item--next').find_element_by_tag_name('a')
  next_page_link.click()
  time.sleep(0.28)
  time.sleep(1.7 + 1.2 * np.random.random(1)[0])
  read_page_entries(driver, scrap_time, page_index, page_lists)

# crashed at page 79 with 1580(=79*20) entries recorded

# saved
# ...

# read page 80 by hand
# ...

# then restarted the loop

for page_index in range(81, nb_pages + 1):
  pager_items = driver.find_element_by_class_name('pager__items')
  next_page_link = pager_items.find_element_by_class_name('pager__item--next').find_element_by_tag_name('a')
  next_page_link.click()
  time.sleep(0.28)
  time.sleep(1.7 + 1.2 * np.random.random(1)[0])
  read_page_entries(driver, scrap_time, page_index, page_lists)



"""
# potential work around:
for page_index in range(<START>, nb_pages + 1):
  pager_items = driver.find_element_by_class_name('pager__items')
  next_page_link = pager_items.find_element_by_class_name('pager__item--next').find_element_by_tag_name('a')
  next_page_link.click()
  time.sleep(0.28)
  time.sleep(1.7 + 1.2 * np.random.random(1)[0])    
  try:
    read_page_entries(driver, scrap_time, page_index, page_lists)
  except(selenium.common.exceptions.StaleElementReferenceException):
    # relaunch
    time.sleep(1.6 + 0.5 * np.random.random(1)[0])
    pager_items = driver.find_element_by_class_name('pager__items')
    next_page_link = pager_items.find_element_by_class_name('pager__item--next').find_element_by_tag_name('a')
    next_page_link.click()
    time.sleep(0.28)
    time.sleep(1.7 + 1.2 * np.random.random(1)[0])
    read_page_entries(driver, scrap_time, page_index, page_lists)
"""




"""
types:

if finishes with:
 • PDF \([0-9\.]+ MB\)
just ignore the entry on step 2(step 2 = dl the content of each page)

IF no pdf tail:
Blog -> webpage
Publication -> webpage
Media Highlights TV -> ignore (video)
Regulation -> probably PDF (expect 'PDF ()' tail)
Commentary -> webpage
white paper -> webpage (review)
Books -> ignore (book reviews)
Policy Analysis .* (eg 'Policy Analysis No. 609')-> webpage (review)
Media Highlights Radio -> ignore (multimedia)
Commentary -> webpage
Public Comments -> webpage

"""
page_list_df = pandas.DataFrame(page_lists)
page_list_df.to_csv('cat-institute-page-list-phase1.csv')


driver.quit()

nb_gathered_links = len(page_list_df)


# processing type


ignore_page = nb_gathered_links * [ False, ]

# lib

def remove_pdf_tail(type_string):
  match = re.search(r' +• PDF \([0-9\.,]+ [KMG]B\)', type_string)
  if(match is None):
    match = re.search(r' +\([0-9\.,]+ [KMG]B\)', type_string)
  if(match is None):
    return False, type_string
  return True, type_string[ : match.start() ]

def remove_volume_and_number_tail(type_string):
  match = re.search(r' +Vol\. [0-9]+', type_string)
  if(match is None):
    match = re.search(r' +No\. [0-9]+', type_string)
  if(match is None):
    return type_string
  return type_string[ : match.start() ]


def check_if_non_pdf_type_is_ignored(type_string):
  if(type_string[-2:] in ['tv', 'TV']):
    return True # multimedia
  if(type_string[-5:] in ['Radio', 'radio', 'Audio', 'Video']):
    return True # multimedia
  if(type_string[-7:] == 'Podcast'):
    return True # multimedia
  if(type_string[-12:] == 'Audio Issues'):
    return True # multimedia
  if(type_string == 'Books'):
    return True # not interessed in book reviews
  if(type_string[-5:] == 'Forum'):
    return True # neither in events
  if(type_string in [ 'Conference', 'Book Forum', 'Events', 'Live Online Policy Forum', 'City Seminar', 'Live Online Book Forum' ]):
    return True # neither in events
  if(type_string == 'Authors'):
    return True # neither in biography/people/etc
  return False


type_list = page_list_df.type.apply(remove_pdf_tail)

is_pdf = type_list.apply(lambda t : t[0])
type_list = type_list.apply(lambda t : t[1])
type_list = type_list.apply(remove_volume_and_number_tail)

page_list_df['is_pdf'] = is_pdf
page_list_df['processed_type'] = type_list

page_list_df.to_csv('cat-institute-page-list-phase1.csv')



page_list_df['is_ignored'] = page_list_df.type.apply(check_if_non_pdf_type_is_ignored)
page_list_df['id'] = page_list_df.index

page_list_df.to_csv('cat-institute-page-list-phase1.csv', index = False)

"""
note: 210 is 404

-> check the 404's
"""

will_download_indexes = (~page_list_df.is_ignored) & (~page_list_df.is_pdf)
nb_downloaded_articles = will_download_indexes.sum()

print(f'Will download {nb_downloaded_articles} articles')


"""
attributes:
id = index
is_404

time_date
title
author
text_file
html_file
(topics)
(related_content)
(license)
"""

# prepare nice html to text converter
html_to_text_converter = html2text.HTML2Text()
html_to_text_converter.body_width = 0
html_to_text_converter.ignore_links = True

do_remove_multiple_line_returns = False

article_data = page_list_df.copy()
nb_articles = len(article_data)

# scrap loop

article_data_dict = {
  'downloaded' : nb_articles * [ False, ],
  'dl_timestamp' : nb_articles * [ None, ],
  'is_404' : nb_articles * [ False, ],
  'html_file' : nb_articles * [ None, ],
  'date_time' : nb_articles * [ None, ],
  'title' : nb_articles * [ None, ],
  'author' : nb_articles * [ None, ],
  'text_file' : nb_articles * [ None, ],
}

relaunch_index = 0



relaunch_index = 2544


for row_index, row in article_data.iterrows():
  
  if(row_index < relaunch_index):
    continue
  
  if(not will_download_indexes[row_index]):
    continue
  
  link = row.link
  article_data_dict['dl_timestamp'][row_index] = time.time()
  res = requests.get(link)
  
  is_404 = not res.ok
  if(is_404):
    if(do_print):
      print(f'Article {row_index} is 404')
    article_data_dict['is_404'][row_index] = True
    continue
  
  article_data_dict['downloaded'][row_index] = True
  
  soup = BeautifulSoup(res.text, 'html.parser')
  article_file_name_body = f'{row_index:05d}'
  
  html_file_name = article_file_name_body + '.html'
  save_html(html_dir, html_file_name, res.text)
  article_data_dict['html_file'][row_index] = html_file_name
  
  article_soup = soup.find('article')
  if(article_soup is None):
    if(row.processed_type == 'Regulation'): # list of links to pdf files
      if(do_print):
        print(f'Article {row_index} is not an article -> ignored')
      article_data.at[row_index, 'is_ignored'] = True
      continue
    if(article_data.loc[row_index].title == 'Carbon Tax Temperature-Savings Calculator'):
      article_data.at[row_index, 'is_ignored'] = True
      continue
    if(article_data.loc[row_index].processed_type == 'Policy Report'):
      if(do_print):
        print(f'Article {row_index} is a policy report with no article -> ignored')
      article_data.at[row_index, 'is_ignored'] = True
      continue
    if(do_print): # i give up
      print(f'Article {row_index} has no "article" tag -> ignored')
      article_data.at[row_index, 'is_ignored'] = True
      continue
  
  article_header_soup = article_soup.find('header')
  
  if(article_header_soup is None):
    match = article_soup.find('div', 'event-page__meta-info')
    if(match is not None): # is an event, set ignored property
      if(do_print):
        print(f'Article {row_index} is an event -> ignored')
      article_data.at[row_index, 'is_ignored'] = True
      continue
    else: # i give up
      if(do_print):
        print(f'Article {row_index} has an article tag but no header -> ignored')
      article_data.at[row_index, 'is_ignored'] = True
      continue
    #else: will crash
    
  # I accept the fact that date_time might contain extra text such as 'publication'
  # seems to have the following format
  # (date time) • (extra)
  # so would be easy to only keep the date time (time isnt always there, format not consistent)
  try:
    article_data_dict['date_time'][row_index] = clean_text(article_header_soup.find('div', 'meta').text)
  except(AttributeError):
    if(do_print):
      print(f'Article {row_index} has no meta, and probably a different structure -> ignored')
    article_data.at[row_index, 'is_ignored'] = True
    continue
  article_data_dict['title'][row_index] = clean_text(article_header_soup.find('h1').text)
  
  try:
    author = clean_text(article_header_soup.find('div', 'meta-line').find('div', 'meta').find('span').text)
  except(AttributeError):
    try:
      author = clean_text(article_header_soup.find('div', 'meta-line').find('div', 'meta').find('a').text)
    except(AttributeError):
      try:
        author = clean_text(article_header_soup.find('div', 'meta--large').find('span').text)
      except(AttributeError):
        try:
          author = clean_text(article_header_soup.find('div', 'meta--large').find('a').text)
        except(AttributeError):
          if(do_print):
            print(f'Article {row_index}: couldn\'t find author, assuming none')
          author = None
        
  article_data_dict['author'][row_index] = author
  
  article_content = article_soup.find('div', 'field--name-body')
  if(article_content is not None):
    article_text = '\n'.join([ html_to_text_converter.handle(str(p)) for p in article_content.find_all('p') ])
  else:
    article_sections = article_soup.find_all('section')
    if(do_print):
      print(f'Found article ({row_index}) with {len(article_sections)} sections')
    article_text = '\n'.join([ '\n'.join([ html_to_text_converter.handle(str(p)) for p in section.find_all('p') ]) for section in article_sections ])
  
  if(do_remove_multiple_line_returns):
    article_text = re.sub('\n+', '\n', article_text)
  
  text_file_name = article_file_name_body + '.txt'
  save_text(text_dir, text_file_name, article_text)
  article_data_dict['text_file'][row_index] = text_file_name
  
  if(testing and (row_index > test_end)):
    break

"""
inspections:


article_data_dict['downloaded'][:test_end]
article_data_dict['is_404'][:test_end]
article_data_dict['html_file'][:test_end]
article_data_dict['text_file'][:test_end]
article_data_dict['date_time'][:test_end]
article_data_dict['title'][:test_end]
article_data_dict['author'][:test_end]


"""


"""
no author:
Article 183: couldn't find author, assuming none (confirmed)
Article 254: couldn't find author, assuming none
Article 258: couldn't find author, assuming none
Article 273: couldn't find author, assuming none
Article 297: couldn't find author, assuming none
Article 630: couldn't find author, assuming none
Article 659: couldn't find author, assuming none
Article 682: couldn't find author, assuming none
Article 779: couldn't find author, assuming none
Article 907: couldn't find author, assuming none
Article 936: couldn't find author, assuming none

ignored article with article but no header:
Article 909 has an article tag but no header -> ignored
Article 909 has an article tag but no header -> ignored
Article 940 has an article tag but no header -> ignored

ignored because no article tag:
Article 948 has no "article" tag -> ignored


managed errors:
Article 210 is 404

GAVE UP AT SOME POINT

"""

d = article_data.copy()
d.rename(columns = { 'title' : 'link_title',
                     'date' : 'link_date_string',
                     'page' : 'search_page',
                     'index_in_page' : 'search_index_in_page',
                     'type' : 'type_string',
                     'processed_type' : 'item_type',
                     'time_stamp' : 'search_time_stamp', }, inplace = True)


for k in article_data_dict:
  d[k] = article_data_dict[k]




d.rename(columns = { 'dl_timestamp' : 'download_time_stamp', 'date_time' : 'date_time_string',  }, inplace = True)


reordered_columns = [
 'id',
 'search_time_stamp',
 'search_page',
 'search_index_in_page',
 'link_date_string',
 'type_string',
 'item_type',
 'link_title',
 'link',
 'is_pdf',
 'is_ignored',
 'is_404',
 'downloaded', # means the html file is available
 'download_time_stamp',
 'html_file',
 'text_file',
 'date_time_string',
 'title',
 'author',
]

d = d[reordered_columns]

# clean date time string
d['date_time_string'] = d.date_time_string.apply(lambda s : s if (s is None) else s.split(' •')[0])

d.to_csv(articles_data_file, index = False)

"""
>>> d.text_file.count()
1651
"""










