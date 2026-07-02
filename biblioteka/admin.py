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
)

MODELE = [
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
]

for model in MODELE:
    admin.site.register(model)

class RelacjaRekorduInline(admin.TabularInline):
    model = RelacjaRekordu
    fk_name = "rekord"
    extra = 1
    autocomplete_fields = ["rekord_powiazany"]


@admin.register(Rekord)
class RekordAdmin(admin.ModelAdmin):
    inlines = [RelacjaRekorduInline]

    search_fields = [
        "identyfikator",
        "tytul_skrocony",
        "tytul_pelny",
    ]

@admin.register(RelacjaRekordu)
class RelacjaRekorduAdmin(admin.ModelAdmin):
    autocomplete_fields = ["rekord", "rekord_powiazany"]

