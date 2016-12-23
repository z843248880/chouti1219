from django.shortcuts import render,HttpResponse

# Create your views here.

from django import forms
import json,re
from chouti01 import models
from django.forms.utils import ErrorDict
from django.core.exceptions import ValidationError

def index(request):
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
    registerpwd = forms.CharField(min_length=6,max_length=15,error_messages={'required':'不能为空','min_length':'最小长度是6','max_length':'最大长度是15'})

def login(request):
    if request.method == 'POST':
        result = {'status':False,'message':''};
        login_choice = eval(json.dumps(request.POST))['login_choice']
        if login_choice == 'phoneLogin':

            obj = PhoneLoginForm(request.POST)
            print(request.POST)
            ret = obj.is_valid()
        elif login_choice == 'userLogin':
            obj = UserLoginForm(request.POST)
            ret = obj.is_valid()
        if ret:
            result['status'] = True
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
        if ret:
            result['status'] = True
            models.UserInfo.objects.create(phone=registermobile, pwd=registerpwd)
            print(models.UserInfo.objects.filter(phone='17769040425').count())
        else:
            result['message'] = json.loads(obj.errors.as_json())

        return HttpResponse(json.dumps(result))



