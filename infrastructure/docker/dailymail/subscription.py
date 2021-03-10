#!/usr/bin/env python

# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
from scraper import Tool
from google.cloud import pubsub_v1
from newspaper import Article
import pandas
import pandas_gbq
from pandas_gbq import schema

if __name__ == "__main__":
    url_list = []
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="Google Cloud project ID")
    parser.add_argument("subscription_id", help="Pub/Sub subscription ID")
    parser.add_argument(
        "timeout", default=2, nargs="?", const=1, help="Pub/Sub subscription ID"
    )

    args = parser.parse_args()
    tool = Tool('https://www.dailymail.co.uk/', "linux-academy-project-91522", "hello_topic", gbq_dataset='my_dataset'
                , gbq_table='.my_table2')
    url_list = tool.subscribe_to_urls_topic()

    filtered_urls = [
        url for url in url_list if tool.filter_urls(url)]

    print(f'From the topic  {args.subscription_id} were  grabbed  {len(filtered_urls)} articles  to scrape')

    for url in filtered_urls:

        """ Load the  search URL 
              Create a list of the URLs leading to valid articles 
          """

        article_content = {
            'url': [],
            'title': [],
            'author': [],
            'date': [],
            'tags': [],
            'text': [],
        }


        try:
            article = Article(url)
            article.download()
            article.parse()
        except Exception as e:
            print(e)
            continue

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
            df = pandas.DataFrame.from_dict(article_content)
            pandas_gbq.to_gbq(df, 'my_dataset.my_table2', project_id=args.project_id, if_exists="append", table_schema
            = [{'name': 'url', 'type': 'STRING'}, {'name': 'title', 'type': 'STRING'}, {'name': 'author', 'type': 'STRING'}, {'name': 'date', 'type': 'TIMESTAMP'}, {'name': 'tags', 'type': 'STRING'}, {'name': 'text', 'type': 'STRING'}])
        except Exception as e:
            print(e)


