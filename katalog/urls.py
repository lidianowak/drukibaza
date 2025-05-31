from django.contrib import admin
from django.urls import path
from biblioteka.views import home, info

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('info/', info, name='info'),
]

