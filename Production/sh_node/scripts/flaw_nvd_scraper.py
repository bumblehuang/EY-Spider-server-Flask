import requests
from lxml import etree
import csv
import mysql.connector
import requests
from selenium import webdriver
import sys
import datetime


def get_one_page(url):
    response = requests.get(url)
    print(response.status_code)
    print(response.text)
    return response.text


def ConnectSQL():
    db = mysql.connector.connect(user='root',
                                 password='Test@20180604',
                                 host='rm-j6cx1z86d86308x6m.mysql.rds.aliyuncs.com',
                                 port = '3306',
                                 database='vulnerabilities'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()

    sql = 'CREATE TABLE IF NOT EXISTS `testnew` (`CVEid`  VARCHAR(255),`CWEid` VARCHAR(255) ,score NUMERIC,\
                                                    PRIMARY KEY (CVEid))'
    cursor.execute(sql)

    return cursor, db


def Urlcreator(months):
    now = datetime.datetime.now()
    url_firstPage = []
    url_page_list = []
    url_page = []

    url_firstPage.append(
        "https://nvd.nist.gov/vuln/full-listing/" + str((now).strftime('%Y/%m')))

    url_page_list.append(url_firstPage[-1])

    # Make a month list for cvesid page
    for i in range(1, months + 1):
        url_page_list.append(
            "https://nvd.nist.gov/vuln/full-listing/" +
            str((now - datetime.timedelta(days=i * 30)).strftime('%Y/%m'))
        )
    print(url_page_list)

    # Make the complete cve pages list based on months
    for i in url_page_list:
        response = requests.get(i)
        html = response.content.decode("utf-8")

        selector = etree.HTML(html)
        cveid_list = selector.xpath('//div[@class="row"]//span[@class="col-md-2"]')
        cveids = []
        for cveid in cveid_list:
            if cveid.xpath('.//a') == []:
                cveid_ = None
            else:
                cveid_ = cveid.xpath('.//a')[0].text
            cveids.append(cveid_)
            if cveid_ != None:
                url_page.append("https://nvd.nist.gov/vuln/detail/" + str(cveid_))
    print(len(url_page))

    return url_page


def scrapper(url_page):
    db = mysql.connector.connect(user='root',
                                 password='Test@20180604',
                                 host='rm-j6cx1z86d86308x6m.mysql.rds.aliyuncs.com',
                                 port = '3306',
                                 database='vulnerabilities'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()

    sql = 'CREATE TABLE IF NOT EXISTS `nvd2` (`CVEid`  VARCHAR(100),`Des` VARCHAR(3000),`Source` VARCHAR(1000), `Modified_Date` VARCHAR(256),`Link` VARCHAR(256), \
                                                PRIMARY KEY (CVEid))'

    cursor.execute(sql)

    table_rows = []
    for index, url in enumerate(url_page):

        response = requests.get(url)
        html = response.content.decode('utf-8')
        selector = etree.HTML(html)

        print(response.status_code)
        print(index)

        if response.status_code == 200:
            # Xpath for reference
            # //*[@id="p_lt_WebPartZone1_zoneCenter_pageplaceholder_p_lt_WebPartZone1_zoneCenter_VulnerabilityDetail_VulnFormView"]/tbody/tr/td/h2/span
            # //*[@id="p_lt_WebPartZone1_zoneCenter_pageplaceholder_p_lt_WebPartZone1_zoneCenter_VulnerabilityDetail_VulnFormView"]/tbody/tr/td/div/div[1]/p[2]/span[1]
            # //*[@id="p_lt_WebPartZone1_zoneCenter_pageplaceholder_p_lt_WebPartZone1_zoneCenter_VulnerabilityDetail_VulnFormView"]/tbody/tr/td/div/div[1]/p[1]/text()
            # //*[@id="p_lt_WebPartZone1_zoneCenter_pageplaceholder_p_lt_WebPartZone1_zoneCenter_VulnerabilityDetail_VulnFormView_Vuln3CvssPanel"]/p[1]/a/span[1]
            # //*[@id="p_lt_WebPartZone1_zoneCenter_pageplaceholder_p_lt_WebPartZone1_zoneCenter_VulnerabilityDetail_VulnFormView_VulnHyperlinksPanel"]/table/tbody/tr/td[1]/a
            ##            print(url)
            CVEids = selector.xpath('//h2[@data-testid="page-header"]//span')
            Deses = selector.xpath(
                '//div[@class="col-lg-9 col-md-7 col-sm-12"]//p[@data-testid ="vuln-description"]//text()')
            Sources = selector.xpath('//div[@class="col-lg-9 col-md-7 col-sm-12"]//p[2]//span[@data-testid ="vuln-description-source"]')
            Modified_Dates = selector.xpath('//div[@class="col-lg-9 col-md-7 col-sm-12"]//p[2]//span[@data-testid ="vuln-description-last-modified"]')
            Links = selector.xpath('//td[@data-testid="vuln-hyperlinks-link-0"]//a')
            ##            print(Links)

            ##            print(CVEids,Deses,Sources,Modified_Dates)

            cells = [CVEids, Deses, Sources, Modified_Dates, Links]

            CVEid, Des, Source, Modified_Date, Link = '', [], '', '', ''

            for col in cells[0]:
                if col == []:
                    CVEid = None
                else:
                    CVEid = col.text

            for col in cells[1]:
                if col == None:
                    Des = None
                else:
                    Des = col.strip()

            for col in cells[2]:
                if col == None:
                    Source = None
                else:
                    Source = col.text

            for col in cells[3]:
                if col == None:
                    Modified_Date = None
                else:
                    Modified_Date = col.text

            for col in cells[4]:
                if col == None:
                    Link = None
                else:
                    Link = col.text


                ##            for exploit in cells[2]:
                ##                if exploit.text == None:
                ##                    num_of_exploit = None
                ##                else:
                ##                    num_of_exploit = exploit.text.strip()

                ##            Category = cells[0].text
                ##            Name = cells[1].strip().encode('utf-8')

                ##            Level = etree.tostring(cells[2])

                ##            Link = cells[2].text

                ##            if index == 0:
                ##                print(type(description))

            sql = '''INSERT INTO nvd2(`CVEid`,`Des`,`Source`,`Modified_Date`,`Link` )\
                   VALUES\
                  (%s, %s, %s, %s, %s)\
                  ON DUPLICATE KEY UPDATE\
                  Des = Des, Source = Source,Modified_Date = Modified_Date, Link = Link ;'''
            

            cursor.execute(sql,
                           (CVEid, Des, Source, Modified_Date, Link))

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
    ##    headers = COOKIES('https://www.seebug.org/vuldb/vulnerabilities?page=1')
    url_page = Urlcreator(12)
    scrapper(url_page)


##    get_one_page('https://xuanwulab.github.io/cn/secnews/2018/05/30/index.html')


if __name__ == '__main__':
    main()
