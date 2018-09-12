#encoding: utf-8
import os
import re
import mysql.connector
import sys
import oss2
import requests
from console_visualizer import go_thierry
import csv
import datetime
#with open('ey_cti_cn_rpt2.html', 'r') as f1:
#        list1 = f1.readlines()
#with open('test.html', 'w') as f:
#    for i in list1:
#        i = re.sub(r'\n','',i)
#        f.write('''f.write(\'\'\'%s\'\'\')\n''' % i)
reload(sys)
sys.setdefaultencoding('utf-8')
import os
oss_host = os.environ['oss_host']
oss_password = os.environ['oss_password']
db_host = os.environ['db_host']
db_password = os.environ['db_password']
auth = oss2.Auth(oss_host, oss_password)
bucket = oss2.Bucket(auth, '', 'cti-pub-files')
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
    #sql = '''alter table trendmicro_hash1 add column news_industry varchar(255) not null;'''
    #cursor.execute(sql)
    ####增加行业
    finance = ['finance','bank','corporate', 'investment', 'group','Share', 'enterprise', 'price','Economic' ,'asset', 'financing']
    science = ['Huawei', 'xiaomi', 'samsung', 'technology' ,'traffic', 'unicom', 'telecom', 'jd', 'Internet', 'ios', 'tencent', 'alibaba']
    sql = '''select news_category, news_hash, news_industry from trendmicro_hash1 where news_industry = '';'''

    cursor.execute(sql)
    dates = cursor.fetchall()

    for row in dates:
        if re.findall(r'finance|bank|corporate|investment|group|Share|enterprise|price|Economic|asset|financing',row[0]) != []:
            industry = 'finance'
        elif re.findall(r'Huawei|xiaomi|samsung|technology|traffic|unicom|telecom|jd|Internet|ios|tencent|alibaba',row[0]) != []:
            industry = 'science'
        else:
            industry = 'retail'
        hashvalue = row[1]
        sql2 = '''update trendmicro_hash1 set news_industry = '%s' where news_hash = '%s';'''%(industry,hashvalue)
        cursor.execute(sql2)


    ####选数据
    sql3 = '''select news_title, news_publishedTime, news_author, news_briefContent ,news_link,news_industry from trendmicro_hash1 where news_industry = '%s'  ORDER BY news_publishedTime DESC limit 3;'''%(category)
    #select news_category ,news_hash, news_industry,news_publishedTime from trendmicro_hash where news_industry = 'finance'  ORDER BY news_publishedTime DESC limit 3

    cursor.execute(sql3)
    results = cursor.fetchall()
    title = []
    time = []
    author = []
    briefContent = []
    link = []
    for row in results:
        title.append(row[0])
        time.append(row[1])
        author.append(row[2])
        briefContent.append(row[3])
        link.append(row[4])

    dicts = {}
    dicts['title'] = title
    dicts['time'] = time
    dicts['author'] = author
    dicts['briefContent'] = briefContent
    dicts['link'] = link
    try:
        db.commit()
    except:
        # if unexecuted, rollback
        db.rollback()
    return dicts




