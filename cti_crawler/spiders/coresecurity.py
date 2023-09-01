import scrapy
from cti_crawler.items import CtiCrawlerItem
from pymysql.converters import escape_string

web_name='coresecurity_blog'
web_address='https://www.coresecurity.com'

class CybersecurityAttSpider(scrapy.Spider):
    name = 'coresecurity_blog'
    # allowed_domains = ['coresecurity.com']
    start_urls = ['https://www.coresecurity.com/blog/']

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
        next_page=response.xpath("//li[@class='pager__item--next']/a/@href").extract()
        # get previous crawled urls
        urlset=self.read_exist_urls('./cti_crawler/urls/'+web_name+'.txt')
        if len(blog_urls)!=0:
            for url in blog_urls:
                if url+'\n' not in urlset:
                    with open('./cti_crawler/urls/'+web_name+'.txt', 'a+', encoding='utf-8') as file: # slow but safe
                        file.write(url+'\n')
                    yield scrapy.Request(url=web_address+url, callback=self.parse_blog)
                else:
                    break
        else:
            with open('./cti_crawler/urls/'+web_name+'_error.txt', 'a+') as file:
                file.write(response.url +'\n')

        if len(next_page)!=0:
            yield scrapy.Request(url=web_address+'/blog'+next_page[0], callback=self.parse)

    def parse_blog(self, response):
        print("procesing:"+response.url)
        item=CtiCrawlerItem()

        item['title'] = escape_string(response.url.split("blog/")[1]) # different blog has different format
        item['publish_date'] = 'none' # not provided
        item['author'] = 'none'
        item['tags'] = 'none'
        item['contents'] = escape_string(' '.join(response.xpath("//div[@class='clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item']/p[*]/text()").extract()).strip())
        item['url'] = escape_string(''.join(response.url))

        yield item