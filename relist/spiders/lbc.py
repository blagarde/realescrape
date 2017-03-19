from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from relist.items import Property
import re


URL_TEMPLATE = "https://www.leboncoin.fr/ventes_immobilieres/offres/ile_de_france/?f=a&th=1&pe=15&sqs=5&ret=2&location=Paris%%20%s"


class LBCSpider(CrawlSpider):

    name = 'lbc'
    allowed_domains = ['leboncoin.fr']
    start_urls = [URL_TEMPLATE % postcode for postcode in "75010 75011 75012 75018 75019 75020".split(' ')]
    regex = r'https://www\.leboncoin\.fr/ventes_immobilieres/\d+.htm\?ca=12_s'
    rules = [Rule(LinkExtractor(allow=regex), 'parse_ad'),
        Rule(LxmlLinkExtractor(allow='.*', restrict_xpaths="//nav/ul/li/a[contains(text(), 'Page suivante')]"))]

    def parse_ad(self, response):
        pty = Property()
        pty['url'] = response.url
        pty['listed_on'] = self.name

        # The page has a JS variable called utag_data which conveniently contains the data we're after.
        utag_data = response.xpath('//script/text()[contains(., "utag_data")]')[0].extract()

        pty['price'] = int(re.search('prix : "(?P<prix>[^"]+)"', utag_data).groupdict()["prix"])
        pty['size'] = float(re.search('surface : "(?P<surface>[^"]+)"', utag_data).groupdict()["surface"])
        pty['postcode'] = int(re.search('cp : "(?P<cp>[^"]+)"', utag_data).groupdict()["cp"])

        # # Price
        # prices = response.css('h2.item_price').xpath("@content").extract()
        # assert len(prices) == 1
        # pty['price'] = int(prices[0].rstrip(u' $\u20ac').replace(' ', ''))
        # # Surface
        # row = response.xpath("//h2/span[contains(sup/text(), '2')]/text()")
        # surfaces = row.extract()
        # assert len(surfaces) == 1
        # pty['size'] = float(surfaces[0].rstrip(' mM'))

        # # # Post code  #  -- Broken
        # # row = response.css('.lbcParams.criterias').xpath("//tr[contains(th//text(), 'Code postal')]")
        # # postcodes = row.xpath('td/text()').extract()
        # # assert len(postcodes) == 1
        # # pty['postcode'] = int(postcodes[0])
    
        # Content
        pty['title'] = response.css('h1[itemprop="name"]').xpath('text()').extract()[0].strip()
        pty['description'] = ' '.join(response.css('p[itemprop="description"]').xpath('text()').extract())

        # Price per square meter
        pty['ppsqm'] = float(pty['price']) / pty['size']

        return pty
    