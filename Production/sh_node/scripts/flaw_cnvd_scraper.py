import requests
from lxml import etree
import mysql.connector
import requests
from selenium import webdriver
import time

def COOKIES(url):
    chrome = webdriver.Chrome()
    chrome.get(url)
    time.sleep(5)

    __jsluid = '__jsluid=' + chrome.get_cookie('__jsluid')['value'] + ';'
    bdshare_firstime = 'bdshare_firstime=' + chrome.get_cookie('bdshare_firstime')['value'] + ';'
    __jsl_clearance = '__jsl_clearance=' + chrome.get_cookie('__jsl_clearance')['value'] + ';'
    JSESSIONID = 'JSESSIONID=' + chrome.get_cookie('JSESSIONID')['value']
    
    # csrftoken='csrftoken='+ chrome.get_cookie('csrftoken')['value']+';'

    chrome.quit()
    # display.stop()

    headers = {
        'Host': 'www.cnvd.org.cn',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
        'Referer': 'http://www.cnvd.org.cn/',
        'Cache-Control': 'max-age=0',
        'Cookie': __jsluid + bdshare_firstime + __jsl_clearance + JSESSIONID 
    }
    print(__jsluid + bdshare_firstime +  __jsl_clearance + JSESSIONID )
    return headers


def get_one_page(url, headers):
    response = requests.get(url, headers=headers)
    print(response.status_code)
    return response.text


def Urlcreator(first_page, page, headers):
    url_firstPage = []
    url_page = []

    url_firstPage.append(
        "http://www.cnvd.org.cn/flaw/show/CNVD-2018-" + str(first_page)
    )


    url_page.append(url_firstPage[-1])

    for i in range(first_page + 1, page + 1):
        url_page.append(
            "http://www.cnvd.org.cn/flaw/show/CNVD-2018-" + str(i)
        )

    return url_page


def scrapper(url_page_list, headers):
    db = mysql.connector.connect(user='root',
                                 password='1234',
                                 host='127.0.0.1',
                                 database='threads'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()

    sql = 'CREATE TABLE IF NOT EXISTS `cnvd` (`CNVDid`  VARCHAR(255),`Published_time` DATE,`Level` NVARCHAR(255),\
                                                `Related_Products` NVARCHAR(255), `CVEid` NVARCHAR(255), `Des` NVARCHAR(2048),\
                                                `Links` NVARCHAR(1024), `Method` NVARCHAR(1024), \
                                                 PRIMARY KEY (CNVDid))'

    cursor.execute(sql)

    for index, url in enumerate(url_page_list):


        response = requests.get(url, headers=headers)
        html = response.content.decode('utf-8')
        selector = etree.HTML(html)
        print(response.status_code)
        print(url)
        ##        print(response.text)

        table_rows = selector.xpath('//table[@class="gg_detail"]')


        ##        print(table_rows)

        #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[1]/td[2]
        # /html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[2]/td[2]
        # /html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[3]/td[2]/text()[1]
        #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[4]/td[2]/text()
        # /html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[5]/td[2]/a
        # /html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[6]/td[2]/text()[1]
        # /html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[7]/td[2]/a
        #/html/body/div[5]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[8]/td[2]/text()[1]
        #
        #
        # descriptions = selector.xpath('//tr//td[@class ="cvesummarylong"]//text()')

        for index, row in enumerate(table_rows):

            CNVDids = row.xpath('.//tr[1]//td[2]')
            Published_times = row.xpath('.//tr[2]//td[2]')
            Levels = row.xpath('.//tr[3]/td[2]/text()')
            Related_Products =  row.xpath('.//tr[4]/td[2]/text()')
            CVEids = row.xpath('.//tr[5]/td[2]/a')
            Deses = row.xpath('.//tr[6]/td[2]/text()')
            Links = row.xpath('.//tr[7]/td[2]/a')
            Methods = row.xpath('.//tr[8]/td[2]/text()[1]')


            cells = [CNVDids[0], Published_times[0], Levels[0], Related_Products[0], CVEids[0], Deses[0],Links[0],Methods[0]]

            # for col in cells[8]:
            #     if row.xpath('.//td[6]') == None:
            #         Popularity_comment = None
            #     else:
            #         Popularity_comment = col.text

            ##            for exploit in cells[2]:
            ##                if exploit.text == None:
            ##                    num_of_exploit = None
            ##                else:
            ##                    num_of_exploit = exploit.text.strip()
            CNVDid = cells[0].text.strip()
            Published_time = cells[1].text.strip()
            ##            Level = etree.tostring(cells[2])
            Level = cells[2].strip()
            Related_Product = cells[3].strip()
            CVEid = cells[4].text.strip()
            Des = cells[5].strip()
            Link = cells[6].text.strip()
            Method = cells[7].strip()
            print(CNVDid,Published_time)

            ##            if index == 0:
            ##                print(type(description))

            sql = 'REPLACE INTO cnvd(`CNVDid`,`Published_time`,`Level`,\
                                        `Related_Products`,`CVEid`, `Des`,\
                                        `Links`, `Method`)\
                   VALUES\
                  (%s, %s, %s, %s,%s, %s, %s, %s);'

            cursor.execute(sql,
                           (CNVDid, Published_time, Level, Related_Product, CVEid, Des,Link,Method))

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
    headers = COOKIES('http://www.cnvd.org.cn/flaw/show/CNVD-2018-10550')
    url_page = Urlcreator(10550, 10560, headers)
    scrapper(url_page, headers)


if __name__ == '__main__':
    main()
