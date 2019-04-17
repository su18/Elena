#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Author : Su18
# @Copyright : <phoebebuffayfan9527@gmail.com>
# @For U : Like knows like.

import os
import sys
import logging
import logging.handlers
from config.settings import logfile_name


class Logger(logging.Logger):
    def __init__(self):
        logger_name = "elena"  # 模块名称
        level = logging.INFO  # 日志记录等级
        logger_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../logfile/%s" % logfile_name))  # 日志文件名

        # 创建日志文件
        logging.Logger.__init__(self, logger_file)
        if not os.path.exists(logger_file):
            os.makedirs(os.path.dirname(logger_file))

        # 设定日志输出格式
        log_format = logging.Formatter("[%(asctime)s] [" + logger_name
                                       + "] [%(levelname)s] %(filename)s [line:%(lineno)d] %(message)s")

        if not sys.stdout.isatty():
            # 判断执行输出流是否是终端，是终端直接显示日志
            try:
                console_handle = logging.StreamHandler()
                console_handle.setLevel(level)
                console_handle.setFormatter(log_format)
                self.addHandler(console_handle)
            except Exception as reason:
                self.error("%s" % reason)

        else:
            # 设置log文件
            try:
                file_handle = logging.FileHandler(logger_file)
                file_handle.setLevel(level)
                file_handle.setFormatter(log_format)
                self.addHandler(file_handle)
            except Exception as reason:
                self.error("%s" % reason)

        # 设置回滚日志,每个日志最大10M,最多备份1个日志
        try:
            handler = logging.handlers.RotatingFileHandler(
                filename=logger_file,
                maxBytes=10 * 1024 * 1024,
                backupCount=1,
                mode='a',
                encoding=None,
                delay=0
            )
            handler.setFormatter(log_format)
        except Exception as reason:
            self.error("%s" % reason)
        else:
            self.addHandler(handler)


logger = Logger()
