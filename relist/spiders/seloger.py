from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from relist.items import Property
import re


URL_TEMPLATE = "http://www.seloger.com/list.htm?ci=7501%s&idtt=2&idtypebien=1&pxmax=400000&nb_pieces=1%%2c2%%2c3%%2c4%%2c4%%2b&surfacemin=40"


class SeLogerSpider(CrawlSpider):

    name = 'seloger'
    allowed_domains = ['seloger.com']
    start_urls = [URL_TEMPLATE % postcode for postcode in "10 11 12 18 19 20".split(' ')]
    rules = [Rule(LxmlLinkExtractor(allow='.*', restrict_xpaths="//div[contains(@class,'listing_infos')]/h2/a"), 'parse_ad'),
        Rule(LxmlLinkExtractor(allow='.*', restrict_xpaths="//a[contains(@class,'pagination_next')][contains(text(), 'Page suivante')]"))]

    def parse_ad(self, response):
        pty = Property()
        pty['url'] = response.url.split('?ci=')[0]
        pty['listed_on'] = self.name

        # Price
        price = ' '.join(response.css('span.resume__prix').xpath('text()').extract())
        pty['price'] = int(re.sub('\s+', ' ', price).replace(u'\xa0', '').rstrip().strip(u' \u20ac').replace(' ', ''))

        # Post code
        text = response.css('div#detail h2 span').xpath('text()')[0].extract()
        postcode = '750' + re.match(ur' \xe0 Paris (\d{2})\xe8me', text).groups()[0]
        pty['postcode'] = int(postcode)
    
        # Content
        title = response.css('h1.detail-title').xpath('text()').extract()[0]
        title = re.sub('\s+', ' ', title)
        pty['title'] = title
        pty['description'] = ' '.join(response.css('p.description').xpath('text()').extract())

        # Surface
        try:
            criteria = ' '.join(response.css('div.criterions li.resume__critere').xpath('text()').extract())
            pty['size'] = float(re.search(r'(\d+,?\d*) ?[mM][2\xb2]', criteria).groups()[0].replace(',', '.'))
        except:  # look for the surface in the title
            pty['size'] = float(re.search(r'(\d+,?\d*) ?[mM][2\xb2]', title).groups()[0].replace(',', '.'))


        # Price per square meter
        pty['ppsqm'] = float(pty['price']) / pty['size']

        return pty
    