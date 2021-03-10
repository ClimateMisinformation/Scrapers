## Introduction
This  is designed to scrape from  different  news sources. The sources are scraped then URLs are filtered 
according to criteria specific to the  news sources. The list  of  good URLs is then published to a google
pub/sub topic.  

A second function can be called to consume the  list  of  good URLs and scrape the article content. This 
content is then published to either a csv file , a JSON file or Google Big Query Table.

## Prerequisites
- A Google account


## Usage
Goto  https://console.cloud.google.com  and select a project. In this example the project  is called "project-id: eng-lightning-244220" 

### Create a topic 
- projects/eng-lightning-244220/topics/dailymail-urls

### Create a subscription
- projects/eng-lightning-244220/subscriptions/dailymail-urls-sub 

### Create a datatable
Go to https://console.cloud.google.com/bigquery?project=eng-lightning-244220 and create a datatable. The
datatable in this example is called "CollectedURLs". Its URL is https://console.cloud.google.com/bigquery?project=eng-lightning-244220&p=eng-lightning-244220&page=dataset&d=CollectedURLs

### Create a schema for the data table
The schema would be:

    'name': 'url', 'type': 'STRING'
    'name': 'title', 'type': 'STRING'
    'name': 'author', 'type': 'STRING'
    'name': 'date', 'type': 'TIMESTAMP'
    'name': 'tags', 'type': 'STRING'
    'name': 'text', 'type': 'STRING' 

### Use the tool

1. Initialize  the tool 

        tool = Tool("https://www.dailymail.co.uk/", "project=eng-lightning-244220", "dailymail-urls")

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


## Examples
