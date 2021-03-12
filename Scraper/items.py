# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

def extract_brand(route):
	return route.split("/")[-2]

def extract_rating(stars):
    rating = []
    for star in stars:
        if star.css('span').xpath('@class').re(r'icon-star-full-fill'):
            rating.append(1)
        elif star.css('span').xpath('@class').re(r'icon-star-half-empty'):
            rating.append(0.5)
        elif star.css('span').xpath('@class').re(r'icon-star-full-empty'):
            rating.append(0)               
    return rating[1::]

class ScraperItem(scrapy.Item):
	# define the fields for your item here like:
	brand = scrapy.Field()
	reviews = scrapy.Field()
	name = scrapy.Field()

	review_title = scrapy.Field()
	review_content = scrapy.Field()
	review_user = scrapy.Field()
	review_date = scrapy.Field()
