import scrapy
from cti_crawler.items import CtiCrawlerItem
from pymysql.converters import escape_string

web_name='c2a_sec'
web_address='https://www.c2a-sec.com/blog/'

class CybersecurityAttSpider(scrapy.Spider):
    name = 'c2a_sec'
    # allowed_domains = ['c2a-sec.com']
    start_urls = ['https://www.c2a-sec.com/blog/']

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
        blog_urls=response.xpath("//a[@class='button button_size_2 button_dark button_js']/@href").extract()
        # next_page=response.xpath("//a[@class='no-underline blue3 underline-hover dn dib-m dib-l']/@href").extract()
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

        # if len(next_page)!=0:
        #     yield scrapy.Request(url=web_address+next_page[0], callback=self.parse)

    def parse_blog(self, response):
        print("procesing:"+response.url)
        item=CtiCrawlerItem()

        item['title'] = escape_string(' '.join(response.xpath("//strong[@class='be']/text()").extract()).strip())
        item['publish_date'] = escape_string(' '.join(response.xpath("//div/a[@class='ex ey ba bb bc bd be bf bg bh ez bk fa fb']/text()").extract()).strip())
        item['author'] = 'none'
        item['tags'] = escape_string(' '.join(response.xpath("//li[@class='fs bv gh le'][/*]/a[@class='em b fd lf fu lg lh ft s li']/text()").extract()).strip())
        item['contents'] = escape_string(' '.join(response.xpath("//div[@class='ab ac ae af ag dc ai aj']/descendant-or-self::text()").extract()).strip())
        item['url'] = escape_string(''.join(response.url))

        yield item