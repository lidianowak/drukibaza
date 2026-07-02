from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from biblioteka.views import home, baza, info

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("baza/", baza, name="baza"),
    path("info/", info, name="info"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

