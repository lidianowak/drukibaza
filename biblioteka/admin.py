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
    WersjaZdigitalizowana,
    RelacjaRekordu,
    RelacjaOsoby,
    RelacjaMiejsca,
    RelacjaInstytucji,
    RelacjaTematu,
    RelacjaGatunku,
    RelacjaWydarzenia,
    RelacjaMotywu,
    Egzemplarz,
    OpracowanieRekordu,
    Tag,
)

from .forms import RekordForm

MODELE = [
    Jezyk,
    Format,
    Czcionka,
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

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = [
        "nazwa",
    ]

@admin.register(Biblioteka)
class BibliotekaAdmin(admin.ModelAdmin):
    search_fields = [
        "nazwa",
    ]

class RelacjaRekorduInline(admin.TabularInline):
    model = RelacjaRekordu
    fk_name = "rekord"
    extra = 1
    autocomplete_fields = ["rekord_powiazany"]

class WersjaZdigitalizowanaInline(admin.TabularInline):
    model = WersjaZdigitalizowana
    extra = 0

class EgzemplarzInline(admin.StackedInline):
    model = Egzemplarz
    extra = 0
    autocomplete_fields = ["biblioteka"]

class OpracowanieRekorduInline(admin.StackedInline):
    model = OpracowanieRekordu
    extra = 0
    autocomplete_fields = ["uzytkownik"]


@admin.register(Rekord)
class RekordAdmin(admin.ModelAdmin):
    form = RekordForm

    readonly_fields = [
        "identyfikator",
        "data_dodania",
        "data_ostatniej_modyfikacji",
    ]

    fieldsets = (
    ("Informacje podstawowe", {
        "fields": (
            "miniatura",
            "autor",
            "tytul_skrocony",
            "tytul_pelny",
            "rok_wydania",
            "miejsce_wydania",
            "drukarz",
            "jezyki",
        )
    }),
    ("Opis fizyczny", {
        "fields": (
            "format",
            "liczba_arkuszy",
            "liczba_kart",
            "kolacjonowanie",
            "czcionki",
            "ozdobniki",
            "ryciny",
            "uwagi",
        )
    }),
    ("Powiązania", {
        "fields": (
            "adresat_dedykacji",
            "powiazane_osoby",
            "instytucje",
            "powiazane_miejsca",
            "tematy",
            "gatunki",
            "wydarzenia",
            "warianty",
            "wznowienia",
            "pozostale_druki_powiazane",
            "literatura_przedmiotu",
            "bibliografie",
            "streszczenie",
            "motywy",
        )
    }),
    ("Metadane", {
        "fields": (
            "status_opracowania",
            "tagi",
            "data_dodania",
            "data_ostatniej_modyfikacji",
        )
    }),
)

    inlines = [
        WersjaZdigitalizowanaInline,
        EgzemplarzInline,
        OpracowanieRekorduInline,
]

    search_fields = [
        "identyfikator",
        "tytul_skrocony",
        "tytul_pelny",
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        istnieje = OpracowanieRekordu.objects.filter(
            rekord=obj,
            uzytkownik=request.user
        ).exists()

        if not istnieje:
            ostatnia = OpracowanieRekordu.objects.filter(
                rekord=obj
            ).count()

            OpracowanieRekordu.objects.create(
                rekord=obj,
                uzytkownik=request.user,
                sposob_dodania="auto",
                kolejnosc=ostatnia + 1
            )


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

@admin.register(Egzemplarz)
class EgzemplarzAdmin(admin.ModelAdmin):
    autocomplete_fields = ["rekord", "biblioteka"]

    search_fields = [
        "rekord__identyfikator",
        "sygnatura",
        "biblioteka__nazwa",
    ]

@admin.register(OpracowanieRekordu)
class OpracowanieRekorduAdmin(admin.ModelAdmin):
    autocomplete_fields = ["rekord", "uzytkownik"]

    search_fields = [
        "rekord__identyfikator",
        "uzytkownik__username",
        "uzytkownik__first_name",
        "uzytkownik__last_name",
        "imie_nazwisko",
    ]

@admin.register(WersjaZdigitalizowana)
class WersjaZdigitalizowanaAdmin(admin.ModelAdmin):
    autocomplete_fields = ["rekord"]

    search_fields = [
        "rekord__identyfikator",
        "link",
    ]