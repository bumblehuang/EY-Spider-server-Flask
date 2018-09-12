import mysql.connector
import time
import console_logger
import logging
import requests
from lxml import etree
import os
db_host = os.environ['db_host']
db_password = os.environ['db_password']
oss_host = os.environ['oss_host']
oss_password = os.environ['oss_password']
log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.INFO)  # DEBUG
fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)
logger = console_logger.get_logger(__name__)

def get_admin_conn():
    db = mysql.connector.connect(user='root',
                                 password=db_password,
                                 host=db_host,
                                 port='3306',
                                 database='admin'
                                 )
    # set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()
    return cursor,db

def get_mysql_conn():
    db = mysql.connector.connect(user='root',
                                 password=db_password,
                                 host=db_host,
                                 port='3306',
                                 database='0_vulnerability'
                                 )
    # set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()
    return cursor,db

def update_job(job_id,created_time,start_time,lasted_time,status,end_time,location,percentage,unsuccess,task_id):
    cursor, db = get_admin_conn()
    job_sql = '''REPLACE INTO job (job_id,job_createdTime,job_startTime,job_lastedTime,\
                                            job_status, job_endTime,job_node,job_percentage,job_unsuccessfulCount,task_id) VALUES (%s, %s, %s, %s,%s, %s, %s,%s,%s,%s)
                                            '''
    cursor.execute(job_sql,(job_id,created_time,start_time,lasted_time,status,end_time,location,percentage,unsuccess,task_id))
    try:
                db.commit()
    except:
                db.rollback()
