import scrapy
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from Scraper.items import Car

class ZigwheelsSpider(CrawlSpider):
    name = 'zigwheels'
    allowed_domains = ['zigwheels.com']
    start_urls = ['http://zigwheels.com/']

    rules = (
        Rule(LinkExtractor(allow=r'newcars/'), callback='parse_brand', follow=True),
    )

    def parse_brand(self, response):
        for car_route in response.css('#modelList li .mk-img-h a::attr(href)').getall():
            url = response.urljoin(car_route)
            yield scrapy.Request(url, callback=self.parse_car_specs)

    def parse_car_specs(self, response):
        for i, li in enumerate(response.css('ul.p-list li')):
            if i > 2: break
            rating[li.css('div.m-wl::text').get()] = li.css('div.m-wr::text').get()
        for li in response.css('div.rv-ls ul li'):
            rating[li.css('div.m-wl::text').get()] = li.css('div.m-wr::text').get()

