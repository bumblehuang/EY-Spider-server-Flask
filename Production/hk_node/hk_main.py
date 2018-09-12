#/usr/bin/env python
# -*- coding: UTF-8 -*-
import functools
import json
import os
import random
import time
import hk_logger
from flask import Flask, redirect, url_for, request, render_template, make_response, abort, jsonify, \
    send_from_directory
import hk_scrapy
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import uuid
import sys
import requests
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
logger = hk_logger.get_logger(__name__)
scheduler = BackgroundScheduler()
## The variables to define the tasks status for scrapying. KEEP THEM IMMUTABLE!
WAITING= 'WAITING TO RUN'
RUNNING = 'RUNNING'
FINISHED = 'FINISHED'
PAUSED = 'PAUSED'
TERMINATED = 'TERMINATED'

## LOCATION IMMUTABLE
LOCATION = 'HK'
Job_Store={}

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

@app.route('/cve_order', methods=['POST'])
def order_cve():
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
        if task_crawlerId == 'cve':
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
                receive=requests.post("http://cti_hk_cns00.int.eycyber.com:8080/insert_task",data= send_out_parameters)
                Job_Store[task_id]=1
                ##created_time,task_id,task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId,task_crawlerType,task_url,task_node,task_communication
                scheduler.add_job(do_cve_task,'interval', days=task_frequency,id=task_id,start_date=task_startTime,args=[created_time,task_id,task_communication])
                return jsonify(send_out_parameters)
def do_cve_task(created_time,task_id,task_communication):
    if task_id in Job_Store:
        task_sequence=Job_Store[task_id]
        Job_Store[task_id]= Job_Store[task_id]+1 
    else:
        Job_Store[task_id]=1
        task_sequence=Job_Store[task_id]
    job_id=task_id+'-'+str(task_sequence)+'-'+LOCATION
    logger.debug('=================================cve initiated========================================')
    logger.debug(job_id)
    logger.debug('=================================cve initiated========================================')
    first_list = hk_scrapy.cve_Urlcreator(0,0,0,0,0,1,50)
    hk_scrapy.cve_scrapper(first_list,job_id,created_time,task_id)

################################### Hades Specail Area #########################################

@app.route('/cisco_order', methods=['POST'])
def order_cisco():
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
        logger.debug('we are extracting parameters for the cisco in the request form...........')
        if task_crawlerId == 'cisco':
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
                receive=requests.post("http://cti_hk_cns00.int.eycyber.com:8080/insert_task",data= send_out_parameters)
                Job_Store[task_id]=1
                ##created_time,task_id,task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId,task_crawlerType,task_url,task_node,task_communication
                scheduler.add_job(do_cisco_task,'interval', days=task_frequency,id=task_id,start_date=task_startTime,args=[created_time,task_id,task_communication])
                return jsonify(send_out_parameters)
                
def do_cisco_task(created_time,task_id,task_communication):
    if task_id in Job_Store:
        task_sequence=Job_Store[task_id]
        Job_Store[task_id]= Job_Store[task_id]+1 
    else:
        Job_Store[task_id]=1
        task_sequence=Job_Store[task_id]
    job_id=task_id+'-'+str(task_sequence)+'-'+LOCATION
    logger.debug('=================================cisco initiated========================================')
    logger.debug(job_id)
    logger.debug('=================================cisco initiated========================================')
    url_page_list = hk_scrapy.cisco_Urlcreator(1,5,job_id,created_time,task_id)
    hk_scrapy.cisco_scrapper(url_page_list,job_id,created_time,task_id)


@app.route('/infosecinstitute', methods=['POST'])
def order_infosecinstitute():
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
        logger.debug('we are extracting parameters for the infosecinstitute in the request form...........')
        if task_crawlerId == 'infosecinstitute':
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
                receive=requests.post("http://cti_hk_cns00.int.eycyber.com:8080/insert_task",data= send_out_parameters)
                Job_Store[task_id]=1
                ##created_time,task_id,task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId,task_crawlerType,task_url,task_node,task_communication
                scheduler.add_job(do_infosecinstitute_task,'interval', days=task_frequency,id=task_id,start_date=task_startTime,args=[created_time,task_id,task_communication])
                return jsonify(send_out_parameters)
def do_infosecinstitute_task(created_time,task_id,task_communication):
    if task_id in Job_Store:
        task_sequence=Job_Store[task_id]
        Job_Store[task_id]= Job_Store[task_id]+1 
    else:
        Job_Store[task_id]=1
        task_sequence=Job_Store[task_id]
    job_id=task_id+'-'+str(task_sequence)+'-'+LOCATION
    logger.debug('=================================infosecinstitute initiated========================================')
    logger.debug(job_id)
    logger.debug('=================================infosecinstitute initiated========================================')
    
    hk_scrapy.infosecinstitute(job_id,created_time,task_id)

@app.route('/trendmicro', methods=['POST'])
def order_trendmicro():
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
        logger.debug('we are extracting parameters for the infosecinstitute in the request form...........')
        if task_crawlerId == 'trendmicro':
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
                receive=requests.post("http://cti_hk_cns00.int.eycyber.com:8080/insert_task",data= send_out_parameters)
                Job_Store[task_id]=1
                ##created_time,task_id,task_owner,task_startTime,task_endTime,task_frequency,task_crawlerId,task_crawlerType,task_url,task_node,task_communication
                scheduler.add_job(do_trendmicro_task,'interval', days=task_frequency,id=task_id,start_date=task_startTime,args=[created_time,task_id,task_communication])
                return jsonify(send_out_parameters)
def do_trendmicro_task(created_time,task_id,task_communication):
    if task_id in Job_Store:
        task_sequence=Job_Store[task_id]
        Job_Store[task_id]= Job_Store[task_id]+1 
    else:
        Job_Store[task_id]=1
        task_sequence=Job_Store[task_id]
    job_id=task_id+'-'+str(task_sequence)+'-'+LOCATION
    logger.debug('=================================trendmicro initiated========================================')
    logger.debug(job_id)
    logger.debug('=================================trendmicro initiated========================================')
    url_page = hk_scrapy.trendmicro_Urlcreator(1, 50)
    hk_scrapy.trendmicro_scrapper(url_page,job_id,created_time,task_id)
    
################################### Hades Specail Area #########################################
if __name__ == '__main__':
    # print(type(flask_db.get_user('admin')))
    # print(flask_db.get_user('admin'))
    # scheduler = BackgroundScheduler()
    scheduler.start()
    app.run(port=9000,threaded=True)
    
