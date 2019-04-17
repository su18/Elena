#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Su18
# @Copyright : <phoebebuffayfan9527@gmail.com>
# @For U : Like knows like.

import urllib.request
import math
import re
import random
import sys
from bs4 import BeautifulSoup
from threading import Thread
from collections import deque
from time import sleep
from module.logger import logger
from config.settings import search_num_results, search_language


class GoogleSearch(object):
    def __init__(self):
        # 查询URL
        self.SEARCH_URL = "https://google.com/search"
        # soup select 选择标签
        self.RESULT_SELECTOR = "div.r a"
        # soup select 选择CSS标签
        self.TOTAL_SELECTOR = "#resultStats"
        # 搜索返回每页的结果数
        self.RESULTS_PER_PAGE = 10
        # UA及接收语言设置
        self.USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                          "Chrome/ 58.0.3029.81 Safari/537.36"
        self.DEFAULT_HEADERS = [
            ('User-Agent', self.USER_AGENT),
            ("Accept-Language", "en-US,en;q=0.5"),
        ]

    def search(self, query, num_results=search_num_results,
               prefetch_pages=True, prefetch_threads=10, language=search_language,
               proxy_list=None):
        # 初始化搜索结果为空
        search_results = []
        # 计算返回结果的页数
        pages = int(math.ceil(num_results / self.RESULTS_PER_PAGE))
        # 双初始化端队列
        fetcher_threads = deque([])
        total = None

        for i in range(pages):
            start = i * self.RESULTS_PER_PAGE

            # 设置通过代理发包
            if proxy_list:
                proxy = random.choice(proxy_list)
                proxy_handler = urllib.request.ProxyHandler(proxy)
            else:
                proxy_handler = urllib.request.ProxyHandler({})
            try:
                opener = urllib.request.build_opener(proxy_handler)
                # 覆盖 addheaders 值
                opener.addheaders = self.DEFAULT_HEADERS

                # 使用 urllib.request 按页数获取 Google 查询返回的结果
                response = opener.open(self.SEARCH_URL + "?q=" + urllib.request.quote(query) + "&hl=" + language + (
                    "" if start == 0 else ("&start=" + str(start))))

                # 使用BeautifulSoup lxml 解析器处理返回结果
                soup = BeautifulSoup(response.read(), 'lxml')
                response.close()
            except Exception as reason:
                logger.error(reason)
                sys.exit()

            if total is None:
                # 处理总共返回结果的数量
                if soup.select(self.TOTAL_SELECTOR):

                    # 查询返回结果数目
                    total_text = soup.select(self.TOTAL_SELECTOR)[0].children.__next__().encode('utf-8')

                    # 使用正则匹配总共返回多少条结果
                    total = int(re.sub("[', ]", "",
                                       re.search("(([0-9]+[', ])*[0-9]+)",
                                                 total_text.decode('utf-8')).group(1)))
                else:
                    logger.info("查询结果为空")
                    total = 0

            # 从结果中选择 href 便签下的结果链接
            results = self.parse_results(soup.select(self.RESULT_SELECTOR))

            # 去除脏数据
            if len(results) > total:
                del results[total - len(results):]

            # 截取查询结果长度
            if len(search_results) + len(results) > num_results:
                del results[num_results - len(search_results):]

            # 将结果加入搜索结果列表中
            search_results += results

            # 采用多线程处理返回结果
            if prefetch_pages:
                for result in results:
                    while True:
                        running = 0
                        for thread in fetcher_threads:
                            if thread.is_alive():
                                running += 1
                        if running < prefetch_threads:
                            break
                        sleep(1)
                    fetcher_thread = Thread(target=result.get_text_)
                    fetcher_thread.start()
                    fetcher_threads.append(fetcher_thread)

        for thread in fetcher_threads:
            thread.join()
        return SearchResponse(search_results, total)

    @staticmethod
    def parse_results(results):
        search_results = []
        url = ''
        title = ''
        for result in results:
            try:
                url = result["href"]
                title = result.find('h3').text
            except Exception:
                pass
            finally:
                search_results.append(SearchResult(title, url))
        return search_results


class SearchResponse(object):
    def __init__(self, results, total):
        self.results = results
        self.total = total


class SearchResult(object):
    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                          "Chrome/ 58.0.3029.81 Safari/537.36"
        self.DEFAULT_HEADERS = [
            ('User-Agent', self.USER_AGENT),
            ("Accept-Language", "en-US,en;q=0.5"),
        ]
        self.__text = None
        self.__markup = None

    def get_text_(self):
        # 访问一次得到的URL，获取字符串
        if self.__text is None:
            try:
                soup = BeautifulSoup(self.get_markup(), "lxml")
                # 去除指定标签
                for junk in soup(["script", "style"]):
                    junk.extract()
                    self.__text = soup.get_text()
            except Exception:
                pass
        return self.__text

    def get_markup(self):
        # 访问一次查询到的网址获取
        if self.__markup is None:
            try:
                opener = urllib.request.build_opener()
                opener.addheaders = self.DEFAULT_HEADERS
                response = opener.open(self.url)
                self.__markup = response.read()
            except Exception:
                pass
        return self.__markup

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()
