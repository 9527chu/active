# Create your views here.
#coding:utf8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from act.models import *
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
import random
import re

users = User.objects.all()
def validate0(value):
     for user in users:
         if value == user.username:
             raise forms.ValidationError('用户名已经存在')

def validate1(value):
    p = re.compile('w+')
    pa = p.match(value)
    if pa is None:
       raise forms.ValidationError('密码以字母，数字，下划线组成')

class UserForm(forms.Form):
    username = forms.CharField(label=u'用户名',error_messages={'required':'请输入帐号'})
    password = forms.CharField(widget = forms.PasswordInput,label=u'密码',error_messages={'required':'请输入帐号'})
    re_password = forms.CharField(widget = forms.PasswordInput, label = '确认密码', error_messages={'required':'请再次输入密码'})
    email    = forms.EmailField(label=u'邮箱',error_messages={'required':'请输入邮箱'})
    nickname = forms.CharField(label=u'昵称',error_messages={'required':'请输入名字'})
    gender   = forms.ChoiceField(choices=(('m','man'),('w','women')),label=u'性别')
    birthday = forms.DateField(label=u'出生日期',error_messages={'required':'请输入出生日期'})
    headImg  = forms.FileField(label=u'头像',error_messages={'required':'请输入出生日期'})
    def va_password(self):
        if 'password' in self.cleaned_data:
            password0 = self.cleaned_data['password']
            password1 = self.cleaned_data['re_password']
        if password0 == password1:
            return password1
        raise ValidationError('两次密码不一致') 

class LogForm(forms.Form):
    username = forms.CharField(label=u'用户名')
    password = forms.CharField(widget = forms.PasswordInput,label=u'密码')

class CrForm(forms.Form):
    title = forms.CharField(label=u'主题')
    content = forms.CharField(label=u'内容',widget=forms.Textarea)
    icon    = forms.FileField(label=u'图片')
    pub_time= forms.DateField(label=u'发布时间')
    st_time = forms.DateField(label=u'开始时间')
    fi_time = forms.DateField(label=u'结束时间')
    tab     = forms.CharField(label=u'活动标签')
    charge  = forms.BooleanField(label=u'是否收费')

class GForm(forms.Form):
    username = forms.CharField(label=u'用户名')
    password = forms.CharField(label=u'旧密码',widget= forms.PasswordInput)
    newpassword = forms.CharField(label=u'新密码',widget= forms.PasswordInput)
    ren_password= forms.CharField(label=u'再次出入新密码',widget=forms.PasswordInput)

class ReForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea,label='内容')

    re_pic  = forms.FileField()


class SForm(forms.Form):
    title  = forms.CharField(required=False)
    #sort   = forms.CharField(required=False)
def regist(request):
    if request.method == 'POST':
        uf = UserForm(request.POST,request.FILES)
        if uf.is_valid():
           
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            re_password = uf.cleaned_data['re_password']
            email = uf.cleaned_data['email']
            nickname = uf.cleaned_data['nickname']
            gender = uf.cleaned_data['gender']
            birthday = uf.cleaned_data['birthday']
            headImg  = uf.cleaned_data['headImg']
            user = User.objects.create_user(username=username,password=password,email=email)
            UF=UserProfile.objects.create(user=user,nickname=nickname,gender=gender,headImg=headImg)
                   
           # username = request.POST.get('username')
           # if username in User.objects.all():
           #     return '用户名已经存在'
           # else:
           #     return '用户名可用' 
           # return render_to_response('regist.html',locals())
            return HttpResponseRedirect('/ulogin/')
    else:
        uf = UserForm()
    return render_to_response('regist.html',locals())


def ulogin(request):
    if request.method == 'POST':
        lf = LogForm(request.POST)
        if lf.is_valid():
            username = lf.cleaned_data['username']
            password = lf.cleaned_data['password']

            user = authenticate(username=username,password=password)
            
            if user :
                if user in users:
                    login(request,user)
                    return HttpResponseRedirect('/my_home/')
                else:
                    return HttpResponse("用户名不存在，请<a href='/regist/'>注册</a>")
            else:
                 return HttpResponse("用户名或密码不正确，请重新<a href='/ulogin/'>登录</a>")
            
    else:
        lf = LogForm()
    return render_to_response('ulogin.html',locals())

def ulogout(request):
    logout(request)
    return HttpResponseRedirect('/ulogin/')

def home(request,id=None):
    acts = Activity.objects.all()
    for act in acts:
        a_num = act.a_num
    act_list = Activity.objects.order_by('-a_num')[0:3]
    return render_to_response('home.html',locals())
#@login_required('/ulogin/')
def cr_act(request):
    sorts = Sort.objects.all()
    
    user = request.user
    if request.user.is_authenticated():
        if request.method == 'POST':

         #if request.user.get_profile().sponsor == True:
                cf = CrForm(request.POST,request.FILES)
                if cf.is_valid():
                    title = cf.cleaned_data['title']
                    content = cf.cleaned_data['content']
                    icon = cf.cleaned_data['icon']
                    pub_time = cf.cleaned_data['pub_time']
                    st_time = cf.cleaned_data['st_time']
                    fi_time = cf.cleaned_data['fi_time']
                    charge  = cf.cleaned_data['charge']
                    sort = request.POST['sort']
                    sort = Sort.objects.get(sort=sort)
                   # sort    = cf.cleaned_data['sort']
                   # sort    = Sort.objects.create(sort=sort)
                    act = Activity.objects.create(title=title,content=content,icon=icon,pub_time=pub_time,st_time=st_time,fi_time=fi_time,charge=charge,sort=sort)
                    tab  = request.POST['tab']
                    tab = Tab.objects.create(tab=tab)
                    act.tab.add(tab)
                   # tact = Activity.objects.get(title=title)
                   # tab = request.POST['tab']

                   # tact.tab.add(tab)
                   # tact.save()
                    return HttpResponseRedirect('/show_act/')
        else:
            cf = CrForm()
    else:
        return HttpResponseRedirect('/ulogin/')
    return render_to_response('cf_act.html',locals())
