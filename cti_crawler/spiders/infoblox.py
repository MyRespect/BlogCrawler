import scrapy
from cti_crawler.items import CtiCrawlerItem
from pymysql.converters import escape_string

web_name='infoblox'
web_address='https://blogs.infoblox.com/'

class CybersecurityAttSpider(scrapy.Spider):
    name = 'infoblox'
    # allowed_domains = ['infoblox.com']
    start_urls = ['https://blogs.infoblox.com/']

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
        blog_urls=response.xpath("//h2[@class='entry-title']/a[@class='entry-title-link']/@href").extract()
        next_page=response.xpath("//li[@class='pagination-next']/a/@href").extract()
        # get previous crawled urls
        urlset=self.read_exist_urls('./cti_crawler/urls/'+web_name+'.txt')
        if len(blog_urls)!=0:
            for url in blog_urls:
                if url+'\n' not in urlset:
                    with open('./cti_crawler/urls/'+web_name+'.txt', 'a+', encoding='utf-8') as file: # slow but safe
                        file.write(url+'\n')
                    yield scrapy.Request(url=url, callback=self.parse_blog)
                else:
                    break
        else:
            with open('./cti_crawler/urls/'+web_name+'_error.txt', 'a+') as file:
                file.write(response.url +'\n')

        if len(next_page)!=0:
            yield scrapy.Request(url=next_page[0], callback=self.parse)

    def parse_blog(self, response):
        print("procesing:"+response.url)
        item=CtiCrawlerItem()

        item['title'] = escape_string(' '.join(response.xpath("//h1[@id='blogpost-title']/text()").extract()).strip())
        item['publish_date'] = escape_string(' '.join(response.xpath("//header[@class='entry-header']/p[@class='entry-meta']/time[@class='entry-time']/text()").extract()).strip())
        item['author'] = "none" 
        item['tags'] = escape_string(' '.join(response.xpath("//div[@class='post-tags']/ul/li[/*]/a/text()").extract()).strip())
        item['contents'] = escape_string(' '.join(response.xpath("//div[@class='entry-content']/descendant-or-self::text()").extract()).strip())
        item['url'] = escape_string(''.join(response.url))

        yield item