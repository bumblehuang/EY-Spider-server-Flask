#encoding: utf-8
import requests
from lxml import etree
import mysql.connector
import requests
##from selenium import webdriver
import sys
import datetime
import hashlib

def get_one_page(url):
    response = requests.get(url)
    print(response.status_code)
    print(response.text)
    return response.text

def ConnectSQL():
    db = mysql.connector.connect(user='root',
                                 password='Test20180604',
                                 host='rm-j6cx1z86d86308x6m.mysql.rds.aliyuncs.com',
                                 database='event_news'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()

    sql = 'CREATE TABLE IF NOT EXISTS `testnew` (`CVEid`  VARCHAR(255),`CWEid` VARCHAR(255) ,score NUMERIC,`news_hash` VARCHAR(255) ,\
                                                    PRIMARY KEY (news_hash))'
    cursor.execute(sql)

    return cursor, db


def Urlcreator(days):

    now = datetime.datetime.now()
    url_firstPage = []
    url_page = []

    url_firstPage.append(
        "https://xuanwulab.github.io/cn/secnews/"+str(now.strftime('%Y/%m/%d'))+"/index.html"
        )

    html = requests.get(url_firstPage[-1]).content.decode("utf-8")
    response = requests.get(url_firstPage[-1])
    print(response.status_code)
    selector = etree.HTML(html)

    # num_of_assests = selector.xpath('//div[@class="paging"]//b')
    # num = []
    # for i in num_of_assests:
    #     num.append(i.text)
    #     print(num)

    # num_of_pages = int(num[0]) // 50 + 1
    #
    # print(num_of_pages)

    
    url_page.append(url_firstPage[-1])
    
    for i in range(1,days+1):
        url_page.append(
            "https://xuanwulab.github.io/cn/secnews/"+str((now - datetime.timedelta(days = i)).strftime('%Y/%m/%d'))+"/index.html"
            )
    print(url_page)
    return url_page


def scrapper(url_page_list):
    db = mysql.connector.connect(user='root',
                                 password='Test@20180604',
                                 host='rm-j6cx1z86d86308x6m.mysql.rds.aliyuncs.com',
                                 port = '3306',
                                 database='event_news'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()

    sql = 'CREATE TABLE IF NOT EXISTS `xuanwu_hash` (`Category`  NVARCHAR(256),`Names` NVARCHAR(100),`Link` NVARCHAR(256), `news_hash` NVARCHAR(255),`Times` DATE, PRIMARY KEY (news_hash));'

    cursor.execute(sql)

    table_rows = []
    for index, url in enumerate(url_page_list):

        
        html = requests.get(url).content.decode('utf-8')
        selector = etree.HTML(html)
        response = requests.get(url)
        print(response.status_code)
        print(index)
##        print(response.text)
        now = datetime.datetime.now()
        Time = (now - datetime.timedelta(days = index)).strftime('%Y/%m/%d')
        table_rows = selector.xpath('//div[@class="singleweibotext"]')

##        print(table_rows)

        for index, row in enumerate(table_rows[:-1]):
            
            Categories = row.xpath('./p/span')
            Names = row.xpath('./p/text()')
            Links = row.xpath('./p/a' )

            


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

            for col in cells[2]:
                if row.xpath('./p/a') == None:
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

            #hash_string = str(Category) + str(Name).strip() + str(Time).strip()
            #hash_string = hash_string.strip()

            #sha1 = hashlib.sha1()
            #sha1.update(hash_string.encode("utf-8"))
            #hashvalue = sha1.hexdigest()


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
            
            hash_string =Category.encode('utf-8') + Name.encode('utf-8') + Time.encode('utf-8')

            sha1 = hashlib.sha1()
            sha1.update(hash_string)
            hashvalue = sha1.hexdigest()





            sql = 'REPLACE INTO `xuanwu_hash`(`Category` ,`Names` ,`Link` , `news_hash` ,`Times` )\
                   VALUES\
                  (%s, %s, %s, %s, %s);'

            cursor.execute(sql,
                           (Category,Name,Link,hashvalue,Time))

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
    #reload(sys)                         # 2
    #sys.setdefaultencoding('utf-8')
    url_page = Urlcreator(500)
    scrapper(url_page)
##    get_one_page('https://xuanwulab.github.io/cn/secnews/2018/05/30/index.html')


if __name__ == '__main__':
    main()

