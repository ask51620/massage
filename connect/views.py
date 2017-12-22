### -*- coding: utf-8 -*-
##from __future__ import unicode_literals
##
##from django.shortcuts import render
##from django.http import HttpResponse
##import requests
### Create your views here.
##
##def connect(request):
##    if request.GET:
##        return HttpResponse(request.GET['hub.challenge'])
##    if request.POST:
####        print request.POST
##        print 1
####        print request
####        return HttpResponse('123')



from django.http import HttpResponse
from django.views.static import serve
import os
import json
import urllib2
import requests
from datetime import datetime, timedelta
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#from django.core.mail import send_mail

# for ssl file from sslforfree.com
token='EAATYBb2RdNwBACobRUZACRhfON2rJYxDRwuT4RyPVZAC48TBhHDiZBRtdTYAZBP6tBuxLJIfEsadg1IY0HDeuc9py0YFm5bCA80UA5lZAemG9E6ZBEhe9emFeNtUTvohRk7muZC7vhxCjxTLMQOVrSIrNEvzg3mMY0206m3eh1iouDaSwDnJZCIp'
content_text = {}
def send_ssl_file(request):
    filepath = 'FILEPATH'
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

class fb_webhook(generic.View):
    global content_text
    def __init__(self):
        self.content_text = {}

    def TRA_seach(self, text):
