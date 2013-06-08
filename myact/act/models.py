#-*-coding:utf8-*-
from django.contrib.auth.models import User
from django.db import models
import datetime

# Create your models here.
choice_0=(
         ('m','man'),
         ('w','woman'),
)
class UserProfile(models.Model):
    user     = models.OneToOneField(User,unique=True)
    attention= models.ManyToManyField('Activity',verbose_name=u'关注',blank=True,null=True)
    join    = models.ManyToManyField('Activity',verbose_name=u'参加',related_name='user_join',blank=True,null=True)
    nickname = models.CharField(max_length=30)
    headImg  = models.FileField(upload_to='./')
    gender   = models.CharField(max_length=30,choices = choice_0)
    birthday = models.DateField(blank=True,null=True)
    last_time = models.DateTimeField(auto_now=True)
    sponsor  = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.user.username

    def att_num(self):
        return self.attention.count()
    def join_num(self):
        return self.join.count()
#class UserProfileInline(admin.StackedInline):
#    model = UserProfile
#    fk_name = 'user'
#    max_num = 1
#
#class UserProfileAdmin(admin.ModelAdmin):
#    inlines = [UserProfileInline,]
class Activity(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    icon = models.FileField(upload_to='./')
    st_time = models.DateTimeField()
    fi_time = models.DateTimeField()
    pub_time= models.DateTimeField(default=datetime.datetime.now())
    sponsor = models.CharField(max_length=30,null=True,blank=True)
    charge  = models.BooleanField(default=False)
    a_num   = models.IntegerField(default=0)
    j_num   = models.IntegerField(default=0)
    sort = models.ForeignKey("Sort") 
    tab = models.ManyToManyField("Tab") #标签与活动多对多
    
    def __unicode__(self):
        return self.title

class Sort(models.Model):
    sort = models.CharField(max_length=30)
    def __unicode__(self):
        return self.sort

class Tab(models.Model):
     tab = models.CharField(max_length=200)
     def __unicode__(self):
         return self.tab

class Review(models.Model):    
     content = models.TextField()
     re_pic  = models.FileField(upload_to='./')
     user = models.ForeignKey(User,verbose_name=u'u_review',related_name='user_reviews')
     activity = models.ForeignKey(Activity,verbose_name=u'act_review',related_name='act_reviews')
     






     
