import scrapy, os, json, re
from lxml import etree
from cti_crawler.items import CtiCrawlerItem
from pymysql.converters import escape_string

# this website uses ajax

web_name='argu_sec'
web_address='https://argus-sec.com/cyber-security-blog/'

class CybersecurityAttSpider(scrapy.Spider):
    name = 'argu_sec'
    # allowed_domains = ['argus-sec.com']
    base_url = 'https://argus-sec.com/wp-admin/admin-ajax.php?'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'

    def start_requests(self):
        pages = 3
        for page in range(1, pages):
            params = {
                "action": "mk_load_more",
                "query": "eyJwb3N0X3R5cGUiOiJwb3N0IiwiZXhjbHVkZV9wb3N0X2Zvcm1hdCI6IiIsIm9mZnNldCI6ZmFsc2UsInBvc3RzIjoiIiwib3JkZXJieSI6ImRhdGUiLCJvcmRlciI6IkRFU0MiLCJhdXRob3IiOiIiLCJjb3VudCI6ZmFsc2UsImNhdCI6Ijk0In0=",
                "atts": "eyJzaG9ydGNvZGVfbmFtZSI6Im1rX2Jsb2ciLCJzdHlsZSI6Im1vZGVybiIsImxheW91dCI6ImZ1bGwiLCJjb2x1bW4iOjMsImRpc2FibGVfbWV0YSI6InRydWUiLCJncmlkX2ltYWdlX2hlaWdodCI6MzUwLCJjb21tZW50c19zaGFyZSI6InRydWUiLCJmdWxsX2NvbnRlbnQiOiJmYWxzZSIsImltYWdlX3NpemUiOiJjcm9wIiwiZXhjZXJwdF9sZW5ndGgiOjIwMCwidGh1bWJuYWlsX2FsaWduIjoibGVmdCIsImxhenlsb2FkIjoiZmFsc2UiLCJkaXNhYmxlX2xhenlsb2FkIjoiZmFsc2UiLCJpIjowfQ==",
                "loop_iterator": "36",
                "safe_load_more": "bc2699f7a7",
                "_wp_http_referer": "/cyber-security-blog/",
                "paged": str(page),
                "maxPages": "2",
            }
            try:
                yield scrapy.FormRequest(self.base_url, formdata = params, callback=self.parse, dont_filter=True)
            except:
                print("FormRequest Error")
                pass
  
    def parse(self, response):
        if response.text:
            jsonBody = json.loads(response.body.decode('gbk').encode('utf-8'))
            str_content = jsonBody['content']
            html_content = etree.HTML(str_content)
            url_list=html_content.xpath("//div[@class='mk-blog-meta']/h3[@class='the-title']/a/@href")
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

        item['title'] = escape_string(''.join(response.xpath("//h1[@class='page-title mk-drop-shadow']/text()").extract()).strip()) 
        item['publish_date'] = 'none'
        item['author'] = escape_string(''.join(response.xpath("//em[1]/text()").extract()))
        item['tags'] = 'none'
        item['contents'] = escape_string(' '.join(response.xpath("//div[@class='mk-single-content clearfix']/descendant-or-self::text()").extract()).strip())
        item['url'] = escape_string(''.join(response.url))

        yield item

    def errback_blog(self, failure):
        request = failure.request
        with open('./cti_crawler/urls/'+web_name+'_error.txt', 'a+') as f:
            file.write(request.url +'\n')
        self.logger.error(repr(failure))