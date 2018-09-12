import mysql.connector
db = mysql.connector.connect(user='root',
                                 password='Test@20180604',
                                 host='rm-j6cx1z86d86308x6m.mysql.rds.aliyuncs.com',
                                 port='3306',
                                 database='admin'
                                 )
import mysql.connector
db = mysql.connector.connect(user='root',
                                 password='Bumble@20180628',
                                 host='rm-j6c9v62tlv18x957p.mysql.rds.aliyuncs.com',
                                 port='3306',
                                 database='admin'
                                 )
db.set_charset_collation('utf8')
cursor = db.cursor()


sql  =  '''select * from customer'''


sql = '''CREATE TABLE IF NOT EXISTS `user` (`id` VARCHAR(255),`password` NVARCHAR(255),PRIMARY KEY(id))'''
cursor.execute(sql)

sql2 = '''REPLACE INTO `user`(`id`  ,`password` ) VALUES('Jacob','Test@201807');'''
cursor.execute(sql2)


create_task_sql = '''CREATE TABLE IF NOT EXISTS `task` (`request_id` VARCHAR(255),`task_id` VARCHAR(255), `task_name` VARCHAR(255),`task_owner` VARCHAR(255),`task_startTime` VARCHAR(255),\
                                                    `task_endTime` VARCHAR(255), `task_sequence` VARCHAR(255),`task_crawlerId` VARCHAR(255), `task_frequency` VARCHAR(255),`task_crawlerType` VARCHAR(255),\
                                                    `task_url` VARCHAR(255),`task_node` VARCHAR(255),`report_frequency` VARCHAR(255),`task_modelid` VARCHAR(255),`task_modelName` VARCHAR(255),\
                                                    `task_reportId` VARCHAR(255),`task_reportName` VARCHAR(255),`task_communication` VARCHAR(255),`task_email` VARCHAR(255),`task_status` VARCHAR(255),\
                                                    PRIMARY KEY(task_id))'''
cursor.execute(create_task_sql)

sql3 = '''select * from user'''
cursor.execute(sql3)

for a in cursor:
	print(a)

sql4 = '''CREATE TABLE IF NOT EXISTS `insert_report` (`insert_report_id` VARCHAR(255),`insert_report_Time` NVARCHAR(255),`insert_report_type` NVARCHAR(255),`insert_report_email` NVARCHAR(255),PRIMARY KEY(insert_report_id))'''
cursor.execute(sql4)


sql5 ='''SELECT job_id from job '''
insert_task_email_frequency=db.Column(db.String(255))
    insert_task_email_timepoint
sql4 = '''CREATE TABLE IF NOT EXISTS `insert_scrapy_task` (`insert_task_owner` VARCHAR(255),`insert_task_startTime` NVARCHAR(255),`insert_task_endTime` NVARCHAR(255),`insert_task_frequency` NVARCHAR(255),`insert_task_crawlerId` NVARCHAR(255),`insert_task_email_frequency` NVARCHAR(255),`insert_task_email_timepoint` NVARCHAR(255),`insert_task_email` NVARCHAR(255),PRIMARY KEY(insert_task_owner,insert_task_startTime))'''
cursor.execute(sql4)


tt= {'status': 'FINISHED', 'lasted_time': '0:6:01.912362', 'job_id': 'f18adb4b-2-SH', 'task_id': 'f18adb4b', 'start_time': '2018-07-14 20:10:01.276081', 'end_time':'2018-07-14 20:16:01.276081', 'created_time':'2018-07-13 20:10:01.276081', 'unsuccessful_count': 0, 'percentage': 1, 'location': 'SH'}
receive3=requests.post("http://cti_hk_cns00.eycyber.com:8080/reporting",data=tt)
jj = '''REPLACE INTO job (job_id,job_createdTime,job_startTime,job_lastedTime,\
                                            job_status, job_endTime,job_node,job_percentage,job_unsuccessfulCount,task_id) VALUES ('8f552c25-9-HK', 's', 's', 's','s', 's', 's','s','s','s')
                                            '''
cursor.execute(sql)


