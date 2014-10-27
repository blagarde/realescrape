from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'realescrape.views.home', name='home'),
    url(r'^list$', 'realescrape.views.adlisting', name='list'),
    url(r'^star$', 'realescrape.views.star', name='star'),
    url(r'^remove$', 'realescrape.views.remove', name='remove'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
