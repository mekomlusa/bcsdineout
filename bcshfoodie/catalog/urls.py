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

from django.contrib.auth.decorators import login_required
 
from . import views

from .models import BookmarkRestaurant

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^restaurants/$', views.RestaurantListView.as_view(), name='restaurants'),
        url(r'^randall/$', views.RestaurantRandomView.as_view(), name='restaurant-random'),
        url(r'^restaurant/(?P<stub>[-\w ]+)$', views.RestaurantDetailView.as_view(), name='restaurant-detail'),
        url(r'^categories/$', views.CategoryListView.as_view(), name='categories'),
        url(r'^category/(?P<stub>[-\w ]+)/$', views.CategoryList2View.as_view(), name='category-list-2'),
        url(r'^myfavres/$', views.FavByUserListView.as_view(), name='my-fav-res'),
]

#app_name = 'ajax'
urlpatterns += [
    url(r'^restaurant/(?P<pk>[-\w ]+)/addbookmark/$',
        login_required(views.AddBookmarkView.as_view(model=BookmarkRestaurant)),
        name='restaurant_bookmark'),
    url(r'^restaurant/(?P<pk>[-\w ]+)/rmbookmark/$',
        login_required(views.RmBookmarkView.as_view(model=BookmarkRestaurant)),
        name='rm_restaurant_bookmark'),
    url(r'^restaurant/(?P<pk>[-\w ]+)/addnote/$',
        login_required(views.addNote), name='restaurant_note'),
    url(r'^restaurant/(?P<pk>[-\w ]+)/updatenote/$',
        login_required(views.updateNote), name='restaurant_note_update'),
    url(r'^restaurant/(?P<pk>[-\w ]+)/deletenote/$',
        login_required(views.deleteNote), name='restaurant_note_delete'),
    url(r'^community/$',
        login_required(views.CommunityView.as_view()), name='community'),
]