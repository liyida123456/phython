#-*- coding = utf-8 -*-
#@Time:2021/10/26 21:30
#@Author:liyida
#@File:douban.py
#@Software:PyCharm

import requests
from bs4 import BeautifulSoup
import re
import xlwt
import time
import json
def main():
    baseurl = "https://movie.douban.com/top250?start="
    movielist = get_data(baseurl)
    savepath = "豆瓣电影top250.xls"
    print(json.dumps(movielist,indent=4,ensure_ascii=False))
    saveData(movielist,savepath)

def get_data(baseurl):
    movielist = []
    for i in range(0,1):
        url = baseurl+str(i*25)
        html = requestData(url)
        soup = BeautifulSoup(html,"html.parser")
        for movie in soup.find_all('div',class_='item'):
            movieData = []
            title = movie.find_all('span',attrs={'class':'title'})#电影标题
            if len(title) == 2:
                chinesename = title[0].string
                movieData.append(chinesename)
                englishname = title[1].string
                movieData.append(englishname.replace('/',''))
            elif len(title) == 1:
                movieData.append(title[0].string)
                movieData.append('无信息')

            link = movie.find('div',attrs={'class':'hd'}).a['href']#电影链接
            movieData.append(link)  if link != '' else movieData.append('无信息')

            act = movie.find('div',attrs={'class':'bd'}).p.text #导演、演员和电影信息
            if act != '':
                act = act.strip()
                dirctor = re.search(r'导演:(.*)主演',act)#导演
                actor = re.search(r'主演:(.*)',act)#演员
                if dirctor != None:
                    movieData.append(dirctor.group(1))
                else:
                    movieData.append('无信息')
                if actor != None:
                    movieData.append(actor.group(1))
                else:
                    movieData.append('无信息')

                info = re.search(r'(\d+.*)',act)#电影信息
                if info != None:
                    movieData.append(info.group(1))
                else:
                    movieData.append('无信息')
            else:
                for i in range(3):
                    movieData.append('无信息')

            rating = movie.find('span',attrs={'class':'rating_num'}).string#评分
            movieData.append(rating) if rating !='' else movieData.append('无信息')
            rating_num = re.findall(r'<span>(\d.*?人评价)',str(movie))#评分人数
            movieData.append(rating_num[0]) if rating_num != '' else movieData.append('无信息')

            intro = movie.find('span',class_='inq')#简介
            if intro != None:
                movieData.append(intro.string)
            else:
                movieData.append('无信息')
            movielist.append(movieData)
        time.sleep(1)
    return movielist

def saveData(movielist,savepath):
    workbook = xlwt.Workbook(encoding="utf8")
    sheet = workbook.add_sheet("豆瓣电影前250",cell_overwrite_ok=True)
    col = ['中文标题','英文标题','电影链接','导演','演员','电影信息','评分','评分人数','简介']
    for i in range(len(col)):
        sheet.write(0,i,col[i])
    for i in range(len(movielist)):
        for j in range(len(movielist[i])):
            sheet.write(i+1,j,movielist[i][j])
    workbook.save(savepath)

def requestData(url):
    head = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)  \
           AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
    }
    html = ""
    try:
        reponse = requests.get(url)
        html = reponse.content.decode("utf-8")
    except Exception as e:
        print(e.args)
    return  html


if __name__ == '__main__':
    main()