ll ='''select COLUMN_NAME,DATA_TYPE,CHARACTER_MAXIMUM_LENGTH from information_schema.columns where TABLE_NAME=job'''
cursor.execute(create_site_sql)
cursor.execute(creat_request_sql)
cursor.execute(creat_task_sql)
cursor.execute(create_job_sql)


CREATE INDEX index_OF_cve
ON cve (cveId)

index = '''CREATE INDEX index_OF_cve
ON cve_hash (vul_cveId) '''

index2 = '''CREATE INDEX index_OF_cve2
ON cnvd_hash (vul_cveId) '''

index3 = '''CREATE INDEX index_OF_cve3
ON cvedetail3 (cveId) '''


sql = '''CREATE TABLE insert_task'''

sql = '''DROP TABLE insert_task'''
cursor.execute(sql)
sql = '''DROP TABLE insert_social_task'''
cursor.execute(sql)


sql = '''DROP TABLE insert_media_report'''
cursor.execute(sql)


import mysql.connector
db = mysql.connector.connect(user='root',
                                 password='Bumble@20180628',
                                 host='rm-j6c9v62tlv18x957p.mysql.rds.aliyuncs.com',
                                 port='3306',
                                 database='github'
                                 )
db.set_charset_collation('utf8')
cursor = db.cursor()
sql = '''DROP TABLE github_result'''
cursor.execute(sql)

sql = '''select * from github_result limit 5'''


create_sql = '''SELECT cve_hash.vul_cveId, cve_hash.vul_type, cve_hash.vul_updateDate,cvedetail3.effectedProduct, cve_hash.vul_score, cve_hash.vul_des, 
    cnvd_hash.vul_patch, cnvd_hash.vul_containSol, cnvd_hash.vul_describe

    FROM (cve_hash
    LEFT JOIN cnvd_hash
    ON cve_hash.vul_cveId = cnvd_hash.vul_cveId
    LEFT JOIN cvedetail3
    ON cnvd_hash.vul_cveId = cvedetail3.cveId)

    WHERE cve_hash.vul_updateDate >= (NOW() - INTERVAL 24 DAY) 
    ORDER BY cve_hash.vul_updateDate DESC'''



create_site_sql = '''CREATE TABLE IF NOT EXISTS `site` (`site_id` VARCHAR(255), `site_title` VARCHAR(255),`site_url` VARCHAR(255),`site_type` VARCHAR(255),\
                                                    `site_attribute` VARCHAR(255), `site_area` VARCHAR(255),`site_ranking` VARCHAR(255), `site_weight` VARCHAR(255),`site_ipAddress` VARCHAR(255),\
                                                    `site_geoAddress` VARCHAR(255), `site_scrapSection` VARCHAR(255),`site_scrapPath` VARCHAR(255),`site_scrapListed` VARCHAR(255),\
                                                    `site_scrapFrequency` VARCHAR(255),`site_worldRank` VARCHAR(255),PRIMARY KEY(site_id))'''

creat_request_sql = '''CREATE TABLE IF NOT EXISTS `request` (`request_id` VARCHAR(255), `request_owner` VARCHAR(255),`request_startTime` VARCHAR(255),`request_endTime` VARCHAR(255),\
                                                    `request_type` VARCHAR(255), `request_sites` VARCHAR(255),`request_scanFrequency` VARCHAR(255), `request_sendFrequency` VARCHAR(255),`request_node` VARCHAR(255),\
                                                    `request_communication` VARCHAR(255),`request_email` VARCHAR(255),PRIMARY KEY(request_id))'''

creat_task_sql = '''CREATE TABLE IF NOT EXISTS `task` (`request_id` VARCHAR(255),`task_id` VARCHAR(255), `task_name` VARCHAR(255),`task_owner` VARCHAR(255),`task_startTime` VARCHAR(255),\
                                                    `task_endTime` VARCHAR(255), `task_sequence` VARCHAR(255),`task_crawlerId` VARCHAR(255), `task_frequency` VARCHAR(255),`task_crawlerType` VARCHAR(255),\
                                                    `task_url` VARCHAR(255),`task_node` VARCHAR(255),`report_frequency` VARCHAR(255),`task_modelid` VARCHAR(255),`task_modelName` VARCHAR(255),\
                                                    `task_reportId` VARCHAR(255),`task_reportName` VARCHAR(255),`task_communication` VARCHAR(255),`task_email` VARCHAR(255),`task_status` VARCHAR(255),\
                                                    PRIMARY KEY(task_id))'''


