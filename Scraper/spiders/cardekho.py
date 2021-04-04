import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Scraper.items import PersonItem

class CardekhoSpider(CrawlSpider):
    name = 'cardekho'
    allowed_domains = ['cardekho.com']
    start_urls = ['https://cardekho.com/newcars']

    rules = (
        Rule(LinkExtractor(allow=r'cars/'), callback='parse_brand', follow=True),
    )

    def parse_brand(self, response):
        for car_route in response.css('section.BrandPagelist li .listView h3 a::attr(href)').getall():
            url = response.urljoin(f'{car_route}/specs')
            yield scrapy.Request(url, callback=self.parse_car_specs, cb_kwargs={'base_url': response, 'car_route': car_route})

    def parse_car_specs(self, response, base_url, car_route):
        car = {
            "brand": response.url,
            "name": response.css('div.title a::text').get(),
            "price": response.css('div.price span span').get(),
            "description": response.css('section.carSummary p::text').get(),
            "key_specifications": [{tr.css('td::text').get(): tr.css('td.right span::text').get()} for tr in response.xpath('//div[contains(@data-id, "Specifications")]').css('table.keyfeature tbody tr')],
            "key_features": [{tr.css('td::text').get(): True if tr.css('td.right i.icon-check').get() else False} for tr in response.xpath('//div[contains(@data-id, "Features")]').css('table.keyfeature tbody tr')],
            "standout_features": [li.css('div.card p::text').get() for li in response.css('section.designHighlightsMain ul li')]
        }
        url = base_url.urljoin(f'{car_route}/user-reviews')
        yield scrapy.Request(url, callback=self.parse_user, meta={'car': car})

    def parse_user(self, response):
        car = response.meta['car']
        for review in response.css('section.ReadReview div.gsc-ta-active li div.readReviewHolder'):
            loader = ItemLoader(item = PersonItem(), selector=review)
            loader.add_value('brand', car['brand'])
            loader.add_value('name', car['name'])
            loader.add_value('price', car['price'])
            loader.add_value('description', car['description'])
            loader.add_value('standout_features', car['standout_features'])
            loader.add_value('key_specifications', car['key_specifications'])
            loader.add_value('key_features', car['key_features'])

            loader.add_css('review_username', '.authorSummary .name')
            loader.add_css('review_title', 'h3 a::text')
            loader.add_css('review_content', 'p span::text')
            loader.add_css('review_date', '.authorSummary .date')
            loader.add_css('rating', 'div.rating span')
            yield loader.load_item()
