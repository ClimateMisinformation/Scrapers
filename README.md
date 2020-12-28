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



