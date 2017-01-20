from django.shortcuts import render,HttpResponse,redirect

# Create your views here.

from django import forms
import json,re,time,datetime
from chouti01 import models
from django.forms.utils import ErrorDict
from django.core.exceptions import ValidationError
from backend import sendMsg, commons, randomcode


global logineduser
logineduser = ''


def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')


class PhoneLoginForm(forms.Form):
    mobile = forms.CharField(validators=[mobile_validate, ],
                            error_messages={'required': u'手机不能为空'},)
    loginpwd = forms.CharField(min_length=8,max_length=15,error_messages={'required':'不能为空','min_length':'最小长度是6','max_length':'最大长度是15'})

class UserLoginForm(forms.Form):
    userid = forms.CharField(min_length=8, max_length=15,error_messages={'required': '不能为空', 'min_length': '最小长度是8', 'max_length': '最大长度是15'})
    loginpwd = forms.CharField(min_length=6, max_length=15,
                               error_messages={'required': '不能为空', 'min_length': '最小长度是6', 'max_length': '最大长度是15'})

class UserRegisterForm(forms.Form):
    registermobile = forms.CharField(validators=[mobile_validate, ],
                            error_messages={'required': u'手机不能为空'},)
    registerpwd = forms.CharField(min_length=8,max_length=15,error_messages={'required':'不能为空','min_length':'最小长度是6','max_length':'最大长度是15'})

def login(request):
    if request.method == 'POST':
        ret = commons.BaseResponse()
# keeploginvalue=1,store session;
        keeploginvalue = request.POST.get('keeploginvalue')
        keeploginvalueInt = int(keeploginvalue)
        login_choice = request.POST.get('login_choice')
        if login_choice == 'phoneLogin':
            current_time = datetime.datetime.now()
            limit_time = current_time - datetime.timedelta(minutes=15)
            username = request.POST.get('mobile')
            password = request.POST.get('loginpwd')
            phone_count = models.login_failed.objects.filter(phone=username).count()
            if not phone_count:
                models.login_failed.objects.create(phone=username,username='',password='',ctime=current_time,times=0)
            # limit_count = models.login_failed.objects.filter(phone=username).update(times=0)
            limit_count = models.login_failed.objects.filter(phone=username,ctime__gt=limit_time,times__gt=2).count()

            if limit_count:
                ret.summary = '您输入的过于频繁，请15分钟后再试'
                return HttpResponse(json.dumps(ret.__dict__))
            else:
                gt_limit_time_count = models.login_failed.objects.filter(phone=username,ctime__lt=limit_time).count()
                if gt_limit_time_count:
                    models.login_failed.objects.filter(phone=username).update(ctime=current_time,times=0)
                from django.db.models import F
                models.login_failed.objects.filter(phone=username).update(ctime=current_time,times=F('times') + 1)
                # ret.status = 'True'

            phoneusercount = models.UserInfo.objects.filter(phone=username,password=password).count()
            if phoneusercount:
                ret.status = 'True'
                request.session['is_login'] = True
                userobj = models.UserInfo.objects.filter(phone=username).all().first()
                user_info = {'username': userobj.username, 'password': userobj.password, 'phone': userobj.phone,'nid':userobj.nid}
                request.session['user_info'] = user_info
                models.login_failed.objects.filter(phone=username).delete()
            else:
                ret.summary = '手机号或密码错误'
                print(ret.__dict__)
                return HttpResponse(json.dumps(ret.__dict__))
        # elif login_choice == 'userLogin':
        #     pass
            # LDAP authentication.
            # username = eval(json.dumps(request.POST))['userid']
            # password = eval(json.dumps(request.POST))['loginpwd']
            # obj = UserLoginForm(request.POST)
            # ret = obj.is_valid()
        print(ret.__dict__)
        return HttpResponse(json.dumps(ret.__dict__))

    return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        phoneval = request.POST.get('registermobile')
        registerpwd = request.POST.get('registerpwd')
        mbcd = request.POST.get('mbcd').upper()
        # print(type(registermobile),type(registerpwd),type(mbcd),registermobile,registerpwd,mbcd)
        ret = commons.BaseResponse()
        obj = UserRegisterForm(request.POST)
        form_ret = obj.is_valid()
        if form_ret:
            current_time = datetime.datetime.now()
            limit_time = current_time - datetime.timedelta(minutes=1)
            codetime = models.SendMsg.objects.filter(phone=phoneval,ctime__lt=limit_time).count()
            if codetime:
                ret.summary = '您输入的验证码已过期，请在5分钟内使用'
                return HttpResponse(json.dumps(ret.__dict__))
            else:
                codecount = models.SendMsg.objects.filter(code=mbcd).count()
                if codecount:
                    ret.status = 'True'
                    print(type(current_time),current_time)
                    store_user_info = {'username':'','password':registerpwd,'phone':phoneval,'ctime':current_time}
                    userobj = models.UserInfo.objects.create(**store_user_info)
                    models.SendMsg.objects.filter(phone=phoneval).delete()
                    request.session['is_login'] = True
                    user_info = {'username': userobj.username, 'password': userobj.password, 'phone': userobj.phone,'nid':userobj.nid}
                    request.session['user_info'] = user_info
                    ret.status = 'True'
                else:
                    ret.summary = '验证码错误'
        else:
            print('django lll')

        return HttpResponse(json.dumps(ret.__dict__))

