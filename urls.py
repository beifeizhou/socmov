from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	(r'^$', 'fbcon.views.index'),
	(r'^login/$', 'fbcon.views.login'),
	(r'^show/$', 'fbcon.views.show'),
	(r'^movie/$', 'fbcon.views.detail_mov'),
	(r'^userprofile/$', 'fbcon.views.profile_user'),
	(r'^cmovie/$', 'fbcon.views.compact_mov'),
	(r'^vote/$', 'fbcon.views.vote'),
    # Examples:
    # url(r'^$', 'socmov.views.home', name='home'),
    # url(r'^socmov/', include('socmov.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
if settings.LOCAL_MEDIA:
	urlpatterns += patterns( '' ,
     (r'^media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root' : settings.MEDIA_ROOT }), )