#        print 1092
        headers = {'content-type': 'application/json',
                       'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
#        print 1093
        if type(text) !=list:
#            print 1094
            url = "https://ptx.transportdata.tw/MOTC/v2/Rail/TRA/Station?$filter=contains(StationName/Zh_tw,'%s')&$format=JSON" %urllib2.quote(text.encode('utf-8'))
            content = requests.get(url, headers=headers)
#            print 1095, content.content
            try:
                a = eval(content.content)
                return a[0]['StationID']
            except:
                return False

        else:
#            print 1096, text
            url ='https://ptx.transportdata.tw/MOTC/v2/Rail/TRA/DailyTimetable/OD/%s/to/%s/%s?$orderby=OriginStopTime/ArrivalTime asc' %(text[0], text[1], text[2])
#            print url
            content = requests.get(url, headers=headers)
#            print 1097
            try:
                a = eval(content.content.replace('null', '""').replace('true', 'True').replace('false', 'False'))
                return a
            except:
                return False


    def get(self, request, *args, **kwargs):
        # 處理FB認證
        verification_code = 'tap51620'
        verify_token = request.GET.get('hub.verify_token')
        if verification_code == verify_token:

            return HttpResponse(request.GET.get('hub.challenge'))
        return HttpResponse("NOT VALID")

    def init_content(self, send_id):
#        print 104
        if send_id not in  content_text:
#            print 1041
            self.content_text[send_id] = {'content':{},'Time':datetime.now().strftime('%Y%m%d%H%M')}
#            print 1042
        else:
#            print 1043,content_text[send_id]
            if datetime.strptime(content_text[send_id]['Time'],'%Y%m%d%H%M')<=(datetime.now()+timedelta(minutes = 5)):
#                print 104
                self.content_text[send_id] = {'content':content_text[send_id]['content'] ,'Time':datetime.now().strftime('%Y%m%d%H%M')}
            else:
                self.content_text[send_id] = {'content':{},'Time':datetime.now().strftime('%Y%m%d%H%M')}
#        print 105

    def return_content(self, send_id, text):
#        print 106,u'火車' in text
#        print text
#        retext = ''
        if u'測試用text_ask5162010024:' in text:
            retext = eval(text.split('測試用text_ask5162010024:')[-1])
            print retext
            return retext

        if ((u'火車' in text) or (u'台鐵' in text) or (u'臺鐵' in text)) and ((u'時刻' in text) or (u'時間' in text) or (u'查詢' in text)):
#            print 107
            self.content_text[send_id]['content'] = {'train_time_cheack':[]}
            retext = u'請問您的起始站為?'
        else:
#            print 108
            if 'train_time_cheack' in self.content_text[send_id]['content']:
                step = len(self.content_text[send_id]['content']['train_time_cheack'])
                tes = True
#                print 109
                if step==0:
#                    print 1091
                    tes = self.TRA_seach(text)
                    if tes:
                        self.content_text[send_id]['content']['train_time_cheack'].append(tes)
                        retext = u'請問您的終點站為?'
                    else:
                        retext = u'車站輸入錯誤，離開查詢系統'
                        self.content_text[send_id] = {'content':{},'Time':datetime.now().strftime('%Y%m%d%H%M')}
                if step==1:
                    tes = self.TRA_seach(text)
                    if tes:
                        self.content_text[send_id]['content']['train_time_cheack'].append(tes)
                        retext = u'請問您的出發時間為?(yyyy-mm-dd)'
                    else:
                        retext = u'車站輸入錯誤，離開查詢系統'
                        self.content_text[send_id] = {'content':{},'Time':datetime.now().strftime('%Y%m%d%H%M')}
                if step==2:
#                    print 1092
                    self.content_text[send_id]['content']['train_time_cheack'].append(text)
                    tes = self.TRA_seach(self.content_text[send_id]['content']['train_time_cheack'])
                    if tes:
#                        print 1093
                        retext =[u'車號\t\t車種\t\t到站時間\t\t出發時間\n']

                        for a in tes:
#                            print a['DailyTrainInfo']['TrainNo'], a['DailyTrainInfo']['TrainTypeName']['Zh_tw'].decode('utf-8'), a['DestinationStopTime']['ArrivalTime'], a['DestinationStopTime']['DepartureTime']
                            retext.append(u'%s\t\t%s\t\t%s\t\t%s\n'%(a['DailyTrainInfo']['TrainNo'], a['DailyTrainInfo']['TrainTypeName']['Zh_tw'].decode('utf-8').split(u'(')[0],
                            a['DestinationStopTime']['ArrivalTime'], a['DestinationStopTime']['DepartureTime']))
                        self.content_text[send_id] = {'content':{},'Time':datetime.now().strftime('%Y%m%d%H%M')}

                    else:
                        retext = u'時間輸入錯誤，離開查詢系統'
#                print 110
            else:
                retext = u'您發送的訊息為:'+text
                self.content_text[send_id] = {'content':{},'Time':datetime.now().strftime('%Y%m%d%H%M')}
        content_text[send_id] = self.content_text[send_id]
#        print 111, retext
        return retext

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        url = "https://graph.facebook.com/v2.6/me/subscribed_apps?access_token=%s" %token
        msg = self.request.body.decode('utf-8')
        # 下三行有處理中文編碼問題
        msg = json.dumps(msg, ensure_ascii=False)
        incoming_message = json.loads(msg, encoding="utf-8")
        incoming_message = json.loads(incoming_message, encoding="utf-8")
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
#        print incoming_message

        if 'entry' in incoming_message:
#            print 12
            if 'id' in incoming_message['entry'][0]:
#                print 2
#                print 'id:',incoming_message['entry'][0]['id']
                if incoming_message['entry'][0]['id'] ==u'0':
#                    print 3
                    content = requests.post(url)
#                    print content.text

##                elif 'messaging' in incoming_message['entry']:
                else :

#                    print 101,incoming_message['entry']
                    for entry in incoming_message['entry']:
#                        print entry
                        if 'messaging' in entry:
                            for message in entry['messaging']:
#                                print message
                                if 'message' in message:
                                    if 'text' in message['message']:
#                                        print 102, message['message']['text']
                                        try:
                                            text = message['message']['text'].encode('utf-8')
                                        except:
                                            text = message['message']['text']
#                                        print 103
                                        self.init_content(message['sender']['id'])
                                        text = self.return_content(message['sender']['id'], text.replace('台','臺'))
#                                        print 112, message['sender']['id'], text
                                        if type(text)!=list:
                                            send_message(message['sender']['id'], text)
                                        else:
                                            for i in text:
#                                                print 113
                                                send_message(message['sender']['id'], i)
#                                        print 114
##        for entry in incoming_message['entry']:
##            for message in entry['messaging']:
##                # 判別接收的訊息是文字(有可能會收到檔案或者sticker)
##                if message.get("message") and 'text' in message['message']:
##                    text = message['message']['text'].encode('utf-8')
##                    if text == ("中文字").encode("utf-8"):
##                        send_simple_message(message['sender']['id'], message['message']['text'])
##                    else:
##                        send_message_with_timestamp_and_email(message['sender']['id'], message['message']['text'], message['timestamp'])
##                else:
##                    return HttpResponse()
        return HttpResponse()

def send_message(to_fb_id, message):
#    print 11
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%token
#    print 12
    response_msg = json.dumps({"recipient":{"id":to_fb_id}, "message":{"text":message}})
#    print 13
    Send = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
#    print 14
##  print Send

def certificate(request):
    test='''<a target="_blank" href="http://privacypolicies.com/privacy/view/ls6Lot">Privacy policy</a>'''
    return HttpResponse(test)