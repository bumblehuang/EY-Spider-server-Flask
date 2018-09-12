#/usr/bin/env python
# -*- coding: UTF-8 -*-
import functools
import json
import os
import random
import time
import sh_logger
from flask import Flask, redirect, url_for, request, render_template, make_response, abort, jsonify, \
    send_from_directory
import sh_scrapy
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import uuid
import sys
import requests
import sh_wechat

reload(sys)
sys.setdefaultencoding('utf-8')
log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.INFO)  # DEBUG

fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)
app = Flask(__name__)
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'
# # login_manager.login_message = 'please login!'
# login_manager.session_protection = 'strong'
logger = sh_logger.get_logger(__name__)
scheduler = BackgroundScheduler()
## The variables to define the tasks status for scrapying. KEEP THEM IMMUTABLE!
WAITING= 'WAITING TO RUN'
RUNNING = 'RUNNING'
FINISHED = 'FINISHED'
PAUSED = 'PAUSED'
TERMINATED = 'TERMINATED'

## LOCATION IMMUTABLE
LOCATION = 'SH'
Job_Store={}

def go_send_it():
    sh_email.send_email()
    return jsonify({'msg':'hello it is done and email sent'})
@app.route('/kill', methods=['POST'])
def kill_shanghai():
    logger.debug(request)
    if request.method == 'POST':
        return jsonify({'h':'h'})
@app.route('/edit_task', methods=['POST'])
def edit_task():
    if request.method == 'POST':
        new_start = request.form['new_start']
        new_end = request.form['new_end']
        new_status = request.form['new_status']
        task_id = request.form['task_id']
        new_frequency = request.form['new_frequency']
        if new_status.strip() == 'TERMINATED':
            scheduler.remove_job(task_id)
        if new_status.strip() == 'PAUSED':
            scheduler.pause_job(task_id)
        if new_status.strip() == 'RESUMED':
            scheduler.resume_job(task_id)
        if new_status.strip() == 'RUNNING':
            the_very_job = scheduler.get_job(task_id)
            logger.debug(the_very_job)
            logger.debug(the_very_job.trigger)
            logger.debug(the_very_job.executor)
            logger.debug(the_very_job.next_run_time)
            logger.debug(the_very_job.name)
            logger.debug(the_very_job.args)
            logger.debug(the_very_job.func)
            logger.debug('========= above is the basic information about the job before the changes ================')
            scheduler.reschedule_job(task_id,trigger = 'interval',days = int(new_frequency) , start_date = new_start)
            logger.debug(the_very_job)
            logger.debug(the_very_job.trigger)
            logger.debug(the_very_job.executor)
            logger.debug(the_very_job.next_run_time)
            logger.debug(the_very_job.name)
            logger.debug(the_very_job.args)
            logger.debug(the_very_job.func)
        return jsonify({'msg':'successfully updated the job....'})
@app.route('/cnvd', methods=['POST'])
def order_cnvd():
    if request.method == 'POST':
        task_owner=request.form['task_owner']
        task_startTime=request.form['task_startTime']##'2018-06-25 12:30:00'
        task_endTime=request.form['task_endTime']##'2018-06-25 16:00:00'
        task_frequency = int(request.form['task_frequency'])## 2 minutes.
        task_crawlerId=request.form['task_crawlerId']
        task_crawlerType=request.form['task_crawlerType'] ## not yet to decide ......
        task_communication = request.form['task_communication']
        task_node=request.form['task_node']
        logger.debug('------------------------------------------------')
        created_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug('we are extracting parameters for the cve in the request form...........')
        if task_crawlerId == 'cnvd':
                logger.debug('we are entering the area of ordering task')
                send_out_parameters={}
                send_out_parameters['task_owner']=task_owner
                send_out_parameters['task_startTime']=task_startTime##'2018-06-25 12:30:00'
                send_out_parameters['task_endTime']=task_endTime##'2018-06-25 16:00:00'
                send_out_parameters['task_frequency']=task_frequency## 2 minutes.
                send_out_parameters['task_crawlerId']=task_crawlerId
                send_out_parameters['task_crawlerType']=task_crawlerType ## not yet to decide ......
                # send_out_parameters['task_url']=task_url ## https://xuanwulab.github.io/cn/secnews/
                send_out_parameters['task_node']=task_node ## this is not to be used in the location here .......
                send_out_parameters['task_communication']=task_communication
                send_out_parameters['created_time']=created_time
                task_id = uuid.uuid4().hex[:8]
                # scheduler.remove_job(task_id)
                send_out_parameters['task_id']=task_id
                send_out_parameters['task_name']= task_node+'-'+task_owner+'-'+str(datetime.datetime.strptime(created_time,"%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d"))+'-'+task_crawlerType
                receive=requests.post("http://cti_hk_cns00.eycyber.com:8080/insert_task",data= send_out_parameters)
                Job_Store[task_id]=1
                ##created_time,task_id,task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId,task_crawlerType,task_url,task_node,task_communication
                scheduler.add_job(do_cnvd_task,'interval', days=task_frequency,id=task_id,start_date=task_startTime,end_date=task_endTime ,args=[created_time,task_id,task_communication])
                return jsonify(send_out_parameters)
