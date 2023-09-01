import scrapy
from cti_crawler.items import CtiCrawlerItem
from pymysql.converters import escape_string

web_name='cybersecurity_att'
web_address='https://cybersecurity.att.com'

class CybersecurityAttSpider(scrapy.Spider):
    name = 'cybersecurity_att'
    # allowed_domains = ['cybersecurity.att.com']
    start_urls = ['https://cybersecurity.att.com/blogs/']

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
        blog_urls=response.xpath("//div[@class='grid-content']/h3/a/@href").extract()
        next_page=response.xpath("//div[@class='pagination']/a[@class='active']/following-sibling::a[1]/@href").extract()
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
            yield scrapy.Request(url=next_page[0], callback=self.parse)

    def parse_blog(self, response):
        print("procesing:"+response.url)
        item=CtiCrawlerItem()

        item['title'] = escape_string(''.join(response.xpath("//div[@class='row rowPad']/h1/text()").extract())) 
        item['publish_date'] = escape_string(''.join(response.xpath("//div[@class='date']/text()").extract()[0][:-2]))
        item['author'] = escape_string(''.join(response.xpath("//div[@class='date']/a/text()").extract()))
        item['tags'] = escape_string(''.join(response.xpath("//div[@class='blog-categories']/p/a/text()").extract()))
        item['contents'] = escape_string(' '.join(response.xpath("//div[@class='blog-content-area']")[0].xpath("string(.)").extract()).strip())
        item['url'] = escape_string(''.join(response.url))

        yield item