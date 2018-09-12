#/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests
from lxml import etree
import mysql.connector
import requests
import sys
import datetime
import sh_logger
from flask import Flask, request
from flask import Response
from flask import json
from flask import Flask, redirect, url_for, request, render_template, make_response, abort, jsonify, \
    send_from_directory,redirect
import time
import re
import hashlib
import sys
import urllib2
import cookielib
import re
reload(sys)
sys.setdefaultencoding('utf-8')
WAITING= 'WAITING TO RUN'
RUNNING = 'RUNNING'
FINISHED = 'FINISHED'
PAUSED = 'PAUSED'
TERMINATED = 'TERMINATED'
LOCATION='SH'
logger = sh_logger.get_logger(__name__)
################################################################################################################################
def COOKIES(url):
    s = requests.session()  # 获取会话对象
    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'}  # 设置请求的信息头

    login = s.get(url, headers=headers1)  # 向服务器发出POST请求
    print login.status_code  # 请求的状态码
    print login.url  # 请求成功后跳转页面的URL
 

    cookie = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    opener.addheaders = [('User-agent',
                          'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36')]
    response = opener.open(url)

    cookieStr = ''
    for item in cookie:
        cookieStr = cookieStr + item.name + '=' + item.value + ';'


    bdshare_firstime = 'bdshare_firstime=' + str(int(time.time() * 1000))
    cookies = cookieStr + bdshare_firstime

    logger.debug(cookies)
    headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        "Origin": "http://www.cnvd.org.cn",
        "Host": "www.cnvd.org.cn",
        "Referer": "http://www.cnvd.org.cn/flaw/list.htm?flag=true",
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cookie': cookies
    }

    response = requests.get(url, headers=headers)

    print("the statu is -----"+str(response.status_code))

    return headers


def get_one_page(url, headers):
    response = requests.get(url, headers=headers)
    print(response.status_code)
    return response.text


def cnvd_Urlcreator(first_page,page,job_id,created_time):
    headers = COOKIES('http://www.cnvd.org.cn/flaw/list.htm?flag=true?number=%E8%AF%B7%E8%BE%93%E5%85%A5%E7%B2%BE%E7%A1%AE%E7%BC%96%E5%8F%B7&startDate=&endDate=&flag=true&field=&order=&max=20&offset=0')
    url_firstPage = []
    url_page_list = []
    url_page = []

    url_firstPage.append(
        "http://www.cnvd.org.cn/flaw/list.htm?flag=true?number=%E8%AF%B7%E8%BE%93%E5%85%A5%E7%B2%BE%E7%A1%AE%E7%BC%96%E5%8F%B7&startDate=&endDate=&flag=true&field=&order=&max=20&offset=0"
    )

    url_page_list.append(url_firstPage[-1])

    for i in range(first_page + 1, page + 1):
        url_page_list.append(
            "http://www.cnvd.org.cn/flaw/list.htm?flag=true?number=%E8%AF%B7%E8%BE%93%E5%85%A5%E7%B2%BE%E7%A1%AE%E7%BC%96%E5%8F%B7&startDate=&endDate=&flag=true&field=&order=&max=20&offset=" + str(
                i * 20)
        )

    #print(url_page_list)

    for i in url_page_list:
        response = requests.get(i, headers=headers)
        html = response.content.decode("utf-8")
        selector = etree.HTML(html)
        #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[5]
        # //*[@id="vulner_0"]/p/a
        # //*[@id="vulner_1"]/p/a
        # /html/body/div[5]/div[1]/div/div[2]/table/tbody/tr[1]/td[1]/a
        cnvdid_list = selector.xpath('//table[@class="tlist"]//tr')

        cnvdids = []
        for cnvdid in cnvdid_list:
            if cnvdid.xpath('./td[1]/a/@href') == []:
                cnvdid_ = None
            else:
                cnvdid_ = cnvdid.xpath('./td[1]/a/@href')[0].strip()
            cnvdids.append(cnvdid_)
            if cnvdid_ != None:
                url_page.append("http://www.cnvd.org.cn" + str(cnvdid_))
    #print(url_page)
    print(len(url_page))
    return url_page