create_job_sql = '''CREATE TABLE IF NOT EXISTS `job` (`job_id` VARCHAR(255), `job_createdTime` VARCHAR(255),`job_startTime` VARCHAR(255),`job_lastedTime` VARCHAR(255),\
                                                    `job_endTime` VARCHAR(255), `job_status` VARCHAR(255),`job_node` VARCHAR(255), `job_percentage` DECIMAL(5,4),`job_unsuccessfulCount` INT,`task_id` VARCHAR(255),`request_id` VARCHAR(255),
                                                    PRIMARY KEY(job_id))'''



import mysql.connector
db = mysql.connector.connect(user='root',
                                 password='Test@20180604',
                                 host='rm-j6cx1z86d86308x6m.mysql.rds.aliyuncs.com',
                                 port='3306',
                                 database='vulnerabilities'
                                 )
db.set_charset_collation('utf8')
cursor = db.cursor()

create_customer_sql = '''CREATE TABLE IF NOT EXISTS `vul_customer` (`customer_email` VARCHAR(255), PRIMARY KEY(customer_email))'''
cursor.execute(create_customer_sql)


create_customer_sql = '''CREATE TABLE IF NOT EXISTS `industry_customer` (`customer_email` VARCHAR(255), PRIMARY KEY(customer_email))'''
cursor.execute(create_customer_sql)


sql4 = '''CREATE TABLE IF NOT EXISTS `insert_social_task` (`insert_task_owner` VARCHAR(255),`insert_task_startTime` NVARCHAR(255),`insert_task_endTime` NVARCHAR(255),`insert_task_frequency` NVARCHAR(255),`insert_task_crawlerId` NVARCHAR(255),\
`insert_keyword` NVARCHAR(255),PRIMARY KEY(insert_task_owner, insert_task_startTime))'''
cursor.execute(sql4)


sql4 = '''CREATE TABLE IF NOT EXISTS `insert_github_task` (`insert_task_owner` VARCHAR(255),`insert_task_startTime` NVARCHAR(255),`insert_task_endTime` NVARCHAR(255),`insert_task_frequency` NVARCHAR(255),`insert_task_crawlerId` NVARCHAR(255),\
`insert_keyword` NVARCHAR(255),`insert_filter_keyword` NVARCHAR(255),PRIMARY KEY(insert_task_owner, insert_task_startTime))'''
cursor.execute(sql4)

