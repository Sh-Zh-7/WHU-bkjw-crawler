# 武汉大学-本科教务-爬虫

![](https://img.shields.io/github/license/Sh-Zh-7/WHU-bkjw-crawler)![](https://img.shields.io/github/repo-size/Sh-Zh-7/WHU-bkjw-crawler)![](https://img.shields.io/badge/tensroflow-2.1.0-red)

一个用来爬取教务系统成绩单并能进行灵活处理的教务系统爬虫程序

## 特性：

- 跨平台：Windows 10, Ubuntu, MacOS均可使用
- 自动识别验证码，用户只需要输入用户名和密码就可以登录
- 爬取的成绩单持久化到本地，一次爬取多次查询，减轻教务系统服务器压力
- 支持按照课程名称查询课程，而且用户无需输入精确的名称即可查询
- 支持按照年份，种类（公必，公选，专必，专选）查询各种课程
- 支持获取课程平均分，GPA， 以学分为权的平均分，总学分等各种信息
- 支持HTML转CSV， 当程序的接口不能满足用户需要的时候，可以使用CSV软件（Excel, WPS表格等）进行进一步处理

## 下载：

首先获取整个项目：

`git clone git@github.com:Sh-Zh-7/WHU-bkjw-crawler.git`

再利用pip安装项目的依赖：

`pip install -r requirements.txt`

如果您是Windows 10的用户，由于目前最新的python解释器对tensorflow 2.0+的支持问题，您可能得使用3.5.x或者3.6.x版本的python解释器才能正常下载tensorflow 2.0+的依赖。

## 使用：

帮助文档：

```shell
usage: spider.py [-h][-A] [-Y Y][-C C] [-K {GB,GX,ZB,ZX,B,X}][-S | -G | -W | -T | --print] [--clear]

您的教务系统助手

optional arguments:
  -h, --help            show this help message and exit
  -A                    查询所有的课程
  -Y Y                  查询某一学年的课程
  -C C                  按照课程名称查找
  -K {GB,GX,ZB,ZX,B,X}  按照课程的种类查找
  -S                    查询课程的平均分
  -G                    查询GPA
  -W                    查询以学分为权的平均分
  -T                    查询总学分
  --print               打印所有课程信息
  --clear               删除所有本地存储
```

下面展示比较常用的几种命令：

- 查看帮助文档: `python spider.py –help`
- 查看某一个课程的信息（以高等数学为例）：`python spider.py -C 高等数学`
- 查看所有课程的GPA：`python spider.py -A -G`
- 查看必修课的加权平均分（以学分为权）：`python spider.py -K B -W`
- 查看专选课的总学分：`python spider.py -K ZX -T `

这个爬虫程序还支持更加强大的命令行参数组合功能，比如如果您想查询2018学年必修课的加权平均分：

```
python spider.py -Y 2018 -K B -W
```

## FAQ：

**Q1：为什么我输入了密码，但是却不显示？**

**A1：** 这是因为本程序使用Unix风格的命令行密码输入，看不到你的密码是为了保护你的隐私。虽然你在前台看不到，但是实际上是能接收到你的密码的。

<br/>

**Q2：出现了意料之外的错误怎么办？**

**A2：** 截图，到此[链接](https://github.com/Sh-Zh-7/WHU-bkjw-crawler/issues)提issue。另外，错误可能分为两种:

1. 第一种是登录时候的错误，这种错误可能是**网络连接或者验证码识别**的问题，**重新执行相同的命令**即可。
2. 第二种错误是查询结果的错误，**当你发现查询结果和自己的计算不一致，请立刻联系开发人员**。

<br/>

**Q3: 为什么不直接爬取csv文件？而要同时爬取html和csv？**

**A3:** 爬取html是因为bs4的html.parser引擎性能更好。爬取csv是为了给予用户更多选择。

## 鸣谢：

WHU 2018级本科 CS ， [谭瑞锋](https://github.com/w824449964)同学的验证码自动识别支持。

## LICENSE： 

[MIT License](https://github.com/Sh-Zh-7/WHU-bkjw-crawler/blob/master/LICENSE/)

Copyright (c) 2020 sh-zh-7
