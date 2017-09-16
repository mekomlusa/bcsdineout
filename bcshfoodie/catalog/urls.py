from django.conf.urls import url
from django.contrib import admin


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


urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^restaurants/$', views.RestaurantListView.as_view(), name='restaurants'),
        url(r'^randall/$', views.RestaurantRandomView.as_view(), name='restaurant-random'),
        url(r'^restaurant/(?P<stub>[-\w ]+)$', views.RestaurantDetailView.as_view(), name='restaurant-detail'),
]