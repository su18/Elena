#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Author : Su18
# @Copyright : <phoebebuffayfan9527@gmail.com>
# @For U : Like knows like.

from module.logger import logger
from google_hacking.google_hack import GoogleHack

logger.info("程序开始运行")
# 实例化
google_hack_process = GoogleHack()
# 读取Json文件
google_hack_process.read_json()
# 开始查询
google_hack_process.query_search()
# 生成报告
google_hack_process.generate_report()

logger.info("程序运行结束，报告请在项目下的report文件夹查看")
