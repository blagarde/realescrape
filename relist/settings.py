# -*- coding: utf-8 -*-

# Scrapy settings for relist project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'relist'

SPIDER_MODULES = ['relist.spiders']
NEWSPIDER_MODULE = 'relist.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'relist (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'relist.pipelines.DjangoPipeline': 300,
}

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'realescrape.settings'
import django
django.setup()