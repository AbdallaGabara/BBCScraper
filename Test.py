import unittest
from infoscraper.infoscraper.spiders import ArticleSpider
from scrapy.http import Request, TextResponse, Response, HtmlResponse


class Test_spider(unittest.TestCase):

    def setUp(self):
        self.spider = ArticleSpider.ArticleSpider()
        pass

    def create_fake_response(self, file_name=None, url=None):
        if not url:
            url = 'http://www.bbc.com'

        request = Request(url=url)
        if file_name is None:
            #you can use any other html file for a BBC main page
            file_name = "BBC_archived.html"

        file = open(file_name, 'r')
        html_content = file.read()
        response = HtmlResponse(url=url, body=html_content, encoding='utf-8')
        file.close()
        return response

    def test_parse(self):
        response = self.create_fake_response()
        items = self.spider.parse(response)
        #access test dictionary by article title, you can add more test cases
        test_array = {'Security fears cloud build-up to Biden inauguration': {'url':'https://www.bbc.com/news/live/world-us-canada-55617421', 'tag': 'news/live', 'tag2': 'world-us-canada','author':'Jude Sheerin', 'Exists': False},
                      'Facebook shuts Uganda government-linked accounts': {'url': 'https://www.bbc.com/news/world-africa-55623722', 'tag': 'news', 'tag2': 'world-africa', 'author': 'N/A', 'Exists': False},
                      "Why 35 years in power isn't enough for this man": {'url': 'https://www.bbc.co.uk/news/world-africa-55550932', 'tag': 'news', 'tag2': 'world-africa', 'author': 'Patience Atuhaire', 'Exists': False},
                      'Democrats start move to impeach Trump again': {'url': 'https://www.bbc.com/news/world-us-canada-55622326', 'tag': 'news', 'tag2': 'world-us-canada', 'author': 'N/A', 'Exists': False},
                      "North Korea throws the gauntlet down for Biden": {'url': 'https://www.bbc.com/news/world-asia-55617502', 'tag': 'news', 'tag2': 'world-asia', 'author': 'Laura Bicker', 'Exists': False},
                      "The Capitol police officer hailed as a 'hero'": {'url': 'https://www.bbc.com/news/world-us-canada-55623752', 'tag': 'news', 'tag2': 'world-us-canada', 'author': 'Holly Honderich', 'Exists': False}
                      }
        for item in items:
            if item['title'] in test_array.keys():
                title=item['title']
                test_array[title]['Exists'] = True
                self.assertEqual(test_array[title]['url'], item['url'],)
                self.assertEqual(test_array[title]['tag'], item['tag'])
                self.assertEqual(test_array[title]['tag2'], item['tag2'])
                self.assertEqual(test_array[title]['author'], item['author'])


            print(item)

        for key in test_array.keys():
            assert(test_array[key]['Exists'])
if __name__ == '__main__':
    unittest.main()