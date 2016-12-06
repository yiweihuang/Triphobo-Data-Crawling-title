# -*- coding: utf-8 -*-
import sys
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from triphobo.items import TriphoboItem

if len(sys.argv) < 4:
    print('Usage: scrapy crawl trip_plans -o dataset/[name].csv')
    sys.exit()
else:
    csv_name = sys.argv[3]

class TripPlansSpider(scrapy.Spider):
    name = "trip_plans"
    start_urls = []
    allowed_domains = ["triphobo.com"]
    file_name = csv_name.split('/')[1].split('.')[0]
    if '_' in file_name:
        file_name = file_name.replace('_', ' ')
        start_urls = ['https://www.triphobo.com/tripplans/' + file_name]
    else:
        start_urls = ['https://www.triphobo.com/tripplans/' + file_name]

    def parse(self, response):
        item = TriphoboItem()
        trip_name = response.xpath('//div[@class="blocklist-trip-name"]/p/text()').extract()
        trip_url = response.xpath('//div[@class="blocklist-trip-name-wrapper"]/a/@href').extract()
        trip_days = response.xpath('//div[@class="blocklist-trip-details"]/span[@class="blocklist-total-days pull-left"]/text()').extract()
        trip_views = response.xpath('//div[@class="blocklist-trip-details"]/span[@class="blocklist-total-views pull-right"]/text()').extract()
        for index, name in enumerate(trip_name):
            item['name'] = name
            item['url'] = trip_url[index]
            item['days'] = trip_days[index]
            item['views'] = trip_views[index]
            yield item

        next_page = response.xpath('//ul[@class="pagination js_num_pagination"]/li[@class="next"]/a/@href').extract()
        if next_page:
            next_href = next_page[0]
            request = scrapy.Request(url=next_href)
            yield request