def cnvd_scrapper(url_page_list,job_id,created_time,task_id):
    # headers = COOKIES('http://www.cnvd.org.cn/flaw/list.htm?flag=true?number=%E8%AF%B7%E8%BE%93%E5%85%A5%E7%B2%BE%E7%A1%AE%E7%BC%96%E5%8F%B7&startDate=&endDate=&flag=true&field=&order=&max=20&offset=0')
    total_length = len(url_page_list)
    suceess_count=0 
    unsuccessful_count=0
    
    start_time = datetime.datetime.now()
    status = RUNNING
    lasted_time='None'
    end_time='None'
    location=LOCATION
    percentage = float(suceess_count) / total_length
    send_out_data={}
    send_out_data['job_id']=job_id
    send_out_data['created_time']=created_time
    send_out_data['start_time']=start_time.strftime("%Y-%m-%d %H:%M:%S")
    send_out_data['lasted_time']=lasted_time
    send_out_data['status']=status
    send_out_data['end_time']=end_time
    send_out_data['location']=location
    send_out_data['percentage']=percentage
    send_out_data['unsuccessful_count']=unsuccessful_count
    send_out_data['task_id']=task_id
    for index, url in enumerate(url_page_list[:]):
        
        logger.debug('======== this is the url area =====================')
        print(url)
        logger.debug('======== this is the url area =====================')
        # time.sleep(2)
        response = requests.get(url, headers=COOKIES('http://www.cnvd.org.cn/flaw/list.htm?flag=true?number=%E8%AF%B7%E8%BE%93%E5%85%A5%E7%B2%BE%E7%A1%AE%E7%BC%96%E5%8F%B7&startDate=&endDate=&flag=true&field=&order=&max=20&offset=0'))
        html = response.content.decode('utf-8')
        selector = etree.HTML(html)

        print(response.status_code)
        print(index)
        
        ##        print(response.text)
        try:
            table_rows = selector.xpath('//div[@class="mw Main clearfix"]//tr')
        except Exception as e:
            print(e)
            logger.debug(e)
            logger.debug('no pass!!!!!!!!')
            pass

        dic = {'CNVD-ID': 'None', '公开日期': 'None', '危害级别': 'None', '影响产品': 'None', 'CVE ID': 'None', '漏洞描述': 'None',
               '参考链接': 'None', '漏洞解决方案': 'None',
               '厂商补丁': 'None', '验证信息': 'None', '报送时间': 'None', '收录时间': 'None', '更新时间': 'None', '漏洞附件': 'None'}
        data_list=[]
        for inde, row in enumerate(table_rows[:-2]):
            td_1 = row.xpath(
                '//div[@class="mw Main clearfix"]//table[@class="gg_detail"]//tr[' + str(inde + 1) + ']//td[1]')[
                0].xpath('string()')
            td_1 = re.sub(r'\s+', ' ', td_1)
            td_1 = td_1.encode('utf-8')
            td_2 = row.xpath(
                '//div[@class="mw Main clearfix"]//table[@class="gg_detail"]//tr[' + str(inde + 1) + ']//td[2]')[
                0].xpath('string()')
            td_2 = re.sub(r'\s+', ' ', td_2)
            td_2 = re.sub(r'^\s+', '', td_2)
            td_2 = re.sub(r'\s+$', '', td_2)
            td_2 = re.sub(r'\(AV.*?\)', '', td_2)
            dic[td_1] = td_2
        #print(dic['CNVD-ID'], dic['公开日期'], dic['危害级别'], dic['影响产品'], dic['CVE ID'], dic['漏洞描述'], dic['参考链接'],
              #dic['漏洞解决方案'], dic['厂商补丁'], dic['验证信息'],  dic['更新时间'], dic['漏洞附件'])

        ##            if index == 0:
        ##                print(type(description))
       # hash_string = str(dic['CVE ID']) + str(dic['CNVD-ID']).strip() + str(dic['更新时间']).strip()
        #hash_string = hash_string.strip()

        #sha1 = hashlib.sha1()
        #sha1.update(hash_string.encode("utf-8"))
        #hashvalue = sha1.hexdigest()
        hash_string = dic['CVE ID'].encode('utf-8') + dic['CNVD-ID'].encode('utf-8') + dic['更新时间'].encode('utf-8')
        sha1 = hashlib.sha1()
        sha1.update(hash_string)
        hashvalue = sha1.hexdigest()

        dicts = {'vul_id':dic['CNVD-ID'], 'vul_cveId':dic['CVE ID'], 'vul_cweId':'', 'vul_describe':dic['漏洞描述'], \
        'vul_score':'', 'vul_level':dic['危害级别'], 'vul_type':'', 'vul_cvssAccess':'', \
        'vul_cvsComplexity':'', 'vul_cvssAuthentication':'', 'vul_cvssConf':'', 'vul_cvssInteg':'', \
        'vul_cvssAvail':'', 'vul_name':'', 'vul_publishedDate':dic['公开日期'], 'vul_updateDate':dic['更新时间'], \
        'vul_containSol':dic['漏洞解决方案'], 'vul_source':'', 'vul_effectedProduct':dic['影响产品'], 'vul_vendor':'', \
        'vul_patch':dic['厂商补丁'], 'vul_author':'', 'vul_expCode':'', 'vul_hash':hashvalue}
        data_list.append(dicts)
        headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
        receive1=requests.post("http://cti_hk_cns00.eycyber.com:8080/cnvd_data",data=json.dumps(data_list),headers=headers)
        #. 每次大 for loop 都会有一个list  你一个小for loop 装一个字典， 这个字典 里面的信息是job的信息 ， 加进去。
        #[{}]

        suceess_count+=1
        percentage = float(suceess_count) / total_length
        send_out_data= job_update(send_out_data,'percentage',percentage)
        # send_out_data= job_update(send_out_data,'status',RUNNING)
        # send_out_data= job_update(send_out_data,'location',LOCATION)
        #reporting ...... 
        receive3=requests.post("http://cti_hk_cns00.eycyber.com:8080/reporting",data=send_out_data)
        # if index % 1400 ==0:## heartbeat sending reporting
        #     logger.debug('===============================')
        #     logger.debug(send_out_data)
        #     logger.debug('===============================')
        #     receive2=requests.post("http://cti_hk_cns00.eycyber.com:8080/reporting",data=send_out_data)
    percentage = float(suceess_count) / total_length
    end_time = datetime.datetime.now()
    lasted_time = end_time - start_time
    send_out_data= job_update(send_out_data,'end_time',end_time.strftime("%Y-%m-%d %H:%M:%S"))
    send_out_data= job_update(send_out_data,'lasted_time',lasted_time)
    send_out_data= job_update(send_out_data,'status',FINISHED)
    send_out_data= job_update(send_out_data,'percentage',percentage)
    logger.debug('============== the reporting data is below=================')
    logger.debug(send_out_data)
    receive3=requests.post("http://cti_hk_cns00.eycyber.com:8080/reporting",data=send_out_data)

