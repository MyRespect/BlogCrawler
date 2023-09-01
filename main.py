from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from cti_crawler.database import CTI_DB

if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    
    process.crawl("argu_sec")
    process.crawl("carnal0wnage")
    process.crawl("cloudflare_blog")
    process.crawl("coresecurity_blog")
    process.crawl("crowdstrike_blog")
    process.crawl("cybersecurity_att")
    process.crawl("darknet_blog")
    process.crawl("ddanchev_blog")
    process.crawl("deependresearch")
    process.crawl("fireeye_blog")
    process.crawl("forcepoint_blog")
    process.crawl("hexacorn_blog")
    process.crawl("honeynet")
    process.crawl("hotforsecurity")
    process.crawl("hphosts_blog")
    process.crawl("infoblox")
    process.crawl("infosecinstitute")
    process.crawl("infosecurity_blog")
    process.crawl("insights_sei")
    process.crawl("juniper")
    process.crawl("kahusecurity")
    process.crawl("karambasecurity")
    process.crawl("krebsonsecurity")
    process.crawl("securelist")
    process.crawl("securityintelligence")
    process.crawl("symantec-enterprise-blogs")
    process.crawl("thehackernews")
    process.crawl("upstream_auto")
    process.crawl("upstream_automotive")
    process.crawl("rsa_digital")
    process.crawl("schneier_blog")
    process.crawl("skullsecurity")
    process.crawl("trustwave")
    process.crawl("sucuri_blog")    
    process.start()


# Run log-0402:
# ddanchev - website formate updated
# hexacorn
# infosecurity_blog
# inforsecinstitute
# juniper - async post form failed
# securelist