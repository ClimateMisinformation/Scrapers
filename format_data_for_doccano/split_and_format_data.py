import os
import pandas as pd
import csv, math

directory = "../data"

files_and_directories = os.listdir(directory)

all_dfs = []
for file in files_and_directories:

    df = pd.read_csv(directory+'/'+file)

    if df.empty:
        print(file + " df is empty")
    else:
        print(file + " appending df ")
        df = df[['url', 'title', 'author', 'date', 'tags', 'text', 'source']]
        print(df.columns)
        all_dfs.append(df)


final_df = pd.concat(all_dfs)


final_df=final_df.sample(frac=1, random_state=1)
final_df = final_df[['text']]

final_df.to_csv("doccano_data.csv")
print(final_df.head())

NUMBER_OF_SPLITS = int(round(final_df.shape[0] / 50, 0))
print(NUMBER_OF_SPLITS)

fileOpens = [open(f"doccano_data/doccano_data{i}.csv","w") for i in range(NUMBER_OF_SPLITS)]
fileWriters = [csv.writer(v, lineterminator='\n') for v in fileOpens]

for i,row in final_df.iterrows():
    fileWriters[math.floor((i/final_df.shape[0])*NUMBER_OF_SPLITS)].writerow(row.tolist())
for file in fileOpens:
    file.close()