def xuanwu_Urlcreator(days):
    now = datetime.datetime.now()
    
    url_firstPage = []
    url_page = []

    url_firstPage.append(
        "https://xuanwulab.github.io/cn/secnews/" + str(now.strftime('%Y/%m/%d')) + "/index.html"
    )

    html = requests.get(url_firstPage[-1]).content.decode("utf-8")
    response = requests.get(url_firstPage[-1])
    print(response.status_code)
    selector = etree.HTML(html)
    if response.status_code == 200:
        url_page.append(url_firstPage[-1])

    for i in range(1, days + 1):
        url_page.append(
            "https://xuanwulab.github.io/cn/secnews/" + str(
                (now - datetime.timedelta(days=i)).strftime('%Y/%m/%d')) + "/index.html"
        )
    print(url_page)
    return url_page


def xuanwu_scrapper(created_time, task_id, job_id,url_page_list):

    suceess_count = 0
    unsuccessful_count = 0

    start_time = datetime.datetime.now()
    status = RUNNING
    lasted_time = 'None'
    end_time = 'None'
    location = LOCATION
    total_length = len(url_page_list)
    percentage = float(suceess_count) / total_length
    job_data = {}
    job_data['job_id'] = job_id
    job_data['created_time'] = created_time
    job_data['start_time'] = start_time.strftime("%Y-%m-%d %H:%M:%S")
    job_data['lasted_time'] = lasted_time
    job_data['status'] = status
    job_data['end_time'] = end_time
    job_data['location'] = location
    job_data['percentage'] = percentage
    job_data['unsuccessful_count'] = unsuccessful_count
    job_data['task_id'] = task_id
    table_rows = []

    for index, url in enumerate(url_page_list):

        html = requests.get(url).content.decode('utf-8')
        selector = etree.HTML(html)

        response = requests.get(url)
        response.encoding='utf-8'
        print(response.status_code)
        print(index)
        ##        print(response.text)
        now = datetime.datetime.now()
        Time = (now - datetime.timedelta(days=index)).strftime('%Y/%m/%d')
        table_rows = selector.xpath('//div[@class="singleweibotext"]')

        ##        print(table_rows)
        data_list = []
        for index, row in enumerate(table_rows):

            Categories = row.xpath('./p/span')
            Names = row.xpath('./p/text()')
            Links = row.xpath('./p/a')

            cells = [Categories, Names, Links]

            for col in cells[0]:
                if row.xpath('./p/span') == None:
                    Category = None
                else:
                    Category = col.text

            for col in cells[1]:
                if row.xpath('./p/text()') == None:
                    Name = None
                else:
                    Name = col.strip().encode('utf-8')
                    Name = re.sub(':','',Name)
                    Name = re.sub('：','',Name)
                    if '：' in Name:
                        print(Name)
            for col in cells[2]:
                if row.xpath('./p/a') == None:
                    Link = None
                else:
                    Link = col.text

            try:
                Category = Category.decode('utf-8')
            except:
                pass
            try:
                Name = Name.decode('utf-8')
            except:
                pass
            try:
                Time = Time.decode('utf-8')
            except:
                pass

            hash_string = Category.encode('utf-8') + Name.encode('utf-8') + Time.encode('utf-8')

            sha1 = hashlib.sha1()
            sha1.update(hash_string)
            hashvalue = sha1.hexdigest()


            send_out_data = {}
            logger.debug(type(Category))
            send_out_data['Category'] = Category
            send_out_data['Names'] = Name
            send_out_data['Link'] = Link
            send_out_data['Times'] = Time
            send_out_data['news_hash'] = hashvalue
            data_list.append(send_out_data)
        headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
        receive1=requests.post("http://cti_hk_cns00.eycyber.com:8080/xuanwu_data",data=json.dumps(data_list),headers=headers)
        suceess_count += 1
        percentage = float(suceess_count) / total_length
        logger.debug('================= we are checking the two digits .... ==============')
        logger.debug(total_length)
        logger.debug(suceess_count)
        logger.debug('================= we are checking the two digits .... ==============')
        job_data = job_update(job_data, 'percentage', percentage)
        # send_out_data= job_update(send_out_data,'status',RUNNING)
        # send_out_data= job_update(send_out_data,'location',LOCATION)
        # reporting ......
        receive3 = requests.post("http://cti_hk_cns00.eycyber.com:8080/reporting", data=job_data)
        # if index % 1400 ==0:## heartbeat sending reporting
        #     logger.debug('===============================')
        #     logger.debug(send_out_data)
        #     logger.debug('===============================')
        #     receive2=requests.post("http://cti_hk_cns00.eycyber.com:8080/reporting",data=send_out_data)
    percentage = float(suceess_count) / total_length
    logger.debug(total_length)
    logger.debug(suceess_count)
    end_time = datetime.datetime.now()
    lasted_time = end_time - start_time
    job_data = job_update(job_data, 'end_time', end_time.strftime("%Y-%m-%d %H:%M:%S"))
    job_data = job_update(job_data, 'lasted_time', lasted_time)
    job_data = job_update(job_data, 'status', FINISHED)
    job_data = job_update(job_data, 'percentage', percentage)
    logger.debug('============== the reporting data is below=================')
    logger.debug(job_data)
    receive3 = requests.post("http://cti_hk_cns00.eycyber.com:8080/reporting", data=job_data)



