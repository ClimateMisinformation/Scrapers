
from datetime import datetime
import os

import pandas


sources = {
  'bbc-non-climate' : 'BBC News',
  'breibart-defense' : 'Breibart News Network',
  'the-onion-politics' : 'The Onion',
}


data_dir_path = 'data'



for data_name, source in sources.items():
  data_file_path = os.path.join(data_dir_path, data_name + '.csv')
  data = pandas.read_csv(data_file_path)
  data.fillna('', inplace = True)
  data['source'] = source
  data.to_csv(data_file_path, index = False)
  del data

































