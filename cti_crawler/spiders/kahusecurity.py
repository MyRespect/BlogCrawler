import scrapy
from cti_crawler.items import CtiCrawlerItem
from pymysql.converters import escape_string

web_name='kahusecurity'
web_address='http://www.kahusecurity.com/'

class CybersecurityAttSpider(scrapy.Spider):
    name = 'kahusecurity'
    # allowed_domains = ['kahusecurity.com']
    start_urls = ['http://www.kahusecurity.com/older.html', 'http://www.kahusecurity.com/index.html']

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
        blog_urls=response.xpath("//a[@class='text-decoration-none custom-link-style-1']/@href").extract()
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

    def parse_blog(self, response):
        print("procesing:"+response.url)
        item=CtiCrawlerItem()

        item['title'] = escape_string(' '.join(response.xpath("//div[@class='post-event-content']/h2/text()").extract()).strip())
        item['publish_date'] = escape_string(' '.join(response.xpath("//div[@class='post-event-content']/h5/text()").extract()).strip())
        item['author'] = 'none'
        item['tags'] = 'none'
        item['contents'] = escape_string(' '.join(response.xpath("//div[@class='post-event-content']/p[/*]/text()").extract()).strip())
        item['url'] = escape_string(''.join(response.url))

        yield item