################################### Hades Specail Area #########################################

def cac_Urlcreator_nl(page):
    url_page_list = []
    url_page = []
    for i in range(1, page + 1):
        url_page_list.append(
            'http://qc.wa.news.cn/nodeart/list?nid=1184063&pgnum=' + str(i) + '&cnt=36&attr=63&tp=1&orderby=1')
    print(url_page_list)
    for j in url_page_list:
        response = requests.get(j)
        print(response.status_code)
        html = response.content.decode("utf-8")

        cac_list = re.findall(r'"LinkUrl":".*?htm"', html)
        for cac_one in cac_list:
            cac_page = re.sub(r'"LinkUrl":"', '', cac_one)
            cac_page = re.sub(r'"', '', cac_page)
            url_page.append(cac_page)
    print(len(url_page))
    return url_page

#网络安全
def cac_Urlcreator_ns(firstpage, page):
    url_page_list = []
    url_page = []
    for i in range(firstpage, page + 1):
        url_page_list.append(
            'http://search.cac.gov.cn/was5/web/search?channelid=246506&searchword=extend5%3D%27%251182959%25%27&prepage=60&list=&page=' + str(
                i))
    print(url_page_list)
    for j in url_page_list:
        # print(j)

        response = requests.get(j)
        print(response.status_code)
  
        html = response.content.decode("utf-8")
        selector = etree.HTML(html)
        tc_list = selector.xpath('//*[@class="zwlist"]//li')
        for inde, row in enumerate(tc_list):
            if row.xpath('.//a/@href') != []:
                if row.xpath('.//a/@href')[0].strip() == 'http://':
                    row_page = row.xpath('.//a[2]/@href')[0].strip()
                else:
                    row_page = row.xpath('.//a/@href')[0].strip()
                # row_page = 'https://www.tc260.org.cn' +row_page
                url_page.append(row_page)
            # print(url_page)
    print(len(url_page))
    return url_page


