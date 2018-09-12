import requests
from lxml import etree
import csv

import mysql.connector
import requests
from selenium import webdriver
import time

def COOKIES(url):
    chrome = webdriver.Chrome()
    chrome.get(url)
    time.sleep(5)
    cookies = ""
    for cookie in chrome.get_cookies():
        cookies += u"%s=%s; "%(cookie["name"], cookie["value"])
    # __jsluid = '__jsluid=' + chrome.get_cookie('__jsluid')['value'] + ';'
    # __jsl_clearance = '__jsl_clearance=' + chrome.get_cookie('__jsl_clearance')['value'] + ';'
    # csrftoken='csrftoken='+ chrome.get_cookie('csrftoken')['value']+';'
   
    headers = {
        'authority': 'www.cnnvd.org.cn',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Cookie': cookies
        }
    response = requests.get(url, headers=headers)
    print(response.status_code)
    print(cookies)
    chrome.quit()
    return headers


def get_one_page(url, headers):
    response = requests.get(url, headers=headers)
    print(response.status_code)
    return response.text


def Urlcreator(first_page, page, headers):
    url_firstPage = []
    url_page = []

    url_firstPage.append(
        'http://www.cnnvd.org.cn/web/vulnerability/querylist.tag?pageno='+str(first_page)+ '&repairLd=' 
    )


    url_page.append(url_firstPage[-1])

    for i in range(first_page + 1, page + 1):
        url_page.append(
            'http://www.cnnvd.org.cn/web/vulnerability/querylist.tag?pageno='+str(i)+ '&repairLd=' 
        )

    return url_page


def scrapper(url_page_list, headers):
    db = mysql.connector.connect(user='root',
                                 password='Test@20180604',
                                 host='rm-j6cx1z86d86308x6m.mysql.rds.aliyuncs.com',
                                 database='vulnerabilities'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()

    sql = 'CREATE TABLE IF NOT EXISTS `cnnvd1` (`CNNVDid`  VARCHAR(255),`Names`  NVARCHAR(500), `Times` Date, `Levels` NVARCHAR(500),`Links` VARCHAR(500),\
                                                 PRIMARY KEY (CNNVDid))'

    cursor.execute(sql)

    for index, url in enumerate(url_page_list):


        response = requests.get(url, headers=headers)
        html = response.content.decode('utf-8')
        selector = etree.HTML(html)
        print(response.status_code)
        print(index)
        ##        print(response.text)

        table_rows = selector.xpath('//div[@class="list_list"]//li')


        ##        print(table_rows)

        #//*[@id="vulner_0"]/div[1]/p/a
        # //*[@id="vulner_0"]/div[2]/a
        #/html/body/div[4]/div/div[1]/div/div[2]/ul/li[2]/div[2]/text()
        #/html/body/div[4]/div/div[1]/div/div[2]/ul/li[2]/div[2]/img


        for index, row in enumerate(table_rows):

            CNNVDids = row.xpath('.//div[1]/p/a')
            Names = row.xpath('.//div[1]/a')
            Published_times = row.xpath('.//div[@class="fr"]/text()')
            Levels =  row.xpath('.//div[2]/img/@title')

            cells = [CNNVDids[0], Names[0], Published_times,Levels[0]]

            for col in cells[2]:
                 if row.xpath('.//div[@class="fr"]/text()') == None:
                     Published_time = None
                 else:
                     Published_time = col.strip()

            ##            for exploit in cells[2]:
            ##                if exploit.text == None:
            ##                    num_of_exploit = None
            ##                else:
            ##                    num_of_exploit = exploit.text.strip()
            CNNVDid = cells[0].text.strip()
##            Published_time = cells[2].text.strip()
            ##            Level = etree.tostring(cells[2])
            Level = cells[3].strip()
            Name = cells[1].text.strip()
            Link = 'http://www.cnnvd.org.cn/web/xxk/ldxqById.tag?CNNVD='+CNNVDid


            ##            if index == 0:
            ##                print(type(description))

            sql = 'REPLACE INTO cnnvd1(`CNNVDid`,`Names`, `Times`, `Levels`,`Links` )\
                   VALUES\
                  (%s, %s, %s, %s, %s);'

            cursor.execute(sql,
                           (CNNVDid, Name, Published_time, Level, Link))

            try:
                db.commit()
            except:
                # if unexecuted, rollback
                db.rollback()


## Code below is for save file locally
##            cellTexts.insert(8, score[index].text)
##            remove_list = [10,1,2]
##            for i in remove_list:
##                cellTexts.remove(cellTexts[i])

##            writer.writerow(cellTexts)


def main():
    # min=0,max=0,month=5,year=2018
    ##    cursor,db = ConnectSQL()
    headers = COOKIES('http://www.cnnvd.org.cn/web/vulnerability/querylist.tag?pageno=1700&repairLd=')
    url_page = Urlcreator(1700, 2000, headers)
    scrapper(url_page, headers)
    time.sleep(2)


if __name__ == '__main__':
    main()
