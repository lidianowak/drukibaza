from django.contrib import admin
from .models import (
    Jezyk,
    Format,
    Czcionka,
    Osoba,
    Miejsce,
    Instytucja,
    Biblioteka,
    Wydarzenie,
    Gatunek,
    Motyw,
    Temat,
    Rekord,
    RelacjaRekordu,
    RelacjaOsoby,
    RelacjaMiejsca,
    RelacjaInstytucji,
    RelacjaTematu,
    RelacjaGatunku,
    RelacjaWydarzenia,
    RelacjaMotywu,
)

from .forms import RekordForm

MODELE = [
    Jezyk,
    Format,
    Czcionka,
    Biblioteka,
]

for model in MODELE:
    admin.site.register(model)


@admin.register(Miejsce)
class MiejsceAdmin(admin.ModelAdmin):
    search_fields = [
        "nazwa",
    ]


@admin.register(Osoba)
class OsobaAdmin(admin.ModelAdmin):
    search_fields = [
        "nazwisko",
        "imiona",
    ]


@admin.register(Instytucja)
class InstytucjaAdmin(admin.ModelAdmin):
    search_fields = [
        "nazwa",
    ]


@admin.register(Temat)
class TematAdmin(admin.ModelAdmin):
    search_fields = [
        "nazwa",
    ]


@admin.register(Gatunek)
class GatunekAdmin(admin.ModelAdmin):
    search_fields = [
        "nazwa",
    ]


@admin.register(Wydarzenie)
class WydarzenieAdmin(admin.ModelAdmin):
    search_fields = [
        "nazwa",
    ]


@admin.register(Motyw)
class MotywAdmin(admin.ModelAdmin):
    search_fields = [
        "nazwa",
    ]


class RelacjaRekorduInline(admin.TabularInline):
    model = RelacjaRekordu
    fk_name = "rekord"
    extra = 1
    autocomplete_fields = ["rekord_powiazany"]


@admin.register(Rekord)
class RekordAdmin(admin.ModelAdmin):
    form = RekordForm
    inlines = [RelacjaRekorduInline]

    search_fields = [
        "identyfikator",
        "tytul_skrocony",
        "tytul_pelny",
    ]


@admin.register(RelacjaRekordu)
class RelacjaRekorduAdmin(admin.ModelAdmin):
    autocomplete_fields = ["rekord", "rekord_powiazany"]


@admin.register(RelacjaOsoby)
class RelacjaOsobyAdmin(admin.ModelAdmin):
    autocomplete_fields = ["rekord", "osoba"]


@admin.register(RelacjaMiejsca)
class RelacjaMiejscaAdmin(admin.ModelAdmin):
    autocomplete_fields = ["rekord", "miejsce"]


@admin.register(RelacjaInstytucji)
class RelacjaInstytucjiAdmin(admin.ModelAdmin):
    autocomplete_fields = ["rekord", "instytucja"]


@admin.register(RelacjaTematu)
class RelacjaTematuAdmin(admin.ModelAdmin):
    autocomplete_fields = ["rekord", "temat"]


@admin.register(RelacjaGatunku)
class RelacjaGatunkuAdmin(admin.ModelAdmin):
    autocomplete_fields = ["rekord", "gatunek"]


@admin.register(RelacjaWydarzenia)
class RelacjaWydarzeniaAdmin(admin.ModelAdmin):
    autocomplete_fields = ["rekord", "wydarzenie"]


@admin.register(RelacjaMotywu)
class RelacjaMotywuAdmin(admin.ModelAdmin):
    autocomplete_fields = ["rekord", "motyw"]

