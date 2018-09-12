# -*- coding: utf-8 -*-
import mysql.connector
import pandas as pd
from pyecharts import Pie, Bar, Page
from types import StringType, UnicodeType
import time
from IPython.display import HTML
import oss2
from datetime import date
import console_logger
import io
import os
db_host = os.environ['db_host']
db_password = os.environ['db_password']
oss_host = os.environ['oss_host']
oss_password = os.environ['oss_password']
logger = console_logger.get_logger(__name__)
auth = oss2.Auth(oss_host, oss_password)
bucket = oss2.Bucket(auth, 'oss-cn-shanghai.aliyuncs.com', 'cti-pub-files')

def data_grabber_with_version():
    db = mysql.connector.connect(user='root',
                                 password=db_password,
                                 host=db_host,
                                 port='3306',
                                 database='0_vulnerability'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')
    cur = db.cursor(buffered=True)

    sql = '''
    SELECT cve.vul_cveId, cve.vul_type, cve.vul_updateDate,cvedetail3.effectedProduct, cve.vul_score, cve.vul_des, 
    cnvd_hash.vul_patch, cnvd_hash.vul_containSol, cnvd_hash.vul_describe

    FROM (cve
    LEFT JOIN cnvd_hash
    ON cve.vul_cveId = cnvd_hash.vul_cveId
    LEFT JOIN cvedetail3
    ON cnvd_hash.vul_cveId = cvedetail3.cveId)

    WHERE cve.vul_updateDate >= (NOW() - INTERVAL 24 DAY) 
    ORDER BY cve.vul_updateDate DESC
    '''

    cur.execute(sql)
    rows = cur.fetchall()

    return rows

def table_drawer_with_version(rows):
    df = pd.DataFrame([ij.strip() if isinstance(ij,(UnicodeType)) else ij for ij in i] for i in rows)
    columns = {0: 'cveId', 1: 'Vulnerability Type', 2: 'Date', 3: 'Effected Product',4:'Level Score',5:'Description',6:'Patch',7:'Solution',8:'描述'}
    df.rename(columns = columns, inplace=True, index = None)

    print(len(df))
    return df

def level(x):
    
    if x < 4:
        return 'low'
    elif 4 <= x <= 7:
        return 'middle'
    else:
        return 'high'

def level_pie_drawer_without_version(report_id, df):

    df = df.drop_duplicates(subset = 'cveId')
    print(len(df))
    df['Level'] = df['Level Score'].apply(level)
    df_count = df.groupby(['Level']).size().reset_index(name='count')
    print(df_count)
    df_dic = {}
    df_dic['high'], df_dic['middle'], df_dic['low'] = 0, 0 ,0
    df_dic_1 = df_count.set_index('Level').T.to_dict('record')
    df_dic_2 = df_dic_1[0]
    df_dic['high'], df_dic['middle'], df_dic['low'] = df_dic_2['high'],df_dic_2['middle'],df_dic_2['low']
    

    attr = ["High", "Midium", "Low"]
    v1 = [df_dic['high'], df_dic['middle'], df_dic['low']]

    pie = Pie("Vulnerability risk level distribution", width=900, title_pos = 'center')
    pie.add("", attr, v1, radius=[40, 75], label_text_color=None,
        is_label_show=False, legend_orient='vertical',
        legend_pos='left')
    pie.render("pie.html")
    with open('pie.html', 'rb') as fileobj:
        directory = report_id+'/pie.html' 
        result = bucket.put_object(directory,fileobj)
        print(result.status)
    return v1 , sum(v1)
def table_drawer_with_high_level(report_id , df):
   
    df = df.drop_duplicates(subset = 'cveId')
    df['Level'] = df['Level Score'].apply(level)
    df = df[df['Level'] == 'high']
    df = df[['cveId','Vulnerability Type','Date','Description']]

    df['cveId'] = df['cveId'].apply(lambda x:"<a href='https://nvd.nist.gov/vuln/detail/{}'>{}</a>".format(x,x))

##    
##    df['cveId'] = '<a href = "www.baidu.com">' + df['cveId'].astype('str') + '</a>'
    df.to_csv('high_level.csv')


    df_small = df.head(5)
    df_small.to_csv('high_level_small.csv')
    # HTML(df.to_html('high_level.html', index = False, header ='High risk vulnerability',escape=False))
    # with open('high_level.csv', 'rb') as fileobj, open('high_level_small.csv','rb') as fileobj2:
    #     directory4 = report_id+'/high_level.csv' 
    #     result = bucket.put_object(directory4,fileobj)
    #     result2  = bucket.put_object(direcotry4_small,fileobj2)
    #     print(result.status)
    #     print(result2.status)
    # print(len(df))

def category_bar_without_version(report_id , df):
    
    df = df.drop_duplicates(subset = 'cveId')
    bar = Bar("Vulnerability risk type distribution", title_pos = 'center' )
    df_count = df.groupby(['Vulnerability Type']).size().reset_index(name='count')
    df_count['Vulnerability Type'][0] = 'Not Defined'
    print(df_count)

    df_dic = df_count.set_index('Vulnerability Type').T.to_dict('record')
    df_dic = df_dic[0]

    attr = [keys for keys in df_dic.keys()]
    v1 = [values for values in df_dic.values() ]

    zipped = zip(attr,v1)
    zipped = sorted(zipped, key = lambda t: t[1])

    attr_10 = [i for i,j in zipped][-10:]
    v1_10 = [j for i,j in zipped][-10:]

    bar.add("", attr_10, v1_10, is_convert = True)

    bar.render("bar1.html")
    with open('bar1.html', 'rb') as fileobj:
        directory2 = report_id+'/bar1.html' 
        result = bucket.put_object(directory2,fileobj)
        print(result.status)
    return attr_10 , v1_10

def date_bar_without_version(report_id, df):
    
    df = df.drop_duplicates(subset = 'cveId')
    bar = Bar("The number of vulnerabilities per day ", title_pos = 'center' )
    df_count = df.groupby(['Date']).size().reset_index(name='count')
    print(df_count)
    
    df_dic = df_count.set_index('Date').T.to_dict('record')
    df_dic = df_dic[0]
    
    
    attr = [keys for keys in df_dic.keys()]
    v1 = [values for values in df_dic.values()]

    zipped = zip(attr,v1)
    zipped = sorted(zipped, key = lambda t: t[0])

    attr_10 = [i for i,j in zipped][-10:]
    v1_10 = [j for i,j in zipped][-10:]
    print(attr_10,v1_10)

    bar = Bar("The number of vulnerabilities per day in {} days".format(len(df_count)))
    bar.add("", attr_10, v1_10, is_label_show=True, is_datazoom_show=True)
    bar.render("bar2.html")
    with open('bar2.html', 'rb') as fileobj:
        directory3 = report_id+'/bar2.html' 
        result = bucket.put_object(directory3, fileobj)
        print(result.status)
    

def patch_solution_table_drawer(report_id,df):
    
    df = df.drop_duplicates(subset = 'cveId')
    df = df[df['Patch'].str.encode('utf-8').str.contains('无补丁信息') == True]
    df = df[['cveId','Vulnerability Type','Date','Description']]
    df = df.sort_values(by = 'Date', ascending = False)
    df['cveId'] = df['cveId'].apply(lambda x:"<a href='https://nvd.nist.gov/vuln/detail/{}'>{}</a>".format(x,x))

##    df['描述'] = df['描述'].apply(lambda x: x.encode('unicode-escape').decode('utf-8'))
##    df['描述'] = df['描述'].apply(str.encode('utf-8'))
    
##    df_count = df.groupby(['Patch']).size().reset_index(name='count')
    
    df.to_csv('./patch_ch.csv', encoding = 'utf-8')
    df_small = df.head(5)
##    df_count = df.groupby(['Patch']).size().reset_index(name='count')
    df_small.to_csv('./patch_ch_small.csv', encoding = 'utf-8')

    # with open('patch_ch.csv', 'rb') as fileobj, open('patch_ch_small.csv','rb') as fileobj2:
    #     directory5 = report_id+'/patch_ch.csv' 
    #     direcroty5_small = report_id + '/patch_ch_small.csv'
    #     result = bucket.put_object(directory5, fileobj)
    #     result2 = bucket.put_object(directory5_small, fileobj2)
    # HTML(df.to_html('patch.html', index = False, header ='Vulnerabilities without Patch',escape=False))
    # with open('patch_ch.csv', 'rb') as fileobj:
    #     result = bucket.put_object('patch.html', fileobj)
    #     print(result.status)
##    writer = pytablewriter.HtmlTableWriter()
##    writer.table_name = "example_table"
##    writer.header_list = list(df.columns.values)
##    writer.value_matrix = df.values.tolist()
##    writer.write_table()
##
##    f = open('patch.html','w')
##    print(writer.to_string())

##    message = str(writer)
##
##    f.write(message)
##    f.close()
def writter(df, level_value, level_sum,category_attr_10, category_value_10 ):
    today = date.today()

    level = {'year': today.year, 'month':today.month, 'day':today.day,'sum_amount': level_sum, 'high_level': level_value[0],
             'high_level_percentage': ((float(level_value[0]) / float(level_sum)) * 100), 'medium_level': level_value[1],
             'medium_level_percentage': (float(level_value[1]) / float(level_sum)) * 100, 'low_level': level_value[2],
             'low_level_percentage': (float(level_value[2]) / float(level_sum)) * 100}

    level_text = '''截至{level[year]}年{level[month]}月{level[day]}日的扫描情况，最近一周共发现{level[sum_amount]}个漏洞,
其中高风险漏洞{level[high_level]}个，占总漏洞的{level[high_level_percentage]:.2f}%; 
中风险漏洞{level[medium_level]}个,占总漏洞的{level[medium_level_percentage]:.2f}%; 
低风险漏洞{level[low_level]}个，占总漏洞的{level[low_level_percentage]:.2f}%.'''.format(level=level)


    category_text =  '''本次所扫描到的漏洞可根据风险类别分为以下主要10类, 高危漏洞类别按数量正序分布如下：
{0[9]}: {1[9]}个；
{0[8]}: {1[8]}个；
{0[7]}: {1[7]}个；
{0[6]}: {1[6]}个；
{0[5]}: {1[5]}个；
{0[4]}: {1[4]}个；
{0[3]}: {1[3]}个；
{0[2]}: {1[2]}个；
{0[1]}: {1[1]}个；
{0[0]}: {1[0]}个。'''.format(category_attr_10, category_value_10)

    date1 = {}

    date1_text = '本周/月安全漏洞发布趋势如下：\
                    xxx:xx个\
                    xxx:xx个'



    return level_text, category_text,date1_text

def df_to_sql(report_id, request_id, df):
    
    df = df.drop_duplicates(subset = 'cveId')
    df['Level'] = df['Level Score'].apply(level)
    
    db = mysql.connector.connect(user='root',
                                 password=db_password,
                                 host=db_host,
                                 database='1_vul_process'
                                 )
    df_dict = df.to_dict('record')

    #set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()


    sql = '''CREATE TABLE IF NOT EXISTS `vul_process` (`report_id`  VARCHAR(255),`request_id`  VARCHAR(255),`prc_vul_cveid` NVARCHAR(255), `prc_vul_type` NVARCHAR(255),\
                                               `prc_vul_updateDate` DATE,`prc_vul_effectedProduct` VARCHAR(255),`prc_vul_level` VARCHAR(255), `prc_vul_describe` VARCHAR(4000),\
                                              `prc_vul_patch` VARCHAR(255),`prc_vul_chi_describe` NVARCHAR(4000), `prc_vul_containSol` VARCHAR(255),`prc_vul_weight` VARCHAR(255),  PRIMARY KEY (report_id,prc_vul_cveid ))'''

    cursor.execute(sql)

    
    for i in df_dict:
        sql = '''REPLACE INTO vul_process (report_id, request_id,prc_vul_cveid, prc_vul_type,
                                            prc_vul_updateDate,prc_vul_effectedProduct ,prc_vul_level ,prc_vul_describe , prc_vul_chi_describe,
                                            prc_vul_patch ,prc_vul_containSol )
                       VALUES
                      (%s, %s, %s, %s,%s,%s,%s ,%s,%s,%s,%s)'''
                
        cursor.execute(sql,(report_id, request_id, i['cveId'], i['Vulnerability Type'], i['Date'], i['Effected Product'], i['Level Score'],i['Description'],i['描述'],i['Patch'],i['Solution'] ))
                
        try:
            db.commit()
        except:
            #if unexecuted, rollback
            db.rollback()
def text_to_sql(report_id,request_id,level_text, category_text,date1_text,report_type = 'week'):
    db = mysql.connector.connect(user='root',
                                 password=db_password,
                                 host=db_host,
                                 database='admin'
                                 )

    #set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()


    sql = '''CREATE TABLE IF NOT EXISTS `2_report` (`report_id`  VARCHAR(255),`request_id`  VARCHAR(255),`report_title`  VARCHAR(255),`report_categoryDis` NVARCHAR(255), `report_DateDis` NVARCHAR(255),\
                                               `report_levelDis` VARCHAR(255),`report_type` VARCHAR(255),\
                                               PRIMARY KEY (report_id))'''

    cursor.execute(sql)

    
   
            


    sql = '''REPLACE INTO 2_report (report_id, request_id, report_levelDis,report_categoryDis, report_DateDis ,\
                                               report_type)\
                   VALUES\
                  (%s,%s,%s,%s,%s,%s)'''
            

    cursor.execute(sql,(report_id, request_id, level_text, category_text,date1_text,report_type ))
            
    try:
        db.commit()
    except:
        #if unexecuted, rollback
        db.rollback()

def go_thierry(report_id, request_id):

    pd.set_option('display.max_colwidth', -1)
    start_time = time.time()
    data = data_grabber_with_version()
    df = table_drawer_with_version(data)
   #1 按等级分类漏洞分布
    level_value ,  level_sum = level_pie_drawer_without_version(report_id , df)
   #2 高威胁等级漏洞展示（高危等级按时间排序）
    table_drawer_with_high_level(report_id, df)
   #3 按漏洞类别分类漏洞分布
    category_attr_10 , category_value_10 = category_bar_without_version(report_id, df)
    writter(df,level_value ,  level_sum,category_attr_10 , category_value_10)
   #4 展示无补丁漏洞（高危等级按时间排序）
    patch_solution_table_drawer(report_id, df)
   #5 按时间显示漏洞数量
    date_bar_without_version(report_id , df)

    level_text, category_text, date1_text= writter(df,level_value,level_sum, category_attr_10, category_value_10 )

    text_to_sql(report_id, request_id, level_text, category_text,date1_text,report_type = 'week')

    df_to_sql(report_id,request_id,df)
    return level_text, category_text
    


    print(time.time() - start_time)

if __name__ == '__main__':
    main()

    
