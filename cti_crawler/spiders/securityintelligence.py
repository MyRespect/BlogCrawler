import scrapy, os, json
from cti_crawler.items import CtiCrawlerItem
from pymysql.converters import escape_string

from selenium import webdriver

web_name='securityintelligence'
web_address='https://securityintelligence.com/category/x-force/'

class CybersecurityAttSpider(scrapy.Spider):
    name = 'securityintelligence'
    # allowed_domains = ['securityintelligence.com']
    start_urls = ['https://securityintelligence.com/wp-json/category/results?cat=97&page={}'.format(str(i))for i in range(1, 85)]

    def read_exist_urls(self, file_path): # read the latest 120 urls
        urlset=[]
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                urlset = f.readlines()
        except FileNotFoundError:
            print("Sorry, the file"+file_path+" does not exist.")
        return urlset

    def parse(self, response):
        print("procesing:"+response.url)
        if response.text:
            json_data=json.loads(response.text)
            json_item=json_data["items"]
            urlset=self.read_exist_urls('./cti_crawler/urls/'+web_name+'.txt')
            if len(json_item)!=0:
                for item in json_item:
                    url=item["permalink"]
                    if url+'\n' not in urlset:
                        with open('./cti_crawler/urls/'+web_name+'.txt', 'a+', encoding='utf-8') as file: # slow but safe
                            file.write(url+'\n')
                        yield scrapy.Request(url=url, callback=self.parse_blog)
                    else:
                        break
            else:
                with open('./cti_crawler/urls/'+web_name+'_error.txt', 'a+') as file:
                    file.write(response.url +'\n')

    def parse_blog(self, response):
        print("procesing:"+response.url)
        item=CtiCrawlerItem()

        item['title'] = escape_string(''.join(response.xpath("//h1[@class='single__title']/text()").extract()).strip()) 
        item['publish_date'] = escape_string(''.join(response.xpath("//div[@class='single__labels']/div[@class='single__date-and-time']/text()").extract()[0]))
        item['author'] = escape_string(''.join(response.xpath("//div[@class='single__labels']/div[@class='single__author']/a/text()").extract()))
        item['tags'] = "none"
        item['contents'] = escape_string(' '.join(response.xpath("//div[@id='single__content']/div[@id='single__height-calc']/p[/*]/text()").extract()).strip())
        item['url'] = escape_string(''.join(response.url))

        yield item

    def errback_blog(self, failure):
        request = failure.request
        with open('./cti_crawler/urls/'+web_name+'_error.txt', 'a+') as f:
            file.write(request.url +'\n')
        self.logger.error(repr(failure))