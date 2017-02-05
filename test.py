#!/usr/bin/python

import urllib.request,urllib.parse,urllib

# def sendMsg(Mobile,Msg):
#     payload = {
#             'mobile':Mobile,
#             'msg':Msg
#     }
#     params = urllib.parse.urlencode(payload)
#     r = urllib.request.urlopen('http://10.102.35.130:8080/spring/sendSend.jsp?%s' % params)
# sendMsg('17769040425','python3 newnew')

# params = 'mobile=17769040425&msg=python2test1359'
# data = r.read()
# print(type(data),data)
# f = open('/tmp/sms.log','a')
# f.write(Mobile+"\n")
# f.write(Msg+"\n")
# f.close()















import json
from datetime import date
from datetime import datetime
import datetime


#
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        #if isinstance(obj, datetime):
            #return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)
#
#
# v = models.tb.objects.values('id', 'name', 'ctime')
# v = list(v)
# v = json.dumps(v, cls=JsonCustomEncoder)

import json
import datetime

a = datetime.datetime.now()
print(a)

b = json.dumps(a,cls=CJsonEncoder)
print(b)

































