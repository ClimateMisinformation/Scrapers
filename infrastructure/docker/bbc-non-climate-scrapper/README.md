# Containerizing the BBC scraping script

## Introduction

  This docker container is built `bbc:latest` image. The image defined in this dir, runs a script which scrapes the BBC.co.uk website for non climate related articles. The results 
  are stored in docker volume  `bbc-vol`  as  `output.csv`
  
## Overview   
  The entry URL is passed as single arg 'url' to scraper.py. Selenium is used to set cookies and  navigate the BBC menu.  
  A list  of  URLs containing news articles is collected from the entry URL page menu. The expected format of the 
  pages is: 
        
  EXPECTED FORMAT  OF BBC ARTICLE PAGES:
  
      inside <article>
        inside <header>
          title: h1 #main-heading 
          author: just after the h1: p > span[1] > a text
          date: just after the p: div > dd > span > span[1] > time (attr=) datetime="2020-11-23T22:24:21.000Z"
          tags: just after the div: div > div[1] > div > ul > li[*] > a text
        end </header>
        content: div[*] with attr: data-component="text-block" > p text
            
  If a URL passes the criteria defined by filter_url(), then it is visited and its content extracted using 
  Beautiful soup.  B. Soup cleans up the inner element text by converting it to UTF8 from the mess it is.
        
  The data extracted is saved to  a  dictionary
        
     article_content = {
       'url': [],
       'title': [],
       'author': [],
       'date': [],
       'tags': [],
       'text': [],
     }
    
  For each URL the article_content dict is added as a row to csv file using  a panda dataframe. 
            
    """

## Usage
The first  step is to build the  image locally and add it to your local docker repo.
    
    docker build -t bbc .

This command deploys a docker container which will run the scraping script and save the collected data into a persistant
docker volume.  

    docker-compose.yml up -d   

The docker volume is "docker_bbc-vol"

    $docker volume ls
    DRIVER    VOLUME NAME
    local     bbc-non-climate-scrapper_bbc-vol

The details of the docker volume like the location on the host system can be seen using: 

    $docker  volume inspect bbc-non-climate-scrapper_bbc-vol
    
    [
        {
            "CreatedAt": "2021-01-24T13:16:29Z",
            "Driver": "local",
            "Labels": {
                "com.docker.compose.project": "bbc-non-climate-scrapper",
                "com.docker.compose.version": "1.27.4",
                "com.docker.compose.volume": "bbc-vol"
            },
            "Mountpoint": "/var/lib/docker/volumes/bbc-non-climate-scrapper_bbc-vol/_data",
            "Name": "bbc-non-climate-scrapper_bbc-vol",
            "Options": null,
            "Scope": "local"
        }
    ]

The docker  container deployed is 

    $docker ps -a | grep bbc-container  
    CONTAINER ID   IMAGE        COMMAND                  CREATED          STATUS         PORTS     NAMES
    bbc-container   bbc:latest   "python /usr/src/app…"   27 minutes ago   Up 5 minutes             bbc-container

    
The progress of the scraping can be seen using

    docker exec bbc-container ls -lat    

Copy data from the docker volume to current directory of the host

    docker cp bbc-non-climate-scrapper_bbc-vol:/tmp/output.csv output.csv


Run the scraper script in a container using a different entry URL 

    docker run --name bbc-non-climate-scrapper_bbc-vol --volume bbc-vol -e URL=http://www.bbc.com  bbc 

```if you have not stopped you will get: 
docker: Error response from daemon: Conflict. The container name "/bbc-container" is already in use by container "3df96f95bd39c177e56a177f1594bacc1516d6381995d3dfddc3f53b1157019f". You have to remove (or rename) that container to be able to reuse that name.
```
## Notes
To run the scraper script directly on your local machine outside of a container you  need to edit scraper.py to redefine the path to geckodriver
 on your local machine. I installed gecko driver on windows 10 using chocolatey and edited line 135 of scraper.py. 

    geckodriver_path = '/usr/bin/geckodriver'  (debian)
    geckodriver_path = C:/ProgramData/chocolatey/bin/geckodriver.exe (windows)