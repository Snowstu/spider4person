#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 公共包：爬虫所需

from scrapy.selector import Selector


def get_urls(html):
    sel = Selector(text=html)
    # 作品集URL
    portfolio_urls = sel.xpath(
        "/html/body/div[@class='rf-project-cover rf-project-cover--project js-item js-project-cover qa-project-cover editable ']/a[@class='rf-project-cover__image-container js-project-cover-image-link js-project-link']/@href").extract()
    return portfolio_urls

def format_behance_url(url):
    if url is None:
        return None
    else:
        return ''.join(url.split('\\'))

def get_author_urls(html):
    sel = Selector(text=html)
    # 作者主页URL
    author_urls = sel.xpath(
        "/html/body/div/a/@href").extract()
    return author_urls

def get_author_names(html):
    sel = Selector(text=html)
    # 作者主页URL
    author_names = sel.xpath(
        "/html/body/div/div/a[@class='rf-profile-row__name js-profile-row__name']/text()").extract()
    return author_names

def get_type_names(html):
    sel = Selector(text=html)
    # 作者主页URL
    type_names = sel.xpath(
        "/html/body/div").extract()
    return type_names

def get_zcool_urls(html):
    sel = Selector(text=html)
    # 站酷URL
    zcool_urls = sel.xpath(
        "/html/body/div/main//div[@class='avatar-container-80']/a/@href").extract()
    return zcool_urls

def get_author_info(html):
    sel = Selector(text=html)
    # 作者信息
    zcool_author_info = sel.xpath(
        "//*[@id='body']/main/div[6]/div/div[1]/div[2]/table/tbody/tr").extract()
    return zcool_author_info

def get_jobs_url(html):
    sel = Selector(text=html)
    # 职位信息
    lagou_jobs_url = sel.xpath(
        "/html/body//div[@class='position']/div/a/@href").extract()
    return lagou_jobs_url