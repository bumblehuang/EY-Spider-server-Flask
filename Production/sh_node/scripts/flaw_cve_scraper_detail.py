# encoding: utf-8
import mysql.connector
import requests
from lxml import etree
import csv
import ssl


def Urlcreator():
    db = mysql.connector.connect(user='root',
                                 password='Test@20180604',
                                 host='rm-j6cx1z86d86308x6m.mysql.rds.aliyuncs.com',
                                 port='3306',
                                 database='vulnerabilities'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')
    cur = db.cursor(buffered=True)

    sql = '''SELECT vul_cveId from `cve_hash` ORDER BY vul_updateDate DESC'''

    cur.execute(sql)

    url_page = []

    for cveid in cur:
        url_page.append(
            "https://www.cvedetails.com/cve/" + str(cveid[0]) + "/"
        )
    print(url_page[:100])

    return url_page


def scrapper(url_page_list):
    db = mysql.connector.connect(user='root',
                                 password='Test@20180604',
                                 host='rm-j6cx1z86d86308x6m.mysql.rds.aliyuncs.com',
                                 port='3306',
                                 database='vulnerabilities'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()

    sql = 'CREATE TABLE IF NOT EXISTS `cvedetail3` (`ncveId`  VARCHAR(255),`cveId`  VARCHAR(256),`productType` VARCHAR(256),`vendor` NVARCHAR(255),\
                                                `effectedProduct` NVARCHAR(255), `version` NVARCHAR(255),`update` NVARCHAR(255), \
                                                `edition` NVARCHAR(255),`language` NVARCHAR(255) \
                                                ,PRIMARY KEY (ncveId))'

    cursor.execute(sql)
    for index, url in enumerate(url_page_list):
        print(url)
        print(index)

        response = requests.get(url)
        html = response.content
        selector = etree.HTML(html)
        print(response.status_code)

        ##row.xpath('//*[@id="pageContent"]/div[' + str(index + 1) + ']/div[1]//div/a/h1')[0].text
        # row.xpath('//*[@id="pageContent"]/div[' + str(index + 1) + ']/div[1]//div/a/h1')[0].text
        # //*[@id="vulnprodstable"]/tbody/tr[2]/td[2]
        # vendor：//*[@id="vulnprodstable"]/tbody/tr[2]/td[3]/a
        # product: //*[@id="vulnprodstable"]/tbody/tr[2]/td[4]/a
        # version://*[@id="vulnprodstable"]/tbody/tr[2]/td[5]
        # update://*[@id="vulnprodstable"]/tbody/tr[2]/td[6]
        # Edition: //*[@id="vulnprodstable"]/tbody/tr[2]/td[7]
        # //*[@id="cvedetails"]/h1/a
        try:
            table_rows = selector.xpath('//table[@id="vulnprodstable"]/tr')
        except Exception as e:
            pass
        # print(table_rows)
        print(len(table_rows))
        for index, row in enumerate(table_rows[1:]):
            print(index)
            cveId = row.xpath('//*[@id="cvedetails"]/h1/a')[0].text.strip()
            

            ncveId = cveId + '_' + str(index + 1)
            
            try:
                productType = row.xpath('//table[@id="vulnprodstable"]/tr[' + str(index + 2) + ']/td[2]')[
                    0].text.strip()
                
            except Exception as e:
                productType = 'None'
            try:
                vendor = row.xpath('//table[@id="vulnprodstable"]/tr[' + str(index + 2) + ']/td[3]/a')[0].text.strip()
                
            except Exception as e:
                vendor = 'None'
            try:
                product = row.xpath('//table[@id="vulnprodstable"]/tr[' + str(index + 2) + ']/td[4]/a')[0].text.strip()
                
            except Exception as e:
                product = 'None'
            try:
                version = row.xpath('//table[@id="vulnprodstable"]/tr[' + str(index + 2) + ']/td[5]')[0].text.strip()
                
            except Exception as e:
                version = 'None'
            try:
                update = row.xpath('//table[@id="vulnprodstable"]/tr[' + str(index + 2) + ']/td[6]')[0].text.strip()
                
            except Exception as e:
                update = 'None'
            try:
                edition = row.xpath('//table[@id="vulnprodstable"]/tr[' + str(index + 2) + ']/td[7]')[0].text.strip()
                
            except Exception as e:
                edition = 'None'
            try:
                language = row.xpath('//table[@id="vulnprodstable"]/tr[' + str(index + 2) + ']/td[8]')[0].text.strip()
                
            except Exception as e:
                language = 'None'

            sql = 'REPLACE INTO `cvedetail3` (`ncveId` ,`cveId`  ,`productType`,`vendor`,\
                                                    `effectedProduct` , `version` ,`update` , \
                                                    `edition` ,`language` \
                                                     ) \
                               VALUES\
                              (%s, %s, %s, %s, %s ,%s,%s, %s, %s);'

            cursor.execute(sql, (ncveId, cveId, vendor, productType, product, version, update, edition, language))

            try:
                db.commit()
            except:
                # if unexecuted, rollback
                db.rollback()


def main():
    # min=0,max=0,month=5,year=2018
    ##    cursor,db = ConnectSQL()
    # headers = COOKIES('http://www.cnvd.org.cn/flaw/list.htm?flag=true?number=%E8%AF%B7%E8%BE%93%E5%85%A5%E7%B2%BE%E7%A1%AE%E7%BC%96%E5%8F%B7&startDate=&endDate=&flag=true&field=&order=&max=20&offset=0')
    url_page = Urlcreator()
    scrapper(url_page)


if __name__ == '__main__':
    main()
