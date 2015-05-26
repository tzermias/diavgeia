from diavgeia.items import DiavgeiaItem
from scrapy.spider import BaseSpider
from scrapy import log
from scrapy.selector import XmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http.request import Request
from datetime import date, timedelta

class DiavgeiaSpider(BaseSpider):
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
        self.log("Initialized DiavgeiaSpider object", level=log.DEBUG)
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
                    self.log("Argument %s is not a valid argument" % key,
                            level=log.WARNING) 
            lala = "&".join(args_array) 
            self.log("Arguments: %s" % lala, level=log.DEBUG)
            self.url =self.base_url + "search?" + lala + "&page=%s"
            self.start_urls = [ self.url % (kwargs['page'] if 'page' in
                kwargs.keys() else 0,)]
            self.log("Request: %s" % self.start_urls[0], level=log.DEBUG)
        else:
            from_date = (date.today() - timedelta(1))
            self.url = self.base_url + \
            "search?from_date=%s&to_date=%s&size=100&page=%%s" % (from_date,
                    date.today())
            self.start_urls = [ self.url % (0,)]

    def parse (self, response):
        xxs = XmlXPathSelector(response)
        xxs.register_namespace("xmlns", "http://diavgeia.gov.gr/schema/v2")

        # Parse Decision
        decisions = xxs.select("//xmlns:decisions/xmlns:decision")

        # Print debug the query field of the XML
        query = xxs.select("//xmlns:info/xmlns:query/text()").extract()[0]
        self.log("Query: %s" % query, level=log.DEBUG)
        for decision in decisions:
            d = DiavgeiaItem()
            for element in decision.select("*"):
                name = element.select("name(.)").extract()[0]
                if len (element.select("*")) != 0:
                    #Handle elements with children here
                    print element
                    d[name] = []
                    for child in element.select("*"):
                        #TODO: Add support for extraValues field
                        ch = {}
                        childname = child.select("name(.)").extract()[0]
                        if len (child.select("./text()" )) != 0:
                            chvalue = child.select("./text()").extract()[0]
                            ch[childname]=chvalue
                        d[name].append(ch)
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
