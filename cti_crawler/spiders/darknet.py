import scrapy
from cti_crawler.items import CtiCrawlerItem
from pymysql.converters import escape_string

web_name='darknet_blog'
web_address='https://www.darknet.org.uk'

class CybersecurityAttSpider(scrapy.Spider):
    name = 'darknet_blog'
    # allowed_domains = ['darknet.org.uk']
    start_urls = ['https://www.darknet.org.uk']

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
        blog_urls=response.xpath("//h1[@class='title entry-title']/a/@href").extract()
        if len(blog_urls)==0:
            blog_urls=response.xpath("//h2[@class='title entry-title']/a/@href").extract()
        next_page=response.xpath("//div[@class='pagination woo-pagination']/a[@class='next page-numbers']/@href").extract()
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

        item['title'] = escape_string(' '.join(response.xpath("//header/h1[@class='title entry-title']/text()").extract()).strip())
        item['publish_date'] = escape_string(response.xpath("//div[@class='post-meta']/text()").extract()[0][14:])
        item['author'] = 'none'
        item['tags'] = escape_string(' '.join(response.xpath("//p[@class='tags']/a/text()").extract()).strip())
        item['contents'] = escape_string(' '.join(response.xpath("//section[@class='entry']/p[/*]/text()").extract()).strip())
        item['url'] = escape_string(''.join(response.url))

        yield item