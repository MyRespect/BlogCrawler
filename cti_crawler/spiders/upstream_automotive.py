import scrapy, os
from pymysql.converters import escape_string
from selenium import webdriver

from cti_crawler.items import CtiCrawlerItem

web_name='upstream_automotive'
web_address='https://upstream.auto/research/automotive-cybersecurity/'
class SmarthomeSpider(scrapy.Spider):
    name = 'upstream_automotive'
    # allowed_domains = ['upstream.auto']
    start_urls = ['https://upstream.auto/research/automotive-cybersecurity/?id={}'.format(str(i))for i in range(1780, 8310, 10)]
    # start_urls = ['https://upstream.auto/research/automotive-cybersecurity/?id=5190']

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
        item=CtiCrawlerItem()

        item['title'] = escape_string(''.join(response.xpath("//div[@class='modal-title']/text()").extract()).strip()) 
        item['publish_date'] = escape_string(''.join(response.xpath("//div[@class='item-details']/p[1]/span[@class='property-details']/text()").extract()).strip())
        item['author'] = 'none'
        item['tags'] = 'none'
        item['contents'] = escape_string(' '.join(response.xpath("//div[@class='item-details']/p[3]/span[@class='property-details']/text()").extract()).strip())
        item['url'] = escape_string(''.join(response.url))

        yield item