# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import time
from scrapy import signals
from scrapy.http import HtmlResponse 
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

class CtiCrawlerSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CtiCrawlerDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest

        if request.url in ['https://symantec-enterprise-blogs.security.com/blogs/threat-intelligence/']:
            spider.browser.get(url=request.url)
            # more_btn=spider.browser.find_element_by_xpath("//div[@class='page-container']/main[@class='main']/a[@class='btn btn--more']") # avoid space
            while True:
                try:
                    more_btn = spider.browser.find_element_by_link_text("View More")
                    spider.browser.execute_script("arguments[0].click();", more_btn)
                    time.sleep(3)
                except:
                    print("There is no remaining blogs")
                    break
            row_response = spider.browser.page_source
            return HtmlResponse(url=spider.browser.current_url, body=row_response, encoding="utf8", request=request)
        elif request.url.split('?')[0] in ['https://upstream.auto/research/automotive-cybersecurity/']:
            spider.browser.get(url=request.url)
            time.sleep(40)
            row_response = spider.browser.page_source
            return HtmlResponse(url=spider.browser.current_url, body=row_response, encoding="utf8", request=request)
        elif request.url in ['https://securelist.com/all/']:
            spider.browser.get(url=request.url)
            while True:
                try:
                    more_btn = spider.browser.find_element_by_link_text("Load more")
                    spider.browser.execute_script("arguments[0].click();", more_btn)
                    # more_btn.click()
                    time.sleep(5)
                except:
                    print("There is no remaining blogs")
                    break
            row_response = spider.browser.page_source
            return HtmlResponse(url=spider.browser.current_url, body=row_response, encoding="utf8", request=request)
        elif request.url in ['https://bdtechtalks.com/category/blog/']:
            spider.browser.get(url=request.url)
            spider.browser.execute_script("window.scrollBy(0, 9000000)")
            time.sleep(10)
            while True:
                try:
                    # more_btn = spider.browser.find_element_by_link_text("Load more")
                    # spider.browser.execute_script("arguments[0].click();", more_btn)
                    more_btn=spider.browser.find_element_by_xpath("//div[@class='td-load-more-wrap td-load-more-infinite-wrap']")
                    more_btn.click()
                    time.sleep(5)
                except:
                    print("There is no remaining blogs")
                    break
            row_response = spider.browser.page_source
            return HtmlResponse(url=spider.browser.current_url, body=row_response, encoding="utf8", request=request)
        elif request.url in ['https://www.rsa.com/en-us/blog/securing-the-digital-world']:
            spider.browser.get(url=request.url)
            spider.browser.execute_script("window.scrollBy(0, 9000000)")
            time.sleep(10)
            # mannual tested that it does not need to click more to load all urls
            # while True:
            #     try:
            #         more_btn=spider.browser.find_element_by_xpath("//div[@id='showMore']/a[@class='cmp-button__text element--background-BE3A34']")
            #         more_btn.click()
            #         time.sleep(5)
            #     except:
            #         print("There is no remaining blogs")
            #         break
            row_response = spider.browser.page_source
            return HtmlResponse(url=spider.browser.current_url, body=row_response, encoding="utf8", request=request)
        elif request.url in ['https://www.trustwave.com/en-us/resources/blogs/spiderlabs-blog/']:
            spider.browser.get(url=request.url)
            spider.browser.execute_script("window.scrollBy(0, 9000000)")
            time.sleep(10)
            while True:
                try:
                    more_btn=spider.browser.find_element_by_xpath("//p[@class='mbl']/button[@id='loadmore']").send_keys('\n')
                    # spider.browser.execute_script("arguments[0].click();", more_btn)
                    time.sleep(5)
                except:
                    print("There is no remaining blogs")
                    break
            row_response = spider.browser.page_source
            return HtmlResponse(url=spider.browser.current_url, body=row_response, encoding="utf8", request=request)
        elif request.url in ['https://www.fireeye.com/blog/threat-research.html']:
            spider.browser.get(url=request.url)
            while True:
                try:
                    # more_btn = spider.browser.find_element_by_link_text("See more")
                    more_btn=spider.browser.find_element_by_xpath("//div[@class='c11v9 loadmore']")
                    more_btn.click()
                    time.sleep(5)
                except:
                    # raise StopIteration
                    print("There is no remaining blogs")
                    break
            row_response = spider.browser.page_source
            return HtmlResponse(url=spider.browser.current_url, body=row_response, encoding="utf8", request=request)
        elif request.url.split('/search')[0] in ['https://ddanchev.blogspot.com']:
            spider.browser.get(url=request.url)
            row_response = spider.browser.page_source
            try:
                more_btn = spider.browser.find_element_by_link_text("Older Posts")
                more_btn.click()
                time.sleep(3)
            except:
                raise StopIteration
            return HtmlResponse(url=spider.browser.current_url, body=row_response, encoding="utf8", request=request)
        elif request.url.split('?')[0] in ['https://www.forcepoint.com/blog']:
            spider.browser.get(url=request.url)
            row_response = spider.browser.page_source
            try:
                spider.browser.execute_script("window.scrollBy(0, 90000)")
                time.sleep(3)
            except:
                raise StopIteration
            return HtmlResponse(url=spider.browser.current_url, body=row_response, encoding="utf8", request=request)    
        else:
            return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