def show_act(request):
    acts = Activity.objects.all()
    paginator = Paginator(acts, 3) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        acts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        acts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        acts = paginator.page(paginator.num_pages)

    return render_to_response('show_act.html', {"acts": acts})

    for act in acts:
        if act.charge == True:
            act.charge == '收费'
        elif act.charge == False:
            act.charge == '免费'
   # tab = Tab()
   # tab  = Tab.activity_set.all()
   # for act in acts:
   #    id = act.id
       
       
    return  render_to_response('show_act.html',locals())

#@login_required('/ulogin/')
def xiu_psw(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            gf = GForm(request.POST)
            if gf.is_valid():
                username = gf.cleaned_data['username']
                password = gf.cleaned_data['password']
                newpassword = gf.cleaned_data['newpassword']
                ren_password = gf.cleaned_data['ren_password']
                user = authenticate(username=username,password=password)
                if user is None:
                    return HttpResponse('原密码错误')
                else:
                    user.set_password(newpassword)
                    user.save()
                    return HttpResponseRedirect('/ulogin/')
        else:
            gf = GForm()
    else:
        return HttpResponseRedirect('/ulogin/')
    return render_to_response('xiu_psw.html',locals())



def my_home(request):
    if request.user.is_authenticated():
        user = request.user
        if user.is_anonymous():
            user.nickname = '游客'
        else:
            user.nickname = user.get_profile().nickname
        show_acts=[]
        acts = Activity.objects.all()
        for var in range(3):
             act = random.choice(acts)
             if act not in show_acts:
                 show_acts.append(act)
    else:
        return HttpResponseRedirect('/ulogin/')
    return render_to_response('my_home.html',locals())


def review(request,a_id):
    if request.user.is_authenticated():
        re_time = datetime.datetime.now()
        act = Activity.objects.get(id=a_id)
        if request.method == "POST":
            rf = ReForm(request.POST,request.FILES)
            if rf.is_valid():
                content = rf.cleaned_data['content']

                re_pic  = rf.cleaned_data['re_pic']
                rev = Review.objects.create(user=request.user,activity=act,content=content,re_pic=re_pic)
                return HttpResponseRedirect('/show_content/%s'%a_id )
        else:
            rf = ReForm()
    else:
        return HttpResponseRedirect('/ulogin/')
    return render_to_response('review.html',locals())

def show_content(request,id):
    re_time = datetime.datetime.now()
    user = request.user
    act = Activity.objects.get(id=id)
    reviews = Review.objects.all()
    return render_to_response('show_content.html',locals())

def show_act1(request,id):
    act = Activity.objects.get(id=id)
    return render_to_response('show_act1.html',locals())

def attention(request):
    aid = request.GET.get('id','')
    act = Activity.objects.get(id=aid)
    user = UserProfile.objects.get(user=request.user)
    if act not in user.attention.all():
        user.attention.add(act)
        act.a_num += 1
        act.save()
    
    return HttpResponseRedirect('%s' % request.META.get('HTTP_REFERER',"/"))
def u_att(request):
    aid = request.GET.get('id','')
    act = Activity.objects.get(id=aid)
    user = UserProfile.objects.get(user=request.user)
    if act in user.attention.all():
        user.attention.remove(act)
        act.a_num -= 1
        act.save()
    return HttpResponseRedirect('%s' % request.META.get('HTTP_REFERER',"/"))


def join(request):
    aid = request.GET.get('id','')
    act = Activity.objects.get(id=aid)
    user = UserProfile.objects.get(user=request.user)
    
   # u_num= u_num.join.all().count()
    if act not in user.join.all():
        user.join.add(act)
        act.j_num += 1
        act.save()
    return HttpResponseRedirect('%s' % request.META.get('HTTP_REFERER',"/"))

def u_join(request):
    aid = request.GET.get('id','')
    act = Activity.objects.get(id=aid)
    user = UserProfile.objects.get(user=request.user)
    if act in user.join.all():
        user.join.remove(act)
        act.j_num -= 1
        act.save()
    return HttpResponseRedirect('%s' % request.META.get('HTTP_REFERER',"/"))

def search(request):
    if request.method == 'POST':
        sf = SForm(request.POST)
        if sf.is_valid():
            title = request.POST.get('title','')
           # sort  = request.POST.get('sort','')
            title = sf.cleaned_data['title']
           # sort  = Sort.objects.get(sort=sort)
            acts = Activity.objects.filter(title__icontains=title).order_by('-id')
           # sacts= Activity.objects.filter(sort=sort)
            return render_to_response('search.html',locals())
    else:
        sf = SForm()
    return render_to_response('search.html',locals())

def sort(request):
   sorts = Sort.objects.all()
   sort  = request.GET.get('sort','')
   if sort == 'all':
        sacts = Activity.objects.all()
   else:
        sort  = Sort.objects.get(sort=sort)
        sacts = Activity.objects.filter(sort=sort)
    
     # acts = Activity.objects.filter(sort__icontains=sort).order_by('-id')
   return render_to_response('show_sort.html',locals())

