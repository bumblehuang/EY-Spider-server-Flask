# -*- coding: utf-8 -*-
import urllib2
import urllib
from http import cookiejar
import requests
from lxml.etree import XMLSyntaxError
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq
import mysql.connector
from flask import Flask, request
from flask import Response
from flask import json
from flask import Flask, redirect, url_for, request, render_template, make_response, abort, jsonify, \
    send_from_directory,redirect
import time
import re
import hashlib
import sys
import cookielib
import datetime
# from config import *
import sh_logger
import time
import re
from selenium import webdriver

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
WAITING= 'WAITING TO RUN'
RUNNING = 'RUNNING'
FINISHED = 'FINISHED'
PAUSED = 'PAUSED'
TERMINATED = 'TERMINATED'
LOCATION='SH'
logger = sh_logger.get_logger(__name__)

MAX_COUNT = 5
# KEYWORDS = ['云安全','GDPR','网络安全','区块链','以太币']
base_url = 'http://weixin.sogou.com/weixin?'
headers = {
    'Host': 'weixin.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Referer': 'http://weixin.sogou.com/weixin?type=2&ie=utf-8&s_from=hotnews&query=%E5%8D%8E%E5%B8%9D%E9%80%80%E6%AC%BE%E5%8F%98%E9%80%80%E5%8D%A1'

}

proxy = None

def get_cookies():
    driver = webdriver.Chrome()
    driver.get("http://weixin.sogou.com/")
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="loginBtn"]').click()
    time.sleep(10)

    # cookies = ""
    # for cookie in driver.get_cookies():
    #     cookies += u"%s=%s; "%(cookie["name"], cookie["value"])
    cookies = driver.get_cookies()
    cookie = {}
    for items in cookies:
        cookie[items.get('name')] = items.get('value')

    print(cookie)
    return cookie
    print(cookie)

def get_cookies_brief():
    url = "http://weixin.sogou.com/"
    headers = {
        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36'
    }

    cookie = cookiejar.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    resp = opener.open(url)

    cookieStr = {}
    for item in cookie:
        cookieStr[item.name] = item.value

    print(cookieStr)
    return cookieStr

def get_proxy():
    # try:
    #     response = requests.get(PROXY_POOL_URL)
    #     if response.status_code == 200:
    #         return response.text
    #     return None
    # except ConnectionError:
    #     return None
    proxy_list = []
    i = random.randit(3)

    return proxy_list[i-1]

def get_html(url, cookies,count=1):
    print('Crawling', url)
    print('Trying Count', count)
    global proxy

    print(proxy)
    if count >= MAX_COUNT:
        print('Tried Too Many Counts')
        return None
    try:
        if proxy:
            proxies = {
                'http': 'http://' + proxy,
                'https': 'https://' + proxy,
            }
            print(proxies)
            response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies, cookies = cookies)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers, cookies = cookies)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            # Need Proxy
            print('302')
            proxy = get_proxy()
            if proxy:
                print('Using Proxy', proxy)
                return get_html(url,cookies)
            else:
                print('Get Proxy Failed')
                return None
    except ConnectionError as e:
        print('Error Occurred', e.args)
        proxy = get_proxy()
        count += 1
        return get_html(url, count)



def get_index(keyword, page,cookies):
    data = {
        'query': keyword,
        #date criteria
        'tsn': 1,
        'type': 2,
        'page': page,
        # 'usip':'AWS云计算'
    }
    queries = urllib.urlencode(data)
    url = 'http://weixin.sogou.com/weixin?usip=&query={data[query]}&ft=&tsn={data[tsn]}&et=&interation=&type={data[type]}&wxid=&page={data[page]}&ie=utf8'.format(data=data)
    #
    print(url)
    html = get_html(url,cookies)
    return html

def parse_index(html):
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('href')

def get_detail(url):
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        print(response.encoding)
        print('**********************')
        print(response.apparent_encoding)
        print('**********************')
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

def parse_detail(html,url):
    try:
        doc = pq(html)
        title = doc('.rich_media_title').text()
        content = doc('.rich_media_content').text()
        try:
            date = re.search('var.*?publish_time = "(.*?)".*?', html).group(1)
        except:
            date = " "
        # date = doc('#publish_time').text()
        nickname = doc('#js_profile_qrcode > div > strong').text()
        wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
        return {
            'title': title,
            'date': date,
            'content': content,
            'nickname': nickname,
            'wechat': wechat,
            'html':str(url)
        }
    except XMLSyntaxError:
        return None

def save_to_mongo(data):
    if db['articles'].update({'title': data['title']}, {'$set': data}, True):
        print('Saved to Mongo', data['title'])
    else:
        print('Saved to Mongo Failed', data['title'])

