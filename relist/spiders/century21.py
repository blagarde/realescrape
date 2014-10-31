from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from relist.items import Property
import re


URL_TEMPLATE = "http://www.century21.fr/annonces/achat-appartement/cp-%s/s-40-/st-0-/b-0-400000/"


class Century21Spider(CrawlSpider):

    name = 'century21'
    allowed_domains = ['century21.fr']
    start_urls = [URL_TEMPLATE % postcode for postcode in "75010 75011 75012 75018 75019 75020".split(' ')]
    regex = r'http://www\.century21\.fr/trouver_logement/detail/\d+/'
    f = lambda link: re.match(r'(http://www\.century21\.fr/trouver_logement/detail/\d+/).*').groups()[0]
    rules = [Rule(LinkExtractor(allow=regex), 'parse_ad'),
        Rule(LxmlLinkExtractor(allow='.*',
            restrict_xpaths="//div[contains(@class,'btnSUIV_PREC suivant')]/a[contains(text(), 'suivant')]",
            process_value=f))]

    def parse_ad(self, response):
        pty = Property()
        pty['url'] = response.url
        pty['listed_on'] = self.name

        # Price
        price = ' '.join(response.css('section.tarif span b').xpath('text()').extract())
        pty['price'] = int(re.sub('\s+', ' ', price).replace(u'\xa0', '').rstrip().strip(u' \u20ac').replace(' ', ''))

        # Surface
        details = ' '.join(response.css('section.precision p').xpath("text()").extract())
        pty['size'] = float(re.search(r'(\d+,?\d*) ?[mM][2\xb2]', details).groups()[0].replace(',', '.'))

        # Post code
        filariane = ' '.join(response.css('div#filAriane div a span').xpath("text()").extract())
        pty['postcode'] = int(re.search(r'(750\d{2})', filariane).groups()[0])
    
        # Content
        pty['title'] = ' '.join(response.css('h1.h1_page').xpath('text()').extract())
        pty['description'] = ' '.join(response.css('div#descTextAnnonce.descriptionLongue p').xpath('text()').extract())

        # Price per square meter
        pty['ppsqm'] = float(pty['price']) / pty['size']

        return pty
    