from django.conf.urls import url

from sw_checkin import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^email/', views.email_view, name='email'),
    url(r'^name/(?P<passenger_id>\d+)/$', views.name_view, name='passenger_name'),
    url(r'^reservation/(?P<passenger_id>\d+)/$', views.reservation_view, name='reservation'),
    url(r'^success/(?P<reservation_id>\d+)/$', views.success_view, name='success')
]