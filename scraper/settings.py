# Scrapy settings for scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'scraper'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

FEED_FORMAT = 'json'

FEED_URI = 'items.json'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'MarkNemec'
