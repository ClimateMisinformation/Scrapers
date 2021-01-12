import requests
from bs4 import BeautifulSoup as bs


class BBC:
    def __init__(self, url: str):
        article = requests.get(url)
        self.soup = bs(article.content, "html.parser")
        self.body = self.get_body()
        self.title = self.get_title()
        print("Title: " + self.title)

    def get_body(self) -> list:
        body = []
        for p in self.soup.find_all("p"):
            if p.find(class_='css-13k1mrq-PromoHeadline'):
                continue
            if p.find('span'):
                continue
            if p.find('style'):
                continue
            print(list(p.children))
            body += p
        return body

    def get_title(self) -> str:
        return self.soup.find("h1").text


parsed = BBC('https://www.bbc.co.uk/news/health-55365294')

parsed.title
