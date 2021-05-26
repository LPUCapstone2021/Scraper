 import scrapy
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.html import replace_escape_chars

from Scraper.items import ZigwheelsItem

class ZigwheelsSpider(CrawlSpider):
    name = 'zigwheels'
    allowed_domains = ['zigwheels.com']
    start_urls = ['https://zigwheels.com/newcars']

    def parse(self, response):
        for route in response.xpath('//*[@id="zwn-brandslider"]/li/a/@href'):
            url = response.urljoin(route.get())
            yield scrapy.Request(url, callback=self.parse_car)

    def parse_car(self, response):
        for route in response.xpath('//*[@id="modelList"]/li/div/div[1]/a/@href'):
            url = response.urljoin(route.get())
            yield scrapy.Request(url, callback=self.parse_car_rating)

    def parse_car_rating(self, response):
        loader = ItemLoader(item = ZigwheelsItem())

        rating = {}

        for i, li in enumerate(response.css('ul.p-list li')):
            if i > 2: break
            rating[replace_escape_chars(li.css('div.m-wl::text').get().lower().split(' ')[0])] = replace_escape_chars(li.css('div.m-wr::text').get())
        for li in response.css('div.rv-ls ul li'):
            rating[replace_escape_chars(li.css('div.m-wl::text').get().lower().split(' ')[0])] = replace_escape_chars(li.css('div.m-wr::text').get())

        loader.add_value('brand', response.xpath('//div[@class="zw-cmn-containerColor"]/div/ol/li[3]/a/span/text()').get())
        loader.add_value('name', response.xpath('//div[@class="zw-cmn-containerColor"]/div/ol/li[4]/a/span/text()').get())
        loader.add_value('mileage', rating['mileage'])
        loader.add_value('performance', rating['performance'])
        loader.add_value('maintenance', rating['maintenance'])
        loader.add_value('comfort', rating['comfort'])
        loader.add_value('safety', rating['safety'])
        loader.add_value('features', rating['features'])

        yield loader.load_item()
