from django.conf.urls import url
from . import views

app_name = 'main_app'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.RegFormView.as_view(), name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^user/(?P<user_id>[0-9]+)/settings/', views.UserSettingView.as_view(), name='user_settings'),
    
    url(r'^user/chat/index/$', views.user_message, name='user_message'),
    url(r'^user/message/add/$', views.MessageCreateView.as_view(), name='message_create'),
    url(r'^user/chat/(?P<chat_id>[0-9]+)/$', views.UserChat.as_view(), name='user_chat'),
   # url(r'^post/$', views.post, name='post'),
    #url(r'^messages/$', views.post_messages, name='messages'),
    
    url(r'^user/report/add/$', views.ReportCreate.as_view(), name='report_create'),
    url(r'^user/reports/', views.UserReportView.as_view(), name='user_reports'),
    url(r'^user/report/(?P<pk>[0-9]+)/$', views.UserReportDetailView.as_view(), name='user_report_detail'),
    url(r'^user/report/generate/(?P<pk>[0-9]+)/$', views.report_pdf, name='report_generate'),
    url(r'^reports/search_report/$', views.AllSearchReportView.as_view(), name='all_search_report'),
    url(r'^reports/found_report/$', views.AllFoundReportView.as_view(), name='all_found_report'),
    url(r'^reports/gift_report/$', views.AllGiftReportView.as_view(), name='all_gift_report'),
    url(r'^reports/shelter_report/$', views.AllShelterReportView.as_view(), name='all_shelter_report'),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetailView.as_view(), name='user_page'),
    url(r'^about/$', views.about, name='about_us'),
    url(r'^volunteer/$', views.volunteer, name='volunteer'),
]
