#encoding: utf-8
import os
import re
import mysql.connector
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 
import requests
from cve_cnvd_visualizer import go_thierry
import os


#with open('ey_cti_cn_rpt2.html', 'r') as f1:
#        list1 = f1.readlines()
#with open('test.html', 'w') as f:
#    for i in list1:
#        i = re.sub(r'\n','',i)
#        f.write('''f.write(\'\'\'%s\'\'\')\n''' % i)
def getnews(category):

    db = mysql.connector.connect(user='root',
                                 password='Test@20180604',
                                 host='rm-j6cx1z86d86308x6m.mysql.rds.aliyuncs.com',
                                 port='3306',
                                 database='event_news'
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




def write_html(filename,finance,science,retail):


    text1,text2 = go_thierry()
    response = requests.get('http://cti-pub-files.oss-cn-shanghai.aliyuncs.com/pages/patch.html')
    html = response.text
    list1 = re.findall(r'.*?\n', html)




    #with open("http://cti-pub-files.oss-cn-shanghai.aliyuncs.com/pages/high_level.html", 'r') as f2:
        #list2 = f2.readlines()

    response2 = requests.get('http://cti-pub-files.oss-cn-shanghai.aliyuncs.com/pages/high_level.html')
    html2 = response2.text
    list2 = re.findall(r'.*?\n', html2)



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
        


        f.write('''<html class=" js flexbox flexboxlegacy webgl no-touch geolocation rgba hsla multiplebgs backgroundsize borderimage borderradius boxshadow textshadow opacity cssanimations csscolumns cssgradients cssreflections csstransforms csstransforms3d csstransitions fontface no-generatedcontent svg inlinesvg smil svgclippaths" lang="zh-cn" xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-cn" style=""><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">''')
        f.write('''<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">''')
        f.write('''''')
        f.write('''<meta name="viewport" content="width=device-width, initial-scale=1">''')
        f.write('''<title>安永网络安全威胁情报</title>''')
        f.write('''<meta http-equiv="Content-Language" content="en">''')
        f.write('''<meta name="apple-mobile-web-app-capable" content="yes">''')
        f.write('''<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">''')
        f.write('''<meta name="msapplication-config" content="/theme/xml/ieconfig.xml">''')
        f.write('''<link rel="shortcut icon" href="https://www.ey.com/ecimages/EYlogo.ico">''')
        f.write('''<link rel="apple-touch-icon" href="https://www.ey.com/ecimages/icon2x.png">''')
        f.write('''<link rel="apple-touch-startup-image" href="https://www.ey.com/ecimages/startup-image.png">''')
        #f.write('''<link rel="stylesheet" href="http://cti-pub-files.oss-cn-shanghai.aliyuncs.com/css/style.css">''')
        f.write('''<style type="text/css">@charset "UTF-8";
html {
  box-sizing: border-box;
}

*, *::after, *::before {
  box-sizing: inherit;
}

/*
This CSS resource incorporates links to font software which is
the valuable copyrighted property of WebType LLC, The Font Bureau
and/or their suppliers. You may not
attempt to copy, install, redistribute, convert, modify or reverse
engineer this font software. Please contact WebType with any
questions: http://www.webtype.com
*/
@font-face {
  font-family: "Interstate";
  src: url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-2.eot");
  src: url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-2.eot?") format("embedded-opentype"), url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-3.woff") format("woff"), url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-1.ttf") format("truetype");
  font-style: normal;
  font-weight: normal;
}

@font-face {
  font-family: "Interstate-Italic";
  src: url("https://www.ey.com/ecimages/fonts/interstate/db2dc2c9-e02f-45ff-a30c-d3de74e5661e-1.eot");
  src: url("https://www.ey.com/ecimages/fonts/interstate/db2dc2c9-e02f-45ff-a30c-d3de74e5661e-2.eot?") format("embedded-opentype"), url("https://www.ey.com/ecimages/fonts/interstate/db2dc2c9-e02f-45ff-a30c-d3de74e5661e-3.woff") format("woff"), url("https://www.ey.com/ecimages/fonts/interstate/db2dc2c9-e02f-45ff-a30c-d3de74e5661e-1.ttf") format("truetype");
  font-style: italic;
  font-weight: normal;
}

@font-face {
  font-family: "Interstate-Light";
  src: url("https://www.ey.com/ecimages/fonts/interstate/51012d22-c228-4858-8e44-7d338468d003-1.eot");
  src: url("https://www.ey.com/ecimages/fonts/interstate/51012d22-c228-4858-8e44-7d338468d003-2.eot?") format("embedded-opentype"), url("https://www.ey.com/ecimages/fonts/interstate/51012d22-c228-4858-8e44-7d338468d003-3.woff") format("woff"), url("https://www.ey.com/ecimages/fonts/interstate/51012d22-c228-4858-8e44-7d338468d003-1.ttf") format("truetype");
  font-style: normal;
  font-weight: normal;
}

@font-face {
  font-family: "InterstateLight";
  src: url("https://www.ey.com/ecimages/fonts/interstate/f4ce22b4-9095-48c2-ac73-d56f54a19a74-2.eot");
  src: url("https://www.ey.com/ecimages/fonts/interstate/f4ce22b4-9095-48c2-ac73-d56f54a19a74-2.eot?") format("embedded-opentype"), url("https://www.ey.com/ecimages/fonts/interstate/f4ce22b4-9095-48c2-ac73-d56f54a19a74-3.woff") format("woff"), url("https://www.ey.com/ecimages/fonts/interstate/f4ce22b4-9095-48c2-ac73-d56f54a19a74-1.ttf") format("truetype");
  font-style: italic;
  font-weight: normal;
}

@font-face {
  font-family: "Interstate-Bold";
  src: url("https://www.ey.com/ecimages/fonts/interstate/ec453a9c-08b8-48f4-b89b-7c4ceffa6e65-1.eot");
  src: url("https://www.ey.com/ecimages/fonts/interstate/ec453a9c-08b8-48f4-b89b-7c4ceffa6e65-2.eot?") format("embedded-opentype"), url("https://www.ey.com/ecimages/fonts/interstate/ec453a9c-08b8-48f4-b89b-7c4ceffa6e65-3.woff") format("woff"), url("https://www.ey.com/ecimages/fonts/interstate/ec453a9c-08b8-48f4-b89b-7c4ceffa6e65-1.ttf") format("truetype");
  font-style: normal;
  font-weight: normal;
}

html {
  font-family: sans-serif;
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
}

body {
  margin: 0;
  height: 100%;
}

article,
aside,
details,
figcaption,
figure,
footer,
header,
hgroup,
main,
menu,
nav,
section,
summary {
  display: block;
}

audio,
canvas,
progress,
video {
  display: inline-block;
  vertical-align: baseline;
}

audio:not([controls]) {
  display: none;
  height: 0;
}

[hidden],
template {
  display: none;
}

a {
  background-color: transparent;
}

a:active,
a:hover {
  outline: 0;
}

abbr[title] {
  border-bottom: 1px dotted;
}

b,
strong {
  font-weight: bold;
}

dfn {
  font-style: italic;
}

h1 {
  font-size: 2em;
  margin: 0.67em 0;
}

mark {
  background: #ff0;
  color: #000;
}

small {
  font-size: 80%;
}

sub,
sup {
  font-size: 75%;
  line-height: 0;
  position: relative;
  vertical-align: baseline;
}

sup {
  top: -0.5em;
}

sub {
  bottom: -0.25em;
}

img {
  border: 0;
}

svg:not(:root) {
  overflow: hidden;
}

figure {
  margin: 1em 40px;
}

hr {
  box-sizing: content-box;
  height: 0;
}

pre {
  overflow: auto;
}

code,
kbd,
pre,
samp {
  font-family: monospace, monospace;
  font-size: 1em;
}

button,
input,
optgroup,
select,
textarea {
  color: inherit;
  font: inherit;
  margin: 0;
}

button {
  overflow: visible;
}

button,
select {
  text-transform: none;
}

button,
html input[type="button"],
input[type="reset"],
input[type="submit"] {
  -webkit-appearance: button;
  cursor: pointer;
}

button[disabled],
html input[disabled] {
  cursor: default;
}

button::-moz-focus-inner,
input::-moz-focus-inner {
  border: 0;
  padding: 0;
}

input {
  line-height: normal;
}

* input[type="checkbox"],
input[type="radio"] {
  box-sizing: border-box;
  padding: 0;
}

input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  height: auto;
}

input[type="search"] {
  -webkit-appearance: textfield;
  box-sizing: content-box;
}

input[type="search"]::-webkit-search-cancel-button,
input[type="search"]::-webkit-search-decoration {
  -webkit-appearance: none;
}

fieldset {
  border: 1px solid #c0c0c0;
  margin: 0 2px;
  padding: 0.35em 0.625em 0.75em;
}

legend {
  border: 0;
  padding: 0;
}

textarea {
  overflow: auto;
}

optgroup {
  font-weight: bold;
}

table {
  border-collapse: collapse;
  border-spacing: 0;
}
table.dataframe {
    font-size:1em;
    }
.dataframe th{
    background:#fff000;
}
#thc1{
    width:18%;
    }
    #thc2{
    width:20%;
    }
    #thc3{
    width:12%;
    }
    #thc4{
    width:50%;
    }
td,
th {
  padding: 0;
}

/* Bitters 1.0.0
http://bitters.bourbon.io
Copyright 2013-2015 thoughtbot, inc.
MIT License */
button, input[type="button"], input[type="reset"], input[type="submit"],
button {
  -webkit-appearance: none;
  -moz-appearance: none;
  -ms-appearance: none;
  -o-appearance: none;
  appearance: none;
  -webkit-font-smoothing: antialiased;
  background-color: #369;
  border-radius: 3px;
  border: none;
  color: #fff;
  cursor: pointer;
  display: inline-block;
  font-family: "Helvetica Neue", "Helvetica", "Roboto", "Arial", sans-serif;
  font-size: 1em;
  font-weight: 600;
  line-height: 1;
  padding: 0.75em 1em;
  text-decoration: none;
  -webkit-user-select: none;
     -moz-user-select: none;
      -ms-user-select: none;
          user-select: none;
  vertical-align: middle;
  white-space: nowrap;
}

button:hover, button:focus, input[type="button"]:hover, input[type="button"]:focus, input[type="reset"]:hover, input[type="reset"]:focus, input[type="submit"]:hover, input[type="submit"]:focus,
button:hover,
button:focus {
  background-color: #204060;
  color: #fff;
}

button:disabled, input[type="button"]:disabled, input[type="reset"]:disabled, input[type="submit"]:disabled,
button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

fieldset {
  background-color: #e6e6e6;
  border: 1px solid #ccc;
  margin: 0 0 0.7em;
  padding: 1.4em;
}

input,
label,
select {
  display: block;
  font-family: "Helvetica Neue", "Helvetica", "Roboto", "Arial", sans-serif;
  font-size: 1em;
}

label {
  font-weight: 600;
  margin-bottom: 0.35em;
}

label.required::after {
  content: "*";
}

label abbr {
  display: none;
}

input[type="color"], input[type="date"], input[type="datetime"], input[type="datetime-local"], input[type="email"], input[type="month"], input[type="number"], input[type="password"], input[type="search"], input[type="tel"], input[type="text"], input[type="time"], input[type="url"], input[type="week"], textarea,
select[multiple=multiple],
textarea {
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 3px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.06);
  box-sizing: border-box;
  font-family: "Helvetica Neue", "Helvetica", "Roboto", "Arial", sans-serif;
  font-size: 1em;
  margin-bottom: 0.7em;
  padding: 0.4666666667em;
  -webkit-transition: border-color;
  transition: border-color;
  width: 100%;
}

input[type="color"]:hover, input[type="date"]:hover, input[type="datetime"]:hover, input[type="datetime-local"]:hover, input[type="email"]:hover, input[type="month"]:hover, input[type="number"]:hover, input[type="password"]:hover, input[type="search"]:hover, input[type="tel"]:hover, input[type="text"]:hover, input[type="time"]:hover, input[type="url"]:hover, input[type="week"]:hover, textarea:hover,
select[multiple=multiple]:hover,
textarea:hover {
  border-color: #b3b3b3;
}

input[type="color"]:focus, input[type="date"]:focus, input[type="datetime"]:focus, input[type="datetime-local"]:focus, input[type="email"]:focus, input[type="month"]:focus, input[type="number"]:focus, input[type="password"]:focus, input[type="search"]:focus, input[type="tel"]:focus, input[type="text"]:focus, input[type="time"]:focus, input[type="url"]:focus, input[type="week"]:focus, textarea:focus,
select[multiple=multiple]:focus,
textarea:focus {
  border-color: #369;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.06), 0 0 5px rgba(45, 89, 134, 0.7);
  outline: none;
}

textarea {
  resize: vertical;
}

input[type="search"] {
  -webkit-appearance: none;
  -moz-appearance: none;
  -ms-appearance: none;
  -o-appearance: none;
  appearance: none;
}

input[type="checkbox"],
input[type="radio"] {
  display: inline;
  margin-right: 0.35em;
}

input[type="file"] {
  padding-bottom: 0.7em;
  width: 100%;
}

select {
  margin-bottom: 1.4em;
  max-width: 100%;
  width: auto;
}

ol,
ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  font-weight: 300;
  font-family: "Helvetica", sans-serif;
}

ol.default-ul,
ul.default-ul {
  margin-bottom: 2em;
}

ol.inline-list,
ul.inline-list {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-wrap: wrap;
      flex-wrap: wrap;
  -webkit-box-pack: center;
      -ms-flex-pack: center;
          justify-content: center;
}

ol.inline-list li,
ul.inline-list li {
  -webkit-box-flex: 1;
      -ms-flex: 1 0 auto;
          flex: 1 0 auto;
  text-align: center;
  display: inline-block;
  padding: 5px 7px;
  border: 1px solid #ccc;
  background: #fff;
  margin: 3px;
}

ol.default-ol,
ul.default-ol {
  list-style-type: decimal;
  margin-bottom: 0.7em;
  padding-left: 1.4em;
}

dl {
  margin-bottom: 0.7em;
}

dl dt {
  font-weight: bold;
  margin-top: 0.7em;
}

dl dd {
  margin: 0;
}

.grid-items .default-ul li {
  margin-bottom: 0;
}

table {
  -webkit-font-feature-settings: "kern", "liga", "tnum";
  -ms-font-feature-settings: "kern", "liga", "tnum";
  font-feature-settings: "kern", "liga", "tnum";
  border-collapse: collapse;
  margin: 0.7em 0;
  table-layout: fixed;
  width: 100%;
}

th {
  border-bottom: 1px solid #a6a6a6;
  font-weight: 600;
  padding: 0.7em 0;
  text-align: left;
}

td {
  border-bottom: 1px solid #ccc;
  padding: 0.7em 0;
}

tr,
td,
th {
  vertical-align: middle;
}

body {
  -webkit-font-feature-settings: "kern", "liga", "pnum";
  -ms-font-feature-settings: "kern", "liga", "pnum";
  font-feature-settings: "kern", "liga", "pnum";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #333;
  font-family: "Helvetica Neue", "Helvetica", "Roboto", "Arial", sans-serif;
  font-size: 1em;
  line-height: 1.4;
}

h1,
h2,
h3,
h4,
h5,
h6 {
  font-family: "Helvetica Neue", "Helvetica", "Roboto", "Arial", sans-serif;
  font-size: 1em;
  line-height: 1.2;
  margin: 0 0 0.7em;
}

p {
  margin: 0 0 0.7em;
}

a {
  color: #369;
  text-decoration: none;
  -webkit-transition: color 0.1s linear;
  transition: color 0.1s linear;
}

a:active, a:focus, a:hover {
  color: #369;
}

a:active, a:focus {
  outline: none;
}

hr {
  border-bottom: 1px solid #ccc;
  border-left: none;
  border-right: none;
  border-top: none;
  margin: 1.4em 0;
}

img,
picture {
  margin: 0;
  max-width: 100%;
}

/*! Flickity v1.0.2
http://flickity.metafizzy.co
---------------------------------------------- */
.flickity-enabled {
  position: relative;
}

.flickity-enabled:focus {
  outline: none;
}

.flickity-viewport {
  overflow: hidden;
  position: relative;
  height: 100%;
}

.flickity-slider {
  position: absolute;
  width: 100%;
  height: 100%;
}

/* draggable */
.flickity-enabled.is-draggable {
  -webkit-tap-highlight-color: transparent;
  tap-highlight-color: transparent;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

.flickity-enabled.is-draggable .flickity-viewport {
  cursor: move;
  cursor: -webkit-grab;
  cursor: grab;
}

.flickity-enabled.is-draggable .flickity-viewport.is-pointer-down {
  cursor: -webkit-grabbing;
  cursor: grabbing;
}

/* ---- previous/next buttons ---- */
.flickity-prev-next-button {
  position: absolute;
  top: 50%;
  width: 44px;
  height: 44px;
  border: none;
  border-radius: 50%;
  background: white;
  background: rgba(255, 255, 255, 0.75);
  cursor: pointer;
  /* vertically center */
  -webkit-transform: translateY(-50%);
  transform: translateY(-50%);
}

.flickity-prev-next-button:hover {
  background: white;
}

.flickity-prev-next-button:focus {
  outline: none;
  box-shadow: 0 0 0 5px #09F;
}

.flickity-prev-next-button:active {
  filter: alpha(opacity=60);
  /* IE8 */
  opacity: 0.6;
}

.flickity-prev-next-button.previous {
  left: 10px;
}

.flickity-prev-next-button.next {
  right: 10px;
}

/* right to left */
.flickity-rtl .flickity-prev-next-button.previous {
  left: auto;
  right: 10px;
}

.flickity-rtl .flickity-prev-next-button.next {
  right: auto;
  left: 10px;
}

.flickity-prev-next-button:disabled {
  filter: alpha(opacity=30);
  /* IE8 */
  opacity: 0.3;
  cursor: auto;
}

.flickity-prev-next-button svg {
  position: absolute;
  left: 20%;
  top: 20%;
  width: 60%;
  height: 60%;
}

.flickity-prev-next-button .arrow {
  fill: #333;
}

/* color & size if no SVG - IE8 and Android 2.3 */
.flickity-prev-next-button.no-svg {
  color: #333;
  font-size: 26px;
}

/* ---- page dots ---- */
.flickity-page-dots {
  position: absolute;
  width: 100%;
  bottom: -25px;
  padding: 0;
  margin: 0;
  list-style: none;
  text-align: center;
  line-height: 1;
}

.flickity-rtl .flickity-page-dots {
  direction: rtl;
}

.flickity-page-dots .dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  margin: 0 8px;
  background: #333;
  border-radius: 50%;
  filter: alpha(opacity=25);
  /* IE8 */
  opacity: 1;
  cursor: pointer;
}

.flickity-page-dots .dot.is-selected {
  filter: alpha(opacity=100);
  /* IE8 */
  opacity: 1;
}

header.navigation {
  background-color: white;
  width: 100%;
  z-index: 999;
}

header.navigation .navigation-wrapper {
  max-width: 68em;
  margin-left: auto;
  margin-right: auto;
  max-width: 96%;
  position: relative;
  padding-bottom: 10px;
  height: 80px;
}

header.navigation .navigation-wrapper::after {
  clear: both;
  content: "";
  display: block;
}

header.navigation .navigation-wrapper::after {
  clear: both;
  content: "";
  display: block;
}

.modal-open header.navigation .navigation-wrapper {
  height: 100vh;
}

@media (min-width: 1200px) {
  header.navigation .navigation-wrapper {
    max-width: 68em;
  }
}

header.navigation .logo {
  float: left;
  height: 80px;
  padding-left: 1em;
  padding-right: 2em;
  margin-top: 15px;
  width: 140px;
  height: 65px;
  background: url(https://cdn.ey.com/branding/svg_logos/EY_Logo-w.svg) no-repeat;
}

header.navigation .logo img {
  display: none;
}

.darklogo header.navigation .logo {
  background: url(https://cdn.ey.com/branding/svg_logos/EY_Logo.svg) no-repeat;
  background-size: cover;
}

@media (min-width: 320px) and (max-width: 667px) {
  .darklogo header.navigation .logo {
    background: url(https://cdn.ey.com/branding/svg_logos/EY_Logo-m.svg) no-repeat;
    background-size: contain;
    height: 55px;
    margin-top: 15px;
  }
}

@media (min-width: 320px) and (max-width: 667px) {
  header.navigation .logo {
    background: url(https://cdn.ey.com/branding/svg_logos/EY_Logo-m-w.svg) no-repeat;
    background-size: contain;
    height: 55px;
    margin-top: 15px;
  }
}

header.navigation .logo img {
  height: 100%;
  padding: 0.4em 0 0;
  -webkit-transition: all .4s;
  transition: all .4s;
}

.darklogo header.navigation .logo img {
  display: none;
}

@media (max-width: 767px) {
  header.navigation .logo img {
    max-height: 60px;
  }
}

@media (max-width: 375px) {
  header.navigation .logo img {
    display: none;
  }
}

header.navigation .navigation-menu-button {
  color: #333;
  text-align: center;
  background: #fff;
  display: inline-block;
  float: right;
  font-weight: 700;
  line-height: 80px;
  margin: 0;
  padding: 0 30px;
  font-size: 32px;
  text-transform: uppercase;
}

@media screen and (min-width: 53.75em) {
  header.navigation .navigation-menu-button {
    display: none;
  }
}

header.navigation .navigation-menu-button:focus, header.navigation .navigation-menu-button:hover {
  color: #333;
}

header.navigation nav {
  float: none;
  min-height: 80px;
  z-index: 999;
}

@media screen and (min-device-width: 320px) {
  header.navigation nav {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 70vw;
    -webkit-transform: translateX(-50%) translateY(-50%);
    transform: translateX(-50%) translateY(-50%);
  }
}

@media screen and (min-width: 53.75em) {
  header.navigation nav {
    float: left;
  }
}

header.navigation nav h3 {
  color: #ffe600;
  font-weight: bold !important;
  font-size: 14px;
  text-align: left;
}

header.navigation ul.navigation-menu {
  -webkit-transform-style: preserve-3d;
  clear: both;
  display: none;
  margin: 0 auto;
  overflow: visible;
  padding: 0;
  width: 100%;
  z-index: 9999;
}

header.navigation ul.navigation-menu.show {
  display: block;
}

@media screen and (min-width: 53.75em) {
  header.navigation ul.navigation-menu {
    display: inline;
    margin: 0;
    padding: 0;
  }
}

header.navigation ul li.nav-link {
  font-size: 1.2em;
  background: white;
  display: block;
  line-height: 80px;
  overflow: hidden;
  padding-right: 0.8em;
  text-align: right;
  width: 100%;
  z-index: 9999;
}

@media (max-width: 768px) {
  header.navigation ul li.nav-link {
    font-size: 1em;
    float: left;
    width: 16%;
    background: transparent;
  }
}

@media screen and (min-width: 53.75em) {
  header.navigation ul li.nav-link {
    background: transparent;
    display: inline;
    line-height: 80px;
    text-decoration: none;
    width: auto;
  }
}

header.navigation ul li.nav-link a {
  color: #808080;
  display: inline-block;
  font-weight: 400;
  text-decoration: none;
}

@media screen and (min-width: 53.75em) {
  header.navigation ul li.nav-link a {
    padding-right: 1em;
  }
}

header.navigation ul li.nav-link a:focus, header.navigation ul li.nav-link a:hover {
  color: #333;
}

header.navigation .active-nav-item a {
  border-bottom: 1px solid rgba(51, 51, 51, 0.5);
  padding-bottom: 3px;
}

header.navigation li.more.nav-link {
  padding-right: 0;
}

@media screen and (min-width: 53.75em) {
  header.navigation li.more.nav-link {
    padding-right: 1em;
  }
}

header.navigation li.more.nav-link > ul > li:first-child a {
  padding-top: 1em;
}

header.navigation li.more.nav-link a {
  margin-right: 1em;
}

header.navigation li.more.nav-link > a {
  padding-right: 0.6em;
}

header.navigation li.more.nav-link > a:after {
  position: absolute;
  top: auto;
  right: -0.4em;
  bottom: auto;
  left: auto;
  content: '\25BE';
  color: #808080;
}

header.navigation li.more {
  overflow: visible;
  padding-right: 0;
}

header.navigation li.more a {
  padding-right: 0.8em;
}

header.navigation li.more > a {
  padding-right: 1.6em;
  position: relative;
}

@media screen and (min-width: 53.75em) {
  header.navigation li.more > a {
    margin-right: 1em;
  }
}

header.navigation li.more > a:after {
  content: '›';
  font-size: 1.2em;
  position: absolute;
  right: 0.5em;
}

header.navigation li.more:focus > .submenu,
header.navigation li.more:hover > .submenu {
  display: block;
}

@media screen and (min-width: 53.75em) {
  header.navigation li.more {
    padding-right: 0.8em;
    position: relative;
  }
}

header.navigation li.more.menu {
  font-family: Arial;
}

header.navigation li.more.menu > a {
  font-size: 28px;
  -webkit-transform: translateY(5px);
  transform: translateY(5px);
}

header.navigation li.more.menu > a::after {
  content: "";
}

header.navigation ul.submenu {
  display: none;
  padding-left: 0;
}

@media screen and (min-width: 53.75em) {
  header.navigation ul.submenu {
    left: -1em;
    position: absolute;
    top: 1.5em;
  }
}

@media screen and (min-width: 53.75em) {
  header.navigation ul.submenu .submenu {
    left: 15.8em;
    top: 0;
  }
}

header.navigation ul.submenu li {
  display: block;
  padding-right: 0;
}

@media screen and (min-width: 53.75em) {
  header.navigation ul.submenu li {
    line-height: 26.6666666667px;
  }
  header.navigation ul.submenu li:first-child > a {
    border-top-left-radius: 3px;
    border-top-right-radius: 3px;
  }
  header.navigation ul.submenu li:last-child > a {
    border-bottom-left-radius: 3px;
    border-bottom-right-radius: 3px;
  }
}

header.navigation ul.submenu li a {
  background-color: #f7f7f7;
  display: inline-block;
  text-align: right;
  width: 100%;
  -webkit-transition: all .3s;
  transition: all .3s;
}

header.navigation ul.submenu li a:hover {
  background: #f0f0f0;
}

@media screen and (min-width: 53.75em) {
  header.navigation ul.submenu li a {
    background-color: white;
    padding-left: 1em;
    text-align: left;
    width: 16em;
  }
}

header.navigation .navigation-tools {
  background: #fff;
  clear: both;
  display: block;
  height: 80px;
  padding-left: 0.5em;
  padding-right: 1em;
}

@media (min-width: 940px) {
  header.navigation .navigation-tools {
    position: absolute;
    right: 0;
    bottom: -40px;
  }
}

@media (max-width: 940px) {
  header.navigation .navigation-tools {
    display: none;
  }
}

@media screen and (min-width: 53.75em) {
  header.navigation .navigation-tools {
    background: transparent;
    clear: none;
    float: right;
  }
}

header.navigation .sign-up {
  background-color: #369;
  border-radius: 3px;
  border: 0;
  color: white;
  display: inline-block;
  font-size: inherit;
  font-weight: bold;
  padding: 7px 18px;
  text-decoration: none;
  background-clip: padding-box;
  display: inline;
  float: right;
  font-size: 0.8em;
  margin-top: 1em;
  padding: 0.75em 1em;
  text-transform: uppercase;
}

header.navigation .sign-up:hover:not(:disabled) {
  background-color: #3573b1;
  cursor: pointer;
}

header.navigation .sign-up:active:not(:disabled), header.navigation .sign-up:focus:not(:disabled) {
  background-color: #305982;
  cursor: pointer;
}

header.navigation .sign-up:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

header.navigation .search-bar {
  float: left;
  padding: 0.85em 0.6em 0.7em 0.6em;
  width: 60%;
}

header.navigation .search-bar form {
  position: relative;
}

header.navigation .search-bar form input[type=search] {
  box-sizing: border-box;
  background: #f2f2f2;
  border-radius: 6px;
  border: 1px solid #f2f2f2;
  color: #808080;
  font-size: 0.9em;
  font-style: italic;
  margin: 0;
  padding: 0.5em 0.8em;
  width: 100%;
}

@media screen and (min-width: 53.75em) {
  header.navigation .search-bar form input[type=search] {
    width: 100%;
  }
}

header.navigation .search-bar form button[type=submit] {
  background-color: #f2f2f2;
  border-radius: 3px;
  border: 0;
  color: #333333;
  display: inline-block;
  font-size: inherit;
  font-weight: bold;
  padding: 7px 18px;
  text-decoration: none;
  background-clip: padding-box;
  background-color: #f2f2f2;
  border-radius: 3px;
  border: 0;
  color: #333333;
  display: inline-block;
  font-size: inherit;
  font-weight: bold;
  padding: 7px 18px;
  text-decoration: none;
  background-clip: padding-box;
  bottom: 0.3em;
  left: auto;
  outline: none;
  padding: 0 9px;
  position: absolute;
  right: 0.3em;
  top: 0.3em;
}

header.navigation .search-bar form button[type=submit]:hover:not(:disabled) {
  background-color: white;
  cursor: pointer;
}

header.navigation .search-bar form button[type=submit]:active:not(:disabled), header.navigation .search-bar form button[type=submit]:focus:not(:disabled) {
  background-color: #e6e6e6;
  cursor: pointer;
}

header.navigation .search-bar form button[type=submit]:hover:not(:disabled) {
  background-color: white;
  cursor: pointer;
}

header.navigation .search-bar form button[type=submit]:active:not(:disabled), header.navigation .search-bar form button[type=submit]:focus:not(:disabled) {
  background-color: #e6e6e6;
  cursor: pointer;
}

header.navigation .search-bar form button[type=submit]:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

header.navigation .search-bar form button[type=submit] img {
  height: 16px;
  opacity: 0.7;
  padding: 1px;
}

@media screen and (min-width: 53.75em) {
  header.navigation .search-bar {
    display: inline-block;
    position: relative;
    width: 16em;
  }
  header.navigation .search-bar input {
    box-sizing: border-box;
    display: block;
  }
}

div.cookienotification {
  z-index: 11;
}

p#cookiecont {
  margin: 20px;
}

.cbp-qtrotator {
  font-family: Helvetica, Arial, sans-serif;
  position: relative;
  margin: 0 auto;
  max-width: 800px;
  width: 100%;
  min-height: 200px;
}

.cbp-qtrotator .cbp-qtcontent {
  position: absolute;
  min-height: 200px;
  border-top: 1px solid #ccc;
  padding: 1em 0;
  top: 0;
  z-index: 0;
  opacity: 0;
  width: 100%;
  -webkit-backface-visibility: hidden;
}

.no-js .cbp-qtrotator .cbp-qtcontent {
  border-bottom: none;
}

.cbp-qtrotator .cbp-qtcontent.cbp-qtcurrent,
.no-js .cbp-qtrotator .cbp-qtcontent {
  position: relative;
  z-index: 10;
  pointer-events: auto;
  opacity: 1;
}

.cbp-qtrotator .cbp-qtcontent:before,
.cbp-qtrotator .cbp-qtcontent:after {
  content: " ";
  display: table;
}

.cbp-qtrotator .cbp-qtcontent:after {
  clear: both;
}

.cbp-qtprogress {
  position: absolute;
  background: #7D0F7C;
  height: 1px;
  width: 0%;
  top: 0;
  z-index: 10;
}

.cbp-qtrotator h3 {
  font-size: 1.5em;
  color: #646464;
  font-weight: 700;
  margin: 0.4em 0 1em;
}

.cbp-qtrotator p {
  font-size: 1em;
  color: #333;
  line-height: 1.5;
}

.cbp-qtrotator .cbp-qtcontent img {
  float: right;
  margin-top: 3em;
  margin-left: 2em;
  width: 20%;
}

/* Example for media query */
@media screen and (max-width: 30.6em) {
  .cbp-qtrotator {
    font-size: 70%;
  }
  .cbp-qtrotator img {
    width: 80px;
  }
}

.hero {
  background-color: #808080;
  background-position: top;
  background-repeat: no-repeat;
  background-size: cover;
  padding-bottom: 3em;
  min-height: 350px;
}

.hero .hero-logo img {
  height: 4em;
  margin-bottom: 1em;
}

.hero .hero-inner {
  max-width: 68em;
  margin-left: auto;
  margin-right: auto;
  color: white;
  margin: auto;
  padding: 3.5em;
  text-align: center;
}

.hero .hero-inner::after {
  clear: both;
  content: "";
  display: block;
}

.hero .hero-inner::after {
  clear: both;
  content: "";
  display: block;
}

.hero .hero-inner .hero-copy {
  text-align: center;
}

.hero .hero-inner .hero-copy h1 {
  font-size: 1.6em;
  margin-bottom: 0.5em;
}

@media screen and (min-width: 53.75em) {
  .hero .hero-inner .hero-copy h1 {
    font-size: 1.8em;
  }
}

.hero .hero-inner .hero-copy p {
  font-weight: 200;
  line-height: 1.4em;
  margin: 0 auto 3em;
}

@media screen and (min-width: 53.75em) {
  .hero .hero-inner .hero-copy p {
    font-size: 1.1em;
    max-width: 40%;
  }
}

.hero .hero-inner button {
  background-color: #369;
  border-radius: 3px;
  border: 0;
  color: white;
  display: inline-block;
  font-size: inherit;
  font-weight: bold;
  padding: 7px 18px;
  text-decoration: none;
  background-clip: padding-box;
  padding: 0.7em 1em;
}

.hero .hero-inner button:hover:not(:disabled) {
  background-color: #3573b1;
  cursor: pointer;
}

.hero .hero-inner button:active:not(:disabled), .hero .hero-inner button:focus:not(:disabled) {
  background-color: #305982;
  cursor: pointer;
}

.hero .hero-inner button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.grid-items::after {
  clear: both;
  content: "";
  display: block;
}

@media (max-width: 767px) {
  .grid-items {
    margin-left: -20px;
    margin-right: -20px;
  }
}

.grid-items .grid-item {
  -webkit-transition: all 0.2s ease-in-out;
  transition: all 0.2s ease-in-out;
  color: #fff;
  background: rgba(0, 0, 0, 0.5);
  border-bottom: 1px solid #fff;
  border-left: 1px solid #fff;
  border-right: 1px solid #fff;
  border-top: 1px solid #fff;
  width: 100%;
  position: relative;
  cursor: pointer;
  float: left;
  overflow: hidden;
  outline: none;
  padding: 2em;
  text-align: left;
  text-decoration: none;
}

@media (min-width: 768px) {
  .grid-items .grid-item {
    height: 10em;
  }
}

@media (max-width: 767px) {
  .grid-items .grid-item {
    padding-left: 0;
    padding-right: 0;
  }
}

#contact .grid-items .grid-item {
  background-color: #333;
}

@media (max-device-width: 1024px) {
  #contact .grid-items .grid-item {
    -webkit-transform: none;
    transform: none;
  }
}

#contact .grid-items .grid-item:hover {
  background-color: #222;
}

@media (min-width: 768px) {
  .grid-items .grid-item {
    padding: 10px;
  }
}

.grid-items .grid-item a {
  color: #fff;
}

.grid-items .grid-item a:hover {
  color: #ffe600;
}

.grid-items .grid-item > a {
  color: #fff;
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  width: 100%;
}

@media (max-device-width: 1024px) {
  .grid-items .grid-item > a {
    width: 100%;
    padding: 20px;
    font-size: 0.8em;
  }
}

@media (min-width: 940px) {
  .grid-items .grid-item > a {
    font-size: 1em;
  }
}

@media (max-width: 940px) {
  .grid-items .grid-item > ul.default-ul,
  .grid-items .grid-item ol.default-ul {
    font-size: 0.8em;
  }
}

@media screen and (min-width: 40em) {
  .grid-items .grid-item {
    width: 25%;
  }
}

.grid-items .grid-item img {
  display: block;
  height: 3em;
  margin: auto;
}

.grid-items .grid-item h3 {
  color: #fff;
  -webkit-transition: color 0.3s;
  transition: color 0.3s;
  font-size: 1.3em;
  line-height: 1.1;
  text-align: center;
  margin-top: 0;
  margin-bottom: 0.4em;
  max-width: 90%;
}

@media (min-width: 768px) {
  .grid-items .grid-item:hover h3 {
    color: #333;
  }
}

.grid-items .grid-item.grid-item-image:hover h3 {
  color: #FFF;
}

.grid-items .grid-item p {
  line-height: 1.5em;
  margin: auto;
  color: #000;
  font-size: 1.1rem;
}

@media screen and (min-width: 40em) {
  .grid-items .grid-item p {
    max-width: 100%;
  }
}

@media (max-width: 767px) {
  .grid-items .grid-item p {
    font-size: 0.8rem;
  }
}

.grid-items .grid-item.grid-item-image p {
  color: #FFF;
}

@media screen and (min-width: 40em) {
  .grid-items .grid-item-tall {
    height: 20em;
  }
}

@media screen and (max-device-width: 667px) and (orientation: landscape) {
  .grid-items .grid-item-tall {
    height: 20em !important;
    min-height: 200px;
  }
}

@media screen and (min-width: 40em) {
  .grid-items .grid-item-big {
    width: 50%;
  }
}

@media screen and (min-width: 40em) {
  .grid-items .grid-item-big p {
    max-width: 100%;
  }
}

@media screen and (min-width: 40em) {
  .grid-items .grid-item-med {
    width: 33.3333333333%;
  }
}

@media screen and (min-width: 40em) {
  .grid-items .grid-item-med p {
    max-width: 60%;
  }
}

.grid-items .grid-item-image {
  background-position: top;
  background-repeat: no-repeat;
  background-size: cover;
}

.grid-item.no-scale:hover {
  -webkit-transform: none;
  transform: none;
  cursor: default;
}

.grid-item.grid-item-image > * {
  font-size: 1.2em;
  padding: 30px;
}

@media (max-width: 767px) {
  .grid-item.grid-item-image > * {
    font-size: 1rem;
    padding: 15px;
  }
}

.section8 .grid-items .grid-item:hover h3 {
  color: #ffe600;
}

.grid-item {
  -webkit-transition: background-color 0.8s;
  transition: background-color 0.8s;
  opacity: 1;
  border: 1px solid #fff;
  border-collapse: collapse;
}

.center,
.center2 {
  font-size: 24px;
  font-family: sans-serif;
  top: 50%;
  -webkit-transition: opacity 0.4s;
  transition: opacity 0.4s;
  -webkit-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  left: 50%;
  position: absolute;
  width: 100%;
  text-align: center;
}

#industries .center,
#insights .center, #industries
.center2,
#insights
.center2 {
  -webkit-transform: translate(-50%, -50%);
          transform: translate(-50%, -50%);
  position: absolute;
  text-align: center;
}

#contact .center, #contact
.center2 {
  color: #FFF;
}

@media (max-width: 667px) {
  ul.center,
  ul.center2 {
    -webkit-transform: none;
            transform: none;
    position: static;
  }
  ul.center li,
  ul.center2 li {
    display: inline-block;
    font-size: 13px;
    text-align: center;
  }
}

.section6 h3.center2 {
  -webkit-transform: translate(-50%, -50%);
          transform: translate(-50%, -50%);
  position: absolute;
  text-align: center;
}

.grid-item p.descr {
  -webkit-transition: all 0.4s;
  transition: all 0.4s;
  -webkit-transform: translate(-50%, -50%);
          transform: translate(-50%, -50%);
  line-height: 1;
  text-align: left;
  max-width: 80%;
  opacity: 0;
  visibility: hidden;
  font-size: 18px;
  font-weight: bold;
}

@media (max-width: 940px) {
  .grid-item p.descr {
    max-width: 80%;
  }
}

@media (max-device-width: 1024px) {
  .grid-item p.descr {
    opacity: 1;
    visibility: visible;
  }
}

.section8 .grid-item p.descr {
  opacity: 1;
  visibility: visible;
}

.section8 .grid-item p.descr a {
  display: block;
  padding: 6% 0;
  line-height: 1.2;
}

@media (max-width: 375px) {
  .section8 .grid-item p.descr {
    -webkit-transform: none;
            transform: none;
  }
}

@media (max-device-width: 1024px) and (orientation: portrait) {
  .section8 .grid-item p.descr {
    -webkit-transform: none;
            transform: none;
  }
}

.section8 .grid-item:hover {
  background: #333;
  color: #fff !important;
}

.section8 .grid-item:hover > * {
  color: #fff;
}

.section8 .grid-item a:hover {
  color: #ffe600;
}

@media (min-width: 768px) {
  .grid-item:hover {
    cursor: pointer;
    background-color: #ffe600;
  }
}

.grid-item:hover .center {
  opacity: 0;
}

.grid-item:hover .descr {
  visibility: visible;
  opacity: 1;
}

@media (min-width: 768px) {
  .grid-item:hover .descr {
    -webkit-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%);
  }
}

.grid-item h3,
.grid-item p {
  margin: 0;
}

section.ads {
  position: relative;
  z-index: 1;
}

@media (min-width: 768px) {
  section.ads {
    margin-bottom: 0;
    padding: 0 !important;
  }
}

.advertisement img {
  min-width: 1088px;
  width: 100%;
}

.eyhero,
.eyhero-home {
  overflow: hidden;
  height: 450px;
  padding-bottom: 0;
}

@media (max-width: 46em) {
  .eyhero,
  .eyhero-home {
    height: 280px;
  }
}

@media (max-width: 375px) {
  .eyhero,
  .eyhero-home {
    min-height: 0;
    margin-top: 68px;
  }
}

@media (max-device-width: 667px) and (orientation: landscape) {
  .eyhero,
  .eyhero-home {
    height: 80vh;
    margin-top: 0;
    padding-top: 68px;
  }
}

.sl-landing .eyhero-home {
  box-sizing: border-box;
  height: 450px;
  overflow: hidden;
}

@media (max-width: 736px) {
  .sl-landing .eyhero-home {
    height: 45vh;
  }
}

@media (max-width: 736px) and (orientation: landscape) {
  .sl-landing .eyhero-home {
    height: 75vh;
    margin-top: 70px;
  }
}

@media (max-width: 601px) and (orientation: portrait) {
  .sl-landing .eyhero-home {
    height: 35vh;
    margin-top: 70px;
  }
}

.sl-headings {
  padding-left: 0;
}

@media (max-width: 375px) {
  .sl-headings {
    padding: 0;
  }
}

.grid-items .grid-item-image:before {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  content: "";
  background: rgba(0, 0, 0, 0.45);
}

@media (max-device-width: 1024px) {
  .grid-items .grid-item-image:before {
    z-index: 0;
  }
}

.grid-items .grid-item-image h3 {
  z-index: 2;
}

.grid-items .grid-item-image > * {
  position: relative;
  z-index: 2;
}

.grid-items .grid-item,
.landing-contact-us .grid-items .grid-item-big,
.section8 .grid-items .grid-item-big {
  min-height: 7.5em;
}

@media (max-width: 736px) {
  .grid-items .grid-item,
  .landing-contact-us .grid-items .grid-item-big,
  .section8 .grid-items .grid-item-big {
    -webkit-box-align: top;
        -ms-flex-align: top;
            align-items: top;
    padding: 10px;
  }
  .section8 .grid-items .grid-item a, .section8
  .landing-contact-us .grid-items .grid-item-big a, .section8
  .section8 .grid-items .grid-item-big a {
    font-size: 16px;
    display: block;
    padding: 4%;
    text-align: center;
  }
  .grid-items .grid-item a > img,
  .landing-contact-us .grid-items .grid-item-big a > img,
  .section8 .grid-items .grid-item-big a > img {
    display: none;
  }
}

@media screen and (max-device-width: 568px) and (orientation: landscape) {
  .contact-us .grid-items,
  .section8 .grid-items {
    display: block !important;
  }
  .contact-us .grid-items .grid-item,
  .contact-us .grid-items .grid-item-big,
  .section8 .grid-items .grid-item,
  .section8 .grid-items .grid-item-big {
    min-height: 7.5em !important;
    float: none !important;
    width: 100% !important;
    display: block !important;
  }
}

@media (max-device-width: 667px) and (orientation: landscape) {
  .landing-contact-us .grid-item > div,
  .section8 .grid-item > div {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-orient: vertical;
    -webkit-box-direction: normal;
        -ms-flex-direction: column;
            flex-direction: column;
  }
}

.os-animation {
  opacity: 0;
}

.os-animation.animated {
  opacity: 1;
}

#contact .grid-item p a {
  width: 100%;
  text-align: left;
  display: block;
  margin: 15px auto 20px;
  font-size: 16px;
  line-height: 1.2;
}

@media (max-width: 767px) {
  .section8 p.descr {
    max-width: none;
  }
}

@media (max-device-width: 1024px) {
  .grid-item p.descr {
    opacity: 1;
    -webkit-transform: none;
            transform: none;
    position: static;
    font-size: 12px;
    max-width: 90%;
    color: #fff;
    margin: 0;
    padding: 0;
  }
  .grid-item h3.center {
    text-align: left;
    position: static;
    font-size: 120%;
    -webkit-transform: none;
    transform: none;
    top: 0;
    max-width: 90%;
    margin: 0;
    color: #ffe600;
    text-align: left;
  }
  .grid-item h3.center + p {
    border-top: 1px solid #ffe600;
    padding-top: 10px;
    margin-top: 5px;
  }
}

@media (max-device-width: 2560px) and (-webkit-min-device-pixel-ratio: 3.7395833333333335), (max-device-width: 2560px) and (min-resolution: 359dpi) {
  .grid-item p.descr {
    opacity: 1;
    -webkit-transform: none;
    transform: none;
    position: static;
    font-size: 12px;
    max-width: 90%;
    color: #fff;
    margin: 0;
    padding: 0;
  }
  .grid-item h3.center {
    text-align: left;
    position: static;
    font-size: 120%;
    -webkit-transform: none;
    transform: none;
    top: 0;
    max-width: 90%;
    color: #ffe600;
  }
  .grid-item h3 {
    text-align: left !important;
  }
  .grid-item h3.center + p {
    border-top: 1px solid #ffe600;
    padding-top: 3%;
  }
}

.grid-items > div > .grid-item {
  width: 100%;
}

@media (max-width: 600px) {
  .contact-us .grid-items > .grid-item-big + div {
    width: 100% !important;
    float: none !important;
    display: block;
  }
  .contact-us .grid-item p a {
    margin: 0 auto 3px;
  }
  .contact-us .grid-item-tall {
    max-height: 7em !important;
  }
}

.center-justify {
  text-align: center;
}

.vertically-center {
  position: absolute;
  top: 50%;
  left: 50%;
  -webkit-transform: translateX(-50%) translateY(-50%);
  transform: translateX(-50%) translateY(-50%);
}

.breadcrumb {
  position: absolute;
  display: inline-block;
  margin-top: 1.4em;
  text-align: left;
}

.breadcrumb a {
  background-color: #f0f0f0;
  border-left: 0;
  color: #808080;
  display: inline-block;
  font-size: 0.8em;
  line-height: 2.1em;
  margin-bottom: 2px;
  margin-right: -5px;
  padding: 0 0.525em 0 1.05em;
  position: relative;
  text-decoration: none;
}

.breadcrumb a:first-child {
  border-bottom-left-radius: 3px;
  border-top-left-radius: 3px;
  padding-left: 0;
}

.breadcrumb a:last-child {
  background-color: #f0f0f0;
  border-bottom-right-radius: 3px;
  border-top-right-radius: 3px;
  color: #676767;
  padding-right: 1.05em;
}

.breadcrumb a:focus, .breadcrumb a:hover {
  background-color: #f0f0f0;
  color: #369;
}

.breadcrumb a:after, .breadcrumb a:before {
  position: absolute;
  top: 0px;
  right: auto;
  bottom: 0px;
  left: 100%;
  border-bottom: 1.05em solid transparent;
  border-left: 0.525em solid transparent;
  border-top: 1.05em solid transparent;
  content: '';
  display: block;
  margin: auto;
  z-index: 2;
}

.breadcrumb a:last-child:after, .breadcrumb a:last-child:before {
  border: none;
}

.breadcrumb a:before {
  border-left-color: #ccc;
  margin-left: 1px;
  z-index: 1;
}

.breadcrumb a:after {
  border-left-color: #f0f0f0;
}

@media screen and (min-width: 40em) {
  .breadcrumb a {
    font-size: 0.8125em;
    padding: 0 1.05em 0 1.4em;
  }
}

.flex-boxes {
  display: -webkit-box;
  display: -moz-flex;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-pack: center;
  box-pack: center;
  -moz-justify-content: center;
  -ms-justify-content: center;
  -o-justify-content: center;
  justify-content: center;
  -ms-flex-pack: center;
  -webkit-box-align: stretch;
  box-align: stretch;
  -moz-align-items: stretch;
  -ms-align-items: stretch;
  -o-align-items: stretch;
  align-items: stretch;
  -ms-flex-align: stretch;
  -webkit-box-lines: multiple;
  -moz-box-lines: multiple;
  box-lines: multiple;
  -ms-flex-wrap: wrap;
  flex-wrap: wrap;
  clear: both;
}

.flex-boxes::after {
  clear: both;
  content: "";
  display: block;
}

.flex-boxes .flex-box {
  -webkit-transition: all 0.2s ease-in-out;
  transition: all 0.2s ease-in-out;
  -webkit-box-flex: 2;
  box-flex: 2;
  -moz-flex: 2 2 15em;
  -ms-flex: 2 2 15em;
  flex: 2 2 15em;
  -webkit-align-self: stretch;
  -ms-grid-row-align: stretch;
      align-self: stretch;
  -ms-flex-item-align: stretch;
  background: #e6e6e6;
  border-radius: 3px;
  box-shadow: inset 0 0 1px #ccc, 0 2px 4px #e6e6e6;
  display: block;
  margin: 0.4em;
  padding: 2em 2em 3em 2em;
  text-decoration: none;
}

.flex-boxes .flex-box:nth-child(1) {
  border-top: 6px solid tomato;
}

.flex-boxes .flex-box:nth-child(1):focus, .flex-boxes .flex-box:nth-child(1):hover {
  background-color: rgba(255, 99, 71, 0.1);
}

.flex-boxes .flex-box:nth-child(2) {
  border-top: 6px solid #72BFBF;
}

.flex-boxes .flex-box:nth-child(2):focus, .flex-boxes .flex-box:nth-child(2):hover {
  background-color: rgba(114, 191, 191, 0.1);
}

.flex-boxes .flex-box:nth-child(3) {
  border-top: 6px solid #92B1E3;
}

.flex-boxes .flex-box:nth-child(3):focus, .flex-boxes .flex-box:nth-child(3):hover {
  background-color: rgba(146, 177, 227, 0.1);
}

.flex-boxes .flex-box:nth-child(4) {
  border-top: 6px solid #E3D743;
}

.flex-boxes .flex-box:nth-child(4):focus, .flex-boxes .flex-box:nth-child(4):hover {
  background-color: rgba(227, 215, 67, 0.1);
}

.flex-boxes .flex-box:nth-child(5) {
  border-top: 6px solid #CCC;
}

.flex-boxes .flex-box:nth-child(5):focus, .flex-boxes .flex-box:nth-child(5):hover {
  background-color: rgba(204, 204, 204, 0.1);
}

.flex-boxes .flex-box:nth-child(6) {
  border-top: 6px solid #F6C05C;
}

.flex-boxes .flex-box:nth-child(6):focus, .flex-boxes .flex-box:nth-child(6):hover {
  background-color: rgba(246, 192, 92, 0.1);
}

.flex-boxes .flex-box img {
  display: block;
  height: 3em;
  margin-bottom: 2em;
  margin: auto;
  opacity: 0.4;
}

.flex-boxes .flex-box .flex-title {
  color: rgba(51, 51, 51, 0.7);
  font-size: 1.2em;
  font-weight: 800;
  margin-bottom: 0.5em;
}

.flex-boxes .flex-box p {
  color: rgba(51, 51, 51, 0.6);
  line-height: 1.5em;
  margin: auto;
}

.flex-boxes .flex-box-big {
  -webkit-box-flex: 1;
  box-flex: 1;
  -moz-flex: 1 1 40em;
  -ms-flex: 1 1 40em;
  flex: 1 1 40em;
}

.accordion-tabs-minimal {
  line-height: 1.5;
  padding: 0;
  margin: 2em auto;
}

.accordion-tabs-minimal::after {
  clear: both;
  content: "";
  display: block;
}

.accordion-tabs-minimal li.tab-header-and-content {
  list-style: none;
  border: 1px solid white;
  border-width: 0 1px;
}

@media screen and (min-width: 40em) {
  .accordion-tabs-minimal li.tab-header-and-content {
    display: inline;
  }
}

.accordion-tabs-minimal a.tab-link {
  background-color: rgba(0, 0, 0, 0.15);
  color: #646464;
  display: block;
  font-family: "EYInterstate", "EY", sans-serif;
  font-size: 1.25em;
  letter-spacing: -0.03em;
  font-weight: bold;
  padding: 0.4666666667em 0.809em;
  text-decoration: none;
  -webkit-transition: all 0.4s;
  transition: all 0.4s;
}

@media (max-width: 767px) {
  .accordion-tabs-minimal a.tab-link {
    font-size: 1.15em;
  }
}

@media screen and (min-width: 40em) {
  .accordion-tabs-minimal a.tab-link {
    display: inline-block;
    border-top: 0;
  }
}

.accordion-tabs-minimal a.tab-link:hover {
  color: #369;
}

.accordion-tabs-minimal a.tab-link:focus {
  outline: none;
}

.accordion-tabs-minimal a.tab-link.is-active {
  border-bottom: 0;
  background-color: #646464;
  color: #fff;
}

.accordion-tabs-minimal .tab-content {
  display: none;
  padding: 1.4em 1.618em;
  width: 100%;
  border-radius: 0 0 10px 10px;
}

@media (max-width: 375px) {
  .accordion-tabs-minimal .tab-content {
    background-color: #FFF;
    border: 1px solid #ccc;
  }
}

@media screen and (min-width: 40em) {
  .accordion-tabs-minimal .tab-content {
    border-top: 4px solid #646464;
    float: left;
  }
}

@media (max-width: 767px) {
  .accordion-tabs-minimal a.tab-link {
    border: 1px solid #646464;
    border-width: 1px 1px 0 1px;
    border-collapse: collapse;
  }
  .tab-link:after {
    content: ">";
    float: right;
    margin-left: 1em;
  }
  .tab-link.is-active:after {
    -webkit-transform: rotate(90deg);
            transform: rotate(90deg);
  }
}

.expander .expander-trigger {
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  border-bottom: 1px solid #ccc;
  color: #369;
  cursor: pointer;
  display: block;
  font-size: 1em;
  margin-bottom: 1em;
  padding-bottom: 0.25em;
  text-decoration: none;
}

.expander .expander-trigger:before {
  font-size: 0.7em;
  content: "\25BC";
  margin-right: 0.5em;
}

.expander .expander-content p {
  color: #333;
  line-height: 1.4;
}

.expander .expander-hidden:before {
  font-size: 0.7em;
  content: "\25BA";
}

.expander .expander-hidden + .expander-content {
  display: none;
}

.cards {
  display: -webkit-box;
  display: -moz-flex;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-lines: multiple;
  -moz-box-lines: multiple;
  box-lines: multiple;
  -ms-flex-wrap: wrap;
  flex-wrap: wrap;
  -webkit-box-pack: justify;
  box-pack: justify;
  -moz-justify-content: space-between;
  -ms-justify-content: space-between;
  -o-justify-content: space-between;
  justify-content: space-between;
  -ms-flex-pack: justify;
}

.card {
  width: 31%;
  background-color: white;
  border: 1px solid #ccc;
  cursor: pointer;
  margin: 0 1em 1.4em 1em;
  position: relative;
  max-width: 68em;
  margin-left: auto;
  margin-right: auto;
}

.card + .card {
  margin-left: 2%;
}

.card .card-image {
  overflow: hidden;
  height: 0;
  padding-bottom: 56.25%;
}

.card .card-image img {
  -webkit-transition: all 0.2s ease-out;
  transition: all 0.2s ease-out;
  width: 100%;
  opacity: 1;
}

.card .card-header {
  -webkit-transition: all 0.2s ease-in-out;
  transition: all 0.2s ease-in-out;
  background-color: white;
  font-weight: bold;
  line-height: 1.5em;
  padding: 0.4666666667em 0.7em;
}

.card .card-copy {
  font-size: 0.9em;
  line-height: 1.5em;
  padding: 0.7em 0.7em;
}

.card .card-copy p {
  margin: 0 0 0.7em;
}

.card:focus, .card:hover {
  cursor: pointer;
}

.card:focus img, .card:hover img {
  -webkit-transform: scale(1.1);
          transform: scale(1.1);
}

.card:active {
  background-color: white;
}

.card:active .card-header {
  background-color: white;
}

.modal label {
  cursor: pointer;
  margin-bottom: 0;
}

.modal label img {
  border-radius: 150px;
  display: block;
  max-width: 300px;
}

.modal .modal-state {
  display: none;
}

.modal .modal-trigger {
  padding: 0.8em 1em;
}

.modal .modal-fade-screen {
  -webkit-transition: opacity 0.25s ease;
  transition: opacity 0.25s ease;
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background-color: #222;
  opacity: 0;
  padding-top: 0.6em;
  text-align: left;
  visibility: hidden;
  display: none;
  z-index: 1;
}

@media screen and (min-width: 53.75em) {
  .modal .modal-fade-screen {
    padding-top: 10em;
  }
}

.modal .modal-fade-screen .modal-bg {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  cursor: pointer;
}

.modal .modal-close {
  position: absolute;
  top: 1.5em;
  right: 1.5em;
  height: 1.5em;
  width: 1.5em;
  background: #fff;
  cursor: pointer;
}

.modal .modal-close:after, .modal .modal-close:before {
  position: absolute;
  top: 3px;
  right: 3px;
  bottom: 0;
  left: 50%;
  -webkit-transform: rotate(45deg);
  transform: rotate(45deg);
  height: 1.5em;
  width: 0.15em;
  background: #ccc;
  content: '';
  display: block;
  margin: -3px 0 0 -1px;
}

.modal .modal-close:hover:after, .modal .modal-close:hover:before {
  background: #b3b3b3;
}

.modal .modal-close:before {
  -webkit-transform: rotate(-45deg);
  transform: rotate(-45deg);
}

.modal .modal-inner {
  -webkit-transition: opacity 0.25s ease;
  transition: opacity 0.25s ease;
  background: #fff;
  border-radius: 3px;
  margin-top: 0;
  margin: auto;
  max-height: 95%;
  overflow: visible;
  padding: 1.5em;
  position: absolute;
  top: 50%;
  -webkit-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  left: 50%;
  width: 95%;
}

.modal .modal-inner h3 {
  margin-top: 0;
}

.modal .modal-inner ul + h3 {
  margin-top: 1em;
}

@media screen and (min-width: 40em) {
  .modal .modal-inner {
    max-height: 70%;
    padding: 3em;
    width: 85%;
  }
}

@media screen and (min-width: 53.75em) {
  .modal .modal-inner {
    width: 55%;
  }
}

.modal .modal-inner h1 {
  color: #333;
  margin-bottom: 0 0 0.6em 0;
  text-align: left;
  text-transform: capitalize;
}

.modal .modal-inner p {
  color: #333;
  line-height: 1.4;
}

.modal .modal-inner .modal-intro {
  font-weight: 800;
}

.modal .modal-inner .modal-content {
  color: #333;
}

@media screen and (min-width: 40em) {
  .modal .modal-inner .modal-content {
    -webkit-columns: 2 8em;
    -moz-columns: 2 8em;
    columns: 2 8em;
  }
}

.modal .modal-inner a.cta {
  color: #fff;
  display: inline-block;
  margin-right: 0.5em;
  margin-top: 1em;
}

.modal .modal-inner a.cta:last-child {
  padding: 0 2em;
}

.modal .modal-state:checked + .modal-fade-screen {
  opacity: 1;
  visibility: visible;
  display: block;
}

.modal .makevisible {
  opacity: 1;
  visibility: visible;
  display: block;
}

.modal-open {
  overflow: hidden;
  -webkit-transition: all .4s;
  transition: all .4s;
}

.modal-content img {
  max-width: 500px !important;
  margin: 30px auto;
  display: block;
}

.eynavigation {
  margin: 2em 0 0;
}

.eynavigation .group {
  box-sizing: border-box;
  width: 22%;
}

@media (min-width: 768px) {
  .eynavigation .group {
    margin-bottom: 20px !important;
  }
}

@media (max-width: 767px) {
  .eynavigation .group {
    display: block;
    width: 30%;
    margin-left: auto;
    margin-right: auto;
  }
}

@media (min-width: 768px) {
  .eynavigation .group {
    float: left;
  }
  .eynavigation .group + .group {
    margin: 0 0 0 2%;
  }
}

@media (min-width: 768px) {
  .eynavigation ul#mobilemenu {
    display: none;
  }
}

@media (max-width: 767px) {
  .eynavigation ul#mobilemenu {
    display: block;
    width: 40%;
    float: left;
    font-weight: bold;
    font-size: 16px;
  }
  .eynavigation ul#mobilemenu:before {
    content: "Advisory:";
    color: #ffe600;
    margin-bottom: 1em;
    display: block;
  }
  .eynavigation ul#mobilemenu li {
    margin: 0;
    padding: 0;
  }
  .eynavigation ul#mobilemenu li a {
    margin-bottom: 5px;
  }
}

.eynavigation #eymainmenu {
  float: left;
  width: 40%;
  padding: 0;
  overflow: hidden;
}

@media screen and (min-width: 320px) {
  .eynavigation #eymainmenu {
    border-left: 1px solid #555;
    margin-left: 2em;
  }
}

@media screen and (min-width: 320px) {
  .eynavigation #eymainmenu:before {
    margin-left: 2em;
    margin-bottom: 1em;
    content: "ey.com:";
    color: #999;
    font-weight: bold;
    font-size: 16px;
    display: block;
  }
}

.eynavigation #eymainmenu .group {
  width: auto;
  margin: 0 0 0 2em;
}

.eynavigation #eymainmenu .group h3 {
  font-size: 16px;
}

.eynavigation h3 a {
  color: #ffe600;
  font-weight: bold;
  text-align: left;
  margin-top: 0;
}

@media (max-width: 767px) {
  .eynavigation h3 a {
    color: #808080;
  }
}

.eynavigation .group li {
  font-size: 13.6px;
  margin: 7px 0;
}

@media (max-width: 767px) {
  .eynavigation .group li {
    display: none;
  }
}

.eynavigation a {
  border-radius: 3px;
  color: #fff;
  width: 100%;
  display: block;
  padding: 2px;
}

.eynavigation a:hover {
  color: #ffe600;
}

header.navigation {
  position: absolute;
  background: transparent;
  z-index: 101;
}

header.navigation.fxd {
  background: transparent;
}

header.navigation.fxd.smallnav {
  background: #000;
}

.navigation-wrapper {
  background: transparent;
}

.main-nav {
  width: 50px;
}

.main-nav .modal-inner {
  background: transparent !important;
  padding: 0 !important;
  max-height: 100%;
}

.main-nav .modal-close {
  background: transparent;
  right: 0.2em;
}

.main-nav .modal-trigger {
  font-size: 40px;
  color: #FFF;
  padding: 0.5em 0;
}

.main-nav .modal-inner {
  height: 100%;
}

@media screen and (min-width: 53.75em) {
  .main-nav .modal-fade-screen {
    padding-top: 0;
  }
}

.eynavigation .localnav {
  float: left;
  width: 40%;
}

@media (max-width: 767px) {
  .modal .modal-inner {
    position: relative;
    -webkit-transform: none;
    transform: none;
    overflow: scroll;
    left: 0;
    padding: 30px;
  }
  div.eynavigation {
    margin: 2em 0 0;
  }
  div.eynavigation #eymainmenu {
    overflow: visible;
  }
  div.eynavigation nav {
    position: relative;
    left: 10px;
    width: 100%;
    -webkit-transform: none;
    transform: none;
  }
  div.eynavigation .article-subnav {
    width: 50%;
    margin-left: 0;
  }
  div.eynavigation .localnav {
    float: left;
    overflow: hidden;
    width: 100%;
  }
  div.eynavigation .localnav li {
    font-size: 15px;
    line-height: 1.2;
    margin: 0 0 1em;
    padding: 0;
    border: none;
  }
  div.eynavigation .localnav li a {
    color: #fff;
    padding: 0;
    border: none;
    margin: 0;
  }
  div.eynavigation .localnav li a.active {
    color: #ffe600;
  }
  .eynavigation .article-subnav {
    width: 50%;
    margin-left: 0;
    display: block !important;
  }
  .eynavigation #eymainmenu {
    margin-left: 0;
    border: none;
    width: 30%;
  }
}

.modal .modal-fade-screen {
  display: block;
}

.generic-modal {
  position: relative;
  z-index: 1000;
}

.modal .modal-inner {
  -webkit-transition: opacity 0.25s ease;
  transition: opacity 0.25s ease;
  opacity: 0;
  -webkit-transform: translate(-50%, -50%);
          transform: translate(-50%, -50%);
  background: #fff;
  border-radius: 3px;
  margin: auto;
  max-height: 95%;
  overflow: visible;
  overflow-Y: scroll;
  padding: 1.5em;
  position: absolute;
  top: 50%;
  left: 50%;
  width: 95%;
}

.modal-open .modal .modal-inner {
  opacity: 1;
}

@media (min-width: 768px) {
  .modal .modal-inner {
    max-width: 500px;
  }
}

@media (min-width: 940px) {
  .modal .modal-inner {
    max-width: 720px;
  }
}

@media (max-width: 767px) {
  .modal .modal-inner h3 {
    font-size: 1.2rem;
  }
  .modal .modal-inner p {
    font-size: 0.8rem;
  }
}

.sliding-panel-content {
  position: fixed;
  top: 0px;
  right: auto;
  bottom: 0px;
  left: 0px;
  height: 100%;
  width: 220px;
  -webkit-transform: translateX(-220px);
  transform: translateX(-220px);
  -webkit-transition: all 0.25s linear;
  transition: all 0.25s linear;
  background: #404040;
  z-index: 999999;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.sliding-panel-content ul {
  padding: 0;
  margin: 0;
}

.sliding-panel-content li {
  list-style: none;
}

.sliding-panel-content li a {
  border-bottom: 1px solid #333;
  color: #fff;
  display: block;
  font-weight: bold;
  padding: 1em;
  text-decoration: none;
}

.sliding-panel-content li a:focus {
  background-color: #4d4d4d;
}

.sliding-panel-content li a:hover {
  background-color: #369;
  color: #fff;
}

.sliding-panel-content.is-visible {
  -webkit-transform: translateX(0);
  transform: translateX(0);
}

.sliding-panel-fade-screen {
  position: fixed;
  top: 0px;
  right: 0px;
  bottom: 0px;
  left: 0px;
  -webkit-transition: all 0.15s ease-out 0s;
  transition: all 0.15s ease-out 0s;
  background: black;
  opacity: 0;
  visibility: hidden;
  z-index: 999998;
}

.sliding-panel-fade-screen.is-visible {
  opacity: 0.4;
  visibility: visible;
}

.sliding-panel-button {
  padding: 10px 16px;
  display: inline-block;
  cursor: pointer;
  position: relative;
  outline: none;
}

@media (min-width: 768px) {
  .sliding-panel-button {
    display: none;
  }
}

.sliding-panel-button img {
  height: 1.3em;
}

.sl-landing > .gallery {
  background: #000 !important;
}

@media (min-width: 940px) {
  .section-contact .gallery {
    width: 80%;
    margin-left: auto;
    margin-right: auto;
    margin-top: 30px;
  }
  .section-contact .gallery .flickity-prev-next-button.next {
    right: 30px;
  }
}

.gallery-cell {
  width: 33.333%;
  box-sizing: border-box;
  display: block;
}

[class^="section"] .gallery-cell {
  min-height: 60px;
}

@media (min-width: 768px) {
  [class^="section"] .gallery-cell {
    min-height: 340px;
  }
}

@media (min-width: 940px) {
  [class^="section"] .gallery-cell {
    min-height: 120px;
  }
}

.section-contact .gallery-cell {
  width: 80%;
  min-height: 460px;
}

@media (max-device-width: 667px) and (orientation: landscape) {
  .section-contact .gallery-cell {
    width: 33%;
    min-height: 320px;
  }
}

@media (min-width: 768px) {
  .section-contact .gallery-cell {
    width: 33%;
  }
}

@media (min-width: 940px) {
  .section-contact .gallery-cell {
    width: 33%;
    min-height: 470px;
  }
}

.section-contact .gallery-cell .caption,
.section-contact .gallery-cell .thumbnail {
  margin: 0 10px;
}

@media (max-device-width: 667px) and (orientation: landscape) {
  .section-contact .gallery-cell .caption,
  .section-contact .gallery-cell .thumbnail {
    font-size: 0.75rem;
  }
}

.gallery-cell img {
  width: 100%;
}

.flickity-page-dots {
  z-index: 1;
  bottom: -25px;
}

.sl-landing .flickity-page-dots {
  bottom: 5px;
}

.flickity-page-dots .dot {
  background: #ccc;
  opacity: 0.5;
}

.flickity-page-dots .dot.is-selected {
  opacity: 1;
}

.flickity-prev-next-button.previous {
  left: 20px;
}

.flickity-prev-next-button.next {
  right: 20px;
}

.sl-landing .flickity-viewport {
  overflow: hidden;
}

@media (max-width: 767px) {
  .sl-landing .flickity-viewport {
    height: 100vh;
  }
}

.sl-landing .gallery {
  background: transparent;
  display: block;
}

.sl-landing .gallery-cell {
  width: 100%;
  overflow: hidden;
  padding-left: 7%;
  margin-right: 10px;
  background: #eee;
  background-repeat: no-repeat;
}

@media (max-width: 767px) {
  .sl-landing .gallery-cell {
    max-width: 100%;
  }
}

.sl-landing .flickity-prev-next-button {
  display: none;
}

.tl-item .caption {
  margin: 20px;
}

.section-latest-thinking .flickity-prev-next-button {
  top: 15%;
}

@media (min-width: 768px) {
  .section-latest-thinking .flickity-page-dots {
    bottom: -1.5em;
  }
}

.section-latest-thinking .gallery-cell {
  width: 33.33%;
  margin-right: 10px;
}

@media (max-width: 767px) {
  .section-latest-thinking .gallery-cell {
    width: 100%;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    display: flex;
  }
}

.section-latest-thinking .gallery-cell .caption {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-align: center;
      -ms-flex-align: center;
          align-items: center;
  min-height: 7.5em;
}

@media (min-width: 768px) {
  .section-latest-thinking .gallery-cell .caption {
    margin: 20px 60px;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-align: center;
        -ms-flex-align: center;
            align-items: center;
    font-size: 1.2em;
    min-height: 12.5em;
  }
}

@media (max-width: 414px) {
  .section-latest-thinking .gallery-cell .caption {
    min-height: 11em;
  }
}

.section-latest-thinking .gallery-cell .thumbnail {
  display: none;
}

.section-latest-thinking .gallery-cell img,
.section-latest-thinking .gallery-cell img[src$="required.jpg"] {
  display: none;
}

.section-latest-thinking .gallery-cell:nth-child(n+1) {
  background: #f04c3e;
  color: #fff;
}

.section-latest-thinking .gallery-cell:nth-child(2n+1) {
  background: #00a3ae;
  color: #fff;
}

.section-latest-thinking .gallery-cell:nth-child(3n+1) {
  background: #91278f;
  color: #fff;
}

.section-latest-thinking .gallery-cell:nth-child(4n+1) {
  background: #2c973e;
  color: #fff;
}

.section-latest-thinking .gallery-cell:nth-child(5n+1) {
  background: #ac98db;
  color: #fff;
}

.flickity-prev-next-button {
  width: 33px;
  height: 33px;
  background: rgba(255, 255, 255, 0.5);
}

@media (max-width: 375px) {
  .flickity-prev-next-button {
    width: 22px;
    height: 22px;
    padding: 5px;
  }
}

article.type-system-ey {
  text-align: righ;
  position: relative;
  background: #fff;
}

article.type-system-ey::after {
  clear: both;
  content: "";
  display: block;
}

h1,
h2,
h3,
p {
  margin: 0;
}

hr {
  border-bottom: 1px solid #ccc;
  border-left: none;
  border-right: none;
  border-top: none;
  margin: 1.4em 0;
}

p {
  color: #333;
  line-height: 1.4;
}

a {
  color: #369;
  text-decoration: none;
}

article a {
  font-weight: bold;
}

.type {
  border-bottom: 1px solid #ccc;
  color: #808080;
  display: inline-block;
  font-family: "Helvetica", sans-serif;
  font-size: 0.7em;
  font-weight: 900;
  letter-spacing: 1px;
  margin-bottom: 2em;
  padding: 0.1em 0;
  text-align: left;
  text-transform: uppercase;
}

h1 {
  font-family: "Interstate-bold", sans-serif;
  line-height: 1;
  font-size: 2em;
  font-weight: normal;
  margin-bottom: 0.6em;
  color: #646464;
}

@media screen and (min-width: 53.75em) {
  h1 {
    font-size: 2.4em;
  }
}

.maincolumn h2,
section h2 {
  font-family: "Interstate-bold", sans-serif;
  font-size: 1.6em;
  font-weight: 400;
  line-height: 1.1em;
  margin-bottom: 0.5em;
  letter-spacing: -.03em;
  color: #646464;
}

@media screen and (min-width: 40em) {
  .maincolumn h2,
  section h2 {
    width: 80%;
    letter-spacing: -0.03em;
    line-height: 1.1;
    padding: 0;
    margin: 1em 0;
  }
  .type-system-ey .maincolumn h2, .type-system-ey
  section h2 {
    font-size: 2.4em;
    margin: 0 0 0.5em;
    font-weight: normal;
  }
  .sl-landing .maincolumn h2, .sl-landing
  section h2 {
    font-size: 2.8em;
    padding-top: 40px;
    margin-top: 0;
  }
}

@media (max-width: 767px) {
  .maincolumn h2,
  section h2 {
    font-size: 1.5em;
    margin-bottom: 1em;
  }
  .maincolumn .maincolumn h2:first-child, .maincolumn
  section h2:first-child {
    margin-top: -1em;
  }
}

@media (min-width: 569px) and (max-width: 768px) {
  .maincolumn h2,
  section h2 {
    margin-top: 0;
  }
}

@media only screen and (min-width: 737px) {
  .type-system-ey .maincolumn h2, .type-system-ey
  section h2 {
    margin: 1em 0;
  }
}

code {
  background: #F7F7F7;
  border-radius: 4.5px;
  border: 1px solid #E0E0E0;
  font-family: monaco;
  font-size: 0.65em;
  font-style: normal;
  padding: 0.1em 0.4em;
  white-space: nowrap;
}

h3 {
  font-family: "Interstate-bold", sans-serif;
  font-size: 1.3em;
  color: #646464;
  font-weight: 700;
  line-height: 1.4em;
  margin-top: 0.5em;
  margin-bottom: 0.5em;
  letter-spacing: -.02em;
}

.accordion h3,
.gallery-cell h3 {
  font-size: 1.1em;
}

p.date {
  color: rgba(51, 51, 51, 0.4);
  font-family: "EYInterstate", "EY", sans-serif;
  font-size: 0.8em;
  margin-bottom: 0.5em;
}

p {
  font-family: "Helvetica", sans-serif;
  font-weight: 300;
  margin: 1em 0;
}

hr {
  width: 3em;
}

a.read-more {
  display: inline-block;
  font-family: "EYInterstate", "EY", sans-serif;
  font-size: 0.8em;
  font-weight: 700;
  margin-left: 0.2em;
  position: relative;
  text-transform: uppercase;
}

a.read-more span {
  font-size: 1.7em;
  position: absolute;
  right: -10px;
  top: -2px;
}

p.author,
p.contact {
  font-family: "EYInterstate", "EY", sans-serif;
  font-style: italic;
  color: #808080;
}

.lighttext blockquote,
.lighttext h1,
.lighttext h2,
.lighttext h3,
.lighttext h4,
.lighttext h5,
.lighttext li,
.lighttext p {
  color: #fff;
}

.eyhero,
.flickity-viewport,
.hero {
  position: relative;
  top: 0;
  left: 0;
  right: 0;
  overflow: visible;
}

.eyhero-home:before,
.eyhero:before {
  content: '';
  display: block;
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background: rgba(0, 0, 0, 0.15);
}

.eyhero,
.flickity-viewport,
.hero {
  overflow: hidden;
}

@media (min-width: 668px) {
  .eyhero,
  .flickity-viewport,
  .hero {
    min-height: 0;
    height: 450px;
  }
}

/*make hero image square on mobile*/
.fixedhero {
  background-size: cover;
}

@media (min-width: 940px) {
  .fixedhero {
    background-attachment: fixed !important;
  }
}

/* fluid type and box via http://madebymike.com.au/writing/fluid-type-calc-examples */
/*! ========================================================================

    PRECISE CONTROL OVER RESPONSIVE TYPOGRAPHY FOR SASS
    ---------------------------------------------------
    Indrek Paas @indrekpaas

    Inspired by Mike Riethmuller's Precise control over responsive typography
    http://madebymike.com.au/writing/precise-control-responsive-typography/

    `strip-unit()` function by Hugo Giraudel

    02.10.2015 Add support for multiple properties

    ========================================================================  */
/* fluid type via http://madebymike.com.au/writing/fluid-type-calc-examples */
/* Single property */
.headline-container h1 {
  font-size: 14px;
}

@media screen and (min-width: 320px) {
  .headline-container h1 {
    font-size: calc(14px + 14 * ((100vw - 320px) / 928));
  }
}

@media screen and (min-width: 1248px) {
  .headline-container h1 {
    font-size: 28px;
  }
}

.headline-container.larger-2 h1 {
  font-size: 16.8px;
}

@media screen and (min-width: 320px) {
  .headline-container.larger-2 h1 {
    font-size: calc(16.8px + 16.8 * ((100vw - 320px) / 928));
  }
}

@media screen and (min-width: 1248px) {
  .headline-container.larger-2 h1 {
    font-size: 33.6px;
  }
}

.headline-container.larger-3 h1 {
  font-size: 18.2px;
}

@media screen and (min-width: 320px) {
  .headline-container.larger-3 h1 {
    font-size: calc(18.2px + 18.2 * ((100vw - 320px) / 928));
  }
}

@media screen and (min-width: 1248px) {
  .headline-container.larger-3 h1 {
    font-size: 36.4px;
  }
}

.headline-container.larger-4 h1 {
  font-size: 19.6px;
}

@media screen and (min-width: 320px) {
  .headline-container.larger-4 h1 {
    font-size: calc(19.6px + 19.6 * ((100vw - 320px) / 928));
  }
}

@media screen and (min-width: 1248px) {
  .headline-container.larger-4 h1 {
    font-size: 39.2px;
  }
}

.headline-container.larger-5 h1 {
  font-size: 21px;
}

@media screen and (min-width: 320px) {
  .headline-container.larger-5 h1 {
    font-size: calc(21px + 21 * ((100vw - 320px) / 928));
  }
}

@media screen and (min-width: 1248px) {
  .headline-container.larger-5 h1 {
    font-size: 42px;
  }
}

.headline-container.larger-6 h1 {
  font-size: 22.4px;
}

@media screen and (min-width: 320px) {
  .headline-container.larger-6 h1 {
    font-size: calc(22.4px + 22.4 * ((100vw - 320px) / 928));
  }
}

@media screen and (min-width: 1248px) {
  .headline-container.larger-6 h1 {
    font-size: 44.8px;
  }
}

.headline-container.smaller-2 h1 {
  font-size: 12.6px;
}

@media screen and (min-width: 320px) {
  .headline-container.smaller-2 h1 {
    font-size: calc(12.6px + 14 * ((100vw - 320px) / 928));
  }
}

@media screen and (min-width: 1248px) {
  .headline-container.smaller-2 h1 {
    font-size: 26.6px;
  }
}

.headline-container.smaller-3 h1 {
  font-size: 12.6px;
}

@media screen and (min-width: 320px) {
  .headline-container.smaller-3 h1 {
    font-size: calc(12.6px + 12.6 * ((100vw - 320px) / 928));
  }
}

@media screen and (min-width: 1248px) {
  .headline-container.smaller-3 h1 {
    font-size: 25.2px;
  }
}

.headline-container.smaller-4 h1 {
  font-size: 11.9px;
}

@media screen and (min-width: 320px) {
  .headline-container.smaller-4 h1 {
    font-size: calc(11.9px + 11.9 * ((100vw - 320px) / 928));
  }
}

@media screen and (min-width: 1248px) {
  .headline-container.smaller-4 h1 {
    font-size: 23.8px;
  }
}

.headline-container.smaller-5 h1 {
  font-size: 11.2px;
}

@media screen and (min-width: 320px) {
  .headline-container.smaller-5 h1 {
    font-size: calc(11.2px + 11.2 * ((100vw - 320px) / 928));
  }
}

@media screen and (min-width: 1248px) {
  .headline-container.smaller-5 h1 {
    font-size: 22.4px;
  }
}

.headline-container.smaller-6 h1 {
  font-size: 10.5px;
}

@media screen and (min-width: 320px) {
  .headline-container.smaller-6 h1 {
    font-size: calc(10.5px + 10.5 * ((100vw - 320px) / 928));
  }
}

@media screen and (min-width: 1248px) {
  .headline-container.smaller-6 h1 {
    font-size: 21px;
  }
}

.headline-container h2 {
  font-size: 10px;
}

@media screen and (min-width: 320px) {
  .headline-container h2 {
    font-size: calc(10px + 10 * ((100vw - 320px) / 928));
  }
}

@media screen and (min-width: 1248px) {
  .headline-container h2 {
    font-size: 20px;
  }
}

.headline-container.smaller-2 h2 {
  font-size: 9px;
}

@media screen and (min-width: 320px) {
  .headline-container.smaller-2 h2 {
    font-size: calc(9px + 9 * ((100vw - 320px) / 928));
  }
}

@media screen and (min-width: 1248px) {
  .headline-container.smaller-2 h2 {
    font-size: 18px;
  }
}

.headline-container.smaller-3 h2 {
  font-size: 9px;
}

@media screen and (min-width: 320px) {
  .headline-container.smaller-3 h2 {
    font-size: calc(9px + 7 * ((100vw - 320px) / 928));
  }
}

@media screen and (min-width: 1248px) {
  .headline-container.smaller-3 h2 {
    font-size: 16px;
  }
}

.headline-container.smaller-4 h2 {
  font-size: 9px;
}

@media screen and (min-width: 320px) {
  .headline-container.smaller-4 h2 {
    font-size: calc(9px + 6 * ((100vw - 320px) / 928));
  }
}

@media screen and (min-width: 1248px) {
  .headline-container.smaller-4 h2 {
    font-size: 15px;
  }
}

.headline-container.smaller-5 h2 {
  font-size: 9px;
}

@media screen and (min-width: 320px) {
  .headline-container.smaller-5 h2 {
    font-size: calc(9px + 5 * ((100vw - 320px) / 928));
  }
}

@media screen and (min-width: 1248px) {
  .headline-container.smaller-5 h2 {
    font-size: 14px;
  }
}

.headline-container.smaller-6 h2 {
  font-size: 9px;
}

@media screen and (min-width: 320px) {
  .headline-container.smaller-6 h2 {
    font-size: calc(9px + 4 * ((100vw - 320px) / 928));
  }
}

@media screen and (min-width: 1248px) {
  .headline-container.smaller-6 h2 {
    font-size: 13px;
  }
}

/* END Single property */
/* fluid type and box via http://madebymike.com.au/writing/fluid-type-calc-examples */
.customheadline .box3x2, .customheadline .frame3x2, .customheadline .noframe, .customjs .box3x2, .customjs .frame3x2, .customjs .noframe, .eyhero .box3x2, .eyhero .frame3x2, .eyhero .noframe, .eyhero-home .box3x2, .eyhero-home .frame3x2, .eyhero-home .noframe, .hero .box3x2, .hero .frame3x2, .hero .noframe,
.customheadline .box4x2, .customheadline .frame4x2, .customjs .box4x2, .customjs .frame4x2, .eyhero .box4x2, .eyhero .frame4x2, .eyhero-home .box4x2, .eyhero-home .frame4x2, .hero .box4x2,
.hero .frame4x2 {
  width: 300px;
}

@media screen and (min-width: 320px) {
  .customheadline .box3x2, .customheadline .frame3x2, .customheadline .noframe, .customjs .box3x2, .customjs .frame3x2, .customjs .noframe, .eyhero .box3x2, .eyhero .frame3x2, .eyhero .noframe, .eyhero-home .box3x2, .eyhero-home .frame3x2, .eyhero-home .noframe, .hero .box3x2, .hero .frame3x2, .hero .noframe,
  .customheadline .box4x2, .customheadline .frame4x2, .customjs .box4x2, .customjs .frame4x2, .eyhero .box4x2, .eyhero .frame4x2, .eyhero-home .box4x2, .eyhero-home .frame4x2, .hero .box4x2,
  .hero .frame4x2 {
    width: calc(270px + 260 * ((100vw - 320px) / 960));
  }
}

@media screen and (min-width: 1280px) {
  .customheadline .box3x2, .customheadline .frame3x2, .customheadline .noframe, .customjs .box3x2, .customjs .frame3x2, .customjs .noframe, .eyhero .box3x2, .eyhero .frame3x2, .eyhero .noframe, .eyhero-home .box3x2, .eyhero-home .frame3x2, .eyhero-home .noframe, .hero .box3x2, .hero .frame3x2, .hero .noframe,
  .customheadline .box4x2, .customheadline .frame4x2, .customjs .box4x2, .customjs .frame4x2, .eyhero .box4x2, .eyhero .frame4x2, .eyhero-home .box4x2, .eyhero-home .frame4x2, .hero .box4x2,
  .hero .frame4x2 {
    width: 560px;
  }
}

@media (max-width: 46em) and (orientation: landscape) {
  .eyhero-headline-1 br,
  .eyhero-subheading-1 br {
    display: none;
  }
}

.frame3x2 {
  background-size: contain;
  position: absolute;
  top: 50%;
  left: 50%;
  -webkit-transform: translateX(-50%) translateY(-55%) scale(0.75);
          transform: translateX(-50%) translateY(-55%) scale(0.75);
}

@media (max-width: 640px) and (orientation: landscape) {
  .frame3x2 h2.eyhero-subheading-1 {
    display: none;
  }
}

@media (max-width: 46em) {
  .frame3x2 {
    -webkit-transform: translateX(-50%) translateY(-50%) scale(1);
            transform: translateX(-50%) translateY(-50%) scale(1);
  }
}

@media (max-width: 46em) and (orientation: landscape) {
  .frame3x2 {
    -webkit-transform: translateX(-50%) translateY(-55%) scale(0.9);
            transform: translateX(-50%) translateY(-55%) scale(0.9);
  }
}

@media (max-width: 375px) and (orientation: portrait) {
  .frame3x2 {
    -webkit-transform: translateX(-50%) translateY(-56%) scale(0.9);
            transform: translateX(-50%) translateY(-56%) scale(0.9);
  }
}

@media (min-width: 650px) {
  .fluid-box {
    -webkit-transform: translateX(-65%) translateY(-50%) scale(1);
            transform: translateX(-65%) translateY(-50%) scale(1);
  }
}

.smartquestion {
  position: relative;
  margin-left: 0;
  padding-bottom: 76.25%;
}

.heading-block {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 58%;
  height: auto;
  text-align: left;
  margin: 0;
  -webkit-transform: translateY(-50%) translateX(-74%);
  transform: translateY(-50%) translateX(-74%);
}

.fluid-box.align-right {
  -webkit-transform: translateX(-20%) translateY(-50%);
  transform: translateX(-20%) translateY(-50%);
}

@font-face {
  font-family: "Interstate";
  src: url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-2.eot");
  src: url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-2.eot?") format("embedded-opentype"), url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-3.woff") format("woff"), url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-1.ttf") format("truetype");
  src: url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-3.woff") format("woff");
  font-style: normal;
  font-weight: normal;
}

[id^="tagline-"] {
  font-family: "Interstate";
  fill: #ffffff;
  letter-spacing: 1px;
  font-size: 24px;
  letter-spacing: -.03em;
}

.eyhero-headline-1,
.eyhero-subheading-1 {
  font-family: 'Interstate', Helvetica, Arial, sans-serif;
}

.eyhero-headline-1,
.eyhero-subheading-1 {
  color: #FFF;
}

.dark-type svg #gradient {
  fill: url("#lightGradient");
}

.dark-type svg [id^="tagline-"] {
  fill: #000;
}

.dark-type .eyhero-headline-1,
.dark-type .eyhero-subheading-1 {
  color: #000;
}

.fluid-box svg #box {
  display: none;
  fill: #ffe600;
}

.fluid-box.frame3x2.box3x2 svg #box {
  display: block !important;
}

.fluid-box.frame3x2.box3x2 .eyhero-headline-1,
.fluid-box.frame3x2.box3x2 .eyhero-subheading-1 {
  color: #333;
}

.fluid-box.frame3x2.box3x2 #dots,
.fluid-box.frame3x2.box3x2 #gradient,
.fluid-box.frame3x2.box3x2 .tab-content,
.fluid-box.frame3x2.box3x2 [id^="frame-"] {
  display: none !important;
}

.eyhero svg,
.flickity-viewport svg,
.hero svg {
  width: 100%;
  margin-left: auto;
  margin-right: auto;
  position: absolute;
  top: 50%;
  -webkit-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  left: 50%;
}

/*hide all taglines*/
[id^="tagline-"] {
  display: none;
  font-family: "Interstate", Arial, sans-serif;
  fill: #ffffff;
  letter-spacing: 1px;
  font-size: 23px;
  letter-spacing: -.01em;
  font-weight: 300;
}

#tagline-en-gl {
  display: block;
}

/*when HTML lang tag matches, show appropriate lang tagline*/
/* Request on Nov 8, 2016 via Melanie/Jeff to add translation */
[lang="fr-ca"] svg [id^="tagline-en"] {
  display: none !important;
}

[lang*="fr-ca"] #tagline-ca-fr {
  display: block;
}

/*Language-specific font sizes*/
svg [id^="tagline-en"] {
  font-size: 22px;
}

#select-box {
  display: inline-block;
  margin: 10px auto;
}

body {
  margin: 0;
  padding: 0;
}

.hero-text-right .headline-container {
  -webkit-transform: translate(-10%, -50%);
          transform: translate(-10%, -50%);
  margin-left: 0;
  right: 5%;
}

#sec-contact {
  overflow: hidden;
}

#sec-contact li {
  margin-bottom: 1em;
}

#sec-contact li > p {
  margin: 0;
}

#sec-contact .twitterfeed {
  float: left;
  display: block;
  margin-right: 4.8291579146%;
  width: 30.1138947236%;
}

#sec-contact .twitterfeed:last-child {
  margin-right: 0;
}

#sec-contact .contact-details {
  float: left;
  display: block;
  margin-right: 4.8291579146%;
  width: 65.0569473618%;
}

#sec-contact .contact-details:last-child {
  margin-right: 0;
}

@media (max-width: 375px) {
  .accordion-body > .gallery-cell {
    float: none;
    width: 100%;
  }
}

@media (min-width: 480px) {
  .accordion-body > .gallery-cell {
    float: left;
    width: 50%;
  }
  .accordion-body > .gallery-cell:nth-child(2n+1) {
    clear: left;
  }
}

@media (min-width: 768px) {
  .accordion-body > .gallery-cell:nth-child(2n+1) {
    clear: none;
  }
  .accordion-body > .gallery-cell {
    float: left;
    width: 33%;
  }
  .accordion-body > .gallery-cell:nth-child(3n+1) {
    clear: left;
  }
}

@media (min-width: 940px) {
  .accordion-body > .gallery-cell:nth-child(3n+1) {
    clear: none;
  }
  .accordion-body > .gallery-cell {
    float: left;
    width: 25%;
  }
  .accordion-body > .gallery-cell:nth-child(4n+1) {
    clear: left;
  }
}

.article-subnav {
  display: block;
}

@media (max-width: 767px) {
  .article .article-subnav {
    display: none;
  }
}

@media (max-width: 375px) {
  .article-subnav {
    width: 60%;
    margin-left: auto;
    margin-right: auto;
  }
}

@media screen and (min-width: 53.75em) {
  .article-subnav {
    float: left;
    display: block;
    margin-right: 2.3576515979%;
    width: 31.7615656014%;
  }
  .article-subnav:last-child {
    margin-right: 0;
  }
}

.article-subnav #featuremenu li,
.article-subnav li {
  list-style-type: none;
  margin: 0;
  padding: 0;
}

.article-subnav a {
  color: #369;
  text-decoration: none;
  font-weight: bold;
  -webkit-transition: all 0.25s;
  transition: all 0.25s;
}

.article-subnav a:hover {
  color: #333;
}

.article-subnav .subnav-link {
  padding: 10px 20px;
  border-bottom: 1px solid rgba(51, 102, 153, 0.2);
  display: block;
  outline: none;
}

@media (max-width: 375px) {
  .article-subnav .subnav-link {
    display: block;
    padding: 0;
    margin-bottom: 1em;
    color: #FFF;
    text-align: left;
  }
}

@media (min-width: 768px) {
  .article-subnav .subnav-link {
    display: block;
    margin-right: 1.4em;
    padding: 0.7em 0;
  }
}

.article-subnav article h4 {
  margin: 0 0 0.5em;
}

.article-subnav article p {
  color: #333;
  line-height: 1.4;
}

.article-subnav article section p:last-of-type {
  margin-bottom: 2em;
}

@media screen and (min-width: 53.75em) {
  .article-subnav article {
    float: left;
    display: block;
    margin-right: 2.3576515979%;
    width: 65.8807828007%;
  }
  .article-subnav article:last-child {
    margin-right: 0;
  }
}

@media (max-width: 377px) {
  #featuremenu li {
    display: block;
    font-size: 14px;
  }
}

#featuremenu a {
  border-bottom: 1px solid rgba(51, 102, 153, 0.2);
  display: block;
  margin-right: 1.4em;
  padding: 0.7em 0;
}

@media (max-width: 767px) {
  #featuremenu a {
    color: #fff;
    background: rgba(255, 255, 255, 0.2);
    margin-bottom: 2px;
    padding: 10px 20px;
  }
}

#featuremenu li.nav-current a {
  color: #000;
}

@media (max-width: 767px) {
  #featuremenu li.nav-current a {
    color: #ffe600;
  }
}

.js-menu a {
  color: #369;
  text-decoration: none;
}

.js-menu a.active {
  color: #ffe600;
  font-weight: bold;
}

@media only screen and (max-width: 767px) {
  #featuremenu.mobilefake {
    margin-top: 0;
    width: 100%;
  }
  #featuremenu.mobilefake li {
    width: 50%;
    margin-bottom: 0;
  }
  #featuremenu li {
    float: left;
    width: auto;
    width: 100%;
    margin: 0;
    padding: 5px;
    line-height: 1.2;
  }
  #featuremenu li.nav-current a {
    color: #ffe600 !important;
    width: 100%;
    float: left;
  }
  #featuremenu li a {
    color: #fff;
    display: block;
    background: rgba(255, 255, 255, 0.2);
    margin-right: 0;
  }
  #featuremenu li a.advisory-home-link {
    color: #fff;
    font-weight: 700 !important;
  }
}

@media (max-device-width: 667px) and (orientation: landscape) {
  #mainnav .mobilefake {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-wrap: wrap;
        flex-wrap: wrap;
  }
  #mainnav .mobilefake a {
    display: inline-block;
    width: 48%;
    padding: 5px;
    margin: 0 2% 2% 0;
    -webkit-box-flex: 1;
        -ms-flex: 1 1 auto;
            flex: 1 1 auto;
  }
}

header.fxd {
  position: fixed;
  z-index: 999;
}

header.fake {
  position: static;
  z-index: 0;
  opacity: 1;
  background: #000;
  padding: 10px 0;
  -webkit-transition: all 0.8s;
  transition: all 0.8s;
}

header.fake img {
  display: none;
}

@media (max-width: 767px) {
  header.fake {
    display: none;
  }
}

.fake.smallnav {
  opacity: 0;
  -webkit-transform: translateY(30px);
          transform: translateY(30px);
}

.main-header .fakenav {
  margin: 10px auto;
}

@media (max-width: 670px) {
  .main-header .fakenav {
    display: none;
  }
}

iframe {
  z-index: 1;
}

.smnt-subMenu,
.zfakenav {
  z-index: 1;
  min-width: 380px;
  position: absolute;
  bottom: 15px;
  left: 50%;
  -webkit-transform: translateX(-50%);
  transform: translateX(-50%);
}

@media (max-device-width: 1024px) and (orientation: portrait) {
  .smnt-subMenu,
  .zfakenav {
    left: 50%;
  }
}

.mobilefake a {
  display: block;
  width: 100%;
  color: #ffe600;
}

.smnt-subNavBtn {
  -webkit-font-smoothing: antialiased;
  text-decoration: none;
  text-align: center;
}

.is-smallmenu .smnt-subNavBtn,
.darklogo .smnt-subNavBtn {
  color: #ffe600;
}

.fakenav a,
.smnt-subMenu a {
  color: #ffe600;
}

.fakenav a:hover, .fakenav a:active,
.smnt-subMenu a:hover,
.smnt-subMenu a:active {
  color: #fff;
}

.smnt-active {
  color: #fff !important;
}

.smnt-end {
  margin: 0;
}

.flex-container {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-orient: horizontal;
  -webkit-box-direction: normal;
      -ms-flex-direction: row;
          flex-direction: row;
  -ms-flex-wrap: nowrap;
      flex-wrap: nowrap;
  -webkit-box-pack: justify;
      -ms-flex-pack: justify;
          justify-content: space-between;
  -ms-flex-line-pack: stretch;
      align-content: stretch;
  -webkit-box-align: start;
      -ms-flex-align: start;
          align-items: flex-start;
}

.flex-container .flex-item {
  -ms-flex-item-align: auto;
      -ms-grid-row-align: auto;
      align-self: auto;
  padding: 0;
  text-align: center;
}

.flex-container .flex-item:nth-child(1) {
  -webkit-box-flex: 1;
      -ms-flex: 1 1 140px;
          flex: 1 1 140px;
  position: relative;
  height: auto;
  box-sizing: border-box;
  padding: 0;
}

.flex-container .flex-item.site-nav {
  -webkit-box-flex: 4;
      -ms-flex: 4 3 100%;
          flex: 4 3 100%;
  -ms-flex-pack: distribute;
      justify-content: space-around;
  -ms-flex-item-align: end;
      align-self: flex-end;
  padding-bottom: 10px;
}

.flex-container .flex-item.site-nav ul {
  display: -webkit-inline-box;
  display: -ms-inline-flexbox;
  display: inline-flex;
  -ms-flex-item-align: end;
      align-self: flex-end;
  -ms-flex-pack: distribute;
      justify-content: space-around;
  overflow: hidden;
  width: 100%;
}

.flex-container .flex-item.site-nav ul li {
  text-align: center !important;
  padding: 0 1%;
}

.flex-container .flex-item.actions {
  -ms-flex-item-align: start;
      align-self: flex-start;
  -webkit-box-flex: 1;
      -ms-flex: 1;
          flex: 1;
  padding: 10px 0 20px;
}

.smnt-inner {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  max-width: 800px;
  -webkit-box-orient: horizontal;
  -webkit-box-direction: normal;
      -ms-flex-direction: row;
          flex-direction: row;
  -ms-flex-wrap: nowrap;
      flex-wrap: nowrap;
  -ms-flex-pack: distribute;
      justify-content: space-around;
  -ms-flex-line-pack: stretch;
      align-content: stretch;
  -webkit-box-align: start;
      -ms-flex-align: start;
          align-items: flex-start;
  position: relative;
  overflow: hidden;
  width: auto;
  padding: 0;
  font-weight: 400;
  margin: 0 auto;
}

.smnt-inner > a {
  -ms-flex-item-align: auto;
      -ms-grid-row-align: auto;
      align-self: auto;
}

.main-header .container {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-align: center;
      -ms-flex-align: center;
          align-items: center;
}

.main-header .container .eylogo {
  width: 140px;
  margin: 10px 0 0 20px;
}

.main-header .container .eyscrollogo {
  -webkit-box-flex: 1;
      -ms-flex: 1 1 100px;
          flex: 1 1 100px;
}

.main-header .container .fakenav {
  -webkit-box-flex: 1;
      -ms-flex: 1 1 auto;
          flex: 1 1 auto;
}

.main-header .container .right {
  -webkit-box-flex: 1;
      -ms-flex: 1 1 90px;
          flex: 1 1 90px;
}

/* fluid type and box via http://madebymike.com.au/writing/fluid-type-calc-examples/ */
/*! ========================================================================
    Mixin via http://www.sassmeister.com/gist/7f22e44ace49b5124eec

    PRECISE CONTROL OVER RESPONSIVE TYPOGRAPHY FOR SASS
    ---------------------------------------------------
    Indrek Paas @indrekpaas

    Inspired by Mike Riethmuller's Precise control over responsive typography
    http://madebymike.com.au/writing/precise-control-responsive-typography/

    `strip-unit()` function by Hugo Giraudel

    02.10.2015 Add support for multiple properties

    ========================================================================  */
.fakenav {
  font-family: "EYInterstate", "Interstate", sans-serif;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-pack: justify;
      -ms-flex-pack: justify;
          justify-content: space-between;
  -ms-flex-wrap: wrap;
      flex-wrap: wrap;
  margin-left: auto;
  margin-right: auto;
  padding: 0;
  width: 200px;
}

@media screen and (min-width: 768px) {
  .fakenav {
    width: calc(500px + 220 * ((100vw - 320px) / 960));
  }
}

@media screen and (min-width: 1280px) {
  .fakenav {
    width: 780px;
  }
}

.fakenav a {
  -webkit-box-flex: 1;
      -ms-flex: 1 1 auto;
          flex: 1 1 auto;
  color: #fff;
  padding: 5px 8px;
  list-style-type: none;
  text-decoration: none;
  text-align: center;
  white-space: nowrap;
}

/* fluid type via http://madebymike.com.au/writing/fluid-type-calc-examples */
/* Single property */
.fakenav a {
  font-size: 10px;
}

@media screen and (min-width: 320px) {
  .fakenav a {
    font-size: calc(10px + 9 * ((100vw - 320px) / 1046));
  }
}

@media screen and (min-width: 1366px) {
  .fakenav a {
    font-size: 19px;
  }
}

.darklogo {
  background-color: #fff;
}

header.main-header {
  position: fixed;
  z-index: 1000;
  width: 100%;
  top: 0;
  background: transparent;
  -webkit-transition: all 0.8s;
  transition: all 0.8s;
}

header.main-header.is-smallmenu, header.main-header.is-smallmenuforced {
  background: #000;
  box-shadow: 0 3px 5px rgba(0, 0, 0, 0.3);
}

header.main-header.is-smallmenu .logo, header.main-header.is-smallmenuforced .logo {
  height: 45px;
  width: 105px;
}

header.main-header .container {
  position: relative;
  padding: 0;
}

.is-smallmenuforced ~ .article .socialshare {
  padding: 50px 0 30px;
}

.is-smallmenuforced ~ .article .section0 {
  padding-top: 0;
}

a.logo {
  float: left;
  width: 145px;
  height: 66px;
  margin: 12px 10px;
}

a.logo img {
  height: 100%;
  max-height: 70px;
}

@media (max-width: 667px) {
  a.logo {
    height: 50px;
  }
}

@media (min-width: 768px) {
  a.logo {
    height: 70px;
    width: 145px;
    margin: 10px 0;
  }
}

@media (max-width: 1150px) {
  a.logo {
    margin-left: 20px;
  }
}

.hamburger {
  position: absolute;
  top: 50%;
  right: 20px;
  -webkit-transform: translateY(-50%);
          transform: translateY(-50%);
  width: 35px;
  height: 35px;
  display: block;
  float: right;
  cursor: pointer;
  -webkit-transition: -webkit-transform 0.5s;
  transition: -webkit-transform 0.5s;
  transition: transform 0.5s;
  transition: transform 0.5s, -webkit-transform 0.5s;
}

.hamburger span {
  position: absolute;
  top: 50%;
  left: 50%;
  display: block;
  width: 33px;
  height: 2px;
  background-color: #fff;
  z-index: 2;
  -webkit-transform: translateX(-50%) translateY(-50%);
          transform: translateX(-50%) translateY(-50%);
  -webkit-transition: background 0.5s;
  transition: background 0.5s;
  transition: -webkit-transform 0.5s;
  -webkit-transition: -webkit-transform 0.5s;
  transition: transform 0.5s;
  transition: transform 0.5s, -webkit-transform 0.5s;
}

.darklogo .hamburger span {
  background-color: #fff;
}

.is-smallmenu .hamburger span {
  background-color: white;
}

.hamburger span:after, .hamburger span:before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  display: block;
  width: 33px;
  height: 2px;
  background-color: #fff;
  -webkit-transform: translateY(-8px);
          transform: translateY(-8px);
  transition: -webkit-transform 0.5s;
  -webkit-transition: -webkit-transform 0.5s;
  transition: transform 0.5s;
  transition: transform 0.5s, -webkit-transform 0.5s;
  -webkit-transform-origin: 50% 50%;
          transform-origin: 50% 50%;
}

.darklogo .hamburger span:after, .darklogo .hamburger span:before {
  background-color: #fff;
}

.is-smallmenu .hamburger span:after, .is-smallmenu .hamburger span:before {
  background-color: white;
}

.hamburger span:after {
  -webkit-transform: translateY(8px);
          transform: translateY(8px);
}

.hamburger:hover span:before {
  -webkit-transform: translateY(-11.2px);
          transform: translateY(-11.2px);
}

.hamburger:hover span:after {
  -webkit-transform: translateY(11.2px);
          transform: translateY(11.2px);
}

.hamburger.is-opened {
  -webkit-transform: rotate(180deg) translateY(50%);
          transform: rotate(180deg) translateY(50%);
}

.hamburger.is-opened span {
  background: transparent;
}

.hamburger.is-opened span:before {
  -webkit-transform: translateY(0) rotate(45deg);
          transform: translateY(0) rotate(45deg);
}

.hamburger.is-opened span:after {
  -webkit-transform: translateY(0px) translateX(1px) rotate(-45deg);
          transform: translateY(0px) translateX(1px) rotate(-45deg);
}

.nav-on .hamburger span {
  background-color: #fff;
}

.nav-on .hamburger span:after,
.nav-on .hamburger span:before {
  background-color: #fff;
}

* {
  box-sizing: border-box;
}

#main-nav {
  padding: 105px 20px 20px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: #333;
  -webkit-transition: all 0.3s cubic-bezier(0.46, 0.03, 0.52, 0.96);
  transition: all 0.3s cubic-bezier(0.46, 0.03, 0.52, 0.96);
  z-index: 10;
  overflow-y: scroll;
}

@media (max-width: 667px) {
  #main-nav {
    padding-top: 55px;
  }
}

#main-nav.show-menu {
  opacity: 1;
  -webkit-transform: none;
          transform: none;
  visibility: visible;
  overflow-y: scroll;
}

#main-nav.hide-menu {
  z-index: -1;
  visibility: hidden;
  opacity: 0;
  -webkit-transform: translateY(-10%);
          transform: translateY(-10%);
}

#main-nav nav {
  overflow: hidden;
  margin: auto;
  width: 100%;
  max-width: 928px;
  margin: auto;
  font-family: "Interstate", "Helvetica Neue", Helvetica, Roboto, Arial, sans-serif;
}

#main-nav nav .navgroup {
  margin-bottom: 20px;
}

#main-nav nav .navgroup + .navgroup {
  margin: 0 0 0 2%;
}

#main-nav nav h3 {
  margin-bottom: 20px;
}

#main-nav nav h3 a {
  color: #ffe600;
  font-weight: bold;
  font-size: 16px;
}

#main-nav nav ul {
  margin-bottom: 30px;
}

#main-nav nav ul li {
  list-style: none;
  font-size: 14px;
  line-height: 1.2;
  padding: 0 !important;
  margin: 0 0 0.5em;
}

#main-nav nav ul li a {
  color: #fff;
}

#main-nav nav ul li a:hover {
  color: #ffe600;
}

#main-nav nav .nav-mobile {
  margin-bottom: 30px;
}

#main-nav nav .nav-mobile > a {
  display: block;
  color: #FFF;
  font-weight: normal;
  padding-left: 0;
  background: rgba(255, 255, 255, 0.2);
  margin-bottom: 2px;
  padding: 10px 20px;
  font-size: 14px;
}

#main-nav nav .nav-mobile > a.current {
  color: #ffe600;
}

@media (min-width: 768px) {
  #main-nav {
    padding: 80px 20px 20px;
    overflow-y: visible;
  }
  #main-nav .navgroup {
    float: left;
    width: 23.5%;
  }
  #main-nav nav .nav-mobile {
    display: none;
  }
}

@media (min-width: 1200px) {
  #main-nav {
    padding: 110px 50px 50px;
  }
  #main-nav nav {
    max-width: 90%;
  }
}

@media (max-width: 767px) {
  #main-nav nav {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-wrap: wrap;
        flex-wrap: wrap;
  }
  #main-nav nav > .navgroup {
    width: 48%;
  }
  #main-nav nav .navgroup + .navgroup {
    margin: 0;
  }
  #main-nav nav > .navgroup:nth-child(odd) {
    margin-left: 0;
    clear: left;
  }
  #main-nav nav > .navgroup:nth-child(even) {
    margin-left: 4%;
  }
}

.eylogo a {
  padding-top: 0;
  margin: 10px 0 0;
}

.modal .modal-fade-screen {
  background-color: #444;
  background: rgba(0, 0, 0, 0.6);
}

#search-container {
  position: relative;
  margin: 0;
  text-align: center;
  z-index: 2;
}

@media (max-width: 767px) {
  #search-container {
    margin: 1em 0;
  }
}

.searchdiv {
  position: relative;
  height: 37px;
  width: 100%;
  overflow: hidden;
  background: #fff;
  border: none;
  padding: 0;
  margin: 34px 0 10px 0;
}

input.form_search_submit[type="button"] {
  position: absolute;
  right: 5px;
  top: 50%;
  -webkit-transform: translateY(-50%);
          transform: translateY(-50%);
  background: transparent url(https://www.ey.com/ecimages/searchicon.png) no-repeat scroll 0 0 !important;
  width: 20px;
  border: none;
  height: 20px;
  border: none;
  cursor: pointer;
  margin: 0;
  padding: 0;
  text-indent: -9999px !important;
  white-space: nowrap;
  overflow: hidden;
}

input#query {
  border: none;
  height: 26px;
  margin-bottom: 10px;
}

#search-field {
  width: 95%;
  -webkit-transform-origin: right;
          transform-origin: right;
  -webkit-transition: all 0.3s ease-out;
  transition: all 0.3s ease-out;
  background-color: rgba(0, 0, 0, 0.7);
  z-index: 1000;
  border-radius: 0;
  box-shadow: none;
  outline: none;
  padding: 0;
  margin: 0;
  border: 0;
  font-size: 16px;
  color: #fff;
  position: absolute;
  left: 70px;
  top: 50%;
  -webkit-transform: translateY(-50%);
          transform: translateY(-50%);
  padding: 7px 5px 7px 28px;
  margin-left: -50px;
  border: 2px solid white;
  z-index: -1;
}

@media (max-width: 767px) {
  #search-field {
    width: 97%;
  }
}

#search-field:focus {
  /*width: 18em;*/
  background-color: #222;
  color: #fff;
  opacity: 1;
}

label.search-label {
  padding-left: 1px;
  display: inline-block;
  text-shadow: 0 0 0.1em rgba(60, 60, 60, 0.3);
  position: relative;
  left: 0.1em;
}

.icon-search svg {
  width: 100%;
  height: 24px;
  max-width: 24px;
  -webkit-transform: translateY(0.1em);
          transform: translateY(0.1em);
}

/*end search*/
.cs-component {
  width: 100%;
  max-width: 420px;
  padding: 0 16px 16px;
  position: relative;
  top: 7px;
  left: 0;
  z-index: 1000;
}

@media (max-width: 767px) {
  .cs-component {
    margin-bottom: 2em;
    width: 100%;
    max-width: none;
  }
}

.cs-component h3 {
  margin: 0 0 0 -10px;
  padding: 0 0 10px;
  color: #fff;
  font-size: 16px;
}

.cs-current-country {
  border-top: 1px solid #ccc;
  display: table;
  width: calc(100% + 32px);
  position: relative;
  z-index: 10;
  background: #ccc;
  margin: 0 -16px -16px;
  padding: 16px;
  -webkit-transition: all 0.25s;
  transition: all 0.25s;
  padding: 7px;
  margin-top: -5px;
}

.cs-current-country:hover,
.cs-current-country:focus {
  cursor: pointer;
  color: #000;
  background: #ffe600;
}

.cs-country {
  display: inline-block;
}

.cs-arrow {
  position: absolute;
  right: 10px;
  -webkit-transition: all 0.05s;
  transition: all 0.05s;
  -webkit-transform-origin: center center;
          transform-origin: center center;
  -webkit-transform: rotateZ(180deg) translateY(-3px);
          transform: rotateZ(180deg) translateY(-3px);
  height: 14px;
  width: 26px;
  overflow: hidden;
}

.cs-arrow.is-open {
  -webkit-transform: rotateZ(0deg) translateY(3px) translateX(2px);
          transform: rotateZ(0deg) translateY(3px) translateX(2px);
}

.cs-arrow:hover {
  cursor: pointer;
}

.cs-arrow:before {
  border: 10px solid transparent;
  content: ' ';
  display: block;
  position: absolute;
  z-index: 2;
  border-bottom-color: #333;
  left: 2px;
  top: -8px;
  bottom: auto;
}

.cs-countries-list {
  position: absolute;
  margin-bottom: calc( -200px);
  height: 45vh;
  background: #fff;
  width: 100%;
  margin-left: -16px;
  padding: 0;
  overflow: hidden;
  overflow-y: scroll;
  visibility: hidden;
  -webkit-transition: all 0.25s;
  transition: all 0.25s;
  opacity: 0;
  -webkit-transform: translate3d(0, 0, 0);
          transform: translate3d(0, 0, 0);
}

@media (max-width: 568px) {
  .cs-countries-list {
    height: 26vh;
  }
}

.cs-countries-list.is-open {
  visibility: visible;
  opacity: 1;
  /*margin-top: calc( -200px - 32px);*/
  margin-top: 16px;
}

.cs-countries-list .cs-countries-list-inner {
  position: relative;
}

.cs-countries-list ul {
  margin: 0;
  padding: 0;
}

.cs-countries-list ul li {
  list-style-type: none;
  padding: 0;
  list-style-position: outside;
  margin: 0;
}

.cs-countries-list ul li a {
  padding: 10px;
  display: block;
  text-decoration: none;
  color: #333;
}

.cs-countries-list ul li a:hover {
  background: rgba(34, 102, 204, 0.15);
  color: inherit;
}

.footer {
  padding: 20px;
  background: #333;
  width: 100%;
}

@media (min-width: 940px) {
  .footer {
    padding: 2.8em 1.618em;
  }
}

.footer .footer-logo {
  margin-bottom: 2em;
  text-align: center;
}

@media (max-width: 736px) {
  .footer .footer-logo {
    display: none;
  }
}

.footer .footer-logo img {
  height: 5em;
}

.footer .footer-links {
  margin-bottom: 0.35em;
}

.footer .footer-links::after {
  clear: both;
  content: "";
  display: block;
}

.footer ul {
  margin-bottom: 1.4em;
  padding: 0;
}

@media (min-width: 46em) {
  .footer ul {
    float: left;
    display: block;
    margin-right: 2.3576515979%;
    width: 31.7615656014%;
  }
  .footer ul:last-child {
    margin-right: 0;
  }
  .footer ul:nth-child(3n) {
    margin-right: 0;
  }
  .footer ul:nth-child(3n+1) {
    clear: left;
  }
  .footer ul::after {
    clear: both;
    content: "";
    display: block;
  }
}

.footer li {
  line-height: 2.5em;
  list-style: none;
  text-align: center;
}

@media (min-width: 46em) {
  .footer li {
    text-align: left;
  }
}

.footer li a {
  color: rgba(255, 255, 255, 0.6);
  text-decoration: none;
}

.footer li a:focus, .footer li a:hover {
  color: white;
}

.footer li h3 {
  color: white;
  font-size: 1em;
  font-weight: 800;
  margin-bottom: 0.4em;
}

.footer hr {
  border: 1px solid rgba(255, 255, 255, 0.3);
  margin: 0 auto 1.4em;
  width: 12em;
}

.footer p {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9em;
  line-height: 1.5em;
  margin: 1em auto;
  max-width: 74em;
}

.footer-links-columns {
  max-width: 67em;
  margin-left: auto;
  margin-right: auto;
}

.footer-links-columns .footer_top ul {
  -webkit-column-count: 3;
     -moz-column-count: 3;
          column-count: 3;
  width: 100%;
}

.footer-links-columns .footer_top ul li:nth-child(3n+1) {
  border-top: 2px solid #808080;
}

.footer-links-columns .footer_top ul li:nth-child(3n+4) {
  -webkit-column-break-before: column;
     page-break-before: column;
          break-before: column;
}

.footer_bottom {
  clear: left;
}

.socialshare {
  display: none;
  z-index: 2;
}

.sharelist .linkedin,
.sharelist .facebook,
.sharelist .digg,
.sharelist .google,
.sharelist .linkedin,
.sharelist .twitter,
.sharelist .print,
.sharelist .email-alerts,
.sharelist .email,
.sharelist .apps,
.sharelist .stumbleupon,
.sharelist .webcasts,
.sharelist .youtube,
.sharelist .yammer {
  background: url("https://cdn.ey.com/echannel/gl/en/issues/business-environment/bbww_portal/images_content/newsprites.png") no-repeat;
  padding: 0;
  width: 16px;
  height: 16px;
}

.sharelist .yammer {
  background-position: 0 -177px;
}

.sharelist {
  margin: 0;
  padding: 0;
  border: 0;
  overflow: hidden;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
}

.sharelist li {
  padding-left: 0;
  white-space: nowrap;
  display: inline;
  float: left;
  padding-left: 4px;
  padding-right: 4px;
  text-indent: -119988px;
  overflow: hidden;
  text-align: left;
  width: 16px;
  height: 16px;
  margin: 0 0 0 6px;
  padding: 0;
  -webkit-box-align: center;
      -ms-flex-align: center;
          align-items: center;
  -webkit-box-pack: justify;
      -ms-flex-pack: justify;
          justify-content: space-between;
  float: none;
  -webkit-box-flex: 1;
      -ms-flex: 1;
          flex: 1;
}

.sharelist li.last {
  padding-right: 0;
}

.sharelist li.sharelabel,
li.linkedin,
li.facebook,
li.twitter {
  /* display: none; */
}

.sharelist li:first-child {
  margin-left: 0;
}

@media (min-width: 481px) and (max-width: 800px) {
  .sharelist li {
    margin-left: 2%;
  }
}

@media (max-width: 480px), (device-height: 568px) {
  .sharelist li:first-child {
    margin-left: 15px;
  }
  .sharelist li:last-child {
    margin-right: 15px;
  }
}

.sharelist a {
  display: block;
  min-height: 16px;
}

.sharelist .facebook {
  background-position: 0 -16px;
}

.sharelist .digg {
  background-position: 0 -131px;
}

.sharelist .google {
  background-position: 0 -99px;
}

.sharelist .linkedin {
  background: url("https://cdn.ey.com/echannel/gl/en/issues/business-environment/bbww_portal/images_content/newsprites.png") no-repeat;
  background-position: 0 -51px;
}

.sharelist .twitter {
  background-position: 0 0;
}

.sharelist .print {
  background-position: 0 -159px;
  height: 18px !important;
}

.sharelist .email-alerts,
.sharelist .email {
  background-position: 0 -67px;
}

.partnerinfo .partnerinfo .sharelist .email-alerts,
.partnerinfo .partnerinfo .sharelist .email {
  float: left;
}

.sharelist .apps {
  background-position: 0 -145px;
}

.sharelist .stumbleupon {
  background-position: 0 -32px;
}

.sharelist .webcasts {
  background-position: 0 -115px;
}

.sharelist .youtube {
  background-position: 0 -83px;
}

.sharelist .sharelabel {
  background: none;
  text-indent: 0;
  width: auto;
}

* + html .google {
  display: none;
}

* + html .sharelist li {
  display: inline;
}

#___plusone_0 {
  float: left !important;
  margin-left: 10px !important;
}

@media (max-device-width: 320px) and (orientation: portrait) {
  .sl-landing .socialshare {
    top: 280px !important;
  }
}

@media (max-width: 767px) {
  .socialshare {
    display: block;
    position: absolute;
    top: 20px;
    right: 30px;
    z-index: 1;
    width: 277px;
    padding: 0;
  }
  .main-header .socialshare {
    display: block;
    left: 50%;
    -webkit-transform: translateX(-50%);
            transform: translateX(-50%);
  }
  .sl-landing .socialshare {
    display: block;
    position: absolute;
    top: 305px;
    left: 50%;
    z-index: 1;
    width: 170px;
    padding: 0;
    -webkit-transform: translateX(-50%);
            transform: translateX(-50%);
  }
  .section0 {
    padding-top: 20px;
  }
  .type-system-ey .socialshare {
    display: block;
    position: absolute;
    top: 20px;
    right: auto;
    z-index: 1;
    width: 277px;
    padding: 0;
    left: 50%;
    -webkit-transform: translateX(-50%);
            transform: translateX(-50%);
  }
}

@media (max-device-width: 46em) and (orientation: landscape) {
  .sl-landing .socialshare {
    top: 105vh;
  }
}

@media (min-device-width: 414px) and (max-device-width: 736px) and (orientation: portrait) {
  .sl-landing .socialshare {
    top: 330px;
  }
}

@media (min-width: 768px) {
  .socialshare {
    display: block;
    position: absolute;
    top: auto;
    width: 200px;
    padding: 20px 0;
    left: 50%;
    -webkit-transform: translateX(-50%);
            transform: translateX(-50%);
    -webkit-transition: all 0.5s;
    transition: all 0.5s;
    opacity: 1;
    overflow: hidden;
  }
  .type-system-ey .socialshare {
    display: block;
    opacity: 1;
    z-index: 2;
    position: absolute;
  }
}

.sharelist li.sharelabel,
.sharelist li.digg,
.sharelist li.google,
.sharelist li.stumbleupon {
  display: none;
}

.navigation .sharelist {
  display: none;
}

.navigation.smallnav .sharelist {
  display: block;
}

.fxd.smallnav {
  height: 70px;
  background: black;
  padding-bottom: 0;
}

.modal-open .fxd.smallnav {
  height: 100vh;
}

.navigation.smallnav .navigation-wrapper {
  padding-bottom: 10px;
}

.navigation.smallnav .eylogo {
  height: 50px;
  width: 50px;
  padding: 0;
  margin: 0;
  background: url("https://cdn.ey.com/echannel/gl/en/about-us/global-review-2014/logo_m.png") no-repeat;
  background-size: contain;
  -webkit-transition: all 0.3s;
  transition: all 0.3s;
}

.navigation.smallnav .eylogo a {
  display: block;
  width: 50px;
  height: 50px;
}

.navigation.smallnav .eylogo:hover {
  cursor: pointer;
}

.navigation.smallnav .eylogo img {
  display: none;
}

.navigation.smallnav .ccbnav {
  display: none;
  top: 0;
  margin-right: 70px;
  -webkit-transition: all 0.3s;
  transition: all 0.3s;
}

.navigation.smallnav .ccbnav ul {
  margin-bottom: 0;
}

.navigation.smallnav .gr-maintitle {
  opacity: 1;
  top: 25px;
}

.navigation.smallnav .socialshare {
  right: 0;
  opacity: 0.7;
}

@media (max-device-width: 1024px) and (orientation: portrait) {
  .navigation.smallnav .socialshare {
    bottom: auto;
    top: 15px;
    width: 210px;
  }
  .navigation.smallnav .socialshare li + li {
    margin-right: 20px;
  }
}

.flex-parent {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
}

@media all and (max-width: 736px) {
  .flex-parent {
    -ms-flex-preferred-size: 100% !important;
        flex-basis: 100% !important;
    -ms-flex-wrap: wrap;
        flex-wrap: wrap;
  }
}

.side-column {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-flex: 1;
      -ms-flex-positive: 1;
          flex-grow: 1;
  -ms-flex-negative: 1;
      flex-shrink: 1;
  -ms-flex-preferred-size: 0;
      flex-basis: 0;
  -webkit-box-orient: vertical;
  -webkit-box-direction: normal;
      -ms-flex-direction: column;
          flex-direction: column;
}

@media all and (max-width: 736px) {
  .side-column {
    -ms-flex-preferred-size: 100% !important;
        flex-basis: 100% !important;
    -ms-flex-wrap: wrap;
        flex-wrap: wrap;
    -webkit-box-orient: horizontal;
    -webkit-box-direction: normal;
        -ms-flex-direction: row;
            flex-direction: row;
  }
}

.parent-grid {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-wrap: wrap;
      flex-wrap: wrap;
}

@media all and (max-width: 736px) {
  .parent-grid {
    -ms-flex-preferred-size: 100% !important;
        flex-basis: 100% !important;
    -ms-flex-wrap: wrap;
        flex-wrap: wrap;
  }
}

.grid-block {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-preferred-size: 25%;
      flex-basis: 25%;
}

@media all and (max-width: 736px) {
  .grid-block {
    -webkit-box-flex: 1;
        -ms-flex: 1 1 auto;
            flex: 1 1 auto;
  }
}

@media all and (max-width: 736px) {
  .grid-block {
    -ms-flex-preferred-size: 100% !important;
        flex-basis: 100% !important;
    -ms-flex-wrap: wrap;
        flex-wrap: wrap;
  }
}

.grid-block h3 {
  text-align: center;
  font-size: 1.3em;
  line-height: 1.1;
}

html.touch .grid-block h3 {
  text-align: left;
  color: #ffe600 !important;
}

.grid-block h3 br {
  display: none;
}

@media all and (max-width: 51em) {
  .grid-block h3 {
    font-size: 1em;
    line-height: 1.1;
  }
}

.item,
.item-transition {
  outline: 1px solid white;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  min-height: 7.5em;
  max-width: 100%;
  -webkit-box-pack: center;
      -ms-flex-pack: center;
          justify-content: center;
  -webkit-box-align: center;
      -ms-flex-align: center;
          align-items: center;
  max-width: 100%;
  -webkit-box-flex: 1;
      -ms-flex-positive: 1;
          flex-grow: 1;
  -ms-flex-negative: 1;
      flex-shrink: 1;
  -ms-flex-preferred-size: 0;
      flex-basis: 0;
  background-color: rgba(0, 0, 0, 0.5);
  position: relative;
  padding: 1em;
}

.item p,
.item-transition p {
  margin-bottom: 0;
}

.item *,
.item-transition * {
  color: #fff;
}

.item a:hover,
.item-transition a:hover {
  color: #ffe600;
}

@media all and (max-width: 46em) {
  .item,
  .item-transition {
    -webkit-box-pack: start;
        -ms-flex-pack: start;
            justify-content: flex-start;
  }
  .item.grid-block-image,
  .item-transition.grid-block-image {
    -webkit-box-pack: center;
        -ms-flex-pack: center;
            justify-content: center;
  }
  .center-blocks-below .item, .center-blocks-below
  .item-transition {
    -webkit-box-pack: center;
        -ms-flex-pack: center;
            justify-content: center;
  }
}

@media (min-width: 940px) {
  .item > *,
  .item-transition > * {
    max-width: 80%;
  }
}

.item-caption {
  font-weight: 700;
  font-size: 1rem;
}

@media all and (max-width: 48em) {
  .item-caption {
    font-size: 0.875rem;
  }
}

html.touch .abs-center + .item-caption {
  padding-top: 0.5em;
}

.grid-block-image {
  position: relative;
  background: none;
}

.grid-block-image p {
  font-size: 1.1rem;
}

.grid-block-image:before {
  content: '';
  background-color: rgba(0, 0, 0, 0.4);
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 0;
}

.grid-block-image > * {
  z-index: 1;
}

html.no-touch .item-transition {
  -webkit-transition: all 0.5s;
  transition: all 0.5s;
}

html.no-touch .item-transition .abs-center {
  -webkit-transform: translate(-50%, -50%);
          transform: translate(-50%, -50%);
  -webkit-transition: all 0.5s;
  transition: all 0.5s;
  position: absolute;
  top: 50%;
  left: 50%;
  margin: 0;
  transition: all 0.5s;
}

html.no-touch .item-transition .item-caption {
  opacity: 0;
  margin: 0;
  color: #333;
  -webkit-transform: translateY(20px);
          transform: translateY(20px);
  -webkit-transition: all 0.5s;
  transition: all 0.5s;
}

html.no-touch .item-transition:hover {
  background-color: #ffe600;
}

html.no-touch .item-transition:hover .item-caption {
  -webkit-transform: translateY(0);
          transform: translateY(0);
  opacity: 1;
}

html.no-touch .item-transition:hover h3 {
  color: #333;
}

html.no-touch .item-transition:hover .abs-center {
  opacity: 0;
}

html.no-touch .contact-us .item-transition:hover,
html.no-touch .contact-us .item:hover {
  background: #444;
}

html.no-touch .contact-us .item-transition:hover a h3 {
  color: #ffe600;
}

.span25 {
  -ms-flex-preferred-size: 25%;
      flex-basis: 25%;
}

.span33 {
  -ms-flex-preferred-size: 33.333%;
      flex-basis: 33.333%;
}

.span45 {
  -ms-flex-preferred-size: 45%;
      flex-basis: 45%;
}

.span50 {
  -ms-flex-preferred-size: 50%;
      flex-basis: 50%;
}

.span66 {
  -ms-flex-preferred-size: 66.666%;
      flex-basis: 66.666%;
}

.span75 {
  -ms-flex-preferred-size: 75%;
      flex-basis: 75%;
}

.span100 {
  -ms-flex-preferred-size: 100%;
      flex-basis: 100%;
}

@media (max-width: 768px) and (min-width: 569px) {
  .smartquestion h2 {
    margin-left: 0;
  }
}

.row {
  display: block;
}

.row::after {
  clear: both;
  content: "";
  display: block;
}

.col {
  float: left;
}

.large-1 {
  float: left;
  display: block;
  margin-right: 2.3576515979%;
  width: 6.1721527019%;
}

.large-1:last-child {
  margin-right: 0;
}

.large-push-1 {
  margin-left: 8.5298042998%;
}

.large-pull-1 {
  margin-left: -8.5298042998%;
}

.large-2 {
  float: left;
  display: block;
  margin-right: 2.3576515979%;
  width: 14.7019570017%;
}

.large-2:last-child {
  margin-right: 0;
}

.large-push-2 {
  margin-left: 17.0596085997%;
}

.large-pull-2 {
  margin-left: -17.0596085997%;
}

.large-3 {
  float: left;
  display: block;
  margin-right: 2.3576515979%;
  width: 23.2317613015%;
}

.large-3:last-child {
  margin-right: 0;
}

.large-push-3 {
  margin-left: 25.5894128995%;
}

.large-pull-3 {
  margin-left: -25.5894128995%;
}

.large-4 {
  float: left;
  display: block;
  margin-right: 2.3576515979%;
  width: 31.7615656014%;
}

.large-4:last-child {
  margin-right: 0;
}

.large-push-4 {
  margin-left: 34.1192171993%;
}

.large-pull-4 {
  margin-left: -34.1192171993%;
}

.large-5 {
  float: left;
  display: block;
  margin-right: 2.3576515979%;
  width: 40.2913699012%;
}

.large-5:last-child {
  margin-right: 0;
}

.large-push-5 {
  margin-left: 42.6490214991%;
}

.large-pull-5 {
  margin-left: -42.6490214991%;
}

.large-6 {
  float: left;
  display: block;
  margin-right: 2.3576515979%;
  width: 48.821174201%;
}

.large-6:last-child {
  margin-right: 0;
}

.large-push-6 {
  margin-left: 51.178825799%;
}

.large-pull-6 {
  margin-left: -51.178825799%;
}

.large-7 {
  float: left;
  display: block;
  margin-right: 2.3576515979%;
  width: 57.3509785009%;
}

.large-7:last-child {
  margin-right: 0;
}

.large-push-7 {
  margin-left: 59.7086300988%;
}

.large-pull-7 {
  margin-left: -59.7086300988%;
}

.large-8 {
  float: left;
  display: block;
  margin-right: 2.3576515979%;
  width: 65.8807828007%;
}

.large-8:last-child {
  margin-right: 0;
}

.large-push-8 {
  margin-left: 68.2384343986%;
}

.large-pull-8 {
  margin-left: -68.2384343986%;
}

.large-9 {
  float: right;
  display: block;
  margin-right: 2.3576515979%;
  width: 74.4105871005%;
}

.large-9:last-child {
  margin-right: 0;
}

.large-push-9 {
  margin-left: 76.7682386985%;
}

.large-pull-9 {
  margin-left: -76.7682386985%;
}

.large-10 {
  float: left;
  display: block;
  margin-right: 2.3576515979%;
  width: 82.9403914003%;
}

.large-10:last-child {
  margin-right: 0;
}

.large-push-10 {
  margin-left: 85.2980429983%;
}

.large-pull-10 {
  margin-left: -85.2980429983%;
}

.large-11 {
  float: left;
  display: block;
  margin-right: 2.3576515979%;
  width: 91.4701957002%;
}

.large-11:last-child {
  margin-right: 0;
}

.large-push-11 {
  margin-left: 93.8278472981%;
}

.large-pull-11 {
  margin-left: -93.8278472981%;
}

.large-12 {
  float: left;
  display: block;
  margin-right: 2.3576515979%;
  width: 100%;
}

.large-12:last-child {
  margin-right: 0;
}

.large-push-12 {
  margin-left: 102.357651598%;
}

.large-pull-12 {
  margin-left: -102.357651598%;
}

.large-1 img, .large-push-1 img, .large-pull-1 img, .large-2 img, .large-push-2 img, .large-pull-2 img, .large-3 img, .large-push-3 img, .large-pull-3 img, .large-4 img, .large-push-4 img, .large-pull-4 img, .large-5 img, .large-push-5 img, .large-pull-5 img, .large-6 img, .large-push-6 img, .large-pull-6 img, .large-7 img, .large-push-7 img, .large-pull-7 img, .large-8 img, .large-push-8 img, .large-pull-8 img, .large-9 img, .large-push-9 img, .large-pull-9 img, .large-10 img, .large-push-10 img, .large-pull-10 img, .large-11 img, .large-push-11 img, .large-pull-11 img, .large-12 img, .large-push-12 img, .large-pull-12 img {
  max-width: 100%;
}

@media (max-width: 767px) {
  .large section {
    padding-top: 30px;
    padding-bottom: 30px;
  }
  .large-1, .large-push-1, .large-pull-1, .large-2, .large-push-2, .large-pull-2, .large-3, .large-push-3, .large-pull-3, .large-4, .large-push-4, .large-pull-4, .large-5, .large-push-5, .large-pull-5, .large-6, .large-push-6, .large-pull-6, .large-7, .large-push-7, .large-pull-7, .large-8, .large-push-8, .large-pull-8, .large-9, .large-push-9, .large-pull-9, .large-10, .large-push-10, .large-pull-10, .large-11, .large-push-11, .large-pull-11, .large-12, .large-push-12, .large-pull-12 {
    float: none;
    margin: 0;
    width: 100%;
  }
}

.large [class*=pull] {
  margin: 1em 0;
}

.no-margin + div {
  background: #ffe600 !important;
  height: 100%;
}

.no-margin {
  margin-right: 0 !important;
}

.large-1.no-margin {
  padding-bottom: 6.1721527019%;
}

.large-2.no-margin {
  padding-bottom: 14.7019570017%;
}

[class*=pull] {
  margin-right: 2em;
  margin-bottom: 1em;
}

.alternate2 {
  background-color: #808080;
}

.thirds {
  max-width: 68em;
  margin-left: auto;
  margin-right: auto;
}

.thirds::after {
  clear: both;
  content: "";
  display: block;
}

.thirds::after {
  clear: both;
  content: "";
  display: block;
}

.thirds > * {
  float: left;
  display: block;
  margin-right: 2.3576515979%;
  width: 31.7615656014%;
}

.thirds > *:last-child {
  margin-right: 0;
}

.halves {
  max-width: 68em;
  margin-left: auto;
  margin-right: auto;
}

.halves::after {
  clear: both;
  content: "";
  display: block;
}

.halves::after {
  clear: both;
  content: "";
  display: block;
}

.halves > * {
  float: left;
  display: block;
  margin-right: 2.3576515979%;
  width: 48.821174201%;
}

.halves > *:last-child {
  margin-right: 0;
}

.sixty-fourty {
  max-width: 68em;
  margin-left: auto;
  margin-right: auto;
}

.sixty-fourty::after {
  clear: both;
  content: "";
  display: block;
}

.sixty-fourty::after {
  clear: both;
  content: "";
  display: block;
}

.sixty-fourty > div:nth-child(1) {
  float: left;
  display: block;
  margin-right: 2.3576515979%;
  width: 31.7615656014%;
}

.sixty-fourty > div:nth-child(1):last-child {
  margin-right: 0;
}

.sixty-fourty > div:nth-child(2) {
  float: left;
  display: block;
  margin-right: 2.3576515979%;
  width: 65.8807828007%;
}

.sixty-fourty > div:nth-child(2):last-child {
  margin-right: 0;
}

.pull-left {
  float: left;
  display: block;
  margin-right: 2.3576515979%;
  width: 14.7019570017%;
  margin-left: -17.0596085997%;
  position: relative;
}

.pull-left:last-child {
  margin-right: 0;
}

.align-middle {
  margin-left: auto !important;
  margin-right: auto !important;
  float: none;
}

.third {
  width: 33%;
}

.fll {
  float: left;
  margin-right: 1em;
}

.flr {
  float: right;
  margin-left: 1em;
}

.highlight {
  background: #fff;
  padding: 5px;
}

.card:first-child {
  padding-left: 0;
  margin-left: 0;
}

.thin-columns .row > div {
  padding: 0 30px;
}

.thin-columns .row > div:first-child {
  padding-left: 0;
}

.thin-columns .row > div:last-child {
  padding-right: 0;
}

.cs-item {
  padding-left: 30px;
  padding-right: 30px;
  display: block;
}

.cs-item .cs-img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  margin: 20px auto 40px auto;
}

.cs-item .cs-img img {
  height: auto;
  width: 100%;
  max-width: none;
}

.vertical-tabs-container {
  border-radius: 3px;
  margin-bottom: 1.4em;
  overflow: hidden;
}

.vertical-tabs-container::after {
  clear: both;
  content: "";
  display: block;
}

.vertical-tabs-container li {
  list-style: none;
}

.vertical-tabs-container a {
  color: #369;
  text-decoration: none;
}

.vertical-tabs-container .vertical-tabs {
  display: none;
  border-right: 1px solid #ccc;
}

@media screen and (min-width: 40em) {
  .vertical-tabs-container .vertical-tabs {
    background-color: #fff;
    display: inline;
    float: left;
    height: 18.75em;
    width: 20%;
  }
}

@media screen and (min-width: 40em) {
  .vertical-tabs-container .vertical-tab {
    border-right: 5px solid rgba(124, 26, 123, 0);
    display: block;
    font-weight: bold;
    margin-right: -1px;
    padding: 0.7em 0.809em;
    text-align: right;
    -webkit-transition: all .25s;
    transition: all .25s;
  }
  .vertical-tabs-container .vertical-tab:hover {
    color: #000;
    border-right-color: rgba(124, 26, 123, 0.6);
  }
  .vertical-tabs-container .vertical-tab.is-active {
    background-color: white;
    margin-right: -1px;
    border-right-color: #7c1a7b;
  }
}

.vertical-tabs-container a.vertical-tab-accordion-heading,
.vertical-tabs-container a.vertical-tab {
  color: #333;
}

.vertical-tabs-container .vertical-tab:focus {
  outline: none;
}

.vertical-tabs-container .vertical-tab-content-container {
  display: block;
  margin: 0 auto;
  -webkit-transition: all 1.5s;
  transition: all 1.5s;
}

.vertical-tabs-container .vertical-tab-content-container a:focus {
  outline: none;
}

@media screen and (min-width: 40em) {
  .vertical-tabs-container .vertical-tab-content-container {
    height: 18.75em;
    width: 80%;
    background-color: white;
    display: inline-block;
  }
}

.vertical-tabs-container .vertical-tab-content {
  background-color: white;
  padding: 1.4em 1.618em;
}

.vertical-tabs-container .vertical-tab-content p {
  color: #333;
  line-height: 1.4;
}

@media screen and (min-width: 40em) {
  .vertical-tabs-container .vertical-tab-content {
    border: 0;
    display: none;
  }
}

.vertical-tabs-container .vertical-tab-accordion-heading {
  background-color: #fff;
  border-top: 1px solid #ccc;
  cursor: pointer;
  display: block;
  font-weight: bold;
  padding: 0.7em 0.809em;
}

.vertical-tabs-container .vertical-tab-accordion-heading:focus, .vertical-tabs-container .vertical-tab-accordion-heading:hover {
  color: #369;
}

.vertical-tabs-container .vertical-tab-accordion-heading:first-child {
  border-top: 0;
}

.vertical-tabs-container .vertical-tab-accordion-heading.is-active {
  background: white;
  border-bottom: 0;
}

@media screen and (min-width: 40em) {
  .vertical-tabs-container .vertical-tab-accordion-heading {
    display: none;
  }
}

.fixed-tabs {
  position: fixed;
}

.fixed-tabs + .vertical-tab-content-container {
  margin-left: 20%;
}

li,
p {
  -webkit-font-feature-settings: "onum" 1, "pnum" 1;
          font-feature-settings: "onum" 1, "pnum" 1;
}

ul.default-ul {
  position: relative;
}

ul.default-ul ul {
  margin-left: 1em;
}

ul.default-ul ul ul li:before {
  height: 0.2rem;
  -webkit-transform: translateY(0.3em) translateX(-1em);
          transform: translateY(0.3em) translateX(-1em);
}

ul.default-ul ul li:before {
  width: 0.4em;
  height: 0.4em;
}

ul.default-ul li {
  padding-left: 1em;
  margin: 0;
  list-style-type: none;
  margin-bottom: 0.5em;
}

ul.default-ul li::before {
  content: '';
  width: 0.5em;
  height: 0.5em;
  display: inline-block;
  background: #bbbbbb;
  position: absolute;
  -webkit-transform: translateY(0.4em) translateX(-1em);
          transform: translateY(0.4em) translateX(-1em);
}

ul.default-ul.lighttext li::before {
  background: #ccc;
}

p.initcap:first-letter {
  font-size: 115px;
  float: left;
  color: #7D0F7C;
  line-height: 1;
  font-weight: bold;
  margin: -8px 3px -10px -10px;
}

[lang$="kr"] p.initcap:first-letter {
  font-size: 105px;
  margin-top: -15px;
}

.servicecallout {
  font-family: "EYInterstate", "EY", sans-serif;
  font-size: 24px;
  color: #646464;
  letter-spacing: -0.05em;
  position: relative;
  margin-top: 1em;
  z-index: 1;
}

@media (max-width: 375px) {
  .servicecallout {
    font-size: 16px;
  }
}

h2 + .servicecallout,
p + .servicecallout {
  margin-top: 2em;
}

.servicecallout:before {
  content: "";
  position: absolute;
  left: -1em;
  top: -1em;
  height: 5px;
  width: 35%;
  background-color: #7D0F7C;
}

.darken-cta {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-align: center;
      -ms-flex-align: center;
          align-items: center;
  background: rgba(0, 0, 50, 0.12);
  margin: 0 -40px -20px;
  padding: 20px 0;
}

.darken-cta > div:first-child {
  padding: 20px;
}

.darken-cta img {
  max-width: 100%;
}

.darken-cta p {
  text-align: right;
}

.btn, .bold-bttn,
.bttn-large {
  padding: .5em 1em;
  text-decoration: none;
  background-color: #fff;
  color: #369;
  font-size: 125%;
  letter-spacing: -.03em;
  line-height: 1;
  display: inline-block;
  margin: auto;
  max-width: 18em;
  font-weight: 700;
  text-align: center;
  -webkit-transition: all 0.25s;
  transition: all 0.25s;
  border: 2px solid #369;
}

.btn:hover, .bold-bttn:hover,
.bttn-large:hover {
  color: #333;
  background-color: #ffe600;
}

.bold-bttn,
.bttn-large {
  position: relative;
  margin: 0 auto 1em;
  border-color: #369;
  padding: 20px 40px 20px 110px;
}

.bold-bttn:before, .bold-bttn:after,
.bttn-large:before,
.bttn-large:after {
  position: absolute;
  content: "";
  top: 0;
  left: 0;
  bottom: 0;
  background-color: #808080;
  display: block;
  z-index: 0;
  width: 4.37rem;
  -webkit-transition: all .25s;
  transition: all .25s;
}

.bold-bttn:after,
.bttn-large:after {
  background: url("https://cdn.ey.com/ey-templates/scroll-template/img/arrow.svg") 15px 50% no-repeat transparent;
  -webkit-transition: all .15s ease-in;
  transition: all .15s ease-in;
}

.bold-bttn:hover,
.bttn-large:hover {
  color: #333;
  background-color: rgba(255, 230, 0, 0.83);
}

.bold-bttn:hover:before,
.bttn-large:hover:before {
  background: gray;
}

.cbp-qtrotator + .bold-bttn, .cbp-qtrotator +
.bttn-large {
  margin-top: 2em;
  margin-bottom: -2em;
}

.sl-landing > section,
article > section,
body > section {
  position: relative;
  -webkit-transition: all 0.4s;
  transition: all 0.4s;
}

.sl-landing > section.lighttext .container > *,
article > section.lighttext .container > *,
body > section.lighttext .container > * {
  color: #fff !important;
}

.sl-landing > section.lighttext a,
article > section.lighttext a,
body > section.lighttext a {
  color: #ffe600 !important;
}

.sl-landing > section.lighttext a.bold-bttn,
article > section.lighttext a.bold-bttn,
body > section.lighttext a.bold-bttn {
  color: #369 !important;
}

@media (min-width: 768px) {
  .sl-landing > section,
  article > section,
  body > section {
    padding: 40px 20px;
  }
}

@media (max-width: 962px) and (orientation: landscape) {
  .sl-landing > section,
  article > section,
  body > section {
    padding: 40px 20px;
  }
}

@media (min-width: 940px) {
  .sl-landing > section,
  article > section,
  body > section {
    padding: 40px;
  }
}

@media (min-width: 1200px) {
  .sl-landing > section,
  article > section,
  body > section {
    padding-left: 0;
    padding-right: 0;
  }
}

@media (min-width: 1200px) {
  .sl-landing > section,
  article > section,
  body > section {
    padding-left: 0;
    padding-right: 0;
  }
}

.article > section.section0 {
  padding-top: 60px;
}

.videowrap {
  padding-bottom: 56.25%;
  position: relative;
  width: 100%;
  height: 0;
}

.videowrap > * {
  width: 100%;
  height: 100% !important;
  position: absolute;
  left: 0;
  top: 0;
}

.sl-landing > section.ads {
  padding: 0;
}

.container {
  max-width: 68em;
  margin-left: auto;
  margin-right: auto;
}

.container::after {
  clear: both;
  content: "";
  display: block;
}

@media (max-width: 768px) {
  .sl-landing .container {
    max-width: 100%;
  }
}

@media (min-width: 940px) {
  .container::after {
    clear: both;
    content: "";
    display: block;
  }
  .sl-landing .container {
    max-width: 68em;
  }
}

@media (max-width: 767px) {
  .container {
    max-width: 100%;
    padding: 6vw;
  }
  #main-nav .container {
    padding: 0;
  }
}

.container .section-contact {
  max-width: 100%;
}

@media (min-width: 768px) {
  .maincolumn {
    padding: 0;
    float: left;
    display: block;
    margin-right: 2.3576515979%;
    width: 74.4105871005%;
    margin-right: 0;
  }
  .maincolumn:last-child {
    margin-right: 0;
  }
  .maincolumn.layout-3cols {
    float: left;
    display: block;
    margin-right: 2.3576515979%;
    width: 48.821174201%;
  }
  .maincolumn.layout-3cols:last-child {
    margin-right: 0;
  }
}

@media (min-width: 768px) {
  .mainaside {
    float: left;
    display: block;
    margin-right: 2.3576515979%;
    width: 23.2317613015%;
    margin-right: 0;
    font-size: 0.875em;
  }
  .mainaside:last-child {
    margin-right: 0;
  }
}

.relatedcontent-items {
  max-width: 68em;
  margin-left: auto;
  margin-right: auto;
}

.relatedcontent-items::after {
  clear: both;
  content: "";
  display: block;
}

.article-subnav a {
  padding: 0 20px;
}

@media (min-width: 768px) {
  .article-subnav {
    float: left;
    display: block;
    margin-right: 2.3576515979%;
    width: 23.2317613015%;
  }
  .article-subnav:last-child {
    margin-right: 0;
  }
}

figure.rounded {
  border-radius: 50%;
  overflow: hidden;
  width: 120px;
  height: 120px;
  margin-left: auto;
  margin-right: auto;
  position: relative;
  left: 50%;
  -webkit-transform: translateX(-50%) translateY(35px);
  transform: translateX(-50%) translateY(35px);
  margin: 0;
}

figure img {
  width: 100%;
  height: auto;
}

.lead {
  font-size: 120%;
  padding-left: 0;
  padding-right: 0;
}

@media (max-width: 375px) {
  .lead {
    font-size: 110%;
  }
}

.section-header {
  border-bottom: 3px solid #CCC;
  height: 32px;
  text-align: center;
  position: relative;
  width: 100%;
  z-index: 2;
  margin: 75px auto;
}

.section-header > *:first-child {
  font-size: 42px;
  font-weight: 100;
  background: #FFF;
  color: #555;
  display: inline-block;
  margin: 0;
  padding: 0 0.5em;
  position: relative;
  width: auto;
}

div.ui-widget {
  font-size: 1rem;
}

.ui-widget-content a {
  color: #369 !important;
}

.ui-widget-content .ui-state-default,
.ui-widget-header .ui-state-default,
div.ui-state-default {
  background: none rgba(255, 255, 255, 0.7);
  color: #369;
  -webkit-transition: all 0.3s;
  transition: all 0.3s;
}

.ui-widget-content .ui-state-default:hover,
.ui-widget-header .ui-state-default:hover,
div.ui-state-default:hover {
  background-color: #fffacc;
  color: #036;
  border-color: #ffe600;
}

.ui-widget-content .ui-state-default:focus,
.ui-widget-header .ui-state-default:focus,
div.ui-state-default:focus {
  outline: none;
}

.ui-corner-all,
.ui-corner-bottom,
.ui-corner-br,
.ui-corner-right {
  border-radius: 0;
}

.ui-accordion .ui-state-active {
  border-bottom: none;
  background: #FFFACC;
}

.ui-accordion .ui-widget-content {
  background: #FFF none;
}

div.ui-accordion .ui-accordion-content {
  background: #FFFACC;
  overflow: hidden !important;
}

div.ui-accordion .ui-accordion-header .ui-accordion-header-icon {
  top: 28px;
}

div.ui-accordion .ui-accordion-content {
  padding-top: 0;
}

.ui-state-hover {
  background-image: none !important;
  background-color: #fffacc;
}

.boxed {
  border: 1px solid #808080;
  padding: 20px;
  margin-top: 2.36%;
  background-color: #FFF;
}

.mt {
  margin-top: 40px;
}

.bannertext {
  margin-top: 0;
  padding: 10px;
  margin-bottom: 20px;
  background: #646464;
  color: #fff;
  text-align: center;
  font-size: 1em;
}

.feaugraphic .bannertext {
  margin-bottom: 0;
}

.boxed .bannertext {
  margin: -20px -20px 20px;
}

.bannertext strong {
  font-size: 1.3em;
  color: #ffe600;
}

.flexwide {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
}

@media (max-width: 767px) {
  .feaugraphic .fll {
    float: none;
  }
  .feaugraphic .large-6 {
    width: 100%;
    margin: 0 0 20px;
  }
  .feaugraphic .flexwide {
    display: block;
  }
}

.article > section[class*=section]:nth-child(even) {
  background-color: #fff;
}

.article > section[class*=section]:nth-child(odd) {
  background-color: #f0f0f0;
}

.sl-landing > section.yellow {
  background-color: #ffe600;
}

.sl-landing > section.gray0 {
  background-color: #f0f0f0;
}

.sl-landing > section.gray1 {
  background-color: #ccc;
}

.sl-landing > section.gray2 {
  background-color: #808080;
}

.sl-landing > section.gray2 h2,
.sl-landing > section.gray2 p {
  color: #FFF;
}

.sl-landing > section.gray3 {
  background-color: #646464;
}

.sl-landing > section.gray3 h2,
.sl-landing > section.gray3 p {
  color: #FFF;
}

.sl-landing > section.gray4 {
  background-color: #333;
}

.sl-landing > section.gray4 h2,
.sl-landing > section.gray4 p {
  color: #FFF;
}

.sl-landing > section div.grid-items .grid-item:hover p.descr {
  color: #fff;
}

@media (min-width: 768px) {
  .sl-landing > section div.grid-items .grid-item:hover p.descr {
    color: #333;
  }
}

.adv-zones td {
  padding: 0.7em;
}

@media (max-width: 768px) {
  .adv-zones {
    font-size: 13px;
  }
}

.only-mobile {
  display: none;
}

.zones-mobile li {
  margin-bottom: 1em;
  font-size: 0.9em;
}

.zones-mobile strong {
  display: block;
  font-size: 1.1em;
}

@media (min-width: 320px) and (max-width: 667px) {
  .only-mobile {
    display: block;
  }
  .adv-zones {
    display: none;
  }
}

@media screen and (device-width: 360px) and (device-height: 640px) and (-webkit-device-pixel-ratio: 3) {
  .only-mobile {
    display: block;
  }
  .adv-zones {
    display: none;
  }
}

.margin-top-small {
  margin-top: 1em;
}

.margin-top-medium {
  margin-top: 3em;
}

.margin-top-large {
  margin-top: 4em;
}

.padding-bottom-small {
  padding-bottom: 8px;
}

.padding-bottom-medium {
  padding-bottom: 16px;
}

.padding-bottom-large {
  padding-bottom: 32px;
}

#featuremenu .nav-current a {
  color: #000;
}

.box-grid {
  background: #fff;
  max-width: 68em;
  margin-left: auto;
  margin-right: auto;
  padding-top: 120px;
  padding-bottom: 120px;
}

.box-grid::after {
  clear: both;
  content: "";
  display: block;
}

.box-grid .box-grid_item {
  float: left;
  height: 360px;
  width: 25%;
}

.box-grid .box-grid_item.double-width {
  width: 50%;
}

.box-grid .box-grid_item.double-height {
  height: 720px;
}

.box-grid .box-grid_item a {
  color: #333;
}

.box-grid .box-grid_panel {
  overflow: hidden;
  padding: 2px;
  position: relative;
}

.box-grid .mask {
  height: 130px;
}

.box-grid article {
  padding: 10px;
}

.box-grid article h3 {
  margin: 0;
}

.box-grid article p {
  font-size: 12px;
}

.grey1 {
  background: #cccccc;
}

div.gallery-cell .bio-email,
div.gallery-cell .bio-telephone {
  display: none;
}

div.biographyModalContents p {
  margin-bottom: 0;
}

@media screen and (min-width: 40em) {
  .modal .modal-inner .modal-content.biographyModalContents,
  .modal .modal-inner .modal-content.generic-modal-content {
    -webkit-columns: auto;
    -moz-columns: auto;
    columns: auto;
  }
}

.generic-modal-link {
  cursor: pointer;
}

@media (min-width: 40em) {
  .section6 .grid-item,
  .alliances .grid-item {
    min-height: 24em;
  }
}

@media (max-width: 767px) {
  .section6 .grid-item,
  .alliances .grid-item {
    -webkit-box-flex: 1;
        -ms-flex: 1;
            flex: 1;
  }
  .section6 .grid-item .descr,
  .alliances .grid-item .descr {
    opacity: 1;
  }
  .section6 .grid-item .center li,
  .alliances .grid-item .center li {
    color: #f0f0f0;
    text-align: left;
    margin-left: 10px;
  }
  .section6 .grid-item h4,
  .alliances .grid-item h4 {
    text-align: center;
  }
  .section6 .grid-item .flexbox .section6 .grid-items,
  .section6 .grid-item .flexboxlegacy .section6 .grid-items,
  .alliances .grid-item .flexbox .section6 .grid-items,
  .alliances .grid-item .flexboxlegacy .section6 .grid-items {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
  }
}

@media (max-width: 767px) and (max-width: 767px) {
  .flexbox .section6 .grid-item:nth-child(3) .center,
  .flexboxlegacy .section6 .grid-item:nth-child(3) .center, .flexbox
  .alliances .grid-item:nth-child(3) .center,
  .flexboxlegacy
  .alliances .grid-item:nth-child(3) .center {
    top: 0;
    -webkit-transform: none;
            transform: none;
    left: 0;
    position: static;
    width: 100%;
    margin-left: auto;
    margin-right: auto;
  }
}

@media (max-width: 767px) {
  .section6 .grid-item h3.center2,
  .alliances .grid-item h3.center2 {
    -webkit-transform: none;
            transform: none;
    position: static;
    text-align: center;
    font-size: 1em;
    padding-top: 15px;
    -webkit-transform: translate(-50%, -50%);
            transform: translate(-50%, -50%);
    left: 50%;
    top: 50%;
    position: absolute;
    margin: 0;
    padding: 0;
  }
}

.section6 .grid-item:hover {
  background-color: rgba(0, 0, 0, 0.5);
  cursor: default;
}

@media (max-width: 767px) {
  #section6 .center ul li {
    display: inline-block;
    font-size: 13px;
    text-align: center;
  }
}

#section6 .alliances-list .grid-item li {
  padding: 5px 10px;
  margin: 0.5em 0;
  width: auto;
  line-height: 1;
}

.alliances-list h4 {
  text-align: center;
  margin-left: 5px;
  margin-top: 15px;
}

.alliances-list a:hover {
  color: #ffe600 !important;
}

.grid-item ul {
  font-size: 16px;
  padding: 0 20px;
}

@media only print {
  * {
    max-width: 100% !important;
    color: #333 !important;
    -webkit-transform: none;
            transform: none;
  }
  .article > section.section0 {
    padding-top: 0;
  }
  .servicecallout,
  .lead {
    font-size: 18px;
  }
  p, li {
    font-size: 10pt;
  }
  ul.default-ul li {
    padding-left: 0;
    list-style: square;
  }
  ul.default-ul li::before {
    display: none;
  }
  .article-subnav,
  .tab-link:after,
  .hamburger,
  .flickity-prev-next-button,
  .flickity-page-dots,
  .section-latest-thinking,
  section[data-section-title="Latest thinking"],
  .type-system-ey .socialshare,
  .socialshare {
    display: none !important;
  }
  .grid-items .grid-item-image:before {
    background: transparent !important;
    display: none;
  }
  .container {
    margin-left: auto !important;
    margin-right: auto !important;
    padding: 0 36px;
  }
  .center,
  .center2 {
    -webkit-transform: none !important;
            transform: none !important;
  }
  .grid-items .grid-item {
    height: auto !important;
  }
  p.center.descr {
    display: block;
    opacity: 1;
    color: #000 !important;
    visibility: visible;
    margin-bottom: 2em;
    color: #333;
    font-weight: normal;
  }
  .grid-items .grid-item h3 {
    text-align: left;
    margin-top: 0.5em;
  }
  h1 {
    font-size: 24px !important;
  }
  h2,
  h3,
  h4,
  li,
  p {
    margin-bottom: 1em !important;
  }
  .bold-bttn,
  .bttn,
  .cbp-qtrotator,
  .footer-links,
  .menucontainer,
  .ui-accordion-header-icon {
    display: none;
  }
  .footer {
    max-width: 96% !important;
    margin-left: auto !important;
    margin-right: auto !important;
    font-size: 9px !important;
  }
  .footer p {
    font-size: 9pt !important;
  }
  .tab-content,
  .ui-accordion-content {
    display: block !important;
    overflow: hidden;
  }
  .ui-state-default,
  .ui-widget-content {
    border: none !important;
  }
  .boxed {
    padding: 30px !important;
  }
  .grid-block-image:before {
    background: none transparent;
  }
  html.no-touch .item-transition .item-caption {
    text-align: left;
    display: block;
    opacity: 1;
    margin: 1em;
    position: static;
    -webkit-transform: none;
            transform: none;
    padding: 1em;
  }
  .frame3x2 svg {
    display: none;
  }
  .eyhero,
  .flickity-viewport,
  .hero {
    min-height: 0;
    height: auto !important;
  }
  .eyhero-home:before,
  .eyhero:before {
    display: none;
  }
  .darken-cta img {
    max-width: 100% !important;
    width: 120px !important;
    margin-left: 30px;
  }
  [class^="section"] {
    background: none transparent !important;
    padding: 0;
  }
  [class*="large-pull-"],
  [class*="large-push-"] {
    margin-left: 0;
  }
  .accordion-tabs-minimal,
  .accordion-tabs-minimal a.tab-link,
  .accordion-tabs-minimal a.tab-link.is-active {
    background: transparent !important;
    font-size: 1.5em;
  }
  .ui-accordion .ui-widget-content {
    border: none !important;
    background: none transparent !important;
  }
  .accordion-tabs-minimal .tab-content,
  .accordion-tabs-minimal a.tab-link {
    padding: 0;
  }
  .accordion-tabs-minimal a.tab-link {
    border: none;
  }
  header.main-header {
    position: static !important;
  }
  .flickity-slider {
    position: static !important;
    width: 100%;
    -webkit-transform: none !important;
            transform: none !important;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-flow: wrap row;
        flex-flow: wrap row;
  }
  .section-contact .gallery-cell,
  .gallery-cell {
    min-height: 0 !important;
    position: static !important;
    margin-bottom: 20px;
    width: 25% !important;
  }
  .section-contact .gallery-cell p,
  .gallery-cell p {
    font-size: 13px !important;
  }
  .section-contact .gallery-cell h3,
  .gallery-cell h3 {
    font-size: 16px !important;
  }
  .section-contact .gallery-cell img,
  .gallery-cell img {
    display: none;
  }
  .section-contact .gallery-cell:first-child .caption,
  .section-contact .gallery-cell:first-child .thumbnail,
  .gallery-cell:first-child .caption,
  .gallery-cell:first-child .thumbnail {
    margin-left: 0;
  }
  div.gallery-cell .bio-email, div.gallery-cell .bio-telephone {
    display: block !important;
  }
  .no-print {
    display: none !important;
  }
}

/*noframe css*/
.headline-container.noframe {
  position: absolute;
  -webkit-transform: translateY(-40%);
          transform: translateY(-40%);
  height: auto;
  width: auto;
  top: 50%;
  padding: 30px;
}

@media (min-width: 768px) {
  .headline-container.noframe {
    padding: 0px 110px;
  }
}

.headline-container.noframe svg {
  display: none;
}

.headline-container.noframe .smartquestion {
  padding-bottom: 0;
}

.headline-container.noframe .heading-block {
  -webkit-transform: none;
          transform: none;
  position: static;
  width: auto;
  margin: auto;
  max-width: 58em;
}

/* Single property */
.noframe .fluid-type h1.eyhero-headline-1 {
  font-size: 20px;
  line-height: 1.1;
}

@media screen and (min-width: 320px) {
  .noframe .fluid-type h1.eyhero-headline-1 {
    font-size: calc(20px + 22 * (100vw - 320px) / 880);
  }
}

@media screen and (min-width: 1200px) {
  .noframe .fluid-type h1.eyhero-headline-1 {
    font-size: 42px;
  }
}

.noframe .fluid-type h2.eyhero-subheading-1 {
  font-size: 13px;
}

@media screen and (min-width: 320px) {
  .noframe .fluid-type h2.eyhero-subheading-1 {
    font-size: calc(13px + 11 * (100vw - 320px) / 880);
  }
}

@media screen and (min-width: 1200px) {
  .noframe .fluid-type h2.eyhero-subheading-1 {
    font-size: 24px;
  }
}
/*# sourceMappingURL=style.css.map */</style>''')
        #f.write('''<link rel="stylesheet" href="http://cti-pub-files.oss-cn-shanghai.aliyuncs.com/css/advisory-jquery-ui.min.css">''')
        
        f.write('''<style type="text/css">
div.gallery-cell .bio-email, div.gallery-cell .bio-telephone {display: none;}
div.biographyModalContents p {margin-bottom: 0;}
@media screen and (min-width: 40em) { .modal .modal-inner .modal-content {-webkit-columns: auto; -moz-columns: auto; columns: auto;}}
/*! jQuery UI - v1.11.4 - 2015-03-11
* http://jqueryui.com
* Includes: core.css, accordion.css, autocomplete.css, button.css, datepicker.css, dialog.css, draggable.css, menu.css, progressbar.css, resizable.css, selectable.css, selectmenu.css, slider.css, sortable.css, spinner.css, tabs.css, tooltip.css, theme.css
* To view and modify this theme, visit http://jqueryui.com/themeroller/?ffDefault=Trebuchet%20MS%2CTahoma%2CVerdana%2CArial%2Csans-serif&fwDefault=bold&fsDefault=1.1em&cornerRadius=4px&bgColorHeader=f6a828&bgTextureHeader=gloss_wave&bgImgOpacityHeader=35&borderColorHeader=e78f08&fcHeader=ffffff&iconColorHeader=ffffff&bgColorContent=eeeeee&bgTextureContent=highlight_soft&bgImgOpacityContent=100&borderColorContent=dddddd&fcContent=333333&iconColorContent=222222&bgColorDefault=f6f6f6&bgTextureDefault=glass&bgImgOpacityDefault=100&borderColorDefault=cccccc&fcDefault=1c94c4&iconColorDefault=ef8c08&bgColorHover=fdf5ce&bgTextureHover=glass&bgImgOpacityHover=100&borderColorHover=fbcb09&fcHover=c77405&iconColorHover=ef8c08&bgColorActive=ffffff&bgTextureActive=glass&bgImgOpacityActive=65&borderColorActive=fbd850&fcActive=eb8f00&iconColorActive=ef8c08&bgColorHighlight=ffe45c&bgTextureHighlight=highlight_soft&bgImgOpacityHighlight=75&borderColorHighlight=fed22f&fcHighlight=363636&iconColorHighlight=228ef1&bgColorError=b81900&bgTextureError=diagonals_thick&bgImgOpacityError=18&borderColorError=cd0a0a&fcError=ffffff&iconColorError=ffd27a&bgColorOverlay=666666&bgTextureOverlay=diagonals_thick&bgImgOpacityOverlay=20&opacityOverlay=50&bgColorShadow=000000&bgTextureShadow=flat&bgImgOpacityShadow=10&opacityShadow=20&thicknessShadow=5px&offsetTopShadow=-5px&offsetLeftShadow=-5px&cornerRadiusShadow=5px
* Copyright 2015 jQuery Foundation and other contributors; Licensed MIT */
.ui-helper-hidden {display: none } .ui-helper-hidden-accessible {border: 0; clip: rect(0 0 0 0); height: 1px; margin: -1px; overflow: hidden; padding: 0; position: absolute; width: 1px } .ui-helper-reset {margin: 0; padding: 0; border: 0; outline: 0; line-height: 1.3; text-decoration: none; font-size: 100%; list-style: none } .ui-helper-clearfix:before, .ui-helper-clearfix:after {content: ""; display: table; border-collapse: collapse } .ui-helper-clearfix:after {clear: both } .ui-helper-clearfix {min-height: 0 } .ui-helper-zfix {width: 100%; height: 100%; top: 0; left: 0; position: absolute; opacity: 0; filter: Alpha(Opacity=0) } .ui-front {z-index: 100 } .ui-state-disabled {cursor: default!important } .ui-icon {display: block; text-indent: -99999px; overflow: hidden; background-repeat: no-repeat } .ui-widget-overlay {position: fixed; top: 0; left: 0; width: 100%; height: 100% } .ui-accordion .ui-accordion-header {display: block; cursor: pointer; position: relative; margin: 2px 0 0 0; padding: .5em .5em .5em .7em; min-height: 0; font-size: 100% } .ui-accordion .ui-accordion-icons {padding-left: 2.2em } .ui-accordion .ui-accordion-icons .ui-accordion-icons {padding-left: 2.2em } .ui-accordion .ui-accordion-header .ui-accordion-header-icon {position: absolute; left: .5em; top: 50%; margin-top: -8px } .ui-accordion .ui-accordion-content {padding: 1em 2.2em; border-top: 0; overflow: auto !important; } .ui-autocomplete {position: absolute; top: 0; left: 0; cursor: default } .ui-button {display: inline-block; position: relative; padding: 0; line-height: normal; margin-right: .1em; cursor: pointer; vertical-align: middle; text-align: center; overflow: visible } .ui-button, .ui-button:link, .ui-button:visited, .ui-button:hover, .ui-button:active {text-decoration: none } .ui-button-icon-only {width: 2.2em } button.ui-button-icon-only {width: 2.4em } .ui-button-icons-only {width: 3.4em } button.ui-button-icons-only {width: 3.7em } .ui-button .ui-button-text {display: block; line-height: normal } .ui-button-text-only .ui-button-text {padding: .4em 1em } .ui-button-icon-only .ui-button-text, .ui-button-icons-only .ui-button-text {padding: .4em; text-indent: -9999999px } .ui-button-text-icon-primary .ui-button-text, .ui-button-text-icons .ui-button-text {padding: .4em 1em .4em 2.1em } .ui-button-text-icon-secondary .ui-button-text, .ui-button-text-icons .ui-button-text {padding: .4em 2.1em .4em 1em } .ui-button-text-icons .ui-button-text {padding-left: 2.1em; padding-right: 2.1em } input.ui-button {padding: .4em 1em } .ui-button-icon-only .ui-icon, .ui-button-text-icon-primary .ui-icon, .ui-button-text-icon-secondary .ui-icon, .ui-button-text-icons .ui-icon, .ui-button-icons-only .ui-icon {position: absolute; top: 50%; margin-top: -8px } .ui-button-icon-only .ui-icon {left: 50%; margin-left: -8px } .ui-button-text-icon-primary .ui-button-icon-primary, .ui-button-text-icons .ui-button-icon-primary, .ui-button-icons-only .ui-button-icon-primary {left: .5em } .ui-button-text-icon-secondary .ui-button-icon-secondary, .ui-button-text-icons .ui-button-icon-secondary, .ui-button-icons-only .ui-button-icon-secondary {right: .5em } .ui-buttonset {margin-right: 7px } .ui-buttonset .ui-button {margin-left: 0; margin-right: -.3em } input.ui-button::-moz-focus-inner, button.ui-button::-moz-focus-inner {border: 0; padding: 0 } .ui-datepicker {width: 17em; padding: .2em .2em 0; display: none } .ui-datepicker .ui-datepicker-header {position: relative; padding: .2em 0 } .ui-datepicker .ui-datepicker-prev, .ui-datepicker .ui-datepicker-next {position: absolute; top: 2px; width: 1.8em; height: 1.8em } .ui-datepicker .ui-datepicker-prev-hover, .ui-datepicker .ui-datepicker-next-hover {top: 1px } .ui-datepicker .ui-datepicker-prev {left: 2px } .ui-datepicker .ui-datepicker-next {right: 2px } .ui-datepicker .ui-datepicker-prev-hover {left: 1px } .ui-datepicker .ui-datepicker-next-hover {right: 1px } .ui-datepicker .ui-datepicker-prev span, .ui-datepicker .ui-datepicker-next span {display: block; position: absolute; left: 50%; margin-left: -8px; top: 50%; margin-top: -8px } .ui-datepicker .ui-datepicker-title {margin: 0 2.3em; line-height: 1.8em; text-align: center } .ui-datepicker .ui-datepicker-title select {font-size: 1em; margin: 1px 0 } .ui-datepicker select.ui-datepicker-month, .ui-datepicker select.ui-datepicker-year {width: 45% } .ui-datepicker table {width: 100%; font-size: .9em; border-collapse: collapse; margin: 0 0 .4em } .ui-datepicker th {padding: .7em .3em; text-align: center; font-weight: bold; border: 0 } .ui-datepicker td {border: 0; padding: 1px } .ui-datepicker td span, .ui-datepicker td a {display: block; padding: .2em; text-align: right; text-decoration: none } .ui-datepicker .ui-datepicker-buttonpane {background-image: none; margin: .7em 0 0 0; padding: 0 .2em; border-left: 0; border-right: 0; border-bottom: 0 } .ui-datepicker .ui-datepicker-buttonpane button {float: right; margin: .5em .2em .4em; cursor: pointer; padding: .2em .6em .3em .6em; width: auto; overflow: visible } .ui-datepicker .ui-datepicker-buttonpane button.ui-datepicker-current {float: left } .ui-datepicker.ui-datepicker-multi {width: auto } .ui-datepicker-multi .ui-datepicker-group {float: left } .ui-datepicker-multi .ui-datepicker-group table {width: 95%; margin: 0 auto .4em } .ui-datepicker-multi-2 .ui-datepicker-group {width: 50% } .ui-datepicker-multi-3 .ui-datepicker-group {width: 33.3% } .ui-datepicker-multi-4 .ui-datepicker-group {width: 25% } .ui-datepicker-multi .ui-datepicker-group-last .ui-datepicker-header, .ui-datepicker-multi .ui-datepicker-group-middle .ui-datepicker-header {border-left-width: 0 } .ui-datepicker-multi .ui-datepicker-buttonpane {clear: left } .ui-datepicker-row-break {clear: both; width: 100%; font-size: 0 } .ui-datepicker-rtl {direction: rtl } .ui-datepicker-rtl .ui-datepicker-prev {right: 2px; left: auto } .ui-datepicker-rtl .ui-datepicker-next {left: 2px; right: auto } .ui-datepicker-rtl .ui-datepicker-prev:hover {right: 1px; left: auto } .ui-datepicker-rtl .ui-datepicker-next:hover {left: 1px; right: auto } .ui-datepicker-rtl .ui-datepicker-buttonpane {clear: right } .ui-datepicker-rtl .ui-datepicker-buttonpane button {float: left } .ui-datepicker-rtl .ui-datepicker-buttonpane button.ui-datepicker-current, .ui-datepicker-rtl .ui-datepicker-group {float: right } .ui-datepicker-rtl .ui-datepicker-group-last .ui-datepicker-header, .ui-datepicker-rtl .ui-datepicker-group-middle .ui-datepicker-header {border-right-width: 0; border-left-width: 1px } .ui-dialog {overflow: hidden; position: absolute; top: 0; left: 0; padding: .2em; outline: 0 } .ui-dialog .ui-dialog-titlebar {padding: .4em 1em; position: relative } .ui-dialog .ui-dialog-title {float: left; margin: .1em 0; white-space: nowrap; width: 90%; overflow: hidden; text-overflow: ellipsis } .ui-dialog .ui-dialog-titlebar-close {position: absolute; right: .3em; top: 50%; width: 20px; margin: -10px 0 0 0; padding: 1px; height: 20px } .ui-dialog .ui-dialog-content {position: relative; border: 0; padding: .5em 1em; background: none; overflow: auto } .ui-dialog .ui-dialog-buttonpane {text-align: left; border-width: 1px 0 0 0; background-image: none; margin-top: .5em; padding: .3em 1em .5em .4em } .ui-dialog .ui-dialog-buttonpane .ui-dialog-buttonset {float: right } .ui-dialog .ui-dialog-buttonpane button {margin: .5em .4em .5em 0; cursor: pointer } .ui-dialog .ui-resizable-se {width: 12px; height: 12px; right: -5px; bottom: -5px; background-position: 16px 16px } .ui-draggable .ui-dialog-titlebar {cursor: move } .ui-draggable-handle {-ms-touch-action: none; touch-action: none } .ui-menu {list-style: none; padding: 0; margin: 0; display: block; outline: none } .ui-menu .ui-menu {position: absolute } .ui-menu .ui-menu-item {position: relative; margin: 0; padding: 3px 1em 3px .4em; cursor: pointer; min-height: 0; list-style-image: url("data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7") } .ui-menu .ui-menu-divider {margin: 5px 0; height: 0; font-size: 0; line-height: 0; border-width: 1px 0 0 0 } .ui-menu .ui-state-focus, .ui-menu .ui-state-active {margin: -1px } .ui-menu-icons {position: relative } .ui-menu-icons .ui-menu-item {padding-left: 2em } .ui-menu .ui-icon {position: absolute; top: 0; bottom: 0; left: .2em; margin: auto 0 } .ui-menu .ui-menu-icon {left: auto; right: 0 } .ui-progressbar {height: 2em; text-align: left; overflow: hidden } .ui-progressbar .ui-progressbar-value {margin: -1px; height: 100% } .ui-progressbar .ui-progressbar-overlay {background: url("data:image/gif;base64,R0lGODlhKAAoAIABAAAAAP///yH/C05FVFNDQVBFMi4wAwEAAAAh+QQJAQABACwAAAAAKAAoAAACkYwNqXrdC52DS06a7MFZI+4FHBCKoDeWKXqymPqGqxvJrXZbMx7Ttc+w9XgU2FB3lOyQRWET2IFGiU9m1frDVpxZZc6bfHwv4c1YXP6k1Vdy292Fb6UkuvFtXpvWSzA+HycXJHUXiGYIiMg2R6W459gnWGfHNdjIqDWVqemH2ekpObkpOlppWUqZiqr6edqqWQAAIfkECQEAAQAsAAAAACgAKAAAApSMgZnGfaqcg1E2uuzDmmHUBR8Qil95hiPKqWn3aqtLsS18y7G1SzNeowWBENtQd+T1JktP05nzPTdJZlR6vUxNWWjV+vUWhWNkWFwxl9VpZRedYcflIOLafaa28XdsH/ynlcc1uPVDZxQIR0K25+cICCmoqCe5mGhZOfeYSUh5yJcJyrkZWWpaR8doJ2o4NYq62lAAACH5BAkBAAEALAAAAAAoACgAAAKVDI4Yy22ZnINRNqosw0Bv7i1gyHUkFj7oSaWlu3ovC8GxNso5fluz3qLVhBVeT/Lz7ZTHyxL5dDalQWPVOsQWtRnuwXaFTj9jVVh8pma9JjZ4zYSj5ZOyma7uuolffh+IR5aW97cHuBUXKGKXlKjn+DiHWMcYJah4N0lYCMlJOXipGRr5qdgoSTrqWSq6WFl2ypoaUAAAIfkECQEAAQAsAAAAACgAKAAAApaEb6HLgd/iO7FNWtcFWe+ufODGjRfoiJ2akShbueb0wtI50zm02pbvwfWEMWBQ1zKGlLIhskiEPm9R6vRXxV4ZzWT2yHOGpWMyorblKlNp8HmHEb/lCXjcW7bmtXP8Xt229OVWR1fod2eWqNfHuMjXCPkIGNileOiImVmCOEmoSfn3yXlJWmoHGhqp6ilYuWYpmTqKUgAAIfkECQEAAQAsAAAAACgAKAAAApiEH6kb58biQ3FNWtMFWW3eNVcojuFGfqnZqSebuS06w5V80/X02pKe8zFwP6EFWOT1lDFk8rGERh1TTNOocQ61Hm4Xm2VexUHpzjymViHrFbiELsefVrn6XKfnt2Q9G/+Xdie499XHd2g4h7ioOGhXGJboGAnXSBnoBwKYyfioubZJ2Hn0RuRZaflZOil56Zp6iioKSXpUAAAh+QQJAQABACwAAAAAKAAoAAACkoQRqRvnxuI7kU1a1UU5bd5tnSeOZXhmn5lWK3qNTWvRdQxP8qvaC+/yaYQzXO7BMvaUEmJRd3TsiMAgswmNYrSgZdYrTX6tSHGZO73ezuAw2uxuQ+BbeZfMxsexY35+/Qe4J1inV0g4x3WHuMhIl2jXOKT2Q+VU5fgoSUI52VfZyfkJGkha6jmY+aaYdirq+lQAACH5BAkBAAEALAAAAAAoACgAAAKWBIKpYe0L3YNKToqswUlvznigd4wiR4KhZrKt9Upqip61i9E3vMvxRdHlbEFiEXfk9YARYxOZZD6VQ2pUunBmtRXo1Lf8hMVVcNl8JafV38aM2/Fu5V16Bn63r6xt97j09+MXSFi4BniGFae3hzbH9+hYBzkpuUh5aZmHuanZOZgIuvbGiNeomCnaxxap2upaCZsq+1kAACH5BAkBAAEALAAAAAAoACgAAAKXjI8By5zf4kOxTVrXNVlv1X0d8IGZGKLnNpYtm8Lr9cqVeuOSvfOW79D9aDHizNhDJidFZhNydEahOaDH6nomtJjp1tutKoNWkvA6JqfRVLHU/QUfau9l2x7G54d1fl995xcIGAdXqMfBNadoYrhH+Mg2KBlpVpbluCiXmMnZ2Sh4GBqJ+ckIOqqJ6LmKSllZmsoq6wpQAAAh+QQJAQABACwAAAAAKAAoAAAClYx/oLvoxuJDkU1a1YUZbJ59nSd2ZXhWqbRa2/gF8Gu2DY3iqs7yrq+xBYEkYvFSM8aSSObE+ZgRl1BHFZNr7pRCavZ5BW2142hY3AN/zWtsmf12p9XxxFl2lpLn1rseztfXZjdIWIf2s5dItwjYKBgo9yg5pHgzJXTEeGlZuenpyPmpGQoKOWkYmSpaSnqKileI2FAAACH5BAkBAAEALAAAAAAoACgAAAKVjB+gu+jG4kORTVrVhRlsnn2dJ3ZleFaptFrb+CXmO9OozeL5VfP99HvAWhpiUdcwkpBH3825AwYdU8xTqlLGhtCosArKMpvfa1mMRae9VvWZfeB2XfPkeLmm18lUcBj+p5dnN8jXZ3YIGEhYuOUn45aoCDkp16hl5IjYJvjWKcnoGQpqyPlpOhr3aElaqrq56Bq7VAAAOw=="); height: 100%; filter: alpha(opacity=25); opacity: 0.25 } .ui-progressbar-indeterminate .ui-progressbar-value {background-image: none } .ui-resizable {position: relative } .ui-resizable-handle {position: absolute; font-size: 0.1px; display: block; -ms-touch-action: none; touch-action: none } .ui-resizable-disabled .ui-resizable-handle, .ui-resizable-autohide .ui-resizable-handle {display: none } .ui-resizable-n {cursor: n-resize; height: 7px; width: 100%; top: -5px; left: 0 } .ui-resizable-s {cursor: s-resize; height: 7px; width: 100%; bottom: -5px; left: 0 } .ui-resizable-e {cursor: e-resize; width: 7px; right: -5px; top: 0; height: 100% } .ui-resizable-w {cursor: w-resize; width: 7px; left: -5px; top: 0; height: 100% } .ui-resizable-se {cursor: se-resize; width: 12px; height: 12px; right: 1px; bottom: 1px } .ui-resizable-sw {cursor: sw-resize; width: 9px; height: 9px; left: -5px; bottom: -5px } .ui-resizable-nw {cursor: nw-resize; width: 9px; height: 9px; left: -5px; top: -5px } .ui-resizable-ne {cursor: ne-resize; width: 9px; height: 9px; right: -5px; top: -5px } .ui-selectable {-ms-touch-action: none; touch-action: none } .ui-selectable-helper {position: absolute; z-index: 100; border: 1px dotted black } .ui-selectmenu-menu {padding: 0; margin: 0; position: absolute; top: 0; left: 0; display: none } .ui-selectmenu-menu .ui-menu {overflow: auto; overflow-x: hidden; padding-bottom: 1px } .ui-selectmenu-menu .ui-menu .ui-selectmenu-optgroup {font-size: 1em; font-weight: bold; line-height: 1.5; padding: 2px 0.4em; margin: 0.5em 0 0 0; height: auto; border: 0 } .ui-selectmenu-open {display: block } .ui-selectmenu-button {display: inline-block; overflow: hidden; position: relative; text-decoration: none; cursor: pointer } .ui-selectmenu-button span.ui-icon {right: 0.5em; left: auto; margin-top: -8px; position: absolute; top: 50% } .ui-selectmenu-button span.ui-selectmenu-text {text-align: left; padding: 0.4em 2.1em 0.4em 1em; display: block; line-height: 1.4; overflow: hidden; text-overflow: ellipsis; white-space: nowrap } .ui-slider {position: relative; text-align: left } .ui-slider .ui-slider-handle {position: absolute; z-index: 2; width: 1.2em; height: 1.2em; cursor: default; -ms-touch-action: none; touch-action: none } .ui-slider .ui-slider-range {position: absolute; z-index: 1; font-size: .7em; display: block; border: 0; background-position: 0 0 } .ui-slider.ui-state-disabled .ui-slider-handle, .ui-slider.ui-state-disabled .ui-slider-range {filter: inherit } .ui-slider-horizontal {height: .8em } .ui-slider-horizontal .ui-slider-handle {top: -.3em; margin-left: -.6em } .ui-slider-horizontal .ui-slider-range {top: 0; height: 100% } .ui-slider-horizontal .ui-slider-range-min {left: 0 } .ui-slider-horizontal .ui-slider-range-max {right: 0 } .ui-slider-vertical {width: .8em; height: 100px } .ui-slider-vertical .ui-slider-handle {left: -.3em; margin-left: 0; margin-bottom: -.6em } .ui-slider-vertical .ui-slider-range {left: 0; width: 100% } .ui-slider-vertical .ui-slider-range-min {bottom: 0 } .ui-slider-vertical .ui-slider-range-max {top: 0 } .ui-sortable-handle {-ms-touch-action: none; touch-action: none } .ui-spinner {position: relative; display: inline-block; overflow: hidden; padding: 0; vertical-align: middle } .ui-spinner-input {border: none; background: none; color: inherit; padding: 0; margin: .2em 0; vertical-align: middle; margin-left: .4em; margin-right: 22px } .ui-spinner-button {width: 16px; height: 50%; font-size: .5em; padding: 0; margin: 0; text-align: center; position: absolute; cursor: default; display: block; overflow: hidden; right: 0 } .ui-spinner a.ui-spinner-button {border-top: none; border-bottom: none; border-right: none } .ui-spinner .ui-icon {position: absolute; margin-top: -8px; top: 50%; left: 0 } .ui-spinner-up {top: 0 } .ui-spinner-down {bottom: 0 } .ui-spinner .ui-icon-triangle-1-s {background-position: -65px -16px } .ui-tabs {position: relative; padding: .2em } .ui-tabs .ui-tabs-nav {margin: 0; padding: .2em .2em 0 } .ui-tabs .ui-tabs-nav li {list-style: none; float: left; position: relative; top: 0; margin: 1px .2em 0 0; border-bottom-width: 0; padding: 0; white-space: nowrap } .ui-tabs .ui-tabs-nav .ui-tabs-anchor {float: left; padding: .5em 1em; text-decoration: none } .ui-tabs .ui-tabs-nav li.ui-tabs-active {margin-bottom: -1px; padding-bottom: 1px } .ui-tabs .ui-tabs-nav li.ui-tabs-active .ui-tabs-anchor, .ui-tabs .ui-tabs-nav li.ui-state-disabled .ui-tabs-anchor, .ui-tabs .ui-tabs-nav li.ui-tabs-loading .ui-tabs-anchor {cursor: text } .ui-tabs-collapsible .ui-tabs-nav li.ui-tabs-active .ui-tabs-anchor {cursor: pointer } .ui-tabs .ui-tabs-panel {display: block; border-width: 0; padding: 1em 1.4em; background: none } .ui-tooltip {padding: 8px; position: absolute; z-index: 9999; max-width: 300px; -webkit-box-shadow: 0 0 5px #aaa; box-shadow: 0 0 5px #aaa } body .ui-tooltip {border-width: 2px } .ui-widget {font-family: Trebuchet MS, Tahoma, Verdana, Arial, sans-serif; font-size: 1.1em } .ui-widget .ui-widget {font-size: 1em } .ui-widget input, .ui-widget select, .ui-widget textarea, .ui-widget button {font-family: Trebuchet MS, Tahoma, Verdana, Arial, sans-serif; font-size: 1em } .ui-widget-content {border: 1px solid #ddd; background: #eee url("https://cdn.ey.com/echannel/gl/en/services/advisory/eytemplate/css/images/ui-bg_highlight-soft_100_eeeeee_1x100.png") 50% top repeat-x; color: #333 } .ui-widget-content a {color: #333 } .ui-widget-header {border: 1px solid #e78f08; background: #f6a828 url("https://cdn.ey.com/echannel/gl/en/services/advisory/eytemplate/css/images/ui-bg_gloss-wave_35_f6a828_500x100.png") 50% 50% repeat-x; color: #fff; font-weight: bold } .ui-widget-header a {color: #fff } .ui-state-default, .ui-widget-content .ui-state-default, .ui-widget-header .ui-state-default {border: 1px solid #ccc; background: #f6f6f6 url("https://cdn.ey.com/echannel/gl/en/services/advisory/eytemplate/css/images/ui-bg_glass_100_f6f6f6_1x400.png") 50% 50% repeat-x; font-weight: bold; color: #1c94c4 } .ui-state-default a, .ui-state-default a:link, .ui-state-default a:visited {color: #1c94c4; text-decoration: none } .ui-state-hover, .ui-widget-content .ui-state-hover, .ui-widget-header .ui-state-hover, .ui-state-focus, .ui-widget-content .ui-state-focus, .ui-widget-header .ui-state-focus {border: 1px solid #fbcb09; background: #fdf5ce url("https://cdn.ey.com/echannel/gl/en/services/advisory/eytemplate/css/images/ui-bg_glass_100_fdf5ce_1x400.png") 50% 50% repeat-x; font-weight: bold; color: #c77405 } .ui-state-hover a, .ui-state-hover a:hover, .ui-state-hover a:link, .ui-state-hover a:visited, .ui-state-focus a, .ui-state-focus a:hover, .ui-state-focus a:link, .ui-state-focus a:visited {color: #c77405; text-decoration: none } .ui-state-active, .ui-widget-content .ui-state-active, .ui-widget-header .ui-state-active {border: 1px solid #fbd850; background: #fff url("https://cdn.ey.com/echannel/gl/en/services/advisory/eytemplate/css/images/ui-bg_glass_65_ffffff_1x400.png") 50% 50% repeat-x; font-weight: bold; color: #eb8f00 } .ui-state-active a, .ui-state-active a:link, .ui-state-active a:visited {color: #eb8f00; text-decoration: none } .ui-state-highlight, .ui-widget-content .ui-state-highlight, .ui-widget-header .ui-state-highlight {border: 1px solid #fed22f; background: #ffe45c url("https://cdn.ey.com/echannel/gl/en/services/advisory/eytemplate/css/images/ui-bg_highlight-soft_75_ffe45c_1x100.png") 50% top repeat-x; color: #363636 } .ui-state-highlight a, .ui-widget-content .ui-state-highlight a, .ui-widget-header .ui-state-highlight a {color: #363636 } .ui-state-error, .ui-widget-content .ui-state-error, .ui-widget-header .ui-state-error {border: 1px solid #cd0a0a; background: #b81900 url("https://cdn.ey.com/echannel/gl/en/services/advisory/eytemplate/css/images/ui-bg_diagonals-thick_18_b81900_40x40.png") 50% 50% repeat; color: #fff } .ui-state-error a, .ui-widget-content .ui-state-error a, .ui-widget-header .ui-state-error a {color: #fff } .ui-state-error-text, .ui-widget-content .ui-state-error-text, .ui-widget-header .ui-state-error-text {color: #fff } .ui-priority-primary, .ui-widget-content .ui-priority-primary, .ui-widget-header .ui-priority-primary {font-weight: bold } .ui-priority-secondary, .ui-widget-content .ui-priority-secondary, .ui-widget-header .ui-priority-secondary {opacity: .7; filter: Alpha(Opacity=70); font-weight: normal } .ui-state-disabled, .ui-widget-content .ui-state-disabled, .ui-widget-header .ui-state-disabled {opacity: .35; filter: Alpha(Opacity=35); background-image: none } .ui-state-disabled .ui-icon {filter: Alpha(Opacity=35) } .ui-icon {width: 16px; height: 16px } .ui-icon, .ui-widget-content .ui-icon {background-image: url("https://cdn.ey.com/echannel/gl/en/services/advisory/eytemplate/css/images/ui-icons_222222_256x240.png") } .ui-widget-header .ui-icon {background-image: url("https://cdn.ey.com/echannel/gl/en/services/advisory/eytemplate/css/images/ui-icons_ffffff_256x240.png") } .ui-state-default .ui-icon {background-image: url("https://cdn.ey.com/echannel/gl/en/services/advisory/eytemplate/css/images/ui-icons_ef8c08_256x240.png") } .ui-state-hover .ui-icon, .ui-state-focus .ui-icon {background-image: url("https://cdn.ey.com/echannel/gl/en/services/advisory/eytemplate/css/images/ui-icons_ef8c08_256x240.png") } .ui-state-active .ui-icon {background-image: url("https://cdn.ey.com/echannel/gl/en/services/advisory/eytemplate/css/images/ui-icons_ef8c08_256x240.png") } .ui-state-highlight .ui-icon {background-image: url("https://cdn.ey.com/echannel/gl/en/services/advisory/eytemplate/css/images/ui-icons_228ef1_256x240.png") } .ui-state-error .ui-icon, .ui-state-error-text .ui-icon {background-image: url("https://cdn.ey.com/echannel/gl/en/services/advisory/eytemplate/css/images/ui-icons_ffd27a_256x240.png") } .ui-icon-blank {background-position: 16px 16px } .ui-icon-carat-1-n {background-position: 0 0 } .ui-icon-carat-1-ne {background-position: -16px 0 } .ui-icon-carat-1-e {background-position: -32px 0 } .ui-icon-carat-1-se {background-position: -48px 0 } .ui-icon-carat-1-s {background-position: -64px 0 } .ui-icon-carat-1-sw {background-position: -80px 0 } .ui-icon-carat-1-w {background-position: -96px 0 } .ui-icon-carat-1-nw {background-position: -112px 0 } .ui-icon-carat-2-n-s {background-position: -128px 0 } .ui-icon-carat-2-e-w {background-position: -144px 0 } .ui-icon-triangle-1-n {background-position: 0 -16px } .ui-icon-triangle-1-ne {background-position: -16px -16px } .ui-icon-triangle-1-e {background-position: -32px -16px } .ui-icon-triangle-1-se {background-position: -48px -16px } .ui-icon-triangle-1-s {background-position: -64px -16px } .ui-icon-triangle-1-sw {background-position: -80px -16px } .ui-icon-triangle-1-w {background-position: -96px -16px } .ui-icon-triangle-1-nw {background-position: -112px -16px } .ui-icon-triangle-2-n-s {background-position: -128px -16px } .ui-icon-triangle-2-e-w {background-position: -144px -16px } .ui-icon-arrow-1-n {background-position: 0 -32px } .ui-icon-arrow-1-ne {background-position: -16px -32px } .ui-icon-arrow-1-e {background-position: -32px -32px } .ui-icon-arrow-1-se {background-position: -48px -32px } .ui-icon-arrow-1-s {background-position: -64px -32px } .ui-icon-arrow-1-sw {background-position: -80px -32px } .ui-icon-arrow-1-w {background-position: -96px -32px } .ui-icon-arrow-1-nw {background-position: -112px -32px } .ui-icon-arrow-2-n-s {background-position: -128px -32px } .ui-icon-arrow-2-ne-sw {background-position: -144px -32px } .ui-icon-arrow-2-e-w {background-position: -160px -32px } .ui-icon-arrow-2-se-nw {background-position: -176px -32px } .ui-icon-arrowstop-1-n {background-position: -192px -32px } .ui-icon-arrowstop-1-e {background-position: -208px -32px } .ui-icon-arrowstop-1-s {background-position: -224px -32px } .ui-icon-arrowstop-1-w {background-position: -240px -32px } .ui-icon-arrowthick-1-n {background-position: 0 -48px } .ui-icon-arrowthick-1-ne {background-position: -16px -48px } .ui-icon-arrowthick-1-e {background-position: -32px -48px } .ui-icon-arrowthick-1-se {background-position: -48px -48px } .ui-icon-arrowthick-1-s {background-position: -64px -48px } .ui-icon-arrowthick-1-sw {background-position: -80px -48px } .ui-icon-arrowthick-1-w {background-position: -96px -48px } .ui-icon-arrowthick-1-nw {background-position: -112px -48px } .ui-icon-arrowthick-2-n-s {background-position: -128px -48px } .ui-icon-arrowthick-2-ne-sw {background-position: -144px -48px } .ui-icon-arrowthick-2-e-w {background-position: -160px -48px } .ui-icon-arrowthick-2-se-nw {background-position: -176px -48px } .ui-icon-arrowthickstop-1-n {background-position: -192px -48px } .ui-icon-arrowthickstop-1-e {background-position: -208px -48px } .ui-icon-arrowthickstop-1-s {background-position: -224px -48px } .ui-icon-arrowthickstop-1-w {background-position: -240px -48px } .ui-icon-arrowreturnthick-1-w {background-position: 0 -64px } .ui-icon-arrowreturnthick-1-n {background-position: -16px -64px } .ui-icon-arrowreturnthick-1-e {background-position: -32px -64px } .ui-icon-arrowreturnthick-1-s {background-position: -48px -64px } .ui-icon-arrowreturn-1-w {background-position: -64px -64px } .ui-icon-arrowreturn-1-n {background-position: -80px -64px } .ui-icon-arrowreturn-1-e {background-position: -96px -64px } .ui-icon-arrowreturn-1-s {background-position: -112px -64px } .ui-icon-arrowrefresh-1-w {background-position: -128px -64px } .ui-icon-arrowrefresh-1-n {background-position: -144px -64px } .ui-icon-arrowrefresh-1-e {background-position: -160px -64px } .ui-icon-arrowrefresh-1-s {background-position: -176px -64px } .ui-icon-arrow-4 {background-position: 0 -80px } .ui-icon-arrow-4-diag {background-position: -16px -80px } .ui-icon-extlink {background-position: -32px -80px } .ui-icon-newwin {background-position: -48px -80px } .ui-icon-refresh {background-position: -64px -80px } .ui-icon-shuffle {background-position: -80px -80px } .ui-icon-transfer-e-w {background-position: -96px -80px } .ui-icon-transferthick-e-w {background-position: -112px -80px } .ui-icon-folder-collapsed {background-position: 0 -96px } .ui-icon-folder-open {background-position: -16px -96px } .ui-icon-document {background-position: -32px -96px } .ui-icon-document-b {background-position: -48px -96px } .ui-icon-note {background-position: -64px -96px } .ui-icon-mail-closed {background-position: -80px -96px } .ui-icon-mail-open {background-position: -96px -96px } .ui-icon-suitcase {background-position: -112px -96px } .ui-icon-comment {background-position: -128px -96px } .ui-icon-person {background-position: -144px -96px } .ui-icon-print {background-position: -160px -96px } .ui-icon-trash {background-position: -176px -96px } .ui-icon-locked {background-position: -192px -96px } .ui-icon-unlocked {background-position: -208px -96px } .ui-icon-bookmark {background-position: -224px -96px } .ui-icon-tag {background-position: -240px -96px } .ui-icon-home {background-position: 0 -112px } .ui-icon-flag {background-position: -16px -112px } .ui-icon-calendar {background-position: -32px -112px } .ui-icon-cart {background-position: -48px -112px } .ui-icon-pencil {background-position: -64px -112px } .ui-icon-clock {background-position: -80px -112px } .ui-icon-disk {background-position: -96px -112px } .ui-icon-calculator {background-position: -112px -112px } .ui-icon-zoomin {background-position: -128px -112px } .ui-icon-zoomout {background-position: -144px -112px } .ui-icon-search {background-position: -160px -112px } .ui-icon-wrench {background-position: -176px -112px } .ui-icon-gear {background-position: -192px -112px } .ui-icon-heart {background-position: -208px -112px } .ui-icon-star {background-position: -224px -112px } .ui-icon-link {background-position: -240px -112px } .ui-icon-cancel {background-position: 0 -128px } .ui-icon-plus {background-position: -16px -128px } .ui-icon-plusthick {background-position: -32px -128px } .ui-icon-minus {background-position: -48px -128px } .ui-icon-minusthick {background-position: -64px -128px } .ui-icon-close {background-position: -80px -128px } .ui-icon-closethick {background-position: -96px -128px } .ui-icon-key {background-position: -112px -128px } .ui-icon-lightbulb {background-position: -128px -128px } .ui-icon-scissors {background-position: -144px -128px } .ui-icon-clipboard {background-position: -160px -128px } .ui-icon-copy {background-position: -176px -128px } .ui-icon-contact {background-position: -192px -128px } .ui-icon-image {background-position: -208px -128px } .ui-icon-video {background-position: -224px -128px } .ui-icon-script {background-position: -240px -128px } .ui-icon-alert {background-position: 0 -144px } .ui-icon-info {background-position: -16px -144px } .ui-icon-notice {background-position: -32px -144px } .ui-icon-help {background-position: -48px -144px } .ui-icon-check {background-position: -64px -144px } .ui-icon-bullet {background-position: -80px -144px } .ui-icon-radio-on {background-position: -96px -144px } .ui-icon-radio-off {background-position: -112px -144px } .ui-icon-pin-w {background-position: -128px -144px } .ui-icon-pin-s {background-position: -144px -144px } .ui-icon-play {background-position: 0 -160px } .ui-icon-pause {background-position: -16px -160px } .ui-icon-seek-next {background-position: -32px -160px } .ui-icon-seek-prev {background-position: -48px -160px } .ui-icon-seek-end {background-position: -64px -160px } .ui-icon-seek-start {background-position: -80px -160px } .ui-icon-seek-first {background-position: -80px -160px } .ui-icon-stop {background-position: -96px -160px } .ui-icon-eject {background-position: -112px -160px } .ui-icon-volume-off {background-position: -128px -160px } .ui-icon-volume-on {background-position: -144px -160px } .ui-icon-power {background-position: 0 -176px } .ui-icon-signal-diag {background-position: -16px -176px } .ui-icon-signal {background-position: -32px -176px } .ui-icon-battery-0 {background-position: -48px -176px } .ui-icon-battery-1 {background-position: -64px -176px } .ui-icon-battery-2 {background-position: -80px -176px } .ui-icon-battery-3 {background-position: -96px -176px } .ui-icon-circle-plus {background-position: 0 -192px } .ui-icon-circle-minus {background-position: -16px -192px } .ui-icon-circle-close {background-position: -32px -192px } .ui-icon-circle-triangle-e {background-position: -48px -192px } .ui-icon-circle-triangle-s {background-position: -64px -192px } .ui-icon-circle-triangle-w {background-position: -80px -192px } .ui-icon-circle-triangle-n {background-position: -96px -192px } .ui-icon-circle-arrow-e {background-position: -112px -192px } .ui-icon-circle-arrow-s {background-position: -128px -192px } .ui-icon-circle-arrow-w {background-position: -144px -192px } .ui-icon-circle-arrow-n {background-position: -160px -192px } .ui-icon-circle-zoomin {background-position: -176px -192px } .ui-icon-circle-zoomout {background-position: -192px -192px } .ui-icon-circle-check {background-position: -208px -192px } .ui-icon-circlesmall-plus {background-position: 0 -208px } .ui-icon-circlesmall-minus {background-position: -16px -208px } .ui-icon-circlesmall-close {background-position: -32px -208px } .ui-icon-squaresmall-plus {background-position: -48px -208px } .ui-icon-squaresmall-minus {background-position: -64px -208px } .ui-icon-squaresmall-close {background-position: -80px -208px } .ui-icon-grip-dotted-vertical {background-position: 0 -224px } .ui-icon-grip-dotted-horizontal {background-position: -16px -224px } .ui-icon-grip-solid-vertical {background-position: -32px -224px } .ui-icon-grip-solid-horizontal {background-position: -48px -224px } .ui-icon-gripsmall-diagonal-se {background-position: -64px -224px } .ui-icon-grip-diagonal-se {background-position: -80px -224px } .ui-corner-all, .ui-corner-top, .ui-corner-left, .ui-corner-tl {border-top-left-radius: 4px } .ui-corner-all, .ui-corner-top, .ui-corner-right, .ui-corner-tr {border-top-right-radius: 4px } .ui-corner-all, .ui-corner-bottom, .ui-corner-left, .ui-corner-bl {border-bottom-left-radius: 4px } .ui-corner-all, .ui-corner-bottom, .ui-corner-right, .ui-corner-br {border-bottom-right-radius: 4px } .ui-widget-overlay {background: #666 url("https://cdn.ey.com/echannel/gl/en/services/advisory/eytemplate/css/images/ui-bg_diagonals-thick_20_666666_40x40.png") 50% 50% repeat; opacity: .5; filter: Alpha(Opacity=50) } .ui-widget-shadow {margin: -5px 0 0 -5px; padding: 5px; background: #000 url("https://cdn.ey.com/echannel/gl/en/services/advisory/eytemplate/css/images/ui-bg_flat_10_000000_40x100.png") 50% 50% repeat-x; opacity: .2; filter: Alpha(Opacity=20); border-radius: 5px } .ui-state-default, .ui-widget-content .ui-state-default, .ui-widget-header .ui-state-default {color: #369;}
</style>''')
        #f.write('''<link rel="stylesheet" href="http://cti-pub-files.oss-cn-shanghai.aliyuncs.com/css/cookienotification.min.css">''')
        f.write('''<style type="text/css">
.cookienotification{position:fixed;bottom:0;border:1px solid #ccc;box-shadow:0 -2px 20px rgba(0,0,0,.3);background:#888;background:-webkit-linear-gradient(top,#888 0,#666 100%);background:-moz-linear-gradient(top,#888 0,#666 100%);background:-o-linear-gradient(top,#888 0,#666 100%);background:linear-gradient(top,#888 0,#666 100%);padding:1em 3em}.cookienote{color:#fff;font:14px/1.8 sans-serif;padding:15px;position:relative;width:100%;margin:0 auto 2em;box-sizing:border-box;-moz-box-sizing:border-box}.cookienote a{font-weight:700;color:#ffe600}#cookiecont{font-size:14px;float:right;margin:0;border:1px solid #999292;padding:2px 10px;border-radius:5px;background:#484744;box-shadow:0 2px 2px rgba(0,0,0,.2)}#cookiecont:hover{border:1px solid #b7afaf;background:#30302e;text-decoration:none;color:#fff}@media only print{.cookienotification{display:none}}

</style>''')

        f.write('''<style>.contact-us-cnt h3{border-left: 5px solid #ffe400;padding: 5px;background: #f7f7f7;font-size: 1.8em;margin-top: 10px;}.modal .modal-inner {max-width: 1000px;}.modal-content img {max-width: 1100px !important;margin: 30px auto;display: block;</style><script async="" src="https://www.google-analytics.com/analytics.js"></script><script async="" src="https://www.google-analytics.com/analytics.js"></script><script async="" src="https://www.google-analytics.com/analytics.js"></script><script>$(document).ready(function() {scrollTemplate.init();});</script><script>(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');ga('create', 'UA-45212726-1', 'auto');ga('send', 'pageview');</script><script type="text/javascript" src="./ey_cti_cn_rpt_files/analytics.min.js.download"></script><script type="text/javascript">Analytics.AddAccount("UA-45212726-1");Analytics.TrackPDFs()</script>''')
        f.write('''</head>''')
        f.write('''<body style="overflow: visible;"><!--   -->	''')
        f.write('''	<div class="topNavContainer line" role="navigation" aria-label="utility navigation" style="display:none">''')
        f.write('''		<ul class="utilitymenu" id="topnav"><li id="nav-utilityonlinesignin"><a href="javascript:window.open('http://clientportal.ey.com/');void(0)" class="topnavdropdown">安永线上登入</a></li><li id="nav-library"><a href="https://www.ey.com/CN/zh/home/library" class="topnavdropdown">图书室</a></li><li id="nav-aboutus"><a href="https://www.ey.com/CN/zh/about-us" class="topnavdropdown">关于我们</a><ul class="level2topicheader" id="aboutDrop"><li class="two"><a href="https://www.ey.com/cn/zh/about-us/our-values" onclick="generic_WT('/cn/zh/about-us/our-values','/cn/zh/about-us/our-values', '%E5%AE%89%E6%B0%B8%E7%9A%84%E4%BB%B7%E5%80%BC%E8%A7%82', '_self', 'Overlay Link');return false;">安永的价值观</a></li><li class="two"><a href="https://www.ey.com/cn/zh/about-us/our-global-approach" onclick="generic_WT('/cn/zh/about-us/our-global-approach','/cn/zh/about-us/our-global-approach', '%E6%88%91%E4%BB%AC%E7%9A%84%E5%85%A8%E7%90%83%E5%B7%A5%E4%BD%9C%E6%96%B9%E6%B3%95', '_self', 'Overlay Link');return false;">我们的全球工作方法</a><ul class="subUlFirst"><li><a href="https://www.ey.com/cn/zh/about-us/our-global-approach/our-leaders" onclick="generic_WT('/cn/zh/about-us/our-global-approach/our-leaders','/cn/zh/about-us/our-global-approach/our-leaders', '%E5%AE%89%E6%B0%B8%E7%9A%84%E9%A2%86%E5%AF%BC%E5%B1%82', '_self', 'Overlay Link');return false;">安永的领导层</a></li><li><a href="https://www.ey.com/cn/zh/about-us/our-global-approach/global-review" onclick="generic_WT('/cn/zh/about-us/our-global-approach/global-review','/cn/zh/about-us/our-global-approach/global-review', '%E3%80%8A%E5%85%A8%E7%90%83%E5%9B%9E%E9%A1%BE%E3%80%8B', '_self', 'Overlay Link');return false;">《全球回顾》</a></li></ul></li><li class="two"><a href="https://www.ey.com/cn/zh/about-us/entrepreneurship" onclick="generic_WT('/cn/zh/about-us/entrepreneurship','/cn/zh/about-us/entrepreneurship', '%E4%BC%81%E4%B8%9A%E5%AE%B6%E7%B2%BE%E7%A5%9E', '_self', 'Overlay Link');return false;">企业家精神</a><ul class="subUlFirst"><li><a href="https://www.ey.com/cn/zh/about-us/entrepreneurship/entrepreneur-of-the-year" onclick="generic_WT('/cn/zh/about-us/entrepreneurship/entrepreneur-of-the-year','/cn/zh/about-us/entrepreneurship/entrepreneur-of-the-year', '%E5%AE%89%E6%B0%B8%E4%BC%81%E4%B8%9A%E5%AE%B6%E5%A5%96', '_self', 'Overlay Link');return false;">安永企业家奖</a></li></ul></li><li class="two"><a href="https://www.ey.com/cn/zh/about-us/our-sponsorships-and-programs" onclick="generic_WT('/cn/zh/about-us/our-sponsorships-and-programs','/cn/zh/about-us/our-sponsorships-and-programs', '%E5%AE%89%E6%B0%B8%E8%B5%9E%E5%8A%A9%E7%9A%84%E9%A1%B9%E7%9B%AE%E5%92%8C%E6%B4%BB%E5%8A%A8', '_self', 'Overlay Link');return false;">安永赞助的项目和活动</a></li><li class="two"><a href="https://www.ey.com/cn/zh/about-us/our-people-and-culture" onclick="generic_WT('/cn/zh/about-us/our-people-and-culture','/cn/zh/about-us/our-people-and-culture', '%E6%88%91%E4%BB%AC%E7%9A%84%E5%91%98%E5%B7%A5%E5%92%8C%E6%9C%BA%E6%9E%84%E6%96%87%E5%8C%96', '_self', 'Overlay Link');return false;">我们的员工和机构文化</a><ul class="subUlFirst"><li><a href="https://www.ey.com/cn/zh/about-us/our-people-and-culture/diversity-and-inclusiveness" onclick="generic_WT('/cn/zh/about-us/our-people-and-culture/diversity-and-inclusiveness','/cn/zh/about-us/our-people-and-culture/diversity-and-inclusiveness', '%E5%A4%9A%E5%85%83%E5%8C%96%E5%92%8C%E5%8C%85%E5%AE%B9%E6%80%A7', '_self', 'Overlay Link');return false;">多元化和包容性</a></li><li><a href="https://www.ey.com/cn/zh/about-us/our-people-and-culture/our-history" onclick="generic_WT('/cn/zh/about-us/our-people-and-culture/our-history','/cn/zh/about-us/our-people-and-culture/our-history', '%E5%AE%89%E6%B0%B8%E7%9A%84%E5%8E%86%E5%8F%B2', '_self', 'Overlay Link');return false;">安永的历史</a></li><li><a href="https://www.ey.com/cn/zh/about-us/our-people-and-culture/our-awards" onclick="generic_WT('/cn/zh/about-us/our-people-and-culture/our-awards','/cn/zh/about-us/our-people-and-culture/our-awards', '%E5%AE%89%E6%B0%B8%E5%8F%96%E5%BE%97%E7%9A%84%E5%A5%96%E9%A1%B9%E4%B8%8E%E5%98%89%E8%AE%B8', '_self', 'Overlay Link');return false;">安永取得的奖项与嘉许</a></li><li><a href="https://www.ey.com/cn/zh/about-us/our-people-and-culture/our-alumni" onclick="generic_WT('/cn/zh/about-us/our-people-and-culture/our-alumni','/cn/zh/about-us/our-people-and-culture/our-alumni', '%E5%AE%89%E6%B0%B8%E5%89%8D%E5%91%98%E5%B7%A5', '_self', 'Overlay Link');return false;">安永前员工</a></li></ul></li><li class="two"><a href="https://www.ey.com/cn/zh/about-us/corporate-responsibility" onclick="generic_WT('/cn/zh/about-us/corporate-responsibility','/cn/zh/about-us/corporate-responsibility', '%E4%BC%81%E4%B8%9A%E7%A4%BE%E4%BC%9A%E8%B4%A3%E4%BB%BB', '_self', 'Overlay Link');return false;">企业社会责任</a></li><li class="two"><a href="https://www.ey.com/cn/zh/about-us/ey-ethics-hotline" onclick="generic_WT('/cn/zh/about-us/ey-ethics-hotline','/cn/zh/about-us/ey-ethics-hotline', '%E5%AE%89%E6%B0%B8%2F%E4%B8%93%E4%B8%9A%E6%93%8D%E5%AE%88%E8%81%94%E7%B3%BB%E7%83%AD%E7%BA%BF', '_self', 'Overlay Link');return false;">安永/专业操守联系热线</a></li></ul></li><li id="nav-newsroom"><a href="https://www.ey.com/CN/zh/newsroom" class="topnavdropdown">新闻中心</a><ul class="level2topicheader" id="newsDrop"><li class="two"><a href="https://www.ey.com/cn/zh/newsroom/pr-contacts" onclick="generic_WT('/cn/zh/newsroom/pr-contacts','/cn/zh/newsroom/pr-contacts', '%E4%BC%81%E4%B8%9A%E4%BC%A0%E8%AE%AF%E4%BA%BA%E5%91%98%E8%81%94%E7%B3%BB%E8%B5%84%E6%96%99', '_self', 'Overlay Link');return false;">企业传讯人员联系资料</a></li><li class="two"><a href="https://www.ey.com/cn/zh/newsroom/pr-activities" onclick="generic_WT('/cn/zh/newsroom/pr-activities','/cn/zh/newsroom/pr-activities', '%E4%BC%81%E4%B8%9A%E4%BC%A0%E8%AE%AF%E6%B4%BB%E5%8A%A8', '_self', 'Overlay Link');return false;">企业传讯活动</a></li><li class="two"><a href="https://www.ey.com/cn/zh/newsroom/analyst-relations" onclick="generic_WT('/cn/zh/newsroom/analyst-relations','/cn/zh/newsroom/analyst-relations', '%E4%B8%8E%E5%88%86%E6%9E%90%E5%91%98%E7%9A%84%E5%85%B3%E7%B3%BB', '_self', 'Overlay Link');return false;">与分析员的关系</a></li><li class="two"><a href="https://www.ey.com/cn/zh/newsroom/facts-and-figures" onclick="generic_WT('/cn/zh/newsroom/facts-and-figures','/cn/zh/newsroom/facts-and-figures', '%E4%BF%A1%E6%81%AF%E5%92%8C%E6%95%B0%E6%8D%AE', '_self', 'Overlay Link');return false;">信息和数据</a></li></ul></li><li id="nav-staycon"><a href="https://www.ey.com/CN/zh#" class="topnavdropdown">保持联系</a><ul class="level2topicheader" id="connectDrop" style="display:none"><li><a href="javascript:openSecureURL('/Email_Alerts', '', 'Email Alerts', '_blank')">电邮提示</a></li><li><a href="javascript:generic_link_WT('https://www.ey.com/gl/en/home/ey-insights', 'null', '%E6%B5%81%E5%8A%A8%E8%A3%85%E7%BD%AE%E5%BA%94%E7%94%A8%E7%A8%8B%E5%BA%8F', '_blank');">流动装置应用程序</a></li><li><a href="javascript:generic_link_WT('https://www.ey.com/gl/en/home/social-media', 'null', '%E7%A4%BE%E4%BA%A4%E5%AA%92%E4%BD%93', '_blank');">社交媒体</a></li><li><a href="javascript:generic_link_WT('http://webcast.ey.com/thoughtcenter/default.aspx', 'null', '%E7%BD%91%E7%BB%9C%E5%B9%BF%E6%92%AD%20%2F%20%E9%9F%B3%E8%A7%86%E9%A2%91%E6%92%AD%E5%AE%A2', '_blank');">网络广播 / 音视频播客</a></li></ul></li><li id="nav-location"><a href="javascript:void(0);" class="topnavdropdown">中国 (简体中文) <span style="background: transparent url(/ecimages/flags/CN.gif) no-repeat scroll 0% 0%; " id="countryoverlayspan"></span></a><div class="overlayContainer" style="display:none"><div id="countryOverlayContent"><div id="location_selectordiv"><span class="title" style="font-weight:bold">地点选择</span><form action="https://www.ey.com/Home" method="post" id="rememberme"><input type="checkbox" id="persist" name="pt" checked="checked">记住我的选项<input type="hidden" name="pc"><input type="hidden" name="pl"></form><div class="clear"></div><div id="location_selector_nav"><div id="letters"></div><a class="countryMenu" href="javascript:setCC('GL','EN');"><span>全球 (English)</span></a></div><div id="country_list_container"></div></div><div class="countryBorderCover"></div></div></div><script type="text/javascript">var countryLetters=[{l:"A",a:["Albania|AL|English|en","Algeria|DZ|French|fr","Angola|AO|English|en","Argentina|AR|Spanish|es","Armenia|AM|English|en","Aruba|AW|English|en","Australia|AU|English|en","Austria|AT|German|de","Azerbaijan|AZ|English|en"]},{l:"B",a:["Bahamas|BS|English|en","Bahrain|BH|English|en","Barbados|BB|English|en","Belarus|BY|English;Russian|en;ru","Belgium|BE|English|en","Bermuda|BM|English|en","Bolivia|BO|Spanish|es","Bosnia-Herzegovina|BA|English|en","Botswana|BW|English|en","Brazil|BR|Portuguese|pt","British Virgin Islands|VG|English|en","Brunei|BN|English|en","Bulgaria|BG|English|en"]},{l:"C",a:["Cambodia|KH|English|en","Canada|CA|English;French|en;fr","Cayman Islands|KY|English|en","Central America|AC|English|en","Channel Islands|NN|English|en","Chile|CL|Spanish|es","Colombia|CO|Spanish|es","Congo|CD|English|en","Costa Rica|CR|Spanish|es","Croatia|HR|English|en","Curacao|AN|English|en","Cyprus|CY|English|en","Czech Republic|CZ|Czech;English|cs;en","中国|CN|English;简体中文|en;zh"]},{l:"D",a:["Denmark|DK|Danish|da","Dominican Republic|DO|Spanish|es"]},{l:"E",a:["Ecuador|EC|Spanish|es","Egypt|EG|English|en","El Salvador|SV|Spanish|es","Equatorial Guinea|GQ|English|en","Estonia|EE|English|en"]},{l:"F",a:["Fiji|FJ|English|en","Finland|FI|Finnish|fi","France|FR|French|fr","Francophone Africa|FA|English|en","FYROM - Macedonia|MK|English|en"]},{l:"G",a:["Gabon|GA|English|en","Georgia|GE|English|en","Germany|DE|German|de","Ghana|GH|English|en","Gibraltar|GI|English|en","Global|GL|English|en","Greece|GR|English|en","Guam|GU|English|en","Guatemala|GT|Spanish|es","Guernsey|GG|English|en","Guinea|GN|English|en"]},{l:"H",a:["Honduras|HN|Spanish|es","Hong Kong|HK|English;简体中文|en;zh","Hungary|HU|English;Hungarian|en;hu"]},{l:"I",a:["Iceland|IS|English|en","India|IN|English|en","Indonesia|ID|English|en","Iraq|IQ|English|en","Ireland|IE|English|en","Isle of Man|IM|English|en","Israel|IL|English;Hebrew|en;he","Italy|IT|Italian|it","Ivory Coast|CI|English|en"]},{l:"J",a:["Jamaica|JM|English|en","Japan|JP|English|en","Jordan|JO|English|en"]},{l:"K",a:["Kazakhstan|KZ|English;Russian|en;ru","Kenya|KE|English|en","Korea|KR|English;Korean|en;ko","Kuwait|KW|English|en"]},{l:"L",a:["Laos|LA|English|en","Latvia|LV|English|en","Lebanon|LB|English|en","Libya|LY|English|en","Lithuania|LT|English|en","Luxembourg|LU|English|en"]},{l:"M",a:["Macau|MO|English;简体中文|en;zh","Madagascar|MG|English|en","Malawi|MW|English|en","Malaysia|MY|English|en","Maldives|MV|English|en","Malta|MT|English|en","Mauritius|MU|English|en","Mexico|MX|Spanish|es","Middle East and North Africa|EM|English|en","Moldova|MD|English|en","Mongolia|MN|English|en","Montenegro|ME|English|en","Morocco|MA|English|en","Mozambique|MZ|English|en","Myanmar|MM|English|en"]},{l:"N",a:["Namibia|NA|English|en","Netherlands|NL|English;Dutch|en;nl","New Zealand|NZ|English|en","Nicaragua|NI|Spanish|es","Nigeria|NG|English|en","Norway|NO|Norwegian|no"]},{l:"O",a:["Oman|OM|English|en"]},{l:"P",a:["Pakistan|PK|English|en","Palestinian Authority|PS|English|en","Panama|PA|Spanish|es","Paraguay|PY|Spanish|es","Peru|PE|Spanish|es","Philippines|PH|English|en","Poland|PL|Polish|pl","Portugal|PT|English|en"]},{l:"Q",a:["Qatar|QA|English|en"]},{l:"R",a:["Romania|RO|English|en","Russia|RU|English;Russian|en;ru","Rwanda|RW|English|en"]},{l:"S",a:["Saint Lucia|LC|English|en","Saipan|SP|English|en","Saudi Arabia|SA|English|en","Senegal|SN|English|en","Serbia|CS|English|en","Singapore|SG|English|en","Slovak Republic|SK|English;Slovak|en;sk","Slovenia|SI|English|en","South Africa|ZA|English|en","Spain|ES|Spanish|es","Sri Lanka|LK|English|en","Sweden|SE|Swedish|sv","Switzerland|CH|German;English;French|de;en;fr"]},{l:"T",a:["Tanzania|TZ|English|en","Thailand|TH|English|en","Trinidad and Tobago|TT|English|en","Tunisia|TN|French|fr","Turkey|TR|English;Turkish|en;tr","台湾|TW|English;繁体中文|en;zh_TW"]},{l:"U",a:["Uganda|UG|English|en","Ukraine|UA|English;Ukrainian|en;uk","United Arab Emirates|AE|English|en","United Kingdom|UK|English|en","United States|US|English|en","Uruguay|UY|Spanish|es","Uzbekistan|UZ|English|en"]},{l:"V",a:["Venezuela|VE|Spanish|es","Vietnam|VN|English;Vietnamese|en;vi"]},{l:"Z",a:["Zambia|ZM|English|en","Zimbabwe|ZW|English|en"]}];</script></li></ul>''')
        f.write('''	</div>''')
        f.write('''<header class="main-header">''')
        f.write('''	<div class="container"><div class="eyscrollogo"><a href="#" class="logo"><img src="http://cti-pub-files.oss-cn-shanghai.aliyuncs.com/pics/careers_ey_logo_zh_CN.png" alt="EY Ernst Young logo" border="0"></a></div>''')
        f.write('''		''')
        f.write('''        <section class="right clearfix">''')
        f.write('''        </section>''')
        f.write('''	</div>''')
        f.write('''</header><div class="eyhero hero-text-left" style="background-image: url(http://cti-pub-files.oss-cn-shanghai.aliyuncs.com/pics/banner.jpg); background-size: cover; background-position: 80% 50%;">      <div class="article-hero-container">        <div class="headline-container frame3x2 box3x2 fluid-box ">        <!-- add box3x2 class above for solid box -->		        <svg viewBox="0 0 800 610" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:sketch="http://www.bohemiancoding.com/sketch/ns">          <defs>            <style type="text/css">              @font-face {                font-family: "Interstate", sans-serif;                src: url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-2.eot");                src: url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-2.eot?") format("embedded-opentype"), url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-3.woff") format("woff"), url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-1.ttf") format("truetype");                src: url("https://www.ey.com/ecimages/fonts/interstate/d8612af1-3daa-4d49-940c-72424499dce4-3.woff") format("woff");              }              [id^="tagline-"] {                font-family: "Interstate";                fill: #ffffff;                letter-spacing: 1px;                font-size: 24px;                letter-spacing: -.03em;              }            </style>            <filter x="-50%" y="-50%" width="200%" height="200%" filterUnits="objectBoundingBox" id="filter-1">              <feOffset dx="0" dy="0" in="SourceAlpha" result="shadowOffsetOuter1"></feOffset>              <feGaussianBlur stdDeviation="2.5" in="shadowOffsetOuter1" result="shadowBlurOuter1"></feGaussianBlur>              <feColorMatrix values="0 0 0 0 0   0 0 0 0 0   0 0 0 0 0  0 0 0 0.35 0" in="shadowBlurOuter1" type="matrix" result="shadowMatrixOuter1"></feColorMatrix>              <feMerge>                <feMergeNode in="shadowMatrixOuter1"></feMergeNode>                <feMergeNode in="SourceGraphic"></feMergeNode>              </feMerge>            </filter>            <linearGradient x1="50%" y1="0%" x2="50%" y2="100%" id="darkGradient">              <stop stop-color="#000000" stop-opacity="0.6" offset="0%"></stop>              <stop stop-color="#000000" stop-opacity="0" offset="100%"></stop>            </linearGradient>            <linearGradient x1="50%" y1="0%" x2="50%" y2="100%" id="lightGradient">              <stop stop-color="#ffffff" stop-opacity="0.6" offset="0%"></stop>              <stop stop-color="#ffffff" stop-opacity="0" offset="100%"></stop>            </linearGradient>          </defs>          <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd" sketch:type="MSPage">            <g id="3x2-frame" sketch:type="MSArtboardGroup">              <g id="frames" sketch:type="MSLayerGroup" transform="translate(9.000000, 32.000000)">                <text class="tab-content" id="tagline-en-gl" filter="url(#filter-1)" sketch:type="MSTextLayer">                  <tspan x="1" y="560">The better the question. The better the answer. The better the world works.</tspan>                </text>                <text class="tab-content" id="tagline-ru-ru" filter="url(#filter-1)" sketch:type="MSTextLayer">                  <tspan x="1" y="560">У вас есть вопрос? У нас есть ответ. Решая сложные задачи бизнеса, мы улучшаем мир.</tspan>                </text>                <text class="tab-content" id="tagline-uk-ua" filter="url(#filter-1)" sketch:type="MSTextLayer">                  <tspan x="1" y="560">У вас є запитання? У нас є відповідь. Вирішуючи складні завдання бізнесу, ми змінюємо світ на краще.</tspan>                </text>                <text class="tab-content" id="tagline-ca-fr" filter="url(#filter-1)" sketch:type="MSTextLayer">                  <tspan x="1" y="560">Meilleure la question, meilleure la réponse. Pour un monde meilleur.</tspan>                </text>                <text class="tab-content" id="tagline-zh_tw-tw" filter="url(#filter-1)" sketch:type="MSTextLayer">                  <tspan x="1" y="560">問題越好。答案越好。商業世界越美好。</tspan>                </text>                <text class="tab-content" id="tagline-zh-cn" filter="url(#filter-1)" sketch:type="MSTextLayer">                  <tspan x="1" y="560">问题越好。答案越好。商业世界越美好。</tspan>                </text>                <g id="dots" transform="translate(1.000000, 511.000000)" fill="#FFE600" sketch:type="MSShapeGroup">                  <rect id="Rectangle-2" x="0" y="0" width="12" height="12"></rect>                  <rect id="0:0:0:0" x="42" y="0" width="12" height="12"></rect>                  <rect id="0:0:0:0-copy" x="21" y="0" width="12" height="12"></rect>                </g>                <path d="M22,115 L537,25.2818985 L537,427 L22,427 L22,115 Z" id="gradient" fill="url(#darkGradient)" sketch:type="MSShapeGroup"></path>                <path d="M88,447 L113,447 L113,472 L88,472 L88,447 Z M44,447 L69,447 L69,472 L44,472 L44,447 Z M0,447 L25,447 L25,472 L0,472 L0,447 Z M130.955,446.766 L534.275,446.766 L534.275,30.151 L25.724,119.822 L25.724,428.874 L0.4993,428.874 L0.4993,98.656 L559.499,0.089 L559.499,471.99 L130.954,471.99 L130.955,446.766 Z" id="frame" fill="#FFE600" sketch:type="MSShapeGroup"></path>                <path d="M0.499300892,98.567 L559.5,0 L559.5,471.901 L0,471.911 L0.499300892,98.567 Z" id="box" sketch:type="MSShapeGroup"></path>                <path d="M0.000699708326,503.779999 L0.000699708326,130.601559 L745.004444,0 L745.004444,503.779699 L0,503.779699 L0.000699708326,503.779999 Z" id="4x2-box" sketch:type="MSShapeGroup"></path>              </g>            </g>          </g>        </svg>		        <div class="smartquestion">          <div class="heading-block fluid-type">            <h1 class="eyhero-headline-1">网络安全威胁情报<br>感知、抵御、应对</h1>            <h2 class="eyhero-subheading-1">安永2018年网络安全威胁情报第x周</h2>          </div>        </div>''')
        f.write('''<div class="status">''')
        f.write('''status''')
        f.write('''</div>      </div>      </div>    </div><article class="article type-system-ey "> <section class="section0" id="section0" data-section-title="漏洞级别概况及目录" style="background-color:#F0F0F0"> <div class="container"><aside id="scroll-on-page-top" class="article-subnav"><ul id="featuremenu"><li id="feature01"><a href="#maincolumn">漏洞级别</a></li><li id="feature02"><a href="#section2">漏洞类别</a></li><li id="feature03"><a href="#section4">漏洞补丁</a></li><li id="feature04"><a href="#section6">漏洞关系</a></li><li id="feature05"><a href="#section8">漏洞趋势</a></li></ul></aside><div class="maincolumn"><h3>本周安全漏洞级别概况</h3>''')
        #f.write('''<p>根据2018年X月第X周的扫描情况，共发现xx个漏洞，</p><p>其中高风险漏洞XX个，占总漏洞数的xx%；中风险漏洞XX个，低危漏洞XX个。</p>''')
        #for list_each3 in list3[:4]:
         #   f.write('''<p>%s</p>''' % list_each3)
        f.write('''<p>%s</p>''' % text1)
        f.write('''<p><iframe src="http://cti-pub-files.oss-cn-shanghai.aliyuncs.com/pie.html" width=800px  height=380px  frameborder="0"  scrolling="no"></iframe><h3>High risk vulnerability</h3>''')
        f.write('''<table border="1" class="dataframe">''')
        f.write('''<thead>''')
        f.write('''<tr style="text-align: right;">''')
        f.write('''<th id=thc1>cveId</th>''')
        f.write('''<th id=thc2>Vulnerability Type</th>''')
        f.write('''<th id=thc3>Date</th>''')
        f.write('''<th id=thc4>Description</th>''')
        f.write('''</tr>''')
        f.write('''</thead>''')

        for list_each1 in list1[8:]:
            f.write('''%s''' % list_each1)
        f.write('''</table>''')
        #f.write('''%s''' % list1)
        f.write('''</p></div></div></section><section class="section2" id="section2" data-section-title="漏洞类别" style="background-color:#F0F0F0">''')
        f.write('''	<div class="container"><div class="row"><div class="col large-9"><h3>漏洞类别</h3> </div></div><div class="row"><div class="col large-9">''')
        
        #for list_each3 in list3[5:]:
            #f.write('''<p>%s</p>''' % list_each3)
        f.write('''<p>%s</p>''' % text2)
        f.write('''<iframe src="http://cti-pub-files.oss-cn-shanghai.aliyuncs.com/bar1.html"''')
        #f.write('''<p>%s</p>''' % list3[1])


        f.write('''width="750" height="420" scrolling="no" frameborder="0"></iframe>''')
        f.write('''		''')
        f.write('''		<!-- <div class="col large-3">  </div> --></div></div></section><section class="section4" id="section4" data-section-title="漏洞补丁" style="background-color:#F0F0F0"><div class="container"><div class="row"><div class="col large-9"><h3>金融行业数据风险事件</h3> </div></div><div class="row"><div class="col large-9">''')
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
        f.write('''			<!-- <div class="col large-3">  </div> --></div></div></section><section class="section4" id="section4" data-section-title="漏洞补丁" style="background-color:#F0F0F0"><div class="container"><div class="row"><div class="col large-9"><h3>科技行业数据风险事件</h3> </div></div><div class="row"><div class="col large-9">''')

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
        f.write('''</div><!-- <div class="col large-3"><img title="安永第19届全球信息安全调查报告" alt="安永第19届全球信息安全调查报告" src="./ey_cti_cn_rpt_files/53-rs.png"></div> --></div></div></section></article><style type="text/css"> .eylogo {display:none;} </style><footer class="footer" id="footer" role="contentinfo">''')
        f.write('''	<div class="footer-logo">''')
        f.write('''<div class="footer-links">''')
        f.write('''</div>''')
        f.write('''	''')
        f.write('''	<p class="detail">安永是指 Ernst &amp; Young Global Limited的全球组织，也可指其一家或以上的成员机构，各成员机构都是独立的法人实体。Ernst &amp; Young Global Limited是英国一家担保有限公司，并不向客户提供服务。<script>$("#topnav > li > a").each(function(){var HKurl = $(this).attr("href");var HKcodes = HKurl.split("/");if(HKcodes[1]=="HK"){var HKnew = HKurl.replace("HK","CN");$(this).attr("href", HKnew);		}});</script><script>var insightnav = '<div class="text-row" style="padding: 10px 20px; color: rgb(255, 255, 255); font-size: 14px;">访问 <a style="background: none; list-style: none; padding: 0px; color: #ffe600; font-size: 14px; display: inline;text-decoration:underline;" href="https://betterworkingworld.ey.com/" target="_blank">Building a Better Working World</a> 察看我们的最新观察。</div>';$(document).ready(function(){$('a[href="/cn/zh/issues"]').attr('target','_blank');$('a[href="/cn/zh/issues"]').attr("onclick", null );$(".nav-issues").append('<div class="sub threecolumn" style="opacity: 0; display: none; width: 730px;">' + insightnav + '</div>');$("#mainnav-issues").append('<div class="subnavOverlayContainer"><div id="navIssuesOverlayContent"><div class="subNavContainer" id="mainnav_issues">' + insightnav + '</div></div></div>');});</script><script>var cookieMsg="This site uses cookies to provide you with a personalised browsing experience.  By using this site you agree to our use of cookies as explained in our Privacy Policy.   Please read our <a href=\"/CN/zh/home/privacy\">Privacy Policy</a> for more information on how we use cookies and how you can manage them."; var cookieClose="Close";</script></p>''')
        f.write('''</footer>''')
        f.write('''''')
        f.write('''''')
        f.write('''''')
        f.write('''''')
        f.write('''''')
        f.write('''''')
        f.write('''''')
        f.write('''</body></html>''')
def main():


   # min=0,max=0,month=5,year=2018
    ##    cursor,db = ConnectSQL()
    #headers = COOKIES('http://www.cnvd.org.cn/flaw/list.htm?flag=true?number=%E8%AF%B7%E8%BE%93%E5%85%A5%E7%B2%BE%E7%A1%AE%E7%BC%96%E5%8F%B7&startDate=&endDate=&flag=true&field=&order=&max=20&offset=0')
    finance = getnews('finance')
    #print(finance)
    science = getnews('science')
    #print(science)
    retail = getnews('retail')
    #print(retail)
    write_html('test_16.html',finance,science,retail)


if __name__ == '__main__':
    main()
