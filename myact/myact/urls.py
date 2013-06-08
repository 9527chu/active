from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import settings


urlpatterns = patterns('',
    url( r'^static/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root': settings.STATIC_ROOT }),  
    # Examples:
    # url(r'^$', 'myact.views.home', name='home'),
    # url(r'^myact/', include('myact.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^regist/$','act.views.regist'),
    url(r'^ulogin/$','act.views.ulogin'),
    url(r'^ulogout/$','act.views.ulogout'),
    url(r'^cr_act/$','act.views.cr_act'),
    url(r'^xiu_psw/$','act.views.xiu_psw'),
    url(r'^my_home/$','act.views.my_home'),
    url(r'^review/(\d+)/$','act.views.review'),
    url(r'^show_content/(\d+)/$','act.views.show_content'),
    url(r'^show_act/$','act.views.show_act'),
    url(r'^show_act1/(\d+)/$','act.views.show_act1'),


    url(r'^attention','act.views.attention'),
    url(r'^u_att','act.views.u_att'),
    
    url(r'^join','act.views.join'),
    url(r'^u_join','act.views.u_join'),
   
        
    url(r'^search','act.views.search'),
    url(r'^show_sort/sort/$','act.views.sort'),
       






   
    url(r'^home/(\d+)/$','act.views.home'),
    
    url(r'^home/$','act.views.home'),
)




urlpatterns += staticfiles_urlpatterns()    
