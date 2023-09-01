import scrapy
from cti_crawler.items import CtiCrawlerItem
from pymysql.converters import escape_string

web_name='hexacorn_blog'
web_address='https://www.hexacorn.com/blog'

class CybersecurityAttSpider(scrapy.Spider):
    name = 'hexacorn_blog'
    # allowed_domains = ['hexacorn.com']
    start_urls = ['https://www.hexacorn.com/blog/']

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
        blog_urls=response.xpath("//h2[@class='posttitle']/a/@href").extract()
        next_page=response.xpath("//div[@class='navigation']/div[@class='alignleft']/a/@href").extract()
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

        # if len(next_page)!=0 and int(next_page[0].split('/')[-2])<5:
        if len(next_page)!=0:
            yield scrapy.Request(url=next_page[0], callback=self.parse)

    def parse_blog(self, response):
        print("procesing:"+response.url)
        item=CtiCrawlerItem()

        item['title'] = escape_string(' '.join(response.xpath("//h2[@class='posttitle']/a/text()").extract()).strip())
        item['publish_date'] = escape_string(response.xpath("//div[@class='post-content']/p[@class='date']/text()").extract()[0])
        item['author'] = "none"
        item['tags'] = "none"
        item['contents'] = escape_string(' '.join(response.xpath("//div[@class='post-content']/div[@class='entry']/descendant-or-self::text()").extract()).strip())
        item['url'] = escape_string(''.join(response.url))

        yield item