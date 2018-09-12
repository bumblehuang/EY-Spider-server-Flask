
#https://www.securityfocus.com/cgi-bin/index.cgi?o=30&l=30&c=12&op=display_list&vendor=&version=&title=&CVE=
#https://www.securityfocus.com/cgi-bin/index.cgi?o=30&l=30&c=12&op=display_list&vendor=&version=&title=&CVE=
#https://www.securityfocus.com/cgi-bin/index.cgi?o=90&l=30&c=12&op=display_list&vendor=&version=&title=&CVE=
#https://www.securityfocus.com/cgi-bin/index.cgi?o=120&l=30&c=12&op=display_list&vendor=&version=&title=&CVE=
import hashlib
from lxml import etree
import re
import mysql.connector
import requests
#url = 'https://www.securityfocus.com/cgi-bin/index.cgi?o=120&l=30&c=12&op=display_list&vendor=&version=&title=&CVE='
#response = requests.get(url,timeout=30)
#print(response.status_code)
#print(response.text)

def Urlcreator(first_page, page):
    url_firstPage = []
    url_page_list = []
    url_page = []
    url_firstPage.append(
        "https://www.securityfocus.com/cgi-bin/index.cgi?o=0&l=30&c=12&op=display_list&vendor=&version=&title=&CVE="
    )

    url_page_list.append(url_firstPage[-1])
    for i in range(first_page + 1, page + 1):
        url_page_list.append(
            "https://www.securityfocus.com/cgi-bin/index.cgi?o=" + str(i * 30) +"&l=30&c=12&op=display_list&vendor=&version=&title=&CVE="
        )

    print(url_page_list)
    for i in url_page_list:
        response = requests.get(i, timeout = 30)
        html = response.content
        selector = etree.HTML(html)

        # //*[@id="vulner_0"]/p/a
        # //*[@id="vulner_1"]/p/a
        # /html/body/div[5]/div[1]/div/div[2]/table/tbody/tr[1]/td[1]/a
        focus_list = selector.xpath('//*[@id="article_list"]//div[2]//a')
        #print(focus_list)
        for index, row in enumerate(focus_list):
            #print(row.xpath('//*[@id="article_list"]//div[2]//a[' + str(index + 1) + ']'))
            if row.xpath('//*[@id="article_list"]//div[2]//a[' + str(index+ 1)+ ']') != []:
                allurl_ = row.xpath('//*[@id="article_list"]//div[2]//a[' + str(index+ 1) + ']')[0].text
                url_page.append(allurl_)
    url_page = [a for a in url_page if a not in [None]]
    print(len(url_page))
    return url_page

def scrapper(url_page_list):
    db = mysql.connector.connect(user='root',
                                 password='Test@20180604',
                                 host='rm-j6cx1z86d86308x6m.mysql.rds.aliyuncs.com',
                                 port='3306',
                                 database='vulnerabilities'
                                 )

    # set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()
    data_list=[]
    for index, url in enumerate(url_page_list):
        print(url)
        print(index)
        response = requests.get(url, timeout=30)
        html = response.content
        selector = etree.HTML(html)

        print(response.status_code)

        try:
            table_rows = selector.xpath('//*[@id="vulnerability"]//table//tr')
        except Exception as e:
            pass

        try:
            title = selector.xpath('//*[@id="vulnerability"]//span')[0].text
        except Exception as e:
            title = 'None'
        dic = {'title': title, 'BugtraqID:': 'None', 'Class:': 'None', 'CVE:': 'None', 'Remote:': 'None',
               'Local:': 'None',
               'Published:': 'None', 'Updated:': 'None',
               'Credit:': 'None', 'Vulnerable:': 'None', 'NotVulnerable:': 'None'}

        for inde, row in enumerate(table_rows):

            td_1 = row.xpath(
                '//*[@id="vulnerability"]//table//tr[' + str(inde + 1) + ']//td[1]')[
                0].xpath('string()')
            td_1 = re.sub(r'\s', '', td_1)
            td_1 = td_1.encode('utf-8')
            if td_1 in dic:
                td_2 = row.xpath('//*[@id="vulnerability"]//table//tr[' + str(inde + 1) + ']//td[2]')[0].xpath(
                    'string()')
                td_2 = re.sub(r'\s+', ' ', td_2)
                td_2 = re.sub(r'(^\s)|(\s$)', '', td_2)
                dic[td_1] = td_2


        hash_string = dic['CVE:'].encode('utf-8') + dic['BugtraqID:'].encode('utf-8') + dic['title'].encode('utf-8') + dic['Published:'].encode('utf-8')

        sha1 = hashlib.sha1()
        sha1.update(hash_string)
        hashvalue = sha1.hexdigest()
        data_list.append(dic)

        
    headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
    receive1=requests.post("http://cti_hk_cns00.eycyber.com:8080/cnvd_data",data=json.dumps(data_list),headers=headers)

def main():
    # min=0,max=0,month=5,year=2018
    ##    cursor,db = ConnectSQL()
    #headers = COOKIES('http://www.cnvd.org.cn/flaw/list.htm?flag=true?number=%E8%AF%B7%E8%BE%93%E5%85%A5%E7%B2%BE%E7%A1%AE%E7%BC%96%E5%8F%B7&startDate=&endDate=&flag=true&field=&order=&max=20&offset=0')
    url_page = Urlcreator(1, 5)
    scrapper(url_page)


if __name__ == '__main__':
    main()
