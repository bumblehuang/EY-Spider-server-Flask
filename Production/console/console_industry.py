#encoding: utf-8
import re
import mysql.connector
import oss2
import csv
import sys
import datetime
reload(sys)
sys.setdefaultencoding('utf-8') 
import requests
from console_visualizer import go_thierry
import os
db_host = os.environ['db_host']
db_password = os.environ['db_password']
oss_host = os.environ['oss_host']
oss_password = os.environ['oss_password']
auth = oss2.Auth(oss_host, oss_password)
bucket = oss2.Bucket(auth, 'oss-cn-shanghai.aliyuncs.com', 'cti-pub-files')


#with open('ey_cti_cn_rpt2.html', 'r') as f1:
#        list1 = f1.readlines()
#with open('test.html', 'w') as f:
#    for i in list1:
#        i = re.sub(r'\n','',i)
#        f.write('''f.write(\'\'\'%s\'\'\')\n''' % i)
def getnews(category):

    db = mysql.connector.connect(user='root',
                                 password=db_password,
                                 host=db_host,
                                 port='3306',
                                 database='0_news'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()
    #sql = '''alter table trendmicro_hash1 add column news_industry varchar(255) not null;'''
    #cursor.execute(sql)
    ####增加行业
    finance = ['finance','bank','corporate', 'investment', 'group','Share', 'enterprise', 'price','Economic' ,'asset', 'financing']
    science = ['Huawei', 'xiaomi', 'samsung', 'technology' ,'traffic', 'unicom', 'telecom', 'jd', 'Internet', 'ios', 'tencent', 'alibaba']
    sql = '''select news_category, news_hash, news_industry from trendmicro_hash1 where news_industry = '';'''

    cursor.execute(sql)
    dates = cursor.fetchall()

    for row in dates:
        if re.findall(r'finance|bank|corporate|investment|group|Share|enterprise|price|Economic|asset|financing',row[0]) != []:
            industry = 'finance'
        elif re.findall(r'Huawei|xiaomi|samsung|technology|traffic|unicom|telecom|jd|Internet|ios|tencent|alibaba',row[0]) != []:
            industry = 'science'
        else:
            industry = 'retail'
        hashvalue = row[1]
        sql2 = '''update trendmicro_hash1 set news_industry = '%s' where news_hash = '%s';'''%(industry,hashvalue)
        cursor.execute(sql2)


    ####选数据
    sql3 = '''select news_title, news_publishedTime, news_author, news_briefContent ,news_link,news_industry from trendmicro_hash1 where news_industry = '%s'  ORDER BY news_publishedTime DESC limit 3;'''%(category)
    #select news_category ,news_hash, news_industry,news_publishedTime from trendmicro_hash where news_industry = 'finance'  ORDER BY news_publishedTime DESC limit 3

    cursor.execute(sql3)
    results = cursor.fetchall()
    title = []
    time = []
    author = []
    briefContent = []
    link = []
    for row in results:
        title.append(row[0])
        time.append(row[1])
        author.append(row[2])
        briefContent.append(row[3])
        link.append(row[4])

    dicts = {}
    dicts['title'] = title
    dicts['time'] = time
    dicts['author'] = author
    dicts['briefContent'] = briefContent
    dicts['link'] = link
    try:
        db.commit()
    except:
        # if unexecuted, rollback
        db.rollback()
    return dicts




def write_html(filename,report_id,request_id):
    text1,text2 = go_thierry(report_id,request_id)
    list1 = csv.reader(open('./high_level.csv', 'r'))
    list2 = csv.reader(open('./patch_ch.csv', 'r'))
    finance = getnews('finance')
    #print(finance)
    science = getnews('science')
    #print(science)
    retail = getnews('retail')

    # text1,text2 = go_thierry()
    # response = requests.get('http://cti-pub-files.oss-cn-shanghai.aliyuncs.com/pages/patch.html')
    # html = response.text
    # list1 = re.findall(r'.*?\n', html)




    # #with open("http://cti-pub-files.oss-cn-shanghai.aliyuncs.com/pages/high_level.html", 'r') as f2:
    #     #list2 = f2.readlines()

    # response2 = requests.get('http://cti-pub-files.oss-cn-shanghai.aliyuncs.com/pages/high_level.html')
    # html2 = response2.text
    # list2 = re.findall(r'.*?\n', html2)



    #response3 = requests.get('http://cti-pub-files.oss-cn-shanghai.aliyuncs.com/pages/patch.html')
    #html3 = response3.text
    #list3 = re.findall(r'.*?\n', html3)

    #with open("./para1.txt", 'r') as f3:
        #list3 = f3.readlines()
    #response = requests.get('http://cti-pub-files.oss-cn-shanghai.aliyuncs.com/para1.txt')
    #all_text = response.text
    #list3= re.findall(r'.*?\n',all_text)
    #last_txt = re.findall(r'File Inclusion.*',all_text)


    with open(filename, 'w') as f:
        


        f.write('''<html class=" js flexbox flexboxlegacy webgl no-touch geolocation rgba hsla multiplebgs backgroundsize borderimage borderradius boxshadow textshadow opacity cssanimations csscolumns cssgradients cssreflections csstransforms csstransforms3d csstransitions fontface no-generatedcontent svg inlinesvg smil svgclippaths" lang="zh-cn" xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-cn" style="">\n''')
        f.write('''<head>\n''')
        f.write('''    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n''')
        f.write('''    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">\n''')
        f.write('''    <meta name="viewport" content="width=device-width, initial-scale=1">\n''')
        f.write('''    <title>云雀网络安全行业威胁情报</title>\n''')
        f.write('''    <meta http-equiv="Content-Language" content="en">\n''')
        f.write('''    <link rel="stylesheet" href="https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/css/style.css">\n''')
        f.write('''    <link rel="stylesheet" href="https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/css/advisory-jquery-ui.min.css">\n''')
        f.write('''    <link rel="stylesheet" href="https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/css/cookienotification.min.css">\n''')
        f.write('''    <style>\n''')
        f.write('''        .contact-us-cnt h3 {\n''')
        f.write('''        border-left: 5px solid #ffe400;\n''')
        f.write('''        padding: 5px;\n''')
        f.write('''        background: #f7f7f7;\n''')
        f.write('''        font-size: 1.8em;\n''')
        f.write('''        margin-top: 10px;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    .modal .modal-inner {\n''')
        f.write('''        max-width: 1000px;\n''')
        f.write('''    }\n''')
        f.write('''\n''')
        f.write('''    .modal-content img {\n''')
        f.write('''        max-width: 1100px !important;\n''')
        f.write('''        margin: 30px auto;\n''')
        f.write('''        display: block;\n''')
        f.write('''    </style>\n''')
        f.write('''    <header class="main-header">\n''')
        f.write('''        <div class="container">\n''')
        f.write('''            <div class="eyscrollogo"><a href="#" class="logo"><img src="https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/pics/careers_ey_logo_zh_CN.png" alt="EY Ernst Young logo" border="0"></a></div>\n''')
        f.write('''            <section class="right clearfix"> </section>\n''')
        f.write('''        </div>\n''')
        f.write('''    </header>\n''')
        f.write('''    <div class="eyhero hero-text-left" style="background-image: url(https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/pics/banner.jpg); background-size: cover; background-position: 80% 50%;">\n''')
        f.write('''        <div class="article-hero-container">\n''')
        f.write('''            <div class="headline-container frame3x2 box3x2 fluid-box ">\n''')
        f.write('''                <!-- add box3x2 class above for solid box -->\n''')
        f.write('''                <svg viewBox="0 0 800 610" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:sketch="http://www.bohemiancoding.com/sketch/ns">\n''')
        f.write('''                    <defs>\n''')
        f.write('''                        <style type="text/css">\n''')
        f.write('''                        @font-face {\n''')
        f.write('''                            font-family: "Interstate", sans-serif;\n''')
        f.write('''                            src: url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-2.eot");\n''')
        f.write('''                            src: url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-2.eot?") format("embedded-opentype"), url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-3.woff") format("woff"), url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-1.ttf") format("truetype");\n''')
        f.write('''                            src: url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-3.woff") format("woff");\n''')
        f.write('''                        }\n''')
        f.write('''\n''')
        f.write('''                        [id^="tagline-"] {\n''')
        f.write('''                            font-family: "Interstate";\n''')
        f.write('''                            fill: #ffffff;\n''')
        f.write('''                            letter-spacing: 1px;\n''')
        f.write('''                            font-size: 24px;\n''')
        f.write('''                            letter-spacing: -.03em;\n''')
        f.write('''                        }\n''')
        f.write('''                        </style>\n''')
        f.write('''                        <filter x="-50%" y="-50%" width="200%" height="200%" filterUnits="objectBoundingBox" id="filter-1">\n''')
        f.write('''                            <feOffset dx="0" dy="0" in="SourceAlpha" result="shadowOffsetOuter1"></feOffset>\n''')
        f.write('''                            <feGaussianBlur stdDeviation="2.5" in="shadowOffsetOuter1" result="shadowBlurOuter1"></feGaussianBlur>\n''')
        f.write('''                            <feColorMatrix values="0 0 0 0 0   0 0 0 0 0   0 0 0 0 0  0 0 0 0.35 0" in="shadowBlurOuter1" type="matrix" result="shadowMatrixOuter1"></feColorMatrix>\n''')
        f.write('''                            <feMerge>\n''')
        f.write('''                                <feMergeNode in="shadowMatrixOuter1"></feMergeNode>\n''')
        f.write('''                                <feMergeNode in="SourceGraphic"></feMergeNode>\n''')
        f.write('''                            </feMerge>\n''')
        f.write('''                        </filter>\n''')
        f.write('''                        <linearGradient x1="50%" y1="0%" x2="50%" y2="100%" id="darkGradient">\n''')
        f.write('''                            <stop stop-color="#000000" stop-opacity="0.6" offset="0%"></stop>\n''')
        f.write('''                            <stop stop-color="#000000" stop-opacity="0" offset="100%"></stop>\n''')
        f.write('''                        </linearGradient>\n''')
        f.write('''                        <linearGradient x1="50%" y1="0%" x2="50%" y2="100%" id="lightGradient">\n''')
        f.write('''                            <stop stop-color="#ffffff" stop-opacity="0.6" offset="0%"></stop>\n''')
        f.write('''                            <stop stop-color="#ffffff" stop-opacity="0" offset="100%"></stop>\n''')
        f.write('''                        </linearGradient>\n''')
        f.write('''                    </defs>\n''')
        f.write('''                    <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd" sketch:type="MSPage">\n''')
        f.write('''                        <g id="3x2-frame" sketch:type="MSArtboardGroup">\n''')
        f.write('''                            <g id="frames" sketch:type="MSLayerGroup" transform="translate(9.000000, 32.000000)">\n''')
        f.write('''                                <g id="dots" transform="translate(1.000000, 511.000000)" fill="#FFE600" sketch:type="MSShapeGroup">\n''')
        f.write('''                                    <rect id="Rectangle-2" x="0" y="0" width="12" height="12"></rect>\n''')
        f.write('''                                    <rect id="0:0:0:0" x="42" y="0" width="12" height="12"></rect>\n''')
        f.write('''                                    <rect id="0:0:0:0-copy" x="21" y="0" width="12" height="12"></rect>\n''')
        f.write('''                                </g>\n''')
        f.write('''                                <path d="M22,115 L537,25.2818985 L537,427 L22,427 L22,115 Z" id="gradient" fill="url(#darkGradient)" sketch:type="MSShapeGroup"></path>\n''')
        f.write('''                                <path d="M88,447 L113,447 L113,472 L88,472 L88,447 Z M44,447 L69,447 L69,472 L44,472 L44,447 Z M0,447 L25,447 L25,472 L0,472 L0,447 Z M130.955,446.766 L534.275,446.766 L534.275,30.151 L25.724,119.822 L25.724,428.874 L0.4993,428.874 L0.4993,98.656 L559.499,0.089 L559.499,471.99 L130.954,471.99 L130.955,446.766 Z" id="frame" fill="#FFE600" sketch:type="MSShapeGroup"></path>\n''')
        f.write('''                                <path d="M0.499300892,98.567 L559.5,0 L559.5,471.901 L0,471.911 L0.499300892,98.567 Z" id="box" sketch:type="MSShapeGroup"></path>\n''')
        f.write('''                                <path d="M0.000699708326,503.779999 L0.000699708326,130.601559 L745.004444,0 L745.004444,503.779699 L0,503.779699 L0.000699708326,503.779999 Z" id="4x2-box" sketch:type="MSShapeGroup"></path>\n''')
        f.write('''                            </g>\n''')
        f.write('''                        </g>\n''')
        f.write('''                    </g>\n''')
        f.write('''                </svg>\n''')
        f.write('''                <div class="smartquestion">\n''')
        f.write('''                    <div class="heading-block fluid-type">\n''')
        f.write('''                        <h1 class="eyhero-headline-1">云雀网络安全行业威胁情报<br>感知、抵御、应对</h1>\n''')
        days1 = datetime.date(2018, 07, 01)
        days2 = datetime.date.today()
        num = (days2-days1).days
        weeks = (num//7)+1
        f.write('''                        <h2 class="eyhero-subheading-1">云雀网络安全行业威胁情报(第%s周)</h2> </div>\n'''%weeks)
        f.write('''                </div>\n''')
        f.write('''                <div class="status">status</div>\n''')
        f.write('''            </div>\n''')
        f.write('''        </div>\n''')
        f.write('''    </div>\n''')
        f.write('''</head>\n''')



        f.write('''<article class="article type-system-ey "> <section class="section0" id="section0" data-section-title="漏洞级别概况及目录" style="background-color:#F0F0F0"> <div class="container"><aside id="scroll-on-page-top" class="article-subnav"><ul id="featuremenu"><li id="feature01"><a href="#maincolumn">漏洞级别</a></li><li id="feature02"><a href="#section2">漏洞类别</a></li><li id="feature03"><a href="#section4">漏洞补丁</a></li><li id="feature04"><a href="#section6">漏洞关系</a></li><li id="feature05"><a href="#section8">漏洞趋势</a></li></ul></aside><div class="maincolumn"><h3>本周安全漏洞级别概况</h3>''')
        #f.write('''<p>根据2018年X月第X周的扫描情况，共发现xx个漏洞，</p><p>其中高风险漏洞XX个，占总漏洞数的xx%；中风险漏洞XX个，低危漏洞XX个。</p>''')
        #for list_each3 in list3[:4]:
         #   f.write('''<p>%s</p>''' % list_each3)
        f.write('''<p>%s</p>''' % text1)
        f.write('''<p><iframe src="https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/%s/pie.html" width=800px  height=380px  frameborder="0"  scrolling="no"></iframe><h3>High risk vulnerability</h3>'''%report_id)
        # f.write('''<table border="1" class="dataframe">''')
        # f.write('''<thead>''')
        # f.write('''<tr style="text-align: right;">''')
        # f.write('''<th id=thc1>cveId</th>''')
        # f.write('''<th id=thc2>Vulnerability Type</th>''')
        # f.write('''<th id=thc3>Date</th>''')
        # f.write('''<th id=thc4>Description</th>''')
        # f.write('''</tr>''')
        # f.write('''</thead>''')

        # for list_each1 in list1[8:]:
        #     f.write('''%s''' % list_each1)
        # f.write('''</table>''')
        i = 0
        for stu_cell in list1:
            # print(stu_cell)
            if i != 0:
                print(i)
                print(stu_cell[1])
                f.write('''<tr>''')
                f.write('''<td>%s</td>\n''' % stu_cell[1])
                f.write('''<td>%s</td>\n''' % stu_cell[2])
                f.write('''<td>%s</td>\n''' % stu_cell[3])
                f.write('''<td>%s</td>\n''' % stu_cell[4])
                f.write('''</tr>''')
                i += 1
            else:
                # print(stu_cell[1])
                # print(i)
                f.write('<table border="1" class="dataframe">\n')
                f.write('<thead>\n')
                f.write('<tr style="text-align: right;">\n')

                f.write('<th id=thc1>%s</th>\n' % stu_cell[1])
                f.write('<th id=thc2>%s</th>\n' % stu_cell[2])
                f.write('<th id=thc3>%s</th>\n' % stu_cell[3])
                f.write('<th id=thc4>%s</th>\n' % stu_cell[4])
                f.write('</tr>\n')
                f.write('</thead>\n')
             
                i += 1
       
        f.write('''</tbody>\n''')
        f.write('''</table>\n''')




        #f.write('''%s''' % list1)
        f.write('''</p></div></div></section><section class="section2" id="section2" data-section-title="漏洞类别" style="background-color:#F0F0F0">''')
        f.write(''' <div class="container"><div class="row"><div class="col large-9"><h3>漏洞类别</h3> </div></div><div class="row"><div class="col large-9">''')
        
        #for list_each3 in list3[5:]:
            #f.write('''<p>%s</p>''' % list_each3)
        f.write('''<p>%s</p>''' % text2)
        f.write('''<iframe src="https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/%s/bar1.html"'''%report_id)
        #f.write('''<p>%s</p>''' % list3[1])


        f.write('''width="750" height="420" scrolling="no" frameborder="0"></iframe>''')
        f.write('''     ''')
        f.write('''     <!-- <div class="col large-3">  </div> --></div></div></section><section class="section4" id="section4" data-section-title="漏洞补丁" style="background-color:#F0F0F0"><div class="container"><div class="row"><div class="col large-9"><h3>金融行业数据风险事件</h3> </div></div><div class="row"><div class="col large-9">''')
        #for list_each in list2:
            #f.write('''%s''' % list_each)
        for i in range(3):
            #<a href="链接的页面" target="_blank">新窗口打开</a>
            #f.write('''<p>%d.%s</p>''' % (i+1,finance['title'][i]))

            f.write('''<p><a href="%s" target="_blank">%d.%s</a></p>''' % (finance['link'][i],i + 1, finance['title'][i]))
            f.write('''<p>时间：%s</p>''' % finance['time'][i])
            f.write('''<p>作者：%s</p>''' % finance['author'][i])
            f.write('''<p>事件概要：%s</p>''' % finance['briefContent'][i])
        #f.write('''*********************''')
        f.write('''</div>''')
        f.write('''         <!-- <div class="col large-3">  </div> --></div></div></section><section class="section4" id="section4" data-section-title="漏洞补丁" style="background-color:#F0F0F0"><div class="container"><div class="row"><div class="col large-9"><h3>科技行业数据风险事件</h3> </div></div><div class="row"><div class="col large-9">''')

        for i in range(3):
            #f.write('''<p>%d.%s</p>''' % (i+1,science['title'][i]))
            f.write('''<p><a href="%s" target="_blank">%d.%s</a></p>''' % (science['link'][i], i + 1, science['title'][i]))
            f.write('''<p>时间：%s</p>''' % science['time'][i])
            f.write('''<p>作者：%s</p>''' % science['author'][i])
            f.write('''<p>事件概要：%s</p>''' % science['briefContent'][i])

        #f.write('''********************''')
        f.write('''         <!-- <div class="col large-3">  </div> --></div></div></section><section class="section4" id="section4" data-section-title="漏洞补丁" style="background-color:#F0F0F0"><div class="container"><div class="row"><div class="col large-9"><h3>新零售行业数据风险事件</h3> </div></div><div class="row"><div class="col large-9">''')

        for i in range(3):
            #f.write('''<p>%d.%s</p>''' % (i+1,retail['title'][i]))
            f.write('''<p><a href="%s" target="_blank">%d.%s</a></p>''' % (retail['link'][i], i + 1, retail['title'][i]))
            f.write('''<p>时间：%s</p>''' % retail['time'][i])
            f.write('''<p>作者：%s</p>''' % retail['author'][i])
            f.write('''<p>事件概要：%s</p>''' % retail['briefContent'][i])
        #f.write('''********************''')
        f.write('''</div><!-- <div class="col large-3"><img title="安永第19届全球信息安全调查报告" alt="安永第19届全球信息安全调查报告" src="https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/pics/53-rs.png"></div> --></div></div></section>''')
        f.write('''    </article>\n''')
        f.write('''    <footer class="footer" id="footer" role="contentinfo">\n''')
        f.write('''        <div class="footer-logo">\n''')
        f.write('''            <div class="footer-links"></div>\n''')
        f.write('''            <p class="detail">声明：以上内容均来自互联网，由CTI网络威胁情报团队整理，其版权归属原作者所有，其观点并不代表我方观点和意见，请酌情参考或采用。若对以上所引用内容有任何疑问或问题，请与jacob.mhj@gmail.com联系。</p>\n''')
        f.write('''        </div>\n''')
        f.write('''    </footer>\n''')
        f.write('''    </body>\n''')
        f.write('''\n''')
        f.write('''</html>\n''')
    with open('report-v16.html', 'rb') as fileobj:
        directory = report_id + '/report-v16.html'
        result = bucket.put_object(directory,fileobj)

def main():


   # min=0,max=0,month=5,year=2018
    ##    cursor,db = ConnectSQL()
    #headers = COOKIES('http://www.cnvd.org.cn/flaw/list.htm?flag=true?number=%E8%AF%B7%E8%BE%93%E5%85%A5%E7%B2%BE%E7%A1%AE%E7%BC%96%E5%8F%B7&startDate=&endDate=&flag=true&field=&order=&max=20&offset=0')
        #print(retail)
    write_html('test_16.html','测试机','测试机')
    

if __name__ == '__main__':
    main()
