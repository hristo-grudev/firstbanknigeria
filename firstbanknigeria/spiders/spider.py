import scrapy

from scrapy.loader import ItemLoader

from ..items import FirstbanknigeriaItem
from itemloaders.processors import TakeFirst


class FirstbanknigeriaSpider(scrapy.Spider):
	name = 'firstbanknigeria'
	start_urls = [
		'https://www.firstbanknigeria.com/home/media/press-release/',
		'https://www.firstbanknigeria.com/home/media/news-insights/'
	]

	def parse(self, response):
		post_links = response.xpath('//h3/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="page-numbers next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1[@class="elementor-heading-title elementor-size-default"]/text()').get()
		description = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "elementor-widget-theme-post-content", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "elementor-widget-container", " " ))]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-date"]/text()').get()

		item = ItemLoader(item=FirstbanknigeriaItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