@app.route('/wechat', methods=['POST'])
def order_wechat():
    if request.method == 'POST':
        task_owner=request.form['task_owner']
        task_startTime=request.form['task_startTime']##'2018-06-25 12:30:00'
        task_endTime=request.form['task_endTime']##'2018-06-25 16:00:00'
        task_frequency = int(request.form['task_frequency'])## 2 minutes.
        task_crawlerId=request.form['task_crawlerId']
        task_crawlerType=request.form['task_crawlerType'] ## not yet to decide ......
        task_communication = request.form['task_communication']
        task_node=request.form['task_node']
        keywords = request.form['keywords']
        logger.debug('------------------------in the wechat task assignment ------------------------')
        created_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug('we are extracting parameters for the cve in the request form...........')
        if task_crawlerId == 'wechat':
                logger.debug('we are entering the area of ordering task for wechat.....')
                send_out_parameters={}
                send_out_parameters['task_owner']=task_owner
                send_out_parameters['task_startTime']=task_startTime##'2018-06-25 12:30:00'
                send_out_parameters['task_endTime']=task_endTime##'2018-06-25 16:00:00'
                send_out_parameters['task_frequency']=task_frequency## 2 minutes.
                send_out_parameters['task_crawlerId']=task_crawlerId
                send_out_parameters['task_crawlerType']=task_crawlerType ## not yet to decide ......
                # send_out_parameters['task_url']=task_url ## https://xuanwulab.github.io/cn/secnews/
                send_out_parameters['task_node']=task_node ## this is not to be used in the location here .......
                send_out_parameters['task_communication']=task_communication
                send_out_parameters['created_time']=created_time
                task_id = uuid.uuid4().hex[:8]
                # scheduler.remove_job(task_id)
                send_out_parameters['task_id']=task_id
                send_out_parameters['task_name']= task_node+'-'+task_owner+'-'+str(datetime.datetime.strptime(created_time,"%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d"))+'-'+task_crawlerType
                receive=requests.post("http://cti_hk_cns00.eycyber.com:8080/insert_task",data= send_out_parameters)
                Job_Store[task_id]=1
                ##created_time,task_id,task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId,task_crawlerType,task_url,task_node,task_communication
                scheduler.add_job(do_wechat_task,'interval', days=task_frequency,id=task_id,start_date=task_startTime,end_date=task_endTime ,args=[created_time,task_id,task_communication,keywords])
                return jsonify(send_out_parameters)
        # except Exception as e:
        #     logger.debug(e)
        #     return jsonify({'msg':'something wrong'})