def auth(func):
    def inner(request,*args,**kwargs):
        user = request.session.get('user_info',None)
        if not user:
            return redirect('/login/')
        return func(request,*args,**kwargs)
    return inner

@auth
def index(request):
    global logineduser
    user = request.session.get('user_info')['username']
    if not user:
        phoneuser = request.session.get('user_info')['phone']
        return render(request, 'index.html', {'logineduser': phoneuser})
    return render(request, 'index.html', {'logineduser': user})

def logout(request):
    request.session.clear()
    return redirect('/login/')

def getmbcode(request):


    ret = commons.BaseResponse()
    if request.method == 'POST':
        phoneval = request.POST.get('phoneval')

        phone_is_used = models.UserInfo.objects.filter(phone=phoneval).count()
        # models.UserInfo.objects.filter(phone=phoneval).delete()
        # return HttpResponse(json.dumps(ret.__dict__))
        if phone_is_used:
            ret.summary = '该手机号已被注册'
            return HttpResponse(json.dumps(ret.__dict__))

        current_time = datetime.datetime.now()
        random_code = randomcode.random_code()

        smg_count = models.SendMsg.objects.filter(phone=phoneval).count()
        if not smg_count:
            models.SendMsg.objects.create(phone=phoneval,code=random_code,ctime=current_time)
            ret.status='True'
        else:
            limit_time = current_time - datetime.timedelta(minutes=15)
            # models.SendMsg.objects.filter(phone=phoneval).update(ctime=limit_time,times=0)
            chaoshicount = models.SendMsg.objects.filter(phone=phoneval,ctime__gt=limit_time,times__gt=9).count()
            if chaoshicount:
                ret.summary = '已超过最大次数（10），请15分钟后再试'
            else:
                orreset = models.SendMsg.objects.filter(phone=phoneval,ctime__lt=limit_time).count()
                if orreset:
                    models.SendMsg.objects.update(times=0)
                from django.db.models import F
                models.SendMsg.objects.filter(phone=phoneval).update(code=random_code,ctime=current_time,times=F('times')+1)
                ret.status = 'True'
        if ret.status:
            sendMsg.sendMsg(phoneval,random_code)
        return HttpResponse(json.dumps(ret.__dict__))


def urlpublish(request):
    if request.method == 'POST':
        ret = commons.BaseResponse()
        getbiaoti = request.POST.get('biaoti',None)
        getlianjie = request.POST.get('lianjie',None)
        getcaption = request.POST.get('caption',None)
        getphone = request.POST.get('phone',None)
        getzhaiyao = request.POST.get('zhaiyao',None)

        phoneid = models.UserInfo.objects.get(phone=getphone).nid
        newtypeid = models.NewsType.objects.get(caption=getcaption).nid
        current_time = datetime.datetime.now()
        models.News.objects.create(user_info_id=phoneid,news_type_id=newtypeid,title=getbiaoti,url=getlianjie,content=getzhaiyao,ctime=current_time)
        a = models.News.objects.all().values_list()
        print(a)
        ret.status = 'True'
        return HttpResponse(json.dumps(ret.__dict__))







