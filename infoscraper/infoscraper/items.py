import scrapy

class Item(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
    tag = scrapy.Field()
    tag2 = scrapy.Field()
    author = scrapy.Field()
    article_text = scrapy.Field()


