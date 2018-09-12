
import requests
from lxml import etree
import csv
import ssl
import mysql.connector
import hashlib




    
def Urlcreator(min,max,vendor_id,product_id,version_id,first_page, page):
    # user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    # headers={"User-Agent":user_agent}
    url_firstPage= []
    url_page = []


    url_firstPage.append("https://www.cvedetails.com/vulnerability-list.php?vendor_id="+str(vendor_id)+"&product_id="+str(product_id)+"&version_id="+str(version_id)+"&page="+str(first_page)+"&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0\
        &opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin="+str(min)+"&cvssscoremax="+str(max)+"&year=0&month=0&cweid=0&order=1&trc=101161&sha=3cf9994d68386594f1283fc226cf51dad5fe72b8"
                         )


    
    html = requests.get(url_firstPage[-1]).content.decode("utf-8")
    selector = etree.HTML(html)

    num_of_assests = selector.xpath('//div[@class="paging"]//b')
    num = []
    for i in num_of_assests:
        num.append(i.text)
        print(num)

    num_of_pages = int(num[0])//50 + 1

    print(num_of_pages)

    url_page.append(url_firstPage[-1])

    for i in range(first_page,page+1):
        url_page.append("https://www.cvedetails.com/vulnerability-list.php?vendor_id="+str(vendor_id)+"&product_id="+str(product_id)+"&version_id="+str(version_id)+"&page="+str(i)+"&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0\
        &opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin="+str(min)+"&cvssscoremax="+str(max)+ "&year=0&month=0&cweid=0&order=1&trc=101161&sha=3cf9994d68386594f1283fc226cf51dad5fe72b8"
                        )

    return url_page

def scrapper(url_page_list):
                                                            
    db = mysql.connector.connect(user='root',
                                 password='Test@20180604',
                                 host='rm-j6cx1z86d86308x6m.mysql.rds.aliyuncs.com',
                                 database='vulnerabilities'
                                 )

    #set the parsing code
    db.set_charset_collation('utf8')
    cursor = db.cursor()


    sql = 'CREATE TABLE IF NOT EXISTS `cve` (`CVEid`  VARCHAR(255),`CWEid` VARCHAR(255), `num_of_exploits` VARCHAR(255),\
                                               `type` VARCHAR(255),`Publish_Dates` DATE,`Update_Dates` DATE,`score` NUMERIC,`des` mediumtext,\
                                               Access_Level VARCHAR(255),Access VARCHAR(255),Complexity VARCHAR(255), Authetication VARCHAR(255),\
                                               Conf VARCHAR(255),Integ VARCHAR(255),Avail VARCHAR(255),\
                                               PRIMARY KEY (CVEid))'

    cursor.execute(sql)

    
    for index, url in enumerate(url_page_list):
        

        

        html = requests.get(url).content.decode("utf-8")
        selector = etree.HTML(html)
        print(index)

####  Below code is for writing csv file locally
##        #Just add the row title for the first time
##        if index == 0:
##
##            # create a new csv file to store data
##            csv_file = open('cve12.csv', 'w')
##            writer = csv.writer(csv_file)
##            assets = selector.xpath('//table[@class ="searchresults sortable"]//tr[1]//th')
##            row_name = []
##
##            #Do not add the row of index from website
##            for index,asset in enumerate(assets):
##                # print(asset.text.strip())
##                if index > 0:
##                    row_name.append(asset.text.strip())
##
##            # add a new row title description
##            row_name.append('description')
##
##            writer.writerow(row_name)

        table_rows = selector.xpath('//tr[@class ="srrowns"]')
        table_des = selector.xpath('//tr//td[@class ="cvesummarylong"]//text()')
        
        
