import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags, replace_escape_chars

class PersonItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    standout_features = scrapy.Field()    
    key_specifications = scrapy.Field()    
    key_features = scrapy.Field()    
    price = scrapy.Field(
        input_processor=MapCompose(remove_tags, lambda price: price[:-1]), 
        output_processor=TakeFirst()
    )
    brand = scrapy.Field(
        input_processor=MapCompose(lambda brand: brand.split('/')[-3]), 
        output_processor=TakeFirst()
    ) 
    rating = scrapy.Field(
        input_processor=MapCompose(lambda stars: (stars.count('icon-star-full-fill') * 1) + (stars.count('icon-star-half-empty') * 0.5)), 
        output_processor=TakeFirst()
    )    
    review_title = scrapy.Field()
    review_content = scrapy.Field(
        input_processor=MapCompose(replace_escape_chars), 
        output_processor=TakeFirst()
    )    
    review_username = scrapy.Field(
        input_processor=MapCompose(remove_tags, lambda username: username[3:]), 
        output_processor=TakeFirst()
    )
    review_date = scrapy.Field(
        input_processor=MapCompose(remove_tags, lambda date: date.split("|")[0].strip()[4:]), 
        output_processor=TakeFirst()
    )