##执法督查
def cac_Urlcreator_aef():
    url_page_list = [
        'http://search.cac.gov.cn/was5/web/search?channelid=246506&prepage=36&searchword=extend5%3D%27%2511121715%25%27',
        'http://search.cac.gov.cn/was5/web/search?channelid=246506&prepage=36&searchword=extend5%3D%27%251182984%25%27']
    for j in url_page_list:
        response = requests.get(j)
        print(response.status_code)
        html = response.content.decode("utf-8")
        selector = etree.HTML(html)
        tc_list = selector.xpath('//*[@class="zwlist"]//li')
        url_page = []
        for inde, row in enumerate(tc_list):
            if row.xpath('.//a/@href') != []:
                if row.xpath('.//a/@href')[0].strip() == 'http://':
                    row_page = row.xpath('.//a[2]/@href')[0].strip()
                else:
                    row_page = row.xpath('.//a/@href')[0].strip()
                url_page.append(row_page)
    print(len(url_page))
    # print(url_page)
    print("*********")
    return url_page

#政策法规
def cac_Urlcreator_pr():
    url_page_list = [
        'http://search.cac.gov.cn/was5/web/search?channelid=246506&prepage=36&searchword=extend5%3D%27%251182981%25%27',
        'http://search.cac.gov.cn/was5/web/search?channelid=246506&prepage=36&searchword=extend5%3D%27%251182982%25%27',
        'http://search.cac.gov.cn/was5/web/search?channelid=246506&prepage=36&searchword=extend5%3D%27%251182983%25%27',
        'http://search.cac.gov.cn/was5/web/search?channelid=246506&prepage=36&searchword=extend5%3D%27%251182962%25%27']

    url_page = []
    for j in url_page_list:
        print(j)
        response = requests.get(j)
        print(response.status_code)
        html = response.content.decode("utf-8")
        selector = etree.HTML(html)
        tc_list = selector.xpath('//*[@class="zwlist"]//li')

        for inde, row in enumerate(tc_list):
            if row.xpath('.//a/@href') != []:
                if row.xpath('.//a/@href')[0].strip() == 'http://':
                    row_page = row.xpath('.//a[2]/@href')[0].strip()
                else:
                    row_page = row.xpath('.//a/@href')[0].strip()
                url_page.append(row_page)

    print(len(url_page))
    return url_page


def cac_scrapper(url,category):
    response = requests.get(url)
    html_text = response.text
    html = response.content
    selector = etree.HTML(html)
    print(response.status_code)
    if selector.xpath('//*[@id="title"]') != []:
        title = selector.xpath('//*[@id="title"]')[0].xpath('string()').strip()
        title = re.sub(r'\s+', ' ', title).strip()

    else:
        title = 'None'
    if selector.xpath('//*[@id="pubtime"]') != []:
        time = selector.xpath('//*[@id="pubtime"]')[0].xpath('string()').strip()
        time = re.sub(r'\s+', '', time)
        time = time.encode('utf-8')
        time = datetime.datetime.strptime(time, '%Y年%m月%d日%H:%M:%S')
        time = time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        time = 'none'
    if selector.xpath('//*[@id="source"]') != []:
        source = selector.xpath('//*[@id="source"]')[0].xpath('string()').strip()
        source = re.sub(r'\s+', '', source).encode("utf-8")
        source = re.sub(r'来源：', '', source)
    else:
        source = 'none'
    if selector.xpath('//*[@id="content"]') != []:
        content = selector.xpath('//*[@id="content"]')[0].xpath('string()')
        content = re.sub(r'\s+', ' ', content)

        content = content.strip()


    else:
        content = 'none'
    hash_string = title.encode('utf-8') + time.encode('utf-8')

    sha1 = hashlib.sha1()
    sha1.update(hash_string)
    hashvalue = sha1.hexdigest()



    author = '中共中央网络安全和信息化委员会办公室'
    
    dic = {}
    dic['compliance_title'] = title
    dic['compliance_author'] = author
    dic['compliance_publishedTime'] = time
    dic['compliance_content'] = content
    dic['compliance_hash'] = hashvalue
    dic['compliance_link'] = url
    dic['compliance_source'] = source
    dic['compliance_tags'] = category
    return dic



