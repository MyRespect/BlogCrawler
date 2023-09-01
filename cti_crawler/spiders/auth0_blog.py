import scrapy
from cti_crawler.items import CtiCrawlerItem
from pymysql.converters import escape_string

web_name='auth0_blog'
web_address='https://auth0.com'

class CybersecurityAttSpider(scrapy.Spider):
    name = 'auth0_blog'
    # allowed_domains = ['auth0.com']
    start_urls = ['https://auth0.com/blog/identity-and-security/', 'https://auth0.com/blog/identity-and-security/page2/']

    def read_exist_urls(self, file_path):
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
        blog_urls=response.xpath("///a[@class='sc-1t3ptg8-4 hZxZfg']/@href").extract()
        next_page=response.xpath("//li[@class='sc-14ab4uv-2 iiwhmX'][6]/a[@class='sc-14ab4uv-3 gwkBeb']/@href").extract()
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
            yield scrapy.Request(url=web_address+next_page[0], callback=self.parse)

    def parse_blog(self, response):
        print("procesing:"+response.url)
        item=CtiCrawlerItem()

        item['title'] = escape_string(' '.join(response.xpath("//h1[@class='bie152-6 gmdlsg']/text()").extract()).strip())
        item['publish_date'] = escape_string(' '.join(response.xpath("//p[@class='bie152-15 jxcMKT']/text()").extract()[0]).strip())
        item['author'] = escape_string(' '.join(response.xpath("//h4[@class='bie152-13 coofmK']/text()").extract()[0]).strip())
        item['tags'] = 'none'
        item['contents'] = escape_string(' '.join(response.xpath("//main[@id='post-content']/descendant-or-self::text()").extract()).strip())
        item['url'] = escape_string(''.join(response.url))

        yield item