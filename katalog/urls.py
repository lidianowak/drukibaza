from django.contrib import admin
from django.urls import path
from biblioteka.views import home, baza, info

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('baza/', baza, name='baza'),
    path('info/', info, name='info'),
]