# def info_to_db(keyword,data):

#     db = mysql.connector.connect(user='root',
#                                  password=db_password,
#                                  host=db_host,
#                                  database='0_social_media'
#                                  )

#     # set the parsing code
#     db.set_charset_collation('utf8')
#     cursor = db.cursor()

#     sql1 = '''CREATE TABLE IF NOT EXISTS `wechat` (
#       `title` nvarchar(255) NOT NULL,
#       `content` mediumtext  DEFAULT NULL,
#       `date`  nvarchar(30) DEFAULT NULL,
#       `nickname` nvarchar(1000)  DEFAULT NULL,
#       `wechat` nvarchar(500)  DEFAULT NULL,
#       `link` text  DEFAULT NULL,
#       `keyword` text  DEFAULT NULL,
#        PRIMARY KEY (`title`));'''.format(keyword)

#     cursor.execute(sql1)

#     sql2 = '''REPLACE INTO `wechat` (`title`,`content`,`date`,`nickname`,`wechat`,`link`,`keyword`) \
#                     VALUES\
#                     (%s, %s, %s, %s, %s, %s, %s);'''

#     # print(data['title'], data['content'], data['date'], data['nickname'], data['wechat'])
#     try:
#         cursor.execute(sql2,
#                        (data['title'], data['content'], data['date'], data['nickname'], data['wechat'],data['html'], keyword))
#     except Exception as e:
#         print(e)
#         print(type(data['html']),data['html'])


#     try:
#         db.commit()
#     except:
#         # if unexecuted, rollback
#         db.rollback()

def wechat_scrape(job_id,created_time,task_id,keywords):
    if ',' in keywords:
        KEYWORDS = keywords.split(',')
    else:
        KEYWORDS = []
        KEYWORDS.append(keywords)
    suceess_count=0 
    unsuccessful_count=0
    start_time = datetime.datetime.now()
    status = RUNNING
    lasted_time='None'
    end_time='None'
    location=LOCATION
    total_length = len(KEYWORDS)
    percentage = suceess_count / total_length
    send_out_data2={}
    send_out_data2['job_id']=job_id
    send_out_data2['created_time']=created_time
    send_out_data2['start_time']=start_time.strftime("%Y-%m-%d %H:%M:%S")
    send_out_data2['lasted_time']=lasted_time
    send_out_data2['status']=status
    send_out_data2['end_time']=end_time
    send_out_data2['location']=location
    send_out_data2['percentage']=percentage
    send_out_data2['unsuccessful_count']=unsuccessful_count
    send_out_data2['task_id']=task_id
    for keyword in KEYWORDS:
        time.sleep(13)
        cookies = get_cookies_brief()
        data_list = []
        for page in range(1, 10):
            time.sleep(8)
            html = get_index(keyword, page,cookies)
            if html:
                article_urls = parse_index(html)
                for article_url in article_urls:
                    time.sleep(5)
                    article_html = get_detail(article_url)
                    if article_html:
                        article_data = parse_detail(article_html,article_url)
                        print(article_data)
                        if article_data:
                            send_out_data = {}
                            send_out_data['title']=article_data['title']
                            send_out_data['content'] = article_data['content']
                            send_out_data['date']= article_data['date']
                            send_out_data['nickname']= article_data['nickname']
                            send_out_data['wechat']=article_data['wechat']
                            send_out_data['link']=article_data['html']
                            send_out_data['keyword']=keyword
                            data_list.append(send_out_data)
                            headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
        receive1=requests.post("http://cti_hk_cns00.eycyber.com:8080/wechat_data",data=json.dumps(data_list),headers=headers)
        suceess_count+=1
        percentage = float(suceess_count)/ total_length
        send_out_data2= job_update(send_out_data2,'percentage',percentage)
        receive3=requests.post("http://cti_hk_cns00.eycyber.com:8080/reporting",data=send_out_data2)
    percentage = float(suceess_count) / total_length
    end_time = datetime.datetime.now()
    lasted_time = end_time - start_time
    send_out_data2= job_update(send_out_data2,'end_time',end_time.strftime("%Y-%m-%d %H:%M:%S"))
    send_out_data2= job_update(send_out_data2,'lasted_time',lasted_time)
    send_out_data2= job_update(send_out_data2,'status',FINISHED)
    send_out_data2= job_update(send_out_data2,'percentage',percentage)
    logger.debug('============== the reporting data is below=================')
    logger.debug(send_out_data2)
    receive3=requests.post("http://cti_hk_cns00.eycyber.com:8080/reporting",data=send_out_data2)

def job_update(send_out_data,key,value):
    send_out_data[key]=value
    return send_out_data



if __name__ == '__main__':
    wechat_scrape()