@app.route('/xuanwu_sh', methods=['POST'])
def order_xuanwu():
    if request.method == 'POST':
        task_owner=request.form['task_owner']
        task_startTime=request.form['task_startTime']##'2018-06-25 12:30:00'
        task_endTime=request.form['task_endTime']##'2018-06-25 16:00:00'
        task_frequency = int(request.form['task_frequency'])## 2 minutes.
        task_crawlerId=request.form['task_crawlerId']
        task_crawlerType=request.form['task_crawlerType'] ## not yet to decide ......
        task_communication = request.form['task_communication']
        task_node=request.form['task_node']
        logger.debug('------------------------------------------------')
        created_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug('we are extracting parameters for the xuanwu in the request form...........')
        if task_crawlerId == 'xuanwu':
                logger.debug('we are entering the area of ordering task')
                send_out_parameters={}
                send_out_parameters['task_owner']=task_owner
                send_out_parameters['task_startTime']=task_startTime##'2018-06-25 12:30:00'
                send_out_parameters['task_endTime']=task_endTime##'2018-06-25 16:00:00'
                send_out_parameters['task_frequency']=task_frequency## 2 minutes.
                send_out_parameters['task_crawlerId']=task_crawlerId
                send_out_parameters['task_crawlerType']=task_crawlerType ## not yet to decide ......
                # send_out_parameters['task_url']=task_url ## https://xuanwulab.github.io/cn/secnews/
                send_out_parameters['task_node']=task_node ## this is not to be used in the location here .......
                send_out_parameters['task_communication']=task_communication
                send_out_parameters['created_time']=created_time
                task_id = uuid.uuid4().hex[:8]
                # scheduler.remove_job(task_id)
                send_out_parameters['task_id']=task_id
                send_out_parameters['task_name']= task_node+'-'+task_owner+'-'+str(datetime.datetime.strptime(created_time,"%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d"))+'-'+task_crawlerType
                receive=requests.post("http://cti_hk_cns00.eycyber.com:8080/insert_task",data= send_out_parameters)
                Job_Store[task_id]=1
                ##created_time,task_id,task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId,task_crawlerType,task_url,task_node,task_communication
                scheduler.add_job(do_xuanwu_task,'interval', days=task_frequency,id=task_id,start_date=task_startTime,end_date=task_endTime ,args=[created_time,task_id,task_communication])
                return jsonify(send_out_parameters)

def do_cnvd_task(created_time,task_id,task_communication):
    if task_id in Job_Store:
        task_sequence=Job_Store[task_id]
        Job_Store[task_id]= Job_Store[task_id]+1
    else:
        Job_Store[task_id]=1
        task_sequence=Job_Store[task_id]
    job_id=task_id+'-'+str(task_sequence)+'-'+LOCATION
    logger.debug('=================================cnvd initiated========================================')
    logger.debug(job_id)
    logger.debug('=================================cnvd initiated========================================')
    page_list = sh_scrapy.cnvd_Urlcreator(1,5,job_id,created_time)
    sh_scrapy.cnvd_scrapper(page_list,job_id,created_time,task_id)

def do_wechat_task(created_time,task_id,task_communication,keywords):
    if task_id in Job_Store:
        task_sequence=Job_Store[task_id]
        Job_Store[task_id]= Job_Store[task_id]+1
    else:
        Job_Store[task_id]=1
        task_sequence=Job_Store[task_id]
    job_id=task_id+'-'+str(task_sequence)+'-'+LOCATION
    logger.debug('================================= wechat initiated ========================================')
    logger.debug(job_id)
    logger.debug('================================= wechat initiated ========================================')
    sh_wechat.wechat_scrape(job_id,created_time,task_id,keywords)

def do_xuanwu_task(created_time,task_id,task_communication):
    if task_id in Job_Store:
        task_sequence=Job_Store[task_id]
        Job_Store[task_id]= Job_Store[task_id]+1
    else:
        Job_Store[task_id]=1
        task_sequence=Job_Store[task_id]
    job_id=task_id+'-'+str(task_sequence)+'-'+LOCATION
    logger.debug('=================================xuanwu initiated========================================')
    logger.debug(job_id)
    logger.debug('=================================xuanwu initiated========================================')
    url_page = sh_scrapy.xuanwu_Urlcreator(30)
    sh_scrapy.xuanwu_scrapper(created_time, task_id, job_id,url_page)

