import scrapy, os
from cti_crawler.items import CtiCrawlerItem
from pymysql.converters import escape_string

from selenium import webdriver

web_name='rsa_digital'
web_address='https://www.rsa.com'

class CybersecurityAttSpider(scrapy.Spider):
    name = 'rsa_digital'
    # allowed_domains = ['bdtechtalks.com']
    start_urls = ['https://www.rsa.com/en-us/blog/securing-the-digital-world']

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chromedriver = "/usr/bin/chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=chromedriver)
        super().__init__()

    def close(self, spider):
        print("Crawler job finished.")
        self.browser.quit()

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
        blog_urls=response.xpath("//div[@class='c58 c58v1']/ul/li[@class='c58-item'][*]/div[@class='c52 c52v2 c00 no-border media-object hidden']/div[@class='c52-image media-object-media']/a/@href").extract()
        # above alreay crawl all blog urls
        # next_page=response.xpath("//li[@class='list-entry'][3]/a[@class='next']/@href").extract()
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
        #     yield scrapy.Request(url=next_page[0], callback=self.parse)

    def parse_blog(self, response):
        print("procesing:"+response.url)
        item=CtiCrawlerItem()

        item['title'] = escape_string(''.join(response.xpath("//div[@class='cmp-page-title text']/h1[@class='text--size-h2']/text()").extract()).strip()) 
        item['publish_date'] = escape_string(response.xpath("//div[@class='cmp-page-title text']/div[@class='text--size-h6 text--compressed']/text()").extract()[0].split('|')[0].strip())
        item['author'] = escape_string(response.xpath("//div[@class='cmp-page-title text']/div[@class='text--size-h6 text--compressed']/text()").extract()[0].split('|')[1].strip())
        item['tags'] = 'none'
        item['contents'] = escape_string(' '.join(response.xpath("//div[@class='c00 c00v0 element--standard']/p[/*]/text()").extract()).strip())
        item['url'] = escape_string(''.join(response.url))

        yield item

    def errback_blog(self, failure):
        request = failure.request
        with open('./cti_crawler/urls/'+web_name+'_error.txt', 'a+') as f:
            file.write(request.url +'\n')
        self.logger.error(repr(failure))