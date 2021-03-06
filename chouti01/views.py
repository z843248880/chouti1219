from django.shortcuts import render,HttpResponse,redirect

# Create your views here.

from django import forms
import json,re,time,datetime
import collections

from datetime import date


from chouti01 import models
from django.forms.utils import ErrorDict
from django.core.exceptions import ValidationError
from backend import sendMsg, commons, randomcode,pager
from django.db.models import F




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

comment_dic = {}

@auth
def index(request):
    if request.method == 'GET':
        current_page = request.GET.get('page','1')
        print('current_page:',current_page)
        all_pages = models.News.objects.all().count()
        page_obj = pager.Pagination(current_page,all_pages)
        global logineduser
        user = request.session.get('user_info')['username']

        sql = """
                SELECT
                    "chouti01_news"."nid",
                    "chouti01_news"."title",
                    "chouti01_news"."url",
                    "chouti01_news"."content",
                    "chouti01_news"."ctime",
                    "chouti01_userinfo"."username",
                    "chouti01_newstype"."caption",
                    "chouti01_news"."favor_count",
                    "chouti01_news"."comment_count",
                    "chouti01_favor"."nid"
                FROM
                    "chouti01_news"
                LEFT OUTER JOIN "chouti01_userinfo" ON (
                    "chouti01_news"."user_info_id" = "chouti01_userinfo"."nid"
                )
                LEFT OUTER JOIN "chouti01_newstype" ON (
                    "chouti01_news"."news_type_id" = "chouti01_newstype"."nid"
                )
                LEFT OUTER JOIN "chouti01_favor" ON (
                    "chouti01_news"."nid" = "chouti01_favor"."news_id"
                    and
                    "chouti01_news".user_info_id = %s
                )
                ORDER BY "chouti01_news"."nid" DESC
                LIMIT 10 OFFSET %s

                """
        # for i in range(14,100):
        #     bt = 'biaoti' + str(i)
        #     lj = 'lianjie' + str(i)
        #     zy = 'zhaiyao' + str(i)
        #     ct = datetime.datetime.now()
        #     uid = 10
        #     ntid = 3
        #
        #     models.News.objects.create(user_info_id=uid,news_type_id=ntid,title=bt,url=lj,content=zy,ctime=ct)

        from django.db import connection
        cursor = connection.cursor()
        current_login_user_nid = request.session['user_info']['nid']
        str_page = page_obj.string_pager('/index/')
        print(page_obj.start)
        cursor.execute(sql,[current_login_user_nid,page_obj.start])
        newsret = cursor.fetchall()
        if not user:
            phoneuser = request.session.get('user_info')['phone']
            return render(request, 'index.html', {'logineduser': phoneuser,'newsitems':newsret,'str_page':str_page})
        return render(request, 'index.html', {'logineduser': user,'newsitems':newsret,'str_page':str_page})

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


def favor(request):
    if request.method == 'POST':
        ret = commons.BaseResponse()
        news_get_id = request.POST.get('news_id')
        user_get_id = request.session.get('user_info')['nid']

        favor_user_news_conut = models.Favor.objects.filter(user_info_id=user_get_id,news_id=news_get_id).count()
        if favor_user_news_conut:
            models.Favor.objects.filter(user_info_id=user_get_id,news_id=news_get_id).delete()
            models.News.objects.filter(nid=news_get_id).update(favor_count=F('favor_count') - 1)

            ret.code = commons.StatusCodeEnum.FavorMinus
        else:
            current_time = datetime.datetime.now()
            models.Favor.objects.create(user_info_id=user_get_id,news_id=news_get_id,ctime=current_time)
            models.News.objects.filter(nid=news_get_id).update(favor_count=F('favor_count') + 1)

            ret.code = commons.StatusCodeEnum.FavorPlus
        ret.status = True
        return HttpResponse(json.dumps(ret.__dict__))

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        #if isinstance(obj, datetime):
            #return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)

