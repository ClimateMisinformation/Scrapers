## Introduction
This  is designed to scrape from  different  news sources. The sources are scraped then URLs are filtered 
according to criteria specific to the  news sources. The list  of  good URLs is then published to a google
pub/sub topic.  

A second function can be called to consume the  list  of  good URLs and scrape the article content. This 
content is then published to either a csv file , a JSON file or Google Big Query Table.

## Prerequisites
- A Google account
- Python 3
- Pip3
- Google Services authentication

## Usage
Go to  https://console.cloud.google.com  and select a project. In this example the project  is called "project-id: linux-academy-project-91522" 

### Create a topic 
- projects/linux-academy-project-91522/topics/hello_topic

### Create a subscription
- projects/linux-academy-project-91522/subscriptions/hello_topic-sub 

### Create a dataset and table
Go to https://console.cloud.google.com/bigquery?project=linux-academy-project-91522 and create a datatable. The
dataset in this example is called "my_dataset ". Its URL is https://console.cloud.google.com/bigquery?project=linux-academy-project-91522&p=linux-academy-project-91522&page=dataset&d=my_dataset 

### Create a schema for the data table
In this example the data table is called my_table. The schema for the table, so each article is :

    'name': 'url', 'type': 'STRING'
    'name': 'title', 'type': 'STRING'
    'name': 'author', 'type': 'STRING'
    'name': 'date', 'type': 'TIMESTAMP'
    'name': 'tags', 'type': 'STRING'
    'name': 'text', 'type': 'STRING' 

If you try an import dataframes with a different schema the import fails.
with the message "Please verify that the structure and data types in the DataFrame match the schema of the destination table."
This can also appear  if no data is  present in the dataframe.

### Use the tool

1. Initialize  the tool 

        tool = Tool(domain_url='https://www.dailymail.co.uk/', project_id="linux-academy-project-91522", gps_topic_id="hello_topic", 
    gbq_dataset='my_dataset', gbq_table='my_table')

2. Scrape the  URLs from the  news site and filter them    

        urls = tool.collect_urls()
        filtered_urls = [url for url in urls if tool.filter_urls(url)] 

3. Publish the urls to the topic

        tool.publish_urls_to_topic(filtered_urls)

4. Subscribe to the topic and consume the URLs

        tool.subscribe_to_urls_topic()
    
5. Visit each URL and collect  the content of each article
     
        mydict = tool.collect_articles()

6. Publish the articles to a big query DB

        tool.publish_article_to_bigquery(mydict)


## Quick start

Install  the requirements using pip
    
    pip install requirements

Manually create a google project, a pub/sub topic, a big query dataset, a big query table 
    
    https://console.cloud.google.com/

Configure  the tool in the examples file to match your project

    tool = Tool(domain_url='https://www.dailymail.co.uk/', project_id="linux-academy-project-91522", gps_topic_id="hello_topic", 
    gbq_dataset='my_dataset', gbq_table='my_table')


Run the examples.py file  

    python examples.py
    
Go to http://127.0.0.1:8088/scrapeurls  a HTTP GET will cause the domain to be scraped for article urls and these added
to the topic you created. 

Go to http://127.0.0.1:8088/publisharticles a HTTP GET will subscribe to the topic  get the articles content and publish
 it to the Big Query database you created.
 
In my case this is visible at  
https://console.cloud.google.com/bigquery?project=linux-academy-project-91522&d=my_dataset&p=linux-academy-project-91522&page=dataset
 
   