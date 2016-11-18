# weixin-api-related
weixin api related work, include "wx-api-alpha" and "dm-message-server" and "weixin-monitor" now.

##weixin-monitor

Monitor for data with Weixin notice to related workers.

###Installation

    pip install celery
   If you don't need message sent between client and server, but only Weixin message send, no need to install celery
  
###Setting

    Fill your weixin app_id, app_secret in server/conf/wx.conf
    Fill path to store access_token in server/conf/wx.conf

###Code

    Client: send message to Server through Celery
    Server: responsible for Weixin Message send,  receive mesage from client based on Celery
    
###Usage
   Start Server
    
    cd server && Celery worker -A wx_task_manager --loglevel=INFO --concurrency=2
   Run Client
   
    cd client && python client.py

##wx-api-alpha

Part functionality wrapper of Weixin API for Python

#dm-message-server

Simple Weixin response server
