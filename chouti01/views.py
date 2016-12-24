from django.shortcuts import render,HttpResponse,redirect

# Create your views here.

from django import forms
import json,re
from chouti01 import models
from django.forms.utils import ErrorDict
from django.core.exceptions import ValidationError

def index(request):
    print('333')
    return render(request,'index.html')


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
        result = {'status':False,'message':''};
        login_choice = eval(json.dumps(request.POST))['login_choice']
        if login_choice == 'phoneLogin':
            username = eval(json.dumps(request.POST))['mobile']
            password = eval(json.dumps(request.POST))['loginpwd']
            obj = PhoneLoginForm(request.POST)
            ret = obj.is_valid()
        elif login_choice == 'userLogin':
            username = eval(json.dumps(request.POST))['userid']
            password = eval(json.dumps(request.POST))['loginpwd']
            obj = UserLoginForm(request.POST)
            ret = obj.is_valid()
        if ret:
            if login_choice == 'phoneLogin':
                mobile_num = models.UserInfo.objects.filter(phone=username).count()
                if mobile_num <= 0:
                    result['message'] = {'loginErrorMessage': [{'phonelogin': 'noTheUser', 'message': '该手机尚未注册'}]}
                else:
                    pwd_sql = models.UserInfo.objects.filter(phone=username).values_list('pwd').first()[0]
                    if password == pwd_sql:
                        result['status'] = True
                        # loginedUser = username
                        # print('234')
                        # return render(request,'index.html',{'loginedUser':loginedUser})
                        # return redirect('/index/')
                    else:
                        result['message'] = {'loginErrorMessage': [{'phonelogin': 'noTheUser', 'message': '手机号或密码错误'}]}

            elif login_choice == 'userLogin':
                user_num = models.UserInfo.objects.filter(name=username).count()
                if user_num <= 0:
                    result['message'] = {'loginErrorMessage': [{'phonelogin': 'noTheUser', 'message': '该用户尚未注册'}]}
                else:

                    pwd_sql = models.UserInfo.objects.filter(user=username).values_list('pwd').first()[0]
                    if password == pwd_sql:
                        result['status'] = True
                    else:
                        result['message'] = {'loginErrorMessage': [{'phonelogin': 'noTheUser', 'message': '用户名或密码错误'}]}
        else:
            result['message'] = json.loads(obj.errors.as_json())

        return HttpResponse(json.dumps(result))

    return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        registermobile = eval(json.dumps(request.POST))['registermobile']
        registerpwd = eval(json.dumps(request.POST))['registerpwd']
        result = {'status': False, 'message': ''};
        obj = UserRegisterForm(request.POST)
        ret = obj.is_valid()
        mobile_num = models.UserInfo.objects.filter(phone=registermobile).count()
        if ret and mobile_num == 0:
            print('1');
            result['status'] = True
            models.UserInfo.objects.create(phone=registermobile, pwd=registerpwd)
        elif ret and mobile_num != 0:
            print('2');
            result['status'] = False
            result['message'] = {'thePhoneIsUsed': [{'register': 'phoneIsUsed', 'message': '该手机号已注册'}]}
        else:
            print(json.loads(obj.errors.as_json()))
            result['message'] = json.loads(obj.errors.as_json())

        return HttpResponse(json.dumps(result))



