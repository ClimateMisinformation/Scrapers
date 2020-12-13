import pandas as pd

df = pd.read_csv('1000_normalised_articles.csv')

print(df.columns)

df = df.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1)

df = df[['url','title','author','date','tags','text','source']]

print(df.columns)

print(df)

df.to_csv('kaggle_dataset.csv', index=False)

df.to_csv('../data/kaggle_dataset.csv', index=False)

