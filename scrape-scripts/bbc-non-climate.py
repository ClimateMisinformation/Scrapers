# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
import requests
import html2text
import pandas
import tempfile
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException as slnm_NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException as slnm_StaleElementReferenceException
from selenium.common.exceptions import WebDriverException as slnm_TimeoutException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait


def set_firefox_options() -> Options:
    """Sets firefox options for Selenium.

        Firefox options for headless browser is enabled.

    """
    firefox_opts = Options()
    firefox_opts.add_argument("--headless")
    firefox_opts.add_argument("--no-sandbox")
    firefox_opts.add_argument("--disable-dev-shm-usage")
    return firefox_opts


def save_data(data_file_path_saved, articles_saved):
    articles_df = pandas.DataFrame(articles_saved)
    articles_df.to_csv(data_file_path_saved, index=False)


def clean_text(text_cleaned):
    return re.sub(' $', '', re.sub('^ ', '', re.sub(' +', ' ', text_cleaned.replace('\n', ' '))))


def check_if_url_must_be_skipped(url_to_check):
    if url_to_check[:len(base_url)] != base_url:
        print('Article is outside BBC news')
        print(f'URL to check: {url_to_check} , BASE_URL is: {base_url}   ')
        return True
    elif url_to_check[:32] == 'https://www.bbc.co.uk/newsround/':
        print('Newsround article')
        return True
    elif url_to_check[:33] == 'https://www.bbc.co.uk/programmes/':
        print('Programmes article')
        return True
    elif url_to_check[:37] == 'https://www.bbc.co.uk/news/resources/':
        print('Resources article')
        return True
    elif url_to_check[:32] == 'https://www.bbc.co.uk/news/live/':
        print('Live article')
        return True
    elif url_to_check[:28] == 'https://www.bbc.co.uk/sport/':
        print('Sport article')
        return True
    elif url_to_check == 'https://www.bbc.co.uk/news/scotland':
        print('Page not an article')
        return True
    elif url_to_check.find('?') > 0:
        print('Has ? in url')
        return True
    else:
        return False


