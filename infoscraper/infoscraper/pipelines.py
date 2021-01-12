import pymongo


class InfoscraperPipeline:

    def __init__(self):
        self.conn = pymongo.MongoClient("mongodb+srv://AG:infoscraper@news.ufgln.mongodb.net/articles?retryWrites=true&w=majority")
        db = self.conn['News']
        self.collection = db['articles_table']

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
