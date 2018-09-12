import requests
from lxml import etree
# import mysql.connector
import requests
from selenium import webdriver
import time



def Urlcreator(first_page, page):
    url_firstPage = []
    url_page_list = []
    url_page = []

    url_firstPage.append(
        "https://www.openbugbounty.org/latest/"
    )

    url_page_list.append(url_firstPage[-1])

    for i in range(first_page + 1, page + 1):
        url_page_list.append(
            "https://www.openbugbounty.org/latest/page/" + str(i) +"/"
        )

    print(url_page_list)

    for i in url_page_list:

        response = requests.get(i)
        html = response.content.decode("utf-8")
        selector = etree.HTML(html)
        #/html/body/div[1]/div[3]/div[1]/table/tbody/tr[1]/td[1]
        #/html/body/div[1]/div[3]/div[1]/table/tbody/tr[2]/td[1]/div/a
        #//*[@id="vulner_0"]/p/a
        #//*[@id="vulner_1"]/p/a
        #/html/body/div[5]/div[1]/div/div[2]/table/tbody/tr[1]/td[1]/a
        obbid_list = selector.xpath('//table//tr')

        obbids = []
        for obbid in obbid_list:
            if obbid.xpath('./td[1]/div/a/@href') == []:
                obbid_ = None
            else:
                obbid_ = obbid.xpath('./td[1]/div/a/@href')[0].strip()
            obbids.append(obbid_)
            if obbid_ != None:
                url_page.append("https://www.openbugbounty.org" + str(obbid_))

    print(len(url_page))
    return url_page


def main():
    url_page = Urlcreator(1,3)




if __name__ == '__main__':
    main()