def cac(job_id,created_time,task_id):
    suceess_count=0 
    unsuccessful_count=0
    
    start_time = datetime.datetime.now()
    status = RUNNING
    lasted_time='None'
    end_time='None'
    location=LOCATION

    send_out_data={}
    send_out_data['job_id']=job_id
    send_out_data['created_time']=created_time
    send_out_data['start_time']=start_time.strftime("%Y-%m-%d %H:%M:%S")
    send_out_data['lasted_time']=lasted_time
    send_out_data['status']=status
    send_out_data['end_time']=end_time
    send_out_data['location']=location
  
    send_out_data['unsuccessful_count']=unsuccessful_count
    send_out_data['task_id']=task_id
    url_page_nl = cac_Urlcreator_nl(1)
    url_page_ns = cac_Urlcreator_ns(1, 1)
    url_page_aef = cac_Urlcreator_aef()
    url_page_pr = cac_Urlcreator_pr()
    url_page_all = {}
    url_page_all['地方网信'] = url_page_nl
    url_page_all['网络安全'] = url_page_ns
    url_page_all['执法督察'] = url_page_aef
    url_page_all['政策法规'] = url_page_pr


    total_length = len(url_page_all)
    percentage = float(suceess_count) / total_length
    send_out_data['percentage']=percentage
    for category, url_page in url_page_all.items():
        try:
            category = category.encode('utf-8')
        except Exception as e:
            pass
        print('正在爬%s模块，总共有%s条' % (category, len(url_page)))
        data_list = []
        for index, url in enumerate(url_page):
            print(url)
            print(index)
            dic = cac_scrapper(url,category)
            data_list.append(dic)
        headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
        receive1=requests.post("http://cti_hk_cns00.eycyber.com:8080/cac_data",data=json.dumps(data_list),headers=headers)
        suceess_count+=1
        percentage = float(suceess_count) / total_length
        send_out_data= job_update(send_out_data,'percentage',percentage)
        receive3=requests.post("http://cti_hk_cns00.eycyber.com:8080/reporting",data=send_out_data)
    percentage = float(suceess_count) / total_length
    end_time = datetime.datetime.now()
    lasted_time = end_time - start_time
    send_out_data= job_update(send_out_data,'end_time',end_time.strftime("%Y-%m-%d %H:%M:%S"))
    send_out_data= job_update(send_out_data,'lasted_time',lasted_time)
    send_out_data= job_update(send_out_data,'status',FINISHED)
    send_out_data= job_update(send_out_data,'percentage',percentage)
    logger.debug('============== the reporting data is below=================')
    logger.debug(send_out_data)
    receive3=requests.post("http://cti_hk_cns00.eycyber.com:8080/reporting",data=send_out_data)
######################compliance#########################


def tc260_Urlcreator(firstpage,page,job_id,created_time,task_id):
    url_page_list = []
    url_page = []
    for i in range(firstpage ,page+1 ):
        subject_dict = {u'新闻动态': 'https://www.tc260.org.cn/front/hydtList.html?postType=1&start=',
                        u'通知公告': 'https://www.tc260.org.cn/front/hydtList.html?postType=2&start='}
        subjects = {}
        for key, value in subject_dict.items():
            url_page_list.append(value + str(i * 100 - 100) + '&length=100')
    print(url_page_list)
    for j in url_page_list:
        response = requests.get(j)
        print(response.status_code)
        html = response.content.decode("utf-8")
        selector = etree.HTML(html)
        tc_list = selector.xpath('//ul[@class="list-group"]/li')
        for inde, row in enumerate(tc_list):
            if row.xpath('//ul[@class="list-group"]/li[' + str(inde + 1) + ']//@href') != []:
                row_page =row.xpath('//ul[@class="list-group"]/li[' + str(inde + 1) + ']//@href')[0].strip()
                row_page = 'https://www.tc260.org.cn' +row_page
                url_page.append(row_page)
    print(len(url_page))
    return url_page

