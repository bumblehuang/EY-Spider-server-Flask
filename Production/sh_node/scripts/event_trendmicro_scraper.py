# -*- coding: utf-8 -*-
from lxml import etree
import mysql.connector
import requests
import re
import hashlib

def Urlcreator(first_page, page):
    url_page_list = []


    for i in range(first_page, page + 1):
        url_page_list.append(
            "https://blog.trendmicro.com/trendlabs-security-intelligence/page/" + str(i) +"/"
        )

    print(len(url_page_list))
    return(url_page_list)


####//*[@id="vulnerability"]/table/tbody
def scrapper(url_page_list):
    db = mysql.connector.connect(user='root',
                                 password='Test@20180604',
                                 host='rm-j6cx1z86d86308x6m.mysql.rds.aliyuncs.com',
                                 port='3306',
                                 database='event_news'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()


    sql = 'CREATE TABLE IF NOT EXISTS `trendmicro` (`title`  NVARCHAR(255),`postedon` NVARCHAR(255),`postedin` NVARCHAR(255), `author` NVARCHAR(255), \
                                                  `content` mediumtext,`tags`  NVARCHAR(255), \
                                                  PRIMARY KEY (title))'

    cursor.execute(sql)
    for index, url in enumerate(url_page_list):
        print(url)
        print(index)

        response = requests.get(url)
        response.encoding = "utf-8"
        html = response.content
        selector = etree.HTML(html.decode('utf-8'))
        print(selector)
        print(response.status_code)

        ##        print(response.text)
        #//*[@id="pageContent"]    //*[@id="pageContent"]
        #//*[@id="post-82187"]
        #标题//*[@id="post-82187"]/div[1]/div/a/h1
        #post_in  //*[@id="post-82187"]/div[3]/ul/li[1]/div[1]    //*[@id="post-82187"]/div[3]/ul/li[1]/div[1]/a
        #post_on  //*[@id="post-82187"]/div[3]/ul/li[2]/div[1]    //*[@id="post-82187"]/div[3]/ul/li[2]/div[1]/a
        #author  //*[@id="post-82187"]/div[3]/ul/li[3]/div[1]     //*[@id="post-82187"]/div[3]/ul/li[3]/div[1]/div/a
        #内容  //*[@id="post-82187"]/div[6]/p           //*[@id="post-82187"]/div[6]/p/text()
        #//*[@id="post-82187"]/div[1]/div/a/h1
        #//*[@id="post-76870"]/div[3]/ul/li[3]/div[1]/a
        #//*[@id="post-82121"]
        #//*[@id="post-76908"]/div[3]/ul/li[3]/div[1]/div/a
        try:
            table_rows = selector.xpath('//*[@id="pageContent"]/div')
        except Exception as e:
            pass

        print(len(table_rows))
        for index,row in enumerate(table_rows):

            if row.xpath('//*[@id="pageContent"]/div[' + str(index + 1) + ']/div[1]/div/a/h1') != []:
                title = row.xpath('//*[@id="pageContent"]/div[' + str(index + 1) + ']/div[1]//div/a/h1')[0].text
                
                postedon = row.xpath('//*[@id="pageContent"]/div[' + str(index + 1) + ']/div[3]/ul/li[1]/div[1]/a')[0].text
                
                postedin = row.xpath('//*[@id="pageContent"]/div[' + str(index + 1) + ']/div[3]/ul/li[2]/div[1]/a')[0].text
                
                author = row.xpath('//*[@id="pageContent"]/div[' + str(index + 1) + ']/div[3]/ul/li[3]/div[1]//a')[0].text
                
                bri_content = row.xpath('//*[@id="pageContent"]/div[' + str(index + 1) + ']//div[6]')[0].xpath('string()')
                bri_content = re.sub(r'\s+', ' ', bri_content)
                bri_content = re.sub(r'(^\s)|(\s$)', '', bri_content)
                tag = re.sub(r'.* Read More', '', bri_content)
##                content_link = row.xpath('//*[@id="pageContent"]/div[' + str(index + 1) + ']/div[3]/ul/li[3]/div[1]/div/a')[0].text

                if re.search(r'Tags:',tag):
                    bri_content = re.sub(r'\s+Read More Tags:.*', '', bri_content)
                    tag = re.sub(r'\s+Tags:\s+', '', tag)
                else:
                    bri_content = re.sub(r'\s+Read More', '', bri_content)
                    tag = 'None'

                   
                hash_string = title.encode('utf-8')+ author.encode('utf-8') + postedon.encode('utf-8')
                
                sha1 = hashlib.sha1()
                sha1.update(hash_string)
                hashvalue = sha1.hexdigest()
                source = 'trendmicro'
                                
                sql = 'REPLACE INTO event_hq(`news_title`,`news_publishedTime` ,`news_category` , `news_author` , `news_briefContent` ,`news_tags`,`news_hash`,`news_source` ) \
                               VALUES\
                              (%s, %s, %s, %s, %s ,%s, %s, %s);'

                cursor.execute(sql, (title, postedon,postedin,author,bri_content,tag, hashvalue, source))

                try:
                    db.commit()
                except:
                    # if unexecuted, rollback
                    db.rollback()

def main():
    # min=0,max=0,month=5,year=2018
    ##    cursor,db = ConnectSQL()
    #headers = COOKIES('http://www.cnvd.org.cn/flaw/list.htm?flag=true?number=%E8%AF%B7%E8%BE%93%E5%85%A5%E7%B2%BE%E7%A1%AE%E7%BC%96%E5%8F%B7&startDate=&endDate=&flag=true&field=&order=&max=20&offset=0')
    url_page = Urlcreator(1, 751)
    scrapper(url_page)


if __name__ == '__main__':
    main()

