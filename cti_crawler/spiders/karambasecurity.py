import scrapy
from cti_crawler.items import CtiCrawlerItem
from pymysql.converters import escape_string

web_name='karambasecurity'
web_address='https://www.karambasecurity.com'

class CybersecurityAttSpider(scrapy.Spider):
    name = 'karambasecurity'
    # allowed_domains = ['karambasecurity.com']
    start_urls = ['https://www.karambasecurity.com/blog']

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
        # extract blog urls using xpath
        blog_urls=response.xpath("//a[@class='btn color-dark btn-bg-transparent btn-sm blog-btn font-middle my-2']/@href").extract()
        # get previous crawled urls
        urlset=self.read_exist_urls('./cti_crawler/urls/'+web_name+'.txt')
        if len(blog_urls)!=0:
            for b_url in blog_urls:
                if b_url+'\n' not in urlset:
                    with open('./cti_crawler/urls/'+web_name+'.txt', 'a+', encoding='utf-8') as file: # slow but safe
                        file.write(b_url+'\n')
                    yield scrapy.Request(url=web_address+b_url, callback=self.parse_blog, errback=self.errback_blog)
                else:
                    break
        else:
            with open('./cti_crawler/urls/'+web_name+'_error.txt', 'a+') as file:
                file.write(response.url +'\n')

    def parse_blog(self, response):
        print("procesing:"+response.url)
        item=CtiCrawlerItem()

        item['title'] = escape_string(''.join(response.xpath("//h3[@class='jsx-3304928901 dashed mb-0']/text()").extract()))
        author_date=response.xpath("//h6[@class='jsx-3304928901 font-sm my-4 py-2']/text()").extract()[0]
        author_date_list=author_date.split('|')
        item['publish_date'] = escape_string(author_date_list[1])
        item['author'] = escape_string(author_date_list[0])
        item['tags'] = 'none'
        item['contents'] = escape_string(' '.join(response.xpath("//div[@class='blog-article-content pb-4 row']/div[@class='col']/p[/*]/descendant-or-self::text()").extract()).strip())
        item['url'] = escape_string(''.join(response.url))

        yield item

    def errback_blog(self, failure):
        request = failure.request
        with open('./cti_crawler/urls/'+web_name+'_error.txt', 'a+') as f:
            file.write(request.url +'\n')
        self.logger.error(repr(failure))