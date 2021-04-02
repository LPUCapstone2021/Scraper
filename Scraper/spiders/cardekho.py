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
            url = response.urljoin(f'{car_route}/user-reviews')
            yield scrapy.Request(url, callback=self.parse_car)

    def parse_car(self, response):
        brand = response.url
        name = response.css('div.title a::text').get()
        for review in response.css('section.ReadReview div.gsc-ta-active li div.readReviewHolder'):
            loader = ItemLoader(item = PersonItem(), selector=review)
            loader.add_value('brand', brand)
            loader.add_value('name', name)
            loader.add_css('review_username', '.authorSummary .name')
            loader.add_css('review_title', 'h3 a::text')
            loader.add_css('review_content', 'p span::text')
            loader.add_css('review_date', '.authorSummary .date')
            loader.add_css('rating', 'div.rating span')
            yield loader.load_item()