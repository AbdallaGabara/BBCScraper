import os
def start_crawling():
    os.chdir('infoscraper')
    os.system('scrapy crawl articles')
