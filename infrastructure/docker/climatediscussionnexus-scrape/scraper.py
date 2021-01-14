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



def extract_urls(base_url) -> list:
    """
       Navigates from the  menu on website  to links articles

       @Returns A list of URL to articles
    """
    current_urls = []
    bb_paper = newspaper.build(base_url)
    print(bb_paper.size())
    for art in bb_paper.articles:
        print(art.url)
        current_urls.append(art.url)
    return current_urls


def filter_urls(url_to_check, base_url) -> bool:
    """
        Filters the URLs collected so that  only those  from  http://www.bbc.co.uk and https://www.bbc.co.uk
        are kept. To remove the remaining non useful URLs we  assume  every  valid BBC article has a 8 digit
        string in its URI  and discard those which  do not.

        @Returns  bool True  if URL is valid.
    """
    if base_url in url_to_check:
        return True
    else:
        return False


if __name__ == "__main__":

    """
        This script scrapes the https://climatediscussionnexus.com/ website for   articles. 
        The entry URL is passed as single arg 'url'. https://newspaper.readthedocs.io is used to set cookies and 
        navigate the menu.  
        A list  of  URLs containing news articles is collected from the entry URL page menu. The expected format of the 
        pages is: 
        
        FORMAT  OF ARTICLE PAGES:
      
            
        If a URL passes the criteria defined by filter_url(), then it is visited and its content extracted using 
        Newspaper which cleans up the inner element text by converting it to UTF8 from the mess may be.
        
        The data extracted is saved to  a  dictionary
        
        article_content = {
        'url': [],
        'title': [],
        'author': [],
        'date': [],
        'tags': [],
        'text': [],
        }
    
       For each URL the article_content dict is saved to a csv file using  a panda dataframe. 
            

    """

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
        os.remove('output.csv')
    except OSError as e:
        print("Error deleting: %s - %s." % (e.filename, e.strerror))
        pass

    """ 
        Load the  search URL 
        Count the number  of pages in the topic
        Create a list of the URLs leading to valid articles 
    """
    try:
        urls = extract_urls(search_url)
        print(f'The menu displayed on URL {search_url} leads to  { len(urls) } articles  to scrape')
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

    for url_index, url in enumerate(urls):
        print(url)
        try:
            article = newspaper.Article(url)
            article.download()
        except Exception as e:
            print(e)
            continue

        try:
            article.parse()
            article_content['url'].append(article.url)
            article_content['title'].append(article.title)
            article_content['author'].append(article.authors)
            article_content['date'].append(article.publish_date)
            article_content['tags'].append('')
            article_content['text'].append(article.text)

        except AttributeError:
            continue
        except Exception as e:
            print(e)

        try:
            pandas.DataFrame.from_dict(article_content).to_csv('output.csv', index=False)
        except Exception as e:
            print(e)

