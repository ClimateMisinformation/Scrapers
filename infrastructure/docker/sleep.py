#!/usr/bin/python3
from time import sleep

import html2text
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException as slnm_NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException as slnm_StaleElementReferenceException
from selenium.common.exceptions import WebDriverException as slnm_TimeoutException
from selenium.webdriver.common.by import By
import pandas
import tempfile
import os
import re

def set_firefox_options() -> Options:
    """Sets firefox options for Selenium.

        Firefox options for headless browser is enabled.

    """
    firefox_opts = Options()
    firefox_opts.add_argument("--headless")
    firefox_opts.add_argument("--no-sandbox")
    firefox_opts.add_argument("--disable-dev-shm-usage")
    return firefox_opts


def save_urls(urls_save):
    """
       Saves  the URLs collected to a CSV

    """
    pandas.DataFrame({'url': urls_save}).to_csv(url_list_path, index=False)


def clean_text(text_cleaned):
    """
       Cleans the article text by removing whitespace characters

       @Args     A string of  text
       @Returns  String of text
    """
    return re.sub(' $', '', re.sub('^ ', '', re.sub(' +', ' ', text_cleaned.replace('\n', ' '))))


def extract_urls() -> list:
    """
       Navigates from the  menu on BBC website  to links articles

       @Returns A list of  BBC article URLs
    """
    url_count = 0
    current_urls = []
    # for each page
    for page_index in range(nb_pages):
        # scrape the links
        link_list = driver.find_element_by_tag_name('ol').find_elements_by_tag_name('li')
        for entry in link_list:
            try:
                link = entry.find_element_by_tag_name('a').get_attribute('href')
            except slnm_NoSuchElementException:
                continue
            except slnm_StaleElementReferenceException:
                print(f'Stale element at page {page_index}')
                continue
            current_urls.append(link)
            url_count += 1
        # goto next page
        if page_index < nb_pages - 1:
            try:
                driver.find_element_by_class_name('qa-pagination-next-page').click()
            except slnm_NoSuchElementException:
                # BBC failed to respond
                break
    print(f'Number of articles linked from from menu: {page_index + 1}')
    return current_urls


def filter_urls(url_to_check)-> bool:
    """
        Filters the URLs collected so that  only those  from  http://www.bbc.co.uk and https://www.bbc.co.uk
        are kept. To remove the remaining non useful URLs we  assume  every  valid BBC article has a 8 digit
        string in its URI  and discard those which  do not.

        @Returns  bool True or  False
    """
    searchObj = re.search(r'[0-9]{8}', url_to_check)
    if ('http://www.bbc.co.uk' or 'https://www.bbc.co.uk' in url_to_check) and (searchObj is not None):
        #print(f'URL added to list is : {url_to_check}  ')
        return True
    else:
        #print('URL is not added to the list, it  may be outside BBC.co.uk news or not an news article')
        return False


if __name__ == "__main__":

    search_urls = {
       'https://www.bbc.co.uk/news/topics/cp7r8vglgq1t/food'
    }

    """
       Create a tmp dir  to save the result in
    """
    tmp_dir = tempfile.mkdtemp()
    url_list_path = os.path.join(tmp_dir, 'urls.csv')
    print('The saved file path is %s' % url_list_path)
    urls = []
    base_url = 'https://www.bbc.co.uk'

    """
        Initiate the web driver
    """
    firefox_options = set_firefox_options()
    driver = webdriver.Firefox(executable_path="C:/ProgramData/chocolatey/bin/geckodriver.exe", options=firefox_options,
                               service_log_path="/tmp/geckodriver.log")
    wait = WebDriverWait(driver, 10)

    """
       For each search URL invoke selenium navigate the menu and save the linked to URLS 
       
     """
    for search_url in search_urls:
        """ Load the  search URL 
            Configure  selenium to accept cookies for the session 
            Count the number  of pages in the topic    
        """
        try:
            driver.get(search_url)
        except slnm_TimeoutException:
            continue
        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "bbccookies-continue-button"))
            )
            element = driver.find_element_by_id("bbccookies-continue-button").click()
        except slnm_NoSuchElementException:
            continue
        except Exception as e:
            print(e)

        """ Get page count from the webpage pagination menu and  output it to  CLI
                  Extract the URI of  articles from the  navigation menu         
        """
        nb_pages = int(driver.find_element_by_class_name('qa-pagination-total-page-number').text)
        print(f'The menu displayed on URL that was input leads to  {nb_pages} article pages')

        """ Create a list of the URLs leading to valid articles  """
        urls = extract_urls()
        urls = filter(filter_urls, urls)
        print(type(urls))
#        print(*urls, sep="\n")

        """ Save a list of  scraped URLs """
        #save_urls(urls)

    """
        FORMAT  OF BBC ARTICLE PAGES:
          inside <article>
            inside <header>
              title: h1 #main-heading 
              author: just after the h1: p > span[1] > a text
              date: just after the p: div > dd > span > span[1] > time (attr=) datetime="2020-11-23T22:24:21.000Z"
              tags: just after the div: div > div[1] > div > ul > li[*] > a text
            end </header>
            content: div[*] with attr: data-component="text-block" > p text
        """

    articleformat = {
        'url': [],
        'title': [],
        'author': [],
        'date': [],
        'tags': [],
        'text': [],
    }

    for url_index, url in enumerate(urls):
        print(url)
        response = requests.get(url)
        if not response.ok:
            print(f'Failed request:  {url}, result: {response.status_code}')
            continue

        page_soup = BeautifulSoup(response.text, 'html.parser')

        try:
            article_soup = page_soup.find('article')
            header_soup = article_soup.find('header')
            title_soup = header_soup.h1.text
            author_soup = header_soup.p.text
            date_soup = header_soup.find('time')
            text_divs = article_soup.find_all(attrs={"data-component": "text-block"})
            temp = []
            for div in text_divs:
                temp.append(div.text)
            text_soup = " ".join(temp)


            articleformat['url'].append(url)
            articleformat['title'].append(title_soup)
            articleformat['author'].append(author_soup)
            articleformat['date'].append(date_soup)
            #articleformat['tags'].append(tags)
            articleformat['text'].append(text_soup)

            #print(articleformat)
            #print(*articleformat, sep="\n")

        except AttributeError:
            continue

    """ 
        Quit Selenium driver 
    
    """

    driver.quit()