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
import os
db_host = os.environ['db_host']
db_password = os.environ['db_password']
oss_host = os.environ['oss_host']
oss_password = os.environ['oss_password']
auth = oss2.Auth(oss_host, oss_password)
bucket = oss2.Bucket(auth, 'oss-cn-shanghai.aliyuncs.com', 'cti-pub-files')

def get_github(keywords):
    db = mysql.connector.connect(user='root',
                                 password='Bumble@20180628',
                                 host='rm-j6c9v62tlv18x957p.mysql.rds.aliyuncs.com',
                                 port='3306',
                                 database='github'
                                 )
    db.set_charset_collation('utf8')
    cursor = db.cursor()
    count = len(keywords)
    keystring = 'where github_keyWords = "' + str(keywords[0]) + '"'
    if count > 1:
        for key in keywords[1:]:
            keystring = keystring + 'or github_keyWords = "' + str(key) + '"'

    sql = '''select github_keyWords, github_author, github_htmlUrl, github_path,github_score,github_tags,github_description from  github_result %s and github_tags != 'no' and github_description != 'None' order by github_score desc limit 50;''' % keystring
    print(sql)
    cursor.execute(sql)
    dates = cursor.fetchall()
    datelist = []
    for date in dates:
        dic = {}

        dic['github_author'] = date[1]
        dic['github_htmlUrl'] = date[2]
        dic['github_path'] = date[3]
        dic['github_description'] = date[6]
        datelist.append(dic)
    try:
        db.commit()
    except:
        # if unexecuted, rollback
        db.rollback()
    print(len(datelist))
    return datelist


def get_weixin(keywords):
    db = mysql.connector.connect(user='root',
                                 password='Bumble@20180628',
                                 host='rm-j6c9v62tlv18x957p.mysql.rds.aliyuncs.com',
                                 port='3306',
                                 database='0_social_media'
                                 )
    db.set_charset_collation('utf8')
    cursor = db.cursor()
    count = len(keywords)
    keystring = 'where keyword = "' + str(keywords[0]) + '"'
    if count > 1:
        for key in keywords[1:]:
            keystring = keystring + 'or keyword = "' + str(key) + '"'

    sql = '''select title, content, nickname, link,date from  wechat %s order by date desc limit 50;''' % keystring
    print(sql)
    cursor.execute(sql)
    dates = cursor.fetchall()
    datelist = []
    for date in dates:
        dic = {}

        dic['title'] = date[0]
        # print(dic['title'])
        dic['content'] = date[1]
        dic['nickname'] = date[2]
        dic['link'] = date[3]
        dic['date'] = date[4]
        datelist.append(dic)

    try:
        db.commit()
    except:
        # if unexecuted, rollback
        db.rollback()
    print(len(datelist))
    return datelist

