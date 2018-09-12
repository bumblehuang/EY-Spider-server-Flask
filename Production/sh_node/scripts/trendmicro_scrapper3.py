# encoding: utf-8
from lxml import etree
import mysql.connector
import requests
import hashlib
from datetime import datetime
import re
def Urlcreator(first_page, page):
    url_page_list = []


    for i in range(first_page, page + 1):
        url_page_list.append(
            "https://blog.trendmicro.com/trendlabs-security-intelligence/page/" + str(i) +"/"
        )
    print(url_page_list)
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


    #sql = 'CREATE TABLE IF NOT EXISTS `trendmicro1` (`title`  NVARCHAR(255),`postedon` NVARCHAR(255),`postedin` NVARCHAR(255), `author` NVARCHAR(255), \
    #                                              `content` NVARCHAR(3000),`tags`  NVARCHAR(255), \
    #                                              PRIMARY KEY (title))'
    sql = 'CREATE TABLE IF NOT EXISTS `trendmicro_hash1`  (`news_title`  NVARCHAR(255),`news_author` NVARCHAR(255),`news_publishedTime` DATE, `news_content` mediumtext, \
                                                  `news_category` NVARCHAR(255), `news_briefContent` NVARCHAR(511),`news_source` NVARCHAR(255), \
                                                  `news_tags` NVARCHAR(255),`news_hash` NVARCHAR(255) ,`news_exploitCode` NVARCHAR(255),`news_damagedItem` NVARCHAR(255), \
                                                  `news_area` NVARCHAR(255),`news_sector` NVARCHAR(255),`news_product` NVARCHAR(255),`news_link` NVARCHAR(255),PRIMARY KEY (news_hash))'

    cursor.execute(sql)
    for index, url in enumerate(url_page_list):
        print(url)
        print(index)

        response = requests.get(url)
        html = response.content
        selector = etree.HTML(html)
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
        #//*[@id="post-82121"]
        try:
            table_rows = selector.xpath('//*[@id="pageContent"]/div')
        except Exception as e:
            pass
        #print(table_rows)
        #print(len(table_rows))
        for index,row in enumerate(table_rows):
            #print(index)
            if row.xpath('//*[@id="pageContent"]/div[' + str(index + 1) + ']/div[1]/div/a/h1') != []:
                title = row.xpath('//*[@id="pageContent"]/div[' + str(index + 1) + ']/div[1]//div/a/h1')[0].text
                #print(title)
                link = row.xpath('//*[@id="pageContent"]/div[' + str(index + 1) + ']/div[1]//div/a/@href')[0].strip()
                #print(link)
                time = row.xpath('//*[@id="pageContent"]/div[' + str(index + 1) + ']/div[3]/ul/li[1]/div[1]/a')[0].text
                time = datetime.strptime(time, '%B %d, %Y')
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




                #print(content)
                #print(tag)
                hash_string = title.encode('utf-8') + author.encode('utf-8') + time.encode('utf-8')

                sha1 = hashlib.sha1()
                sha1.update(hash_string)
                hashvalue = sha1.hexdigest()
               # sql = 'REPLACE INTO trendmicro1(`title`,`postedon` ,`postedin` , `author` , `content` ,tags ) \
               #                VALUES\
                #              (%s, %s, %s, %s, %s ,%s);'
                dic = {}
                dic['news_title'] = title 
                dic['news_publishedTime'] = time
                dic['news_category'] = postedin
                dic['news_author'] = author
                dic['news_briefContent'] = content
                dic['news_tags'] = tag
                dic['news_source'] = ''
                dic['news_content']= ''
                dic['news_hash'] = hashvalue
                dic['news_exploitCode'] = ''
                dic['news_damagedItem'] = ''
                dic['news_area'] = ''
                dic['news_sector'] = ''
                dic['news_product'] = ''
                dic['news_link'] = link
             



                #cursor.execute(sql, (title, postedon,postedin,author,content,tag))
                sql = 'REPLACE INTO trendmicro_hash1(`news_title` ,`news_publishedTime` , `news_category` , \
                                                           `news_author`,`news_briefContent`,`news_tags` ,`news_source` , \
                                                          `news_content` ,`news_hash` ,`news_exploitCode` ,`news_damagedItem`,`news_area`,`news_sector`,`news_product`,`news_link`) \
                               VALUES\
                              (%s, %s, %s, %s, %s, %s, %s, %s ,%s, %s, %s, %s, %s ,%s,%s);'

                cursor.execute(sql,
                               (title, time, postedin, author, content, tag, '', '', hashvalue, '', '', '', '', '',link))

                try:
                    db.commit()
                except:
                    # if unexecuted, rollback
                    db.rollback()

def main():
    # min=0,max=0,month=5,year=2018
    ##    cursor,db = ConnectSQL()
    #headers = COOKIES('http://www.cnvd.org.cn/flaw/list.htm?flag=true?number=%E8%AF%B7%E8%BE%93%E5%85%A5%E7%B2%BE%E7%A1%AE%E7%BC%96%E5%8F%B7&startDate=&endDate=&flag=true&field=&order=&max=20&offset=0')
    url_page = Urlcreator(1, 500)
    scrapper(url_page)


if __name__ == '__main__':
    main()
