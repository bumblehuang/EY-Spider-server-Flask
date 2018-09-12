# -*- coding: UTF-8 -*-
from flask import Flask, request
from flask import Response
from flask import json
from flask import Flask, redirect, url_for, request, render_template, make_response, abort, jsonify, send_from_directory,redirect
import requests
import time
import uuid
import console_logger
import datetime
import console_wechat
import console_github
import logging
import mysql.connector
import console_db
import sys
import console_visualizer
from flask_login import LoginManager
import flask_login
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin,BaseView,expose,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import BaseForm
from flask_login import LoginManager, UserMixin,login_required
from wtforms import StringField
import console_datasecurity
import console_datasecurity_brief
import console_email
import console_vul
import console_vul_brief
# import console_industry
# import console_industry_brief
## console_industry and console_industry_brief are the old version report template for the  skylark industry report
import console_industry_second
import console_industry_second_brief
import uuid
from sqlalchemy import event
from sqlalchemy.event import listens_for
import uuid
from wtforms import TextField, PasswordField,SelectField,validators
from wtforms.validators import Required
from apscheduler.schedulers.background import BackgroundScheduler
import os
LOCATION = 'HK'
db_host = os.environ['db_host']
db_password = os.environ['db_password']
reload(sys)
sys.setdefaultencoding('utf-8')
log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.INFO)  # DEBUG
s = requests.session()
s.keep_alive = False
fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)
app = Flask(__name__)
logger = console_logger.get_logger(__name__)
scheduler = BackgroundScheduler()
storage=[]
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:'+db_password+'@'+db_host+':3306/admin'
db = SQLAlchemy(app)
admin = Admin(app,name='Skylark')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'please login!'
login_manager.session_protection = 'strong'
Job_Store={}

class InsertscrapyForm(BaseForm): 
    insert_task_owner= StringField()
    insert_task_startTime = StringField(render_kw={"placeholder": "标准格式: 2029-01-01 20:00:00"})
    insert_task_endTime=StringField(render_kw={"placeholder": "标准格式: 2029-01-01 20:00:00"})
    insert_task_frequency=StringField(render_kw={"placeholder": "直接输入天数 例如:1"})
    insert_task_crawlerId=SelectField(
            coerce=str,
            choices=[('cve', 'cve'),('cnvd', 'cnvd'),('xuanwu', 'xuanwu'),('trendmicro', 'trendmicro'),('infosecinstitute', 'infosecinstitute'),('cisco', 'cisco'),('cac', 'cac')])
    insert_task_email_frequency = SelectField(
            coerce=str,
            choices=[('monthly', 'monthly'),('daily', 'daily'),('weekly', 'weekly')])
    insert_task_email_timepoint = StringField(render_kw={"placeholder": "xx:xx(for daily) or digits for others"})
    insert_task_email =StringField(render_kw={"placeholder": "exmaple@xxx.com"})
##  如果需要重新定义 form则以上代码是重写form的代码

class InsertmediaForm(BaseForm): 
    insert_report_owner= StringField()
    insert_report_frequency= SelectField(
            coerce=str,
            choices=[('monthly', 'monthly'),('daily', 'daily'),('weekly', 'weekly')])
    insert_github_keywords = StringField(render_kw={"placeholder": "以英文逗号分隔: xxx,yyy"})
    insert_social_keyword = StringField(render_kw={"placeholder": "以英文逗号分隔: xxx,yyy"})
    insert_report_email_timepoint = StringField(render_kw={"placeholder": "xx:xx(for daily) or digits for others"})
    insert_report_email =StringField(render_kw={"placeholder": "exmaple@xxx.com"})


class InsertsocialForm(BaseForm): 
    insert_task_owner= StringField()
    insert_task_startTime = StringField(render_kw={"placeholder": "标准格式: 2029-01-01 20:00:00"})
    insert_task_endTime=StringField(render_kw={"placeholder": "标准格式: 2029-01-01 20:00:00"})
    insert_task_frequency=StringField(render_kw={"placeholder": "直接输入天数 例如:1"})
    insert_task_crawlerId=SelectField(
            coerce=str,
            choices=[('wechat', 'wechat'),('github','github')])

    insert_keyword = StringField(render_kw={"placeholder": "以英文逗号分隔: xxx,yyy"})
    insert_filter_keyword = StringField(render_kw={"placeholder": "以英文逗号分隔: xxx,yyy"})

class customer_email_Form(BaseForm): 
    customer_email = StringField()
class InsertReportForm(BaseForm): 
    insert_report_id= StringField(render_kw={"placeholder": "当前版本需要手动随机创建id"})
    insert_report_Time=StringField(render_kw={"placeholder": "标准格式: 2029-01-01 20:00:00"})
    insert_report_type=SelectField(
            coerce=str,
            choices=[('vul', 'vul'),('industry', 'industry')])
    insert_report_email=StringField()
class media_customer(db.Model):
    __tablename__ = 'media_customer'
    customer_email = db.Column(db.String(255),primary_key=True)
class vul_customer(db.Model):
    __tablename__ = 'vul_customer'
    customer_email = db.Column(db.String(255),primary_key=True)

class industry_customer(db.Model):
    __tablename__ = 'industry_customer'
    customer_email = db.Column(db.String(255),primary_key=True)

class insert_scrapy_task(db.Model):
    __tablename__ = 'insert_scrapy_task'
    # __table_args__ = (
    #     PrimaryKeyConstraint('insert_task_owner', 'insert_task_startTime','insert_task_endTime'),)
    insert_task_owner=db.Column(db.String(255),primary_key=True)
    insert_task_startTime=db.Column(db.String(255),primary_key=True)
    insert_task_endTime=db.Column(db.String(255))
    insert_task_frequency=db.Column(db.String(255))
    insert_task_crawlerId=db.Column(db.String(255))
    insert_task_email_frequency=db.Column(db.String(255))
    insert_task_email_timepoint=db.Column(db.String(255))
    insert_task_email = db.Column(db.String(255))

class insert_media_report(db.Model):
    __tablename__ = 'insert_media_report'

    insert_report_owner= db.Column(db.String(255),primary_key=True)
    insert_report_frequency=db.Column(db.String(255))
    insert_github_keywords = db.Column(db.String(255))
    insert_social_keyword = db.Column(db.String(255))
    insert_report_email_timepoint = db.Column(db.String(255))
    insert_report_email = db.Column(db.String(255),primary_key = True)

class insert_social_task(db.Model):
    __tablename__ = 'insert_social_task'
    # __table_args__ = (
    #     PrimaryKeyConstraint('insert_task_owner', 'insert_task_startTime','insert_task_endTime'),)
    insert_task_owner=db.Column(db.String(255),primary_key=True)
    insert_task_startTime=db.Column(db.String(255),primary_key=True)
    insert_task_endTime=db.Column(db.String(255))
    insert_task_frequency=db.Column(db.String(255))
    insert_task_crawlerId=db.Column(db.String(255))
    insert_keyword =db.Column(db.String(255))

class insert_github_task(db.Model):
    __tablename__ = 'insert_github_task'
    # __table_args__ = (
    #     PrimaryKeyConstraint('insert_task_owner', 'insert_task_startTime','insert_task_endTime'),)
    insert_task_owner=db.Column(db.String(255),primary_key=True)
    insert_task_startTime=db.Column(db.String(255),primary_key=True)
    insert_task_endTime=db.Column(db.String(255))
    insert_task_frequency=db.Column(db.String(255))
    insert_task_crawlerId=db.Column(db.String(255))
    insert_keyword =db.Column(db.String(255))
    insert_filter_keyword=db.Column(db.String(255))

class task(db.Model):
    task_id=db.Column(db.String(255),primary_key=True)
    task_name=db.Column(db.String(255))
    task_owner=db.Column(db.String(255))
    task_startTime=db.Column(db.String(255))
    task_endTime=db.Column(db.String(255))
    task_sequence=db.Column(db.String(255))
    task_crawlerId=db.Column(db.String(255))
    task_frequency=db.Column(db.String(255))
    task_crawlerType=db.Column(db.String(255))
    task_url=db.Column(db.String(255))
    task_node=db.Column(db.String(255))
    task_modelid=db.Column(db.String(255))
    task_modelName=db.Column(db.String(255))
    task_reportId=db.Column(db.String(255))
    task_reportName=db.Column(db.String(255))
    task_communication=db.Column(db.String(255))
    task_email=db.Column(db.String(255))
    request_id=db.Column(db.String(255))
    task_status = db.Column(db.String(255))
class job(db.Model):
    task_id=db.Column(db.String(255))
    job_id=db.Column(db.String(255),primary_key=True, unique=True)
    job_createdTime=db.Column(db.String(255))
    job_startTime=db.Column(db.String(255))
    job_lastedTime=db.Column(db.String(255))
    job_endTime=db.Column(db.String(255))
    job_status=db.Column(db.String(255))
    job_node=db.Column(db.String(255))
    job_percentage=db.Column(db.String(255))
    job_unsuccessfulCount=db.Column(db.String(255))

