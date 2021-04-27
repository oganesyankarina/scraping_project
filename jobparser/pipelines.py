# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from pymongo import MongoClient
from itemadapter import ItemAdapter


class JobparserPipeline:
    def __init__(self):
        # TODO: где нужно поставить self.client.close()
        self.client = MongoClient("localhost:27017")
        self.db = self.client["vacancies"]

    def process_item(self, item, spider: scrapy.Spider):
        # Определять новые поля без определения их в вашем классе Item нельзя
        # item['abracadabra'] = 42
        # Так можно удалять
        # del item['name']
        # item.pop("name")
        # TODO:
        try:
            item['salary_min'] = self.parse_salary(item['salary'])[0]
            item['salary_max'] = self.parse_salary(item['salary'])[1]
            item['salary_currency'] = self.parse_salary(item['salary'])[2]
        except Exception as e:
            item['salary_min'] = 'з/п не указана'
            item['salary_max'] = 'з/п не указана'
            item['salary_currency'] = 'з/п не указана'
        del item['salary']
        item['url'] = item['url'].split('?')[0]
        item['source'] = spider.allowed_domains[0]
        # print("42")
        # своя коллекция для каждого паука

        # self.db[spider.name].insert_one(item)
        self.db[spider.name].update_one({'url': {"$eq": item['url']}}, {'$set': item}, upsert=True)
        # self.db[spider.name].update_one({"$and": [{'url': {"$eq": item['url']}},
        #                                           {'name': {"$eq": item['name']}}]},
        #                                 {'$set': item}, upsert=True)
        # примеры
        # if spider.name:
        #     ...
        # if "somedomain" in spider.allowed_domains:
        #     ...
        # self.db['hhru'].insert_one(item)
        # self.db['hhru'].update_one(...)

        # print()
        return item

    def parse_salary(self, salary):
        if salary[2] == ' до ':
            salary_min = salary[1]
            salary_max = salary[3]
            currency = salary[5]
        elif salary[0] == 'до ':
            salary_min = None
            salary_max = salary[1]
            currency = salary[3]
        elif salary[0] == 'от ':
            salary_min = salary[1]
            salary_max = None
            currency = salary[3]
        else:
            salary_min = 'з/п не указана'
            salary_max = 'з/п не указана'
            currency = 'з/п не указана'
        return [salary_min, salary_max, currency]
