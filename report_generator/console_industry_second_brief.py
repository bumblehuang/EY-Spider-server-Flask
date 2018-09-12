#encoding: utf-8
import re
import mysql.connector
import oss2
import csv
import sys
import datetime
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
from console_visualizer import go_thierry
import os
db_host = os.environ['db_host']
db_password = os.environ['db_password']
oss_host = os.environ['oss_host']
oss_password = os.environ['oss_password']
auth = oss2.Auth(oss_host, oss_password)
bucket = oss2.Bucket(auth, 'oss-cn-shanghai.aliyuncs.com', 'cti-pub-files')


def Industry(table):
    db = mysql.connector.connect(user='root',
                                 password=db_password,
                                 host=db_host,
                                 port='3306',
                                 database='0_news')

    # set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()

    with open('finance.txt') as f1:
        finance = f1.readlines()
    with open('science.txt') as f2:
        science = f2.readlines()
    with open('retail.txt') as f3:
        retail = f3.readlines()



    sql = '''select news_content,news_hash,news_sector from %s where news_sector = '';''' % table
    cursor.execute(sql)
    dates = cursor.fetchall()
    for date in dates:
        finance_count = 0
        science_count = 0
        retail_count = 0
        for fin in finance:
            fin = re.sub('[\r\n]+','',fin)
            if re.findall(fin,date[0]) != []:
                finance_count += 1
        for sci in science:
            sci = re.sub('[\r\n]+','',sci)
            if re.findall(sci,date[0]) != []:
                science_count += 1
        for ret in retail:
            ret = re.sub('[\r\n]+','',ret)
            if re.findall(ret,date[0]) != []:
                retail_count += 1
        print(finance_count,science_count,retail_count)
        max = retail_count
        industry_name = 'retail'
        if max < finance_count:
            max = finance_count
            industry_name = 'finance'
        if max < science_count:
            industry_name = 'science'
        sql2 = '''update %s set news_sector = '%s' where news_hash = '%s';''' % (table,industry_name,date[1])
        cursor.execute(sql2)
    try:
        db.commit()
    except:
        # if unexecuted, rollback
        db.rollback()


def Industr_compliance(table):
    db = mysql.connector.connect(user='root',
                                 password=db_password,
                                 host=db_host,
                                 port='3306',
                                 database='0_compliance')

    # set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()

    with open('finance.txt') as f1:
        finance = f1.readlines()
    with open('science.txt') as f2:
        science = f2.readlines()
    with open('retail.txt') as f3:
        retail = f3.readlines()



    sql = '''select compliance_content,compliance_hash from %s where compliance_industry = '';''' % table
    cursor.execute(sql)
    dates = cursor.fetchall()
    for date in dates:
        finance_count = 0
        science_count = 0
        retail_count = 0
        for fin in finance:
            fin = re.sub('[\r\n]+','',fin)
            if re.findall(fin,date[0]) != []:
                finance_count += 1
        for sci in science:
            sci = re.sub('[\r\n]+','',sci)
            if re.findall(sci,date[0]) != []:
                science_count += 1
        for ret in retail:
            ret = re.sub('[\r\n]+','',ret)
            if re.findall(ret,date[0]) != []:
                retail_count += 1
        print(finance_count,science_count,retail_count)
        max = retail_count
        industry_name = 'retail'
        if max < finance_count:
            max = finance_count
            industry_name = 'finance'
        if max < science_count:
            industry_name = 'science'
        sql2 = '''update %s set compliance_industry = '%s' where compliance_hash = '%s';''' % (table,industry_name,date[1])
        cursor.execute(sql2)
    try:
        db.commit()
    except:
        # if unexecuted, rollback
        db.rollback()


