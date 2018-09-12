#encoding: utf-8
import re
import mysql.connector
import oss2
import csv
import sys
import datetime
import requests
from console_visualizer import go_thierry
import os
db_host = os.environ['db_host']
db_password = os.environ['db_password']
oss_host = os.environ['oss_host']
oss_password = os.environ['oss_password']
auth = oss2.Auth(oss_host, oss_password)
bucket = oss2.Bucket(auth, 'oss-cn-shanghai.aliyuncs.com', 'cti-pub-files')
reload(sys)
sys.setdefaultencoding('utf-8')

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
        sql2 = '''update %s set news_sector = '%s' where news_hash = '%s';''' % (table, industry_name,date[1])
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
                finance_count += len(re.findall(fin,date[0]))
        for sci in science:
            sci = re.sub('[\r\n]+','',sci)
            if re.findall(sci,date[0]) != []:
                science_count += len(re.findall(sci,date[0]))
        for ret in retail:
            ret = re.sub('[\r\n]+','',ret)
            if re.findall(ret,date[0]) != []:
                retail_count += len(re.findall(ret,date[0]))
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
    select news_title,news_publishedTime,news_author,news_content,news_link,news_sector from cisco_hash WHERE news_publishedTime >= (NOW() - INTERVAL 7 DAY)  and news_sector = '%s' ORDER BY news_publishedTime DESC;''' % (category,category,category)



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
    sql = '''select compliance_title,compliance_publishedTime,compliance_author,compliance_content,compliance_link,compliance_industry from cac_hash WHERE compliance_publishedTime >= (NOW() - INTERVAL 365 DAY)  and compliance_industry = '%s' order by compliance_publishedTime desc;''' % category



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


    text1,text2 = go_thierry(report_id,request_id)
    list1 = csv.reader(open('./high_level.csv', 'r'))
    list2 = csv.reader(open('./patch_ch.csv', 'r'))

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



    with open(filename, 'w') as f:




        f.write('''<html class=" js flexbox flexboxlegacy webgl no-touch geolocation rgba hsla multiplebgs backgroundsize borderimage borderradius boxshadow textshadow opacity cssanimations csscolumns cssgradients cssreflections csstransforms csstransforms3d csstransitions fontface no-generatedcontent svg inlinesvg smil svgclippaths" lang="zh-cn" xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-cn" style="">\n''')
        f.write('''\n''')
        f.write('''<head>\n''')
        f.write('''    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n''')
        f.write('''    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">\n''')
        f.write('''    <meta name="viewport" content="width=device-width, initial-scale=1">\n''')
        f.write('''    <title>云雀网络安全行业威胁情报</title>\n''')
        f.write('''    <meta http-equiv="Content-Language" content="en">\n''')
        f.write('''    <link rel="stylesheet" href="https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/css/style.css">\n''')
        f.write('''    <link rel="stylesheet" href="https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/css/advisory-jquery-ui.min.css">\n''')
        f.write('''    <link rel="stylesheet" href="https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/css/cookienotification.min.css">\n''')
        f.write('''    <style>\n''')
        f.write('''        .contact-us-cnt h3 {\n''')
        f.write('''        border-left: 5px solid #ffe400;\n''')
        f.write('''        padding: 5px;\n''')
        f.write('''        background: #f7f7f7;\n''')
        f.write('''        font-size: 1.8em;\n''')
        f.write('''        margin-top: 10px;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    .modal .modal-inner {\n''')
        f.write('''        max-width: 1000px;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    .modal-content img {\n''')
        f.write('''        max-width: 1100px !important;\n''')
        f.write('''        margin: 30px auto;\n''')
        f.write('''        display: block;\n''')
        f.write('''    </style>\n''')
        f.write('''    <header class="main-header">\n''')
        f.write('''        <div class="container">\n''')
        f.write('''            <div class="eyscrollogo"><a href="#" class="logo"><img src="https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/pics/careers_ey_logo_zh_CN.png" alt="EY Ernst Young logo" border="0"></a></div>\n''')
        f.write('''            <section class="right clearfix"> </section>\n''')
        f.write('''        </div>\n''')
        f.write('''    </header>\n''')
        f.write('''    <div class="eyhero hero-text-left" style="background-image: url(https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/pics/banner.jpg); background-size: cover; background-position: 80% 50%;">\n''')
        f.write('''        <div class="article-hero-container">\n''')
        f.write('''            <div class="headline-container frame3x2 box3x2 fluid-box ">\n''')
        f.write('''                <!-- add box3x2 class above for solid box -->\n''')
        f.write('''                <svg viewBox="0 0 800 610" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:sketch="http://www.bohemiancoding.com/sketch/ns">\n''')
        f.write('''                    <defs>\n''')
        f.write('''                        <style type="text/css">\n''')
        f.write('''                        @font-face {\n''')
        f.write('''                            font-family: "Interstate", sans-serif;\n''')
        f.write('''                            src: url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-2.eot");\n''')
        f.write('''                            src: url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-2.eot?") format("embedded-opentype"), url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-3.woff") format("woff"), url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-1.ttf") format("truetype");\n''')
        f.write('''                            src: url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-3.woff") format("woff");\n''')
        f.write('''                        }\n''')
        f.write('''\n''')
        f.write('''                        [id^="tagline-"] {\n''')
        f.write('''                            font-family: "Interstate";\n''')
        f.write('''                            fill: #ffffff;\n''')
        f.write('''                            letter-spacing: 1px;\n''')
        f.write('''                            font-size: 24px;\n''')
        f.write('''                            letter-spacing: -.03em;\n''')
        f.write('''                        }\n''')
        f.write('''                        </style>\n''')
        f.write('''                        <filter x="-50%" y="-50%" width="200%" height="200%" filterUnits="objectBoundingBox" id="filter-1">\n''')
        f.write('''                            <feOffset dx="0" dy="0" in="SourceAlpha" result="shadowOffsetOuter1"></feOffset>\n''')
        f.write('''                            <feGaussianBlur stdDeviation="2.5" in="shadowOffsetOuter1" result="shadowBlurOuter1"></feGaussianBlur>\n''')
        f.write('''                            <feColorMatrix values="0 0 0 0 0   0 0 0 0 0   0 0 0 0 0  0 0 0 0.35 0" in="shadowBlurOuter1" type="matrix" result="shadowMatrixOuter1"></feColorMatrix>\n''')
        f.write('''                            <feMerge>\n''')
        f.write('''                                <feMergeNode in="shadowMatrixOuter1"></feMergeNode>\n''')
        f.write('''                                <feMergeNode in="SourceGraphic"></feMergeNode>\n''')
        f.write('''                            </feMerge>\n''')
        f.write('''                        </filter>\n''')
        f.write('''                        <linearGradient x1="50%" y1="0%" x2="50%" y2="100%" id="darkGradient">\n''')
        f.write('''                            <stop stop-color="#000000" stop-opacity="0.6" offset="0%"></stop>\n''')
        f.write('''                            <stop stop-color="#000000" stop-opacity="0" offset="100%"></stop>\n''')
        f.write('''                        </linearGradient>\n''')
        f.write('''                        <linearGradient x1="50%" y1="0%" x2="50%" y2="100%" id="lightGradient">\n''')
        f.write('''                            <stop stop-color="#ffffff" stop-opacity="0.6" offset="0%"></stop>\n''')
        f.write('''                            <stop stop-color="#ffffff" stop-opacity="0" offset="100%"></stop>\n''')
        f.write('''                        </linearGradient>\n''')
        f.write('''                    </defs>\n''')
        f.write('''                    <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd" sketch:type="MSPage">\n''')
        f.write('''                        <g id="3x2-frame" sketch:type="MSArtboardGroup">\n''')
        f.write('''                            <g id="frames" sketch:type="MSLayerGroup" transform="translate(9.000000, 32.000000)">\n''')
        f.write('''                                <g id="dots" transform="translate(1.000000, 511.000000)" fill="#FFE600" sketch:type="MSShapeGroup">\n''')
        f.write('''                                    <rect id="Rectangle-2" x="0" y="0" width="12" height="12"></rect>\n''')
        f.write('''                                    <rect id="0:0:0:0" x="42" y="0" width="12" height="12"></rect>\n''')
        f.write('''                                    <rect id="0:0:0:0-copy" x="21" y="0" width="12" height="12"></rect>\n''')
        f.write('''                                </g>\n''')
        f.write('''                                <path d="M22,115 L537,25.2818985 L537,427 L22,427 L22,115 Z" id="gradient" fill="url(#darkGradient)" sketch:type="MSShapeGroup"></path>\n''')
        f.write('''                                <path d="M88,447 L113,447 L113,472 L88,472 L88,447 Z M44,447 L69,447 L69,472 L44,472 L44,447 Z M0,447 L25,447 L25,472 L0,472 L0,447 Z M130.955,446.766 L534.275,446.766 L534.275,30.151 L25.724,119.822 L25.724,428.874 L0.4993,428.874 L0.4993,98.656 L559.499,0.089 L559.499,471.99 L130.954,471.99 L130.955,446.766 Z" id="frame" fill="#FFE600" sketch:type="MSShapeGroup"></path>\n''')
        f.write('''                                <path d="M0.499300892,98.567 L559.5,0 L559.5,471.901 L0,471.911 L0.499300892,98.567 Z" id="box" sketch:type="MSShapeGroup"></path>\n''')
        f.write('''                                <path d="M0.000699708326,503.779999 L0.000699708326,130.601559 L745.004444,0 L745.004444,503.779699 L0,503.779699 L0.000699708326,503.779999 Z" id="4x2-box" sketch:type="MSShapeGroup"></path>\n''')
        f.write('''                            </g>\n''')
        f.write('''                        </g>\n''')
        f.write('''                    </g>\n''')
        f.write('''                </svg>\n''')
        f.write('''                <div class="smartquestion">\n''')
        f.write('''                    <div class="heading-block fluid-type">\n''')
        f.write('''                        <h1 class="eyhero-headline-1">云雀网络安全行业威胁情报<br>感知、抵御、应对</h1>\n''')
        f.write('''                        <h2 class="eyhero-subheading-1">云雀网络安全行业威胁情报(第6周)</h2> </div>\n''')
        f.write('''                </div>\n''')
        f.write('''                <div class="status">status</div>\n''')
        f.write('''            </div>\n''')
        f.write('''        </div>\n''')
        f.write('''    </div>\n''')
        f.write('''</head>\n''')
        f.write('''<article class="article type-system-ey ">\n''')
        f.write('''    <section class="section0" id="section0" data-section-title="漏洞级别概况及目录" style="background-color:#F0F0F0">\n''')
        f.write('''        <div class="container">\n''')
        f.write('''            <aside id="scroll-on-page-top" class="article-subnav">\n''')
        f.write('''                <ul id="featuremenu">\n''')
        f.write('''                    <li id="feature01"><a href="#maincolumn">数据风险事件</a></li>\n''')
        f.write('''                    <li id="feature02"><a href="#section4">合规新闻</a></li>\n''')
        f.write('''                    <li id="feature03"><a href="#section6">漏洞级别</a></li>\n''')
        f.write('''                    <li id="feature04"><a href="#section8">漏洞类别</a></li>\n''')
        f.write('''                </ul>\n''')
        f.write('''            </aside>\n''')
        f.write('''            <div class="maincolumn">\n''')
        f.write('''\n''')
        f.write('''        <div class="container">\n''')
        f.write('''          \n''')
        f.write('''            <h3>数据风险事件</h3>\n''')
        f.write('''<p>截至2018年8月6日对相关事件站点的扫描情况，我们列出金融、科技和零售三个行业的最新资讯，内容如下：</p>\n''')
        f.write('''            \n''')
        f.write('''                    <h4>金融行业数据风险事件</h4>\n''')
        f.write('''            \n''')
        f.write('''            \n''')
        f.write('''               \n''')
        for index, fin in enumerate(finance):
            f.write('''<p><a href="%s" target="_blank">%d.%s</a></p>''' % (fin['link'],index + 1, fin['title']))
            f.write('''<p>时间：%s</p>''' % fin['time'])
            f.write('''<p>作者：%s</p>''' % fin['author'])
            f.write('''<p>事件概要：%s</p>''' % fin['content'][:200])



        f.write('''                </div></div>\n''')
        f.write('''                <!-- <div class="col large-3">  </div> -->\n''')
        f.write('''\n''')
        f.write('''    <section class="section2" id="section2" data-section-title="数据风险事件" style="background-color:#F0F0F0">\n''')
        f.write('''        <div class="container">\n''')
        f.write('''            <div class="row">\n''')
        f.write('''                <div class="col large-9">\n''')
        f.write('''                    <h4>科技行业数据风险事件</h4> </div>\n''')
        f.write('''            </div>\n''')
        f.write('''            <div class="row">\n''')
        f.write('''                <div class="col large-9">\n''')

        for index, sci in enumerate(science):
            f.write('''<p><a href="%s" target="_blank">%d.%s</a></p>''' % (sci['link'],index + 1, sci['title']))
            f.write('''<p>时间：%s</p>''' % sci['time'])
            f.write('''<p>作者：%s</p>''' % sci['author'])
            f.write('''<p>事件概要：%s</p>''' % sci['content'][:200])




        f.write('''                    <!-- <div class="col large-3">  </div> --></div>\n''')
        f.write('''            </div>\n''')
        f.write('''    </section>\n''')
        f.write('''    <section class="section2" id="section2" data-section-title="数据风险事件" style="background-color:#F0F0F0">\n''')
        f.write('''        <div class="container">\n''')
        f.write('''            <div class="row">\n''')
        f.write('''                <div class="col large-9">\n''')
        f.write('''                    <h4>新零售行业数据风险事件</h4> </div>\n''')
        f.write('''            </div>\n''')
        f.write('''            <div class="row">\n''')
        f.write('''                <div class="col large-9">\n''')

        for index, ret in enumerate(retail):
            f.write('''<p><a href="%s" target="_blank">%d.%s</a></p>''' % (ret['link'],index + 1, ret['title']))
            f.write('''<p>时间：%s</p>''' % ret['time'])
            f.write('''<p>作者：%s</p>''' % ret['author'])
            f.write('''<p>事件概要：%s</p>''' % ret['content'][:200])



        f.write('''                </div>\n''')
        f.write('''                <!-- <div class="col large-3"><img title="安永第19届全球信息安全调查报告" alt="安永第19届全球信息安全调查报告" src="https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/pics/53-rs.png"></div> --></div>\n''')
        f.write('''        </div>\n''')
        f.write('''    </section>\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''    <section class="section4" id="section4" data-section-title="合规新闻" style="background-color:#F0F0F0">\n''')
        f.write('''        <div class="container">\n''')
        f.write('''            <div class="row">\n''')
        f.write('''                <div class="col large-9">\n''')
        f.write('''                    <h3>合规新闻</h3>\n''')
        f.write('''<p>截至2018年8月6日对相关合规新闻站点的扫描情况，我们列出三个金融、科技和零售行业的最新资讯，内容如下：</p>\n''')


        f.write('''                    <h4>金融行业合规新闻</h4> </div>\n''')
        f.write('''            </div>\n''')
        f.write('''            <div class="row">\n''')
        f.write('''                <div class="col large-9">\n''')

        for index, fin in enumerate(com_finance):
            f.write('''<p><a href="%s" target="_blank">%d.%s</a></p>''' % (fin['link'],index + 1, fin['title']))
            f.write('''<p>时间：%s</p>''' % fin['time'])
            f.write('''<p>作者：%s</p>''' % fin['author'])
            f.write('''<p>事件概要：%s</p>''' % fin['content'][:200])


        f.write('''                </div>\n''')
        f.write('''                <!-- <div class="col large-3">  </div> --></div>\n''')
        f.write('''        </div>\n''')
        f.write('''    </section>\n''')
        f.write('''    <section class="section4" id="section4" data-section-title="合规新闻" style="background-color:#F0F0F0">\n''')
        f.write('''        <div class="container">\n''')
        f.write('''            <div class="row">\n''')
        f.write('''                <div class="col large-9">\n''')
        f.write('''                    <h4>科技行业合规新闻</h4> </div>\n''')
        f.write('''            </div>\n''')
        f.write('''            <div class="row">\n''')
        f.write('''                <div class="col large-9">\n''')

        for index, sci in enumerate(com_science):
            f.write('''<p><a href="%s" target="_blank">%d.%s</a></p>''' % (sci['link'],index + 1, sci['title']))
            f.write('''<p>时间：%s</p>''' % sci['time'])
            f.write('''<p>作者：%s</p>''' % sci['author'])
            f.write('''<p>事件概要：%s</p>''' % sci['content'][:200])



        f.write('''                    <!-- <div class="col large-3">  </div> --></div>\n''')
        f.write('''            </div>\n''')
        f.write('''    </section>\n''')
        f.write('''    <section class="section4" id="section4" data-section-title="合规新闻" style="background-color:#F0F0F0">\n''')
        f.write('''        <div class="container">\n''')
        f.write('''            <div class="row">\n''')
        f.write('''                <div class="col large-9">\n''')
        f.write('''                    <h4>新零售行业合规新闻</h4> </div>\n''')
        f.write('''            </div>\n''')
        f.write('''            <div class="row">\n''')
        f.write('''                <div class="col large-9">\n''')

        for index, ret in enumerate(com_retail):
            f.write('''<p><a href="%s" target="_blank">%d.%s</a></p>''' % (ret['link'],index + 1, ret['title']))
            f.write('''<p>时间：%s</p>''' % ret['time'])
            f.write('''<p>作者：%s</p>''' % ret['author'])
            f.write('''<p>事件概要：%s</p>''' % ret['content'][:200])




        f.write('''                </div>\n''')
        f.write('''                <!-- <div class="col large-3"><img title="安永第19届全球信息安全调查报告" alt="安永第19届全球信息安全调查报告" src="https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/pics/53-rs.png"></div> --></div>\n''')
        f.write('''        </div>\n''')
        f.write('''    </section>\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')
        f.write('''\n''')


        f.write('''<section class="section6" id="section6" data-section-title="漏洞类别" style="background-color:#F0F0F0">\n''')
        f.write('''\n''')
        f.write('''        <div class="container">\n''')
        f.write('''            <div class="row">\n''')
        f.write('''                <div class="col large-9">\n''')

        f.write('''<h3>本周安全漏洞级别概况</h3>''')
        f.write('''<p>%s</p>''' % text1)
        f.write(
            '''<p><iframe src="https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/%s/pie.html" width=800px  height=380px  frameborder="0"  scrolling="no"></iframe><h3>High risk vulnerability</h3>''' % report_id)
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

                i += 1

        f.write('''</tbody>\n''')
        f.write('''</table>\n''')
        f.write(
            '''</p></div></div></section><section class="section8" id="section8" data-section-title="漏洞类别" style="background-color:#F0F0F0">''')
        f.write(
            ''' <div class="container"><div class="row"><div class="col large-9"><h3>漏洞类别</h3> </div></div><div class="row"><div class="col large-9">''')

        f.write('''<p>%s</p>''' % text2)
        f.write('''<iframe src="https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/%s/bar1.html"''' % report_id)
        f.write('''width="750" height="420" scrolling="no" frameborder="0"></iframe>''')



        f.write('''                    <!-- <div class="col large-3">  </div> --></div>\n''')
        f.write('''            </div>\n''')
        f.write('''    </section>\n''')
        f.write('''\n''')
        f.write('''</article>\n''')
        f.write('''<footer class="footer" id="footer" role="contentinfo">\n''')
        f.write('''    <div class="footer-logo">\n''')
        f.write('''        <div class="footer-links"></div>\n''')
        f.write('''        <p class="detail">声明：以上内容均来自互联网，由CTI网络威胁情报团队整理，其版权归属原作者所有，其观点并不代表我方观点和意见，请酌情参考或采用。若对以上所引用内容有任何疑问或问题，请与jacob.mhj@gmail.com联系。</p>\n''')
        f.write('''    </div>\n''')
        f.write('''</footer>\n''')
        f.write('''</body>\n''')
        f.write('''\n''')
        f.write('''</html>\n''')
    with open('industry.html', 'rb') as fileobj:
        directory = report_id + '/industry.html'
        result = bucket.put_object(directory,fileobj)
def main():



    write_html('industry.html','report_id','request_id')


if __name__ == '__main__':
    main()

