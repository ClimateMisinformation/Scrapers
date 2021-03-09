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


from scraper import Tool
from flask import Flask, request, escape
from google.cloud import pubsub_v1
from newspaper import Config
from newspaper import Article
import pandas


def scrapeurls(request_body):

    request_json = request_body.get_json(silent=True)
    request_args = request_body.args

    if request_json and 'url' in request_json:
        search_url = request_json['url']
    elif request_args and 'url' in request_args:
        search_url = request_args['url']
    else:
        search_url = 'https://www.dailymail.co.uk/'

    try:
        tool = Tool(search_url, "linux-academy-project-91522", "hello_topic")
        urls = tool.collect_urls()
        filtered_urls = [
            url for url in urls if tool.filter_urls(url)]
        print(f'After filtering {search_url} there are  {len(filtered_urls)} articles')
    except Exception as e:
        print(e)

    tool.publish_urls_to_topic(filtered_urls)

    return 'Scraped URLS'


def publisharticles():

    tool = Tool('https://www.dailymail.co.uk/', "linux-academy-project-91522", "hello_topic")
    try:
        tool.subscribe_to_urls_topic()
    except Exception as e:
        print(e)

    mydict = tool.collect_articles()
    tool.publish_article_to_bigquery(mydict)


    return 'Published Articles'


if __name__ == "__main__":
    app = Flask(__name__)

    @app.route('/', methods=['POST', 'GET'])
    def default():
        return
        #return scrapenews(request)


    # option 2
    app.add_url_rule('/scrapeurls', 'scrapeurls', scrapeurls, methods=['POST', 'GET'], defaults={'request': request})
    app.add_url_rule('/publisharticles', 'publisharticles', publisharticles, methods=['POST', 'GET'])
    app.run(host='127.0.0.1', port=8088, debug=True)
