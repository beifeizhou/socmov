from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^/?$', 'djangonyc.exampleapp.views.index'),
    (r'^accounts/profile', 'djangonyc.exampleapp.views.profile'),
    (r'^xd_receiver\.html$', 'djangonyc.exampleapp.views.xd_receiver'),
    (r'^facebook/', include('facebookconnect.urls')),
)
