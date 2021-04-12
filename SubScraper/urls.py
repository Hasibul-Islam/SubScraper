from django.conf.urls import url, include
from django.urls import path
from django.conf import settings
# from django.contrib import admin
from django.conf.urls.static import static
urlpatterns = [

    # url('admin/', admin.site.urls),
    # url(r'^$', views.home, name='index'),
    url('', include('Scrap.urls')),
    # url('auth/', include('user.urls')),
    # url('campaign/', include('campaign.urls')),
    # path('', views.home, name='home')

]