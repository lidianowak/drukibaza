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

