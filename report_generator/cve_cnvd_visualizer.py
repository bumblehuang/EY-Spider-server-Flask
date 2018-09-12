# coding=utf-8
import mysql.connector
import pandas as pd
from pyecharts import Pie, Bar, Page
from types import StringType, UnicodeType
import time
import matplotlib.pyplot as plt
from pandas.tools.plotting import table
from html2text import unescape
from matplotlib import rc
import pytablewriter
from IPython.display import HTML
from pyecharts_snapshot.main import make_a_snapshot
from datetime import date
import numpy as np


today = date.today()


def data_grabber_with_version():
    db = mysql.connector.connect(user='root',
                                 password='Test@20180604',
                                 host='rm-j6cx1z86d86308x6m.mysql.rds.aliyuncs.com',
                                 port='3306',
                                 database='vulnerabilities'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')
    cur = db.cursor(buffered=True)

    sql = '''
    SELECT cve_hash.vul_cveId, cve_hash.vul_type, cve_hash.vul_updateDate,cvedetail1.effectedProduct, cve_hash.vul_score, cve_hash.vul_des, 
    cnvd_hash.vul_patch, cnvd_hash.vul_containSol, cnvd_hash.vul_describe

    FROM (cve_hash
    LEFT JOIN cnvd_hash
    ON cve_hash.vul_cveId = cnvd_hash.vul_cveId
    LEFT JOIN cvedetail1
    ON cnvd_hash.vul_cveId = cvedetail1.cveId)

    WHERE cve_hash.vul_updateDate >= (NOW() - INTERVAL 12 DAY) 
    ORDER BY cve_hash.vul_updateDate DESC
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

def level_pie_drawer_without_version(df):

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
    

    level_attr = ["High", "Midium", "Low"]
    level_value = [df_dic['high'], df_dic['middle'], df_dic['low']]

    pie = Pie("Vulnerability risk level distribution", width=900, title_pos = 'center')
    pie.add("", level_attr, level_value, radius=[40, 75], label_text_color=None,
        is_label_show=True, legend_orient='vertical',
        legend_pos='left')
    pie.render("./level_pie_{}.html".format(today))

    return level_value,sum(level_value)


def table_drawer_with_high_level(df):
   
    df = df.drop_duplicates(subset = 'cveId')
    df['Level'] = df['Level Score'].apply(level)
    df = df[df['Level'] == 'high']
    df = df[['cveId','Vulnerability Type','Date','Description']]

    df['cveId'] = df['cveId'].apply(lambda x:"<a href='https://nvd.nist.gov/vuln/detail/{}' target='_Blank'>{}</a>".format(x,x))

##    
##    df['cveId'] = '<a href = "www.baidu.com">' + df['cveId'].astype('str') + '</a>'

    df.to_csv('high_level.csv')
    HTML(df.to_html('./high_level_table_{}.html'.format(today) , index = False, header ='High risk vulnerability',escape=False))
    
    print(len(df))

def category_bar_without_version(df):
    
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

    bar.render("./category_bar_{}.html".format(today))

    return attr_10,v1_10


def date_bar_without_version(df):
    
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
    bar.render("./date_bar_{}.html".format(today))

    
   

def patch_solution_table_drawer(df):
    
    df = df.drop_duplicates(subset = 'cveId')
    df = df[df['Patch'].str.encode('utf-8').str.contains('无补丁信息') == True]
    df = df[['cveId','Vulnerability Type','Date','描述']]
    df = df.sort_values(by = 'Date', ascending = False)
    df['cveId'] = df['cveId'].apply(lambda x:"<a href='https://nvd.nist.gov/vuln/detail/{}' target='_Blank' >{}</a>".format(x,x))

##    df['描述'] = df['描述'].apply(lambda x: x.encode('unicode-escape').decode('utf-8'))
##    df['描述'] = df['描述'].apply(str.encode('utf-8'))
    
##    df_count = df.groupby(['Patch']).size().reset_index(name='count')
    df.to_csv('./patch_ch_{}.csv'.format(today), encoding = 'utf-8')
##    df.to_string('patch_ch.txt', index = False, header ='Vulnerabilities without Patch')
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

    level_text = '''据{level[year]}年{level[month]}月{level[day]}日的扫描情况，共发现{level[sum_amount]}个漏洞,
其中高风险漏洞{level[high_level]}个，占总漏洞的{level[high_level_percentage]:.2f}%; 
中风险漏洞{level[medium_level]}个,占总漏洞的{level[medium_level_percentage]:.2f}%; 
低危漏洞{level[low_level]}个，占总漏洞的{level[low_level_percentage]:.2f}%.'''.format(level=level)


    category_text =  '''本次所扫描到的漏洞可根据风险类别分为以下主要10类, 高危漏洞类别按数量正序分布如下：
{0[9]}: {1[9]}个
{0[8]}: {1[8]}个
{0[7]}: {1[7]}个
{0[6]}: {1[6]}个
{0[5]}: {1[5]}个
{0[4]}: {1[4]}个
{0[3]}: {1[3]}个
{0[2]}: {1[2]}个
{0[1]}: {1[1]}个
{0[0]}: {1[0]}个'''.format(category_attr_10, category_value_10)

    date1 = {}

    date1_text = '本周/月安全漏洞发布趋势如下：\
                    xxx:xx个\
                    xxx:xx个'



    return level_text, category_text





def go_thierry():                                                                                      
    pd.set_option('display.max_colwidth', -1)
    start_time = time.time()
    data = data_grabber_with_version()
    df = table_drawer_with_version(data)
##    #1 按等级分类漏洞分布
    level_value, level_sum = level_pie_drawer_without_version(df)
##    #2 高威胁等级漏洞展示（高危等级按时间排序）
    table_drawer_with_high_level(df)
##    #3 按漏洞类别分类漏洞分布
    category_attr_10, category_value_10 = category_bar_without_version(df)
##    #4 展示无补丁漏洞（高危等级按时间排序）
    patch_solution_table_drawer(df)
##    #5 按时间显示漏洞数量
    date_bar_without_version(df)
    level_text, category_text = writter(df,level_value,level_sum, category_attr_10, category_value_10 )
    #print(text1)
    print(time.time() - start_time)

    #print("开始")
    print(level_text)
    print(category_text)
    return level_text, category_text
    

if __name__ == '__main__':
    go_thierry()

    








    
    
