from django.contrib import admin
from django.urls import path
from biblioteka.autocomplete import (
    OsobaAutocomplete,
    MiejsceAutocomplete,
    InstytucjaAutocomplete,
    TematAutocomplete,
    GatunekAutocomplete,
    WydarzenieAutocomplete,
    MotywAutocomplete,
    RekordAutocomplete,
    TagAutocomplete,
)
from django.conf import settings
from django.conf.urls.static import static

from biblioteka.views import home, baza, info

urlpatterns = [
    path("admin/", admin.site.urls),

    path("autocomplete/osoba/", OsobaAutocomplete.as_view(), name="osoba-autocomplete"),
    path("autocomplete/miejsce/", MiejsceAutocomplete.as_view(), name="miejsce-autocomplete"),
    path("autocomplete/instytucja/", InstytucjaAutocomplete.as_view(), name="instytucja-autocomplete"),
    path("autocomplete/temat/", TematAutocomplete.as_view(), name="temat-autocomplete"),
    path("autocomplete/gatunek/", GatunekAutocomplete.as_view(), name="gatunek-autocomplete"),
    path("autocomplete/wydarzenie/", WydarzenieAutocomplete.as_view(), name="wydarzenie-autocomplete"),
    path("autocomplete/motyw/", MotywAutocomplete.as_view(), name="motyw-autocomplete"),
    path("autocomplete/rekord/", RekordAutocomplete.as_view(), name="rekord-autocomplete"),

    path("", home, name="home"),
    path("baza/", baza, name="baza"),
    path("info/", info, name="info"),
    path(
    "autocomplete/tag/",
    TagAutocomplete.as_view(),
    name="tag-autocomplete",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

