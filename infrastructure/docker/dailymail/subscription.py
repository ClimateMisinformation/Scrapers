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
from scraper import Tools
from google.cloud import pubsub_v1
from newspaper import Article
import pandas
import pandas_gbq

def sub(project_id, subscription_id, timeout=None):
    """Receives messages from a Pub/Sub subscription."""
    urls = []
    # Initialize a Subscriber client
    subscriber_client = pubsub_v1.SubscriberClient()
    # Create a fully qualified identifier in the form of
    # `projects/{project_id}/subscriptions/{subscription_id}`
    subscription_path = subscriber_client.subscription_path(project_id, subscription_id)

    def callback(message):
        print(f"Received {message}.")
        print(message.data)
        urls.append(message.data.decode("utf-8"))
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
    # print(len(urllist))
    subscriber_client.close()
    return urls


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
    url_list = sub(args.project_id, args.subscription_id, args.timeout)
    print(url_list)



    try:
        filtered_urls = [
            url for url in url_list if Tools.filter_urls(url, "https://www.dailymail.co.uk/")]
    except Exception as e:
        print(e)

    print(f'From the topic  {args.subscription_id } were  grabbed  {len(filtered_urls)} articles  to scrape')

    for url in filtered_urls:

        """ Load the  search URL 
              Create a list of the URLs leading to valid articles 
          """
        print(type(url))
        print(url)

        article_content = {
            'url': [],
            'title': [],
            'author': [],
            'date': [],
            'tags': [],
            'text': [],
        }

        # field_names = ['url', 'title', 'author', 'date', 'tags', 'text']
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
            print(type(df))
            pandas_gbq.to_gbq(df, 'my_dataset.my_table', project_id=args.project_id, if_exists="append")
        except Exception as e:
            print(e)


