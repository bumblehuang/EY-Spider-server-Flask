#/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests
from lxml import etree
import mysql.connector
import requests
import sys
import datetime
import hk_logger
from flask import Flask, request
from flask import Response
from flask import json
from flask import Flask, redirect, url_for, request, render_template, make_response, abort, jsonify, \
    send_from_directory,redirect

import time
import re
import hashlib
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
WAITING= 'WAITING TO RUN'
RUNNING = 'RUNNING'
FINISHED = 'FINISHED'
PAUSED = 'PAUSED'
TERMINATED = 'TERMINATED'
LOCATION='HK'
logger = hk_logger.get_logger(__name__)


################################################################################################################################




def job_update(send_out_data,key,value):
    send_out_data[key]=value
    return send_out_data

def cve_Urlcreator(min,max,vendor_id,product_id,version_id,first_page, page):

    url_firstPage= []
    url_page = []


    url_firstPage.append("https://www.cvedetails.com/vulnerability-list.php?vendor_id="+str(vendor_id)+"&product_id="+str(product_id)+"&version_id="+str(version_id)+"&page="+str(first_page)+"&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0\
        &opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin="+str(min)+"&cvssscoremax="+str(max)+"&year=0&month=0&cweid=0&order=1&trc=101161&sha=3cf9994d68386594f1283fc226cf51dad5fe72b8"
                         )


    
    html = requests.get(url_firstPage[-1]).content.decode("utf-8")
    selector = etree.HTML(html)

    num_of_assests = selector.xpath('//div[@class="paging"]//b')
    num = []
    for i in num_of_assests:
        num.append(i.text)
        print(num)

    num_of_pages = int(num[0])//50 + 1

    print(num_of_pages)

    url_page.append(url_firstPage[-1])

    for i in range(first_page,page+1):
        url_page.append("https://www.cvedetails.com/vulnerability-list.php?vendor_id="+str(vendor_id)+"&product_id="+str(product_id)+"&version_id="+str(version_id)+"&page="+str(i)+"&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0\
        &opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin="+str(min)+"&cvssscoremax="+str(max)+ "&year=0&month=0&cweid=0&order=1&trc=101161&sha=3cf9994d68386594f1283fc226cf51dad5fe72b8"
                        )

    return url_page

