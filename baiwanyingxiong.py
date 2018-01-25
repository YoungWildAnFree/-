#coding:utf-8
from PIL import Image
import numpy as np
import urllib.request
from PIL import ImageFilter
import pytesseract
import webbrowser
import tiku_search

import random
from bs4 import BeautifulSoup

import os
import time


start = time.time()

#西瓜视频 截图选择的问题域和选项域
question_box = (50, 220, 1000, 500)
answer_box = (50, 550, 1020, 1080)
#芝士超人
# question_box = (30, 270, 1050,480)
# answer_box = (20, 500, 1050,1000)

#通过adb驱动 进行收集截屏 然后传入电脑d盘
os.system('adb shell screencap -p /sdcard/1.png')
os.system('adb pull /sdcard/1.png d:/')

#读取图片 截取问题域窗口
im = Image.open('d:/1.png')
question_im = im.crop(question_box)
#对图片增强显示 更容易识别汉子
question_im = question_im.filter(ImageFilter.EDGE_ENHANCE)
# question_im.show()

#识别问题字符串
question_str = pytesseract.image_to_string(question_im,lang='chi_sim')
question = question_str.split('.')[1].replace(' ','')

#将中文编码
key = urllib.parse.quote(question,encoding='gb2312')
#进行百度和百度知道搜索
url_search = "http://www.baidu.com/s?wd={}&cl=3".format(key)
url_zhidao = "https://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&ie=gbk&word={}".format(key)

#通过webbrowser自动打开网页
# webbrowser.open(url_zhidao,new=0)
webbrowser.open(url_search,new=0)

#对百度知道网站信息进行爬取
req1 = urllib.request.Request(url=url_zhidao)
response = urllib.request.urlopen(req1)
html = response.read()
# print(html)
soup = BeautifulSoup(html, 'lxml')

#找到问题 和答案描述
html_answer = soup.find_all('dd',class_='dd answer')
html_title =soup.find_all('a',class_='ti')

#提取各个问题到一个列表中
title_list=[]
for i in html_title:
    title_list.append(str(i).split('target="_blank">')[1].replace('<', '').replace('>', '').replace('em', '').replace('/', ''))

#先将百度搜索的页面打开然后对问题进行处理 这样可以先从浏览器中找答案
#开始对选项进行识别
answer_im = im.crop(answer_box)
# answer_im= answer_im.convert('L')
# answer_im.show()
answer_str = pytesseract.image_to_string(answer_im, lang='chi_sim').split('\n')[::2]

#将各个选项提取到列表中
answer_jiance = []
for i in range(len(answer_str)):
    answer_jiance.append(answer_str[i].split(' ')[0])

#对爬取的百度知道信息进行处理
answer_count = [0,0,0]
m=0
for i in range(len(answer_str)):
        answer_str[i] = answer_str[i].replace(' ', '').replace('-', '').replace('.', '')
# print(answer_count,answer_str)

#从控制台输出 百度知道信息：题目 答案 并对截图中的选项出现的次数进行统计 并且在控制台中用不同的颜色进行区分
for i in html_answer:
    print()
    search_answer=str(i).split('/i>')[1].replace(' ','').replace('-','').replace('.','').replace('·','')
    try:
        print('\033[4;33m' + '题目： '+ title_list[m]+ '\033[0m')
    except IndexError:
        m=1
    m+=1
    for tmp in [search_answer[m:m +60] for m in range(0, len(search_answer), 60)]:
        print()
        try:
            for n in range(len(tmp)):
                a= 0
                t=""
                if tmp[n] == answer_jiance[0]:
                    for a in range(len(answer_str[0])):
                        t += tmp[n+a]
                    print('\033[4;31m'+ t + '\033[0m',end='')
                elif tmp[n] == answer_jiance[1]:
                    for a in range(len(answer_str[1])):
                        t += tmp[n+a]
                    print('\033[4;35m' +t + '\033[0m',end='')
                elif tmp[n] == answer_jiance[2]:
                    for a in range(len(answer_str[2])):
                        t += tmp[n+a]
                    print('\033[4;34m' + t+ '\033[0m',end='')
                else:
                    print(tmp[n+a],end='')
        except IndexError:
            pass
        if( answer_str[0] in search_answer):
            answer_count[0]=answer_count[0]+1
        if ( answer_str[1] in search_answer):
            answer_count[1]=answer_count[1]+1
        if (answer_str[2] in search_answer):
            answer_count[2] = answer_count[2]+1

#输出最终问题
print(question)
#输出统计的选项出现的次数
for i in range(len(answer_count)):
    try:
        print('\033[1;30m' +"{"+answer_str[i]+":"+str(answer_count[i])+"}"+'\033[0m' ,end=" ")
    except IndexError:
        print('没有读取到答案')
#预测答案 做了个简单的判断 如果包含不或者是没 就输出次数少的那个 如果不包含 那就直接输出出现次数多的那个
#print(question)
print('预测的最终结果：')
if '不' in question or '没' in question:
    print('\033[1;30m' + answer_str[answer_count.index(np.array(answer_count).min())] + '\033[0m')
else:
    print('\033[1;30m' + answer_str[answer_count.index(np.array(answer_count).max())] + '\033[0m')

# tiku_search.tiku_search(question)
#对选项的搜索链接 打印出来
print('*'*30)
print("选项搜索链接")
for i in range(len(answer_str)):
    key = urllib.parse.quote(answer_str[i], encoding='gb2312')
    url = "http://www.baidu.com/s?wd={}&cl=3".format(key)
    print(str(answer_str[i]) +": "+ url)
# print()
end = time.time()
print(end-start)

#对图片保存
im.save('d:/backupimag/{}.png'.format(random.random()))