#(filename,report_id,request_id)
def write_html(filename, github_keywords, weixin_keywords,report_id,request_id):
    git_kw = github_keywords[0]
    wx_kw = weixin_keywords[0]
    if len(github_keywords) > 1:
        for git in github_keywords[1:]:
            git_kw = git_kw + '、' + str(git)
    if len(weixin_keywords) > 1:
        for wx in weixin_keywords[1:]:
            wx_kw = wx_kw + '、' + str(wx)

    github = get_github(github_keywords)
    # print(github)
    weixin = get_weixin(weixin_keywords)
    with open(filename, 'w') as f:

        f.write(
            '''<html class=" js flexbox flexboxlegacy webgl no-touch geolocation rgba hsla multiplebgs backgroundsize borderimage borderradius boxshadow textshadow opacity cssanimations csscolumns cssgradients cssreflections csstransforms csstransforms3d csstransitions fontface no-generatedcontent svg inlinesvg smil svgclippaths" lang="zh-cn" xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-cn" style="">\n''')
        f.write('''\n''')
        f.write('''<head>\n''')
        f.write('''    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n''')
        f.write('''    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">\n''')
        f.write('''    <meta name="viewport" content="width=device-width, initial-scale=1">\n''')
        f.write('''    <title>云雀数据安全威胁情报</title>\n''')
        f.write('''    <meta http-equiv="Content-Language" content="en">\n''')
        f.write(
            '''    <link rel="stylesheet" href="https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/css/style.css">\n''')
        f.write(
            '''    <link rel="stylesheet" href="https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/css/advisory-jquery-ui.min.css">\n''')
        f.write(
            '''    <link rel="stylesheet" href="https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/css/cookienotification.min.css">\n''')
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
        f.write(
            '''            <div class="eyscrollogo"><a href="#" class="logo"><img src="https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/skylark.png" alt="EY Ernst Young logo" border="0"></a></div>\n''')
        f.write('''            <section class="right clearfix"> </section>\n''')
        f.write('''        </div>\n''')
        f.write('''    </header>\n''')
        f.write(
            '''    <div class="eyhero hero-text-left" style="background-image: url(https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/pics/banner.jpg); background-size: cover; background-position: 80% 50%;">\n''')
        f.write('''        <div class="article-hero-container">\n''')
        f.write('''            <div class="headline-container frame3x2 box3x2 fluid-box ">\n''')
        f.write('''                <!-- add box3x2 class above for solid box -->\n''')
        f.write(
            '''                <svg viewBox="0 0 800 610" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:sketch="http://www.bohemiancoding.com/sketch/ns">\n''')
        f.write('''                    <defs>\n''')
        f.write('''                        <style type="text/css">\n''')
        f.write('''                        @font-face {\n''')
        f.write('''                            font-family: "Interstate", sans-serif;\n''')
        f.write(
            '''                            src: url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-2.eot");\n''')
        f.write(
            '''                            src: url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-2.eot?") format("embedded-opentype"), url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-3.woff") format("woff"), url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-1.ttf") format("truetype");\n''')
        f.write(
            '''                            src: url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-3.woff") format("woff");\n''')
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
        f.write(
            '''                        <filter x="-50%" y="-50%" width="200%" height="200%" filterUnits="objectBoundingBox" id="filter-1">\n''')
        f.write(
            '''                            <feOffset dx="0" dy="0" in="SourceAlpha" result="shadowOffsetOuter1"></feOffset>\n''')
        f.write(
            '''                            <feGaussianBlur stdDeviation="2.5" in="shadowOffsetOuter1" result="shadowBlurOuter1"></feGaussianBlur>\n''')
        f.write(
            '''                            <feColorMatrix values="0 0 0 0 0   0 0 0 0 0   0 0 0 0 0  0 0 0 0.35 0" in="shadowBlurOuter1" type="matrix" result="shadowMatrixOuter1"></feColorMatrix>\n''')
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
        f.write(
            '''                    <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd" sketch:type="MSPage">\n''')
        f.write('''                        <g id="3x2-frame" sketch:type="MSArtboardGroup">\n''')
        f.write(
            '''                            <g id="frames" sketch:type="MSLayerGroup" transform="translate(9.000000, 32.000000)">\n''')
        f.write(
            '''                                <g id="dots" transform="translate(1.000000, 511.000000)" fill="#FFE600" sketch:type="MSShapeGroup">\n''')
        f.write(
            '''                                    <rect id="Rectangle-2" x="0" y="0" width="12" height="12"></rect>\n''')
        f.write(
            '''                                    <rect id="0:0:0:0" x="42" y="0" width="12" height="12"></rect>\n''')
        f.write(
            '''                                    <rect id="0:0:0:0-copy" x="21" y="0" width="12" height="12"></rect>\n''')
        f.write('''                                </g>\n''')
        f.write(
            '''                                <path d="M22,115 L537,25.2818985 L537,427 L22,427 L22,115 Z" id="gradient" fill="url(#darkGradient)" sketch:type="MSShapeGroup"></path>\n''')
        f.write(
            '''                                <path d="M88,447 L113,447 L113,472 L88,472 L88,447 Z M44,447 L69,447 L69,472 L44,472 L44,447 Z M0,447 L25,447 L25,472 L0,472 L0,447 Z M130.955,446.766 L534.275,446.766 L534.275,30.151 L25.724,119.822 L25.724,428.874 L0.4993,428.874 L0.4993,98.656 L559.499,0.089 L559.499,471.99 L130.954,471.99 L130.955,446.766 Z" id="frame" fill="#FFE600" sketch:type="MSShapeGroup"></path>\n''')
        f.write(
            '''                                <path d="M0.499300892,98.567 L559.5,0 L559.5,471.901 L0,471.911 L0.499300892,98.567 Z" id="box" sketch:type="MSShapeGroup"></path>\n''')
        f.write(
            '''                                <path d="M0.000699708326,503.779999 L0.000699708326,130.601559 L745.004444,0 L745.004444,503.779699 L0,503.779699 L0.000699708326,503.779999 Z" id="4x2-box" sketch:type="MSShapeGroup"></path>\n''')
        f.write('''                            </g>\n''')
        f.write('''                        </g>\n''')
        f.write('''                    </g>\n''')
        f.write('''                </svg>\n''')
        f.write('''                <div class="smartquestion">\n''')
        f.write('''                    <div class="heading-block fluid-type">\n''')
        f.write('''                        <h1 class="eyhero-headline-1">云雀数据安全威胁情报<br>感知、抵御、应对</h1>\n''')

        days1 = datetime.date(2018, 07, 01)
        days2 = datetime.date.today()
        num = (days2 - days1).days
        weeks = num // 7 + 1

        f.write('''                        <h2 class="eyhero-subheading-1">安永2018年数据安全情报第%s周</h2> </div>\n''' % weeks)

        f.write('''                </div>\n''')
        f.write('''                <div class="status">status</div>\n''')
        f.write('''            </div>\n''')
        f.write('''        </div>\n''')
        f.write('''    </div>\n''')
        f.write('''</head>\n''')
        f.write('''<article class="article type-system-ey ">\n''')
        f.write(
            '''    <section class="section0" id="section0" data-section-title="漏洞级别概况及目录" style="background-color:#F0F0F0">\n''')
        f.write('''        <div class="container">\n''')
        f.write('''            <aside id="scroll-on-page-top" class="article-subnav">\n''')
        f.write('''                <ul id="featuremenu">\n''')
        f.write('''                    <li id="feature01"><a href="#maincolumn">社交网络</a></li>\n''')
        f.write('''                    <li id="feature02"><a href="#section2">开源社区</a></li>\n''')
        f.write('''                    <li id="feature03"><a href="#section4">搜索引擎</a></li>\n''')
        f.write('''                </ul>\n''')
        f.write('''            </aside>\n''')
        f.write('''         \n''')
        f.write(
            '''    <section class="section1" id="section1" data-section-title="社交网络" style="background-color:#F0F0F0">\n''')
        f.write('''        <div class="container">\n''')
        f.write('''            <div class="row">\n''')
        f.write('''                <div class="col large-9">\n''')
        f.write('''                    <h3>社交网络</h3> \n''')

        f.write('''                <p>我们根据%s关键词在微博和微信等社交网络上进行检索，检索结果如下：</p></div>\n''' % wx_kw)
        f.write('''                    \n''')
        f.write('''            </div>\n''')
        f.write('''\n''')
        f.write('''            <div class="row">\n''')
        f.write('''                <div class="col large-9">\n''')
        f.write('''  
                           \n''')
        for index, wx in enumerate(weixin):
            # print('title')
            # print(wx['title'])
            ##            try :
            ##                wx_title = wx['title'].decode('utf-8')
            ##            except:
            ##                wx_title = wx['title']
            # print(wx_title)
            # http://weixin.sogou.com/weixin?type=2&query=%E4%BA%91%E8%AE%A1%E7%AE%97%E5%AE%89%E5%85%A8%E7%9A%84%E4%BA%94%E4%B8%AA%E9%98%B6%E6%AE%B5&ie=utf8&s_from=input&_sug_=y&_sug_type_=
            link = 'http://weixin.sogou.com/weixin?type=2&query=' + wx[
                'title'] + '&ie=utf8&s_from=input&_sug_=y&_sug_type_='
            f.write('''                    <p><a href="%s" target="_blank">%d.%s</a></p>\n''' % (
            link, index + 1, wx['title']))
            # print(wx['content'][:200])
            f.write('''                                <p>公众号名称：%s</p>\n''' % wx['nickname'])
            f.write('''                                <p>时间：%s</p>\n''' % wx['date'])
            f.write('''                                <p>摘要：%s...</p>\n''' % wx['content'][:200])

        f.write('''                </div>\n''')
        f.write('''                <!-- <div class="col large-3">  </div> --></div>\n''')
        f.write('''        </div>\n''')
        f.write('''    </section>\n''')
        f.write(
            '''    <section class="section2" id="section2" data-section-title="开源社区" style="background-color:#F0F0F0">\n''')
        f.write('''        <div class="container">\n''')
        f.write('''            <div class="row">\n''')
        f.write('''                <div class="col large-9">\n''')
        f.write('''                    <h3>开源社区</h3> \n''')
        f.write('''                <p>我们根据%s关键词在github开源社区上进行检索，检索结果如下：</p></div>\n''' % git_kw)

        f.write('''                    \n''')
        f.write('''            </div>\n''')
        f.write('''            <div class="row">\n''')
        f.write('''                <div class="col large-9">\n''')
        f.write('''                    \n''')

        for index, gith in enumerate(github):
            print('here')
            f.write('''                    <p><a href="%s" target="_blank">%d.%s</a></p>\n''' % (
            gith['github_htmlUrl'], index + 1, gith['github_path']))
            f.write('''                                <p>作者：%s</p>\n''' % gith['github_author'])
            f.write('''                                <p>摘要：%s...</p>\n''' % gith['github_description'])

        f.write('''                    <!-- <div class="col large-3">  </div> --></div>\n''')
        f.write('''            </div>\n''')
        f.write('''    </section>\n''')
        f.write(
            '''    <section class="section4" id="section4" data-section-title="搜索引擎" style="background-color:#F0F0F0">\n''')
        f.write('''        <div class="container">\n''')
        f.write('''            <div class="row">\n''')
        f.write('''                <div class="col large-9">\n''')
        f.write('''                    <h3>搜索引擎</h3> \n''')
        f.write('''                 <p>我们根据*************关键词在google等搜索引擎上进行检索，检索结果如下：</p></div>\n''')
        f.write('''            </div>\n''')
        f.write('''            <div class="row">\n''')
        f.write('''                <div class="col large-9">\n''')
        f.write(
            '''                    <p><a href="https://blog.trendmicro.com/trendlabs-security-intelligence/drupal-vulnerability-cve-2018-7602-exploited-to-deliver-monero-mining-malware/" target="_blank">1.Drupal Vulnerability (CVE-2018-7602) Exploited to Deliver Monero-Mining Malware</a></p>\n''')
        f.write('''\n''')
        f.write(
            '''<p>摘要：We were able to observe a series of network attacks exploiting CVE-2018-7602, a security flaw in the Drupal content management framework. For now, these attacks aim to turn affected systems into... </p>\n''')
        f.write(
            '''<p><a href="https://blog.trendmicro.com/trendlabs-security-intelligence/another-potential-muddywater-campaign-uses-powershell-based-prb-backdoor/" target="_blank">2.Another Potential MuddyWater Campaign uses Powershell-based PRB-Backdoor</a></p>\n''')
        f.write('''\n''')
        f.write(
            '''<p>摘要：we found a new sample that may be related to the MuddyWater campaign. Like the previous campaigns, these samples again involve a Microsoft Word document embedded with a malicious macro ...</p>\n''')
        f.write(
            '''<p><a href="https://blog.trendmicro.com/trendlabs-security-intelligence/confucius-update-new-tools-and-techniques-further-connections-with-patchwork/" target="_blank">3.Confucius Update: New Tools and Techniques, Further Connections with Patchwork</a></p>\n''')
        f.write('''\n''')
        f.write(
            '''<p>摘要：We look into the latest tools and techniques used by Confucius, as the threat actor seems to have a new modus operandi, setting up two new websites and new payloads with which to compromise its targets...</p>\n''')
        f.write(
            '''<p><a href="https://blog.trendmicro.com/trendlabs-security-intelligence/another-potential-muddywater-campaign-uses-powershell-based-prb-backdoor/" target="_blank">4.Another Potential MuddyWater Campaign uses Powershell-based PRB-Backdoor</a></p>\n''')
        f.write('''\n''')
        f.write(
            '''<p>摘要：we found a new sample that may be related to the MuddyWater campaign. Like the previous campaigns, these samples again involve a Microsoft Word document embedded with a malicious macro that is ...</p>\n''')
        f.write(
            '''<p><a href="https://blog.trendmicro.com/trendlabs-security-intelligence/confucius-update-new-tools-and-techniques-further-connections-with-patchwork/" target="_blank">5.Confucius Update: New Tools and Techniques, Further Connections with Patchwork</a></p>\n''')
        f.write('''\n''')
        f.write(
            '''<p>摘要：We look into the latest tools and techniques used by Confucius, as the threat actor seems to have a new modus operandi, setting up two new websites and new payloads with which to compromise its targets...</p>\n''')
        f.write('''                </div>\n''')
        f.write(
            '''                <!-- <div class="col large-3"><img title="安永第19届全球信息安全调查报告" alt="安永第19届全球信息安全调查报告" src="https://cti-pub-files.oss-cn-shanghai.aliyuncs.com/pics/53-rs.png"></div> --></div>\n''')
        f.write('''        </div>\n''')
        f.write('''    </section>\n''')
        f.write('''</article>\n''')
        f.write('''<footer class="footer" id="footer" role="contentinfo">\n''')
        f.write('''    <div class="footer-logo">\n''')
        f.write('''        <div class="footer-links"></div>\n''')
        f.write(
            '''        <p class="detail">声明：以上内容均来自互联网，由CTI网络威胁情报团队整理，其版权归属原作者所有，其观点并不代表我方观点和意见，请酌情参考或采用。若对以上所引用内容有任何疑问或问题，请与services@eycyber.com联系。</p>\n''')
        f.write('''    </div>\n''')
        f.write('''</footer>\n''')
        f.write('''</body>\n''')
        f.write('''\n''')
        f.write('''</html>\n''')
    with open('datesecurity.html', 'rb') as fileobj:
        directory = report_id + '/datesecurity.html'
        result = bucket.put_object(directory,fileobj)

def main():
    write_html('datesecurity.html', ['Lancome', 'Armani'], ['GDPR', '云安全'],'测试机','测试机')


if __name__ == '__main__':
    main()
