import scrapy
from cti_crawler.items import CtiCrawlerItem
from pymysql.converters import escape_string

web_name='cloudflare_blog'
web_address='https://blog.cloudflare.com'

class CybersecurityAttSpider(scrapy.Spider):
    name = 'cloudflare_blog'
    # allowed_domains = ['cloudflare.com']
    start_urls = ['https://blog.cloudflare.com/']

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
        blog_urls=response.xpath("//a[@class='fw5 no-underline gray1']/@href").extract()
        next_page=response.xpath("//a[@class='no-underline blue3 underline-hover dn dib-m dib-l']/@href").extract()
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

        item['title'] = escape_string(' '.join(response.xpath("//h1[@class='f6 f7-l fw4 gray1 pt1 pt3-l mb1']/text()").extract()).strip())
        item['publish_date'] = escape_string(response.xpath("//p[@class='f3 fw5 gray5 db di-l mt2']/text()").extract()[1])
        item['author'] = escape_string(' '.join(response.xpath("//div[@class='author-name-tooltip']/a[@class='fw5 f3 no-underline black mr3']/text()").extract()).strip())
        item['tags'] = escape_string(' '.join(response.xpath("//a[@class='dib pl2 pr2 pt1 pb1 mb2 bg-gray8 no-underline blue3 f2']/text()").extract()).strip())
        item['contents'] = escape_string(' '.join(response.xpath("//div[@class='post-content lh-copy gray1']/p[*]/text()").extract()).strip())
        item['url'] = escape_string(''.join(response.url))

        yield item