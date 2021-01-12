import pymongo
import scrapy
import os
from scrapy.crawler import Crawler, CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from infoscraper.infoscraper.spiders import ArticleSpider
from infoscraper.infoscraper.pipelines import InfoscraperPipeline
from infoscraper.start_crawling import start_crawling

if __name__ == '__main__':

    # Start Crawling the Website and Store results in a Database
    decision = None
    while (decision != "Y") and (decision != "N"):
        decision = input("Do you want to update the database with new articles or use the archive? Y/N")

    if decision == "Y":
        start_crawling()

    # Connecting to database
    connect = pymongo.MongoClient("mongodb+srv://AG:infoscraper@news.ufgln.mongodb.net/articles?retryWrites=true&w=majority")
    db = connect['News']
    collection = db['articles_table']

    # Get keyword from our user
    keyword = input("Enter your keyword of interest: ")

    # Query the database for the keyword yof interest by checking if the keyword in the article, its title, and its tags
    query = {
    "$or":
    [{"article_text": {
    "$regex": keyword,
    "$options": 'i'
    }}
    ,
    {"title": {
    "$regex": keyword,
    "$options": 'i'  # case-insensitive
    }}
    ,
    {"tag": {
    "$regex": keyword,
    "$options": 'i'  # case-insensitive
    }}
    ,
    {"tag2": {
    "$regex": keyword,
    "$options": 'i'  # case-insensitive
    }}
    ]
    }
    query_output = collection.find(query)

    # Printing the results
    if len(query) == 0:
        print("Your search yielded no results!")
    else:
        for row in query_output:
            print("title: {} \nauthor: {} \ntag1: {} \ntag2: {} \nurl: {} \narticle: \n{} \n ".format(row['title'], row['author'], row['tag'], row['tag2'], row['url'], row['article_text']))
