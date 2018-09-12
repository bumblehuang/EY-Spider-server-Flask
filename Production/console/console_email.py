#coding:utf-8
import smtplib
from smtplib import *
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from email.utils import formataddr
import console_logger

import os
import mysql.connector
db_host = os.environ['db_host']
db_password = os.environ['db_password']
mail_server_1 = os.environ['mail_server']
mail_password = os.environ['mail_password']
oss_host = os.environ['oss_host']
oss_password = os.environ['oss_password']
logger = console_logger.get_logger(__name__)
def mail_sender(topic,filename):
    db = mysql.connector.connect(user='root',
                                 password=db_password,
                                 host=db_host,
                                 port='3306',
                                 database='admin'
                                 )
    db.set_charset_collation('utf8')
    cursor = db.cursor()
    whom_to_send=[]
    if filename == 'industry_mail.html':
        sql  =  '''select * from industry_customer'''
    elif filename == 'test_vul_word0705.html':
        sql  =  '''select * from vul_customer'''
    elif filename == 'datesecurity_mail.html':
        sql = '''select * from media_customer'''
    cursor.execute(sql)

    # try:
    #                 db.commit()
    # except:
    #                 db.rollback()
    for i in cursor:
        logger.debug(str(i[0]))
        whom_to_send.append(str(i[0]))

    with open(filename, 'rb') as fp:
        temp_file = fp.read()
    logger.debug(whom_to_send)
    email_of_user="skylark@eycyber.com" #发件人地址
    sender_name = "Cyber Threat Intelligence" #发件人昵称
    #收件人地址
    # "jacob.ma@cn.ey.com","mark-jj.lu@cn.ey.com",
    subject=topic #邮件标题
    
    username="CTI" 			#smtp服务器用户名
    password=mail_password		#smtp服务器密码
    mail_server = mail_server_1	#smtp服务器地址
	
    print whom_to_send
    print email_of_user
    # f = open(temp_file, 'r')
    # mail_text = f.read()
    msg = MIMEText(temp_file, 'html', 'utf-8')
    # msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = formataddr([sender_name,email_of_user])
    msg['To']='Default Customer'

    Server=smtplib.SMTP()
    try:
        #Server.set_debuglevel(1)
        # for i in whom_to_send:
            # ";".join(whom_to_send) 
            # msg['To']=i
        Server.connect(mail_server)
        # Server.ehlo_or_helo_if_needed()
        Server.login(username,password)
        Server.sendmail(email_of_user,whom_to_send,msg.as_string())
        return "200"
    except SMTPResponseException as e:
        error_code = e.smtp_code
        return  error_code

    Server.quit()
def mail_sender2(topic,filename,individual):

    with open(filename, 'rb') as fp:
        temp_file = fp.read()
    
    email_of_user="skylark@eycyber.com" #发件人地址
    sender_name = "Cyber Threat Intelligence" #发件人昵称
    #收件人地址
    # "jacob.ma@cn.ey.com","mark-jj.lu@cn.ey.com",
    subject=topic #邮件标题
    
    username="CTI"          #smtp服务器用户名
    password=mail_password      #smtp服务器密码
    mail_server = mail_server_1 #smtp服务器地址
    
    print individual
    print email_of_user
    # f = open(temp_file, 'r')
    # mail_text = f.read()
    msg = MIMEText(temp_file, 'html', 'utf-8')
    # msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = formataddr([sender_name,email_of_user])
    msg['To']=individual

    Server=smtplib.SMTP()
    try:
        #Server.set_debuglevel(1)
        # for i in whom_to_send:
            # ";".join(whom_to_send) 
            # msg['To']=i
        Server.connect(mail_server)
        # Server.ehlo_or_helo_if_needed()
        Server.login(username,password)
        Server.sendmail(email_of_user,individual,msg.as_string())
        logger.debug('successfully execute.')
        return "200"
    except SMTPResponseException as e:
        print(e)
        error_code = e.smtp_code
        return  error_code

    Server.quit()
if __name__=="__main__":
	mail_sender(whom_to_send,temp_file,subject,email_of_user,sender_name)

