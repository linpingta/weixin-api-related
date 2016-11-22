#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
import hashlib
import time
from lxml import etree

from forms import WatchContentForm, TaskContentForm


token = 'xiaozhi'


def parseMsgXml(rootElem):
    msg = {}
    if rootElem.tag == 'xml':
        for child in rootElem:
            msg[child.tag] = smart_str(child.text)
    return msg

def getReplyXml(msg, reply_content):
    extTpl = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>";
    extTpl = extTpl % (msg['FromUserName'],msg['ToUserName'],str(int(time.time())),'text',reply_content)
    return extTpl


@csrf_exempt
def index(request):
    if request.method == 'GET':
	signature = request.GET.get('signature', None)
	timestamp = request.GET.get('timestamp', None)
	nonce = request.GET.get('nonce', None)
	echostr = request.GET.get('echostr', None)
	check_list = [token, timestamp, nonce]
	check_list.sort()
	checkstr = '%s%s%s' % tuple(check_list)
	if hashlib.sha1(checkstr).hexdigest() == signature:
	    return HttpResponse(echostr)
	else:
	    return HttpResponse('fail')
    else:
        xml_str = smart_str(request.body)
	request_xml = etree.fromstring(xml_str)

	msg = parseMsgXml(request_xml)
	print msg
	if 'EventKey' in msg:
	    event_key = msg['EventKey']
	    if event_key == 'd3_about_us':
		reply_content = u'd3,出海广告平台,还有很多很多'
	    else:
	    	reply_content = u'd3投放系统\n1.analyse->account: 账户分析\n2.analyse->campaign: 活动分析\n3.analyse->creative: 创意分析\n4.setting->about：了解d3\n5.setting->watch：设置默认消息类型\n6.setting->task: 自定义消息类型'
	else:
	    reply_content = u'd3投放系统\n1.analyse->account: 账户分析\n2.analyse->campaign: 活动分析\n3.analyse->creative: 创意分析\n4.setting->about：了解d3\n5.setting->watch：设置默认消息类型\n6.setting->task: 自定义消息类型'

	response_msg = getReplyXml(msg, reply_content)
	return HttpResponse(response_msg)

def watch_index(request):
    # mock data
    watches = []
    watches.append({'title':'账户余额', 'valid':1})
    watches.append({'title':'创意据登', 'valid':1})
    watches.append({'title':'频率控制', 'valid':0})
    watches.append({'title':'其它监控', 'valid':0})

    context = { 'watches':watches }
    return render(request, 'message/watch_index.html', context=context)

def watch_edit(request):
    if request.method == 'POST':
	watch_content_form = WatchContentForm(request.POST)
	if watch_content_form.is_valid():
	    return HttpResponseRedirect('/watch_index/')
    else:
	watch_content_form = WatchContentForm()

    return render(request, 'message/watch_edit.html', {'watch_content_form' : watch_content_form})

def task_index(request):
    # mock tasks
    task_infos = []
    task_infos.append({'id':1, 'name':'campaign_组监控', 'ad_type':'campaign', 'condition':'123, 456', 'roi':'-10', 'check_type':'daily'})
    task_infos.append({'id':2, 'name':'account_组监控', 'ad_type':'account', 'condition':'1234, 2345', 'roi':'-20', 'check_type':'daily'})
    task_infos.append({'id':3, 'name':'我的监控', 'ad_type':'campaign', 'condition':'', 'roi':'-10', 'check_type':'lifetime'})

    context = { 'task_infos':task_infos }
    return render(request, 'message/task_index.html', context=context)

def task_create(request):
    if request.method == 'POST':
	task_content_form = TaskContentForm(request.POST)
	if task_content_form.is_valid():
	    new_task_id = 4
	    return HttpResponseRedirect('/task_detail/%s' % new_task_id)
    else:
	task_content_form = TaskContentForm()

    return render(request, 'message/task_create.html', {'task_content_form' : task_content_form})

def task_delete(request, task_id):
    # do real work here
    return HttpResponseRedirect('/task_index/')

def task_detail(request, task_id):
    task = {'id':1, 'name':'campaign_组监控', 'ad_type':'campaign', 'condition':'123, 456', 'roi':'-10', 'check_type':'daily'}
    task['id'] = int(task_id)

    return render(request, 'message/task_detail.html', {'task': task})

def task_edit(request, task_id):
    task = {}
    task['id'] = task_id
    if request.method == 'POST':
	task_content_form = TaskContentForm(request.POST)
	if task_content_form.is_valid():
	    new_task_id = 3
	    return HttpResponseRedirect('/task_detail/%d' % int(new_task_id))
    else:
	# get info from db
	content_dict = {
	    'name' : 'campaign_组监控',
	    'ad_type': '1',
	    'condition': '123, 456',
	    'roi': '-10',
	    'check_type': '1',
	}
	task_content_form = TaskContentForm(content_dict)

    return render(request, 'message/task_edit.html', {'task_content_form' : task_content_form, 'task' : task})
