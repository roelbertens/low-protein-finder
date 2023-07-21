import scrapy


class JumboSpider(scrapy.Spider):
    name = "jumbo"
    allowed_domains = ["jumbo.com"]
    start_urls = ["https://jumbo.com"]

    def parse(self, response):
        pass
