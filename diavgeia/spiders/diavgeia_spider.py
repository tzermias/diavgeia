from diavgeia.items import *
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http.request import Request
from datetime import date, timedelta

class DiavgeiaSpider(Spider):
    """ DiavgeiaSpider
    
    The class that performs the whole spider mechanism.
    """
    name = "diavgeia_spider"
    allowed_domains = ["diavgeia.gov.gr"]
    allowed_arguments = (
            "ada", "org", "subject", "protocol", "term", "unit", "signer",
            "type", "tag", "from_date", "to_date", "from_issue_date", "status",
            "size"
        )
    base_url = "https://test3.diavgeia.gov.gr/luminapi/opendata/"

    def __init__(self , *args, **kwargs):
        super(DiavgeiaSpider, self).__init__(*args, **kwargs)
        self.logger.debug("Initialized DiavgeiaSpider object")
        # Parse arguments.
        # Currently legal arguments are ada, subject, protocol, term, unit,
        # signer, type, tag, from_date, to_date, from_issue_date, status and size
        # If no arguments are specified, then the crawler retrieves every
        # decision submitted the previous day.
        if len(kwargs) > 0:
            args_array = []
            for key in kwargs:
                if key in self.allowed_arguments:
                    args_array.append("%s=%s" % (key, kwargs[key]))
                else:
                    self.logger.warning("Argument %s is not a valid argument" % key) 
            lala = "&".join(args_array) 
            self.logger.debug("Arguments: %s" % lala)
            self.url =self.base_url + "search?" + lala + "&page=%s"
            self.start_urls = [ self.url % (kwargs['page'] if 'page' in
                kwargs.keys() else 0,)]
            self.logger.debug("Request: %s" % self.start_urls[0])
        else:
            from_date = (date.today() - timedelta(1))
            self.url = self.base_url + \
            "search?from_date=%s&to_date=%s&size=100&page=%%s" % (from_date,
                    date.today())
            self.start_urls = [ self.url % (0,)]


    def parse (self, response):
        xxs = Selector(response)
        xxs.register_namespace("xmlns", "http://diavgeia.gov.gr/schema/v2")

        # Parse Decision
        decisions = xxs.xpath("//xmlns:decisions/xmlns:decision")

        # Print debug the query field of the XML
        query = xxs.xpath("//xmlns:info/xmlns:query/text()").extract()[0]
        self.logger.debug("Query: %s" % query)
        for decision in decisions:
            d = DiavgeiaItem()
            for element in decision.xpath("*"):
                name = element.xpath("name(.)").extract()[0]
                if len (element.xpath("*")) != 0:
                    #Handle elements with children here
                    d[name] = []
                    for child in element.xpath("*"):
                        #TODO: Add support for extraValues field
                        ch = {}
                        childname = child.xpath("name(.)").extract()[0]
                        if len (child.xpath("./text()" )) != 0:
                            chvalue = child.xpath("./text()").extract()[0]
                            ch[childname]=chvalue
                            # Get information about signers, units etc.
                            if childname == "signerId":
                                yield Request(self.base_url + \
                                        "signers/%s" % (chvalue),
                                        self.parseSigner)
                        d[name].append(ch)
                if len (element.xpath("./text()" )) != 0:
                    value = element.xpath("./text()").extract()[0]
                    d[name] = value
            yield d

        # Get next page info
        total = int(xxs.xpath("//xmlns:info/xmlns:total/text()").extract()[0])
        page = int(xxs.xpath("//xmlns:info/xmlns:page/text()").extract()[0])
        size = int(xxs.xpath("//xmlns:info/xmlns:size/text()").extract()[0])
        if (page*size <= total):
            yield Request(self.url % (page+1), self.parse)

    def parseSigner(self, response):
        """ Parse data for signer (first name, last name etc) """
        xxs = Selector(response)
        xxs.register_namespace("xmlns", "http://diavgeia.gov.gr/schema/v2")

        signers = xxs.xpath("//xmlns:signer")
        s = Signer()
        for signer in signers.xpath("*"):
            name = signer.xpath("name(.)").extract()[0]
            if len (signer.xpath("./text()" )) != 0:
                value = signer.xpath("./text()").extract()[0]
                s[name] = value
        yield s

        
# vi: ts=4 sts=4 et sw=4 tw=80
