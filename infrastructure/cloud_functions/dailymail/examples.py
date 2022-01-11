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

"""
This  script  runs a  local server and  exposes two  URLs

http://127.0.0.1:8088/scrapeurls  scrapes article URLs from website  and publishes to google topic

http://127.0.0.1:8088/publisharticles  subscribes to publishes 


#  The values given below  when initialising Tool() are are examples and will be replaced in your environment:
#  domain_url       - for now only dailymail.com is tested
#  project_id       - your google project id
#  gps_topic_id     - create a pub/sub topic in your google project, enter  it here
#  gbq_dataset      - create a big query dataset in your google project, enter  it here
#  gbq_table        - create a big query table in your google project, enter  it here

"""



def scrapeurls(request=request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'url' in request_json:
        search_url = request_json['url']
    elif request_args and 'url' in request_args:
        search_url = request_args['url']
    else:
        search_url = 'https://www.dailymail.co.uk/'

    try:
        tool = Tool(domain_url='https://www.dailymail.co.uk/', project_id="linux-academy-project-91522", gps_topic_id="hello_topic",
                    gbq_dataset='my_dataset'
                    , gbq_table='my_table')
        urls = tool.collect_urls()
        filtered_urls = [
            url for url in urls if tool.filter_urls(url)]
        print(f'After filtering {search_url} there are  {len(filtered_urls)} articles')
    except Exception as e:
        print(e)

    tool.publish_urls_to_topic(filtered_urls)

    return 'Scraped URLS'


def publisharticles():
    tool = Tool(domain_url='https://www.dailymail.co.uk/', project_id="linux-academy-project-91522", gps_topic_id="hello_topic", gbq_dataset='my_dataset'
                , gbq_table='my_table')

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


    app.add_url_rule('/scrapeurls', 'scrapeurls', scrapeurls, methods=['POST', 'GET'], defaults={'request': request})
    app.add_url_rule('/publisharticles', 'publisharticles', publisharticles, methods=['POST', 'GET'])
    app.run(host='127.0.0.1', port=8088, debug=True)
