#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
import tempfile
import os

def set_firefox_options() -> Options:
    """Sets firefox options for Selenium.

        Firefox options for headless browser is enabled.

    """
    firefox_opts = Options()
    firefox_opts.add_argument("--headless")
    firefox_opts.add_argument("--no-sandbox")
    firefox_opts.add_argument("--disable-dev-shm-usage")
    return firefox_opts


if __name__ == "__main__":

    search_urls = {
        'food': r'https://www.bbc.co.uk/news/topics/cp7r8vglgq1t/food',
    }

    firefox_options = set_firefox_options()
    firefox_binary = FirefoxBinary('/usr/bin/firefox')
    driver = webdriver.Firefox(executable_path="/usr/bin/geckodriver", options=firefox_options, service_log_path="/tmp/geckodriver.log")
    wait = WebDriverWait(driver, 10)
    driver.get("http://www.google.com")
    url_list_file_name = 'urls.csv'
    base_url = 'https://www.bbc.co.uk'
    data_file_path = os.path.join('data', 'bbc-non-climate.csv')
    url_count = 0
    urls = []
    page_index = 0
    article_count = 0
    start_index = 1530

    """ Create a tmp dir  to save the result in"""
    tmp_dir = tempfile.mkdtemp()
    url_list_path = os.path.join(tmp_dir, url_list_file_name)
    print('The URL path  is %s' % url_list_path)
