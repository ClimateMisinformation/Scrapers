"""
Merge the data from the different sources into a single csv file:
- List all the csv files in the directory whose path is given as argument (default: "data/")
- merge them using only the agreed columns
- save the resulting df into a csv file in the current directory (default: "articles.csv")
"""

import glob
import os
import sys

import pandas

#

data_source_path = 'data'
output_file_path = 'articles.csv'

#

for arg in sys.argv[1:]:
  if(os.path.isdir(arg)):
    data_source_path = arg
  else:
    output_file_path = arg

#

column_names = pandas.read_csv('column-description.csv').columns

data_sources = []
for csv_file_path in glob.glob(os.path.join(data_source_path, '*.csv')):
  data_sources.append(pandas.read_csv(csv_file_path)[column_names])

merged_data = pandas.concat(data_sources, ignore_index = True)

merged_data.to_csv(output_file_path, index = False)


"""
test:

import subprocess


f = open('test/a.csv', 'w')
f.write('url,source,title,author,date,tags,text\na,b,c,d,e,f,g')
f.close()

f = open('test/0.csv', 'w')
f.write('url,source,title,author,date,tags,text\n0,1,2,3,4,5,6')
f.close()

r=subprocess.call(['python', 'data-merger.py', 'test', 'test-articles.csv'])

assert(r==0)

f = open('test-articles.csv', 'r')
c = f.read()
f.close()

assert(c == 'url,source,title,author,date,tags,text\na,b,c,d,e,f,g\n0,1,2,3,4,5,6\n')

"""
















