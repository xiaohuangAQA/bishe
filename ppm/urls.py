# -- coding: utf-8 --
# author : TangQiang
# time   : 2024/4/7
# email  : tangqiang.0701@gmail.com
# file   : urls.py

from django.urls import path
from . import views
app_name = 'ppm'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.HomeSearch.as_view(), name='search'),
    path('statistics/', views.statistics, name='statistics'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('document/', views.document, name='document'),
    path('browse/', views.BrowseView.as_view(), name='browse'),
    path('more/', views.showMore.as_view(), name='more'),
    #path('more/<type>/<id>', views.more, name='more'),
    path('disease/<str:sid>/', views.show_disease, name='show_disease'),
]