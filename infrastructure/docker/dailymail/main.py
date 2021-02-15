#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import scraper
from flask import Flask, request, escape
from google.cloud import pubsub_v1


def publish(messages):
    print("foo")
    project_id = "linux-academy-project-91522"
    topic_name = "dailymail-url"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    for message in messages:
        future = publisher.publish(
            topic_path, data=message.encode('utf-8')
        )


def scrape(a_request):

    filtered_urls = []
    request_json = a_request.get_json(silent=True)
    request_args = a_request.args

    if request_json and 'url' in request_json:
        search_url = request_json['url']
    elif request_args and 'url' in request_args:
        search_url = request_args['url']
    else:
        search_url = 'https://www.dailymail.co.uk/'

    """ Load the  search URL 
           Create a list of the URLs leading to valid articles 
       """
    try:
        urls = scraper.extract_urls(search_url)
        print(urls)
        filtered_urls = [
            url for url in urls if filter_urls(url)
        ]
        print(f'The menu displayed on URL {search_url} leads to  {len(filtered_urls)} articles  to scrape')
    except Exception as e:
        print(e)
    publish(filtered_urls)
    return 'Scraped URLS'


def export(filtered_urls):

    article_content = {
        'url': [],
        'title': [],
        'author': [],
        'date': [],
        'tags': [],
        'text': [],
        }

    for url_index, url in enumerate(filtered_urls):
        print(url)
        try:
            article = newspaper.Article(url)
            article.download()
        except Exception as e:
            print(e)
            continue

        try:
            article.parse()
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
            pandas.DataFrame.from_dict(article_content).to_csv(outputfile, index=False)
        except Exception as e:
            print(e)

    return 'Saved articles '
    # return 'Saved articles from '.format(escape(search_url))


if __name__ == "__main__":
    app = Flask(__name__)

    @app.route('/', methods=['POST', 'GET'])
    def default():
        return scrape(request)


    # option 2
    app.add_url_rule('/scrape', 'scrape', scrape, methods=['POST', 'GET'], defaults={'request': request})

    app.run(host='127.0.0.1', port=8088, debug=True)
