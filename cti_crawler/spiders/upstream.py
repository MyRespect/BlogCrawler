import scrapy, os, json, re
from lxml import etree
from cti_crawler.items import CtiCrawlerItem
from pymysql.converters import escape_string

from selenium import webdriver

web_name='upstream_auto'
web_address='https://upstream.auto'

class CybersecurityAttSpider(scrapy.Spider):
    name = 'upstream_auto'
    # allowed_domains = ['upstream.auto']
    base_url = 'https://upstream.auto/wp-admin/admin-ajax.php?'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'

    def start_requests(self):
        pages = 6
        for page in range(1, pages):
            params = {
                "action": "postLoadMore",
                "page": str(page),
                "category": "blog",
                "numberposts": "9",
            }
            try:
                yield scrapy.FormRequest(self.base_url, formdata = params, callback=self.parse, dont_filter=True)
            except:
                print("FormRequest Error")
                pass
  
    def parse(self, response):
        if response.text:
            html_content = etree.HTML(response.text)
            url_list=html_content.xpath("//div[@class='grid-item']/a/@href")
            urlset=self.read_exist_urls('./cti_crawler/urls/'+web_name+'.txt')
            for url in url_list:
                if url+'\n' not in urlset:
                    with open('./cti_crawler/urls/'+web_name+'.txt', 'a+', encoding='utf-8') as file: # slow but safe
                        file.write(url+'\n')
                    yield scrapy.Request(url=url, callback=self.parse_blog)
                else:
                    break                

    def read_exist_urls(self, file_path): # read the latest 120 urls
        urlset=[]
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                urlset = f.readlines()
        except FileNotFoundError:
            print("Sorry, the file"+file_path+" does not exist.")
        return urlset

    def parse_blog(self, response):
        print("procesing:"+response.url)
        item=CtiCrawlerItem()

        item['title'] = escape_string(''.join(response.xpath("//div[@class='row']/div[@class='col-md-8']/div[@class='white']/h1/text()").extract()).strip()) 
        item['publish_date'] = 'none'
        item['author'] = 'none'
        item['tags'] = 'none'
        item['contents'] = escape_string(' '.join(response.xpath("///div[@class='content']/p[/*]/text()").extract()).strip())
        item['url'] = escape_string(''.join(response.url))

        yield item

    def errback_blog(self, failure):
        request = failure.request
        with open('./cti_crawler/urls/'+web_name+'_error.txt', 'a+') as f:
            file.write(request.url +'\n')
        self.logger.error(repr(failure))