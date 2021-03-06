#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 业务包：爬出behance作品集

import scrapy
from behance.item.tagItems import tagItem, authorItem, pictureItem
import constants as cs
import behance.common.selectUrl as sel
import json


class portfolioSpider(scrapy.Spider):
    name = "portfolio"
    allowed_domains = ["behance.net"]
    headers = {
        "X-Requested-With": "XMLHttpRequest",
    }
    save_portfolio_ids = set()

    def start_requests(self):
        for tag in cs.BEHANCE_SEARCH_TAG:
            for ordinal in range(1, 10):
                url = "https://www.behance.net/search?ordinal=%s&content=projects&sort=appreciations&time=all&schema_tags=%s&user_tags=%s"
                yield scrapy.Request(url=url % (ordinal, tag, tag), callback=self.parse, headers=self.headers)

    def parse(self, response):
        if "html" not in response.body:
            return
        html = json.loads(response.body)["html"]
        portfolio_urls = sel.get_urls(html)

        for idx in range(0, len(portfolio_urls)):
            portfolio_url = portfolio_urls[idx]
            portfolio_id = portfolio_url.split("/")[4]

            self.save_portfolio_ids.add(int(portfolio_id))
            yield scrapy.Request(url=portfolio_url, callback=self.picture_parse, headers=self.headers)
        pass

    def picture_parse(self, response):
        if "view" not in response.body:
            return
        data = json.loads(response.body)["view"]["project"]
        tag_words = json.loads(response.body)["view"]["site"]["meta"]
        tags = data["tags"]
        module = data["modules"]
        for i in range(0, len(tags)):
            item = tagItem()
            tag_name = tags[i]["title"]
            tag_id = tags[i]["id"]
            pic_url = module[i]["src"]
            tag_word = tag_words["keywords"]
            item["tag_name"] = tag_name
            item["tag_id"] = tag_id
            item["pic_url"] = pic_url
            item["tag_words"] = tag_word
            yield item


class authorSpider(scrapy.Spider):
    name = "author"
    allowed_domains = ["behance.net"]
    headers = {
        "X-Requested-With": "XMLHttpRequest",
    }

    per_page = 48

    def start_requests(self):
        for ordinal in range(0, 10):
            _ordinal = self.per_page * ordinal
            url = "https://www.behance.net/search?ordinal=%s&per_page=48&content=users&sort=appreciations&time=all&country=CN"
            yield scrapy.Request(url=url % _ordinal, callback=self.parse, headers=self.headers)

    def parse(self, response):
        if "html" not in response.body:
            return
        html = json.loads(response.body)["html"]
        author_names = sel.get_author_names(html)
        author_urls = sel.get_author_urls(html)

        for i in range(0, self.per_page):
            # item一定要放循环中 不然数据库会出现大量重复数据
            item = authorItem()
            item["author_name"] = author_names[i]
            item["author_url"] = author_urls[i]
            yield item


class typeSpider(scrapy.Spider):
    name = "type"
    allowed_domains = ["behance.net"]
    headers = {
        "X-Requested-With": "XMLHttpRequest"
    }

    def start_requests(self):
        url = "https://www.behance.net/search"
        yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        if "html" not in response.body:
            return
        html = json.loads(response.body)["html"]
        type_names = sel.get_type_names(html)
        print type_names


class zcoolSpider(scrapy.Spider):
    name = 'zcool'
    allowed_domains = ["zcool.com.cn"]
    headers = {
        "Content-Type": "text/html"
    }

    def start_requests(self):
        for pages in range(1, 2):
            url = "http://www.zcool.com.cn/designer?recommend=-1&city=-1&professionId=11&sort=0&p=%s"
            yield scrapy.Request(url=url % pages, callback=self.parse, headers=self.headers)

    def parse(self, response):
        html = response._body
        zcool_urls = sel.get_zcool_urls(html)
        for zcool_url in zcool_urls:
            yield scrapy.Request(url=zcool_url, callback=self.person_parse, headers=self.headers)

    def person_parse(self, response):
        html = response._body
        zcool_author_info = sel.get_author_info(html)
        print zcool_author_info


class jobSpider(scrapy.Spider):
    name = "job"
    allowed_domains = ["lagou.com"]
    headers = {
        "X-Requested-With": "XMLHttpRequest",
    }

    def start_requests(self):
        job_url = 'http://www.lagou.com/jobs/positionAjax.json?'
        return [scrapy.http.FormRequest(job_url,
                                        formdata={'pn': str(1), 'kd': 'java'}, callback=self.parse)]
        # yield scrapy.http.FormRequest(url=job_url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        html = response.body
        print html
        jobs_url = sel.get_jobs_url(html)
        print jobs_url


class pictureSpider(scrapy.Spider):
    name = "picture"
    allowed_domains = ["behance.net"]
    headers = {
        "X-Requested-With": "XMLHttpRequest",
    }
    save_portfolio_ids = set()
    per_page = 48
    def start_requests(self):
        for tag in cs.BEHANCE_SEARCH_TAG:
            for ordinal in range(1, 10):
                _ordinal = self.per_page * ordinal
                url = "https://www.behance.net/search?ordinal=%s&content=projects&sort=appreciations&time=all&schema_tags=%s&user_tags=%s"
                yield scrapy.Request(url=url % (_ordinal, tag, tag), callback=self.parse, headers=self.headers)

    def parse(self, response):
        if "html" not in response.body:
            return
        html = json.loads(response.body)["html"]
        portfolio_urls = sel.get_urls(html)

        for idx in range(0, len(portfolio_urls)):
            portfolio_url = portfolio_urls[idx]
            portfolio_id = portfolio_url.split("/")[4]

            self.save_portfolio_ids.add(int(portfolio_id))
            yield scrapy.Request(url=portfolio_url, callback=self.picture_parse, headers=self.headers)
        pass

    def picture_parse(self, response):
        if "view" not in response.body:
            return
        data = json.loads(response.body)["view"]["project"]
        tags = data["tags"]
        module = data["modules"]
        for i in range(0, len(tags)):
            item = pictureItem()
            picture_url = module[i]["src"]
            if picture_url == '':
                continue
            item["picture_url"] = picture_url
            yield item