def create_two_tables():### 此方法

    cursor , db = get_admin_conn()


    create_site_sql = '''CREATE TABLE IF NOT EXISTS `site` (`site_id` VARCHAR(255), `site_title` VARCHAR(255),`site_url` VARCHAR(255),`site_type` VARCHAR(255),\
                                                    `site_attribute` VARCHAR(255), `site_area` VARCHAR(255),`site_ranking` VARCHAR(255), `site_weight` VARCHAR(255),`site_ipAddress` VARCHAR(255),\
                                                    `site_geoAddress` VARCHAR(255), `site_scrapSection` VARCHAR(255),`site_scrapPath` VARCHAR(255),`site_scrapListed` VARCHAR(255),\
                                                    `site_scrapFrequency` VARCHAR(255),`site_worldRank` VARCHAR(255),PRIMARY KEY(site_id))'''

    creat_request_sql = '''CREATE TABLE IF NOT EXISTS `request` (`request_id` VARCHAR(255), `request_owner` VARCHAR(255),`request_startTime` VARCHAR(255),`request_endTime` VARCHAR(255),\
                                                    `request_type` VARCHAR(255), `request_sites` VARCHAR(255),`request_scanFrequency` VARCHAR(255), `request_sendFrequency` VARCHAR(255),`request_node` VARCHAR(255),\
                                                    `request_communication` VARCHAR(255),`request_email` VARCHAR(255),PRIMARY KEY(request_id))'''


    creat_task_sql = '''CREATE TABLE IF NOT EXISTS `task` (`request_id` VARCHAR(255),`task_id` VARCHAR(255), `task_name` VARCHAR(255),`task_owner` VARCHAR(255),`task_startTime` VARCHAR(255),\
                                                    `task_endTime` VARCHAR(255), `task_sequence` VARCHAR(255),`task_crawlerId` VARCHAR(255), `task_frequency` VARCHAR(255),`task_crawlerType` VARCHAR(255),\
                                                    `task_url` VARCHAR(255),`task_node` VARCHAR(255),`report_frequency` VARCHAR(255),`task_modelid` VARCHAR(255),`task_modelName` VARCHAR(255),\
                                                    `task_reportId` VARCHAR(255),`task_reportName` VARCHAR(255),`task_communication` VARCHAR(255),`task_email` VARCHAR(255),\
                                                    PRIMARY KEY(task_id))'''



    create_job_sql = '''CREATE TABLE IF NOT EXISTS `job` (`job_id` VARCHAR(255), `job_createdTime` VARCHAR(255),`job_startTime` VARCHAR(255),`job_lastedTime` VARCHAR(255),\
                                                    `job_endTime` VARCHAR(255), `job_status` VARCHAR(255),`job_node` VARCHAR(255), `job_percentage` DECIMAL(5,4),`job_unsuccessfulCount` INT,`task_id` VARCHAR(255),`request_id` VARCHAR(255),
                                                    PRIMARY KEY(job_id))'''
hk_scrapy.infosecinstitute('12345gjj-1-SH','2018-07-27 21:40:10','12345gjj')

sh_scrapy.cac('123456jj-1-SH','2018-07-27 21:40:10','123456jj')
hk_scrapy.infosecinstitute('12345gjj-1-SH','2018-07-27 21:40:10','12345gjj')
url_page = hk_scrapy.trendmicro_Urlcreator(1, 50)
hk_scrapy.trendmicro_scrapper(url_page,'12345gjj-1-SH','2018-07-27 21:40:10','12345gjj')
    cursor.execute(create_site_sql)
    cursor.execute(creat_request_sql)
    cursor.execute(creat_task_sql)
    cursor.execute(create_job_sql)
    try:
                db.commit()
    except:
                #if unexecuted, rollback
                db.rollback()
username="skylark@msg.eycyber.com"          #smtp服务器用户名
password=mail_password      #smtp服务器密码
mail_server = mail_server_1 #smtp服务器地址

Server.ehlo_or_helo_if_needed()

Server.login('c2t5bGFya0Btc2cuZXljeWJlci5jb20=','NWE2ZjRiZDNFVkVyNlE=')

'skylark@msg.eycyber.com', '5a6f4bd3EVEr6Q'


sql4 = '''CREATE TABLE IF NOT EXISTS `insert_media_report` (`insert_report_owner` VARCHAR(255),\
`insert_report_frequency` NVARCHAR(255),`insert_github_keywords` NVARCHAR(255),`insert_social_keyword` NVARCHAR(255),`insert_report_email_timepoint` NVARCHAR(255),\
`insert_report_email` NVARCHAR(255),PRIMARY KEY(insert_report_owner,insert_report_email))'''
cursor.execute(sql4)


create_customer_sql = '''CREATE TABLE IF NOT EXISTS `media_customer` (`customer_email` VARCHAR(255), PRIMARY KEY(customer_email))'''
cursor.execute(create_customer_sql)



import mysql.connector
db = mysql.connector.connect(user='root',
                                 password='Bumble@20180628',
                                 host='rm-j6c9v62tlv18x957p.mysql.rds.aliyuncs.com',
                                 port='3306',
                                 database='0_compliance'
                                 )
db.set_charset_collation('utf8')
cursor = db.cursor()
sql = '''select compliance_content,compliance_hash from cac_hash where compliance_hash = 'd4ac21995604d71052a84212f293ae6e3018c573';''' 
cursor.execute(sql)
datas = cursor.fetchall()
with open('checkCAC','w','utf-8') as cac:
    for each in datas:
        cac.write(each)







