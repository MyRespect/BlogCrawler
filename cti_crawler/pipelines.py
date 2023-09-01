# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from cti_crawler.database import CTI_DB

class CtiCrawlerPipeline:
    def process_item(self, item, spider):
        table_name = ''
        if spider.name == 'cybersecurity_att':
            table_name = 'cybersecurity_att'
        elif spider.name == 'carnal0wnage':
        	table_name = 'carnal0wnage'
        elif spider.name == 'insights_sei':
        	table_name = 'insights_sei'
        elif spider.name == 'coresecurity_blog':
        	table_name = 'coresecurity_blog'
        elif spider.name == 'symantec-enterprise-blogs':
        	table_name = 'symantec_enterprise_blogs' # - is not allowed
        elif spider.name == 'cloudflare_blog':
            table_name = 'cloudflare_blog'
        elif spider.name == 'crowdstrike_blog':
            table_name = 'crowdstrike_blog'
        elif spider.name == 'darknet_blog':
            table_name = 'darknet_blog'
        elif spider.name == 'deependresearch':
            table_name = 'deependresearch'
        elif spider.name == 'ddanchev_blog':
            table_name = 'ddanchev_blog'
        elif spider.name == 'fireeye_blog':
            table_name = 'fireeye_blog'
        elif spider.name == 'forcepoint_blog':
            table_name = 'forcepoint_blog'
        elif spider.name == 'karambasecurity':
            table_name = 'karambasecurity'
        elif spider.name == 'argu_sec':
            table_name = 'argu_sec'
        elif spider.name == 'upstream_auto':
            table_name = 'upstream_auto'
        elif spider.name == 'hexacorn_blog':
            table_name = 'hexacorn_blog'
        elif spider.name == 'hotforsecurity':
            table_name = 'hotforsecurity'
        elif spider.name == 'hphosts_blog':
            table_name = 'hphosts_blog'
        elif spider.name == 'thehackernews':
            table_name = 'thehackernews'
        elif spider.name == 'honeynet':
            table_name = 'honeynet'
        elif spider.name == 'infosecinstitute':
            table_name = 'infosecinstitute'
        elif spider.name == 'infosecurity_blog':
            table_name = 'infosecurity_blog'
        elif spider.name == 'securityintelligence':
            table_name = 'securityintelligence'
        elif spider.name == 'infoblox':
            table_name = 'infoblox'
        elif spider.name == 'juniper':
            table_name = 'juniper'
        elif spider.name == 'securelist':
            table_name = 'securelist'
        elif spider.name == 'kahusecurity':
            table_name = 'kahusecurity'
        elif spider.name == 'krebsonsecurity':
            table_name = 'krebsonsecurity'
        elif spider.name == 'upstream_automotive':
            table_name = 'upstream_automotive'
        elif spider.name == 'embitel_embeded':
            table_name = 'embitel_embeded'
        elif spider.name == 'auth0_blog':
            table_name = 'auth0_blog'
        elif spider.name == 'teskalabs':
            table_name = 'teskalabs'
        elif spider.name == 'autotrainingcentre':
            table_name = 'autotrainingcentre'
        elif spider.name == 'bdtechtalks':
            table_name = 'bdtechtalks'
        elif spider.name == 'c2a_sec':
            table_name = 'c2a_sec'
        elif spider.name == 'c2a_sec':
            table_name = 'c2a_sec'
        elif spider.name == 'rsa_digital':
            table_name = 'rsa_digital'
        elif spider.name == 'schneier_blog':
            table_name = 'schneier_blog'
        elif spider.name == 'skullsecurity':
            table_name = 'skullsecurity'
        elif spider.name == 'trustwave':
            table_name = 'trustwave'
        elif spider.name == 'sucuri_blog':
            table_name = 'sucuri_blog'
        source = CTI_DB(table_name)
        db=source.connection()
        source.create_table(db)
        source.add_item(item, db)
        return item