def write_html(filename,report_id,request_id):


    text1,text2 = go_thierry(report_id,request_id)
    #response = requests.get('http://cti-pub-files.oss-cn-shanghai.aliyuncs.com/pages/patch.html')
    #html = response.text
    #list1 = re.findall(r'.*?\n', html)




    #with open("http://cti-pub-files.oss-cn-shanghai.aliyuncs.com/pages/high_level.html", 'r') as f2:
        #list2 = f2.readlines()

    #response2 = requests.get('http://cti-pub-files.oss-cn-shanghai.aliyuncs.com/pages/high_level.html')
    #html2 = response2.text
    #list2 = re.findall(r'.*?\n', html2)
    list1 = csv.reader(open('high_level_small.csv', 'r'))
    finance = getnews('finance')
    #print(finance)
    science = getnews('science')
    #print(science)
    retail = getnews('retail')

    #response3 = requests.get('http://cti-pub-files.oss-cn-shanghai.aliyuncs.com/pages/patch.html')
    #html3 = response3.text
    #list3 = re.findall(r'.*?\n', html3)

    #with open("./para1.txt", 'r') as f3:
        #list3 = f3.readlines()
    #response = requests.get('http://cti-pub-files.oss-cn-shanghai.aliyuncs.com/para1.txt')
    #all_text = response.text
    #list3= re.findall(r'.*?\n',all_text)
    #last_txt = re.findall(r'File Inclusion.*',all_text)


    with open(filename, 'w') as f:


        f.write('''﻿<html class=" js flexbox flexboxlegacy webgl no-touch geolocation rgba hsla multiplebgs backgroundsize borderimage borderradius boxshadow textshadow opacity cssanimations csscolumns cssgradients cssreflections csstransforms csstransforms3d csstransitions fontface no-generatedcontent svg inlinesvg smil svgclippaths" lang="zh-cn" xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-cn" style="">\n''')
        f.write('''\n''')
        f.write('''<head>\n''')
        f.write('''    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n''')
        f.write('''    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">\n''')
        f.write('''    <meta name="viewport" content="width=device-width, initial-scale=1">\n''')
        days1 = datetime.date(2018, 07, 01)
        days2 = datetime.date.today()
        num = (days2-days1).days
        weeks = (num//7)+1
        postfix = '(第'+str(weeks)+'周)'
        f.write('''    <title>xx网络安全行业威胁情报%s</title>\n'''%postfix)
        f.write('''    <meta http-equiv="Content-Language" content="en">\n''')
        f.write('''    <meta name="apple-mobile-web-app-capable" content="yes">\n''')
        f.write('''    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n''')
        f.write('''    <meta name="msapplication-config" content="/theme/xml/ieconfig.xml">\n''')
        f.write('''    <link rel="shortcut icon" href="https://www.ey.com/ecimages/EYlogo.ico">\n''')
        f.write('''    <link rel="apple-touch-icon" href="https://www.ey.com/ecimages/icon2x.png">\n''')
        f.write('''    <link rel="apple-touch-startup-image" href="https://www.ey.com/ecimages/startup-image.png">\n''')
        f.write('''    <style type="text/css">\n''')
        f.write('''    @charset "UTF-8";\n''')
        f.write('''    article.type-system-ey {\n''')
        f.write('''        text-align: righ;\n''')
        f.write('''        position: relative;\n''')
        f.write('''        background: #fff;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    html {\n''')
        f.write('''        font-family: sans-serif;\n''')
        f.write('''        -ms-text-size-adjust: 100%;\n''')
        f.write('''        -webkit-text-size-adjust: 100%;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    html {\n''')
        f.write('''        box-sizing: border-box;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    * {\n''')
        f.write('''        box-sizing: border-box;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    *,\n''')
        f.write('''    *::after,\n''')
        f.write('''    *::before {\n''')
        f.write('''        box-sizing: inherit;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    body {\n''')
        f.write('''        margin: 0;\n''')
        f.write('''        padding: 0;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    body {\n''')
        f.write('''        -webkit-font-feature-settings: "kern", "liga", "pnum";\n''')
        f.write('''        -ms-font-feature-settings: "kern", "liga", "pnum";\n''')
        f.write('''        font-feature-settings: "kern", "liga", "pnum";\n''')
        f.write('''        -webkit-font-smoothing: antialiased;\n''')
        f.write('''        -moz-osx-font-smoothing: grayscale;\n''')
        f.write('''        color: #333;\n''')
        f.write('''        font-family: "Helvetica Neue", "Helvetica", "Roboto", "Arial", sans-serif;\n''')
        f.write('''        font-size: 1em;\n''')
        f.write('''        line-height: 1.4;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    body {\n''')
        f.write('''        margin: 0;\n''')
        f.write('''        height: 100%;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    article,\n''')
        f.write('''    aside,\n''')
        f.write('''    details,\n''')
        f.write('''    figcaption,\n''')
        f.write('''    figure,\n''')
        f.write('''    footer,\n''')
        f.write('''    header,\n''')
        f.write('''    hgroup,\n''')
        f.write('''    main,\n''')
        f.write('''    menu,\n''')
        f.write('''    nav,\n''')
        f.write('''    section,\n''')
        f.write('''    summary {\n''')
        f.write('''        display: block;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    .article>section[class*=section]:nth-child(odd) {\n''')
        f.write('''        background-color: #f0f0f0;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    .article>section.section0 {\n''')
        f.write('''        padding-top: 60px;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    @media (min-width: 1200px) {\n''')
        f.write('''        .sl-landing>section,\n''')
        f.write('''        article>section,\n''')
        f.write('''        body>section {\n''')
        f.write('''            padding-left: 0;\n''')
        f.write('''            padding-right: 0;\n''')
        f.write('''        }\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    @media (min-width: 1200px) {\n''')
        f.write('''        .sl-landing>section,\n''')
        f.write('''        article>section,\n''')
        f.write('''        body>section {\n''')
        f.write('''            padding-left: 0;\n''')
        f.write('''            padding-right: 0;\n''')
        f.write('''        }\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    @media (min-width: 940px) {\n''')
        f.write('''        .sl-landing>section,\n''')
        f.write('''        article>section,\n''')
        f.write('''        body>section {\n''')
        f.write('''            padding: 40px;\n''')
        f.write('''        }\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    @media (min-width: 768px) {\n''')
        f.write('''        .sl-landing>section,\n''')
        f.write('''        article>section,\n''')
        f.write('''        body>section {\n''')
        f.write('''            padding: 40px 20px;\n''')
        f.write('''        }\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    .sl-landing>section,\n''')
        f.write('''    article>section,\n''')
        f.write('''    body>section {\n''')
        f.write('''        position: relative;\n''')
        f.write('''        -webkit-transition: all 0.4s;\n''')
        f.write('''        transition: all 0.4s;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    @media (min-width: 940px) {\n''')
        f.write('''        .container::after {\n''')
        f.write('''            clear: both;\n''')
        f.write('''            content: "";\n''')
        f.write('''            display: block;\n''')
        f.write('''        }\n''')
        f.write('''        .sl-landing .container {\n''')
        f.write('''            max-width: 68em;\n''')
        f.write('''        }\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    .container::after {\n''')
        f.write('''        clear: both;\n''')
        f.write('''        content: "";\n''')
        f.write('''        display: block;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    .maincolumn:last-child {\n''')
        f.write('''        margin-right: 0;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    @media (min-width: 768px) {\n''')
        f.write('''        .maincolumn {\n''')
        f.write('''            padding: 0;\n''')
        f.write('''            float: left;\n''')
        f.write('''            display: block;\n''')
        f.write('''            margin-right: 2.3576515979%;\n''')
        f.write('''            width: 100%;\n''')
        f.write('''            margin-right: 0;\n''')
        f.write('''        }\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    @media only screen and (min-width: 737px) {\n''')
        f.write('''        .type-system-ey .maincolumn h2,\n''')
        f.write('''        .type-system-ey section h2 {\n''')
        f.write('''            margin: 1em 0;\n''')
        f.write('''        }\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    .type-system-ey .maincolumn h2,\n''')
        f.write('''    .type-system-ey section h2 {\n''')
        f.write('''        font-size: 2.4em;\n''')
        f.write('''        margin: 0 0 0.5em;\n''')
        f.write('''        font-weight: normal;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    @media screen and (min-width: 40em) {\n''')
        f.write('''        .maincolumn h2,\n''')
        f.write('''        section h2 {\n''')
        f.write('''            width: 80%;\n''')
        f.write('''            letter-spacing: -0.03em;\n''')
        f.write('''            line-height: 1.1;\n''')
        f.write('''            padding: 0;\n''')
        f.write('''            margin: 1em 0;\n''')
        f.write('''        }\n''')
        f.write('''        .type-system-ey .maincolumn h2,\n''')
        f.write('''        .type-system-ey section h2 {\n''')
        f.write('''            font-size: 2.4em;\n''')
        f.write('''            margin: 0 0 0.5em;\n''')
        f.write('''            font-weight: normal;\n''')
        f.write('''        }\n''')
        f.write('''        .sl-landing .maincolumn h2,\n''')
        f.write('''        .sl-landing section h2 {\n''')
        f.write('''            font-size: 2.8em;\n''')
        f.write('''            padding-top: 40px;\n''')
        f.write('''            margin-top: 0;\n''')
        f.write('''        }\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    .maincolumn h2,\n''')
        f.write('''    section h2 {\n''')
        f.write('''        font-family: "Interstate-bold", sans-serif;\n''')
        f.write('''        font-size: 1.6em;\n''')
        f.write('''        font-weight: 400;\n''')
        f.write('''        line-height: 1.1em;\n''')
        f.write('''        margin-bottom: 0.5em;\n''')
        f.write('''        letter-spacing: -.03em;\n''')
        f.write('''        color: #646464;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    h1,\n''')
        f.write('''    h2,\n''')
        f.write('''    h3,\n''')
        f.write('''    p {\n''')
        f.write('''        margin: 0;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    h1,\n''')
        f.write('''    h2,\n''')
        f.write('''    h3,\n''')
        f.write('''    h4,\n''')
        f.write('''    h5,\n''')
        f.write('''    h6 {\n''')
        f.write('''        font-family: "Helvetica Neue", "Helvetica", "Roboto", "Arial", sans-serif;\n''')
        #f.write('''        font-size: 1em;\n''')
        f.write('''        line-height: 1.2;\n''')
        f.write('''        margin: 0 0 0.7em;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    p {\n''')
        f.write('''        -webkit-font-feature-settings: "onum" 1, "pnum" 1;\n''')
        f.write('''        font-feature-settings: "onum" 1, "pnum" 1;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    p {\n''')
        f.write('''        font-family: "Helvetica", sans-serif;\n''')
        f.write('''        font-weight: 300;\n''')
        f.write('''        margin: 1em 0;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    p {\n''')
        f.write('''        color: #333;\n''')
        f.write('''        line-height: 1.4;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    p {\n''')
        f.write('''        margin: 0 0 0.7em;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    h3 {\n''')
        f.write('''        font-family: "Interstate-bold", sans-serif;\n''')
        f.write('''        font-size: 1.3em;\n''')
        f.write('''        color: #646464;\n''')
        f.write('''        font-weight: 700;\n''')
        f.write('''        line-height: 1.4em;\n''')
        f.write('''        margin-top: 0.5em;\n''')
        f.write('''        margin-bottom: 0.5em;\n''')
        f.write('''        letter-spacing: -.02em;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    table.dataframe {\n''')
        f.write('''        font-size: 1em;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    table {\n''')
        f.write('''        -webkit-font-feature-settings: "kern", "liga", "tnum";\n''')
        f.write('''        -ms-font-feature-settings: "kern", "liga", "tnum";\n''')
        f.write('''        font-feature-settings: "kern", "liga", "tnum";\n''')
        f.write('''        border-collapse: collapse;\n''')
        f.write('''        margin: 0.7em 0;\n''')
        f.write('''        table-layout: fixed;\n''')
        f.write('''        width: 100%;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    table {\n''')
        f.write('''        border-collapse: collapse;\n''')
        f.write('''        border-spacing: 0;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    tr,\n''')
        f.write('''    td,\n''')
        f.write('''    th {\n''')
        f.write('''        vertical-align: middle;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    .dataframe th {\n''')
        f.write('''        background: #fff000;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    #thc1 {\n''')
        f.write('''        width: 18%;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    #thc2 {\n''')
        f.write('''        width: 20%;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    #thc3 {\n''')
        f.write('''        width: 12%;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    #thc4 {\n''')
        f.write('''        width: 50%;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    td,\n''')
        f.write('''    th {\n''')
        f.write('''        padding: 0;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''    th {\n''')
        f.write('''        border-bottom: 1px solid #a6a6a6;\n''')
        f.write('''        font-weight: 600;\n''')
        f.write('''        padding: 0.7em 0;\n''')
        f.write('''        text-align: left;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    td {\n''')
        f.write('''        border-bottom: 1px solid #ccc;\n''')
        f.write('''        padding: 0.7em 0;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    a {\n''')
        f.write('''        color: #369;\n''')
        f.write('''        text-decoration: none;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    article a {\n''')
        f.write('''        font-weight: bold;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    a {\n''')
        f.write('''        color: #369;\n''')
        f.write('''        text-decoration: none;\n''')
        f.write('''        -webkit-transition: color 0.1s linear;\n''')
        f.write('''        transition: color 0.1s linear;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    a {\n''')
        f.write('''        background-color: transparent;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    .container {\n''')
        f.write('''        max-width: 52em;\n''')
        f.write('''        margin-left: auto;\n''')
        f.write('''        margin-right: auto;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    a {\n''')
        f.write('''        color: #369;\n''')
        f.write('''        text-decoration: none;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    article a {\n''')
        f.write('''        font-weight: bold;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    a.logo {\n''')
        f.write('''        height: 70px;\n''')
        f.write('''        width: 145px;\n''')
        f.write('''        margin: 10px 0;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    a.logo {\n''')
        f.write('''        float: right;\n''')
        f.write('''        width: 145px;\n''')
        f.write('''        height: 66px;\n''')
        f.write('''        margin: -20px -61px -100px;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    a.logo img {\n''')
        f.write('''        height: 100%;\n''')
        f.write('''        max-height: 70px;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    h4 {\n''')
        f.write('''        font-size: 0.8em;\n''')
        f.write('''        color: #646464;\n''')
        f.write('''        font-weight: 700;\n''')
        f.write('''        line-height: 1.2em;\n''')
        f.write('''        margin-top: 0.5em;\n''')
        f.write('''        margin-bottom: 0.5em;\n''')
        f.write('''        letter-spacing: -.02em;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    .footer p {\n''')
        f.write('''        color: rgba(255, 255, 255, 0.6);\n''')
        f.write('''        font-size: 0.8em;\n''')
        f.write('''        line-height: 1.5em;\n''')
        f.write('''        margin: 1em auto;\n''')
        f.write('''        max-width: 52em;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    .footer {\n''')
        f.write('''        padding: 10px;\n''')
        f.write('''        background: #333;\n''')
        f.write('''        width: 100%;\n''')
        f.write('''    }\n''')
        f.write('''.topdetails {
        font-size:0.8em;
        color: #646464;
        text-align:center;
    }
\n''')
        f.write('''    </style>\n''')
        f.write('''    </div>\n''')
        f.write('''    </div>\n''')
        f.write('''    </div>\n''')
        f.write('''    <article class="article type-system-ey ">\n''')
        f.write('''<p class="topdetails">若该邮件无法正常显示，请<a href="https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/%s/report-v16.html" target="_blank">点击此处查看详情</a></p>\n'''%report_id)
        f.write('''        <section class="section0" id="section0" data-section-title="漏洞级别概况及目录" style="background-color:#F0F0F0">\n''')
        f.write('''            <div class="container">\n''')
        f.write('''                <div class="eyscrollogo"><a href="#" class="logo">\n''')
        f.write('''</a></div>\n''')
        f.write('''                <div class="maincolumn">\n''')
        days1 = datetime.date(2018, 07, 01)
        days2 = datetime.date.today()
        num = (days2-days1).days
        weeks = (num//7)+1
        postfix = '(第'+str(weeks)+'周)'
        f.write('''                    <h2>xx网络安全行业威胁情报%s</h2>\n'''%postfix)
        f.write('''                    <p>针对当下常见的网络应用，我们搜集并整理了的主流漏洞发布站点中与其相关的安全漏洞更新信息（若您需要定制化内容请<a href="mailto:services@eycyber.com">点击</a>联系我们），并进行汇总和分析，具体内容如下，</p>\n''')
        f.write('''                    <h3>1.本周安全漏洞级别概况</h3>\n''')

        #f.write('''                    <p>据2018年7月4日的扫描情况，共发现142个漏洞, 其中高风险漏洞1个，占总漏洞的0.70%; 中风险漏洞10个,占总漏洞的7.04%; 低危漏洞131个，占总漏洞的92.25%.以下为最新发布的十条高风险漏洞\n''')
        #f.write('''                    </p>\n''')
        f.write('''<p>%s,以下为最新发布的十条高风险漏洞:</p>\n''' % text1)
        f.write('''                    <p>\n''')
        f.write('''                        <!--*<h3>High risk vulnerability</h3>-->\n''')
        #f.write('''<table border="1" class="dataframe">\n''')
        #f.write('''<thead>\n''')
        #f.write('''<tr style="text-align: right;">\n''')
        #f.write('''<th id=thc1>cveId</th>''')
        #f.write('''<th id=thc2>Vulnerability Type</th>\n''')
        #f.write('''<th id=thc3>Date</th>\n''')
        #f.write('''<th id=thc4>Description</th>\n''')
        #f.write('''</tr>\n''')
        #f.write('''</thead>\n''')

        #for list_each1 in list1[8:]:
            #f.write('''%s\n''' % list_each1)
        #f.write('''</table>\n''')

        i = 0
        for stu_cell in list1:
            #print(stu_cell)
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
                #print(stu_cell[1])
                #print(i)
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
        #f.write('''        </section>\n''')
        f.write('''        <section class="section2" id="section2" data-section-title="漏洞类别" style="background-color:#F0F0F0">\n''')
        f.write('''            <div class="container">\n''')
        f.write('''                <div class="maincolumn">\n''')
        f.write('''                    <h3>2.漏洞类别</h3>\n''')
        #f.write('''                    <p>本次所扫描到的漏洞可根据风险类别分为以下主要10类, 高危漏洞类别按数量正序分布如下： Not Defined: 47个 XSS: 19个 Overflow: 14个 Exec Code: 10个 DoS: 8个 CSRF: 7个 Exec Code XSS: 6个 DoS Overflow: 6个 +Info: 6个 Bypass: 4个</p>''')
        f.write('''<p>%s</p>\n''' % text2)

        #f.write('''        <section class="section2" id="section2" data-section-title="漏洞类别" style="background-color:#F0F0F0">\n''')
        #f.write('''            <div class="container">\n''')
        #f.write('''                <div class="maincolumn">\n''')
        #f.write('''                    <h3>2.漏洞类别</h3>\n''')
        #f.write('''                    <p>本次所扫描到的漏洞可根据风险类别分为以下主要10类, 高危漏洞类别按数量正序分布如下： Not Defined: 47个 XSS: 19个 Overflow: 14个 Exec Code: 10个 DoS: 8个 CSRF: 7个 Exec Code XSS: 6个 DoS Overflow: 6个 +Info: 6个 Bypass: 4个</p>\n''')
        f.write('''                    <!-- <div class="col large-3">  </div> -->\n''')
        f.write('''                    <section class="section3" id="section3" data-section-title="金融事件" style="background-color:#F0F0F0">\n''')
        f.write('''                        <div class="container">\n''')
        f.write('''                            <div class="maincolumn">\n''')
        f.write('''                                <h3>3.金融行业数据风险事件</h3> </div>\n''')
        f.write('''                        </div>\n''')
        for i in range(3):
            # <a href="链接的页面" target="_blank">新窗口打开</a>
            # f.write('''<p>%d.%s</p>''' % (i+1,finance['title'][i]))

            f.write('''                                <p><a href="%s" target="_blank">%d.%s</a></p>\n''' % (finance['link'][i], i + 1, finance['title'][i]))
            f.write('''                                <p>时间：%s</p>\n''' % finance['time'][i])
            f.write('''                                <p>作者：%s</p>\n''' % finance['author'][i])
            f.write('''                                <p>事件概要：%s</p>\n''' % finance['briefContent'][i])
        f.write('''                        <!-- <div class="col large-3">  </div> -->\n''')

        f.write('''                        <section class="section4" id="section4" data-section-title="科技事件" style="background-color:#F0F0F0">\n''')
        f.write('''                            <div class="container">\n''')
        f.write('''                                <div class="maincolumn">\n''')
        f.write('''                                    <h3>4.科技行业数据风险事件</h3> </div>\n''')
        f.write('''                            </div>\n''')

        for i in range(3):
            #f.write('''<p>%d.%s</p>''' % (i+1,science['title'][i]))
            f.write('''                                <p><a href="%s" target="_blank">%d.%s</a></p>\n''' % (science['link'][i], i + 1, science['title'][i]))
            f.write('''                                <p>时间：%s</p>\n''' % science['time'][i])
            f.write('''                                <p>作者：%s</p>\n''' % science['author'][i])
            f.write('''                                <p>事件概要：%s</p>\n''' % science['briefContent'][i])
        f.write('''                            <!-- <div class="col large-3">  </div> -->\n''')
        f.write('''                            <section class="section5" id="section5" data-section-title="零售事件" style="background-color:#F0F0F0">\n''')
        f.write('''                                <div class="container">\n''')
        f.write('''                                    <div class="maincolumn">\n''')
        f.write('''                                        <h3>5.新零售行业数据风险事件</h3> </div>\n''')
        f.write('''                                </div>\n''')

        for i in range(3):
            #f.write('''<p>%d.%s</p>''' % (i+1,retail['title'][i]))
            f.write('''<p><a href="%s" target="_blank">%d.%s</a></p>\n''' % (retail['link'][i], i + 1, retail['title'][i]))
            f.write('''<p>时间：%s</p>\n''' % retail['time'][i])
            f.write('''<p>作者：%s</p>\n''' % retail['author'][i])
            f.write('''<p>事件概要：%s</p>\n''' % retail['briefContent'][i])

        f.write('''                </div>\n''')
        f.write('''                <div class="container">\n''')
        f.write('''                    <div class="maincolumn">\n''')
        f.write('''                        <h4>更多详细内容请<a href="https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/%s/report-v16.html" target="_blank">点击此处查看</a></h4></div>\n'''%report_id)
        f.write('''                </div>\n''')
        f.write('''            </div>\n''')
        f.write('''    </article>\n''')
        f.write('''    <footer class="footer" id="footer" role="contentinfo">\n''')
        f.write('''        <div class="footer-logo">\n''')
        f.write('''            <div class="footer-links"></div>\n''')
        f.write('''            <p class="detail">声明：以上内容均来自互联网，由CTI网络威胁情报团队整理，其版权归属原作者所有，其观点并不代表我方观点和意见，请酌情参考或采用。若对以上所引用内容有任何疑问或问题，请与services@eycyber.com联系。</p>\n''')
        f.write('''        </div>\n''')
        f.write('''    </footer>\n''')
        f.write('''    </body>\n''')
        f.write('''\n''')
        f.write('''</html>\n''')
    with open('test_industry_word0705_3.html', 'rb') as fileobj:
        directory = report_id + '/test_industry_word0705_3.html'
        result = bucket.put_object(directory,fileobj)
def main():


    # min=0,max=0,month=5,year=2018
    ##    cursor,db = ConnectSQL()
    #headers = COOKIES('http://www.cnvd.org.cn/flaw/list.htm?flag=true?number=%E8%AF%B7%E8%BE%93%E5%85%A5%E7%B2%BE%E7%A1%AE%E7%BC%96%E5%8F%B7&startDate=&endDate=&flag=true&field=&order=&max=20&offset=0')
    
    #print(retail)
    write_html('test_industry_word0705_3.html','s','d')


if __name__ == '__main__':
    main()
