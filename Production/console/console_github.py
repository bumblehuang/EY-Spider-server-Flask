# coding:utf-8
import requests
import time
import json
import re
import base64
import csv
import sys
import mysql.connector
import os
import re
import base64
import mysql.connector
import os
import console_logger
import console_db
import datetime
WAITING= 'WAITING TO RUN'
RUNNING = 'RUNNING'
FINISHED = 'FINISHED'
PAUSED = 'PAUSED'
TERMINATED = 'TERMINATED'
LOCATION='HK'
db_host = os.environ['db_host']
db_password = os.environ['db_password']
reload(sys)
sys.setdefaultencoding('utf-8')
logger = console_logger.get_logger(__name__)
class mysqldb(object):
    def __init__(self):
        self.conn = mysql.connector.connect(
            user='root',
            password=db_password,
            host=db_host,
            port='3306',
            database='github'
        )
        self.conn.set_charset_collation('utf8')
        self.cur = self.conn.cursor(buffered=True)

    def process_item(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception, e:
            print e
        return self.cur

class detail_search():
    # encoding:utf-8

    def keyword():
        pass

    def create_table(self,
                     sql='''CREATE TABLE
IF
	NOT EXISTS `github_result` (
		`github_keyWords` NVARCHAR ( 255 ),
		`github_fileName` NVARCHAR ( 255 ),
		`github_path` NVARCHAR ( 255 ),
		`github_gitUrl` NVARCHAR ( 255 ),
		`github_htmlUrl` NVARCHAR ( 255 ),
		`github_author` NVARCHAR ( 255 ),
		`github_authorId` NVARCHAR ( 255 ),
		`github_count` NVARCHAR ( 255 ),
		`github_content` MEDIUMTEXT,
		`github_score` NVARCHAR ( 255 ),
		`github_sha` NVARCHAR ( 255 ),
		`github_singleUrl` NVARCHAR ( 255 ),
        `github_tags` NVARCHAR ( 255 ),
        `github_description` MEDIUMTEXT,
	PRIMARY KEY ( github_sha ) 
	);'''):
        a = mysqldb()
        self.cur = a.process_item(sql)



    def database_attain(self,
                        sql='''select keywords, result_num,origin_url from result where flag = '1' and result_num_q4<result_num_2018q2_1 and result_num_2018q2_1 !='0';'''):
        a = mysqldb()
        self.cur = a.process_item(sql)

    def page_crawler(self, url):
        #         url = 'https://api.github.com/search/code?q=%s&page=1&per_page=100&access_token=6646e40e911b412e27e7dee7ba1edc41135e6852'%keywords
        a = requests.get(url)
        self.raw_html = a.text

    #         return self.raw_html
    def page_parser_1(self, raw_html):
        decodejson = json.loads(raw_html)
        try:
            self.raw_data = decodejson['items']
        except Exception, e:
            print e
            time.sleep(10)
            
            


    def page_parser_2(self, data):
        self.sha = data['sha']
        pk_sql = '''select github_sha from github_result where github_sha='%s';''' % self.sha
        self.database_attain(pk_sql)
        values = self.cur.fetchall()
        if values != []:
            print('这个结果已经存入数据库')
            return 1
        print('did we get here ???????')
        self.file_name = data['name']
        self.path = data['path']
        self.git_url = data['git_url']
        self.html_url = data['html_url']
        self.author = data['repository']['owner']['login']
        self.author_id = data['repository']['owner']['id']
        self.single_url = data['url']
        self.score = data['score']
        self.description = data['repository']['description']
        return 0
        
    def page_parser_3(self, raw_html):
        decodejson = json.loads(raw_html)
        self.code_base64 = decodejson['content']


    def page_storage(self, keywords, file_name,path,git_url,html_url,author,author_id,count,code_base64,score,single_url, sha,description):
        cur = mysqldb()
        
        sql = '''insert into github_result(github_keyWords,github_fileName,github_path, github_gitUrl,github_htmlUrl,github_author,github_authorId,github_count,
                                                      github_content,github_score,github_singleUrl,github_sha,github_description) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")''' % (keywords, file_name,path,git_url,html_url,author,author_id,count,code_base64,score,single_url, sha,description)
        cur.process_item(sql)

    def run(self,keywords_list):
        self.create_table()
        #keywords = '欧莱雅'
        
        #keywords_list = ['Connext','联蔚科技']
        for keywords in keywords_list:
            url = 'https://api.github.com/search/code?q=%s&page=1&per_page=10&access_token=6646e40e911b412e27e7dee7ba1edc41135e6852' % keywords
            keywords = keywords.decode('utf-8')
            #print(keywords)
            a = requests.Session()
            b = a.get(url)
            # print b.text
            decodejson = json.loads(b.text)
            # print b.text
            try:
                result_num = decodejson['total_count']
            except Exception, e:
                time.sleep(5)
                print e
                # print b.text
            self.count = int(result_num)
    #api借口限制查看前一千条
            #num =int(self.count/100)
            
            for i in range(1,11):
                print(i)
                api_url_1 = 'https://api.github.com/search/code?q=%s&page=%s&per_page=100&access_token=6646e40e911b412e27e7dee7ba1edc41135e6852' % (keywords, i)
                self.page_crawler(api_url_1)
                raw_html_1 = self.raw_html
                self.page_parser_1(raw_html_1)
                j = 0
                for data in self.raw_data:
                    j += 1
                    #print(keywords)
                    print("正在爬取%s第%s页第%s条" % (keywords.encode('utf-8'),i ,j))
                    a = self.page_parser_2(data)
                    if a == 1:
                        continue
                    try:
                        api_url_2 = self.git_url + '?access_token=6646e40e911b412e27e7dee7ba1edc41135e6852'
                        self.page_crawler(api_url_2)
                        raw_html_2 = self.raw_html
                        self.page_parser_3(raw_html_2)
                        try:
                            print(keywords, self.file_name,self.path,self.git_url,self.html_url,self.author,self.author_id,self.count,self.code_base64,self.score,self.single_url, self.sha,self.description)
                        except Exception as e:
                            print(e)
                        self.page_storage(keywords, self.file_name,self.path,self.git_url,self.html_url,self.author,self.author_id,self.count,self.code_base64,self.score,self.single_url, self.sha,self.description)
                    except Exception as e:
                        print(e)
def filter(keywords,filter_keywords):

    db = mysql.connector.connect(
            user='root',
            password=db_password,
            host=db_host,
            port='3306',
            database='github'
        )

    # set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()
    
    print(keywords)
    sql = '''select github_keyWords,github_content,github_sha from github_result where github_keyWords = '%s';''' % keywords

    cursor.execute(sql)
    dates = cursor.fetchall()
    filter_count = 0
    for row in dates:

        code_ori = base64.b64decode(row[1])
        sha = row[2]
        count = 0
        for i in filter_keywords:
            if re.findall(i,code_ori) != []:
                count += 1
        if count != 0:
            filter_count += 1
            print('正在filter%s条' % filter_count)
            sql2 = '''update github_result set github_tags = 'no' where github_sha = '%s';''' % sha
            cursor.execute(sql2)
    try:
        db.commit()
    except:
        # if unexecuted, rollback
        db.rollback()




def execute_github(job_id,created_time,task_id,keywords,filter_keywords):
    if ',' in keywords:
        keywords_list = keywords.strip().split(',')
    else:
        keywords_list=[]
        keywords_list.append(keywords)
    if ',' in filter_keywords:
        filter_keywords = filter_keywords.strip().split(',')
    else:
        filter_keywords = [filter_keywords]
    logger.debug(keywords_list)
    logger.debug(filter_keywords)

    total_length = len(keywords_list)
    suceess_count=0 
    unsuccessful_count=0
    start_time = datetime.datetime.now()
    status = RUNNING
    lasted_time='None'
    end_time='None'
    location=LOCATION
    percentage = suceess_count / total_length
    a = detail_search()
    # keywords_list = ['Lancome','Armani']
    a.run(keywords_list)
    # filter_keywords = ['baidu','taobao','手表','京东','服饰','longines','tissot','uniqlo','nike','amazon']
    for keyword in keywords_list:
        filter(keyword, filter_keywords)
        suceess_count+=1
        percentage = float(suceess_count)/ total_length
        console_db.update_job(job_id,created_time,start_time.strftime("%Y-%m-%d %H:%M:%S"),lasted_time,status,end_time,location,str(float(percentage)*100)[:5]+'%',unsuccessful_count,task_id)
    percentage = float(suceess_count) / total_length
    end_time = datetime.datetime.now()
    lasted_time = str(end_time - start_time)[:-7]
    end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
    status = FINISHED
    console_db.update_job(job_id,created_time,start_time.strftime("%Y-%m-%d %H:%M:%S"),lasted_time,status,end_time,location,str(float(percentage)*100)[:5]+'%',unsuccessful_count,task_id)
    job_list = job_id.strip().split('-')
    task_sequence = job_list[1]
    run_status = 'FINISHED'
    console_db.update_task(task_id,task_sequence,run_status)
