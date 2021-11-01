#-*- coding = utf-8 -*-
#@Time:2021/11/1 14:42
#@Author:liyida
#@File:拉钩.py
#@Software:PyCharm
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import time
import os
web = Chrome()
web.get("https://www.lagou.com")
web.find_element_by_xpath('//*[@id="cboxClose"]').click()
time.sleep(1)
path = r'./job'
if os.path.exists(path):
    print("文件夹已存在")
else:
    os.mkdir(path)
    web.find_element_by_xpath('//*[@id="search_input"]').send_keys('python',Keys.ENTER)
    page_num = int(web.find_element_by_xpath('//*[@id="s_position_list"]/div[2]/div/span[5]').text)
    count = 1
    for i in range(page_num):
        job_list = web.find_elements_by_class_name('position_link')
        for job in job_list:
            element = job.find_element_by_tag_name('h3')
            web.execute_script("arguments[0].click()",element)
            web.switch_to.window(web.window_handles[-1])
            content = web.find_element_by_xpath('//*[@id="job_detail"]/dd[2]').text
            f = open(path+'/需求_%d.txt'%count,'w+',encoding='utf8')
            f.write(content)
            f.close()
            web.close()
            web.switch_to_window(web.window_handles[0])
            count += 1
            time.sleep(1)
        next_page = web.find_element_by_class_name('pager_next')
        web.execute_script("arguments[0].click()",next_page)
        time.sleep(1)