def cve_scrapper(url_page_list,job_id,created_time,task_id):
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
    send_out_data['created_time']=datetime.datetime.strptime(created_time,"%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
    send_out_data['start_time']=start_time.strftime("%Y-%m-%d %H:%M:%S")
    send_out_data['lasted_time']=lasted_time
    send_out_data['status']=status
    send_out_data['end_time']=end_time
    send_out_data['location']=location
    send_out_data['percentage']=percentage
    send_out_data['unsuccessful_count']=unsuccessful_count
    send_out_data['task_id']=task_id
    for index, url in enumerate(url_page_list):
        data_list=[]
        html = requests.get(url).content.decode("utf-8")
        selector = etree.HTML(html)
        print(index)
        
        table_rows = selector.xpath('//tr[@class ="srrowns"]')
        table_des = selector.xpath('//tr//td[@class ="cvesummarylong"]//text()')
        logger.debug('===============this is the start of the scrapy task ==============')
        logger.debug(index)
        logger.debug('===============this is the start of the scrapy task ==============')
        
        descriptions = selector.xpath('//tr//td[@class ="cvesummarylong"]//text()')
        
        for index,(row, des) in enumerate(zip(table_rows, table_des)):

            CWEid = None
            num_of_exploit = None
            CVEids = row.xpath('.//td[2]//a')
            CWEids = row.xpath('.//td[3]//a')
            num_of_exploits = row.xpath('.//td[4]//a')
            types = row.xpath('.//td[5]')
            Publish_Dates = row.xpath('.//td[6]')
            Update_Dates = row.xpath('.//td[7]')
            scores = row.xpath('.//td[8]//div')
            Access_Levels = row.xpath('.//td[9]')
            Accesses =row.xpath('.//td[10]')
            Complexities =row.xpath('.//td[11]')
            Authetications = row.xpath('.//td[12]')
            Confs =row.xpath('.//td[13]')
            Integs =row.xpath('.//td[14]')
            Avails =row.xpath('.//td[15]')

            cells = [CVEids[0],CWEids,num_of_exploits,types[0],Publish_Dates[0],Update_Dates[0],scores[0],Access_Levels[0],Accesses[0]
            ,Complexities[0],Authetications[0],Confs[0],Integs[0],Avails[0],des]

            for col in cells[1]:
                if row.xpath('.//td[3]//a') == None:
                    CWEid = None
                else:
                    CWEid = col.text
                    
            for exploit in cells[2]:
                if exploit.text == None:
                    num_of_exploit = None
                else:
                    num_of_exploit = exploit.text.strip()
            CVEid = cells[0].text
            type_ = cells[3].text
            Publish_Date = cells[4].text
            Update_Date = cells[5].text
            score = cells[6].text
            Access_Level = cells[7].text
            Access = cells[8].text
            Complexity =cells[9].text
            Authetication = cells[10].text
            Conf =cells[11].text
            Integ =cells[12].text
            Avail =cells[13].text
            description = cells[14].encode('utf-8').strip()
             
            hash_string = str(CVEid) + str(CWEid).strip() + str(num_of_exploit).strip() + str(type_).strip() + str(Publish_Date) + str(Update_Date) + str(score) 
            hash_string = hash_string.strip()
            
            sha1 = hashlib.sha1()
            sha1.update(unicode(hash_string,"utf-8"))
            hashvalue = sha1.hexdigest()
            


            sql = '''REPLACE INTO cve_hash (vul_cveId, vul_cweId, vul_numOfExploits, vul_type, vul_publishedDate, vul_updateDate, vul_score, vul_accessLevel,vul_access,\
            vul_complexity, vul_authentication,vul_conf,vul_integ,vul_avail,vul_des,vul_hash)\
                   VALUES\
                  (%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s)'''
            
            bsend_out_data={}
            bsend_out_data['vul_cveId']=CVEid
            bsend_out_data['vul_cweId']=CWEid
            bsend_out_data['vul_numOfExploits']=num_of_exploit
            bsend_out_data['vul_type']=type_
            bsend_out_data['vul_publishedDate']=Publish_Date
            bsend_out_data['vul_updateDate']=Update_Date
            bsend_out_data['vul_score']=score
            bsend_out_data['vul_accessLevel']=Access_Level
            bsend_out_data['vul_access']=Access
            bsend_out_data['vul_complexity']=Complexity
            bsend_out_data['vul_authentication']=Authetication
            bsend_out_data['vul_conf']=Conf
            bsend_out_data['vul_integ']=Integ
            bsend_out_data['vul_avail']=Avail
            bsend_out_data['vul_des']=description
            bsend_out_data['vul_hash']=hashvalue
            data_list.append(bsend_out_data)
        headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
        receive1=requests.post("http://xxxx:8080/cve_data",data=json.dumps(data_list),headers=headers)
        logger.debug(receive1.status_code)
        logger.debug('sending heartbeat reporting job information to the console.......')
        suceess_count+=1
        percentage = float(suceess_count) / total_length
        send_out_data= job_update(send_out_data,'percentage',percentage)
        logger.debug('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        logger.debug(suceess_count)
        logger.debug(total_length)
        logger.debug(send_out_data)
        logger.debug('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        receive2=requests.post("http://xxxx:8080/reporting",data=send_out_data)
        logger.debug(receive2.status_code)
        logger.debug('end of the loop..........')
    logger.debug('###################we have sent the email and the status is #############')
    percentage = float(suceess_count) / total_length
    logger.debug(suceess_count)
    logger.debug('===============this is the end of the scrapy task ==============')
    end_time = datetime.datetime.now()
    logger.debug(end_time)
    logger.debug('===============this is the end of the scrapy task ==============')
    lasted_time = end_time - start_time
    status = FINISHED
    unsuccessful_count = total_length - suceess_count
    send_out_data['lasted_time']=lasted_time
    send_out_data['status']=status
    send_out_data['end_time']=end_time.strftime("%Y-%m-%d %H:%M:%S")
    send_out_data['location']=location
    send_out_data['percentage']=percentage
    send_out_data['unsuccessful_count']=unsuccessful_count
    receive2=requests.post("http://xxxx:8080/reporting",data=send_out_data)
    logger.debug(receive2.status_code)

################################### Hades Specail Area #########################################

def cisco_Urlcreator(first_page,page,job_id,created_time,task_id):
    url_page_list = []
    url_page = []
    for i in range(first_page ,page+1 ):
        url_page_list.append("https://blogs.cisco.com/security/talos/page/" + str(i))
    print(url_page_list)
    for j in url_page_list:
        response = requests.get(j)
        html = response.text
        print(response.status_code)
        allurl = re.findall(r'<h2><a href = ".*?</h2>',html)
        for allurl_ in allurl:
            allurl_ = re.sub(r'<h2><a href = "','',allurl_)
            allurl_ = re.sub(r'"">.*?</h2>', '', allurl_)
            allurl_ = allurl_.encode('utf-8')
            url_page.append(allurl_)
    print(len(url_page))
    return url_page

def cisco_scrapper(url_page_list,job_id,created_time,task_id):
    total_length = len(url_page_list)
    suceess_count=0 
    unsuccessful_count=0
    data_list=[]
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

    for index, url in enumerate(url_page_list):
        print(url)
        print(index)
        response = requests.get(url)
        html_text = response.text
        html = response.content
        selector = etree.HTML(html)
        print(response.status_code)
        if selector.xpath('//*[@class="kindle_title title"]')!= []:
            title = selector.xpath('//*[@class="kindle_title title"]')[0].xpath('string()')
            title = re.sub(r'\s+',' ',title).strip()

        else:
            title = 'None'
        #print(title)
        if selector.xpath('//*[@id="post_info"]/div[2]/text()')!= []:
            time = selector.xpath('//*[@id="post_info"]/div[2]/text()')[0]
            #time = re.sub(r'\s+', '', time)

            time = time.strip()
            comment = re.findall(r'- (\d+)\s+', time)[0]
            time = re.findall(r'-\s+(.*?)\s+-', time)[0]
            time = datetime.datetime.strptime(time, '%B %d, %Y')
            time = time.strftime('%Y-%m-%d')
        else:
            time = 'none'
        #print(time)
        #print(comment)
        if selector.xpath('//*[@id="post_info"]/div[2]/a')!= []:
            author = selector.xpath('//*[@id="post_info"]/div[2]/a')[0].xpath('string()').strip()
            author = re.sub(r'\s+','',author)
            #author = re.sub(r'By\s+','',author)
         #class="par parsys" bbbbbbbbbb                                                                   b
        else:
            author = 'none'
        #print(author)
        #     //*[@id="article_post"]
        if selector.xpath('//*[@id="article_post"]')!= []:
            content = selector.xpath('//*[@id="article_post"]')[0].xpath('string()')
            content = re.sub(r'\s+',' ',content)
            content = re.sub(r'.*?Comments','',content)
            content = re.sub(r'Read More.*','',content)
            content = content.strip()


        else:
            content = 'none'
        tags = re.findall(r'<ul class = "tagged">.*?</ul>',html_text)
        ##print(tags)
        if tags != []:
            
            tags = re.sub(r'<.*?>',' ',tags[0])
            tags = tags.strip()
            tags = re.sub(r'\s+',';',tags)
        else:
            tags = 'None'
        hash_string = title.encode('utf-8') + author.encode('utf-8') + time.encode('utf-8')

        sha1 = hashlib.sha1()
        sha1.update(hash_string)
        hashvalue = sha1.hexdigest()

        dic = {}

        dic['news_title'] = title
        dic['news_publishedTime'] = time
        dic['news_category'] = ''
        dic['news_author'] = author
        dic['news_briefContent'] = content
        dic['news_tags'] = tags
        dic['news_source'] = ''
        dic['news_content'] = ''
        dic['news_hash'] = hashvalue
        dic['news_exploitCode'] = ''
        dic['news_damagedItem'] = ''
        dic['news_area'] = ''
        dic['news_sector'] = ''
        dic['news_product'] = ''
        dic['news_link'] = url

        data_list.append(dic)
        headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
        receive1=requests.post("http://xxxx:8080/cisco_data",data=json.dumps(data_list),headers=headers)
        suceess_count+=1
        percentage = float(suceess_count) / total_length
        send_out_data= job_update(send_out_data,'percentage',percentage)
        if index % 11 ==0:## heartbeat sending reporting for the job status......
            receive2=requests.post("http://xxxx:8080/reporting",data=send_out_data)
    percentage = float(suceess_count) / total_length
    end_time = datetime.datetime.now()
    lasted_time = end_time - start_time
    send_out_data= job_update(send_out_data,'end_time',end_time.strftime("%Y-%m-%d %H:%M:%S"))
    send_out_data= job_update(send_out_data,'lasted_time',lasted_time)
    send_out_data= job_update(send_out_data,'status',FINISHED)
    send_out_data= job_update(send_out_data,'percentage',percentage)
    receive3=requests.post("http://xxxx:8080/reporting",data=send_out_data)

###infosecinstitute######
def infosecinstitute_Urlcreator(url, page):
    url_page_list = []
    url_page = []
    for i in range(1, page+1):
        url_page_list.append(url + str(i) +'/')
    print(url_page_list)

    for j in url_page_list:
        response = requests.get(j)
        print(response.status_code)

        html = response.content.decode("utf-8")
        selector = etree.HTML(html)
        tc_list = selector.xpath('//*[@class="posts all"]/li')
        for inde, row in enumerate(tc_list):
            if row.xpath('.//a/@href') != []:
                row_page = row.xpath('.//a/@href')[0].strip()
                url_page.append(row_page)
    print(len(url_page))
    return url_page


def infosecinstitute_scrapper(url):
    response = requests.get(url)
    html_text = response.text
    html = response.content
    selector = etree.HTML(html)
    print(response.status_code)
    if selector.xpath('//header/h1') != []:
        title = selector.xpath('//header/h1')[0].xpath('string()')
        title = re.sub(r'\s+', ' ', title).strip()

    else:
        title = ''
    if selector.xpath('//*[@class="meta"]') != []:
        try:
            category_list = selector.xpath('//*[@class="meta"]')[0].xpath('string()').strip()
            category_list = re.sub(r'\s+', ' ', category_list).encode('utf-8').strip()
            print(category_list)
            category = re.findall(r'Posted in(.*?)on',category_list)[0].strip()
            #time = re.sub(r'发布时间：', '', time)
            time = re.findall(r'on(.*)',category_list)[0].strip()
            time = datetime.datetime.strptime(time, '%B %d, %Y')
            time = time.strftime('%Y-%m-%d')
            #print(category)
            #print(time)
            print('***************')
        except Exception as e:
            time = ''
            category = ''
    else:
        category = ''
        time = ''
    #print(category)
    #print(time)
    #/html/body/main/section[2]/div/div[1]/section/div[2]/h5/a

    if selector.xpath('//*[@class="name"]/h5/a') != []:
        author = selector.xpath('//*[@class="name"]/h5/a')[0].xpath('string()').strip()
        author = re.sub(r'\s+', '', author).encode('utf-8')
        #time = re.sub(r'发布时间：', '', time)


    else:
        author = ''
    print(author)
    if selector.xpath('//*[@class="post-content"]') != []:
        content = selector.xpath('//*[@class="post-content"]')[0].xpath('string()')
        content = re.sub(r'\s+', ' ', content)

        content = content.strip()


    else:
        content = ''
    # print(content)
    author = ''
    hash_string = title.encode('utf-8') + author.encode('utf-8') + time.encode('utf-8')

    sha1 = hashlib.sha1()
    sha1.update(hash_string)
    hashvalue = sha1.hexdigest()
    dic = {}

    dic['news_title'] = title
    dic['news_publishedTime'] = time
    dic['news_category'] = category
    dic['news_author'] = author
    dic['news_briefContent'] = ''
    dic['news_tags'] = ''
    dic['news_source'] = ''
    dic['news_content'] = content
    dic['news_hash'] = hashvalue
    dic['news_exploitCode'] = ''
    dic['news_damagedItem'] = ''
    dic['news_area'] = ''
    dic['news_sector'] = ''
    dic['news_product'] = ''
    dic['news_link'] = url
    return dic




def infosecinstitute(job_id,created_time,task_id):
    url = 'https://resources.infosecinstitute.com/page/'
    url_page = infosecinstitute_Urlcreator(url, 5)

    #print(url_page)
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
        dic = infosecinstitute_scrapper(url)
        receive1=requests.post("http://xxxx:8080/infosecinstitute_data",data=json.dumps(dic))##,headers=headers
        suceess_count+=1
        percentage = float(suceess_count) / total_length

        send_out_data= job_update(send_out_data,'percentage',percentage)
        if index % 14 ==0:
            receive666=requests.post("http://xxxx:8080/reporting",data=send_out_data)
    percentage = float(suceess_count) / total_length
    send_out_data= job_update(send_out_data,'percentage',percentage)
    send_out_data= job_update(send_out_data,'status',RUNNING)
    send_out_data= job_update(send_out_data,'location',LOCATION)
    percentage = float(suceess_count) / total_length
    end_time = datetime.datetime.now()
    lasted_time = end_time - start_time
    send_out_data= job_update(send_out_data,'end_time',end_time.strftime("%Y-%m-%d %H:%M:%S"))
    send_out_data= job_update(send_out_data,'lasted_time',lasted_time)
    send_out_data= job_update(send_out_data,'status',FINISHED)
    send_out_data= job_update(send_out_data,'percentage',percentage)
    receive3=requests.post("http://xxxx:8080/reporting",data=send_out_data)

def trendmicro_Urlcreator(first_page, page):
    url_page_list = []


    for i in range(first_page, page + 1):
        url_page_list.append(
            "https://blog.trendmicro.com/trendlabs-security-intelligence/page/" + str(i) +"/"
        )
    print(url_page_list)
    print(len(url_page_list))
    return(url_page_list)


####//*[@id="vulnerability"]/table/tbody
def trendmicro_scrapper(url_page_list,job_id,created_time,task_id):
    total_length = len(url_page_list)
    suceess_count=0 
    unsuccessful_count=0
    data_list=[]
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

    for index, url in enumerate(url_page_list):
        print(url)
        print(index)
        response = requests.get(url)
        html = response.content
        selector = etree.HTML(html)
        print(response.status_code)
        try:
            table_rows = selector.xpath('//*[@id="pageContent"]/div')
        except Exception as e:
            pass
        #print(table_rows)
        #print(len(table_rows))
        data_list=[]
        for index,row in enumerate(table_rows):
            #print(index)
            if row.xpath('//*[@id="pageContent"]/div[' + str(index + 1) + ']/div[1]/div/a/h1') != []:
                title = row.xpath('//*[@id="pageContent"]/div[' + str(index + 1) + ']/div[1]//div/a/h1')[0].text
                #print(title)
                link = row.xpath('//*[@id="pageContent"]/div[' + str(index + 1) + ']/div[1]//div/a/@href')[0].strip()
                #print(link)
                time = row.xpath('//*[@id="pageContent"]/div[' + str(index + 1) + ']/div[3]/ul/li[1]/div[1]/a')[0].text
                time = datetime.datetime.strptime(time, '%B %d, %Y')
                time = time.strftime('%Y-%m-%d')
                #print(time)
                postedin = row.xpath('//*[@id="pageContent"]/div[' + str(index + 1) + ']/div[3]/ul/li[2]//a')[0].text
                #print(postedin)
                author = row.xpath('//*[@id="pageContent"]/div[' + str(index + 1) + ']/div[3]/ul/li[3]//a')[0].text
                #print(author)
                content = row.xpath('//*[@id="pageContent"]/div[' + str(index + 1) + ']//div[6]')[0].xpath('string()')
                content = re.sub(r'\s+', ' ', content)
                content = re.sub(r'(^\s)|(\s$)', '', content)
                tag = re.sub(r'.* Read More', '', content)
                if re.search(r'Tags:',tag):
                    content = re.sub(r'\s+Read More Tags:.*', '', content)
                    tag = re.sub(r'\s+Tags:\s+', '', tag)
                else:
                    content = re.sub(r'\s+Read More', '', content)
                    tag = 'None'
                hash_string = title.encode('utf-8') + author.encode('utf-8') + time.encode('utf-8')

                sha1 = hashlib.sha1()
                sha1.update(hash_string)
                hashvalue = sha1.hexdigest()
                dic={}
                dic['news_title']=title
                dic['news_publishedTime']=time
                dic['news_category']=postedin
                dic['news_author']=author
                dic['news_briefContent']=content
                dic['news_tags']=tag
                dic['news_source']=None
                dic['news_content']=None
                dic['news_hash']=hashvalue
                dic['news_exploitCode']=None
                dic['news_damagedItem']=None
                dic['news_area']=None
                dic['news_sector']=None
                dic['news_product']=None
                dic['news_link']=link
                data_list.append(dic)
        headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
        receive1=requests.post("http://xxxx:8080/trendmicro_data",data=json.dumps(data_list),headers=headers)
        suceess_count+=1
        percentage = float(suceess_count) / total_length
        send_out_data= job_update(send_out_data,'percentage',percentage)
        receive2=requests.post("http://xxxx:8080/reporting",data=send_out_data)
    percentage = float(suceess_count) / total_length
    end_time = datetime.datetime.now()
    lasted_time = end_time - start_time
    send_out_data= job_update(send_out_data,'end_time',end_time.strftime("%Y-%m-%d %H:%M:%S"))
    send_out_data= job_update(send_out_data,'lasted_time',lasted_time)
    send_out_data= job_update(send_out_data,'status',FINISHED)
    send_out_data= job_update(send_out_data,'percentage',percentage)
    receive3=requests.post("http://xxxx:8080/reporting",data=send_out_data)

################################### Hades Specail Area #########################################

