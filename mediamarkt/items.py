import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


def clean(value):
    value = value.replace('\n', ' ').strip()
    value = value.replace('  ', ' ').strip()
    return value.replace('zł', '').strip()


class MediamarktItem(scrapy.Item):
    name = scrapy.Field(input_processor=MapCompose(remove_tags, clean), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(remove_tags, clean), output_processor=TakeFirst())