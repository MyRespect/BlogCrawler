import scrapy
from cti_crawler.items import CtiCrawlerItem
from pymysql.converters import escape_string

web_name='insights_sei'
web_address='https://insights.sei.cmu.edu/'

class CybersecurityAttSpider(scrapy.Spider):
    name = 'insights_sei'
    # allowed_domains = ['insights.sei.cmu.edu']
    start_urls = ['https://insights.sei.cmu.edu/']

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

        # extract data using xpath
        blog_urls=response.xpath("//div[@class='view-content row']/div[@class='row p-4 align-items-center w-100 views-row'][*]/div[@class='col-sm-10']/h3/a/@href").extract()
        # above alreay crawl all blog urls
        # next_page=response.xpath("//li[@class='list-entry'][3]/a[@class='next']/@href").extract()
        # get previous crawled urls
        urlset=self.read_exist_urls('./cti_crawler/urls/'+web_name+'.txt')
        if len(blog_urls)!=0:
            for url in blog_urls:
                if url+'\n' not in urlset:
                    with open('./cti_crawler/urls/'+web_name+'.txt', 'a+', encoding='utf-8') as file: # slow but safe
                        file.write(url+'\n')
                    yield scrapy.Request(url=url, callback=self.parse_blog, errback=self.errback_blog)
                else:
                    break
        else:
            with open('./cti_crawler/urls/'+web_name+'_error.txt', 'a+') as file:
                file.write(response.url +'\n')

        # if len(next_page)!=0:
        #     yield scrapy.Request(url=next_page[0], callback=self.parse)

    def parse_blog(self, response):
        print("procesing:"+response.url)
        item=CtiCrawlerItem()

        item['title'] = escape_string(''.join(response.xpath("//h2[@class='asset-name entry-title mt-0 mb-4']/text()").extract()).strip()) 
        item['publish_date'] = escape_string(''.join(response.xpath("//div[@class='media-body']/h6[@id='alert']/time/text()").extract()))
        item['author'] = escape_string(''.join(response.xpath("//h5[@class='m-media-object__listing__author m-media-object__listing__author--blog']/a/text()").extract()))
        tag1=response.xpath("//div[@class='media-body']/span[@class='badge badge--blog badge--blog-inline'][1]/a/text()").extract()
        tag1=tag1+response.xpath("//div[@class='media-body']/span[@class='badge badge--blog badge--blog-inline'][2]/a/text()").extract()
        item['tags'] = escape_string(' '.join(tag1).strip())
        item['contents'] = escape_string(' '.join(response.xpath("//div[@class='blog-post-body'][*]/*/text()").extract()).strip())
        item['url'] = escape_string(''.join(response.url))

        yield item

    def errback_blog(self, failure):
        request = failure.request
        with open('./cti_crawler/urls/'+web_name+'_error.txt', 'a+') as f:
            file.write(request.url +'\n')
        self.logger.error(repr(failure))