from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'southwest.views.home', name='home'),
    url(r'^southwest-checkin/', include('sw_checkin.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
