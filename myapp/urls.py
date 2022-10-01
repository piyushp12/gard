from django.contrib import admin
from django.urls import path,include
from myapp.views import *


urlpatterns = [
    path('',LoginView.as_view(),name="home"),
    path('index/',HomeView.as_view(),name="index"),
    path('detailview/<int:id>',DetailView.as_view(),name="detailview"),
    path('toggle/',Toggle.as_view(),name="toggle"),
    path('api/',DeviceAPi.as_view(), name="api"),
    path('outapi/',DeviceOutAPI.as_view(),name="outapi"),
]
