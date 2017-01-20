#!/usr/bin/python

import urllib.request,urllib.parse,urllib

def sendMsg(Mobile,Msg):
    payload = {
            'mobile':Mobile,
            'msg':Msg
    }
    params = urllib.parse.urlencode(payload)
    r = urllib.request.urlopen('http://10.102.35.130:8080/spring/sendSend.jsp?%s' % params)


# params = 'mobile=17769040425&msg=python2test1359'
# data = r.read()
# print(type(data),data)
# f = open('/tmp/sms.log','a')
# f.write(Mobile+"\n")
# f.write(Msg+"\n")
# f.close()