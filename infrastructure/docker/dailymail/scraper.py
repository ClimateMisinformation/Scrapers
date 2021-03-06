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
from google.cloud import pubsub_v1

""" 
    When run as  main script, this script scrapes the URL passed as arg[0] for news articles. 
    If URL passes the criteria defined by filter_url(). i.e. URLs containing in page HTML anchor links, 
    such as  /#respond are ignored.
    
    Each URL is visited and the HTML content is extracted using https://newspaper.readthedocs.io/. 
    Newspaper also cleans inner element text by converting it to UTF8.  
   
    The data extracted populates rows in an "Articles"  dictionary

       article_content = {
       'url': [],
       'title': [],
       'author': [],
       'date': [],
       'tags': [],
       'text': [],
       }
       
   Finally a file  is created in /tmp/output.json. The "Articles" dictionary is converted to a Panda dataframe 
   then saved as JSON.    

   """


class Tool:
    def __init__(self, domain_url, project_id=None, subscription_id=None, timeout=None ):
        self.domain_url = domain_url
        self.project_id = project_id
        self.subscription_id = subscription_id
        self.timeout = timeout

    def __repr__(self):
        return f'Tool("{self.domain_url}", "{self.project_id}", "{self.subscription_id}",{self.timeout})'

    def __str__(self):
        return f'({self.domain_url}, {self.project_id}, {self.subscription_id},{self.timeout})'


    # @staticmethod
    def collect_urls(self) -> list:
        """
           Mocks a browser to go to a news website containing links to articles and collects article URLs which
           it returns as a list.

           Parameters
           ----------
            domain_url: string
                The domain url of a news source. For example bbc.co.uk

           @Returns A list of URL to articles
        """
        current_urls = []

        """ Configure newspaper user agent
        """
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
        config = Config()
        config.browser_user_agent = user_agent
        config.request_timeout = 10
        paper = newspaper.build(self.domain_url, config=config, memoize_articles=False, language='en')

        try:
            for this_article in paper.articles:
                current_urls.append(this_article.url)
        except Exception as e:
            print(e)

        print(f'The news source at URL {self.domain_url} leads to {len(current_urls)} articles  to scrape')

        return current_urls

    @staticmethod
    def filter_urls( url_to_check, domain_url) -> bool:
        """ Filters the URLs collected so that  only those  from base_url domain
            are kept. In-page html links '#' are removed.

            Parameters
            ----------
            url_to_check:  string
                The url which will be compared to the root
            domain_url:  string
                The  root url  of the website we  are  searching

            @Returns: bool
                True  if URL is valid.

        """
        if domain_url in url_to_check and '#' not in url_to_check:
            return True
        else:
            return False

    @staticmethod
    def clean_text(dirty_text) -> bool:
        """ Cleans the text content collected so that text such as boilerplate form labels and empty space are removed
        /n are  kept which  may  cause a problem.

        Parameters
        ----------
        dirty_text: string
           the utf8 text  needing cleaning

        @Returns  bool True  is content is valid
        """
        if len(dirty_text) < 3:
            return False
        else:
            return True

    @staticmethod
    def subscribe_to_urls_topic(project_id, subscription_id, timeout=None) -> list:
        """Receives messages from a google pub/sub topic containing URLS strings from
        a given Pub/Sub subscription and appends them to a list
        which is then returned,

        Parameters
        ----------

        project_id : string
            The google project id where the topic is located
        subscription_id : string
            The google topic subscription  with the  URLs.
        timeout: int
            The time (s) how long the  program will run for

         @Returns list

        """
        # Initialize a list  to hold the URLs
        _urls = []
        # Initialize a Subscriber client
        subscriber_client = pubsub_v1.SubscriberClient()
        # Create a fully qualified identifier in the form of
        # `projects/{project_id}/subscriptions/{subscription_id}`
        subscription_path = subscriber_client.subscription_path(project_id, subscription_id)

        def callback(message):
            print(f"Received {message}.")
            print(message.data)
            _urls.append(message.data.decode("utf-8"))
            # Acknowledge the message. Unack'ed messages will be redelivered.
            # message.ack()
            print(f" Not Acknowledged {message.message_id}.")

        streaming_pull_future = subscriber_client.subscribe(
            subscription_path, callback=callback
        )
        print(f"Listening for messages on {subscription_path}..\n")

        try:
            # Calling result() on StreamingPullFuture keeps the main thread from
            # exiting while messages get processed in the callbacks.
            streaming_pull_future.result(timeout=timeout)
        except:  # noqa
            streaming_pull_future.cancel()

        subscriber_client.close()
        return _urls


    @staticmethod
    def collect_articles(_article_urls) -> dict:
        """ Configures newspaper user agent used to scrape the news-sources. Then receives scrapes the article URLs
        from that  news-source and returns a dict with each row  being an article.

        Parameters
        ----------
        article_urls:  list
            a list  of URLS linking to articles

        @Returns dict

        """
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
        config = Config()
        config.browser_user_agent = user_agent
        config.request_timeout = 10

        articles_content = {
            'url': [],
            'title': [],
            'author': [],
            'date': [],
            'tags': [],
            'text': [],
        }

        # field_names = ['url', 'title', 'author',  'date', 'tags', 'text']

        for url_i, url in enumerate(_article_urls):
            # print(url)
            try:
                bq_article = newspaper.Article(url)
                bq_article.download()
            except Exception as e:
                print(e)
                continue

            try:
                # might not need this
                # soup = BeautifulSoup(article.html, 'html.parser')
                article.parse()

            except Exception as e:
                print(e)

            try:
                articles_content['url'].append(article.url)
                articles_content['title'].append(article.title)
                articles_content['author'].append(article.authors)
                articles_content['date'].append(article.publish_date)
                articles_content['tags'].append('')
                articles_content['text'].append(article.text.replace("\n", " ").replace(",", " "))
            except AttributeError as e:
                print(e)
                continue
            except Exception as e:
                print(e)
        return articles_content


    @staticmethod
    def publish_articles_to_topic():
        """ Publishes the  collected articles to a google pub/sub topic. The topic must  already  exist and
        account authentication be setup

        Parameters
        ----------


        @Returns

        """
        return

    @staticmethod
    def publish_article_to_bigquery(articles_gbq):
        """ Publishes the  collected article  to a google big query table. The table must  already exist and
        account authentication be setup.

        Parameters
        ----------
        articles_gbq : dict
            a dictionary containing the content  of  the scraped articles

        @Returns  None

        """

        try:
            df = pandas.DataFrame.from_dict(articles_gbq)
            print(type(df))
            pandas_gbq.to_gbq(df, 'my_dataset.my_table', project_id=args.project_id, if_exists="append")
        except Exception as e:
            print(e)
        return


    @staticmethod
    def pub(project_id, topic_id, content):

        """ Publishes the  a single url to a google pub/sub topic. The topic must  already  exist and
        account authentication be setup

        Parameters
        ----------

        project_id : string
            The google project id where the topic is located
        subscription_id : string
            The google topic subscription  with the  URLs.
        content: bytearray
            The content  of  the message

         @Returns None

        """

        # Initialize a Publisher client.
        client = pubsub_v1.PublisherClient()
        # Create a fully qualified identifier of form `projects/{project_id}/topics/{topic_id}`
        topic_path = client.topic_path(project_id, topic_id)

        # Data sent to Cloud Pub/Sub must be a bytestring.
        data = bytes(content, 'UTF8')

        # Publish a message, the client returns a future.
        api_future = client.publish(topic_path, data)
        message_id = api_future.result()
        print(f"Published {data} to {topic_path}: {message_id}")
        return

    @staticmethod
    def publish_urls_to_topic(project_id, topic_id, url_list):

        """ Publishes the  collected article urls to a google pub/sub topic. The topic must  already  exist and
        account authentication be setup

        Parameters
        ----------

        project_id : string
            The google project id where the topic is located
        subscription_id : string
            The google topic subscription  with the  URLs.
        url_list: list
            The urls to store
        @Returns None

        """

        for url in url_list:
            pub(project_id, topic_id, url)

        return





