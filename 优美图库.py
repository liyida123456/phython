#-*- coding = utf-8 -*-
#@Time:2021/10/31 19:43
#@Author:liyida
#@File:优美图库.py
#@Software:PyCharm
from bs4 import BeautifulSoup
import requests
import os
import re
def main():
    baseurl = 'https://www.umei.cc/meinvtupian/meinvxiezhen/'
    for i in range(1,3):
        if i == 1:
            url = baseurl+'index.htm'
        else:
            url = baseurl+'index_'+str(i)+'.htm'
        html = get_html(url)
        html.encoding = "utf8"
        soup = BeautifulSoup(html.text,'lxml')
        imagelist = soup.find('div',attrs={'class':'TypeList'}).find_all('a',attrs={'class':'TypeBigPics'})
        count = 1#记录套图数量
        for image in imagelist:
            os.mkdir(r'.\第%d个套图'%count)#创建文件夹
            link = 'https://www.umei.cc'+image.get('href')
            first_page = get_html(link)#获取第一页
            first_page.encoding = "utf8"
            page_content = BeautifulSoup(first_page.text,'html.parser')
            end_page = page_content.find('div',attrs={'class':'NewPages'}).find('a',string='尾页')#获取最后一页链接
            page_num = re.search(r'_(\d+)?.',end_page.get('href')).group(1)#获取页面数量
            baseurl = image.get('href').split('.')[0]
            for i in range(1,int(page_num)+1):#循环遍历套图
                if i == 1:
                    imageurl = 'https://www.umei.cc'+baseurl+'.htm'
                else:
                    imageurl = 'https://www.umei.cc'+baseurl+'_'+str(i)+'.htm'#获取套图的url
                page_content = BeautifulSoup(get_html(imageurl).text,'html.parser')
                src = page_content.find('div',attrs={'class':'ImageBody'}).find('img').get('src')#获取每张图片url
                f = open(r'.\%d\image_%d.jpg'%(count,i),mode='wb')#保存到相应文件夹
                f.write(get_html(src).content)#保存每张图片
                print("第%d个套图的第%d张图片下载好了"%(count,i))
            count += 1

def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/95.0.4638.54 Safari/537.36'
    }
    r = requests.get(url=url,headers=headers)
    return r

if __name__ == '__main__':
    main()