################################### Hades Specail Area #########################################
@app.route('/cac', methods=['POST'])
def order_cac():
    if request.method == 'POST':
        task_owner=request.form['task_owner']
        task_startTime=request.form['task_startTime']##'2018-06-25 12:30:00'
        task_endTime=request.form['task_endTime']##'2018-06-25 16:00:00'
        task_frequency = int(request.form['task_frequency'])## 2 minutes.
        task_crawlerId=request.form['task_crawlerId']
        task_crawlerType=request.form['task_crawlerType'] ## not yet to decide ......
        task_communication = request.form['task_communication']
        task_node=request.form['task_node']
        logger.debug('------------------------------------------------')
        created_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug('we are extracting parameters for the cve in the request form...........')
        if task_crawlerId == 'cac':
                logger.debug('we are entering the area of ordering task')
                send_out_parameters={}
                send_out_parameters['task_owner']=task_owner
                send_out_parameters['task_startTime']=task_startTime##'2018-06-25 12:30:00'
                send_out_parameters['task_endTime']=task_endTime##'2018-06-25 16:00:00'
                send_out_parameters['task_frequency']=task_frequency## 2 minutes.
                send_out_parameters['task_crawlerId']=task_crawlerId
                send_out_parameters['task_crawlerType']=task_crawlerType ## not yet to decide ......
                # send_out_parameters['task_url']=task_url ## https://xuanwulab.github.io/cn/secnews/
                send_out_parameters['task_node']=task_node ## this is not to be used in the location here .......
                send_out_parameters['task_communication']=task_communication
                send_out_parameters['created_time']=created_time
                task_id = uuid.uuid4().hex[:8]
                # scheduler.remove_job(task_id)
                send_out_parameters['task_id']=task_id
                send_out_parameters['task_name']= task_node+'-'+task_owner+'-'+str(datetime.datetime.strptime(created_time,"%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d"))+'-'+task_crawlerType
                receive=requests.post("http://cti_hk_cns00.eycyber.com:8080/insert_task",data= send_out_parameters)
                Job_Store[task_id]=1
                ##created_time,task_id,task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId,task_crawlerType,task_url,task_node,task_communication
                scheduler.add_job(do_cac_task,'interval', days=task_frequency,id=task_id,start_date=task_startTime,end_date=task_endTime ,args=[created_time,task_id,task_communication])
                return jsonify(send_out_parameters)


def do_cac_task(created_time,task_id,task_communication):
    if task_id in Job_Store:
        task_sequence=Job_Store[task_id]
        Job_Store[task_id]= Job_Store[task_id]+1
    else:
        Job_Store[task_id]=1
        task_sequence=Job_Store[task_id]
    job_id=task_id+'-'+str(task_sequence)+'-'+LOCATION
    logger.debug('=================================cac initiated========================================')
    logger.debug(job_id)
    logger.debug('=================================cac initiated========================================')
    sh_scrapy.cac(job_id,created_time,task_id)

################compliance
@app.route('/tc260', methods=['POST'])
def order_tc260():
    if request.method == 'POST':
        task_owner=request.form['task_owner']
        task_startTime=request.form['task_startTime']##'2018-06-25 12:30:00'
        task_endTime=request.form['task_endTime']##'2018-06-25 16:00:00'
        task_frequency = int(request.form['task_frequency'])## 2 minutes.
        task_crawlerId=request.form['task_crawlerId']
        task_crawlerType=request.form['task_crawlerType'] ## not yet to decide ......
        task_communication = request.form['task_communication']
        task_node=request.form['task_node']
        logger.debug('------------------------------------------------')
        created_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug('we are extracting parameters for the cve in the request form...........')
        if task_crawlerId == 'tc260':
                logger.debug('we are entering the area of ordering task')
                send_out_parameters={}
                send_out_parameters['task_owner']=task_owner
                send_out_parameters['task_startTime']=task_startTime##'2018-06-25 12:30:00'
                send_out_parameters['task_endTime']=task_endTime##'2018-06-25 16:00:00'
                send_out_parameters['task_frequency']=task_frequency## 2 minutes.
                send_out_parameters['task_crawlerId']=task_crawlerId
                send_out_parameters['task_crawlerType']=task_crawlerType ## not yet to decide ......
                # send_out_parameters['task_url']=task_url ## https://xuanwulab.github.io/cn/secnews/
                send_out_parameters['task_node']=task_node ## this is not to be used in the location here .......
                send_out_parameters['task_communication']=task_communication
                send_out_parameters['created_time']=created_time
                task_id = uuid.uuid4().hex[:8]
                # scheduler.remove_job(task_id)
                send_out_parameters['task_id']=task_id
                send_out_parameters['task_name']= task_node+'-'+task_owner+'-'+str(datetime.datetime.strptime(created_time,"%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d"))+'-'+task_crawlerType
                receive=requests.post("http://cti_hk_cns00.eycyber.com:8080/insert_task",data= send_out_parameters)
                Job_Store[task_id]=1
                ##created_time,task_id,task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId,task_crawlerType,task_url,task_node,task_communication
                scheduler.add_job(do_tc260_task,'interval', days=task_frequency,id=task_id,start_date=task_startTime,end_date=task_endTime ,args=[created_time,task_id,task_communication])
                return jsonify(send_out_parameters)


