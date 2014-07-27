from diavgeia.items import DiavgeiaItem
from scrapy.spider import BaseSpider
from scrapy import log
from scrapy.selector import XmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http.request import Request

class DiavgeiaSpider(BaseSpider):
    """ DiavgeiaSpider
    
    The class that performs the whole spider mechanism.
    """
    name = "diavgeia_spider"
    allowed_domains = ["diavgeia.gov.gr"]
    base_url = "https://test3.diavgeia.gov.gr/luminapi/opendata/"

    def __init__(self , *args, **kwargs):
        super(DiavgeiaSpider, self).__init__(*args, **kwargs)
        self.log("Initialized DiavgeiaSpider object", level=log.DEBUG)
        self.url = self.base_url + \
        "search?from_date=01-01-2014&to_date=02-01-2014&size=100&page=%s"
        self.start_urls = [ self.url % (0,)]

    def parse (self, response):
        xxs = XmlXPathSelector(response)
        xxs.register_namespace("xmlns", "http://diavgeia.gov.gr/schema/v2")

        # Parse Decision
        decisions = xxs.select("//xmlns:decisions/xmlns:decision")
        for decision in decisions:
            d = DiavgeiaItem()
            for element in decision.select("*"):
                #TODO: This handles only elements with no children
                name = element.select("name(.)").extract()[0]
                if len (element.select("./text()" )) != 0:
                    value = element.select("./text()").extract()[0]
                    d[name] = value
            yield d

        # Get next page info
        total = int(xxs.select("//xmlns:info/xmlns:total/text()").extract()[0])
        page = int(xxs.select("//xmlns:info/xmlns:page/text()").extract()[0])
        size = int(xxs.select("//xmlns:info/xmlns:size/text()").extract()[0])
        if (page*size <= total):
            yield Request(self.url % (page+1), self.parse)

        
# vi: ts=4 sts=4 et sw=4 tw=80
