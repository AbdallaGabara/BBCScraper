from infoscraper.infoscraper.spiders import ArticleSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os


class Run_Spiders:
    def __init__(self):
        settings_file_path = 'infoscraper.infoscraper.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.process = CrawlerProcess(get_project_settings())
        self.spider = ArticleSpider.ArticleSpider

    def run_spiders(self):
        self.process.crawl(self.spider)
        self.process.start()