import scrapy
from scrapy.http import HtmlResponse
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
import requests
import re
from twisted.internet import reactor

from ..items import Item

class ArticleSpider(scrapy.Spider):

    name = 'articles'
    start_urls = ['https://www.bbc.com']

    def parse(self, response):

        items = Item()
        articles = response.css('a.block-link__overlay-link::text').extract()

        # Extract all the articles urls from the main page to be inspected later
        urls = response.xpath('//a[contains(@class, "media__link")]/@href').getall()
        article_texts = []
        tags = []
        tags_2 = []
        authors = []

        for i in range(len(urls)):
            if urls[i].find(".") < 0:                      # Check if the url is a partial path or a full url
                urls[i] = self.start_urls[0] + urls[i]     # If it is a partial path convert it to a full url

            tag = re.search('((?<=com/)|(?<=uk/))(.*)(?=/[a-z])', urls[i])  # Search for a first tag in the url
            tag_2 = None
            if tag is None:
                tag = 'N/A'
            else:
                tag = tag.group(0)
                tag_2 = re.search('(?<={}/)(.*)((?=/)|(?=-[0-9]))'.format(tag), urls[i])   # Search for a second tag in the url
            if tag_2 is None:
                tag_2 = 'N/A'
            else:
                tag_2 = tag_2.group(0)

            # Adding tags to the tags list
            tags.append(tag)
            tags_2.append(tag_2)

        for i, url in enumerate(urls, start=0):
            article_text = ""
            author = None
            request = requests.get(url)
            article_response = HtmlResponse(url=url, body=request.content)

            # Extract paragraphs/text blocks and the name of authors (if available) from the HTML
            text_array = article_response.xpath('//article/div/p/span[@data-reactid]//text() | //div[@class="css-83cqas-RichTextContainer e5tfeyi2"]/p/text() | //div[@class="body-content"]/p//text() | //div[@class="body-text-card__text body-text-card__text--future body-text-card__text--drop-capped body-text-card__text--flush-text"]/div/p//text() |//div[@class="body-text-card__text body-text-card__text--culture body-text-card__text--drop-capped body-text-card__text--flush-text"]/div/p//text() | //div[@class="body-text-card__text body-text-card__text--worklife body-text-card__text--drop-capped body-text-card__text--flush-text"]/div/p//text()').getall()
            author = article_response.xpath('//span[@class ="qa-contributor-name gel-long-primer"]//text() | //p[@class="lx-commentary__meta-reporter gel-long-primer"]//text() | //span[@class="index-body"]//text() | //a[@class="author-unit__text b-font-family-serif"]//text() | //a[@class="author-unit__text b-font-family-serif"]//text() | //p[@class="css-1pjc44v-Contributor e5xb54n0"]/span/strong//text()').get()

            # Concatenate the paragraphs into one string (article_text)
            for paragraph in text_array:
                article_text = article_text + "\n" + paragraph


            if author is None:    # If no author is named
                author = 'N/A'
            else:
                # Get the author's name by removing the word "By"/"by" and whatever precedes it
                t_author = re.search('((?<=by )|(?<=By ))(.*)', author)
                if t_author is not None:
                    author = t_author.group(0)

            article_texts.append(article_text)
            authors.append(author.strip())      # strip the author's name of any unnecessary spacing

        for i, article in enumerate(articles, start=0):

            # Remove unnecessary spacing and special characters from the article title
            title = re.search("[^\s*].*[^\s*]", article.replace("\n", "")).group(0)

            items['title'] = title
            items['url'] = urls[i]
            items['tag'] = tags[i]
            items['tag2'] = tags_2[i]
            items['author'] = authors[i]
            items['article_text'] = article_texts[i]
            yield items
