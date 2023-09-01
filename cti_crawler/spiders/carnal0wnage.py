import scrapy
from cti_crawler.items import CtiCrawlerItem
from pymysql.converters import escape_string

web_name='carnal0wnage'
web_address='http://carnal0wnage.attackresearch.com'

class CybersecurityAttSpider(scrapy.Spider):
    name = 'carnal0wnage'
    # allowed_domains = ['carnal0wnage.attackresearch.com']
    start_urls = ['http://carnal0wnage.attackresearch.com/']

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
        # extract blog archive urls using xpath
        archive_urls=response.xpath("//a[@class='post-count-link']/@href").extract()
        for a_url in archive_urls:
            if a_url.count('/')==5:
                yield scrapy.Request(url=a_url, callback=self.parse_archive )

    def parse_archive(self, response):
        print("procesing:"+response.url)
        # extract blog urls using xpath
        blog_urls=response.xpath("//h3[@class='post-title entry-title']/a/@href").extract()
        # get previous crawled urls
        urlset=self.read_exist_urls('./cti_crawler/urls/'+web_name+'.txt')
        if len(blog_urls)!=0:
            for b_url in blog_urls:
                if b_url+'\n' not in urlset:
                    with open('./cti_crawler/urls/'+web_name+'.txt', 'a+', encoding='utf-8') as file: # slow but safe
                        file.write(b_url+'\n')
                    yield scrapy.Request(url=b_url, callback=self.parse_blog, errback=self.errback_blog)
                else:
                    break
        else:
            with open('./cti_crawler/urls/'+web_name+'_error.txt', 'a+') as file:
                file.write(response.url +'\n')

    def parse_blog(self, response):
        print("procesing:"+response.url)
        item=CtiCrawlerItem()

        item['title'] = escape_string(''.join(response.xpath("//h3[@class='post-title entry-title']/text()").extract())) 
        item['publish_date'] = escape_string(''.join(response.xpath("//a[@class='timestamp-link']/abbr[@class='published']/text()").extract()[0]))
        item['author'] = escape_string(''.join(response.xpath("//span[@class='post-author vcard']/span[@class='fn']/span/text()").extract()[0]))
        item['tags'] = escape_string(''.join(response.xpath("//span[@class='post-labels']/a/text()").extract()))
        item['contents'] = escape_string(' '.join(response.xpath("//div[@class='post-body entry-content']").xpath("string(.)").extract()).strip())
        item['url'] = escape_string(''.join(response.url))

        yield item

    def errback_blog(self, failure):
        request = failure.request
        with open('./cti_crawler/urls/'+web_name+'_error.txt', 'a+') as f:
            file.write(request.url +'\n')
        self.logger.error(repr(failure))