import requests
from lxml import etree
import mysql.connector
import requests
from selenium import webdriver
import time
import logging
import re



def Urlcreator(year_start, year_end):
    url_firstPage = []
    url_page_list = []
    url_page = []

    url_firstPage.append(
        "https://www.us-cert.gov/ncas/bulletins/" + str(year_start)
    )

    url_page_list.append(url_firstPage[-1])

    for i in range(year_start + 1, year_end + 1):
        url_page_list.append(
            "https://www.us-cert.gov/ncas/bulletins/" + str(i)
        )

    print(url_page_list)

    for i in url_page_list:

        response = requests.get(i)
        html = response.content.decode("utf-8")
        selector = etree.HTML(html)
        # xpath:
        #//*[@id="block-system-main"]/div/div/div/div[2]/div/ul/li[34]/span[1]

        sb_list = selector.xpath('//div[@class="item-list"]//li')
        # print(sb_list)
        sbids = []
        for sbid in sb_list:
            #if there is nothing under this path
            if sbid.xpath('./span[@class="document_id"]') == []:
                sbid_ = None
            #else, we collect the sb number, deleting the space and semicolon at the same time
            else:
                sbid_ = sbid.xpath('./span[@class="document_id"]')[0].text.strip().rstrip(" :")
            sbids.append(sbid_)
            if sbid_ != None:
                url_page.append("https://www.us-cert.gov/ncas/bulletins/" + str(sbid_))

    print(len(url_page))
    return url_page


def scrapper(url_page_list):
    db = mysql.connector.connect(user='root',
                                 password='Test@20180604',
                                 host='rm-j6cx1z86d86308x6m.mysql.rds.aliyuncs.com',
                                 port = '3306',
                                 database='vulnerabilities'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()

    sql = 'CREATE TABLE IF NOT EXISTS `uscert12` (`VendorProduct` VARCHAR(200),`Description` VARCHAR(3000),`Published_Date` DATE, `CVSS_Score` VARCHAR(200), \
                                                `Source` VARCHAR(500),`BreifDes` VARCHAR(200),PRIMARY KEY (VendorProduct,Published_Date,BreifDes) )'

    cursor.execute(sql)

    table_rows = []
    trace_index = 0
    for index, url in enumerate(url_page_list):

        html = requests.get(url).content.decode('utf-8')
        selector = etree.HTML(html)
        response = requests.get(url)
        print(response.status_code)
        print(index)

        table_rows = selector.xpath('//div[@id="high_v"]//tr')+\
                     selector.xpath('//div[@id="medium_v"]//tr')+\
                     selector.xpath('//div[@id="low_v"]//tr')+\
                     selector.xpath('//div[@id="snya_v"]//tr')
        print(len(table_rows))

        for index, row in enumerate(table_rows):
            trace_index += 1
            print(trace_index)
#//*[@id="table_severity_not_yet_assigned"]/tbody/tr[1]/td[1]/text()[1]
#//*[@id="table_severity_not_yet_assigned"]/tbody/tr[1]/td[2]/text()
#//*[@id="table_severity_not_yet_assigned"]/tbody/tr[1]/td[3]
#//*[@id="table_severity_not_yet_assigned"]/tbody/tr[1]/td[4]
#//*[@id="table_severity_not_yet_assigned"]/tbody/tr[1]/td[5]
#//*[@id="table_severity_not_yet_assigned"]/tbody/tr[1]/td[5]/a[1]
#//*[@id="table_severity_not_yet_assigned"]/tbody/tr[1]/td[5]/a[2]
#source: //*[@id="low_v"]/table/tbody/tr[4]/td[5]/a[1]
#//*[@id="medium_v"]/table/tbody/tr[13]/td[5]/a[3]/text()
            try:
                Vendors = row.xpath('./td[1]/text()[1]')
                Deses = row.xpath('./td[2]/text()')
                Dates = row.xpath('./td[3]')
                Scores = row.xpath('./td[4]/a')
            except Exception as e:
                print(e)

            try:
                Source = ''
                for index,i in enumerate(row.xpath('./td[5]/a/@href')):
                    Source += u"%s; "%(i)
                
                
            except Exception as e:
                print(e)
            
            cells = [Vendors, Deses, Dates, Scores]
            
            #make a empty list of value
            Vendor,Des,Date,Score,Brief_Des = '','','','',''
            value = [Vendor, Des, Date, Score]

            #if the type of ele is string, just strip it; else select text from it
            #update the elements in value list
            for index,ele in enumerate(cells):
                if ele == []:
                    value[index] = None
                else:
                    try:
                        value[index] = ele[0].strip()
                    except AttributeError as e:
                        value[index] = ele[0].text


            if all(i is None for i in value) or value[0] == None or value[1] == None:
                print('gg')
            else:
                Brief_Des = value[1][:200]             
                sql = '''REPLACE INTO uscert11(`VendorProduct`,`Description`,`Published_Date`, `CVSS_Score`,`Source`,`BreifDes`)\
                        VALUES\
                         (%s, %s, %s, %s, %s, %s);'''

                cursor.execute(sql,(value[0], value[1], value[2], value[3], Source, Brief_Des))

                try:
                    db.commit()
                except:
                    db.rollback()


def main():
    url_page = Urlcreator(2015,2018)
    scrapper(url_page[:2])

if __name__ == '__main__':
    main()