if __name__ == "__main__":

    """ This script scrapes the  given URL website for  articles and constructs a list 

        If a URL in the list passes the criteria defined by filter_url(), then it is visited and its content extracted using 
        Beautiful soup.  B. Soup cleans up the inner element text by converting it to UTF8.  
                
        The data extracted is saved to a dictionary with the structure below

        article_content = {
        'url': [],
        'title': [],
        'author': [],
        'date': [],
        'tags': [],
        'text': [],
        }
        
       The rows of the dictionary are then exported and saved as a json file in /tmp/  

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
    output_file = '/tmp/output.json'
    try:
        os.remove(output_file)
    except OSError as e:
        print("Error deleting: %s - %s." % (e.filename, e.strerror))
        pass

    """ Load the  search URL 
        Create a list of the URLs leading to valid articles 
    """
    try:
        tool = Tool(search_url,"linux-academy-project-91522", "hello_topic-sub")
        urls = tool.collect_urls()
        filtered_urls = [
            url for url in urls if tool.filter_urls(url, search_url)]
        print(f'After filtering {search_url} there are  { len(filtered_urls) } articles')
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

    # field_names = ['url', 'title', 'author',  'date', 'tags', 'text']


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
            pandas.DataFrame.from_dict(article_content).to_json(output_file)
        except Exception as e:
            print(e)
