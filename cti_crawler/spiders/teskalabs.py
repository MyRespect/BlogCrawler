import scrapy
from cti_crawler.items import CtiCrawlerItem
from pymysql.converters import escape_string

web_name='teskalabs'
web_address='https://teskalabs.com'

class CybersecurityAttSpider(scrapy.Spider):
    name = 'teskalabs'
    # allowed_domains = ['teskalabs.com']
    start_urls = ['https://teskalabs.com/blog/']

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
        blog_urls=response.xpath("//h3[@class='list-group-item-heading']/a[@class='t-black']/@href").extract()
        # next_page=response.xpath("//a[@class='no-underline blue3 underline-hover dn dib-m dib-l']/@href").extract()
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

        # if len(next_page)!=0:
        #     yield scrapy.Request(url=web_address+next_page[0], callback=self.parse)

    def parse_blog(self, response):
        print("procesing:"+response.url)
        item=CtiCrawlerItem()

        item['title'] = escape_string(response.xpath("//div[@class='col-sm-8']/h1/text()").extract()[0])
        item['publish_date'] = 'none'
        item['author'] =  escape_string(' '.join(response.xpath("//h4[@class='author-card-name']/a/text()").extract()).strip())
        item['tags'] = escape_string(' '.join(response.xpath("//div[@class='blog-entry-tags']/a[/*]/text()").extract()).strip())
        item['contents'] = escape_string(' '.join(response.xpath("//div[@class='col-sm-8']/descendant-or-self::text()").extract()).strip())
        item['url'] = escape_string(''.join(response.url))

        yield item