class site(db.Model):
    site_id=db.Column(db.String(255),primary_key=True)
    site_title=db.Column(db.String(255))
    site_url=db.Column(db.String(255))
    site_type=db.Column(db.String(255))
    site_attribute=db.Column(db.String(255))
    site_area=db.Column(db.String(255))
    site_ranking=db.Column(db.String(255))
    site_weight=db.Column(db.String(255))
    site_ipAddress=db.Column(db.String(255))
    site_geoAddress=db.Column(db.String(255))
    site_scrapSection=db.Column(db.String(255))
    site_scrapPath=db.Column(db.String(255))
    site_scrapListed=db.Column(db.String(255))
    site_scrapFrequency=db.Column(db.String(255))
    site_worldRank=db.Column(db.String(255))

class User(db.Model, flask_login.UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.String(255), primary_key=True, unique=True)
    password = db.Column(db.String(100))
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id
# insert_report` (`insert_report_id` VARCHAR(255),`insert_report_Time` NVARCHAR(255),
#     `insert_report_type` NVARCHAR(255),`insert_report_email` NVARCHAR(255)
class insert_report(db.Model):
    insert_report_id= db.Column(db.String(255),primary_key=True)
    insert_report_Time=db.Column(db.String(255))
    insert_report_type=db.Column(db.String(255))
    insert_report_email=db.Column(db.String(255))

@listens_for(insert_media_report, 'after_insert')
def do_media_stuff(mapper, connect, target):
    logger.debug('*************************** below is the order information created ********************************')
    
    logger.debug(target.insert_report_owner)
    logger.debug(target.insert_report_frequency)
    logger.debug(target.insert_github_keywords)
    logger.debug(target.insert_social_keyword)
    logger.debug(target.insert_report_email_timepoint)
    logger.debug(target.insert_report_email)
    logger.debug('*************************** below is the order information created *******************************')
    insert_report_owner= target.insert_report_owner
    insert_report_frequency=target.insert_report_frequency
    insert_github_keywords= target.insert_github_keywords
    insert_social_keyword = target.insert_social_keyword
    insert_report_email_timepoint= target.insert_report_email_timepoint
    insert_report_email = target.insert_report_email
    if insert_report_frequency == 'monthly':
        if insert_report_email_timepoint.strip() != '':
            if int(insert_report_email_timepoint) <= 31:## 属于 monthly的代码逻辑
                console_db.insert_media_customer(insert_report_mail)
                scheduler.add_job(media_report_manual,'cron',day = int(insert_report_email_timepoint),hour = 9, minute = 0,args=[insert_github_keywords,insert_social_keyword])
            else:
                logger.debug('invalid input.....')
    if insert_report_frequency == 'daily':## 属于daily的代码逻辑
        if insert_report_email_timepoint.strip() != '':
            time_list = insert_report_email_timepoint.strip().split(':')
            the_hour = int(time_list[0])
            the_minute= int(time_list[1])
            if the_hour<= 24 and the_minute <= 59:
                console_db.insert_media_customer(insert_report_email)
                scheduler.add_job(media_report_manual,'cron',hour = the_hour, minute = the_minute,args=[insert_github_keywords,insert_social_keyword])
            else: 
                logger.debug('invalid input.....')
    if insert_report_frequency == 'weekly':## 属于weekly的代码逻辑
        if insert_report_email_timepoint.strip() != '':
            if int(insert_report_email_timepoint) <= 7:
                console_db.insert_media_customer(insert_report_email)
                scheduler.add_job(media_report_manual,'cron',day_of_week = int(insert_report_email_timepoint),hour = 9, minute = 0,args=[insert_github_keywords,insert_social_keyword])
            else: 
                logger.debug('invalid input.....')
def media_report_manual(github_keywords,weixin_keywords):
    request_id = 'Jacob'+uuid.uuid4().hex[16:]
    report_id = str(uuid.uuid4())
    github_keywords = github_keywords.strip().split(',')
    weixin_keywords = weixin_keywords.strip().split(',')
    email_3(github_keywords,weixin_keywords,request_id,report_id)
@event.listens_for(insert_social_task, 'after_insert')
def do_task_after_update(mapper, connection, target):
    logger.debug('*************************** below is the order information created ********************************')
    logger.debug(target.insert_task_owner)
    logger.debug(target.insert_task_startTime)
    logger.debug(target.insert_task_endTime)
    logger.debug(target.insert_task_frequency)
    logger.debug(target.insert_task_crawlerId)
    logger.debug('*************************** below is the order information created *******************************')
    task_owner = target.insert_task_owner
    task_startTime= target.insert_task_startTime
    task_endTime= target.insert_task_endTime
    task_frequency= target.insert_task_frequency
    task_crawlerId= target.insert_task_crawlerId
    keywords = target.insert_keyword
    insert_social_task_fromAdmin(task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId,keywords)
    

@event.listens_for(insert_github_task, 'after_insert')
def do_task_after_update(mapper, connection, target):
    logger.debug('*************************** below is the order information created ********************************')
    logger.debug(target.insert_task_owner)
    logger.debug(target.insert_task_startTime)
    logger.debug(target.insert_task_endTime)
    logger.debug(target.insert_task_frequency)
    logger.debug(target.insert_task_crawlerId)
    logger.debug('*************************** below is the order information created *******************************')

    task_owner = target.insert_task_owner
    task_startTime= target.insert_task_startTime
    task_endTime= target.insert_task_endTime
    task_frequency= target.insert_task_frequency
    task_crawlerId= target.insert_task_crawlerId
    keywords = target.insert_keyword
    filter_keyword =target.insert_filter_keyword
    insert_github_task_fromAdmin(task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId,keywords,filter_keyword)


def insert_github_task_fromAdmin(task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId,keywords,filter_keyword):
    if task_crawlerId == 'github':
        logger.debug(task_crawlerId)
        task_crawlerType='Social Media'
        task_communication= 'email'
        task_node='CONSOLE'
        created_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task_id = uuid.uuid4().hex[:8]
        task_name= 'console'+'-'+task_owner+'-'+str(datetime.datetime.strptime(created_time,"%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d"))+'-'+task_crawlerType
        Job_Store[task_id]=1
        task_sequence = Job_Store[task_id]
        logger.debug(type(task_frequency))
        console_db.insert_task(task_id,task_name,task_owner,task_startTime,task_endTime,task_sequence,task_crawlerId,task_frequency,task_crawlerType,None,task_node,None,None,None,None,None,None,'RUNNING')
        scheduler.add_job(github_scrapy,'interval', days=int(task_frequency),id=task_id,start_date=task_startTime,args=[created_time,task_id,task_communication,keywords,filter_keyword])
        return jsonify({'msg':'add the job of github ... '})

def insert_social_task_fromAdmin(task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId,keywords):
    send_in_parameters={}
    send_in_parameters['task_owner']=task_owner
    send_in_parameters['task_startTime']=task_startTime
    send_in_parameters['task_endTime']=task_endTime
    send_in_parameters['task_frequency']=task_frequency
    send_in_parameters['task_crawlerId']=task_crawlerId
    send_in_parameters['task_crawlerType']='Event'
    send_in_parameters['task_node']='SH'
    send_in_parameters['task_communication']='email'
    send_in_parameters['keywords']= keywords
    logger.debug('-----------------post into node 02 -------------------')
    logger.debug(send_in_parameters)
    if task_crawlerId == 'wechat':
        receive=requests.post("http://xxxx:8082/wechat",data=send_in_parameters)
        logger.debug('========== posted into wechat route')
    if task_crawlerId == 'github':
        logger.debug('尚未开发。。。。。。。。')