def tc260_scrapper(url_page,job_id,created_time,task_id):
    total_length = len(url_page)
    suceess_count=0 
    unsuccessful_count=0
    
    start_time = datetime.datetime.now()
    status = RUNNING
    lasted_time='None'
    end_time='None'
    location=LOCATION
    percentage = float(suceess_count) / total_length
    send_out_data={}
    send_out_data['job_id']=job_id
    send_out_data['created_time']=created_time
    send_out_data['start_time']=start_time.strftime("%Y-%m-%d %H:%M:%S")
    send_out_data['lasted_time']=lasted_time
    send_out_data['status']=status
    send_out_data['end_time']=end_time
    send_out_data['location']=location
    send_out_data['percentage']=percentage
    send_out_data['unsuccessful_count']=unsuccessful_count
    send_out_data['task_id']=task_id
    for index, url in enumerate(url_page):
        print(url)
        print(index)
        response = requests.get(url)
        html_text = response.text
        html = response.content
        selector = etree.HTML(html)
        print(response.status_code)
        if selector.xpath('//*[@class="news_end_tit"]/text()')!= []:
            title = selector.xpath('//*[@class="news_end_tit"]/text()')[0]
            title = re.sub(r'\s+',' ',title).strip()

        else:
            title = ''
        if selector.xpath('//*[@class="news_end_tit"]/span')!= []:
            time = selector.xpath('//*[@class="news_end_tit"]/span')[0].xpath('string()').strip()
        else:
            time = ''
        if selector.xpath('//*[@id="new_content"]')!= []:
            content = selector.xpath('//*[@id="new_content"]')[0].xpath('string()')
            content = re.sub(r'\s+',' ',content)
            content = content.strip()

        else:
            content = ''
        hash_string = title.encode('utf-8') + time.encode('utf-8')

        sha1 = hashlib.sha1()
        sha1.update(hash_string)
        hashvalue = sha1.hexdigest()

        dic = {}
        dic['compliance_title'] = title
        dic['compliance_author'] = '全国信息安全标准化技术委员会'
        dic['compliance_publishedTime'] = time
        dic['compliance_content'] = content
        dic['compliance_hash'] = hashvalue
        dic['compliance_link'] = url
        dic['compliance_source'] = '全国信息安全标准化技术委员会'
        dic['compliance_tags'] = ''

        # data_list.append(dic)
        headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
        receive1=requests.post("http://cti_hk_cns00.eycyber.com:8080/tc260_data",data=json.dumps(dic),headers=headers)
        suceess_count+=1
        percentage = float(suceess_count) / total_length
        send_out_data= job_update(send_out_data,'percentage',percentage)
        if index % 11 ==0:## heartbeat sending reporting for the job status......
            receive2=requests.post("http://cti_hk_cns00.eycyber.com:8080/reporting",data=send_out_data)
    percentage = float(suceess_count) / total_length
    end_time = datetime.datetime.now()
    lasted_time = end_time - start_time
    send_out_data= job_update(send_out_data,'end_time',end_time.strftime("%Y-%m-%d %H:%M:%S"))
    send_out_data= job_update(send_out_data,'lasted_time',lasted_time)
    send_out_data= job_update(send_out_data,'status',FINISHED)
    send_out_data= job_update(send_out_data,'percentage',percentage)
    receive3=requests.post("http://cti_hk_cns00.eycyber.com:8080/reporting",data=send_out_data)


##########safe_gove


def save_gove_Urlcreator(firstpage,page):
    url_page_list = []
    url_page = []
    for i in range(firstpage,page+1):
        url_string = 'http://www.safe.gov.cn/wps/portal/!ut/p/c5/hY3NCoJAGEWfpSf4rjb6ubURZqYxQ8JSNzKEiOFPiwh6-3TXprp3eTgcqmn55J595x79PLmBSqrDRstEHqzyENlzBGOCk9wX1vctL7wKG6liLTgFIqEAI3bHTMvcg9n-sS9r77e_cnxZDMr0PLZUUc0fnZQZJldGJwh8MFM1tJ27vug-lriJYvMGKtbQqQ!!/dl3/d3/L0lJSklna2shL0lCakFBTXlBQkVSQ0lBISEvWUZOQzFOS18yN3chLzdfSENEQ01LRzEwOEw3NzBJUUdJSEQwNTIwNzc!/?WCM_PI=1&PC_7_HCDCMKG108L770IQGIHD052077000000_WCM_Page.6cb085004383ddc69621df7e81ade6ff='
        url_page_list.append(url_string + str(i))
    url_page = []
    for j in url_page_list:
        while True:
            response = requests.get(j)
            print(response.status_code)
            if response.status_code == 200:
                break
        html = response.text
        all_url = re.findall(r'<td align="left" ><a href=".*?" target="_blank"',html)
        for a_url in all_url:
            a_url = re.sub(r'^<td align="left" ><a href="','http://www.safe.gov.cn',a_url)
            a_url = re.sub(r'" target="_blank"$', '', a_url)
            url_page.append(a_url)
    print(len(url_page))
    return url_page
