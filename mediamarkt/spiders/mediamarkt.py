import scrapy
from ..items import MediamarktItem
from scrapy.exceptions import CloseSpider


def parse_items(response):
    global price
    product = MediamarktItem()

    unavailable = response.css('div.offer-unavailable').get()
    name = response.css('h1.title.is-heading::text').get()
    if name is not None:
        if unavailable is None:
            price_box_div = response.css('div.price-box')
            main_price = price_box_div.css('div.main-price.is-big')
            price = main_price.css('span.whole::text').get().strip()
        else:
            price = 'UNAVAILABLE'

        product['name'] = name
        product['price'] = price

        yield product


class MediamarktScrapySpider(scrapy.Spider):
    name = 'mediamarkt'

    def start_requests(self):
        yield scrapy.Request(f'https://mediamarkt.pl/outlet/telefony-i-smartfony/smartfony/{self.category}/')

    def parse(self, response, **kwargs):
        list_page = response.css('div.offers.is-list')

        if response.status == 404:
            raise CloseSpider('Received 404 response')

        if len(list_page.css('div.more-offers')) == 0:
            raise CloseSpider('No items on the page')

        for link in list_page.css('a.is-hover-underline.spark-link ::attr(href)'):
            yield response.follow(link, callback=parse_items)

        next_page = list_page.css('a.spark-button.button.is-primary.is-default.icon-left::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

# category=wszystkie-smartfony
# category=iphone
# category=galaxy
# category=smartfony-5g
# category=fold