@listens_for(insert_scrapy_task, 'after_insert')
def do_stuff(mapper, connect, target):
    logger.debug('*************************** below is the order information created ********************************')
    logger.debug(target.insert_task_owner)
    logger.debug(target.insert_task_startTime)
    logger.debug(target.insert_task_endTime)
    logger.debug(target.insert_task_frequency)
    logger.debug(target.insert_task_crawlerId)
    logger.debug(target.insert_task_email_frequency)
    logger.debug(target.insert_task_email_timepoint)
    logger.debug(target.insert_task_email)
    logger.debug('*************************** below is the order information created *******************************')
    task_owner = target.insert_task_owner
    task_startTime= target.insert_task_startTime
    task_endTime= target.insert_task_endTime
    task_frequency= target.insert_task_frequency
    task_crawlerId= target.insert_task_crawlerId
    insert_task_email_frequency= target.insert_task_email_frequency
    insert_task_email_timepoint= target.insert_task_email_timepoint
    insert_task_email = target.insert_task_email
    if task_crawlerId == 'cve':
            insert_cve_fromADMIN(task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId)
            logger.debug('we have done the update version insertion.......')
    if task_crawlerId == 'cnvd':
            insert_cnvd_fromADMIN(task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId)
            logger.debug('we have done the update version insertion.......')
    if task_crawlerId == 'xuanwu':
            insert_xuanwu_fromADMIN(task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId)
            logger.debug('we have done the update version insertion.......')
    if task_crawlerId == 'trendmicro':
            insert_trendmicro_fromADMIN(task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId)
            logger.debug('we have done the update version insertion.......')
    if task_crawlerId == 'infosecinstitute':
            insert_infosecinstitute_fromADMIN(task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId)
            logger.debug('we have done the update version insertion.......')
    if task_crawlerId == 'cisco':
            insert_cisco_fromADMIN(task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId)
            logger.debug('we have done the update version insertion.......')
    if task_crawlerId == 'cac':
            insert_cac_fromADMIN(task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId)
            logger.debug('we have done the update version insertion.......')
    if insert_task_email_frequency == 'monthly':
        if insert_task_email_timepoint.strip() != '':
            if int(insert_task_email_timepoint) <= 31:## 属于 monthly的代码逻辑
                console_db.insert_customer(insert_task_email)
                scheduler.add_job(task_email_manual,'cron',start_date=task_startTime,end_date=task_endTime,day = int(insert_task_email_timepoint),hour = 9, minute = 0)
            else:
                logger.debug('invalid input.....')
    if insert_task_email_frequency == 'daily':## 属于daily的代码逻辑
        if insert_task_email_timepoint.strip() != '':
            time_list = insert_task_email_timepoint.strip().split(':')
            the_hour = int(time_list[0])
            the_minute= int(time_list[1])
            if the_hour<= 24 and the_minute <= 59:
                console_db.insert_customer(insert_task_email)
                scheduler.add_job(task_email_manual,'cron',start_date=task_startTime,end_date=task_endTime,hour = the_hour, minute = the_minute)
            else: 
                logger.debug('invalid input.....')
    if insert_task_email_frequency == 'weekly':## 属于weekly的代码逻辑
        if insert_task_email_timepoint.strip() != '':
            if int(insert_task_email_timepoint) <= 7:
                console_db.insert_customer(insert_task_email)
                scheduler.add_job(task_email_manual,'cron',start_date=task_startTime,end_date=task_endTime,day_of_week = int(insert_task_email_timepoint),hour = 9, minute = 0)
            else: 
                logger.debug('invalid input.....')

@event.listens_for(insert_scrapy_task, 'after_update')# 听取机制
def do_task_after_update(mapper, connection, target):
    logger.debug('*************************** below is the order information updated - in the after update scope ********************************')
    logger.debug(target.insert_task_owner)
    logger.debug(target.insert_task_startTime)
    logger.debug(datetime.datetime.strptime(target.insert_task_startTime, "%Y-%m-%d %H:%M:%S"))
    logger.debug(target.insert_task_endTime)
    logger.debug(target.insert_task_frequency)
    logger.debug(target.insert_task_crawlerId)
    logger.debug('*************************** below is the order information updated - in the after update scope *******************************')
    start_time = datetime.datetime.strptime(target.insert_task_startTime, "%Y-%m-%d %H:%M:%S")
    if start_time > datetime.datetime.now():
        task_owner = target.insert_task_owner
        task_startTime= target.insert_task_startTime
        task_endTime= target.insert_task_endTime
        task_frequency= target.insert_task_frequency
        task_crawlerId= target.insert_task_crawlerId
        insert_task_email_frequency= target.insert_task_email_frequency
        insert_task_email_timepoint= target.insert_task_email_timepoint
        insert_task_email = target.insert_task_email
        if task_crawlerId == 'cve':
            insert_cve_fromADMIN(task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId)
            logger.debug('we have done the update version insertion.......')
            if insert_task_email_frequency == 'monthly':
                if int(insert_task_email_timepoint) <= 31:
                    console_db.insert_customer(insert_task_email)
                    scheduler.add_job(task_email_manual,'cron',start_date=task_startTime,end_date=task_endTime,day = int(insert_task_email_timepoint),hour = 9, minute = 0)
                else: 
                    logger.debug('invalid input.....')
            if insert_task_email_frequency == 'daily':
                time_list = insert_task_email_timepoint.strip().split(':')
                the_hour = int(time_list[0])
                the_minute= int(time_list[1])
                if the_hour<= 24 and the_minute <= 59:
                    console_db.insert_customer(insert_task_email)
                    scheduler.add_job(task_email_manual,'cron',start_date=task_startTime,end_date=task_endTime,hour = the_hour, minute = the_minute)
                else: 
                    logger.debug('invalid input.....')
            if insert_task_email_frequency == 'weekly':
                if int(insert_task_email_timepoint) <= 7:
                    console_db.insert_customer(insert_task_email)
                    scheduler.add_job(task_email_manual,'cron',start_date=task_startTime,end_date=task_endTime,day_of_week = int(insert_task_email_timepoint),hour = 9, minute = 0)
                else: 
                    logger.debug('invalid input.....')

