import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://lipetsk.hh.ru/search/vacancy?area=&fromSearchLine=true&st=searchVacancy&text=python']

    def parse(self, response: HtmlResponse):
        links = response.xpath(
            '//div[contains(@data-qa, "__vacancy")]//span[contains(@class, "__name")]//a/@href'
        ).getall()

        for link in links:
            yield response.follow(link, callback=self.process_item)

        next_page = response.xpath(
            '//a[contains(@class, "HH-Pager-Controls-Next")]/@href'
        ).get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def process_item(self, response: HtmlResponse):
        name = response.xpath("//h1//text()").get()
        item = JobparserItem()
        item["url"] = response.url
        item["name"] = name
        item["salary"] = response.xpath('//p[@class="vacancy-salary"]//span/text()').getall()
        yield item
