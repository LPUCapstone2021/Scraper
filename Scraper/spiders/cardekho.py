# yield scrapy.Request(url, callback=self.parse_car, cb_kwargs={'car_route': car_route})



import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
# from scrapy.loader import ItemLoader
from Scraper.items import ScraperItem
from w3lib.html import remove_tags

class CardekhoSpider(CrawlSpider):
    name = 'cardekho'
    allowed_domains = ['cardekho.com']
    start_urls = ['https://cardekho.com/newcars']

    rules = (
        Rule(LinkExtractor(allow=r'cars/'), callback='parse_brand', follow=True),
    )

    def parse_brand(self, response):
        item = ScraperItem()
        for car_route in response.css('section.BrandPagelist li .listView h3 a::attr(href)').getall():
            url = response.urljoin(f'{car_route}/user-reviews')
            yield scrapy.Request(url, callback=self.parse_car, cb_kwargs={'item': item})

    def parse_car(self, response, item):
        item['brand'] = response.url.split('/')[-3]
        item['name'] = response.css('div.title a::text').get()
        for review in response.css('section.ReadReview div.gsc-ta-active li div.readReviewHolder'):
            # item['reviews'] = {
            #     'title': review.css('h3 a::text').get(),
            #     'content': review.css('p::text').get(),
            #     'user': remove_tags(review.css('.authorSummary .name').get())[3:],
            #     'date': remove_tags(review.css('.authorSummary .date').get()).split("|")[0].strip()
            # }
            item['review_title'] = review.css('h3 a::text').get()
            item['review_content'] = review.css('p::text').get().strip("\n")
            item['review_user'] = remove_tags(review.css('.authorSummary .name').get())[3:]
            item['review_date'] = remove_tags(review.css('.authorSummary .date').get()).split("|")[0].strip()
        yield item
