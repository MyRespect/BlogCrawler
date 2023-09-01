import scrapy, os
from selenium import webdriver
from cti_crawler.items import CtiCrawlerItem
from pymysql.converters import escape_string


web_name='symantec-enterprise-blogs'
web_address='https://symantec-enterprise-blogs.security.com'

class CybersecurityAttSpider(scrapy.Spider):
    name = 'symantec-enterprise-blogs'
    # allowed_domains = ['symantec-enterprise-blogs.security.com']
    start_urls = ['https://symantec-enterprise-blogs.security.com/blogs/threat-intelligence/']


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
        blog_urls=response.xpath("//div[@class='blog-teaser__content-inner']/a[@class='blog-teaser__link']/@href").extract()
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

        item['title'] = escape_string(''.join(response.xpath("//h1[@id='page-title']/text()").extract()).strip()) 
        item['publish_date'] = escape_string(''.join(response.xpath("//div[@class='meta']/span[@class='meta__date']/time/text()").extract()[0]))
        item['author'] = escape_string(''.join(response.xpath("//div[@class='author__content']/span[@class='author__name']/text()").extract()))
        item['tags'] = 'none'
        item['contents'] = escape_string(' '.join(response.xpath("//div[@class='blog-post__content']/span[*]/app-paragraph-rte/div/p[*]/text()").extract()).strip())
        item['url'] = escape_string(''.join(response.url))

        yield item

    def errback_blog(self, failure):
        request = failure.request
        with open('./cti_crawler/urls/'+web_name+'_error.txt', 'a+') as f:
            file.write(request.url +'\n')
        self.logger.error(repr(failure))