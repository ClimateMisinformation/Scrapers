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


from scraper import Tools
from flask import Flask, request, escape
from google.cloud import pubsub_v1
from newspaper import Config
from newspaper import Article


def publish(messages):
    project_id = "linux-academy-project-91522"
    topic_name = "hello_topic"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    # print(messages)
    for message in messages:
        data = message.encode('utf-8')
        future = publisher.publish(topic_path, data)
        #print(future.result())
    print(f"Published messages to {topic_path}")


def scrape(req):
    filtered_urls = []
    request_json = req.get_json(silent=True)
    request_args = req.args

    if request_json and 'url' in request_json:
        search_url = request_json['url']
    elif request_args and 'url' in request_args:
        search_url = request_args['url']
    else:
        search_url = 'https://www.dailymail.co.uk/'

    """ Configure newspaper user agent
    """
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
    config = Config()
    config.browser_user_agent = user_agent
    config.request_timeout = 10

    try:
        urls = Tools.extract_urls(search_url)
        filtered_urls = [
            url for url in urls if Tools.filter_urls(url, search_url)
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
        return
        #return scrape(request)


    # option 2
    app.add_url_rule('/scrape', 'scrape', scrape, methods=['POST', 'GET'], defaults={'request': request})
    app.run(host='127.0.0.1', port=8088, debug=True)
