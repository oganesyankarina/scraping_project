import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruspiderSpider(scrapy.Spider):
    name = 'SjruSpider'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python']

    def parse(self, response: HtmlResponse):
        # '//div[contains(@class, "search-result-item")]'

        # links = response.xpath(
        #     '//div[contains(@data-qa, "__vacancy")]//span[contains(@class, "__name")]//a/@href'
        # ).getall()
        #
        # for link in links:
        #     yield response.follow(link, callback=self.process_item)
        #
        # next_page = response.xpath(
        #     '//a[contains(@class, "HH-Pager-Controls-Next")]/@href'
        # ).get()
        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)
        pass

    def process_item(self, response: HtmlResponse):
        # name = response.xpath("//h1//text()").get()
        # item = JobparserItem()
        # item["url"] = response.url
        # item["name"] = name
        # item["salary"] = response.xpath('//p[@class="vacancy-salary"]//span/text()').getall()
        # yield item
        pass

