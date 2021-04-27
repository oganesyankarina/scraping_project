import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruspiderSpider(scrapy.Spider):
    name = 'SjruSpider'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python']

    def parse(self, response: HtmlResponse):
        links = response.xpath(
            '//div[contains(@class, "search-result-item")]//a[contains(@target, "_blank")]/@href'
        ).getall()
        print('ссылки на вакансии найдены')
        print(links)

        for link in links:
            yield response.follow('https://www.superjob.ru' + link, callback=self.process_item)

        next_page = response.xpath(
            '//a[contains(@class, "button-dalshe")]/@href'
        ).get()
        print('кнопка Дальше найдена')
        print(next_page)
        if next_page:
            yield response.follow('https://www.superjob.ru' + next_page, callback=self.parse)
        pass

    def process_item(self, response: HtmlResponse):
        name = response.xpath("//h1//text()").get()
        item = JobparserItem()
        item["url"] = response.url
        item["name"] = name
        # item["salary"] = response.xpath('//p[@class="vacancy-salary"]//span/text()').getall()
        yield item

