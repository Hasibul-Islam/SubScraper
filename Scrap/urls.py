from django.conf.urls import url, include
from django.urls import path
from django.conf import settings
# from django.contrib import admin
from Scrap import views
from django.conf.urls.static import static
urlpatterns = [

    url('', views.scrap),
    

]