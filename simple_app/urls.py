"""simple_app URL Configuration."""
from django.conf.urls import include, url
from django.contrib import admin

from simple_app.restapi.views import DomainView, DomainsView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/(?P<pk>[a-zA-Z0-9]+)$', DomainView.as_view(), name='domain'),
    url(r'^api/$', DomainsView.as_view(), name='domains'),
]