def do_tc260_task(created_time,task_id,task_communication):
    if task_id in Job_Store:
        task_sequence=Job_Store[task_id]
        Job_Store[task_id]= Job_Store[task_id]+1
    else:
        Job_Store[task_id]=1
        task_sequence=Job_Store[task_id]
    job_id=task_id+'-'+str(task_sequence)+'-'+LOCATION
    logger.debug('=================================tc260 initiated========================================')
    logger.debug(job_id)
    logger.debug('=================================tc260 initiated========================================')
    
    url_page = sh_scrapy.tc260_Urlcreator(1,2,job_id,created_time,task_id)
    sh_scrapy.tc260_scrapper(url_page,job_id,created_time,task_id)

@app.route('/safe_gave', methods=['POST'])
def order_safe_gave():
    if request.method == 'POST':
        task_owner=request.form['task_owner']
        task_startTime=request.form['task_startTime']##'2018-06-25 12:30:00'
        task_endTime=request.form['task_endTime']##'2018-06-25 16:00:00'
        task_frequency = int(request.form['task_frequency'])## 2 minutes.
        task_crawlerId=request.form['task_crawlerId']
        task_crawlerType=request.form['task_crawlerType'] ## not yet to decide ......
        task_communication = request.form['task_communication']
        task_node=request.form['task_node']
        logger.debug('------------------------------------------------')
        created_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug('we are extracting parameters for the cve in the request form...........')
        if task_crawlerId == 'safe_gave':
                logger.debug('we are entering the area of ordering task')
                send_out_parameters={}
                send_out_parameters['task_owner']=task_owner
                send_out_parameters['task_startTime']=task_startTime##'2018-06-25 12:30:00'
                send_out_parameters['task_endTime']=task_endTime##'2018-06-25 16:00:00'
                send_out_parameters['task_frequency']=task_frequency## 2 minutes.
                send_out_parameters['task_crawlerId']=task_crawlerId
                send_out_parameters['task_crawlerType']=task_crawlerType ## not yet to decide ......
                # send_out_parameters['task_url']=task_url ## https://xuanwulab.github.io/cn/secnews/
                send_out_parameters['task_node']=task_node ## this is not to be used in the location here .......
                send_out_parameters['task_communication']=task_communication
                send_out_parameters['created_time']=created_time
                task_id = uuid.uuid4().hex[:8]
                # scheduler.remove_job(task_id)
                send_out_parameters['task_id']=task_id
                send_out_parameters['task_name']= task_node+'-'+task_owner+'-'+str(datetime.datetime.strptime(created_time,"%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d"))+'-'+task_crawlerType
                receive=requests.post("http://cti_hk_cns00.eycyber.com:8080/insert_task",data= send_out_parameters)
                Job_Store[task_id]=1
                ##created_time,task_id,task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId,task_crawlerType,task_url,task_node,task_communication
                scheduler.add_job(do_safe_gave_task,'interval', days=task_frequency,id=task_id,start_date=task_startTime,end_date=task_endTime ,args=[created_time,task_id,task_communication])
                return jsonify(send_out_parameters)


def do_safe_gave_task(created_time,task_id,task_communication):
    if task_id in Job_Store:
        task_sequence=Job_Store[task_id]
        Job_Store[task_id]= Job_Store[task_id]+1
    else:
        Job_Store[task_id]=1
        task_sequence=Job_Store[task_id]
    job_id=task_id+'-'+str(task_sequence)+'-'+LOCATION
    logger.debug('=================================safe_gave initiated========================================')
    logger.debug(job_id)
    logger.debug('=================================safe_gave initiated========================================')
    
    url_page = sh_scrapy.save_gove_Urlcreator(1,2)
    sh_scrapy.save_gove_scrapper(url_page,job_id,created_time,task_id)
################################### Hades Specail Area #########################################
if __name__ == '__main__':
    # print(type(flask_db.get_user('admin')))
    # print(flask_db.get_user('admin'))
    # scheduler = BackgroundScheduler()
    scheduler.start()
    app.run(port=9000,threaded=True)
    
