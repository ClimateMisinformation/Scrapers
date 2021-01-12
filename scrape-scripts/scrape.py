from base_scraper import base_scraper


def scrape():
    site = "https://www.dailymail.co.uk/textbased/channel-1/index.html"
    mybase = base_scraper.scraper(site)
    mybase.site
    mybase.prepare_urls()
    # mybase.display_article_links()
    mybase.display_timing()


scrape()
