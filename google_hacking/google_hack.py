#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Author : Su18
# @Copyright : <phoebebuffayfan9527@gmail.com>
# @For U : Like knows like.

import sys
import json
import time
from google_hacking.google_search import GoogleSearch
from config.settings import target_site, file_name, file_encode, time_sleep, proxy_List
from module.logger import logger
from module.report import ReportGenerate


class GoogleHack(object):
    def __init__(self):
        self.search_list = []
        self.basic_site = "site:"+target_site+" "
        self.search_result = []

    def read_json(self):
        # 加载字典文件,在前面加上site组成完成查询语句
        logger.info("正在读取 GHDB Json 文件")
        try:
            with open(file_name, "r", encoding=file_encode) as json_file:
                content = json.load(json_file)
                # 先不进行子域名查询和C段查询
                # del content['basic_information']
                # 生成查询队列列表
                for primary_category, sub_category in content.items():
                    for j in sub_category:
                        for i in range(len(j['query'])):
                            search_query = self.basic_site+(j['query'][i])
                            self.search_list.append(search_query)
        except Exception as reason:
            logger.error(reason)
            sys.exit()
        logger.info("文件读取已完成")

    def query_search(self):
        logger.info("开始执行Google查询，查询时间可能较长，建议耐心等待")
        try:
            # 从查询列表里循环查询语句，查询并拿出结果
            for i in self.search_list:
                logger.info("正在查询语句：%s" % i)
                final_result = GoogleSearch().search(i, proxy_list=proxy_List)
                # 两次查询的时间间隔
                time.sleep(time_sleep)
                if final_result.results:
                    self.search_result.append(final_result.results)
                    # 将搜索出的结果记录到日志中
                    for j in range(len(final_result.results)):
                        logger.info("查询结果已经记录：{} {}".format(final_result.results[j].title,
                                                            final_result.results[j].url))

        except KeyboardInterrupt as reason:
            logger.exception(reason)
        logger.info("查询过程已结束")

    def generate_report(self):
        logger.info("开始生成 HTML 报告")
        # 实例化生成报告类
        result_report = ReportGenerate()
        for i in range(len(self.search_result)):
            for j in self.search_result[i]:
                result_title = j.title
                result_url = j.url
                # 返回抓取的页面内容，否则返回提示字符
                result_content = str(j._SearchResult__markup, encoding='utf-8') if j._SearchResult__markup \
                    else "页面内容为空，可能已经删除或被移动至其他位置"
                result_report.generate(result_title, result_url, result_content)
        # 生成报告
        result_report.report()



