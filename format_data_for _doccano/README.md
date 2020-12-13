Doccano has very especific data requirements, especially when it comes to the size of the csv files. 


This Python script:

- reads data from the main data folder
- shuffles the data 
- makes sure the data is in the correct format
- splits it into N csvs of 100rows each (doccano-acceptable size)
- saves those csvs in doccano_data 


**ISSUE** due to the shuffling everytime we run the script the output csvs will be different so bE CAREFUL
