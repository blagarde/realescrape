from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from relist.items import Property
import re


URL_TEMPLATE = "http://totalimmo.thetranet.fr/transaction/resultat.php?provenance=index&client_code=AUBU&typebienvente_id=1&piecemin=&piecemax=&chambremin=&chambremax=&surfacemin=40&surfacemax=&prixmin=&prixmax=400000&vvirt=&cp1=%s&cp2=&cp3=&cp4=&cp5=&ville1=&ville2=&ville3=&nbelementpage=1000&btSearch.x=17&btSearch.y=9"

class AuburtinSpider(CrawlSpider):

    name = 'auburtin'
    allowed_domains = ['thetranet.fr']
    start_urls = [URL_TEMPLATE % postcode for postcode in "75018".split(' ')]
    regex = r'http://totalimmo\.thetranet\.fr/transaction/detail\.php\?client_code=AUBU&bien_id=\d+&agence_id=\d+&nbResultat=\d+&numpage=\d+&orderShort=prixasc'
    rules = [Rule(LinkExtractor(allow=regex), 'parse_ad')]

    def parse_ad(self, response):
        pty = Property()
        pty['url'] = response.url
        pty['listed_on'] = self.name

        # Price
        titreresulta = response.css('tr.titreresulta td b').xpath('text()').extract()
        prices = [re.match(ur'([0-9 ]+) \u20ac', elt) for elt in titreresulta]
        prices = [m.groups()[0] for m in prices if m is not None]
        assert len(prices) == 1
        pty['price'] = int(prices[0].replace(' ', ''))

        # Surface
        matches = [re.search(r'(\d+\.?\d*) ?[mM][2\xb2]', text) for text in  response.css('tr td').xpath('text()').extract()]
        matches = [m.groups()[0] for m in matches if m is not None]
        assert len(set(matches)) >= 1
        pty['size'] = sorted(map(float, matches))[-1]

        # Post code
        matches = [re.search(r'(750\d{2})', text) for text in titreresulta]
        matches = [m.groups()[0] for m in matches if m is not None]
        assert len(matches) == 1
        pty['postcode'] = int(matches[0])
    
        # Content
        shortdesc = response.css('tr.lignresulta td b').xpath('text()').extract()
        assert len(shortdesc) == 1
        pty['title'] = shortdesc[0]

        descriptions = response.css('tr.lignresulta td div').xpath('text()').extract()
        pty['description'] = ' '.join(descriptions)

        # Price per square meter
        pty['ppsqm'] = float(pty['price']) / pty['size']

        return pty
    