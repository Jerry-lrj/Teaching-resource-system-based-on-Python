
# -*- coding: utf-8 -*-
"""
关闭弹窗
MOOC课程信息爬取

@author: Administrator
"""

import time, pymysql, re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as BS



def Chrome_web(url):
    # 谷歌浏览器爬取
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(50)
    driver.get(url)
    driver.maximize_window()  # 将浏览器最大化显示
    driver.implicitly_wait(5)  # 控制间隔时间，等待浏览器反应
    return driver


def PhantomJS_web(url):
    # 无头浏览器爬取
    driver = webdriver.PhantomJS(executable_path='D:\\电脑学习\\软件\\phantomjs-2.source.source-windows\\bin\\phantomjs.exe')
    driver.set_page_load_timeout(5)
    driver.get(url)
    time.sleep(5)


def crawl_web(subject):
    stop = 0
    url = 'http://www.icourse163.org/category/all'
    driver = Chrome_web(url)
    # driver=PhantomJS_web(url)   #等待时间过长
    if subject == '':
        subject = '全部'
    else:
        try:
            ele = driver.find_element_by_link_text(subject)
            ele.click()
        except:
            print('请输入正确的课程类别!')
            stop = 1
    kc_names, kc_schools, kc_teachers, kc_introductions, kc_stunums, kc_start_times, kc_links, kc_id_nums = [], [], [], [], [], [], [], []

    page_num, max_page_num = 1, 1
    while 1:
        if page_num > 100 or page_num > max_page_num:  # 设置爬取页数
            print('已爬取MOOC' + subject + '课程' + str(page_num - 1) + '页！')
            break
        if stop == 1:
            break
        htm_const = driver.page_source
        soup = BS(htm_const, 'xml')
        if page_num == 1:
            max_page_num = int(soup.find_all(name='a', attrs={'class': 'th-bk-main-gh'})[-2].string)
        c_names = soup.find_all(name='img', attrs={'height': '150px'})
        c_schools = soup.find_all(name='a', attrs={'class': 't21 f-fc9'})
        c_teachers = soup.find_all(name='a', attrs={'class': 'f-fc9'})
        c_introductions = soup.find_all(name='span', attrs={'class': 'p5 brief f-ib f-f0 f-cb'})
        c_stunums = soup.find_all(name='span', attrs={'class': 'hot'})
        c_start_times = soup.find_all(name='span', attrs={'class': 'txt'})
        c_links = soup.find_all(name='span', attrs={'class': ' u-course-name f-thide'})
        for i in range(len(c_names)):
            kc_names.append(c_names[i]['alt'])
            kc_schools.append(c_schools[i].string)
            kc_teachers.append(c_teachers[i].string)
            if c_introductions[i].string == None:
                c_introduction = ''
            else:
                c_introduction = c_introductions[i].string
            kc_introductions.append(c_introduction)
            c_stunum = re.compile('[0-9]+').findall(c_stunums[i].string)[0]
            kc_stunums.append(int(c_stunum))
            kc_start_times.append(c_start_times[i].string)
            kc_links.append('http:' + c_links[i].parent['href'])
            c_id_num = re.compile('[0-9]{4,}').findall(c_links[i].parent['href'])[0]
            kc_id_nums.append(int(c_id_num))
        try:
            next_page = WebDriverWait(driver, 10).until(
                # EC.visibility_of(driver.find_element_by_xpath(".//*[@id='searchHotelPanel']/div[6]/div[source]/div/ul/li[10]/a/span[source]"))
                EC.visibility_of(driver.find_element_by_link_text('下一页'))
            )
            next_page.click()
            time.sleep(5)
        except Exception as e:
            print(e)
            break
        page_num += 1

    driver.quit()
    kc_info = [kc_names, kc_schools, kc_teachers, kc_introductions, kc_stunums, kc_start_times, kc_links, kc_id_nums]
    return kc_info


def kc_print(kc_info):
    # 打印课程信息
    for i in range(len(kc_info[0])):
        print(kc_info[0][i])
        print('课程信息：' + kc_info[1][i] + ' ' + kc_info[2][i] + ' ' + str(kc_info[4][i]) + ' ' + kc_info[5][i])
        print('课程简介：' + kc_info[3][i])
        print('*****' * 20)


def save_mysql(subject, kc_info):
    db = pymysql.connect(host='localhost', user='root', passwd='', db='mooc_course', charset='utf8')
    cur = db.cursor()
    try:
        cur.execute("select * from %s" % subject)
        results = cur.fetchall()
        ori_len = len(results)
    except:
        # 建立新表
        sql = "create table %s" % subject + "(order_num int(4) not null,\
         course varchar(20),\
         school varchar(20),\
         teacher varchar(20),\
         start_time varchar(20),\
         stu_num int(6),\
         introduction varchar(255),\
         link varchar(255),\
         id int(11) not null,\
         commend int(11) not null,\
         collect int(11) not null,\
         primary key(id)\
         )"
        cur.execute(sql)
        db.commit()
        ori_len = 0
        print('已在mooc_course数据库中建立新表' + subject)
    for i in range(len(kc_info[0])):
        cur = db.cursor()
        sql = "insert into %s" % subject + "(order_num,course,school,teacher,introduction,stu_num,start_time,link,id, commend) VALUES ('%d','%s','%s','%s','%s','%d','%s','%s','%d', '%d')" % \
              (ori_len + i, kc_info[0][i], kc_info[1][i], kc_info[2][i], kc_info[3][i], kc_info[4][i], kc_info[5][i],
               kc_info[6][i], kc_info[7][i], 0)  # 执行数据库插入操作

        try:
            # 使用 cursor() 方法创建一个游标对象 cursor
            cur.execute(sql)
        except Exception as e:
            # 发生错误时回滚
            db.rollback()
            print('第' + str(i + 1) + '数据存入数据库失败！' + str(e))
        else:
            db.commit()  # 事务提交
            print('第' + str(i + 1) + '数据已存入数据库')
    db.close()


def mooc_crawl(subject, subject_Eng):
    kc_info = crawl_web(subject)
    if kc_info[0] != []:  # 错误类别不执行
        # kc_print(kc_info)
        save_mysql(subject_Eng, kc_info)


# 单独爬取某一类别
start_time = time.time()
subject = '计算机'
subjects = {'全部': 'all_sub', '计算机': 'computer', '经济管理': 'management', '心理学': 'psychology',
            '外语': 'language', '文学历史': 'literary_history', '艺术设计': 'art', '工学': 'engineering',
            '理学': 'science', '生命科学': 'biomedicine', '哲学': 'philosophy', '法学': 'law',
            '教育教学': 'teaching_method', '大学先修课': 'advanced_placement', '职业教育课程': 'TAFE'}
kc_info = crawl_web(subject)
if kc_info[0] != []:  # 错误类别不执行
    if subject == '':
        subject_Eng = 'all_sub'
    else:
        subject_Eng = subjects[subject]
        save_mysql(subject_Eng, kc_info)
        # kc_print(kc_info)
end_time = time.time()
print('执行程序一共花了：' + str(end_time - start_time))