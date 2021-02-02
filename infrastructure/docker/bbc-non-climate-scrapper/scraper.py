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

import requests
from bs4 import BeautifulSoup, UnicodeDammit
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException as slnm_NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException as slnm_StaleElementReferenceException
from selenium.common.exceptions import WebDriverException as slnm_TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import pandas
import re
import argparse
import os


def set_firefox_options() -> Options:
    """Sets firefox options for Selenium.

        Firefox options for headless browser is enabled.

        @Returns Firefox options object

    """
    firefox_opts = Options()
    firefox_opts.add_argument("--headless")
    firefox_opts.add_argument("--no-sandbox")
    firefox_opts.add_argument("--disable-dev-shm-usage")
    return firefox_opts


def extract_urls() -> list:
    """
       Navigates from the  menu on BBC website  to links articles

       @Returns A list of URL to BBC articles
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
    return current_urls


def filter_urls(url_to_check) -> bool:
    """
        Filters the URLs collected so that  only those  from  http://www.bbc.co.uk and https://www.bbc.co.uk
        are kept. To remove the remaining non useful URLs we  assume  every  valid BBC article has a 8 digit
        string in its URI  and discard those which  do not.

        @Returns  bool True  if URL is valid.
    """
    searchobj = re.search(r'[0-9]{8}', url_to_check)
    if ('http://www.bbc.co.uk' or 'https://www.bbc.co.uk' in url_to_check) and (searchobj is not None):
        # print(f'URL added to list is : {url_to_check}  ')
        return True
    else:
        # print('URL is not added to the list, it  may be outside BBC.co.uk news or not an news article')
        return False


if __name__ == "__main__":

    """
        This script scrapes the BBC.co.uk website for  non climate related articles. 
        The entry URL is passed as single arg 'url'. Selenium is used to set cookies and  navigate the menu.  
        A list  of  URLs containing news articles is collected from the entry URL page menu. The expected format of the 
        pages is: 
        
        FORMAT  OF BBC ARTICLE PAGES:
          inside <article>
            inside <header>
              title: h1 #main-heading 
              author: just after the h1: p > span[1] > a text
              date: just after the p: div > dd > span > span[1] > time (attr=) datetime="2020-11-23T22:24:21.000Z"
              tags: just after the div: div > div[1] > div > ul > li[*] > a text
            end </header>
            content: div[*] with attr: data-component="text-block" > p text
            
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
    
       For each URL the article_content dict is saved to a csv file using  a panda dataframe. This is inefficient.
            

    """
    #geckodriver_path = '/usr/bin/geckodriver'
    geckodriver_path = "C:/ProgramData/chocolatey/bin/geckodriver.exe" #(windows)

    """
       create argument parser to receive URL to scrape
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args()
    search_url = args.url
    urls = []

    """
       Remove output file if it already exists
    """
    try:
        os.remove('/tmp/output.csv')
    except OSError as e:
        print("Error deleting: %s - %s." % (e.filename, e.strerror))
        pass

    """
        Initiate the web driver
    """
    firefox_options = set_firefox_options()
    driver = webdriver.Firefox(executable_path=geckodriver_path, options=firefox_options,
                               service_log_path="/tmp/geckodriver.log")
    wait = WebDriverWait(driver, 10)
    print(f'The URL is {search_url}')

    """ 
        Load the  search URL 
        Configure  selenium to accept cookies for the session 
        Count the number  of pages in the topic
        Save the page URLs to a list    
    """
    try:
        driver.get(search_url)
    except slnm_TimeoutException:
        pass
    try:
        WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.ID, "bbccookies-continue-button")))

        driver.find_element_by_id("bbccookies-continue-button").click()
    except slnm_NoSuchElementException:
        pass
    except Exception as e:
        print(e)

    """ Get page count from the webpage pagination menu and  output it to  CLI
              Extract the URI of  articles from the  navigation menu         
    """
    nb_pages = int(driver.find_element_by_class_name('qa-pagination-total-page-number').text)
    print(f'The menu displayed on URL {search_url} leads to  {nb_pages} articles  to scrape')

    """ Create a list of the URLs leading to valid articles  """
    urls = extract_urls()
    urls = filter(filter_urls, urls)
    # print(type(urls))
    #        print(*urls, sep="\n")

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

    article_content = {
        'url': [],
        'title': [],
        'author': [],
        'date': [],
        'tags': [],
        'text': [],
    }

    field_names = ['url', 'title', 'author',  'date', 'tags', 'text']

    for url_index, url in enumerate(urls):
        # print(url)
        response = requests.get(url)
        if not response.ok:
            print(f'Failed request:  {url}, result: {response.status_code}')
            continue
        text = UnicodeDammit.detwingle(response.content)
        page_soup = BeautifulSoup(text, 'html.parser')

        try:
            article_soup = page_soup.find('article')
            header_soup = article_soup.find('header')
            title_soup = header_soup.h1.text
            author_soup = header_soup.p.span.strong.text
            date_soup = header_soup.find('time').text
            text_divs = article_soup.find_all(attrs={"data-component": "text-block"})

            temp = []
            for div in text_divs:
                temp.append(div.text)
            text_soup = " ".join(temp)

            article_content['url'].append(url)
            article_content['title'].append(title_soup)
            article_content['author'].append(author_soup)
            article_content['date'].append(date_soup)
            article_content['tags'].append('')
            article_content['text'].append(text_soup)

            # print(*articleformat, sep="\n")

        except AttributeError:
            continue
        except Exception as e:
            print(e)

        try:
            pandas.DataFrame.from_dict(article_content).to_csv('/tmp/output.csv', index=False)
        except Exception as e:
            print(e)

    """ 
        Quit Selenium driver 
    
    """

    driver.quit()