if __name__ == "__main__":

    search_urls = {
        'food': r'https://www.bbc.co.uk/news/topics/cp7r8vglgq1t/food',

    }

    firefox_options = set_firefox_options()
    driver = webdriver.Firefox(options=firefox_options)
    wait = WebDriverWait(driver, 10)
    tmp_dir = ''
    url_list_file_name = 'urls.csv'
    base_url = 'https://www.bbc.co.uk'
    data_file_path = os.path.join('data', 'bbc-non-climate.csv')
    firefox_bin_path = '/usr/bin/firefox'
    geckodriver_path = '/usr/bin/geckodriver'
    firefox_binary = FirefoxBinary(firefox_bin_path)
    capabilities = DesiredCapabilities.FIREFOX.copy()
    capabilities['marionette'] = True
    url_count = 0
    urls = []
    page_index = 0
    article_count = 0
    start_index = 1530

    """
    FORMAT  OF SEARCHED PAGES
    
    List of articles:
      <ol class="gs-u-m0 gs-u-p0 lx-stream__feed qa-stream"
      <li class="lx-stream__post-container placeholder-animation-finished">
    
    Some <li> contain a video without  a URL link
        
    Links:
      <a class="qa-heading-link lx-stream-post__header-link"
       href=/news/CATEG-NUMBER>...
    
    
    Pages:
    <div class="lx-pagination__nav ..."
    
        <span class="lx-pagination__page-number qa-pagination-current-page-number">
        CURRENT PAGE NUMBER
            <span class="lx-pagination__page-number qa-pagination-total-page-number">
        
        TOTAL NB PAGES
            <a class="lx-pagination__btn gs-u-mr+ qa-pagination-next-page lx-pagination__btn--active"
        LINK TO NEXT PAGE
            href=/false/page/2
        
    """

    " For each search URL invoke selenium navigate the menu and save the linked to URLS "
    for topic, search_url in search_urls.items():
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
                ec.element_to_be_clickable((By.ID, "bbccookies-continue-button"))
            )
            element = driver.find_element_by_id("bbccookies-continue-button").click()
        except slnm_NoSuchElementException:
            continue
        except Exception as e:
            print(e)

        """ Get page count from the pagination menu and  output it to  CLI
            Extract the URI of  articles from the  navigation menu         
            
        """
        nb_pages = int(driver.find_element_by_class_name('qa-pagination-total-page-number').text)
        print(f'Topic "{topic}" has {nb_pages} result pages')
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
                urls.append(link)
                url_count += 1
                if (url_count + 1) % 120 == 0:
                    save_urls(urls)
            # goto next page
            if page_index < nb_pages - 1:
                try:
                    driver.find_element_by_class_name('qa-pagination-next-page').click()
                except slnm_NoSuchElementException:
                    # BBC failed to respond
                    break
        print(f'Actual number of pages: {page_index + 1}')

    # (crashed at some point with 4079 urls, half of them link to the faq)
    # last valid article is about covid-19

    """ Save a list of  scraped URLs """
    save_urls(urls)

    """ Remove the FAQ content"""
    url_df = pandas.read_csv(url_list_path)
    url_df = url_df[url_df.url != r'http://www.bbc.co.uk/faqs/questions/bbc_online/sharing']
    url_df.to_csv(url_list_path, index=False)

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

    html_to_text_converter = html2text.HTML2Text()
    html_to_text_converter.body_width = 0
    html_to_text_converter.ignore_links = True
    column_names = pandas.read_csv('column-description.csv').columns
    article_urls = pandas.read_csv(url_list_path)

    articles = {
        'url': [],
        'title': [],
        'author': [],
        'date': [],
        'tags': [],
        'text': [],
    }


    for url_index, url in enumerate(article_urls.url):
        if url_index < start_index:
            continue
        if check_if_url_must_be_skipped(url):
            print(f'Article URL not conforming: {url_index} : {url} - SKIPPED')
            continue
        """ Get  the  data """
        response = requests.get(url)
        if not response.ok:
            print(f'Failed request: {url_index} : {url}, result: {response.status_code}')
            continue
        page_soup = BeautifulSoup(response.text, 'html.parser')
        article_soup = page_soup.find('article')
        """extract and article title, author, date, tags"""
        header_soup = article_soup.find('header')
        if header_soup is None:
            print(f'Article has no header: {url_index} : {url} - SKIPPED')
            continue
        title = clean_text(header_soup.find('h1').text)
        # check
        nb_p = len(header_soup.find_all('p'))
        if nb_p > 1:
            raise Exception(f'several p in header for {url_index} : {url}')
        try:
            author = clean_text(header_soup.find('p').find('strong').text)
        except AttributeError:
            print(f'(No author found for article {url_index} : {url})')
            author = ''
        if author[:3] == 'By ':
            author = author[3:]
        """ Check the article is contains 1 time/date of publication """
        nb_times = len(header_soup.find_all('time'))
        if nb_times > 1:
            raise Exception(f'Article {url_index} : {url} has several times')

        date = header_soup.find('time').attrs['datetime'][:10]
        # check
        nb_ul = len(header_soup.find_all('ul'))
        if nb_ul > 1:
            raise Exception(f'{url_index} : {url} morArticle is outside BBC newse than one ul in header')
        try:
            tag_list = [s.find('a').text for s in header_soup.find_all('li')]
        except AttributeError:
            tag_list = []
        tags = clean_text(', '.join(tag_list))
        """ Extract content from the article & convert  it to text """
        div_list = article_soup.find_all('div')
        text_ps = []
        for div_soup in div_list:
            try:
                data_component = div_soup.attrs['data-component']
            except KeyError:
                continue
            if data_component != 'text-block':
                continue
            text_ps += [clean_text(html_to_text_converter.handle(str(p_soup))) for p_soup in div_soup.find_all('p')]
        text = '\n'.join(text_ps)
        if len(text) == 0:
            raise Exception(f'{url_index} : {url} article has no content')
        """ Append scraped  values  to the article object """
        articles['url'].append(url)
        articles['title'].append(title)
        articles['author'].append(author)
        articles['date'].append(date)
        articles['tags'].append(tags)
        articles['text'].append(text)
        """ Save the  article object to CSV """
        article_count += 1
        if (article_count % 120) == 0:
            print(f'Saving {article_count} articles (last {url_index} : {url})')
            save_data(data_file_path, articles)

    save_data(data_file_path, articles)

    """ Display some stats  on the cli """
    articles = pandas.read_csv(data_file_path)
    climate_phrases = ['climate', 'global warming', 'carbon dioxyde', 'renewable', 'CO2', 'coal', 'carbon',
                       'rising temperatures', ]
    article_mention_counts = {phrase: sum(articles.text.str.lower().str.find(phrase) > 0) for phrase in climate_phrases}
    print('Mention counts:')
    for p, c in article_mention_counts.items():
        print(f'{p} : {c}')

    """ Quit Selenium driver """

    driver.quit()


    """
    # after: check articles containing the following (but KEEP them if not climate change related)
    
    climate
    global warming
    co2
    carbon
    renewable
    weather
    temperature
    """
