import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from vietinbank.items import Article


class VietinbankSpider(scrapy.Spider):
    name = 'vietinbank'
    start_urls = ['https://www.vietinbank.de/sites/home/de/News']

    def parse(self, response):
        links = response.xpath('//a[@class="link-topnews"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//div[@class="content_main_title left fs16 fwb fw widthmax"]/div/b/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//div[@class="news_writer"]/span/text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@class="left news_content"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
