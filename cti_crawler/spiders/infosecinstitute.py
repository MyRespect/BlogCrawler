import scrapy
from cti_crawler.items import CtiCrawlerItem
from pymysql.converters import escape_string

web_name='infosecinstitute'
web_address='https://resources.infosecinstitute.com/article-archive/'

class CybersecurityAttSpider(scrapy.Spider):
    name = 'infosecinstitute'
    # allowed_domains = ['infosecinstitute.com']
    start_urls = ['https://resources.infosecinstitute.com/article-archive/']

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
        blog_urls=response.xpath("//a[@class='inner full flex']/@href").extract()
        next_page=response.xpath("//a[@class='next page-numbers']/@href").extract()
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

        item['title'] = escape_string(' '.join(response.xpath("//h1[@class='mb-3 h2 larger']/text()").extract()).strip())
        item['publish_date'] = "none"
        item['author'] = escape_string(' '.join(response.xpath("//span[@class='author-name color-black-dark font-weight-bold']/text()").extract()).strip())
        item['tags'] = "none"
        item['contents'] = escape_string(' '.join(response.xpath("//div[@class='wysiwyg']/descendant-or-self::text()").extract()).strip())
        item['url'] = escape_string(''.join(response.url))

        yield item