##        Access_Level = selector.xpath('//tr[@class ="srrowns"]//td[9]//div')
##        Access =
##        Complexity =
##        Authetication
##        Conf. =
##        Integ. =
##        Avail. =
        
        descriptions = selector.xpath('//tr//td[@class ="cvesummarylong"]//text()')
        
        for index,(row, des) in enumerate(zip(table_rows, table_des)):

            CWEid = None
            num_of_exploit = None
            CVEids = row.xpath('.//td[2]//a')
            CWEids = row.xpath('.//td[3]//a')
            num_of_exploits = row.xpath('.//td[4]//a')
            types = row.xpath('.//td[5]')
            Publish_Dates = row.xpath('.//td[6]')
            Update_Dates = row.xpath('.//td[7]')
            scores = row.xpath('.//td[8]//div')
            Access_Levels = row.xpath('.//td[9]')
            Accesses =row.xpath('.//td[10]')
            Complexities =row.xpath('.//td[11]')
            Authetications = row.xpath('.//td[12]')
            Confs =row.xpath('.//td[13]')
            Integs =row.xpath('.//td[14]')
            Avails =row.xpath('.//td[15]')

            cells = [CVEids[0],CWEids,num_of_exploits,types[0],Publish_Dates[0],Update_Dates[0],scores[0],Access_Levels[0],Accesses[0]
            ,Complexities[0],Authetications[0],Confs[0],Integs[0],Avails[0],des]


            

####            cells = row.xpath('.//td') 
##            cellTexts = []
####            cellTexts.append(id[index].text)
##            for col in cells:
##                if col.text == None:
##                    cellTexts.append('')
##                else:
##                    cellTexts.append(col.text.strip())
##
##            cellTexts.append(des.strip())
         
            for col in cells[1]:
                if row.xpath('.//td[3]//a') == None:
                    CWEid = None
                else:
                    CWEid = col.text
                    
            for exploit in cells[2]:
                if exploit.text == None:
                    num_of_exploit = None
                else:
                    num_of_exploit = exploit.text.strip()
            CVEid = cells[0].text
            type_ = cells[3].text
            Publish_Date = cells[4].text
            Update_Date = cells[5].text
            score = cells[6].text
            Access_Level = cells[7].text
            Access = cells[8].text
            Complexity =cells[9].text
            Authetication = cells[10].text
            Conf =cells[11].text
            Integ =cells[12].text
            Avail =cells[13].text
            description = cells[14].encode('utf-8').strip()
##            print(CVEid,CWEid)

##            if index == 0:
##                print(type(description))

             
            hash_string = str(CVEid) + str(CWEid).strip() + str(num_of_exploit).strip() + str(type_).strip() + str(Publish_Date) + str(Update_Date) + str(score) 
            hash_string = hash_string.strip()
            
            sha1 = hashlib.sha1()
            sha1.update(unicode(hash_string,"utf-8"))
            hashvalue = sha1.hexdigest()
            


            sql = '''REPLACE INTO cve_hash (vul_cveId, vul_cweId, vul_numOfExploits, vul_type, vul_publishedDate, vul_updateDate, vul_score, vul_accessLevel,vul_access,\
            vul_complexity, vul_authentication,vul_conf,vul_integ,vul_avail,vul_des,vul_hash)\
                   VALUES\
                  (%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s)'''
            

            cursor.execute(sql,(CVEid, CWEid, num_of_exploit, type_, Publish_Date, Update_Date, score, Access_Level,Access,
            Complexity,Authetication,Conf,Integ,Avail,description,hashvalue))
            
            try:
                db.commit()
            except:
                #if unexecuted, rollback
                db.rollback()

## Code below is for save file locally
##            cellTexts.insert(8, score[index].text)
##            remove_list = [10,1,2]
##            for i in remove_list:
##                cellTexts.remove(cellTexts[i])

##            writer.writerow(cellTexts)


def main():
    #min=0,max=0,month=5,year=2018
##    cursor,db = ConnectSQL()
    url_page = Urlcreator(0,0,0,0,0,1,1800)
    scrapper(url_page)


if __name__ == '__main__':
    main()
