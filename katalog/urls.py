from django.contrib import admin
from django.urls import path
from biblioteka.views import home, info

urlpatterns = [
    path('', views.home, name='home'),
    path('baza/', views.baza, name='baza'),
    path('info/', views.info, name='info'), 
]