### comment tree   标准的json格式，带键值的
# icount = 1
# def tree_search(d_dic, comment_obj):
#     for k, v in d_dic.items():
#         if v['name'][0] == comment_obj[5]:
#             d_dic[k]['val'] = collections.OrderedDict()
#             d_dic[k]['val']['name'] = comment_obj
#             d_dic[k]['val']['val'] = collections.OrderedDict()
#             return
#         else:
#             if v['val']:
#                 tree_search(d_dic[k]['val'], comment_obj)
#
#
# def build_tree(comment_list):
#     global icount
#     comment_dic = collections.OrderedDict()
#     for comment_obj in comment_list:
#         # print('funck?:',type(str(comment_obj[5])),'_________-',comment_obj[5])
#         if comment_obj[5] == 'None':
#             comment_dic['dict' + str(icount)] = collections.OrderedDict()
#             comment_dic['dict' + str(icount)]['name'] = comment_obj
#             comment_dic['dict' + str(icount)]['val'] = collections.OrderedDict()
#             icount += 1
#         else:
#             tree_search(comment_dic, comment_obj)
#     return comment_dic

def tree_search(d_dic, comment_obj):
    for k, v_dic in d_dic.items():
        # print(k)
        # print('----------------: ',str(k[0]),'  &  ',comment_obj[5])
        if str(k.strip('()').split(',')[0]) == comment_obj[5]:
            d_dic[k][str(comment_obj)] = collections.OrderedDict()
            return
        else:
            if v_dic:
                tree_search(d_dic[k], comment_obj)


def build_tree(comment_list):
    comment_dic = collections.OrderedDict()
    for comment_obj in comment_list:
        # print('funck?:',type(str(comment_obj[5])),'_________-',comment_obj[5])
        if str(comment_obj[5]) == 'None':
            comment_dic[str(comment_obj)] = collections.OrderedDict()
        else:
            tree_search(comment_dic, comment_obj)
    return comment_dic

def content(request):
    ret = commons.BaseResponse()
    if request.method == 'POST':
        # models.Comment.objects.filter(nid__lt=10).delete()
        news_get_id = request.POST.get('news_id')
        user_get_id = request.session.get('user_info')['nid']
        contentneirong = request.POST.get('contentneirong')
        replyid = request.POST.get('replyid')
        # current_time = datetime.datetime.now()
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        models.Comment.objects.create(user_info_id=user_get_id,news_id=news_get_id,ctime=current_time,content=contentneirong,reply_id=replyid)
        models.News.objects.filter(nid=news_get_id).update(comment_count=F('comment_count') + 1)
        ret.status = True
        return HttpResponse(json.dumps(ret.__dict__))
    elif request.method == 'GET':
        global comment_dic
        news_get_id = request.GET.get('news_id')
        print('enwid:', news_get_id)
        sql = """
            SELECT
                "chouti01_comment"."nid",
                "chouti01_comment"."content",
                "chouti01_userinfo"."nid",
                "chouti01_news"."comment_count",
                "chouti01_comment"."ctime",
                "chouti01_comment"."reply_id",
                "chouti01_news"."nid"
            FROM
                "chouti01_comment"
            LEFT OUTER JOIN "chouti01_userinfo" ON (
                "chouti01_comment"."user_info_id" = "chouti01_userinfo"."nid"
            )
            LEFT OUTER JOIN "chouti01_news" ON (
                "chouti01_comment"."news_id" = "chouti01_news"."nid"
            )
            WHERE
                "chouti01_comment"."news_id" = %s
            """

        from django.db import connection
        cursor = connection.cursor()

        cursor.execute(sql,[news_get_id,])
        contentret = cursor.fetchall()
        print('rr11:',contentret)
        contentret_new = build_tree(contentret)
        ret.status = True
        ret.summary = contentret_new
        print('retttttttttttttttttttttt:',ret.summary)
        # for k,v in ret.summary.items():
        #     print('-----------------')
        #     print(type(k))
        #     print(type(v),'\n')
        # print('ret.summary,',ret.summary)
        # print(contentret_new)
        return HttpResponse(json.dumps(ret.__dict__,cls=CJsonEncoder))

def searchtable(request):
    if request.method == 'GET':
        models.Comment.objects.filter(nid__in=[23,24]).delete()
        a = models.Comment.objects.values_list('nid','content','reply_id')
        print(a)
        return HttpResponse(None)


def abctest(request):
    return render(request,'abctest.html')









