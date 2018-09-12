#encoding: utf-8
import hashlib
import requests
import re
from lxml import etree
import mysql.connector
from datetime import datetime
#https://securosis.com/blog/P0
#url = 'https://www.coresecurity.com/blog?page=0'
#url = 'https://www.coresecurity.com/blog/introducing-access-assurance-suite-91'
#r = requests.get(url)
#print(r.status_code)
#print(r.text)

#//*[@id="node-63357"]/div/div[2]/div[2]/h3/a



def Urlcreator(firstpage,page):
    url_page_list = []
    url_page = []
    for i in range(firstpage - 1,page ):
        url_page_list.append("https://www.us-cert.gov/ncas/current-activity?page=" + str(i))
    #print(url_page_list)
    for j in url_page_list:
        #print(j)
        response = requests.get(j)
        html = response.text
        allurl = re.findall(r'<h3 class="entry-title">.*?</h3>',html)
        #print(allurl)
        for allurl_ in allurl:

            allurl_ = re.sub(r'<h3 class="entry-title">.*?<a href="','',allurl_)
            #print(allurl_)
            allurl_ = re.sub(r'">.*?</h3>', '', allurl_)
            allurl_ = allurl_.encode('utf-8')
            allurl_ = "https://www.us-cert.gov" + allurl_
            url_page.append(allurl_)
        #print(fire_page)
        #for index, row in enumerate(fire_page):
            #print(index)
            #if row.xpath('/html/body/main/div/div/div[1]/div/div/div/div/ul/div[' + str(index+ 1) + ']/h2/a/@href') != []:
                #allurl_ = row.xpath('/html/body/main/div/div/div[1]/div/div/div/div/ul/div[' + str(index+ 1) + ']/h2/a/@href')[0].strip()
                #allurl_ = "https://www.fireeye.com" + allurl_
                #print(allurl_)
                #url_page.append(allurl_)
    #print(url_page)
    print(len(url_page))
    return url_page

def scrapper(url_page):
    db = mysql.connector.connect(user='root',
                                 password='Test@20180604',
                                 host='rm-j6cx1z86d86308x6m.mysql.rds.aliyuncs.com',
                                 port='3306',
                                 database='event_news'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()


    sql = 'CREATE TABLE IF NOT EXISTS `uscert_hash`  (`news_title`  NVARCHAR(255),`news_author` NVARCHAR(255),`news_publishedTime` DATE, `news_content` mediumtext, \
                                                  `news_category` NVARCHAR(255), `news_briefContent` NVARCHAR(511),`news_source` NVARCHAR(255), \
                                                  `news_tags` NVARCHAR(255),`news_hash` NVARCHAR(255) ,`news_exploitCode` NVARCHAR(255),`news_damagedItem` NVARCHAR(255), \
                                                  `news_area` NVARCHAR(255),`news_sector` NVARCHAR(255),`news_product` NVARCHAR(255),PRIMARY KEY (news_hash))'


    cursor.execute(sql)
    for index, url in enumerate(url_page):
        #print(url)
        print(index)
        response = requests.get(url, timeout=30)
        html = response.content
        selector = etree.HTML(html)
        print(response.status_code)
###标题/html/body/main/div/div/div[1]/div/div/div/div[2]/h1/text()        //*[@id="page-title"]
#     /html/body/main/div/div/div[1]/div/div/div/div[2]/h1/text()
###时间/html/body/main/div/div/div[1]/div/div/div/div[2]/div/time       //*[@id="node-current-activity-11137"]/footer
##作者  /html/body/main/div/div/div[1]/div/div/div/div[2]/div/span[2]/a
###内容    //*[@id="node-63329"]/div/div/div/div[2]/div[2]/h3/a           //*[@id="node-current-activity-11137"]/div[2]/div/div/div
#title entrytitle
#/html/body/main/div/div/div[1]/div
        #/html/body/main/div/div/div[1]/div
#tag /html/body/main/div/div/div[1]/div/div/div/div[4]/p/small
                                                                        #  标签    //*[@id="node-63357"]/div/div/div/div[2]/div[2]/ul/li[2]/a

        #dict = {'news_title':'None','news_time':'None','news_author':'None','news_content':'None','news_content':'None','news_tags':'None'}
        #print(selector.xpath('//div[@class="title entrytitle"]/h1/text()')[0].strip())
        if selector.xpath('//*[@id="page-title"]')!= []:
            title = selector.xpath('//*[@id="page-title"]')[0].xpath('string()')
            title = re.sub(r'\s+',' ',title)
            title = title.strip()

        else:
            title = 'None'
        #print(title)
        if selector.xpath('//*[@class="submitted meta-text"]')!= []:
            time = selector.xpath('//*[@class="submitted meta-text"]')[0].xpath('string()')
            time = re.sub(r'\s+', ' ', time)
            time = re.sub(r'.*:\s+','',time)
            time = time.strip()
            time = datetime.strptime(time, '%B %d, %Y')
            time = time.strftime('%Y-%m-%d')
            
        else:
            time = 'none'
        #print(time)
        #if selector.xpath('//article[@class="entry"]/address')!= []:
            #author = selector.xpath('//article[@class="entry"]/address')[0].xpath('string()')
            #author = re.sub(r'^By\s+','',author)
         #class="par parsys" bbbbbbbbbb                                                                   b
        #else:
            #author = 'none'
        #print(author)
        
        if selector.xpath('//*[@class="field-items"]')!= []:
            content = selector.xpath('//*[@class="field-items"]')[0].xpath('string()')
            content = re.sub(r'\s+',' ',content)
            content = content.strip()
        else:
            content = 'none'
        #print(content)
        hash_string = title.encode('utf-8')  + time.encode('utf-8')

        sha1 = hashlib.sha1()
        sha1.update(hash_string)
        hashvalue = sha1.hexdigest()

        sql = 'REPLACE INTO uscert_hash(`news_title` ,`news_publishedTime` , `news_category` , \
                                                   `news_author`,`news_briefContent`,`news_tags` ,`news_source` , \
                                                  `news_content` ,`news_hash` ,`news_exploitCode` ,`news_damagedItem`,`news_area`,`news_sector`,`news_product`) \
                       VALUES\
                      (%s, %s, %s, %s, %s, %s, %s, %s ,%s, %s, %s, %s, %s ,%s);'


        cursor.execute(sql,(title,time,'','','','',url,content,hashvalue,'','','','',''))

        try:
            db.commit()
        except:
            # if unexecuted, rollback
            db.rollback()




def main():
    # min=0,max=0,month=5,year=2018
    ##    cursor,db = ConnectSQL()
    #headers = COOKIES('http://www.cnvd.org.cn/flaw/list.htm?flag=true?number=%E8%AF%B7%E8%BE%93%E5%85%A5%E7%B2%BE%E7%A1%AE%E7%BC%96%E5%8F%B7&startDate=&endDate=&flag=true&field=&order=&max=20&offset=0')
    url_page = Urlcreator(1, 30)
    #print(url_page)
    scrapper(url_page)


if __name__ == '__main__':
    main()
