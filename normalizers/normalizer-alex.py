
from datetime import datetime
import os

import pandas


sources = {
'cato-institute' : {
 'details_csv' : 'pages.csv',
 'url' : 'link',
 'author' : 'author',
 'title' : 'title',
 'date' : 'date_time_string',
 'text_file' : 'text_file',
 'tags' : None,
 'text_dir' : 'text',
 'text_processing' : 'html2text(body_width=0,ignore_links=True), <p> -> \\n, rm multiple \\n',
 'original_date_formats' : [ '%B %d, %Y %I:%M%p', '%B %d, %Y' ], #'June 10, 2020 12:25PM',
},
'co2-coalition' : {
 'details_csv' : 'co2-coalition.csv',
 'url' : None,
 'author' : None,
 'title' : 'title',
 'date' : None,
 'text_file' : 'text_file_name',
 'tags' : None,
 'text_dir' : 'text',
 'text_processing' : '<p>:html2text(body_width=0,ignore_image=True)',
 'original_date_formats' : None,
},
'the-bfd' : {
 'details_csv' : 'pages.csv',
 'url' : 'url',
 'author' : 'author',
 'title' : 'title',
 'date' : 'date_time',
 'text_file' : 'text_path',
 'tags' : 'categories',
 'text_dir' : 'text',
 'text_processing' : 'html2text(body_width=0), <p> -> \\n',
 'original_date_formats' : [ '%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%d' ] #'2020-10-20T11:00:00+13:00',
}
}


source_path = 'old-data'
data_path = 'data'

column_names = list(pandas.read_csv('column-description.csv').columns)

def load_text(text_dir, file_name):
  if(file_name == ''):
    return ''
  text_file = open(os.path.join(text_dir, file_name), 'r')
  text = text_file.read()
  text_file.close()
  if(len(text) == 0):
    print('!')
  return text

date_string_exceptions = [
 'Cato Handbook For Policymakers',
 'January/February 2010',
 'Winter 2020',
 'May/June 2009',
 'March/April 2010',
 'March/April 2011',
 'May/June 2011',
 'Winter 2019',
 'January/February 2020',
 'September/October 2019',
 'November/December 2019',
 'Fall 2019',
 'Fall 2020',
 'Spring/Summer 2019',
 'Fall 2018',
]


def check_for_exceptions(date_string):
  if(date_string in date_string_exceptions):
    return True
  x = date_string.split('/')
  if(len(x) == 2):
    x = x[1].split()
    if(len(x) == 2):
      try:
        u = int(x[1])
      except(ValueError):
        pass
      else:
        return True
    else:
      try:
        u = int(x[0])
      except(ValueError):
        pass
      else:
        return True
  x = date_string.split()
  if(len(x) == 2):
    try:
      u = int(x[1])
    except(ValueError):
      pass
    else:
      return True
  return False

def convert_date(date_string, conversion_patterns):
  if(date_string == ''):
   return ''
  is_converted = False
  for pattern in conversion_patterns:
    try:
      converted_datetime = datetime.strptime(date_string, pattern)
    except(ValueError):
      continue
    else:
      is_converted = True
    if(is_converted):
      break
  if(not is_converted):
    if(not check_for_exceptions(date_string)):
      raise Exception(f'unknown format: {date_string}')
    else:
      return ''
  return converted_datetime.strftime('%Y-%m-%d')





for source_name, source_info in sources.items():
  source_data_path = os.path.join(source_path, source_name)
  meta_data_path = os.path.join(source_data_path, source_info['details_csv'])
  meta_data = pandas.read_csv(meta_data_path)
  meta_data.fillna('', inplace = True)
  for column in column_names:
    if(column == 'text'):
      continue
    column_to_rename = source_info[column]
    if(column_to_rename is not None):
      meta_data.rename(columns = { column_to_rename : column }, inplace = True)
    else:
      meta_data[column] = ''
  text_dir_path = os.path.join(source_data_path, source_info['text_dir'])
  meta_data['text'] = meta_data[source_info['text_file']].apply(lambda r : load_text(text_dir_path, r))
  normalized_data = meta_data[meta_data.text.str.len() > 0][column_names]
  if(source_name == 'the-bfd'):
    normalized_data['tags'] = normalized_data['tags'].apply(lambda t : ', '.join(eval(t)))
  if(source_info['original_date_formats'] is not None):
    normalized_data['date'] = normalized_data['date'].apply(lambda d : convert_date(d, source_info['original_date_formats']))
  if(source_name == 'co2-coalition'):
    normalized_data['url'] = 'https://co2coalition.org/frequently-asked-questions/'
    normalized_data['author'] = 'Co2 Coalition'
    normalized_data['date'] = '2020-10-22' # scraping date
  output_file_path = os.path.join(data_path, source_name + '.csv')
  normalized_data.to_csv(output_file_path, index = False)
  del normalized_data
  del meta_data