def getnews(category):

    db = mysql.connector.connect(user='root',
                                 password=db_password,
                                 host=db_host,
                                 port='3306',
                                 database='0_news'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()
    sql = '''select news_title,news_publishedTime,news_author,news_content,news_link,news_sector from infosecinstitute_hash WHERE news_publishedTime >= (NOW() - INTERVAL 7 DAY)  and news_sector = '%s'
    union ALL
    select news_title,news_publishedTime,news_author,news_content,news_link,news_sector from freebuf_hash1 WHERE news_publishedTime >= (NOW() - INTERVAL 7 DAY)  and news_sector = '%s'
    union ALL
    select news_title,news_publishedTime,news_author,news_content,news_link,news_sector from cisco_hash WHERE news_publishedTime >= (NOW() - INTERVAL 7 DAY)  and news_sector = '%s' ORDER BY news_publishedTime DESC limit 5;''' % (category,category,category)



    cursor.execute(sql)
    datas = cursor.fetchall()
    data_list = []
    for data in datas:
        dic = {}
        dic['title'] = data[0]
        dic['time'] = data[1]
        dic['author'] = data[2]
        dic['content'] = data[3]
        dic['link'] = data[4]
        data_list.append(dic)

    try:
        db.commit()
    except:
        # if unexecuted, rollback
        db.rollback()
    return data_list

def get_compliance(category):

    db = mysql.connector.connect(user='root',
                                 password=db_password,
                                 host=db_host,
                                 port='3306',
                                 database='0_compliance'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()
    sql = '''select compliance_title,compliance_publishedTime,compliance_author,compliance_content,compliance_link,compliance_industry from cac_hash WHERE compliance_publishedTime >= (NOW() - INTERVAL 365 DAY)  and compliance_industry = '%s' limit 5;''' % category



    cursor.execute(sql)
    datas = cursor.fetchall()
    data_list = []
    for data in datas:
        dic = {}
        dic['title'] = data[0]
        dic['time'] = data[1]
        dic['author'] = data[2]
        dic['content'] = data[3]
        dic['link'] = data[4]
        data_list.append(dic)

    try:
        db.commit()
    except:
        # if unexecuted, rollback
        db.rollback()
    return data_list


def write_html(filename,report_id,request_id):
    Industr_compliance('cac_hash')
    Industry('cisco_hash')
    Industry('infosecinstitute_hash')
    Industry('freebuf_hash1')
    com_finance = get_compliance('finance')
    com_science = get_compliance('science')
    com_retail = get_compliance('retail')


    finance = getnews('finance')
    science = getnews('science')
    retail = getnews('retail')


    list1 = csv.reader(open('high_level_small.csv', 'r'))
    text1, text2 = go_thierry(report_id, request_id)

    with open(filename, 'w') as f:
        f.write('''﻿<style type="text/css">\n''')
        f.write('''_charset "UTF-8";\n''')
        f.write('''article.type-system-ey {\n''')
        f.write('''    text-align: righ;\n''')
        f.write('''    position: relative;\n''')
        f.write('''    background: #fff;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''html {\n''')
        f.write('''    font-family: sans-serif;\n''')
        f.write('''    -ms-text-size-adjust: 100%;\n''')
        f.write('''    -webkit-text-size-adjust: 100%;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''html {\n''')
        f.write('''    box-sizing: border-box;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''* {\n''')
        f.write('''    box-sizing: border-box;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''*,\n''')
        f.write('''*::after,\n''')
        f.write('''*::before {\n''')
        f.write('''    box-sizing: inherit;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''body {\n''')
        f.write('''    margin: 0;\n''')
        f.write('''    padding: 0;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''body {\n''')
        f.write('''    -webkit-font-feature-settings: "kern", "liga", "pnum";\n''')
        f.write('''    -ms-font-feature-settings: "kern", "liga", "pnum";\n''')
        f.write('''    font-feature-settings: "kern", "liga", "pnum";\n''')
        f.write('''    -webkit-font-smoothing: antialiased;\n''')
        f.write('''    -moz-osx-font-smoothing: grayscale;\n''')
        f.write('''    color: #333;\n''')
        f.write('''    font-family: "Helvetica Neue", "Helvetica", "Roboto", "Arial", sans-serif;\n''')
        f.write('''    font-size: 1em;\n''')
        f.write('''    line-height: 1.4;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''body {\n''')
        f.write('''    margin: 0;\n''')
        f.write('''    height: 100%;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''article,\n''')
        f.write('''aside,\n''')
        f.write('''details,\n''')
        f.write('''figcaption,\n''')
        f.write('''figure,\n''')
        f.write('''footer,\n''')
        f.write('''header,\n''')
        f.write('''hgroup,\n''')
        f.write('''main,\n''')
        f.write('''menu,\n''')
        f.write('''nav,\n''')
        f.write('''section,\n''')
        f.write('''summary {\n''')
        f.write('''    display: block;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''.article>section[class*=section]:nth-child(odd) {\n''')
        f.write('''    background-color: #f0f0f0;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''.article>section.section0 {\n''')
        f.write('''    padding-top: 60px;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''_media (min-width: 1200px) {\n''')
        f.write('''    .sl-landing>section,\n''')
        f.write('''    article>section,\n''')
        f.write('''    body>section {\n''')
        f.write('''        padding-left: 0;\n''')
        f.write('''        padding-right: 0;\n''')
        f.write('''    }\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''_media (min-width: 1200px) {\n''')
        f.write('''    .sl-landing>section,\n''')
        f.write('''    article>section,\n''')
        f.write('''    body>section {\n''')
        f.write('''        padding-left: 0;\n''')
        f.write('''        padding-right: 0;\n''')
        f.write('''    }\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''_media (min-width: 940px) {\n''')
        f.write('''    .sl-landing>section,\n''')
        f.write('''    article>section,\n''')
        f.write('''    body>section {\n''')
        f.write('''        padding: 40px;\n''')
        f.write('''    }\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''_media (min-width: 768px) {\n''')
        f.write('''    .sl-landing>section,\n''')
        f.write('''    article>section,\n''')
        f.write('''    body>section {\n''')
        f.write('''        padding: 40px 20px;\n''')
        f.write('''    }\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''.sl-landing>section,\n''')
        f.write('''article>section,\n''')
        f.write('''body>section {\n''')
        f.write('''    position: relative;\n''')
        f.write('''    -webkit-transition: all 0.4s;\n''')
        f.write('''    transition: all 0.4s;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''_media (min-width: 940px) {\n''')
        f.write('''    .container::after {\n''')
        f.write('''        clear: both;\n''')
        f.write('''        content: "";\n''')
        f.write('''        display: block;\n''')
        f.write('''    }\n''')
        f.write('''    .sl-landing .container {\n''')
        f.write('''        max-width: 68em;\n''')
        f.write('''    }\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''.container::after {\n''')
        f.write('''    clear: both;\n''')
        f.write('''    content: "";\n''')
        f.write('''    display: block;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''.maincolumn:last-child {\n''')
        f.write('''    margin-right: 0;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''_media (min-width: 768px) {\n''')
        f.write('''    .maincolumn {\n''')
        f.write('''        padding: 0;\n''')
        f.write('''        float: left;\n''')
        f.write('''        display: block;\n''')
        f.write('''        margin-right: 2.3576515979%;\n''')
        f.write('''        width: 100%;\n''')
        f.write('''        margin-right: 0;\n''')
        f.write('''    }\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''_media only screen and (min-width: 737px) {\n''')
        f.write('''    .type-system-ey .maincolumn h2,\n''')
        f.write('''    .type-system-ey section h2 {\n''')
        f.write('''        margin: 1em 0;\n''')
        f.write('''    }\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''.type-system-ey .maincolumn h2,\n''')
        f.write('''.type-system-ey section h2 {\n''')
        f.write('''    font-size: 2.4em;\n''')
        f.write('''    margin: 0 0 0.5em;\n''')
        f.write('''    font-weight: normal;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''_media screen and (min-width: 40em) {\n''')
        f.write('''    .maincolumn h2,\n''')
        f.write('''    section h2 {\n''')
        f.write('''        width: 80%;\n''')
        f.write('''        letter-spacing: -0.03em;\n''')
        f.write('''        line-height: 1.1;\n''')
        f.write('''        padding: 0;\n''')
        f.write('''        margin: 1em 0;\n''')
        f.write('''    }\n''')
        f.write('''    .type-system-ey .maincolumn h2,\n''')
        f.write('''    .type-system-ey section h2 {\n''')
        f.write('''        font-size: 2.4em;\n''')
        f.write('''        margin: 0 0 0.5em;\n''')
        f.write('''        font-weight: normal;\n''')
        f.write('''    }\n''')
        f.write('''    .sl-landing .maincolumn h2,\n''')
        f.write('''    .sl-landing section h2 {\n''')
        f.write('''        font-size: 2.8em;\n''')
        f.write('''        padding-top: 40px;\n''')
        f.write('''        margin-top: 0;\n''')
        f.write('''    }\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''.maincolumn h2,\n''')
        f.write('''section h2 {\n''')
        f.write('''    font-family: "Interstate-bold", sans-serif;\n''')
        f.write('''    font-size: 1.6em;\n''')
        f.write('''    font-weight: 400;\n''')
        f.write('''    line-height: 1.1em;\n''')
        f.write('''    margin-bottom: 0.5em;\n''')
        f.write('''    letter-spacing: -.03em;\n''')
        f.write('''    color: #646464;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''h1,\n''')
        f.write('''h2,\n''')
        f.write('''h3,\n''')
        f.write('''p {\n''')
        f.write('''    margin: 0;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''h1,\n''')
        f.write('''h2,\n''')
        f.write('''h3,\n''')
        f.write('''h4,\n''')
        f.write('''h5,\n''')
        f.write('''h6 {\n''')
        f.write('''    font-family: "Helvetica Neue", "Helvetica", "Roboto", "Arial", sans-serif;\n''')
        f.write('''    line-height: 1.2;\n''')
        f.write('''    margin: 0 0 0.7em;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''p {\n''')
        f.write('''    -webkit-font-feature-settings: "onum" 1, "pnum" 1;\n''')
        f.write('''    font-feature-settings: "onum" 1, "pnum" 1;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''p {\n''')
        f.write('''    font-family: "Helvetica", sans-serif;\n''')
        f.write('''    font-weight: 300;\n''')
        f.write('''    margin: 1em 0;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''p {\n''')
        f.write('''    color: #333;\n''')
        f.write('''    line-height: 1.4;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''p {\n''')
        f.write('''    margin: 0 0 0.7em;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''h3 {\n''')
        f.write('''    font-family: "Interstate-bold", sans-serif;\n''')
        f.write('''    font-size: 1.3em;\n''')
        f.write('''    color: #646464;\n''')
        f.write('''    font-weight: 700;\n''')
        f.write('''    line-height: 1.4em;\n''')
        f.write('''    margin-top: 0.5em;\n''')
        f.write('''    margin-bottom: 0.5em;\n''')
        f.write('''    letter-spacing: -.02em;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''table.dataframe {\n''')
        f.write('''    font-size: 1em;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''table {\n''')
        f.write('''    -webkit-font-feature-settings: "kern", "liga", "tnum";\n''')
        f.write('''    -ms-font-feature-settings: "kern", "liga", "tnum";\n''')
        f.write('''    font-feature-settings: "kern", "liga", "tnum";\n''')
        f.write('''    border-collapse: collapse;\n''')
        f.write('''    margin: 0.7em 0;\n''')
        f.write('''    table-layout: fixed;\n''')
        f.write('''    width: 100%;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''table {\n''')
        f.write('''    border-collapse: collapse;\n''')
        f.write('''    border-spacing: 0;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''tr,\n''')
        f.write('''td,\n''')
        f.write('''th {\n''')
        f.write('''    vertical-align: middle;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''.dataframe th {\n''')
        f.write('''    background: #fff000;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''#thc1 {\n''')
        f.write('''    width: 18%;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''#thc2 {\n''')
        f.write('''    width: 20%;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''#thc3 {\n''')
        f.write('''    width: 12%;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''#thc4 {\n''')
        f.write('''    width: 50%;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''td,\n''')
        f.write('''th {\n''')
        f.write('''    padding: 0;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''th {\n''')
        f.write('''    border-bottom: 1px solid #a6a6a6;\n''')
        f.write('''    font-weight: 600;\n''')
        f.write('''    padding: 0.7em 0;\n''')
        f.write('''    text-align: left;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''td {\n''')
        f.write('''    border-bottom: 1px solid #ccc;\n''')
        f.write('''    padding: 0.7em 0;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''a {\n''')
        f.write('''    color: #369;\n''')
        f.write('''    text-decoration: none;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''article a {\n''')
        f.write('''    font-weight: bold;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''a {\n''')
        f.write('''    color: #369;\n''')
        f.write('''    text-decoration: none;\n''')
        f.write('''    -webkit-transition: color 0.1s linear;\n''')
        f.write('''    transition: color 0.1s linear;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''a {\n''')
        f.write('''    background-color: transparent;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''.container {\n''')
        f.write('''    max-width: 52em;\n''')
        f.write('''    margin-left: auto;\n''')
        f.write('''    margin-right: auto;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''a {\n''')
        f.write('''    color: #369;\n''')
        f.write('''    text-decoration: none;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''article a {\n''')
        f.write('''    font-weight: bold;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''a.logo {\n''')
        f.write('''    height: 70px;\n''')
        f.write('''    width: 145px;\n''')
        f.write('''    margin: 10px 0;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''a.logo {\n''')
        f.write('''    float: right;\n''')
        f.write('''    width: 145px;\n''')
        f.write('''    height: 66px;\n''')
        f.write('''    margin: -20px -61px -100px;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''a.logo img {\n''')
        f.write('''    height: 100%;\n''')
        f.write('''    max-height: 70px;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''h4 {\n''')
        f.write('''    font-size: 0.8em;\n''')
        f.write('''    color: #646464;\n''')
        f.write('''    font-weight: 700;\n''')
        f.write('''    line-height: 1.2em;\n''')
        f.write('''    margin-top: 0.5em;\n''')
        f.write('''    margin-bottom: 0.5em;\n''')
        f.write('''    letter-spacing: -.02em;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''.footer p {\n''')
        f.write('''    color: rgba(255, 255, 255, 0.6);\n''')
        f.write('''    font-size: 0.8em;\n''')
        f.write('''    line-height: 1.5em;\n''')
        f.write('''    margin: 1em auto;\n''')
        f.write('''    max-width: 52em;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''.footer {\n''')
        f.write('''    padding: 10px;\n''')
        f.write('''    background: #333;\n''')
        f.write('''    width: 100%;\n''')
        f.write('''}\n''')
        f.write('''\n''')
        f.write('''.topdetails {\n''')
        f.write('''    font-size: 0.8em;\n''')
        f.write('''    color: #646464;\n''')
        f.write('''    text-align: center;\n''')
        f.write('''}\n''')
        f.write('''</style>\n''')
        f.write('''<article class="article type-system-ey ">\n''')
        f.write(
            '''    <p class="topdetails">若该邮件无法正常显示，请<a href="https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/%s/industry.html" target="_blank">点击此处查看详情</a></p>\n'''%report_id)
        f.write(
            '''    <section class="section0" id="section0" data-section-title="漏洞级别概况及目录" style="background-color:#F0F0F0">\n''')
        f.write('''        <div class="container">\n''')
        f.write('''            <div class="eyscrollogo"><a href="#" class="logo">\n''')
        f.write('''</a></div>\n''')
        f.write('''            <div class="maincolumn">\n''')
        f.write('''                <h2>云雀网络安全行业威胁情报(第6周)</h2>\n''')
        f.write(
            '''                                    <section class="section3" id="section3" data-section-title="金融事件" style="background-color:#F0F0F0">\n''')
        f.write('''                        <div class="container">\n''')
        f.write('''                            <div class="maincolumn">\n''')
        f.write('''\n''')
        f.write('''                            	            <h3>一、数据风险事件</h3>\n''')
        f.write('''<p>截至2018年8月6日对各大相关事件站点的扫描情况，我们列出金融、科技和零售三个行业的最新资讯，内容如下：</p>\n''')
        f.write('''                                <h4>金融行业数据风险事件</h4> \n''')
        f.write('''                            </div>\n''')
        f.write('''                        </div>\n''')


        for index, fin in enumerate(finance):
            f.write('''<p><a href="%s" target="_blank">%d.%s</a></p>''' % (fin['link'],index + 1, fin['title']))
            f.write('''<p>时间：%s</p>''' % fin['time'])
            f.write('''<p>作者：%s</p>''' % fin['author'])
            f.write('''<p>事件概要：%s</p>''' % fin['content'][:200])


        f.write(
            '''                        <section class="section4" id="section4" data-section-title="科技事件" style="background-color:#F0F0F0">\n''')
        f.write('''                            <div class="container">\n''')
        f.write('''                                <div class="maincolumn">\n''')
        f.write('''                                    <h4>科技行业数据风险事件</h4> </div>\n''')
        f.write('''                            </div>\n''')

        for index, sci in enumerate(science):
            f.write('''<p><a href="%s" target="_blank">%d.%s</a></p>''' % (sci['link'],index + 1, sci['title']))
            f.write('''<p>时间：%s</p>''' % sci['time'])
            f.write('''<p>作者：%s</p>''' % sci['author'])
            f.write('''<p>事件概要：%s</p>''' % sci['content'][:200])


        f.write(
            '''                            <section class="section5" id="section5" data-section-title="零售事件" style="background-color:#F0F0F0">\n''')
        f.write('''                                <div class="container">\n''')
        f.write('''                                    <div class="maincolumn">\n''')
        f.write('''                                        <h4>新零售行业数据风险事件</h4> </div>\n''')
        f.write('''                                </div>\n''')

        for index, ret in enumerate(retail):
            f.write('''<p><a href="%s" target="_blank">%d.%s</a></p>''' % (ret['link'],index + 1, ret['title']))
            f.write('''<p>时间：%s</p>''' % ret['time'])
            f.write('''<p>作者：%s</p>''' % ret['author'])
            f.write('''<p>事件概要：%s</p>''' % ret['content'][:200])


        f.write('''                            </section>\n''')
        f.write('''                        </section>\n''')
        f.write('''                    </section>\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write(
            '''        <section class="section2" id="section2" data-section-title="漏洞类别" style="background-color:#F0F0F0">\n''')
        f.write('''            <div class="container">\n''')
        f.write('''                <div class="maincolumn">\n''')
        f.write(
            '''                    <section class="section3" id="section3" data-section-title="金融事件" style="background-color:#F0F0F0">\n''')
        f.write('''                        <div class="container">\n''')
        f.write('''                            <div class="maincolumn">\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''                            	            <h3>二、合规新闻</h3>\n''')
        f.write('''<p>截至2018年8月6日对相关合规站点的扫描情况，我们列出金融、科技和零售三个行业的最新资讯，内容如下：</p>\n''')
        f.write('''                                <h4>金融行业合规新闻</h4> \n''')
        f.write('''                            </div>\n''')
        f.write('''                        </div>\n''')

        for index, fin in enumerate(com_finance):
            f.write('''<p><a href="%s" target="_blank">%d.%s</a></p>''' % (fin['link'],index + 1, fin['title']))
            f.write('''<p>时间：%s</p>''' % fin['time'])
            f.write('''<p>作者：%s</p>''' % fin['author'])
            f.write('''<p>事件概要：%s</p>''' % fin['content'][:200])


        f.write(
            '''                        <section class="section4" id="section4" data-section-title="科技事件" style="background-color:#F0F0F0">\n''')
        f.write('''                            <div class="container">\n''')
        f.write('''                                <div class="maincolumn">\n''')
        f.write('''                                    <h4>科技行业合规新闻</h4> </div>\n''')
        f.write('''                            </div>\n''')
        for index, sci in enumerate(com_science):
            f.write('''<p><a href="%s" target="_blank">%d.%s</a></p>''' % (sci['link'],index + 1, sci['title']))
            f.write('''<p>时间：%s</p>''' % sci['time'])
            f.write('''<p>作者：%s</p>''' % sci['author'])
            f.write('''<p>事件概要：%s</p>''' % sci['content'][:200])

        f.write(
            '''                            <section class="section5" id="section5" data-section-title="零售事件" style="background-color:#F0F0F0">\n''')
        f.write('''                                <div class="container">\n''')
        f.write('''                                    <div class="maincolumn">\n''')
        f.write('''                                        <h4>新零售行业合规新闻</h4> </div>\n''')
        f.write('''                                </div>\n''')


        for index, ret in enumerate(com_retail):
            f.write('''<p><a href="%s" target="_blank">%d.%s</a></p>''' % (ret['link'],index + 1, ret['title']))
            f.write('''<p>时间：%s</p>''' % ret['time'])
            f.write('''<p>作者：%s</p>''' % ret['author'])
            f.write('''<p>事件概要：%s</p>''' % ret['content'][:200])




        f.write('''                            </section>\n''')
        f.write('''                        </section>\n''')
        f.write('''                    </section>\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')

        f.write('''                    <h3>三、本周安全漏洞级别概况</h3>\n''')
        f.write('''<p>%s,以下为最新发布的十条高风险漏洞:</p>\n''' % text1)
        f.write('''                    <p>\n''')
        f.write('''                        <!--*<h3>High risk vulnerability</h3>-->\n''')
        i = 0
        for stu_cell in list1:
            # print(stu_cell)
            if i != 0:
                print(i)
                print(stu_cell[1])
                f.write('''<tr>''')
                f.write('''<td>%s</td>\n''' % stu_cell[1])
                f.write('''<td>%s</td>\n''' % stu_cell[2])
                f.write('''<td>%s</td>\n''' % stu_cell[3])
                f.write('''<td>%s</td>\n''' % stu_cell[4])
                f.write('''</tr>''')
                i += 1
            else:
                f.write('<table border="1" class="dataframe">\n')
                f.write('<thead>\n')
                f.write('<tr style="text-align: right;">\n')

                f.write('<th id=thc1>%s</th>\n' % stu_cell[1])
                f.write('<th id=thc2>%s</th>\n' % stu_cell[2])
                f.write('<th id=thc3>%s</th>\n' % stu_cell[3])
                f.write('<th id=thc4>%s</th>\n' % stu_cell[4])
                f.write('</tr>\n')
                f.write('</thead>\n')
                f.write('<tbody>\n')

                i += 1

        f.write('''</tbody>\n''')
        f.write('''</table>\n''')

        f.write('''                    </p>\n''')
        f.write('''                </div>\n''')
        f.write('''            </div>\n''')
        # f.write('''        </section>\n''')
        f.write(
            '''        <section class="section2" id="section2" data-section-title="漏洞类别" style="background-color:#F0F0F0">\n''')
        f.write('''            <div class="container">\n''')
        f.write('''                <div class="maincolumn">\n''')
        f.write('''                    <h3>四、漏洞类别</h3>\n''')
        # f.write('''                    <p>本次所扫描到的漏洞可根据风险类别分为以下主要10类, 高危漏洞类别按数量正序分布如下： Not Defined: 47个 XSS: 19个 Overflow: 14个 Exec Code: 10个 DoS: 8个 CSRF: 7个 Exec Code XSS: 6个 DoS Overflow: 6个 +Info: 6个 Bypass: 4个</p>''')
        f.write('''<p>%s</p>\n''' % text2)

        f.write('''       \n''')
        f.write('''                </div>\n''')
        f.write('''                <div class="container">\n''')
        f.write('''                    <div class="maincolumn">\n''')
        f.write(
            '''                        <h4>更多详细内容请<a href="https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/%s/industry.html" target="_blank">点击此处查看</a></h4></div>\n'''%report_id)
        f.write('''                </div>\n''')
        f.write('''            </div>\n''')
        f.write('''        </section>\n''')
        f.write('''    </section>\n''')
        f.write('''</article>\n''')
        f.write('''<footer class="footer" id="footer" role="contentinfo">\n''')
        f.write('''    <div class="footer-logo">\n''')
        f.write('''        <div class="footer-links"></div>\n''')
        f.write(
            '''        <p class="detail">声明：以上内容均来自互联网，由CTI网络威胁情报团队整理，其版权归属原作者所有，其观点并不代表我方观点和意见，请酌情参考或采用。若对以上所引用内容有任何疑问或问题，<a href="mailto:请与services@eycyber.com联系">请与services@eycyber.com联系</a>。</p>\n''')
        f.write('''    </div>\n''')
        f.write('''</footer>\n''')
        f.write('''</div>\n''')


    with open('industry_mail.html', 'rb') as fileobj:
        directory = report_id + '/industry_mail.html'
        result = bucket.put_object(directory,fileobj)

def main():
    write_html('industry_mail.html','report_id','request_id')


if __name__ == '__main__':
    main()