def cnvd_update(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x):
    db = mysql.connector.connect(user='root',
                                 password=db_password,
                                 host=db_host,
                                 port='3306',
                                 database='0_vulnerability'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')

    cursor = db.cursor()


    sql = 'CREATE TABLE IF NOT EXISTS `cnvd_hash` (`vul_id`  VARCHAR(255),`vul_cveId` NVARCHAR(255),`vul_cweId` NVARCHAR(255), `vul_describe` NVARCHAR(255), \
                                                `vul_score` NVARCHAR(255),`vul_level` NVARCHAR(255),`vul_type` NVARCHAR(255),`vul_cvssAccess` NVARCHAR(255), \
                                                `vul_cvsComplexity` NVARCHAR(255),`vul_cvssAuthentication` NVARCHAR(255),`vul_cvssConf` NVARCHAR(255),`vul_cvssInteg` NVARCHAR(255), \
                                                `vul_cvssAvail` NVARCHAR(255),`vul_name` NVARCHAR(255),`vul_publishedDate` DATE,`vul_updateDate` DATE, \
                                                `vul_containSol` NVARCHAR(255),`vul_source` NVARCHAR(255),`vul_effectedProduct` NVARCHAR(255),`vul_vendor` NVARCHAR(255), \
                                                `vul_patch` NVARCHAR(255),`vul_author` NVARCHAR(255),`vul_expCode` NVARCHAR(255), `vul_hash` NVARCHAR(255),PRIMARY KEY (vul_hash))'

    cursor.execute(sql)

    sql = 'REPLACE INTO `cnvd_hash`(`vul_id`  ,`vul_cveId` ,`vul_cweId` , `vul_describe` , \
                                                `vul_score`,`vul_level` ,`vul_type` ,`vul_cvssAccess` , \
                                                `vul_cvsComplexity` ,`vul_cvssAuthentication` ,`vul_cvssConf`,`vul_cvssInteg` , \
                                                `vul_cvssAvail` ,`vul_name` ,`vul_publishedDate` ,`vul_updateDate` , \
                                                `vul_containSol` ,`vul_source` ,`vul_effectedProduct` ,`vul_vendor` , \
                                                `vul_patch`,`vul_author` ,`vul_expCode`, `vul_hash` ) \
                       VALUES\
                      (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s);'

    cursor.execute(sql,(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x))

    try:
            db.commit()
    except:
            # if unexecuted, rollback
            db.rollback()
    logger.debug('*************************** inserted into CNVD HASH ************************')
def cve_insert_data(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p):
    sql = '''REPLACE INTO cve (vul_cveId, vul_cweId, vul_numOfExploits, vul_type, vul_publishedDate, vul_updateDate, vul_score, vul_accessLevel,vul_access,\
            vul_complexity, vul_authentication,vul_conf,vul_integ,vul_avail,vul_des,vul_hash)\
                   VALUES\
                  (%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s)'''
    db = mysql.connector.connect(user='root',
                                 password=db_password,
                                 host=db_host,
                                 port='3306',
                                 database='0_vulnerability'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')

    cursor = db.cursor()
    cursor.execute(sql,(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p))
    try:
            db.commit()
    except:
            # if unexecuted, rollback
            db.rollback()

def second_cve_Urlcreator():
    db = mysql.connector.connect(user='root',
                                 password=db_password,
                                 host=db_host,
                                 port='3306',
                                 database='0_vulnerability'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')
    cur = db.cursor(buffered=True)

    sql = '''SELECT vul_cveId from `cve` ORDER BY vul_updateDate DESC LIMIT 400'''

    cur.execute(sql)

    url_page = []

    for cveid in cur:
        url_page.append(
            "https://www.cvedetails.com/cve/" + str(cveid[0]) + "/"
        )
    print(url_page[:100])

    return url_page


def second_cve_scrapper(url_page_list):
    db = mysql.connector.connect(user='root',
                                 password=db_password,
                                 host=db_host,
                                 port='3306',
                                 database='0_vulnerability'
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

def return_task(task_id):
    select_sql = '''SELECT * FROM `task` WHERE `task_id` = %s'''%task_id
    cursor , db = get_admin_conn()
    logger.debug(query_sql)
    cursor.execute(query_sql)
    result_set = []
    logger.debug('***********************  the result of the task query ***************************')
    for ids in cursor:
      result_set.append(ids)
    logger.debug('***********************  the result of the task query ***************************')
    return result_set
def update_task(task_id,sequence,status):
    select_sql = '''UPDATE task SET task_sequence=%s ,task_status ='%s'  WHERE task_id = '%s' '''%(sequence , status, task_id)
    cursor , db = get_admin_conn()
    logger.debug(select_sql)
    cursor.execute(select_sql)
    try:
            db.commit()
    except:
            # if unexecuted, rollback
            db.rollback()

def insert_task(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r):
    insert_sql = 'REPLACE INTO `task` (`task_id` ,`task_name`  ,`task_owner`,`task_startTime`,\
                                                    `task_endTime` , `task_sequence` ,`task_crawlerId` , \
                                                    `task_frequency` ,`task_crawlerType`,`task_url`,`task_node`,`task_modelid`,`task_modelName`,`task_reportId`,`task_reportName`,\
                                                    `task_communication`,`task_email`,`task_status`) \
                               VALUES\
                              (%s, %s, %s, %s, %s ,%s,%s, %s, %s,%s, %s, %s, %s, %s ,%s,%s, %s,%s);'
    cursor , db = get_admin_conn()
    cursor.execute(insert_sql,(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r))
    try:
            db.commit()
    except:
            # if unexecuted, rollback
            db.rollback()
def query_task(a,b):
    query_sql = 'SELECT task_id FROM task WHERE task_owner='+a+'AND task_crawlerId='+b+';'
    cursor , db = get_admin_conn()
    logger.debug(query_sql)
    cursor.execute(query_sql)
    result_set = []
    logger.debug('***********************  the result of the task query ***************************')
    for ids in cursor:
      result_set.append(ids)
    logger.debug('***********************  the result of the task query ***************************')
    return result_set

def insert_customer(email):
    if email.strip() != '':
        cursor, db = get_admin_conn()
        sql = '''REPLACE INTO `industry_customer`(`customer_email`) VALUES('%s')''' % email
        logger.debug('Inserting new customer into the database........') 
        logger.debug(sql)
        cursor.execute(sql)
        try:
                db.commit()
        except:
                # if unexecuted, rollback
                db.rollback()
        sql = '''REPLACE INTO `vul_customer`(`customer_email`) VALUES('%s')''' % email
        logger.debug('Inserting new customer into the database........') 
        logger.debug(sql)
        cursor.execute(sql)
        try:
                db.commit()
        except:
                # if unexecuted, rollback
                db.rollback()

def insert_media_customer(email):
    if email.strip() != '':
        cursor, db = get_admin_conn()
        sql = '''REPLACE INTO `media_customer`(`customer_email`) VALUES('%s')''' % email
        logger.debug('Inserting new customer into the database........') 
        logger.debug(sql)
        cursor.execute(sql)
        try:
                db.commit()
        except:
                # if unexecuted, rollback
                db.rollback()

def event_securityfocus_hash2_db(dic):
    cursor,db = get_mysql_conn()
    sql = 'CREATE TABLE IF NOT EXISTS `securityfocus_hash1` (`vul_id`  VARCHAR(255),`vul_cveld` NVARCHAR(255),`vul_cweld` NVARCHAR(255), `vul_describe` NVARCHAR(255), \
                                                `vul_score` NVARCHAR(255),`vul_level` NVARCHAR(255),`vul_type` NVARCHAR(255),`vul_cvssAccess` NVARCHAR(255), \
                                                `vul_cvsComplexity` NVARCHAR(255),`vul_cvssAuthentication` NVARCHAR(255),`vul_cvssConf` NVARCHAR(255),`vul_cvssInteg` NVARCHAR(255), \
                                                `vul_cvssAvail` NVARCHAR(255),`vul_name` NVARCHAR(255),`vul_publishedDate` DATETIME,`vul_updateDate` DATETIME, \
                                                `vul_containSol` NVARCHAR(255),`vul_source` NVARCHAR(255),`vul_effectedProduct` NVARCHAR(255),`vul_vendor` NVARCHAR(255), \
                                                `vul_patch` NVARCHAR(255),`vul_author` NVARCHAR(255),`vul_code` NVARCHAR(255), `vul_hash` NVARCHAR(255),PRIMARY KEY (vul_hash))'


    cursor.execute(sql)

    sql = 'REPLACE INTO `securityfocus_hash1`(`vul_id`  ,`vul_cveld` ,`vul_cweld` , `vul_describe` , \
                                        `vul_score`,`vul_level` ,`vul_type` ,`vul_cvssAccess` , \
                                        `vul_cvsComplexity` ,`vul_cvssAuthentication` ,`vul_cvssConf`,`vul_cvssInteg` , \
                                        `vul_cvssAvail` ,`vul_name` ,`vul_publishedDate` ,`vul_updateDate` , \
                                        `vul_containSol` ,`vul_source` ,`vul_effectedProduct` ,`vul_vendor` , \
                                        `vul_patch`,`vul_author` ,`vul_code`, `vul_hash` ) \
               VALUES\
              (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s);'


    cursor.execute(sql,(dic['BugtraqID:'], dic['CVE:'], '', '', '', '',dic['Class:'], '', '', '', '', '',\
                            '', dic['title'], dic['Published:'], dic['Updated:'], '', url, '', '', '', '', '',\
                            hashvalue))

    try:
            db.commit()
    except:
            
            db.rollback()
def insert_wechat_data(a,b,c,d,e,f,g):
    db = mysql.connector.connect(user='root',
                                 password=db_password,
                                 host=db_host,
                                 database='0_social_media'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()

    sql1 = '''CREATE TABLE IF NOT EXISTS `wechat` (
      `title` nvarchar(255) NOT NULL,
      `content` mediumtext  DEFAULT NULL,
      `date`  nvarchar(30) DEFAULT NULL,
      `nickname` nvarchar(1000)  DEFAULT NULL,
      `wechat` nvarchar(500)  DEFAULT NULL,
      `link` text  DEFAULT NULL,
      `keyword` text  DEFAULT NULL,
       PRIMARY KEY (`title`));'''

    cursor.execute(sql1)

    sql2 = '''REPLACE INTO `wechat` (`title`,`content`,`date`,`nickname`,`wechat`,`link`,`keyword`) \
                    VALUES\
                    (%s, %s, %s, %s, %s, %s, %s);'''

    # print(data['title'], data['content'], data['date'], data['nickname'], data['wechat'])
    try:
        cursor.execute(sql2,
                       (a,b,c,d,e,f,g))
    except Exception as e:
        print(e)
        print(type(f),f)


    try:
        db.commit()
    except:
        # if unexecuted, rollback
        db.rollback()


def xuanwu_update(a,b,c,d,e):
    db = mysql.connector.connect(user='root',
                                 password=db_password,
                                 host=db_host,
                                 port='3306',
                                 database='0_news'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')

    cursor = db.cursor()


    sql = 'CREATE TABLE IF NOT EXISTS `xuanwu_hash` (`news_category`  NVARCHAR(256),`news_title` NVARCHAR(100),`news_link` NVARCHAR(256), `news_hash` NVARCHAR(255),`news_publishedTime` DATE, PRIMARY KEY (news_hash));'

    cursor.execute(sql)

    sql = 'REPLACE INTO `xuanwu_hash`(`news_category` ,`news_title` ,`news_link` , `news_hash` ,`news_publishedTime` )\
                       VALUES\
                      (%s, %s, %s, %s, %s);'

    cursor.execute(sql,(a,b,c,d,e))

    try:
            db.commit()
    except:
            # if unexecuted, rollback
            db.rollback()
    logger.debug('*************************** inserted into xuanwu ************************')



################################### Hades Specail Area #########################################
def cisco_insert_data(dic):
    db = mysql.connector.connect(user='root',
                                 password=db_password,
                                 host=db_host,
                                 port='3306',
                                 database='0_news'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS `cisco_hash`  (`news_title`  NVARCHAR(255),`news_author` NVARCHAR(255),`news_publishedTime` DATE, `news_content` mediumtext, \
                                                  `news_category` NVARCHAR(255), `news_briefContent` NVARCHAR(511),`news_source` NVARCHAR(255), \
                                                  `news_tags` NVARCHAR(255),`news_hash` NVARCHAR(255) ,`news_exploitCode` NVARCHAR(255),`news_damagedItem` NVARCHAR(255), \
                                                  `news_area` NVARCHAR(255),`news_sector` NVARCHAR(255),`news_product` NVARCHAR(255),`news_link` NVARCHAR(255),PRIMARY KEY (news_hash))'
    cursor.execute(sql)

    sql = 'REPLACE INTO cisco_hash(`news_title` ,`news_publishedTime` , `news_category` , \
                                               `news_author`,`news_briefContent`,`news_tags` ,`news_source` , \
                                              `news_content` ,`news_hash` ,`news_exploitCode` ,`news_damagedItem`,`news_area`,`news_sector`,`news_product`,`news_link`) \
                   VALUES\
                  (%s, %s, %s, %s, %s, %s, %s, %s ,%s, %s, %s, %s, %s ,%s,%s);'

    # print(dic['news_title'],dic['news_publishedTime'],dic['news_category'] ,dic['news_author'],dic['news_briefContent'],dic['news_tags'],dic['news_source'],dic['news_content'],dic['news_hash'],dic['news_exploitCode'] ,dic['news_damagedItem'] ,dic['news_area'],dic['news_sector'] , dic['news_product'] ,dic['news_link'])

    cursor.execute(sql, (
    dic['news_title'], dic['news_publishedTime'], dic['news_category'], dic['news_author'], dic['news_briefContent'],
    dic['news_tags'], dic['news_source'], dic['news_content'], dic['news_hash'], dic['news_exploitCode'],
    dic['news_damagedItem'], dic['news_area'], dic['news_sector'], dic['news_product'], dic['news_link']))
    # cursor.execute(sql,
    # (title, time, postedin, author, content, tag, '', '', hashvalue, '', '', '', '', '', link))

    try:
        db.commit()
    except:
        # if unexecuted, rollback
        db.rollback()

def cac_insert_data(dic):
    db = mysql.connector.connect(user='root',
                                 password=db_password,
                                 host=db_host,
                                 port='3306',
                                 database='0_compliance'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS `cac_hash`  (`compliance_title`  NVARCHAR(255),`compliance_author` NVARCHAR(255),`compliance_publishedTime` DATETIME, `compliance_content` mediumtext, \
                                                      `compliance_hash` NVARCHAR(255),`compliance_link` NVARCHAR(255),`compliance_source` NVARCHAR(255),`compliance_tags` NVARCHAR(255),PRIMARY KEY (compliance_hash))'
    cursor.execute(sql)

    sql = 'REPLACE INTO cac_hash(`compliance_title`,`compliance_author`,`compliance_publishedTime` , `compliance_content`, \
                                                                     `compliance_hash` ,`compliance_link`,`compliance_source`,`compliance_tags`) \
                                      VALUES\
                                     (%s, %s, %s, %s, %s, %s ,%s,%s);'

    cursor.execute(sql, (
    dic['compliance_title'], dic['compliance_author'], dic['compliance_publishedTime'], dic['compliance_content'],
    dic['compliance_hash'], dic['compliance_link'], dic['compliance_source'], dic['compliance_tags']))

    try:
        db.commit()
    except:
        # if unexecuted, rollback
        db.rollback()

def infosecinstitute_insert_data(dic):
    db = mysql.connector.connect(user='root',
                                 password=db_password,
                                 host=db_host,
                                 port='3306',
                                 database='0_news'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS `infosecinstitute_hash`  (`news_title`  NVARCHAR(255),`news_author` NVARCHAR(255),`news_publishedTime` DATE, `news_content` mediumtext, \
                                                  `news_category` NVARCHAR(255), `news_briefContent` NVARCHAR(511),`news_source` NVARCHAR(255), \
                                                  `news_tags` NVARCHAR(255),`news_hash` NVARCHAR(255) ,`news_exploitCode` NVARCHAR(255),`news_damagedItem` NVARCHAR(255), \
                                                  `news_area` NVARCHAR(255),`news_sector` NVARCHAR(255),`news_product` NVARCHAR(255),`news_link` NVARCHAR(255),PRIMARY KEY (news_hash))'
    cursor.execute(sql)

    sql = 'REPLACE INTO infosecinstitute_hash(`news_title` ,`news_publishedTime` , `news_category` , \
                                               `news_author`,`news_briefContent`,`news_tags` ,`news_source` , \
                                              `news_content` ,`news_hash` ,`news_exploitCode` ,`news_damagedItem`,`news_area`,`news_sector`,`news_product`,`news_link`) \
                   VALUES\
                  (%s, %s, %s, %s, %s, %s, %s, %s ,%s, %s, %s, %s, %s ,%s,%s);'

    # print(dic['news_title'],dic['news_publishedTime'],dic['news_category'] ,dic['news_author'],dic['news_briefContent'],dic['news_tags'],dic['news_source'],dic['news_content'],dic['news_hash'],dic['news_exploitCode'] ,dic['news_damagedItem'] ,dic['news_area'],dic['news_sector'] , dic['news_product'] ,dic['news_link'])

    cursor.execute(sql, (
    dic['news_title'], dic['news_publishedTime'], dic['news_category'], dic['news_author'], dic['news_briefContent'],
    dic['news_tags'], dic['news_source'], dic['news_content'], dic['news_hash'], dic['news_exploitCode'],
    dic['news_damagedItem'], dic['news_area'], dic['news_sector'], dic['news_product'], dic['news_link']))
    # cursor.execute(sql,
    # (title, time, postedin, author, content, tag, '', '', hashvalue, '', '', '', '', '', link))

    try:
        db.commit()
    except:
        # if unexecuted, rollback
        db.rollback()
def trendmicro_insert_data(each):
    db = mysql.connector.connect(user='root',
                                 password=db_password,
                                 host=db_host,
                                 port='3306',
                                 database='0_news'
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
    sql = 'REPLACE INTO trendmicro_hash1(`news_title` ,`news_publishedTime` , `news_category` , \
                                                           `news_author`,`news_briefContent`,`news_tags` ,`news_source` , \
                                                          `news_content` ,`news_hash` ,`news_exploitCode` ,`news_damagedItem`,`news_area`,`news_sector`,`news_product`,`news_link`) \
                               VALUES\
                              (%s, %s, %s, %s, %s, %s, %s, %s ,%s, %s, %s, %s, %s ,%s,%s);'
    title=each['news_title']
    time =each['news_publishedTime']
    postedin=each['news_category']
    author=each['news_author']
    content=each['news_briefContent']
    tag=each['news_tags']
    hashvalue=each['news_hash']
    link=each['news_link']
    cursor.execute(sql,
                   (title, time, postedin, author, content, tag, '', '', hashvalue, '', '', '', '', '',link))

    try:
        db.commit()
    except:
        # if unexecuted, rollback
        db.rollback()

###compliance
def tc260_insert_data(dic):
    db = mysql.connector.connect(user='root',
                                 password=db_password,
                                 host=db_host,
                                 port='3306',
                                 database='0_compliance'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS `tc260_hash`  (`compliance_title`  NVARCHAR(255),`compliance_author` NVARCHAR(255),`compliance_publishedTime` DATETIME, `compliance_content` mediumtext, \
                                                      `compliance_hash` NVARCHAR(255),`compliance_link` NVARCHAR(255),`compliance_source` NVARCHAR(255),`compliance_tags` NVARCHAR(255),PRIMARY KEY (compliance_hash))'
    cursor.execute(sql)

    sql = 'REPLACE INTO tc260_hash(`compliance_title`,`compliance_author`,`compliance_publishedTime` , `compliance_content`, \
                                                                     `compliance_hash` ,`compliance_link`,`compliance_source`,`compliance_tags`) \
                                      VALUES\
                                     (%s, %s, %s, %s, %s, %s ,%s,%s);'

    cursor.execute(sql, (
    dic['compliance_title'], dic['compliance_author'], dic['compliance_publishedTime'], dic['compliance_content'],
    dic['compliance_hash'], dic['compliance_link'], dic['compliance_source'], dic['compliance_tags']))

    try:
        db.commit()
    except:
        # if unexecuted, rollback
        db.rollback()

###compliance
def safe_gave_insert_date(dic):
    db = mysql.connector.connect(user='root',
                                 password=db_password,
                                 host=db_host,
                                 port='3306',
                                 database='0_compliance'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS `safe_gave_hash`  (`compliance_title`  NVARCHAR(255),`compliance_author` NVARCHAR(255),`compliance_publishedTime` DATETIME, `compliance_content` mediumtext, \
                                                      `compliance_hash` NVARCHAR(255),`compliance_link` NVARCHAR(255),`compliance_source` NVARCHAR(255),`compliance_tags` NVARCHAR(255),PRIMARY KEY (compliance_hash))'
    cursor.execute(sql)

    sql = 'REPLACE INTO safe_gave_hash(`compliance_title`,`compliance_author`,`compliance_publishedTime` , `compliance_content`, \
                                                                     `compliance_hash` ,`compliance_link`,`compliance_source`,`compliance_tags`) \
                                      VALUES\
                                     (%s, %s, %s, %s, %s, %s ,%s,%s);'

    cursor.execute(sql, (
    dic['compliance_title'], dic['compliance_author'], dic['compliance_publishedTime'], dic['compliance_content'],
    dic['compliance_hash'], dic['compliance_link'], dic['compliance_source'], dic['compliance_tags']))

    try:
        db.commit()
    except:
        # if unexecuted, rollback
        db.rollback()

################################### Hades Specail Area #########################################