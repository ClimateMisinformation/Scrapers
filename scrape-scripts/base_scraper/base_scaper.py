from bs4 import BeautifulSoup
import requests
import re
import time
from tqdm import tqdm
import pandas
import html2text
import datetime
import sys
from urllib.parse import urlparse
from urllib.parse import urlunparse
from urllib.parse import urljoin


class scraper(object):
    def __init__(self, site):
        self.site = site
        self.site_obj = urlparse(site)
        self.start_time = time.time()
        self.time_taken = 0
        self.urls = []
        self.articles = {
            'url': [],
            'title': [],
            'author': [],
            'date': [],
            'tags': [],
            'text': [],
        }

    def prepare_urls(self):
        print(self.urls)
        response = requests.get(self.site)
        soup = BeautifulSoup(response.text, 'html.parser')
        # body = soup.body
        html_to_text_converter = html2text.HTML2Text()
        html_to_text_converter.body_width = 0
        html_to_text_converter.ignore_links = True

        links = soup.find_all(self.has_class_but_no_id,
                              href=re.compile("text-"))

        for a in links:
            url = a['href']
            full_url = urlunparse((self.site_obj.scheme,
                                   self.site_obj.netloc, url, '', '', ''))

            self.urls.append(full_url)

        for url in tqdm(self.urls):
            try:
                response = requests.get(url)
                page_soup = BeautifulSoup(response.text, 'html.parser')
                content_soup = page_soup.find('div', 'article')
                title = self.clean_text(content_soup.find('h1').text)
                author = self.clean_text(content_soup.find(
                    'p', 'author-section byline-plain').text)
                datestring = page_soup.body.div.span.text
                dateobject = datetime.datetime.strptime(
                    datestring, '%A, %B %d %Y')
                date = dateobject.date()
                tags = 'Neutral'
                text = self.clean_text(content_soup.text)
                self.articles['url'].append(url)
                self.articles['title'].append(title)
                self.articles['author'].append(author)
                self.articles['date'].append(date)
                self.articles['tags'].append(tags)
                self.articles['text'].append(text)
            except Exception:
                print("Unexpected error:", sys.exc_info()[0])
                raise
        # pandas.DataFrame(articles).to_csv('data/dailymail.csv', index=False)
        print("New urls after counting pagination:", len(self.urls))
        self.finish_time = time.time()
        self.time_taken = self.finish_time - self.start_time

    def has_class_but_no_id(self, tag):
        return tag.has_attr('class') and not tag.has_attr('id')

    def clean_text(self, text):
        return re.sub(' $', '', re.sub('^ ', '', re.sub(' +', ' ', text.replace('\n', ' '))))

    def get_articles(self):
        urls = prepare_urls(self)

    def display_article_links(self):
        print(self.articles['url'])

    def display_timing(self):
        print("Time taken: {:.2f} sec".format(
            self.time_taken))
