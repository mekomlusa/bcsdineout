from django.conf.urls import url
from django.contrib import admin
import os


urlpatterns = [
    url(r'^admin/', admin.site.urls),
]

# Use include() to add URLS from the catalog application 
from django.conf.urls import include

urlpatterns += [
    url(r'^catalog/', include('catalog.urls')),
]

#Add URL maps to redirect the base URL to our application
from django.views.generic import RedirectView
urlpatterns += [
    url(r'^$', RedirectView.as_view(url='/catalog/', permanent=True)),
]

from django.conf.urls import url

from catalog import views


urlpatterns += [
        url(r'^$', views.index, name='index'),

]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^signup/$', views.signup, name='user-signup'),
    url(r'^search-form/$', views.search_form, name='search'),
    url(r'^search/$', views.search2, name='result'),
    
]

# to serve static files with DEBUG closed
if settings.DEBUG is False:  
    urlpatterns += patterns('',
            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )