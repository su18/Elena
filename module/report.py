#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Author : Su18
# @Copyright : <phoebebuffayfan9527@gmail.com>
# @For U : Like knows like.

import os
import html
from module.logger import logger
from config.settings import report_file_name


class ReportGenerate(object):

    def __init__(self):
        # 创建html模板文件
        self.header = """
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Google Hacking结果报告</title>
    <style>
    ::selection{
      background: black;
      color: white;
    }

        html,body,ul,p,a{
            padding: 0;
            margin: 0;
            list-style: none;
            text-decoration: none;
        }
        .wrapper{
            width: 980px;
            margin: 0 auto;
        }
        .wrapper h1{
            height: 100px;
            line-height: 100px;
            font-size: 32px;
            color: #22BD7A;
        }
        .main{
        }
        .box{
            margin-bottom:15px;
            position: relative;
            color:#3D4047;
            overflow: hidden;
        }
        .list-li{
            border-radius: 15px;
            border-bottom-left-radius: 0;
            border-bottom-right-radius: 0;
            background-color: #e0f9f0;
            padding: 0 20px;
            height: 75px;
            line-height: 75px;
            text-align: center;
            cursor: pointer;
            font-family: 'Microsoft YaHei';
            font-size: 20px;
        }
        .content{
            background-color: rgb(189,242,224);
            padding:10px 40px;
            line-height: 25px;
            display: none;
            color: #333;
            border-bottom-left-radius: 15px;
            border-bottom-right-radius: 15px;
            box-shadow:0 0 5px 4px rgba(83,221,173,0.3) inset;
        }

    </style>
</head>
<body>
    <div class="wrapper">
        <h1>Google Hacking结果报告</h1>
        <div class="main">
        """
        self.footer = """        </div>
    </div>
    <script src="http://libs.baidu.com/jquery/2.0.0/jquery.min.js"></script>
    <script>
        $(document).ready(function () {
          $('.list-li').on('click',function () {
            $(this).next().slideToggle();
          })
        })
    </script>
</body>
</html>"""
        self.juicy_result_template = """
                    <div class="box">
                <p class="list-li">%s</p>
                <p class="content">%s</p>
            </div>
        """
        self.juicy_result = ""

    def generate(self, title, url, markup):
        # 将查询结果写入html中，使用escape防止被html源码被标签解析
        self.juicy_result += self.juicy_result_template % ("标题：" + title + " " + "地址：" + url, html.escape(markup))

    def report(self):
        report_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../report/%s") % report_file_name)
        if not os.path.exists(report_file_name):
            try:
                os.makedirs(os.path.dirname(report_file))
            except Exception as reason:
                logger.error(reason)
        try:
            with open(report_file, 'w', encoding='utf-8') as report:
                all_result = self.header + self.juicy_result + self.footer
                report.write(all_result)
            logger.info("报告生成完毕")
        except Exception as reason:
            logger.info("报告生成失败")
            logger.error(reason)

