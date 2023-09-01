import scrapy, os, json, re
from lxml import etree
from cti_crawler.items import CtiCrawlerItem
from pymysql.converters import escape_string

# this website uses ajax

web_name='juniper'
web_address='https://community.juniper.net/browse/blogs'

class CybersecurityAttSpider(scrapy.Spider):
    name = 'juniper'
    # allowed_domains = ['juniper.net']
    base_url = 'https://community.juniper.net/browse/blogs?'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'

    def start_requests(self):
        pages = 3
        for page in range(1, pages):
            params = {
                "ctl00$ScriptManager1": "ctl00$MainCopy$ctl06$BlogContents|ctl00$MainCopy$ctl06$HLDataPager$ctl02$ctl00", 
                "__HL-RequestVerificationToken": "zWfoeq2dBHtwjZvRaIBc6Uv9DYvh-NosutNLcMDkcVj2FbsGUB6pGNHAeN-P9X8dmSkuAldk64RMOCH4B3qwKS1NTkk1",
                "ctl00$SearchControl$ProductList$0": "Announcement",
                "ctl00$SearchControl$ProductList$1": "Blog",
                "ctl00$SearchControl$ProductList$2": "Community",
                "ctl00$SearchControl$ProductList$3": "Egroup",
                "ctl00$SearchControl$ProductList$4": "CalendarEvent",
                "ctl00$SearchControl$ProductList$5": "Glossary",
                "ctl00$SearchControl$ProductList$6": "Navigation",
                "ctl00$SearchControl$ProductList$7": "Library",
                "ctl00$SearchControl$DateRangeDDL": "on this day",
                "ctl00$MainCopy$ctl03$tabs": "LiTab1",
                "__EVENTTARGET": "ctl00$MainCopy$ctl06$HLDataPager$ctl02$ctl00",
                "__ASYNCPOST": "true",
            }
            try:
                yield scrapy.FormRequest(self.base_url, formdata = params, callback=self.parse, dont_filter=True)
            except:
                print("FormRequest Error")
                pass
  
    def parse(self, response):
        if response.text:
            str_content = response.text
            html_content = etree.HTML(str_content)
            url_list=html_content.xpath("//h3/a[/*]/@href")
            urlset=self.read_exist_urls('./cti_crawler/urls/'+web_name+'.txt')
            for url in url_list:
                if url+'\n' not in urlset:
                    with open('./cti_crawler/urls/'+web_name+'.txt', 'a+', encoding='utf-8') as file: # slow but safe
                        file.write(url+'\n')
                    yield scrapy.Request(url=url, callback=self.parse_blog)
                else:
                    break              

    def read_exist_urls(self, file_path): # read the latest 120 urls
        urlset=[]
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                urlset = f.readlines()
        except FileNotFoundError:
            print("Sorry, the file"+file_path+" does not exist.")
        return urlset

    def parse_blog(self, response):
        print("procesing:"+response.url)
        item=CtiCrawlerItem()

        item['title'] = escape_string(''.join(response.xpath("//h3[@id='MainCopy_ctl08_ucPermission_TitlePanel']/text()").extract()).strip()) 
        item['publish_date'] = escape_string(''.join(response.xpath("//div[@id='MainCopy_ctl08_ucPermission_ByLinePanel']/text()").extract()).strip()) 
        item['author'] = escape_string(''.join(response.xpath("//div[@id='MainCopy_ctl08_ucPermission_ByLinePanel']/a[@id='MainCopy_ctl08_ucPermission_UserName_lnkProfile']/text()").extract()))
        item['tags'] = 'none'
        item['contents'] = escape_string(' '.join(response.xpath("///div[@class='lia-message-template-content-zone']/p[/*]/text()").extract()).strip())
        item['url'] = escape_string(''.join(response.url))

        yield item

    def errback_blog(self, failure):
        request = failure.request
        with open('./cti_crawler/urls/'+web_name+'_error.txt', 'a+') as f:
            file.write(request.url +'\n')
        self.logger.error(repr(failure))