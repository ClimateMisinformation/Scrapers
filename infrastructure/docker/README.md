# Containerizing the scraping scripts

## Introduction

  This directory contains the resources needed to build docker image we  can use  to scape resources. The images defined in the sub dir, run a script which scrapes  website for  articles. The results are stored in a docker volume   as  `output.csv`. 
  
  The BBC scraper is described in detail in its own sub directory because it works slightly differently  to the other, using selenium where the others do not.
  
## Overview   
  The entry URL is passed as single arg 'url' to scraper.py. A list  of  URLs containing news articles is collected from the entry URL page menu. The format of the 
  pages is derived by newspaper3k: 
        
  If a URL passes the criteria defined by filter_url(), then it is visited using https://newspaper.readthedocs.io/en/latest/. The content is extracted using this and Beautiful soup and converted to UTF8.
        
  The data extracted is saved to  a dictionary
        
     article_content = {
       'url': [],
       'title': [],
       'author': [],
       'date': [],
       'tags': [],
       'text': [],
     }
    
  For each URL the article_content dict is added as a row to csv or  json file using  a panda dataframe. 
            


## Usage
### Prerequisites
- Docker: https://www.docker.com/get-started
- Python3:https://www.python.org/downloads/
- Pip3: https://pip.pypa.io/en/stable/installing/  
- Docker-compose: https://docs.docker.com/compose/install/ 

### Steps
The first  step is to build the image locally and add it to your local docker repository. This command uses docker-compose to build and deploy a docker container and docker volume. The container will run the scraping script and save the collected data into a persistent
docker volume.  These steps are to run the breitbart-scraper 

    cd infrastructure/docker/breitbart-scrapper
    docker-compose.yml up -d   

The docker volume is "docker_bbc-vol"

    $docker volume ls
    DRIVER    VOLUME NAME
    local     breitbart-scraper_breitbartnews-vol

The details of the docker volume like the location on the host system can be seen using: 

    $docker  volume inspect breitbart-scraper_breitbartnews-vol
    
    [
        {
            "CreatedAt": "2021-01-24T14:16:44Z",
            "Driver": "local",
            "Labels": {
                "com.docker.compose.project": "breitbart-scraper",
                "com.docker.compose.version": "1.27.4",
                "com.docker.compose.volume": "breitbartnews-vol"
            },
            "Mountpoint": "/var/lib/docker/volumes/breitbart-scraper_breitbartnews-vol/_data",
            "Name": "breitbart-scraper_breitbartnews-vol",
            "Options": null,
            "Scope": "local"
        }
    ]

The docker  container deployed is 

    $docker ps -a   
    CONTAINER ID   IMAGE                  COMMAND                  CREATED         STATUS                  PORTS     NAMES
    6e362ed67264   breitbartnews:latest   "python /usr/src/app…"   2 seconds ago   Up Less than a second             breitbartnewscontainer
    
The progress of the scraping can be seen using this command. The file size of output.csv should increase. 

    docker exec breitbartnewscontainer ls -lat    

Copy data from the docker volume to current directory of the host

     docker cp breitbartnewscontainer:/tmp/output.csv output.csv


Run the scraper script in a container using a different entry URL and the docker CLI 

    docker run --name breitbartnewscontainer --volume breitbartnews-vol -e URL_ENV=http://www.bbc.com   


Run the scraper script outside a container, for example from your IDE. Assume we start at the repository root dir and a 
dir called /tmp/ is writable on your machine.

    python  infrastructure\docker\breitbart-scraper\scraper.py  --url  http://www.bbc.com

  
```if you have not stopped you will get: 
docker: Error response from daemon: Conflict. The container name "/bbc-container" is already in use by container "3df96f95bd39c177e56a177f1594bacc1516d6381995d3dfddc3f53b1157019f". You have to remove (or rename) that container to be able to reuse that name.
```
