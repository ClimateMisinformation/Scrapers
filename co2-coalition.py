import os

from bs4 import BeautifulSoup
import html2text
import pandas

data_dir = 'co2-coalition'
data_text_dir = os.path.join(data_dir, 'text')
data_file_name = 'co2-coalition.csv'

def make_file_name(index):
  return f'{index:02d}'

def save_text(data_dir, file_path, content):
  f = open(os.path.join(data_dir, file_path), 'w')
  f.write(content)
  f.close()


def get_text(soup, tag, tag_class, do_strip = False):
  text = html_converter.handle(str(soup.find(tag, tag_class)))
  if(do_strip):
    text = text.strip()
  return text



html_converter = html2text.HTML2Text()
html_converter.body_width = 0
html_converter.ignore_images = True

f = open('html/faq.html', 'r')
content = f.read()
f.close()


faq_soup = BeautifulSoup(content, 'html.parser')

entries = {
  'id' : [],
  'title' : [],
  'text_file_name' : [],
}

entry_index = 0
title = html_converter.handle(str(faq_soup.find('span', 'span-title2'))).strip()
content = html_converter.handle(str(faq_soup.find('p', 'p1')))
text_file_name = make_file_name(entry_index) + '.txt'
save_text(data_text_dir, text_file_name, content)

entries['id'].append(entry_index)
entries['title'].append(title)
entries['text_file_name'].append(text_file_name)

entry_index += 1

faq_entries_container = faq_soup.find('div', 'vc_tta-panels-container')
faq_entries = faq_entries_container.find_all('div', 'vc_tta-panel')
print(f'Found {len(faq_entries)} entries')

for entry in faq_entries:
  title = get_text(entry, 'span', 'vc_tta-title-text', do_strip = True).capitalize()
  print(f' Entry {entry_index} : {title}')
  content = get_text(entry.find('div', 'vc_tta-panel-body'), 'div', 'wpb_wrapper')
  text_file_name = make_file_name(entry_index) + '.txt'
  save_text(data_text_dir, text_file_name, content)
  entries['id'].append(entry_index)
  entries['title'].append(title)
  entries['text_file_name'].append(text_file_name)
  entry_index += 1

d = pandas.DataFrame(entries)
d.to_csv(data_file_name, index = False)












