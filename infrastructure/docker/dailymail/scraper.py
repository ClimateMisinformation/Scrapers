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
import pandas
import re
import argparse
import os
import newspaper
from newspaper import Config
from newspaper import Article
from newspaper.utils import BeautifulSoup


class Tools:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def extract_urls(base_url) -> list:
        """
           Navigates from the  menu on website  to links articles

           @Returns A list of URL to articles
        """
        current_urls = []
        """ Configure newspaper user agent
           """
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
        config = Config()
        config.browser_user_agent = user_agent
        config.request_timeout = 10
        paper = newspaper.build(base_url, config=config, memoize_articles=False, language='en')
        for this_article in paper.articles:
            current_urls.append(this_article.url)
        return current_urls

    @staticmethod
    def filter_urls(url_to_check, srch_url) -> bool:
        """ Filters the URLs collected so that  only those  from base_url domain
            are kept. In-page html links '#' are removed.
            @Returns  bool True  if URL is valid.
        """
        if srch_url in url_to_check and '#' not in url_to_check:
            return True
        else:
            return False

    @staticmethod
    def clean_text(dirty_text):
        """ Cleans the text content collected so that text such as boilerplate form labels and empty space are removed
        /n are  kept which  may  cause a problem.
        @Returns  bool True  is content is valid
        """
        if len(dirty_text) < 3:
            return False
        else:
            return True


if __name__ == "__main__":

    """ This script scrapes the   website for  articles. 

        If URL passes the criteria defined by filter_url(), then it is visited and its content extracted using 
        Beautiful soup.  B. Soup cleans up the inner element text by converting it to UTF8.  
        URLs ending with a /#respond  are collected which needs to be stopped.
        
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

    """
       create argument parser to receive URL to scrape
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--url",  help="base URL of the news source")
    args = parser.parse_args()
    if args.url:
        search_url = args.url
    elif os.environ.get('URL_ENV'):
        search_url = os.environ.get('URL_ENV')
    else:
        search_url = 'https://www.dailymail.co.uk/'
        print("No news source is defined in the script arguments. "
              "Setting search_url = 'https://www.dailymail.co.uk/' ")
    urls = []
    filtered_urls = []

    """ Remove output file if it already exists
    """
    output_file = '/tmp/output.csv'
    try:
        os.remove(output_file)
    except OSError as e:
        print("Error deleting: %s - %s." % (e.filename, e.strerror))
        pass

    """ Load the  search URL 
        Create a list of the URLs leading to valid articles 
    """
    try:
        urls = Tools.extract_urls(search_url)
        filtered_urls = [
            url for url in urls if Tools.filter_urls(url, search_url)]
        print(f'The menu displayed on URL {search_url} leads to  { len(filtered_urls) } articles  to scrape')
    except Exception as e:
        print(e)

    article_content = {
            'url': [],
            'title': [],
            'author': [],
            'date': [],
            'tags': [],
            'text': [],
        }

    field_names = ['url', 'title', 'author',  'date', 'tags', 'text']

    for url_index, url in enumerate(filtered_urls):
        # print(url)
        try:
            article = newspaper.Article(url)
            article.download()
        except Exception as e:
            print(e)
            continue

        try:
            #  might not need this
            article.parse()
            soup = BeautifulSoup(article.html, 'html.parser')
        except Exception as e:
            print(e)

        try:
            article_content['url'].append(article.url)
            article_content['title'].append(article.title)
            article_content['author'].append(article.authors)
            article_content['date'].append(article.publish_date)
            article_content['tags'].append('')
            article_content['text'].append(article.text.replace("\n", " ").replace(",", " "))
        except AttributeError as e:
            print(e)
            continue
        except Exception as e:
            print(e)

        try:
            pandas.DataFrame.from_dict(article_content).to_csv(output_file, index=False)
        except Exception as e:
            print(e)