def task_email_manual():
    request_id = 'Jacob'+uuid.uuid4().hex[16:]
    report_id = str(uuid.uuid4())
    console_vul.write_html('report-v15.html',report_id,request_id)
    console_vul_brief.write_html('test_vul_word0705.html',report_id,request_id)
    console_industry_second.write_html('industry.html',report_id,request_id)
    console_industry_second_brief.write_html('industry_mail.html',report_id,request_id)
    
    days1 = datetime.date(2018, 07, 01)
    days2 = datetime.date.today()
    num = (days2-days1).days
    weeks = (num//7)+1
    postfix = '(第'+str(weeks)+'周)'
    console_email.mail_sender("xx网络安全漏洞威胁情报"+postfix,'test_vul_word0705.html')
    console_email.mail_sender("xx网络安全行业威胁情报"+postfix,'industry_mail.html')

@listens_for(insert_report, 'after_insert')
def do_report(mapper, connect, target):
    logger.debug('====================')
    scheduler.add_job(email_manual,'date', run_date=target.insert_report_Time,args=[target.insert_report_type,target.insert_report_email])
def email_manual(insert_report_type,insert_report_email):
    request_id = 'Jacob'+uuid.uuid4().hex[16:]
    report_id = str(uuid.uuid4())
    logger.debug('********************')
    insert_report_type = insert_report_type.strip()
    insert_report_email = insert_report_email.strip()
    days1 = datetime.date(2018, 07, 01)
    days2 = datetime.date.today()
    num = (days2-days1).days
    weeks = (num//7)+1
    postfix = '(第'+str(weeks)+'周)'
    if insert_report_type == 'vul':
        logger.debug('********'+insert_report_type+'******')
        logger.debug('********'+insert_report_email+'******')
        console_vul.write_html('report-v15.html',report_id,request_id)
        console_vul_brief.write_html('test_vul_word0705.html',report_id,request_id)
        console_email.mail_sender2("xx网络安全漏洞威胁情报"+postfix,'test_vul_word0705.html',insert_report_email)
        logger.debug('hello. we get in vul')
    if insert_report_type == 'industry':
        logger.debug('********'+insert_report_type+'******')
        logger.debug('********'+insert_report_email+'******')
        console_industry_second.write_html('industry.html',report_id,request_id)
        console_industry_second_brief.write_html('industry_mail.html',report_id,request_id)
        console_email.mail_sender2("xx网络安全行业威胁情报"+postfix,'industry_mail.html',insert_report_email)
        logger.debug('hello. we get in industry.........')

@event.listens_for(task, 'after_update')
def change_task_after_update(mapper, connection, target):
    if target.task_node == 'HK':
        new_start = target.task_startTime
        new_end = target.task_endTime
        new_status = target.task_status
        task_id = target.task_id
        send_out_information = {}
        send_out_information['new_frequency'] = target.task_frequency
        send_out_information['new_status']= str(new_status)
        send_out_information['new_start'] = str(new_start)
        send_out_information['new_end'] = str(new_end)
        send_out_information['task_id'] = str(task_id)
        logger.debug(send_out_information)
        receive=requests.post("xxx:8081/edit_task",data=send_out_information)
        logger.debug(receive)
    if target.task_node == 'SH':
        new_start = target.task_startTime
        new_end = target.task_endTime
        new_status = target.task_status
        task_id = target.task_id
        send_out_information = {}
        send_out_information['new_frequency'] = target.task_frequency
        send_out_information['new_status']= str(new_status)
        send_out_information['new_start'] = str(new_start)
        send_out_information['new_end'] = str(new_end)
        send_out_information['task_id'] = str(task_id)
        logger.debug(send_out_information)
        receive=requests.post("xxx:8082/edit_task",data=send_out_information)
        logger.debug(receive)
    else:
        logger.debug('changing console task')
    return jsonify({'msg':'task modified.'})


class MyView_customer(ModelView):
    can_create = True
    column_display_pk=True
    can_delete = True
    def is_accessible(self):
        return flask_login.current_user.is_authenticated
    form = customer_email_Form
class MyView_job(ModelView):
    try:
        logger.debug(flask_login.current_user.is_authenticated)
    except Exception as e:
        logger.debug(e)
    can_create = False
    column_display_pk=True
    def is_accessible(self):
        try:
            logger.debug('we are trying to access the customizable view')
            logger.debug(login_manager)
            logger.debug(login_manager)
            logger.debug(flask_login.current_user.id)
            logger.debug(flask_login.current_user.password)

        except Exception as e:
            logger.debug('oops !!!!!')
        return flask_login.current_user.is_authenticated

class Myview_insert_media_report(ModelView):
    can_create = True
    column_display_pk=True
    def is_accessible(self):
        return flask_login.current_user.is_authenticated
    form = InsertmediaForm
class MyView_insert_task(ModelView):
    can_create = True
    column_display_pk=True
    def is_accessible(self):
        return flask_login.current_user.is_authenticated
    form = InsertscrapyForm
class MyView_insert_social_task(ModelView):
    can_create = True
    column_display_pk=True
    def is_accessible(self):
        return flask_login.current_user.is_authenticated
    form = InsertsocialForm
class MyView_insert_report(ModelView):
    can_create = True
    column_display_pk=True
    def is_accessible(self):
        return flask_login.current_user.is_authenticated
    form = InsertReportForm
class MyView_task(ModelView):
    can_create = False
    column_display_pk=True
    column_exclude_list = ('task_modelid','task_modelName','task_reportId','task_reportName')
    column_editable_list = ('task_status','task_startTime','task_endTime','task_frequency')
    # form_overrides = dict('task_status'=SelectField)
    # form_args = dict(
    #     # Pass the choices to the `SelectField`
    #     'task_status'=dict(
    #         choices=['RUNNING', 'RESUMED', 'PAUSED','TERMINATED']
    #     ))
    form_choices = {
                 'task_status': [
                     ('RUNNING', 'RUNNING'),
                     ('RESUMED', 'RESUMED'),
                     ('PAUSED', 'PAUSED'),
                     ('TERMINATED', 'TERMINATED')
                ]
           }
    def is_accessible(self):
        return flask_login.current_user.is_authenticated

class MyView_site(ModelView):
    can_create = False
    def is_accessible(self):
        return flask_login.current_user.is_authenticated
general=[insert_scrapy_task,insert_social_task,insert_github_task]
admin.add_view(MyView_insert_task(general[0], db.session))
admin.add_view(MyView_insert_social_task(general[1], db.session , category='Insert Social Website Task'))
admin.add_view(MyView_insert_social_task(general[2], db.session , category='Insert Social Website Task'))
# admin.add_view(MyView_insert_task(insert_social_task, db.session))
admin.add_view(Myview_insert_media_report(insert_media_report, db.session))
admin.add_view(MyView_insert_report(insert_report, db.session))
admin.add_view(MyView_job(job, db.session))
admin.add_view(MyView_task(task, db.session))
admin.add_view(MyView_site(site, db.session))
admin.add_view(MyView_customer(vul_customer, db.session,category='Customer List'))
admin.add_view(MyView_customer(industry_customer, db.session,category='Customer List'))
admin.add_view(MyView_customer(media_customer, db.session,category='Customer List'))


@login_manager.user_loader
def user_loader(username):
    user = User()
    user.id = username
    logger.debug("user_loader user is %s, is_authenticated %s" % (user.id, user.is_authenticated))
    return user


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
# @flask_login.login_required
def index():
    logger.debug("index page, method is %s" % request.method)
    logger.debug('==========================================')
    return redirect(url_for('login'))

@app.route('/error')
@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(500)
def error(e):
    logger.debug("error occurred: %s" % e)
    try:
        code = e.code
        if code == 400:
            return render_template('400.html')
        elif code == 401:
            return render_template('401.html')
        else:
            return render_template('error.html')
    except Exception as e:
        logger.debug('exception is %s' % e)
    finally:
        return render_template('error.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        logger.debug("login post method")
        username = request.form['username']
        password = request.form['password']
        logger.debug(username)
        logger.debug(password)
        next_url = request.args.get("next")
        logger.debug('next is %s' % next_url)

        if username == 'xxx' and password== 'xxx':
            # set login user
            user1 = User()
            user1.id = username
            user1.password = password
            flask_login.login_user(user1,remember=True)
           
            # return jsonify({"status":'1'})
            # return jsonify({'status':'1'})
            logger.debug('we get here')
            # resp = make_response(render_template('index.html', name=username))
            # resp.set_cookie('username', username)
            # if not is_safe_url(next_url):
            #     return abort(400)
            try:
                logger.debug('here we still got the user')
                logger.debug(flask_login.current_user.is_authenticated)
                logger.debug(flask_login.current_user.id)
                logger.debug(flask_login.current_user.password)
            except Exception as e:
                logger.debug('oooooooooooooooooo')
            return redirect('http://localhost:9000/admin/')
        else:
            return abort(401)

    logger.debug("login get method")
    return render_template('login.html')


@app.route('/logout')
@flask_login.login_required
def logout():
    # remove the username from the session if it's there
    logger.debug("logout page")
    flask_login.logout_user()
    return redirect(url_for('login'))


@app.route("/reporting", methods=['GET', 'POST'])
def receive():
    if request.method == 'POST':
        job_id=request.form['job_id']
        created_time=request.form['created_time']
        start_time = request.form['start_time']
        lasted_time = request.form['lasted_time']
        lasted_time = lasted_time[:-7]
        status = request.form['status']
        end_time = request.form['end_time']
        location = request.form['location']
        percentage = request.form['percentage']
        unsuccessful_count = request.form['unsuccessful_count']
        task_id = request.form['task_id']
        logger.debug('===================================now running the job of '+job_id+'======================================')
        logger.debug('CREATED TIME is'+created_time)
        logger.debug('START TIME IS '+start_time)
        logger.debug('LASTING DURATION IS '+lasted_time)
        logger.debug('END TIME IS '+end_time)
        logger.debug('running in the node of '+location)
        logger.debug('The percentage of successful Response is '+percentage[:6])
        logger.debug('This job belongs to '+task_id)
        logger.debug('===================================now running the job of '+job_id+'======================================')
        logger.debug(type(percentage))
        insert_percentage = str(float(percentage)*100)[:5] + '%'
        logger.debug(insert_percentage)
        console_db.update_job(job_id,created_time,start_time,lasted_time,status,end_time,location,insert_percentage,unsuccessful_count,task_id)
        job_list = job_id.strip().split('-')
        task_sequence = job_list[1]
        run_status = 'RUNNING'
        console_db.update_task(task_id,task_sequence,run_status)
        return jsonify({'msg':'successful'})

@app.route("/cnvd_select", methods=['GET', 'POST'])
def handleCNVD():
    if request.method == 'POST':
        input_dict = json.loads(request.data)
        task_owner=input_dict['task_owner']
        task_startTime=input_dict['task_startTime']##'2018-06-25 12:30:00'
        task_endTime=input_dict['task_endTime']##'2018-06-25 16:00:00'
        task_frequency = input_dict['task_frequency']## 2 minutes.
        task_crawlerId=input_dict['task_crawlerId']## cnvd
        task_crawlerType=input_dict['task_crawlerType'] ## not yet to decide ......
        task_communication= input_dict['task_communication']
        task_node=input_dict['task_node'] ## this is not to be used in the location here .......

        if task_node=='SH':
            send_in_parameters={}
            send_in_parameters['task_owner']=task_owner
            send_in_parameters['task_startTime']=task_startTime##'2018-06-25 12:30:00'
            send_in_parameters['task_endTime']=task_endTime##'2018-06-25 16:00:00'
            send_in_parameters['task_frequency']=task_frequency## 2 minutes.
            send_in_parameters['task_crawlerId']=task_crawlerId
            send_in_parameters['task_crawlerType']=task_crawlerType ## not yet to decide ......
            ## https://xuanwulab.github.io/cn/secnews/
            send_in_parameters['task_node']=task_node ## this is not to be used in the location here .......
            send_in_parameters['task_communication']=task_communication

            receive=requests.post("http://xxxx:8082/cnvd",data= send_in_parameters)
            logger.debug(receive.json)
            
            # ui_response = receive.data
            return jsonify({'msg':'the parameters have been sent into the second layer(Shanghai Node).......'})
        else:
            return jsonify({'msg':'this is not shanghai and we have not yet implemented other lcation .......'})

@app.route("/cnvd_data", methods=['GET', 'POST'])
def handleCNVD_data():
    if request.method == 'POST':
        data_list = json.loads(request.data)
        for each_one in data_list:
            a=each_one['vul_id']
            b=each_one['vul_cveId'] 
            c=each_one['vul_cweId'] 
            d=each_one['vul_describe']
            e=each_one['vul_score'] 
            f=each_one['vul_level'] 
            g=each_one['vul_type']
            h=each_one['vul_cvssAccess']
            i=each_one['vul_cvsComplexity']
            j=each_one['vul_cvssAuthentication']
            k=each_one['vul_cvssConf']
            l=each_one['vul_cvssInteg']
            m=each_one['vul_cvssAvail']
            n=each_one['vul_name']
            o=each_one['vul_publishedDate']
            p=each_one['vul_updateDate']
            q=each_one['vul_containSol']
            r=each_one['vul_source']
            s=each_one['vul_effectedProduct']
            t=each_one['vul_vendor']
            u=each_one['vul_patch']
            v=each_one['vul_author']
            w=each_one['vul_expCode']
            x=each_one['vul_hash']
            console_db.cnvd_update(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x)
            logger.debug([a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x])
            return jsonify({'msg':'inserted into the cnvd.....'})
@app.route("/cve", methods=['GET', 'POST'])
def cveOrder():
    if request.method == 'POST':
        input_dict = json.loads(request.data)
        task_owner=input_dict['task_owner']
        task_startTime=input_dict['task_startTime']
        task_endTime=input_dict['task_endTime']
        task_frequency = input_dict['task_frequency']
        task_crawlerId=input_dict['task_crawlerId']
        task_crawlerType=input_dict['task_crawlerType']
        task_communication= input_dict['task_communication']
        task_node=input_dict['task_node']
        if task_node=='HK':
            send_in_parameters={}
            send_in_parameters['task_owner']=task_owner
            send_in_parameters['task_startTime']=task_startTime
            send_in_parameters['task_endTime']=task_endTime
            send_in_parameters['task_frequency']=task_frequency
            send_in_parameters['task_crawlerId']=task_crawlerId
            send_in_parameters['task_crawlerType']=task_crawlerType 
            send_in_parameters['task_node']=task_node 
            send_in_parameters['task_communication']=task_communication

            logger.debug('-----------------post into node 02 -------------------')
            receive=requests.post("http://xxx:8081/cve_order",data= send_in_parameters)
            logger.debug('did we get here')
            return jsonify({'msg':'successful'})

@app.route("/cve_data", methods=['GET', 'POST'])
def handleCVE_data():
    if request.method == 'POST':
        data_list = json.loads(request.data)
        # logger.debug(data_list)
        logger.debug(type(data_list))
        logger.debug('this is the area of receiving cve data............')
        for each in data_list:
            a=each['vul_cveId']
            b=each['vul_cweId']
            c=each['vul_numOfExploits']
            d=each['vul_type']
            e=each['vul_publishedDate']
            f=each['vul_updateDate']
            g=each['vul_score']
            h=each['vul_accessLevel']
            i=each['vul_access']
            j=each['vul_complexity']
            k=each['vul_authentication']
            l=each['vul_conf']
            m=each['vul_integ']
            n=each['vul_avail']
            o=each['vul_des']
            p=each['vul_hash']
            console_db.cve_insert_data(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p)
        logger.debug('################################################') 
        logger.debug('all the cve first stage data have been inserted ')
        logger.debug('################################################')

        return jsonify({'msg':'successful.....'})

@app.route("/wechat_task", methods=['GET', 'POST'])
def wechat_task():
    if request.method == 'POST':
        input_dict = json.loads(request.data)
        task_owner=input_dict['task_owner']
        task_startTime=input_dict['task_startTime']##'2018-06-25 12:30:00'
        task_endTime=input_dict['task_endTime']##'2018-06-25 16:00:00'
        task_frequency = input_dict['task_frequency']## 2 minutes.
        task_crawlerId=input_dict['task_crawlerId']
        task_crawlerType=input_dict['task_crawlerType'] ## not yet to decide ......
        task_communication= input_dict['task_communication']
        task_node=input_dict['task_node'] ## this is not to be used in the location here .......

        if task_node=='SH':
            send_in_parameters={}
            send_in_parameters['task_owner']=task_owner
            send_in_parameters['task_startTime']=task_startTime##'2018-06-25 12:30:00'
            send_in_parameters['task_endTime']=task_endTime##'2018-06-25 16:00:00'
            send_in_parameters['task_frequency']=task_frequency## 2 minutes.
            send_in_parameters['task_crawlerId']=task_crawlerId
            send_in_parameters['task_crawlerType']=task_crawlerType ## not yet to decide ......
            send_in_parameters['task_node']=task_node ## this is not to be used in the location here .......
            send_in_parameters['task_communication']=task_communication

            receive=requests.post("http://xxxx:8082/wechat",data= send_in_parameters)
            logger.debug(receive.json)
            
            # ui_response = receive.data
            return jsonify({'msg':'the parameters have been sent into the second layer(Shanghai Node).......'})
        else:
            return jsonify({'msg':'this is not shanghai and we have not yet implemented other lcation .......'})
@app.route("/wechat_data", methods=['GET', 'POST'])
def handleWECHAT_data():
    if request.method == 'POST':
        data_list = json.loads(request.data)
        for send_out_data in data_list:
            a=send_out_data['title']
            b=send_out_data['content']
            c=send_out_data['date']
            d=send_out_data['nickname']
            e=send_out_data['wechat']
            f=send_out_data['link']
            g=send_out_data['keyword']
            console_db.insert_wechat_data(a,b,c,d,e,f,g)
            logger.debug('################################################') 
            logger.debug('all the wechat data have been inserted ')
            logger.debug('################################################')
        return jsonify({'msg':'inserted into the cnvd.....'})

@app.route("/github_task", methods=['GET', 'POST'])
def github_task():
    if request.method == 'POST':
        input_dict = json.loads(request.data)
        task_owner=input_dict['task_owner']
        task_startTime=input_dict['task_startTime']
        task_endTime=input_dict['task_endTime']
        task_frequency = input_dict['task_frequency']
        task_crawlerId=input_dict['task_crawlerId']
        task_crawlerType=input_dict['task_crawlerType']
        task_communication= input_dict['task_communication']
        task_node=input_dict['task_node']
        keywords = input_dict['keywords']
        filter_keyword = input_dict['filter_keyword']
        created_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task_id = uuid.uuid4().hex[:8]
        task_name= 'console'+'-'+task_owner+'-'+str(datetime.datetime.strptime(created_time,"%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d"))+'-'+task_crawlerType
        Job_Store[task_id]=1
        task_sequence = Job_Store[task_id]
        console_db.insert_task(task_id,task_name,task_owner,task_startTime,task_endTime,task_sequence,task_crawlerId,task_frequency,task_crawlerType,None,task_node,None,None,None,None,None,None,'RUNNING')
        scheduler.add_job(github_scrapy,'interval', days=task_frequency,id=task_id,start_date=task_startTime,args=[created_time,task_id,task_communication,keywords,filter_keyword])
        return jsonify({'msg':'add the job of github ... '})


            
def github_scrapy(created_time,task_id,task_communication,keywords,filter_keyword):
    
    if task_id in Job_Store:
            task_sequence=Job_Store[task_id]
            Job_Store[task_id]= Job_Store[task_id]+1 
    else:
            Job_Store[task_id]=1
            task_sequence=Job_Store[task_id]
    job_id=task_id+'-'+str(task_sequence)+'-'+LOCATION
    logger.debug('================================= github initiated ========================================')
    logger.debug(job_id)
    logger.debug('================================= github initiated ========================================')
    console_github.execute_github(job_id,created_time,task_id,keywords,filter_keyword)

    
@app.route("/insert_task", methods=['GET', 'POST'])
def insert_task():
    if request.method == 'POST':
        # input_dict = json.loads(request.data)
        # input_dict['task_crawlerId']
        task_owner=request.form['task_owner']
        task_startTime=request.form['task_startTime']##'2018-06-25 12:30:00'
        task_endTime=request.form['task_endTime']##'2018-06-25 16:00:00'
        task_frequency = int(request.form['task_frequency'])## 2 minutes.
        task_crawlerId=request.form['task_crawlerId']
        task_crawlerType=request.form['task_crawlerType'] ## not yet to decide ......
        task_communication = request.form['task_communication']
        task_node=request.form['task_node']
        task_id=request.form['task_id']
        task_name=request.form['task_name']
        console_db.insert_task(task_id,task_name,task_owner,task_startTime,None,None,task_crawlerId,task_frequency,task_crawlerType,None,task_node,None,None,None,None,task_communication,None,'RUNNING')
        logger.debug('task info inserted')
        return jsonify({'msg':'Task information successfully inserted...........'})

@app.route("/query_task", methods=['GET', 'POST'])
def query_task():
    if request.method == 'POST':
        input_dict = json.loads(request.data)
        task_owner = "'"+input_dict['task_owner']+"'"
        task_crawlerId = "'"+input_dict['task_crawlerId']+"'"
        result = console_db.query_task(task_owner,task_crawlerId)
        logger.debug(result)
        feedback_list = []
        for each_set in result:
            task_id = "'"+str(each_set[0].encode('utf-8'))+"'"
            result2 = console_db.query_jobs(task_id)
            feedback = {}
            for job_id,created_time,start_time,lasted_time,status,end_time,location,percentage,unsuccess in result2:
                feedback['job_id']='=======================Task '+task_id+'======has the job of ======'+job_id+'======================================'
                feedback['created_time']= 'CREATED TIME is'+created_time
                feedback['start_time']= 'START TIME IS '+start_time
                feedback['lasted_time'] = 'LASTING DURATION IS '+lasted_time
                feedback['end_time'] = 'END TIME IS '+end_time
                feedback['location']= 'running in the node of '+location
                feedback['percentage']= 'The percentage of successful Response is '+str(percentage)
                feedback['task_id']='This job belongs to '+task_id
                feedback_list.append(feedback)
        return jsonify(feedback_list)

def initiate_default_tasks():
    request_id = 'Jacob'+uuid.uuid4().hex[16:]
    report_id = str(uuid.uuid4())
    scheduler.add_job(email_1,'cron',  day_of_week='*', hour=18,args=[request_id,report_id])
    scheduler.add_job(email_2,'cron',  day_of_week='*', hour=15,args=[request_id,report_id])
    scheduler.add_job(email_1,'cron',  day_of_week='*', hour=9,args=[request_id,report_id])
    scheduler.add_job(email_2,'cron',  day_of_week='*', hour=10,args=[request_id,report_id])
    scheduler.add_job(cve_detail_setup,'cron', day_of_week='*', hour=23 ,minute= 30)

@app.route("/initiate_customizable", methods=['GET', 'POST'])
def initiate_customizable():
    if request.method == 'POST':
        input_dict = json.loads(request.data)
        request_id = 'Tom'+uuid.uuid4().hex[16:]
        report_id = str(uuid.uuid4())
        time = input_dict['time']
        method = input_dict['method']
        if method =='email_1':
            scheduler.add_job(email_1,'interval', days = 200,start_date=time,args=[request_id,report_id])
        if method =='email_2':
            scheduler.add_job(email_2,'interval', days = 200,start_date=time,args=[request_id,report_id])

        return jsonify({'msg':'successfully ordered'})
@app.route('/event_securityfocus_hash2', methods=['POST'])
def event_securityfocus_hash2_data():
    if request.method == 'POST':
        dic_list = json.loads(request.data)
        for dic in dic_list:
            console_db.event_securityfocus_hash2_db(dic)
        return jsonify({'msg':'data successfully inserted'})

@app.route("/initiate_cron_trigger", methods=['GET', 'POST'])
def initiate_cron_trigger():
    if request.method == 'POST':
        request_id = 'Jacob'+uuid.uuid4().hex[16:]
        report_id = str(uuid.uuid4())
        scheduler.add_job(email_1,'cron',  day_of_week='*', hour=18,args=[request_id,report_id])
        scheduler.add_job(email_2,'cron',  day_of_week='*', hour=15,args=[request_id,report_id])
        scheduler.add_job(email_1,'cron',  day_of_week='*', hour=9,args=[request_id,report_id])
        scheduler.add_job(email_2,'cron',  day_of_week='*', hour=10,args=[request_id,report_id])
        scheduler.add_job(cve_detail_setup,'cron', day_of_week='*', hour=23 ,minute= 30)
        return jsonify({'msg':'successfully added cron job......'})

@app.route("/simulate_automation", methods=['GET', 'POST'])
def simulate_automation():
    if request.method == 'POST':
        # cve_detail_setup()
        # trend_micro_setup()
        request_id = 'Jacob'+uuid.uuid4().hex[16:]
        report_id = str(uuid.uuid4())
        scheduler.add_job(cve_detail_setup,'cron', day_of_week='*',hour=19,minute= 35)
        scheduler.add_job(email_1,'cron',  day_of_week='*', hour=19,minute=36,args=[request_id,report_id])
        scheduler.add_job(email_2,'cron',  day_of_week='*', hour=17,minute=36,args=[request_id,report_id])
        return jsonify({'msg':'successfully emailed'})
def insert_cve_fromADMIN(task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId):
    send_in_parameters={}
    send_in_parameters['task_owner']=task_owner
    send_in_parameters['task_startTime']=task_startTime
    send_in_parameters['task_endTime']=task_endTime
    send_in_parameters['task_frequency']=task_frequency
    send_in_parameters['task_crawlerId']=task_crawlerId
    send_in_parameters['task_crawlerType']='Event'
    send_in_parameters['task_node']='HK'
    send_in_parameters['task_communication']='email'
    logger.debug('-----------------post into node 02 -------------------')
    receive=requests.post("http://xxx:8081/cve_order",data= send_in_parameters)
def insert_cnvd_fromADMIN(task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId):
    send_in_parameters={}
    send_in_parameters['task_owner']=task_owner
    send_in_parameters['task_startTime']=task_startTime
    send_in_parameters['task_endTime']=task_endTime
    send_in_parameters['task_frequency']=task_frequency
    send_in_parameters['task_crawlerId']=task_crawlerId
    send_in_parameters['task_crawlerType']='Event'
    send_in_parameters['task_node']='SH'
    send_in_parameters['task_communication']='email'
    logger.debug('-----------------post into node 02 -------------------')
    receive=requests.post("http://xxxx:8082/cnvd",data= send_in_parameters)
def insert_xuanwu_fromADMIN(task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId):
    send_in_parameters={}
    send_in_parameters['task_owner']=task_owner
    send_in_parameters['task_startTime']=task_startTime
    send_in_parameters['task_endTime']=task_endTime
    send_in_parameters['task_frequency']=task_frequency
    send_in_parameters['task_crawlerId']=task_crawlerId
    send_in_parameters['task_crawlerType']='Event'
    send_in_parameters['task_node']='SH'
    send_in_parameters['task_communication']='email'
    logger.debug('-----------------post into node 02 -------------------')
    receive=requests.post("http://xxxx:8082/xuanwu_sh",data= send_in_parameters)
def insert_cisco_fromADMIN(task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId):
    send_in_parameters={}
    send_in_parameters['task_owner']=task_owner
    send_in_parameters['task_startTime']=task_startTime
    send_in_parameters['task_endTime']=task_endTime
    send_in_parameters['task_frequency']=task_frequency
    send_in_parameters['task_crawlerId']=task_crawlerId
    send_in_parameters['task_crawlerType']='Event'
    send_in_parameters['task_node']='HK'
    send_in_parameters['task_communication']='email'
    logger.debug('-----------------post into node 02 -------------------')
    receive=requests.post("http://xxx:8081/cisco_order",data= send_in_parameters)
def insert_cac_fromADMIN(task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId):
    send_in_parameters={}
    send_in_parameters['task_owner']=task_owner
    send_in_parameters['task_startTime']=task_startTime
    send_in_parameters['task_endTime']=task_endTime
    send_in_parameters['task_frequency']=task_frequency
    send_in_parameters['task_crawlerId']=task_crawlerId
    send_in_parameters['task_crawlerType']='Event'
    send_in_parameters['task_node']='SH'
    send_in_parameters['task_communication']='email'
    logger.debug('-----------------post into node 02 -------------------')
    receive=requests.post("http://xxxx:8082/cac",data= send_in_parameters)
def insert_infosecinstitute_fromADMIN(task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId):
    send_in_parameters={}
    send_in_parameters['task_owner']=task_owner
    send_in_parameters['task_startTime']=task_startTime
    send_in_parameters['task_endTime']=task_endTime
    send_in_parameters['task_frequency']=task_frequency
    send_in_parameters['task_crawlerId']=task_crawlerId
    send_in_parameters['task_crawlerType']='Event'
    send_in_parameters['task_node']='HK'
    send_in_parameters['task_communication']='email'
    logger.debug('-----------------post into node 02 -------------------')
    receive=requests.post("http://xxx:8081/infosecinstitute",data= send_in_parameters)
def insert_trendmicro_fromADMIN(task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId):
    send_in_parameters={}
    send_in_parameters['task_owner']=task_owner
    send_in_parameters['task_startTime']=task_startTime
    send_in_parameters['task_endTime']=task_endTime
    send_in_parameters['task_frequency']=task_frequency
    send_in_parameters['task_crawlerId']=task_crawlerId
    send_in_parameters['task_crawlerType']='Event'
    send_in_parameters['task_node']='HK'
    send_in_parameters['task_communication']='email'
    logger.debug('-----------------post into node 02 -------------------')
    receive=requests.post("http://xxx:8081/trendmicro",data= send_in_parameters)

def default_cve_order():
    send_in_parameters={}
    send_in_parameters['task_owner']='Jocob'
    k = datetime.datetime.today()
    a= str(k)[:11]+'20:10:20'
    send_in_parameters['task_startTime']=a
    send_in_parameters['task_endTime']='2029-07-23 20:00:00'
    send_in_parameters['task_frequency']=1
    send_in_parameters['task_crawlerId']='cve'
    send_in_parameters['task_crawlerType']='event'
    send_in_parameters['task_node']='HK'
    send_in_parameters['task_communication']='email'
    receive=requests.post("http://xxx:8081/cve_order",data= send_in_parameters)
def default_cnvd_order():
    send_in_parameters={}
    send_in_parameters['task_owner']='Jocob'
    k = datetime.datetime.today()
    a= str(k)[:11]+'21:40:20'
    send_in_parameters['task_startTime']=a
    send_in_parameters['task_endTime']='2029-07-23 20:00:00'
    send_in_parameters['task_frequency']=1
    send_in_parameters['task_crawlerId']='cnvd'
    send_in_parameters['task_crawlerType']='event'
    send_in_parameters['task_node']='SH'
    send_in_parameters['task_communication']='email'
    receive=requests.post("http://xxxx:8082/cnvd",data= send_in_parameters)

def email_1(request_id,report_id):
    days1 = datetime.date(2018, 07, 01)
    days2 = datetime.date.today()
    num = (days2-days1).days
    weeks = (num//7)+1
    postfix = '(第'+str(weeks)+'周)'
    console_vul.write_html('report-v15.html',report_id,request_id)
    console_vul_brief.write_html('test_vul_word0705.html',report_id,request_id)
    console_email.mail_sender("xx网络安全漏洞威胁情报"+postfix,'test_vul_word0705.html')
def email_2(request_id,report_id):
    days1 = datetime.date(2018, 07, 01)
    days2 = datetime.date.today()
    num = (days2-days1).days
    weeks = (num//7)+1
    postfix = '(第'+str(weeks)+'周)'
    console_industry_second.write_html('industry.html',report_id,request_id)
    console_industry_second_brief.write_html('industry_mail.html',report_id,request_id)
    console_email.mail_sender("xx网络安全行业威胁情报"+postfix,'industry_mail.html')
def email_3(github_keywords,weixin_keywords,request_id,report_id):
    days1 = datetime.date(2018, 07, 01)
    days2 = datetime.date.today()
    num = (days2-days1).days
    weeks = (num//7)+1
    postfix = '(第'+str(weeks)+'周)'
    console_datasecurity.write_html('datesecurity.html',github_keywords, weixin_keywords,report_id,request_id)
    console_datasecurity_brief.write_html('datesecurity_mail.html',github_keywords, weixin_keywords,report_id,request_id)
    console_email.mail_sender("xx数据安全威胁情报"+postfix,'datesecurity_mail.html')
def cve_detail_setup():
    page_list = console_db.second_cve_Urlcreator()
    console_db.second_cve_scrapper(page_list)

@app.route("/xuanwu", methods=['GET', 'POST'])
def handleXuanwu():
    if request.method == 'POST':
        input_dict = json.loads(request.data)
        task_owner = input_dict['task_owner']
        task_startTime = input_dict['task_startTime']  ##'2018-06-25 12:30:00'
        task_endTime = input_dict['task_endTime']  ##'2018-06-25 16:00:00'
        task_frequency = input_dict['task_frequency']  ## 2 minutes.
        task_crawlerId = input_dict['task_crawlerId']  ## xuanwu
        task_crawlerType = input_dict['task_crawlerType']  ## not yet to decide ......
        task_communication = input_dict['task_communication']
        task_node = input_dict['task_node']  ## this is not to be used in the location here .......

        if task_node == 'SH':
            send_in_parameters = {}
            send_in_parameters['task_owner'] = task_owner
            send_in_parameters['task_startTime'] = task_startTime  ##'2018-06-25 12:30:00'
            send_in_parameters['task_endTime'] = task_endTime  ##'2018-06-25 16:00:00'
            send_in_parameters['task_frequency'] = task_frequency  ## 2 minutes.
            send_in_parameters['task_crawlerId'] = task_crawlerId
            send_in_parameters['task_crawlerType'] = task_crawlerType  ## not yet to decide ......
            ## https://xuanwulab.github.io/cn/secnews/
            send_in_parameters['task_node'] = task_node  ## this is not to be used in the location here .......
            send_in_parameters['task_communication'] = task_communication

            receive = requests.post("http://xxxx:8082/xuanwu_sh", data=send_in_parameters)
            logger.debug(receive.json)

            # ui_response = receive.data
            return jsonify({'msg': 'the parameters have been sent into the second layer(Shanghai Node).......'})
        else:
            return jsonify({'msg': 'this is not shanghai and we have not yet implemented other location .......'})

@app.route("/xuanwu_data", methods=['GET', 'POST'])
def handleXuanwu_data():
    if request.method == 'POST':
        data_list = json.loads(request.data)
        logger.debug(len(data_list))

        for each_one in data_list:
            a = each_one['Category']
            b = each_one['Names']
            c = each_one['Link']
            e = each_one['Times']
            d = each_one['news_hash']
            console_db.xuanwu_update(a,b,c,d,e)
            logger.debug([a,b,c,d,e])
        return jsonify({'msg':'inserted into the xuanwu.....'})


################################### Hades Specail Area #########################################
@app.route("/cisco_select", methods=['GET', 'POST'])
def handlecisco():
    if request.method == 'POST':
        input_dict = json.loads(request.data)
        task_owner=input_dict['task_owner']
        task_startTime=input_dict['task_startTime']##'2018-06-25 12:30:00'
        task_endTime=input_dict['task_endTime']##'2018-06-25 16:00:00'
        task_frequency = input_dict['task_frequency']## 2 minutes.
        task_crawlerId=input_dict['task_crawlerId']
        task_crawlerType=input_dict['task_crawlerType'] ## not yet to decide ......
        task_communication= input_dict['task_communication']
        task_node=input_dict['task_node'] ## this is not to be used in the location here .......

        if task_node=='HK':
            send_in_parameters={}
            send_in_parameters['task_owner']=task_owner
            send_in_parameters['task_startTime']=task_startTime##'2018-06-25 12:30:00'
            send_in_parameters['task_endTime']=task_endTime##'2018-06-25 16:00:00'
            send_in_parameters['task_frequency']=task_frequency## 2 minutes.
            send_in_parameters['task_crawlerId']=task_crawlerId
            send_in_parameters['task_crawlerType']=task_crawlerType ## not yet to decide ......
            ## https://xuanwulab.github.io/cn/secnews/
            send_in_parameters['task_node']=task_node ## this is not to be used in the location here .......
            send_in_parameters['task_communication']=task_communication

            receive=requests.post("http://xxx:8081/cisco_order",data= send_in_parameters)
            logger.debug(receive.json)
            
            # ui_response = receive.data
            return jsonify({'msg':'the parameters have been sent into the second layer(HK Node).......'})
        else:
            return jsonify({'msg':'this is not HK and we have not yet implemented other lcation .......'})
@app.route("/cisco_data", methods=['GET', 'POST'])
def handlecisco_data():
    if request.method == 'POST':
        data_list = json.loads(request.data)
        # logger.debug(data_list)
        logger.debug(type(data_list))
        logger.debug('this is the area of receiving cisco data............')
        for each in data_list:   
            console_db.cisco_insert_data(each)
        logger.debug('################################################') 
        logger.debug('all the cisco data have been inserted ')
        logger.debug('################################################')
        return jsonify({'msg':'successful.....'})

###cac#########
@app.route("/cac_select", methods=['GET', 'POST'])
def handlecac():
    if request.method == 'POST':
        input_dict = json.loads(request.data)
        task_owner=input_dict['task_owner']
        task_startTime=input_dict['task_startTime']##'2018-06-25 12:30:00'
        task_endTime=input_dict['task_endTime']##'2018-06-25 16:00:00'
        task_frequency = input_dict['task_frequency']## 2 minutes.
        task_crawlerId=input_dict['task_crawlerId']
        task_crawlerType=input_dict['task_crawlerType'] ## not yet to decide ......
        task_communication= input_dict['task_communication']
        task_node=input_dict['task_node'] ## this is not to be used in the location here .......

        if task_node=='SH':
            send_in_parameters={}
            send_in_parameters['task_owner']=task_owner
            send_in_parameters['task_startTime']=task_startTime##'2018-06-25 12:30:00'
            send_in_parameters['task_endTime']=task_endTime##'2018-06-25 16:00:00'
            send_in_parameters['task_frequency']=task_frequency## 2 minutes.
            send_in_parameters['task_crawlerId']=task_crawlerId
            send_in_parameters['task_crawlerType']=task_crawlerType ## not yet to decide ......
            ## https://xuanwulab.github.io/cn/secnews/
            send_in_parameters['task_node']=task_node ## this is not to be used in the location here .......
            send_in_parameters['task_communication']=task_communication

            receive=requests.post("http://xxxx:8082/cac",data= send_in_parameters)
            logger.debug(receive.json)
            
            # ui_response = receive.data
            return jsonify({'msg':'the parameters have been sent into the second layer(Shanghai Node).......'})
        else:
            return jsonify({'msg':'this is not shanghai and we have not yet implemented other lcation .......'})






@app.route("/cac_data", methods=['GET', 'POST'])
def handlecac_data():
    if request.method == 'POST':
        data_list = json.loads(request.data)
        # logger.debug(data_list)
        logger.debug(type(data_list))
        logger.debug('this is the area of receiving cac data............')
        for each in data_list:   
            console_db.cac_insert_data(each)
        logger.debug('################################################') 
        logger.debug('all the cac data have been inserted ')
        logger.debug('################################################')
        return jsonify({'msg':'successful.....'})


@app.route("/infosecinstitute_select", methods=['GET', 'POST'])
def handleinfosecinstitute():
    if request.method == 'POST':
        input_dict = json.loads(request.data)
        task_owner=input_dict['task_owner']
        task_startTime=input_dict['task_startTime']##'2018-06-25 12:30:00'
        task_endTime=input_dict['task_endTime']##'2018-06-25 16:00:00'
        task_frequency = input_dict['task_frequency']## 2 minutes.
        task_crawlerId=input_dict['task_crawlerId']
        task_crawlerType=input_dict['task_crawlerType'] ## not yet to decide ......
        task_communication= input_dict['task_communication']
        task_node=input_dict['task_node'] ## this is not to be used in the location here .......

        if task_node=='HK':
            send_in_parameters={}
            send_in_parameters['task_owner']=task_owner
            send_in_parameters['task_startTime']=task_startTime##'2018-06-25 12:30:00'
            send_in_parameters['task_endTime']=task_endTime##'2018-06-25 16:00:00'
            send_in_parameters['task_frequency']=task_frequency## 2 minutes.
            send_in_parameters['task_crawlerId']=task_crawlerId
            send_in_parameters['task_crawlerType']=task_crawlerType ## not yet to decide ......
            ## https://xuanwulab.github.io/cn/secnews/
            send_in_parameters['task_node']=task_node ## this is not to be used in the location here .......
            send_in_parameters['task_communication']=task_communication

            receive=requests.post("http://xxx:8081/infosecinstitute",data= send_in_parameters)
            logger.debug(receive.json)
            
            # ui_response = receive.data
            return jsonify({'msg':'the parameters have been sent into the second layer(HK Node).......'})
        else:
            return jsonify({'msg':'this is not HK and we have not yet implemented other lcation .......'})



@app.route("/infosecinstitute_data", methods=['GET', 'POST'])
def handleinfosecinstitute_data():
    if request.method == 'POST':
        each = json.loads(request.data)
        # logger.debug(data_list)
        logger.debug('this is the area of receiving infosecinstitute data............')
        console_db.infosecinstitute_insert_data(each)
        logger.debug('################################################') 
        logger.debug('all the infosecinstitute data have been inserted ')
        logger.debug('################################################')
        return jsonify({'msg':'successful.....'})

@app.route("/trendmicro_select", methods=['GET', 'POST'])
def handletrendmicro():
    if request.method == 'POST':
        input_dict = json.loads(request.data)
        task_owner=input_dict['task_owner']
        task_startTime=input_dict['task_startTime']##'2018-06-25 12:30:00'
        task_endTime=input_dict['task_endTime']##'2018-06-25 16:00:00'
        task_frequency = input_dict['task_frequency']## 2 minutes.
        task_crawlerId=input_dict['task_crawlerId']
        task_crawlerType=input_dict['task_crawlerType'] ## not yet to decide ......
        task_communication= input_dict['task_communication']
        task_node=input_dict['task_node'] ## this is not to be used in the location here .......

        if task_node=='HK':
            send_in_parameters={}
            send_in_parameters['task_owner']=task_owner
            send_in_parameters['task_startTime']=task_startTime##'2018-06-25 12:30:00'
            send_in_parameters['task_endTime']=task_endTime##'2018-06-25 16:00:00'
            send_in_parameters['task_frequency']=task_frequency## 2 minutes.
            send_in_parameters['task_crawlerId']=task_crawlerId
            send_in_parameters['task_crawlerType']=task_crawlerType ## not yet to decide ......
            send_in_parameters['task_node']=task_node ## this is not to be used in the location here .......
            send_in_parameters['task_communication']=task_communication

            receive=requests.post("http://xxx:8081/trendmicro",data= send_in_parameters)
            logger.debug(receive.json)
            
            # ui_response = receive.data
            return jsonify({'msg':'the parameters have been sent into the second layer(HK Node).......'})
        else:
            return jsonify({'msg':'this is not HK and we have not yet implemented other lcation .......'})



@app.route("/trendmicro_data", methods=['GET', 'POST'])
def handletrendmicro_data():
    if request.method == 'POST':
        data_list = json.loads(request.data)
        logger.debug('this is the area of receiving infosecinstitute data............')
        for each in data_list:   
            console_db.trendmicro_insert_data(each)
        logger.debug('################################################') 
        logger.debug('all the infosecinstitute data have been inserted ')
        logger.debug('################################################')
        return jsonify({'msg':'successful.....'})


###tc260#########
@app.route("/tc260_select", methods=['GET', 'POST'])
def handletc260():
    if request.method == 'POST':
        input_dict = json.loads(request.data)
        task_owner=input_dict['task_owner']
        task_startTime=input_dict['task_startTime']##'2018-06-25 12:30:00'
        task_endTime=input_dict['task_endTime']##'2018-06-25 16:00:00'
        task_frequency = input_dict['task_frequency']## 2 minutes.
        task_crawlerId=input_dict['task_crawlerId']
        task_crawlerType=input_dict['task_crawlerType'] ## not yet to decide ......
        task_communication= input_dict['task_communication']
        task_node=input_dict['task_node'] ## this is not to be used in the location here .......

        if task_node=='SH':
            send_in_parameters={}
            send_in_parameters['task_owner']=task_owner
            send_in_parameters['task_startTime']=task_startTime##'2018-06-25 12:30:00'
            send_in_parameters['task_endTime']=task_endTime##'2018-06-25 16:00:00'
            send_in_parameters['task_frequency']=task_frequency## 2 minutes.
            send_in_parameters['task_crawlerId']=task_crawlerId
            send_in_parameters['task_crawlerType']=task_crawlerType ## not yet to decide ......
            ## https://xuanwulab.github.io/cn/secnews/
            send_in_parameters['task_node']=task_node ## this is not to be used in the location here .......
            send_in_parameters['task_communication']=task_communication

            receive=requests.post("http://xxxx:8082/tc260",data= send_in_parameters)
            logger.debug(receive.json)
            
            # ui_response = receive.data
            return jsonify({'msg':'the parameters have been sent into the second layer(Shanghai Node).......'})
        else:
            return jsonify({'msg':'this is not shanghai and we have not yet implemented other lcation .......'})


@app.route("/tc260_data", methods=['GET', 'POST'])
def handletc260_data():
    if request.method == 'POST':
        each = json.loads(request.data)
        # logger.debug(data_list)
        
        logger.debug('this is the area of receiving tc260 data............')
        # for each in data_list:   
        console_db.tc260_insert_data(each)
        logger.debug('################################################') 
        logger.debug('all the tc260 data have been inserted ')
        logger.debug('################################################')
        return jsonify({'msg':'successful.....'})

###safe_gave#########
@app.route("/safe_gave_select", methods=['GET', 'POST'])
def handlesafe_gave():
    if request.method == 'POST':
        input_dict = json.loads(request.data)
        task_owner=input_dict['task_owner']
        task_startTime=input_dict['task_startTime']##'2018-06-25 12:30:00'
        task_endTime=input_dict['task_endTime']##'2018-06-25 16:00:00'
        task_frequency = input_dict['task_frequency']## 2 minutes.
        task_crawlerId=input_dict['task_crawlerId']
        task_crawlerType=input_dict['task_crawlerType'] ## not yet to decide ......
        task_communication= input_dict['task_communication']
        task_node=input_dict['task_node'] ## this is not to be used in the location here .......

        if task_node=='SH':
            send_in_parameters={}
            send_in_parameters['task_owner']=task_owner
            send_in_parameters['task_startTime']=task_startTime##'2018-06-25 12:30:00'
            send_in_parameters['task_endTime']=task_endTime##'2018-06-25 16:00:00'
            send_in_parameters['task_frequency']=task_frequency## 2 minutes.
            send_in_parameters['task_crawlerId']=task_crawlerId
            send_in_parameters['task_crawlerType']=task_crawlerType ## not yet to decide ......
            ## https://xuanwulab.github.io/cn/secnews/
            send_in_parameters['task_node']=task_node ## this is not to be used in the location here .......
            send_in_parameters['task_communication']=task_communication

            receive=requests.post("http://xxxx:8082/safe_gave",data= send_in_parameters)
            logger.debug(receive.json)
            
            # ui_response = receive.data
            return jsonify({'msg':'the parameters have been sent into the second layer(Shanghai Node).......'})
        else:
            return jsonify({'msg':'this is not shanghai and we have not yet implemented other lcation .......'})

@app.route("/safe_gave_data", methods=['GET', 'POST'])
def handlesafe_gave_data():
    if request.method == 'POST':
        each = json.loads(request.data)
        # logger.debug(data_list)

        logger.debug('this is the area of receiving safe_gave data............')
  
        console_db.safe_gave_insert_data(each)
        logger.debug('################################################') 
        logger.debug('all the safe_gave data have been inserted ')
        logger.debug('################################################')
        return jsonify({'msg':'successful.....'})
################################### Hades Specail Area #########################################



app.secret_key = 'aHR0cDovL3d3dy53YW5kYS5jbi8='
if __name__ == '__main__':
    scheduler.remove_all_jobs()
    # default_cnvd_order()
    # default_cve_order()
    # import app
    # from werkzeug.contrib.fixers import ProxyFix
    # app.wsgi_app = ProxyFix(app.wsgi_app)
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        logger.debug(os.environ.get('WERKZEUG_RUN_MAIN'))
        print('=================== 子进程已被创造 =======================')
    initiate_default_tasks()
    scheduler.start()
    logger.debug('************************ below is information about the pending jobs ***********************************')
    logger.debug(scheduler.print_jobs())
    logger.debug(scheduler.get_jobs())
    app.run(debug=True, host="0.0.0.0", port=9000, threaded=True,use_reloader=False)