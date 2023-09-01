### Cyber-Physical Threat Intelligence (CTI) Blog Crawler

#### Developer

1. Use the URL prefix of the website as the spider name, table name, and web name. 

2. Modify pipelines.py to create a table for the corresponding blog website.

3. Modify process_response in middlewares.py to process the dynamically loaded website

4. Write your own crawler in the spider folder

5. Use "xpath" helper extension in your browser to help you quickly position 

#### Usage

* scrapy crawl cybersecurity_att -s LOG_FILE=all.log

* scrapy crawl carnal0wnage -s LOG_FILE=all.log

* scrapy crawl insights_sei -s LOG_FILE=all.log

* scrapy crawl coresecurity_blog -s LOG_FILE=all.log

* scrapy crawl symantec-enterprise-blogs -s LOG_FILE=all.log