def save_gove_scrapper(url_page,job_id,created_time,task_id):

    total_length = len(url_page)
    suceess_count=0 
    unsuccessful_count=0
    start_time = datetime.datetime.now()
    status = RUNNING
    lasted_time='None'
    end_time='None'
    location=LOCATION
    percentage = float(suceess_count) / total_length
    send_out_data={}
    send_out_data['job_id']=job_id
    send_out_data['created_time']=created_time
    send_out_data['start_time']=start_time.strftime("%Y-%m-%d %H:%M:%S")
    send_out_data['lasted_time']=lasted_time
    send_out_data['status']=status
    send_out_data['end_time']=end_time
    send_out_data['location']=location
    send_out_data['percentage']=percentage
    send_out_data['unsuccessful_count']=unsuccessful_count
    send_out_data['task_id']=task_id
    for index, url in enumerate(url_page):
        print(index)
        response = requests.get(url)
        html_text = response.text
        html = response.content
        selector = etree.HTML(html)
        if selector.xpath('//*[@id="syh"]')!= []:
            reference = selector.xpath('//*[@id="syh"]')[0].xpath('string()').strip()
            reference = re.sub(r'\s+',' ',reference)

        else:
            reference = None
        if selector.xpath('//*[@id="Title"]')!= []:
            title= selector.xpath('//*[@id="Title"]')[0].xpath('string()').strip()
            title = re.sub(r'\s+',' ',title)
            title = re.sub(r'.*?=\'','',title)
            title = re.sub(r'\';.*','',title)
        else:
            title = None
        if selector.xpath('//*[@id="lSubcat"]')!= []:
            classification = selector.xpath('//*[@id="lSubcat"]')[0].xpath('string()').strip()
            
            classification = re.sub(r'(&nbsp;)|(&gt;)','',classification)
            classification = classification.encode('utf-8')
            classification = re.sub(r'(主题)|(体裁)|(服务对象)','',classification).strip()
            
            classification = re.sub(r'>>','',classification)
            classification = re.sub(r'\s+',' ',classification).strip()
        else:
            classification = None
        if selector.xpath('//*[@id="wenhaotd"]/span')!= []:
            titanic = selector.xpath('//*[@id="wenhaotd"]/span')[0].xpath('string()').strip()
            titanic = re.sub(r'\s+',' ',titanic)
            titanic = re.sub(r'主题 &gt;&gt; ','',titanic)
            titanic = re.sub(r'&gt;','',titanic).strip()
        else:
            titanic = None
        time_text = re.findall(r'<td width="50%" style=\'font-size:14px\'>.*?</tr>',html_text,re.S)
        time_text = re.sub(r'\n|\r','',time_text[1],re.S)
        time_text = re.sub(r'^.*?<span>','',time_text,re.S)
        
        source = re.sub(r'</span>.*','',time_text,re.S)
        
        time = re.sub(r'^.*?<span>','',time_text,re.S)
        time = re.sub(r'</span>.*','',time,re.S)
        time = datetime.datetime.strptime(time, '%Y/%m/%d')
        time = time.strftime('%Y-%m-%d')
        if selector.xpath('//*[@id="newsContent"]')!= []:
            content = selector.xpath('//*[@id="newsContent"]')[0].xpath('string()')
            content = re.sub(r'\s+',' ',content)
            content = content.strip()
        else:
            content = ''

        hash_string = title.encode('utf-8') + time.encode('utf-8')

        sha1 = hashlib.sha1()
        sha1.update(hash_string)
        hashvalue = sha1.hexdigest()

        dic = {}
        dic['compliance_title'] = title
        dic['compliance_author'] = '国家外管局'
        dic['compliance_publishedTime'] = time
        dic['compliance_content'] = content
        dic['compliance_hash'] = hashvalue
        dic['compliance_link'] = url
        dic['compliance_source'] = source
        dic['compliance_tags'] = ''


        headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
        receive1=requests.post("http://cti_hk_cns00.eycyber.com:8080/safe_gave_data",data=json.dumps(dic),headers=headers)
        suceess_count+=1
        percentage = float(suceess_count) / total_length
        send_out_data= job_update(send_out_data,'percentage',percentage)
        send_out_data= job_update(send_out_data,'status',RUNNING)
        send_out_data= job_update(send_out_data,'location',LOCATION)
        if index % 11 ==0:## heartbeat sending reporting for the job status......
            receive2=requests.post("http://cti_hk_cns00.eycyber.com:8080/reporting",data=send_out_data)
    percentage = float(suceess_count) / total_length
    end_time = datetime.datetime.now()
    lasted_time = end_time - start_time
    send_out_data= job_update(send_out_data,'end_time',end_time.strftime("%Y-%m-%d %H:%M:%S"))
    send_out_data= job_update(send_out_data,'lasted_time',lasted_time)
    send_out_data= job_update(send_out_data,'status',FINISHED)
    send_out_data= job_update(send_out_data,'percentage',percentage)
    receive3=requests.post("http://cti_hk_cns00.eycyber.com:8080/reporting",data=send_out_data)
################################### Hades Specail Area #########################################

def job_update(send_out_data,key,value):
    send_out_data[key]=value
    return send_out_data

