# Climate Battle Cards

Description of directories

## scrape-scripts 

  Web scrapers. See `column-description.csv` for a description of the columns.

  Put your scrapped data in the data directory. 
  
  Once everything has been scrapped run the `data-merger.py` script to merge all the data into one file (normally done only once).

## normalizers 

  scripts by alex to normalize data according to agreed columns (see `column-description.csv`)

## data 

   CSVs of scraped data, organised by data source.
   
## format_data_for_doccano 

  Doccano has very especific data requirements, especially when it comes to the size of the csv files.

  This Python script:

   - reads data from the main data folder
   - shuffles the data
   - makes sure the data is in the correct format
   - splits it into N csvs of 100rows each (doccano-acceptable size)
   - saves those csvs in doccano_data folder 
   
## text_preprocessing 

  Implementation of text cleaning and document embedding 
  
  The document embedding techniques implemented: 
  
  - word2vec + average
  - tfidf

## model_evaluation 

  Evaluation of models and document embedding techniques


# How to contribute 

You can contribute to this repository by solving an issue and suggesting improvements/changes in the code, documentation and project organisation. Look for issues labeled "good-first-issue"

When contributing to this repository, please first communicate with the owners of this repository the change you wish to make via a github-issue or slack https://aiforgoodcommunity.slack.com/#climate-misinformation  before starting to work on it.

If you  are working on an existing issue please assign it to yourself in githbn issues  so that  it is visible what you  are  doing and unneeded replication is avoided. When you  finish working on an issue unassign yourself. 

To start contributing, follow the steps below

    Fork the repo
    Clone the repo
    Create a branch using git checkout -b feature-branch
    Make the required changes
    Create a pull request using below commands
        git add --all
        git commit -m "your commit message"
        git push origin feature-branch
    Go to Repository
    Create Pull Request against master branch
    Add a suitable title and description to the pull request and tag the issue number in Pull Request description, if the pull request is related to some issue logged here: Issues
    You're done. Wait for your code to get reviewed and merged.
    
## Git workflow
We do not yet need to deploy to a production env many times per day so we will use the GitHub flow strategy to merge changes.  It  is described here https://guides.github.com/introduction/flow/. The only GitHub Flow rule is  **Anything in the master branch is deployable**    Each change is reviewed on a feature branch then merged into master. 
